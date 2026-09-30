#!/usr/bin/env python3
"""presence.py — is the brand anywhere outside its own site? A factual floor for audits with
no Search Console / Bing Webmaster Tools / tool access.

    python3 presence.py example.com [--brand "Example Co"] [--check URL ...] [--from-page URL] [--crawls 3]

1. Common Crawl — captures of the domain in the latest N crawl indexes. Common Crawl is
   upstream of most open LLM training sets: no captures means future models' built-in
   knowledge will not include the site (check CCBot isn't blocked; earn links from
   well-connected sites — crawl priority follows link centrality).
2. Wayback Machine — has the site ever been archived, and when first.
3. Back-mentions — for each URL given with --check (or every outbound link on --from-page,
   e.g. a portfolio / clients / "as featured in" page), does that page mention the brand
   name or link to the domain? For agencies and studios this is often the single most
   informative off-site check: sites you built that don't credit you are missed mentions.

Search-engine index presence itself needs GSC/BWT (or a manual `site:` query); this script
does not scrape search engines.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import fetch, same_site  # noqa: E402
from _page import parse_page  # noqa: E402


def common_crawl(host: str, n: int) -> list[dict]:
    r = fetch("https://index.commoncrawl.org/collinfo.json", timeout=20, extra_headers={"Accept": "application/json"})
    if r.status != 200:
        return [{"crawl": "?", "error": f"collinfo {r.status or r.error}"}]
    out = []
    for c in json.loads(r.text)[:n]:
        q = f"{c['cdx-api']}?url={urllib.parse.quote(host)}/*&output=json&limit=500"
        rr = fetch(q, timeout=40, extra_headers={"Accept": "application/json"})
        if rr.status >= 500 or rr.status == 0:  # the CC index API is often briefly overloaded
            time.sleep(3)
            rr = fetch(q, timeout=40, extra_headers={"Accept": "application/json"})
        if rr.status == 200:
            lines = [l for l in rr.text.splitlines() if l.strip().startswith("{")]
            urls = {json.loads(l).get("url") for l in lines}
            out.append({"crawl": c["id"], "captures": len(lines), "unique_urls": len(urls)})
        elif rr.status == 404:
            out.append({"crawl": c["id"], "captures": 0, "unique_urls": 0})
        else:
            out.append({"crawl": c["id"], "error": f"{rr.status or rr.error}"})
    return out


def wayback(host: str) -> dict:
    r = fetch(f"https://web.archive.org/cdx/search/cdx?url={urllib.parse.quote(host)}&output=json&limit=1&fl=timestamp", timeout=30,
              extra_headers={"Accept": "application/json"})
    first = None
    if r.status == 200:
        try:
            rows = json.loads(r.text or "[]")
            first = rows[1][0] if len(rows) > 1 else None
        except (ValueError, IndexError):
            pass
    return {"status": r.status, "first_capture": first}


def mentions(url: str, domain: str, names: list[str]) -> dict:
    r = fetch(url, timeout=20)
    if r.status != 200:
        return {"url": url, "status": r.status or r.error, "mentions": False, "links": False}
    html = r.text
    p = parse_page(r.final_url, html)
    text = p.visible_text.lower()
    named = any(re.search(r"(?<![\w-])" + re.escape(n.lower()) + r"(?![\w-])", text) for n in names if n)
    linked = any(domain in (urllib.parse.urlsplit(u).hostname or "") for u, *_ in p.links_external)
    return {"url": url, "status": r.status, "mentions": named, "links": linked}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain")
    ap.add_argument("--brand", action="append", default=[], help="brand name/alias (repeatable)")
    ap.add_argument("--check", nargs="*", default=[], help="URLs that should mention the brand")
    ap.add_argument("--from-page", help="check every outbound link on this page (portfolio, clients, press)")
    ap.add_argument("--crawls", type=int, default=3)
    ap.add_argument("--json")
    a = ap.parse_args()
    host = urllib.parse.urlsplit(a.domain if "//" in a.domain else "https://" + a.domain).hostname or a.domain
    bare = host[4:] if host.startswith("www.") else host
    names = a.brand or [bare.split(".")[0]]
    report = {"domain": bare}

    print(f"Common Crawl ({a.crawls} latest indexes):")
    report["common_crawl"] = common_crawl(bare, a.crawls)
    for c in report["common_crawl"]:
        print(f"  {c.get('crawl')}: " + (f"{c['captures']} captures, {c['unique_urls']} URLs" if "captures" in c else c.get("error", "")))
    checked = [c for c in report["common_crawl"] if "captures" in c]
    if checked and all(c["captures"] == 0 for c in checked):
        print("  ! not in recent Common Crawl — future open-model training data won't contain the site. "
              "Check CCBot is allowed (robots + CDN) and earn links from well-connected sites.")
    if len(checked) < len(report["common_crawl"]):
        print("  (some indexes could not be queried — re-run later before concluding anything)")
    report["wayback"] = wayback(bare)
    print(f"Wayback first capture: {report['wayback']['first_capture'] or 'none'}")

    targets = list(a.check)
    if a.from_page:
        r = fetch(a.from_page, timeout=20)
        if r.status == 200:
            p = parse_page(r.final_url, r.text)
            skip = re.compile(r"(facebook|instagram|twitter|x\.com|linkedin|tiktok|youtube|wa\.me|whatsapp|google|apple\.com|pages\.dev$)", re.I)
            for u, *_ in p.links_external:
                h = urllib.parse.urlsplit(u).hostname or ""
                if not skip.search(h) and not same_site(u, "https://" + bare):
                    targets.append(u)
    targets = list(dict.fromkeys(targets))
    if targets:
        print(f"\nBack-mentions on {len(targets)} page(s):")
        report["back_mentions"] = [mentions(u, bare, names) for u in targets]
        for m in report["back_mentions"]:
            flag = "names+links" if m["mentions"] and m["links"] else "names" if m["mentions"] else "links" if m["links"] else "NONE"
            print(f"  {flag:<12} {m['status']}  {m['url']}")
        miss = [m for m in report["back_mentions"] if not (m["mentions"] or m["links"]) and m["status"] == 200]
        if miss:
            print(f"  ! {len(miss)} page(s) neither name nor link the brand — each is a missed, legitimate mention "
                  "(e.g. a 'Site by …' credit, a case-study link, a partner listing).")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(report, f, indent=1)


if __name__ == "__main__":
    main()
