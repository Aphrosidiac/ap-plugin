#!/usr/bin/env python3
"""bot_access.py — does the CDN / WAF / host let AI crawlers through? robots.txt can say
"allow" while Cloudflare, Vercel, Akamai or a security plugin answers 403 or a challenge page.

    python3 bot_access.py https://example.com [https://example.com/page ...] [--all] [--json out.json]

For each URL it requests the page with a normal browser user-agent (the baseline) and then
with each AI crawler's user-agent, and compares status, size, title and challenge markers.

READ THE RESULT CORRECTLY. A spoofed user-agent from your IP is not the real bot:
- A 403/challenge for a spoofed bot UA while the browser UA gets 200 means the edge is
  filtering on that UA. That is strong evidence the real bot is blocked too — UNLESS the
  edge verifies bots by IP (Cloudflare "verified bots"), in which case the real crawler may
  pass while your spoof fails. Confirm in the CDN dashboard (Cloudflare: Security > Bots /
  AI Crawl Control) and in server logs (log_bots.py), which show the real bots' status codes.
- 200 for every UA means nothing at the edge filters on user-agent. IP-based blocks can still
  exist; logs are the ground truth.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import BROWSER_UA, fetch, load_bots  # noqa: E402

MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
GOOGLEBOT_SMARTPHONE = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/140.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

CHALLENGE = [
    (re.compile(r"<title>\s*Just a moment", re.I), "Cloudflare JS challenge"),
    (re.compile(r"cf-browser-verification|challenge-platform|cf_chl_opt", re.I), "Cloudflare challenge"),
    (re.compile(r"Attention Required! \| Cloudflare", re.I), "Cloudflare block page"),
    (re.compile(r"Vercel Security Checkpoint|x-vercel-challenge", re.I), "Vercel checkpoint"),
    (re.compile(r"_Incapsula_Resource|Incapsula incident", re.I), "Imperva/Incapsula"),
    (re.compile(r"px-captcha|PerimeterX|HUMAN Security", re.I), "HUMAN/PerimeterX"),
    (re.compile(r"Access Denied.*Reference #|errors\.edgesuite\.net", re.I | re.S), "Akamai"),
    (re.compile(r"DataDome|captcha-delivery\.com", re.I), "DataDome"),
    (re.compile(r"sucuri_cloudproxy|Sucuri WebSite Firewall", re.I), "Sucuri"),
    (re.compile(r"Wordfence|wfvt_", re.I), "Wordfence"),
    (re.compile(r"g-recaptcha|hcaptcha\.com|turnstile", re.I), "CAPTCHA widget"),
]


def title_of(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:80] if m else ""


def probe(url: str, name: str, ua: str, insecure: bool) -> dict:
    r = fetch(url, ua=ua, insecure=insecure, timeout=20)
    body = r.text if r.body else ""
    marks = [label for rx, label in CHALLENGE if rx.search(body[:200000])]
    hdr_marks = []
    if r.h("cf-mitigated"):
        hdr_marks.append(f"cf-mitigated: {r.h('cf-mitigated')}")
    if r.h("x-vercel-mitigated"):
        hdr_marks.append(f"x-vercel-mitigated: {r.h('x-vercel-mitigated')}")
    return {"agent": name, "status": r.status, "vary": r.h("vary"), "bytes": len(r.body), "title": title_of(body),
            "final_url": r.final_url, "markers": marks + hdr_marks, "server": r.h("server"),
            "error": r.error, "ms": r.elapsed_ms}


def verdict(base: dict, res: dict) -> str:
    if res["error"]:
        return "ERROR"
    if res["status"] in (401, 403, 406, 429, 451, 503) or res["status"] >= 500:
        return "BLOCKED" if base["status"] == 200 else "BOTH-FAIL"
    if any("challenge" in m.lower() or "captcha" in m.lower() or "checkpoint" in m.lower() or "block" in m.lower() or "cf-mitigated" in m for m in res["markers"]):
        if not base["markers"]:
            return "CHALLENGED"
    if base["bytes"] and res["bytes"] < 0.35 * base["bytes"] and res["status"] == 200:
        return "DIFFERENT (much smaller body — cloaking or a stub page?)"
    if base["title"] and res["title"] and res["title"] != base["title"]:
        return "DIFFERENT (title differs)"
    return "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--all", action="store_true", help="include 'extra' tier bots, not just core")
    ap.add_argument("--json")
    ap.add_argument("--insecure", action="store_true")
    args = ap.parse_args()
    bots = [b for b in load_bots() if b.get("ua") and (args.all or b.get("tier") == "core")]
    report = []
    exit_code = 0
    for url in args.urls:
        url = url if url.startswith("http") else "https://" + url
        base = probe(url, "browser", BROWSER_UA, args.insecure)
        rows = []
        agents = [("mobile-browser", MOBILE_UA), ("Googlebot-Smartphone", GOOGLEBOT_SMARTPHONE)] + [(b["token"], b["ua"]) for b in bots]
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = [ex.submit(probe, url, n, ua, args.insecure) for n, ua in agents]
            for fu in futs:
                rows.append(fu.result())
        print(f"\n{url}\n  baseline (browser UA): {base['status']} · {base['bytes']} B · '{base['title']}'" + (f" · markers {base['markers']}" if base['markers'] else ""))
        if "user-agent" in (base.get("vary") or "").lower():
            print("  ! response sends 'Vary: User-Agent' — the server picks the document by UA. Compare the bodies below;"
                  " substantively different content for bots is cloaking, and it also defeats edge caching")
        if base["markers"]:
            print("  ! the browser baseline itself hit a challenge — this edge challenges non-browser clients; results below are unreliable")
        print(f"  {'agent':<20} {'status':>6} {'bytes':>9}  verdict")
        for r in rows:
            v = verdict(base, r)
            r["verdict"] = v
            if v not in ("ok",):
                exit_code = 1
            print(f"  {r['agent']:<20} {r['status']:>6} {r['bytes']:>9}  {v}" + (f"  [{', '.join(r['markers'])}]" if r['markers'] else ""))
        report.append({"url": url, "baseline": base, "agents": rows})
    if args.json:
        with open(args.json, "w") as f:
            json.dump(report, f, indent=1)
    blocked = [(x["url"], r["agent"]) for x in report for r in x["agents"] if r.get("verdict", "ok") != "ok"]
    if blocked:
        print("\nNon-ok results: confirm in the CDN/WAF dashboard and server logs before changing anything (see the docstring).")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
