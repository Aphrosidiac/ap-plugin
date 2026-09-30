#!/usr/bin/env python3
"""log_bots.py — what AI crawlers actually did on the server. Ground truth that robots.txt,
spoofed-UA probes and dashboards can only approximate.

    python3 log_bots.py access.log [more.log.gz ...] [--verify] [--days 30] [--json out.json]
    zcat /var/log/nginx/access.log*.gz | python3 log_bots.py - --verify

Reads combined/common log format (nginx, Apache, Caddy's common output) and JSON-lines logs
that carry user agent / path / status / ip fields (Cloudflare Logpush, Vercel log drains).

Reports per bot: hits, unique paths, status mix (a bot that gets 403/429/5xx is being refused
at the edge or the app), top paths, and — the most useful number here — the paths fetched by
user-triggered agents (ChatGPT-User, Perplexity-User, Claude-User, MistralAI-User...). Each
such fetch means a real person's question pulled that page into an answer, so they are the
closest first-party proxy for "which pages get cited".

--verify checks each claimed-bot IP against the owner's published IP ranges (fetched live) and
falls back to reverse+forward DNS where the owner documents a hostname. Unverified hits are
spoofers (scrapers borrowing a famous user-agent) and are reported separately.
"""
from __future__ import annotations

import argparse
import gzip
import ipaddress
import json
import os
import re
import socket
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import fetch, load_bots  # noqa: E402

COMBINED = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>\S+)[^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)(?: "(?P<ref>[^"]*)" "(?P<ua>[^"]*)")?'
)


def open_any(path):
    if path == "-":
        return sys.stdin
    if path.endswith(".gz"):
        return gzip.open(path, "rt", errors="replace")
    return open(path, errors="replace")


