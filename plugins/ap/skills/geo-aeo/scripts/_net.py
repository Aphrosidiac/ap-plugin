"""_net.py — stdlib-only HTTP helpers shared by the geo-aeo scripts.

No third-party dependencies on purpose: these scripts must run on any box with python3,
inside any project, without a venv. Redirects are followed by hand so the chain is visible
(a 301 -> 302 -> 200 chain is a finding, not an implementation detail).
"""
from __future__ import annotations

import gzip
import json
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)


def load_bots() -> list[dict]:
    with open(os.path.join(DATA, "ai_bots.json"), encoding="utf-8") as f:
        return json.load(f)["bots"]


def _ssl_context(insecure: bool = False) -> ssl.SSLContext:
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    ctx = ssl.create_default_context()
    # python.org builds on macOS ship without a CA bundle; fall back to the system one.
    for cafile in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
        if os.path.exists(cafile):
            try:
                ctx.load_verify_locations(cafile)
            except Exception:
                pass
    try:
        import certifi  # type: ignore

        ctx.load_verify_locations(certifi.where())
    except Exception:
        pass
    return ctx


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: D401
        return None


@dataclass
class Response:
    url: str
    final_url: str
    status: int
    headers: dict
    body: bytes
    chain: list = field(default_factory=list)  # [(status, url), ...] hops before final
    elapsed_ms: int = 0
    ttfb_ms: int = 0
    error: str = ""

    @property
    def text(self) -> str:
        ctype = self.headers.get("content-type", "")
        enc = "utf-8"
        if "charset=" in ctype:
            enc = ctype.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        try:
            return self.body.decode(enc, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")

    def h(self, name: str) -> str:
        return self.headers.get(name.lower(), "")


def _hdrs(items) -> dict:
    """Lower-case header dict; repeated headers (Vary, Link, X-Robots-Tag…) are merged, not overwritten."""
    out: dict = {}
    for k, v in items:
        k = k.lower()
        out[k] = f"{out[k]}, {v}" if k in out else v
    return out


def fetch(
    url: str,
    ua: str = BROWSER_UA,
    timeout: float = 20.0,
    max_hops: int = 10,
    insecure: bool = False,
    method: str = "GET",
    extra_headers: dict | None = None,
    max_bytes: int = 15_000_000,
) -> Response:
    ctx = _ssl_context(insecure)
    opener = urllib.request.build_opener(
        _NoRedirect(), urllib.request.HTTPSHandler(context=ctx)
    )
    chain: list = []
    cur = url
    t0 = time.time()
    for _ in range(max_hops + 1):
        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=0.9",
        }
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(cur, headers=headers, method=method)
        t1 = time.time()
        try:
            resp = opener.open(req, timeout=timeout)
            status = resp.status
            hdrs = _hdrs(resp.headers.items())
            ttfb = int((time.time() - t1) * 1000)
            raw = resp.read(max_bytes)
        except urllib.error.HTTPError as e:
            status = e.code
            hdrs = _hdrs((e.headers or {}).items())
            ttfb = int((time.time() - t1) * 1000)
            try:
                raw = e.read(max_bytes)
            except Exception:
                raw = b""
        except Exception as e:  # DNS, TLS, timeout, reset
            return Response(url, cur, 0, {}, b"", chain, int((time.time() - t0) * 1000), 0, f"{type(e).__name__}: {e}")
        if status in (301, 302, 303, 307, 308) and "location" in hdrs:
            chain.append((status, cur))
            cur = urllib.parse.urljoin(cur, hdrs["location"])
            continue
        enc = hdrs.get("content-encoding", "")
        try:
            if "gzip" in enc:
                raw = gzip.decompress(raw)
            elif "deflate" in enc:
                raw = zlib.decompress(raw)
        except Exception:
            pass
        if cur.endswith(".gz") and raw[:2] == b"\x1f\x8b":
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
        return Response(url, cur, status, hdrs, raw, chain, int((time.time() - t0) * 1000), ttfb)
    return Response(url, cur, 0, {}, b"", chain, int((time.time() - t0) * 1000), 0, "too many redirects")


def origin(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return f"{p.scheme}://{p.netloc}"


def same_site(a: str, b: str) -> bool:
    ha = urllib.parse.urlsplit(a).hostname or ""
    hb = urllib.parse.urlsplit(b).hostname or ""
    strip = lambda h: h[4:] if h.startswith("www.") else h  # noqa: E731
    return strip(ha) == strip(hb)


def normalize(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    path = p.path or "/"
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), path, p.query, ""))
