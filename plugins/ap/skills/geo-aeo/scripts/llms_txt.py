#!/usr/bin/env python3
"""llms_txt.py — draft an /llms.txt (llmstxt.org format) from a site's sitemap.

    python3 llms_txt.py https://example.com [--max 120] [--out public/llms.txt] [--name "Acme"] [--summary "..."]

Evidence check before you spend time on this (references/technical-access.md): Google says
Search ignores llms.txt, and a May 2026 log study found 97% of llms.txt files got zero
requests. It is a cheap courtesy for coding agents and doc tools, not a GEO lever. Markdown
responses to `Accept: text/markdown` are what agents actually request — do that first.

The draft is a starting point: a human (or you, reading the pages) must rewrite the summary
and descriptions so each line says what the page answers, and prune to the pages worth
reading. Never list URLs that are noindexed, redirected, or behind a login.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import fetch, origin  # noqa: E402
from _page import parse_page  # noqa: E402
from _robots import parse as parse_robots  # noqa: E402


def sitemap_urls(base: str, limit: int) -> list[str]:
    r = fetch(base + "/robots.txt", timeout=10)
    cands = parse_robots(r.text).sitemaps if r.status == 200 else []
    cands = cands or [base + "/sitemap.xml", base + "/sitemap_index.xml"]
    out, seen = [], set()
    while cands and len(out) < limit * 3:
        u = cands.pop(0)
        if u in seen:
            continue
        seen.add(u)
        r = fetch(u, timeout=20)
        if r.status != 200:
            continue
        try:
            root = ET.fromstring(r.body)
        except ET.ParseError:
            continue
        ns = root.tag.split("}")[0] + "}" if "}" in root.tag else ""
        if root.tag.endswith("sitemapindex"):
            cands += [(s.findtext(f"{ns}loc") or "").strip() for s in root.findall(f"{ns}sitemap")]
        else:
            out += [(x.findtext(f"{ns}loc") or "").strip() for x in root.findall(f"{ns}url")]
    return [u for u in dict.fromkeys(out) if u]


def describe(u: str):
    r = fetch(u, timeout=20)
    if r.status != 200 or r.chain or "html" not in r.h("content-type"):
        return None
    p = parse_page(r.final_url, r.text)
    robots = (p.meta.get("robots", "") + r.h("x-robots-tag")).lower()
    if "noindex" in robots:
        return None
    title = re.split(r"\s+[|–—-]\s+", p.title)[0].strip() or u
    desc = p.meta.get("description") or (p.paragraphs[0] if p.paragraphs else "")
    return {"url": r.final_url, "title": title, "desc": re.sub(r"\s+", " ", desc)[:180], "site_title": p.title,
            "og_site": p.meta.get("og:site_name", "")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--max", type=int, default=120)
    ap.add_argument("--out")
    ap.add_argument("--name")
    ap.add_argument("--summary")
    a = ap.parse_args()
    base = origin(a.url if a.url.startswith("http") else "https://" + a.url)
    urls = sitemap_urls(base, a.max)[: a.max] or [base + "/"]
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        pages = [p for p in ex.map(describe, urls) if p]
    home = next((p for p in pages if urllib.parse.urlsplit(p["url"]).path in ("", "/")), pages[0] if pages else None)
    name = a.name or (home and (home["og_site"] or home["title"])) or base
    summary = a.summary or (home and home["desc"]) or "TODO: one-sentence description of who this is and what the site answers."
    groups = defaultdict(list)
    for p in pages:
        seg = urllib.parse.urlsplit(p["url"]).path.strip("/").split("/")[0]
        groups[seg.replace("-", " ").title() if seg else "Main"].append(p)
    L = [f"# {name}", "", f"> {summary}", "",
         "TODO: 2–4 sentences of the facts an assistant most often gets wrong about us "
         "(what we do, for whom, where, prices from, how to contact). Keep them identical to the About page.", ""]
    singles = [g for g in list(groups) if len(groups[g]) == 1 and g != "Main"]
    if len(singles) > 1:
        for g in singles:
            groups["Pages"] += groups.pop(g)
    main_first = sorted(groups, key=lambda g: (g != "Main", -len(groups[g])))
    optional = []
    for g in main_first:
        items = groups[g]
        if g.lower() in ("tag", "tags", "category", "categories", "author", "page", "search"):
            continue
        if len(items) > 25:
            optional.append((g, items[25:]))
            items = items[:25]
        L.append(f"## {g}")
        L += [f"- [{p['title']}]({p['url']})" + (f": {p['desc']}" if p["desc"] else "") for p in items]
        L.append("")
    if optional:
        L.append("## Optional")
        for g, items in optional:
            L += [f"- [{p['title']}]({p['url']})" for p in items]
        L.append("")
    text = "\n".join(L)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {a.out} ({len(pages)} pages) — now edit the TODO lines and descriptions by hand", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