def parse_line(line: str):
    line = line.strip()
    if not line:
        return None
    if line.startswith("{"):
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            return None
        g = lambda *ks: next((o[k] for k in ks if k in o and o[k] not in (None, "")), "")  # noqa: E731
        ts = g("EdgeStartTimestamp", "timestamp", "time", "ts")
        return {"ip": str(g("ClientIP", "ip", "remote_addr", "client_ip")),
                "time": _ts(ts), "path": str(g("ClientRequestURI", "path", "request_uri", "url")),
                "status": int(g("EdgeResponseStatus", "status", "status_code") or 0),
                "ua": str(g("ClientRequestUserAgent", "user_agent", "ua", "http_user_agent"))}
    m = COMBINED.match(line)
    if not m:
        return None
    try:
        t = datetime.strptime(m.group("time"), "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        t = None
    return {"ip": m.group("ip"), "time": t, "path": m.group("path"), "status": int(m.group("status")), "ua": m.group("ua") or ""}


def _ts(v):
    if isinstance(v, (int, float)):
        v = v / 1e9 if v > 1e14 else v / 1e3 if v > 1e11 else v
        return datetime.fromtimestamp(v, tz=timezone.utc)
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None


class Verifier:
    def __init__(self, bots):
        self.nets: dict[str, list] = {}
        self.cache: dict = {}
        for b in bots:
            url = b.get("ip_json")
            if not url:
                continue
            r = fetch(url, timeout=15)
            nets = []
            if r.status == 200:
                try:
                    for p in json.loads(r.text).get("prefixes", []):
                        cidr = p.get("ipv4Prefix") or p.get("ipv6Prefix")
                        if cidr:
                            nets.append(ipaddress.ip_network(cidr, strict=False))
                except Exception:
                    pass
            self.nets[b["token"]] = nets
            print(f"  ip list {b['token']}: {len(nets)} prefixes", file=sys.stderr)

    def check(self, bot: dict, ip: str) -> str:
        key = (bot["token"], ip)
        if key in self.cache:
            return self.cache[key]
        res = "unknown"
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            self.cache[key] = "bad-ip"
            return "bad-ip"
        nets = self.nets.get(bot["token"])
        if nets:
            res = "verified" if any(addr in n for n in nets) else "SPOOFED"
        if res != "verified" and bot.get("rdns"):
            try:
                host = socket.gethostbyaddr(ip)[0]
                ok = any(host.endswith("." + d) or host == d for d in bot["rdns"])
                if ok and ip in socket.gethostbyname_ex(host)[2]:
                    res = "verified"
                elif res == "unknown":
                    res = "SPOOFED"
            except Exception:
                pass
        self.cache[key] = res
        return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--days", type=int, default=0, help="only the last N days")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json")
    args = ap.parse_args()

    bots = [b for b in load_bots() if b.get("ua_match")]
    rx = [(b, re.compile(re.escape(b["ua_match"]), re.I)) for b in bots]
    verifier = Verifier(bots) if args.verify else None
    since = datetime.now(timezone.utc) - timedelta(days=args.days) if args.days else None

    stats = defaultdict(lambda: {"hits": 0, "status": Counter(), "paths": Counter(), "days": Counter(), "verify": Counter(), "ips": set()})
    total = parsed = 0
    for path in args.logs:
        with open_any(path) as fh:
            for line in fh:
                total += 1
                rec = parse_line(line)
                if not rec:
                    continue
                parsed += 1
                if since and rec["time"] and rec["time"] < since:
                    continue
                ua = rec["ua"]
                for b, r in rx:
                    if r.search(ua):
                        s = stats[b["token"]]
                        s["hits"] += 1
                        s["status"][rec["status"]] += 1
                        s["paths"][rec["path"].split("#")[0]] += 1
                        if rec["time"]:
                            s["days"][rec["time"].strftime("%Y-%m-%d")] += 1
                        s["ips"].add(rec["ip"])
                        if verifier:
                            s["verify"][verifier.check(b, rec["ip"])] += 1
                        break

    print(f"\n{parsed:,}/{total:,} lines parsed · {sum(s['hits'] for s in stats.values()):,} AI-bot hits\n")
    if parsed == 0:
        print("No lines parsed — unsupported format? Expecting combined log format or JSON lines.")
        sys.exit(1)
    byt = {b["token"]: b for b in bots}
    order = sorted(stats, key=lambda t: -stats[t]["hits"])
    print(f"{'bot':<22}{'purpose':<10}{'hits':>8}{'paths':>7}  {'2xx':>5} {'3xx':>5} {'4xx':>5} {'5xx':>5}  verify")
    for t in order:
        s = stats[t]
        c = s["status"]
        band = lambda lo: sum(v for k, v in c.items() if lo <= k < lo + 100)  # noqa: E731
        v = " ".join(f"{k}:{n}" for k, n in s["verify"].most_common()) if verifier else ""
        print(f"{t:<22}{byt[t]['purpose']:<10}{s['hits']:>8}{len(s['paths']):>7}  {band(200):>5} {band(300):>5} {band(400):>5} {band(500):>5}  {v}")

    problems = []
    for t in order:
        c = stats[t]["status"]
        bad = sum(v for k, v in c.items() if k in (401, 403, 429) or k >= 500)
        if bad and bad / stats[t]["hits"] > 0.05:
            problems.append(f"{t}: {bad}/{stats[t]['hits']} requests refused or failed ({dict((k, v) for k, v in c.items() if k in (401, 403, 429) or k >= 500)}) — edge/WAF or app is blocking it")
        nf = c.get(404, 0)
        if nf and nf / stats[t]["hits"] > 0.1:
            problems.append(f"{t}: {nf} hits on 404s — broken internal links or stale sitemap URLs are wasting its crawl")
    if problems:
        print("\nProblems:")
        for p in problems:
            print("  ! " + p)

    users = [t for t in order if byt[t]["purpose"] in ("user", "agent")]
    if users:
        print("\nPages pulled into live AI answers (user-triggered fetches) — proxy for citations:")
        agg = Counter()
        for t in users:
            agg.update(stats[t]["paths"])
        for p, n in agg.most_common(args.top):
            print(f"  {n:>6}  {p}")
    for t in order[:6]:
        print(f"\nTop paths for {t}:")
        for p, n in stats[t]["paths"].most_common(min(args.top, 8)):
            print(f"  {n:>6}  {p}")
    if not any(byt[t]["purpose"] == "search" and t not in ("Googlebot", "Bingbot") for t in stats):
        print("\nNo AI search-index bot (OAI-SearchBot, PerplexityBot, Claude-SearchBot, meta-webindexer) seen. "
              "Either the window is short, the site is new/unlinked, or something upstream blocks them.")

    if args.json:
        out = {t: {"hits": s["hits"], "status": dict(s["status"]), "unique_paths": len(s["paths"]),
                   "top_paths": s["paths"].most_common(50), "days": dict(sorted(s["days"].items())),
                   "verify": dict(s["verify"]), "unique_ips": len(s["ips"])} for t, s in stats.items()}
        with open(args.json, "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
