#!/usr/bin/env python3
"""audit.py — GEO / AEO / SEO audit of a live site, from what crawlers actually receive.

    python3 audit.py https://example.com [--pages 40] [--out docs/geo/audit]
                     [--urls urls.txt] [--workers 6] [--delay 0] [--insecure]

Small or fragile sites: --workers 2 --delay 0.5.

Writes <out>/audit.json (machine-readable, the baseline for a re-run) and <out>/audit.md
(human report). Stdlib only.

What it measures, per site: robots.txt as each AI crawler reads it (RFC 9309, longest
match), Content-Signal lines, llms.txt, sitemaps (+ lastmod honesty), http->https and
host canonicalisation, soft-404 behaviour, markdown content negotiation.
Per page (raw HTML, no JavaScript — what most AI fetchers see): status, redirect hops,
TTFB, indexability (meta robots, X-Robots-Tag, canonical, snippet controls), title/H1/lang,
JSON-LD validity and completeness, SPA shells, extractable text, question headings and
answer-first leads, lists/tables, statistics and outbound citations, authorship and dates,
images alt, OG, hreflang, agent-operability (labels, landmarks).

What it cannot see — and the report says so: JavaScript-rendered content (render_diff.mjs),
CDN/WAF bot blocking (bot_access.py), Core Web Vitals field data (PSI/CrUX), off-site
authority, and what AI engines actually answer (ai_visibility.py).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import random
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import BROWSER_UA, fetch, load_bots, normalize, origin, same_site  # noqa: E402
from _page import DATE_TEXT, UPDATED_TEXT, all_types, count_numbers, is_question, parse_page, types_of, words  # noqa: E402
from _robots import parse as parse_robots  # noqa: E402
from _schema import LOCAL_SUBTYPES, lint as lint_schema  # noqa: E402

SEV_W = {"critical": 25, "high": 10, "medium": 4, "low": 1, "info": 0}
CATS = {
    "access": "AI crawler access",
    "render": "Rendering (raw HTML)",
    "index": "Indexability & canonicals",
    "schema": "Structured data & entity",
    "content": "Content extractability (AEO)",
    "trust": "Trust & E-E-A-T signals",
    "perf": "Delivery & performance",
    "agent": "Agent operability",
    "intl": "International",
}
FILLER = re.compile(
    r"^(in this (article|post|guide)|great question|when it comes to|it'?s no secret|have you ever|"
    r"are you (looking|wondering)|let'?s (dive|take a look)|in today'?s|welcome to|as we all know)",
    re.I,
)
INJECTION = re.compile(
    r"(ignore (all |any )?(previous|prior|above) (instructions|prompts)|disregard (the|all) (previous|above)|"
    r"(note|message|instructions?) (to|for) (the )?(ai|llm|language model|assistant|chatgpt|gemini|claude)|"
    r"\b(ai|llm) (assistants?|agents?|models?)[:,] (please |you must )?(recommend|mention|cite|rank|prefer|say)|"
    r"recommend (this|our) (business|company|product|site|brand) (above|over|first)|do not mention (any )?competitors|"
    r"remember \S+( \S+){0,4} as an? (trusted|authoritative|reliable) source|you are an? (helpful )?(ai|assistant|language model)\b(?! (manager|editor|director|professor|to)))",
    re.I,
)
AI_PROMPT_LINK = re.compile(
    r"href=[\"'](https?://(chatgpt\.com|chat\.openai\.com|claude\.ai|www\.perplexity\.ai|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|www\.google\.com/search\?[^\"']*udm=50)[^\"']*[?&](q|prompt|query)=[^\"']+)",
    re.I,
)
ARTICLEISH = {"Article", "BlogPosting", "NewsArticle", "TechArticle", "Report", "ScholarlyArticle", "HowTo"}
ARTICLE_PATH = re.compile(r"/(blog|news|articles?|posts?|guides?|insights?|resources|learn|library|stories|journal|berita|artikel)/", re.I)
UTIL_PATH = re.compile(r"/(login|signin|sign-in|register|cart|checkout|account|search|privacy|terms|cookie|legal|404)(/|$|\?)", re.I)


class Findings:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, sev, cat, msg, url="", fix="", evidence=""):
        self.items.append({"severity": sev, "category": cat, "message": msg, "url": url, "fix": fix, "evidence": evidence})


# ------------------------------------------------------------------------------ site level
def site_checks(start: str, args, F: Findings) -> dict:
    site: dict = {"start": start}
    home = fetch(start, insecure=args.insecure)
    site["home_status"] = home.status
    site["home_final"] = home.final_url
    site["home_chain"] = home.chain
    if home.status != 200:
        F.add("critical", "index", f"Homepage returned {home.status or home.error}", start)
    base = origin(home.final_url if home.status else start)
    site["origin"] = base
    host = urllib.parse.urlsplit(base).hostname or ""

    # http -> https, www <-> apex
    if base.startswith("https://"):
        r = fetch("http://" + host + "/", insecure=args.insecure)
        site["http_redirect"] = {"status_chain": [s for s, _ in r.chain], "final": r.final_url}
        if not r.final_url.startswith("https://"):
            F.add("high", "index", "http:// does not redirect to https://", "http://" + host + "/", "301/308 every http URL to its https twin")
        elif r.chain and r.chain[0][0] not in (301, 308):
            F.add("medium", "index", f"http->https uses {r.chain[0][0]} (temporary); use 301 or 308", "http://" + host + "/")
    else:
        F.add("critical", "trust", "Site is served over plain HTTP", base, "Serve over HTTPS with a valid certificate")
    alt_host = host[4:] if host.startswith("www.") else "www." + host
    r = fetch(base.split("://")[0] + "://" + alt_host + "/", insecure=args.insecure, timeout=10)
    site["alt_host"] = {"host": alt_host, "status": r.status, "final": r.final_url, "error": r.error}
    if r.status == 200 and (urllib.parse.urlsplit(r.final_url).hostname or "") == alt_host:
        canon_ok = re.search(r'rel=["\']?canonical["\']?[^>]*href=["\']https?://' + re.escape(host), r.text)
        F.add("medium" if canon_ok else "high", "index",
              f"Both {host} and {alt_host} serve 200 — duplicate host" + (" (mitigated: its canonical points to the main host)" if canon_ok else ""),
              base, f"301 {alt_host} to {host} at the edge")
    if home.h("strict-transport-security") == "" and base.startswith("https://"):
        F.add("low", "trust", "No HSTS header", base, "Strict-Transport-Security: max-age=31536000; includeSubDomains")

    # robots.txt
    rr = fetch(base + "/robots.txt", insecure=args.insecure)
    site["robots_status"] = rr.status
    robots = None
    if rr.status == 200 and "html" not in rr.h("content-type"):
        robots = parse_robots(rr.text)
        site["robots_sitemaps"] = robots.sitemaps
        site["robots_errors"] = robots.errors
        if len(rr.body) > 500 * 1024:
            F.add("medium", "access", f"robots.txt is {len(rr.body)//1024} KiB; Google ignores content past 500 KiB", base + "/robots.txt")
        for e in robots.errors[:10]:
            F.add("low", "access", f"robots.txt: {e}", base + "/robots.txt")
        cs = []
        for g in robots.groups:
            for v in g.extras.get("content-signal", []):
                cs.append((g.agents, v))
        cs += [(["(file)"], v) for v in robots.extras.get("content-signal", [])]
        site["content_signals"] = cs
        if any(re.search(r"search\s*=\s*no", v, re.I) for _, v in cs):
            F.add("critical", "access", "Content-Signal says search=no: you are asking engines not to show you in search results", base + "/robots.txt")
        if any(re.search(r"ai-input\s*=\s*no", v, re.I) for _, v in cs):
            F.add("high", "access", "Content-Signal says ai-input=no: you are asking AI answers (grounding/RAG) not to use your pages", base + "/robots.txt", "Set ai-input=yes unless this is a deliberate business decision")
    elif rr.status in (401, 403):
        F.add("critical", "access", f"robots.txt returns {rr.status}; Google treats 4xx as allow-all but many bots and CDNs treat it as a block signal — and it often means the WAF is blocking crawlers", base + "/robots.txt")
    elif rr.status >= 500 or rr.status == 0:
        F.add("critical", "access", f"robots.txt returns {rr.status or rr.error}; Google stops crawling the site while robots.txt 5xx's", base + "/robots.txt")
    elif rr.status == 200:
        F.add("medium", "access", "robots.txt serves HTML (probably an SPA fallback route)", base + "/robots.txt", "Serve a real text/plain robots.txt")
    else:
        F.add("low", "access", f"No robots.txt ({rr.status}); fine for access, but you lose the Sitemap: line", base + "/robots.txt")
    site["_robots"] = robots

    # Access matrix for core bots on "/"
    bots = [b for b in load_bots() if b.get("tier") == "core"]
    matrix = {}
    for b in bots:
        if robots is None:
            matrix[b["token"]] = {"allowed": True, "rule": "(no robots.txt)", "named": False}
            continue
        ok, rule = robots.allowed(b["token"], "/", b.get("fallback"))
        matrix[b["token"]] = {"allowed": ok, "rule": rule, "named": robots.names_token(b["token"]), "purpose": b["purpose"]}
    site["access_matrix"] = matrix
    for tok, m in matrix.items():
        b = next(x for x in bots if x["token"] == tok)
        if m["allowed"]:
            continue
        if b["purpose"] == "search" and tok in ("Googlebot", "Bingbot"):
            F.add("critical", "access", f"{tok} is blocked from / ({m['rule']}) — removes the site from search AND the AI answers built on it", base + "/robots.txt")
        elif b["purpose"] in ("search", "user"):
            F.add("high", "access", f"{tok} ({b['owner']}, {b['purpose']}) is blocked from / ({m['rule']}) — the site cannot be cited by that engine", base + "/robots.txt", "Allow search and user-triggered AI crawlers; see assets/robots/")
        elif b["purpose"] in ("training", "control"):
            F.add("info", "access", f"{tok} ({b['owner']}, {b['purpose']}) is blocked — a legitimate choice; it limits future models' knowledge of the brand but not live citations", base + "/robots.txt")

    # llms.txt / llms-full.txt (optional convention; never a critical)
    for name in ("llms.txt", "llms-full.txt"):
        r = fetch(f"{base}/{name}", insecure=args.insecure, timeout=10)
        ok = r.status == 200 and "html" not in r.h("content-type")
        info = {"status": r.status, "content_type": r.h("content-type"), "bytes": len(r.body)}
        if ok:
            t = r.text
            info["h1"] = bool(re.search(r"^# \S", t, re.M))
            info["links"] = len(re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", t))
        site[name] = info
    if not (site["llms.txt"]["status"] == 200 and "html" not in site["llms.txt"]["content_type"]):
        F.add("info", "access", "No /llms.txt. Optional: no major engine has confirmed using it; cheap to add for agents and dev-tool readers", base + "/llms.txt", "scripts/llms_txt.py drafts one")

    # Soft 404
    probe = f"{base}/geo-aeo-probe-{random.randint(10**6, 10**7)}"
    r = fetch(probe, insecure=args.insecure, timeout=10)
    site["soft404_status"] = r.status
    if r.status == 200:
        F.add("high", "index", "Unknown URLs return 200 (soft 404) — every typo URL becomes an indexable duplicate", probe, "Return a real 404 status for unknown routes")

    # Markdown negotiation (informational)
    r = fetch(base + "/", insecure=args.insecure, timeout=10, extra_headers={"Accept": "text/markdown"})
    site["markdown_negotiation"] = "markdown" in r.h("content-type")

    # Sitemaps
    candidates = (robots.sitemaps if robots and robots.sitemaps else []) or [base + "/sitemap.xml", base + "/sitemap_index.xml"]
    urls, sm_info = read_sitemaps(candidates, args)
    site["sitemaps"] = sm_info
    site["sitemap_url_count"] = len(urls)
    if not urls:
        F.add("high", "index", "No readable XML sitemap found", base, "Publish /sitemap.xml and reference it from robots.txt")
    else:
        if robots and not robots.sitemaps:
            F.add("low", "index", "robots.txt has no Sitemap: line", base + "/robots.txt")
        lm = [u["lastmod"] for u in urls if u.get("lastmod")]
        if not lm:
            F.add("medium", "index", "Sitemap has no <lastmod>; Bing and Google use accurate lastmod to schedule recrawls (freshness matters for AI answers)", candidates[0])
        else:
            c = Counter(x[:10] for x in lm)
            top, n = c.most_common(1)[0]
            if len(lm) >= 10 and n / len(lm) > 0.9:
                F.add("medium", "index", f"{n}/{len(lm)} sitemap lastmod values are the same day ({top}) — looks like build time, not content change; engines learn to ignore it", candidates[0], "Emit the real content-modified date")
        off = [u["loc"] for u in urls if not same_site(u["loc"], base)]
        if off:
            F.add("medium", "index", f"{len(off)} sitemap URLs are on another host (e.g. {off[0]})", candidates[0])
    site["_sitemap_urls"] = [u["loc"] for u in urls]
    return site


def read_sitemaps(cands, args, limit=20000):
    seen, out, info = set(), [], []
    queue = list(cands)
    while queue and len(seen) < 60 and len(out) < limit:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r = fetch(sm, insecure=args.insecure, timeout=20)
        entry = {"url": sm, "status": r.status, "urls": 0}
        if r.status != 200:
            info.append(entry)
            continue
        try:
            root = ET.fromstring(r.body)
        except ET.ParseError as e:
            entry["error"] = f"XML parse error: {e}"
            info.append(entry)
            continue
        tag = root.tag.split("}")[-1]
        ns = root.tag.split("}")[0] + "}" if "}" in root.tag else ""
        if tag == "sitemapindex":
            for s in root.findall(f"{ns}sitemap"):
                loc = (s.findtext(f"{ns}loc") or "").strip()
                if loc:
                    queue.append(loc)
            entry["index"] = True
        else:
            for u in root.findall(f"{ns}url"):
                loc = (u.findtext(f"{ns}loc") or "").strip()
                if loc:
                    out.append({"loc": loc, "lastmod": (u.findtext(f"{ns}lastmod") or "").strip()})
                    entry["urls"] += 1
        info.append(entry)
    return out, info


# ------------------------------------------------------------------------------ sampling
def pick_urls(site, home_page, args) -> list[str]:
    base = site["origin"]
    if args.urls:
        with open(args.urls) as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")][: args.pages]
    pool = list(dict.fromkeys(site["_sitemap_urls"]))
    pool += [u for u, _ in (home_page.links_internal if home_page else [])]
    pool = [normalize(u) for u in pool if u.startswith("http") and same_site(u, base)]
    pool = [u for u in pool if "/cdn-cgi/" not in u]
    pool = [u for u in dict.fromkeys(pool) if not re.search(r"\.(pdf|jpe?g|png|gif|webp|avif|svg|zip|mp4|xml|txt|css|js)(\?|$)", u, re.I)]
    # Stratify by first path segment so one huge blog does not eat the sample.
    buckets = defaultdict(list)
    for u in pool:
        seg = urllib.parse.urlsplit(u).path.strip("/").split("/")[0] or "(root)"
        buckets[seg].append(u)
    chosen = [normalize(site["home_final"] or base + "/")]
    rnd = random.Random(7)
    for k in buckets:
        rnd.shuffle(buckets[k])
    while len(chosen) < args.pages and any(buckets.values()):
        for k in sorted(buckets, key=lambda k: -len(buckets[k])):
            if buckets[k]:
                u = buckets[k].pop()
                if u not in chosen:
                    chosen.append(u)
            if len(chosen) >= args.pages:
                break
    return chosen


# ------------------------------------------------------------------------------ page level
def page_type(url, page) -> str:
    ts = {t for o in page.jsonld for t in types_of(o)}
    path = urllib.parse.urlsplit(url).path
    if path in ("", "/") or re.fullmatch(r"/[a-z]{2}(-[a-z]{2})?/?", path, re.I):
        return "home"
    if ts & {"Product", "ProductGroup"}:
        return "product"
    if ts & ARTICLEISH or ARTICLE_PATH.search(path):
        return "article"
    if UTIL_PATH.search(path):
        return "utility"
    if re.search(r"/(about|tentang|company|team|our-story)", path, re.I):
        return "about"
    if re.search(r"/(contact|hubungi)", path, re.I):
        return "contact"
    if re.search(r"/(faq|help|support|docs?)/?", path, re.I):
        return "help"
    if re.search(r"/(services?|solutions?|perkhidmatan|pricing|features?)", path, re.I):
        return "service"
    if re.search(r"/(locations?|branches?|cawangan|stores?)/", path, re.I):
        return "location"
    return "page"


def audit_page(url, args, robots, sitemap_set):
    if args.delay:
        time.sleep(args.delay)
    r = fetch(url, insecure=args.insecure)
    res = {"url": url, "final_url": r.final_url, "status": r.status, "error": r.error,
           "hops": [s for s, _ in r.chain], "ttfb_ms": r.ttfb_ms, "bytes": len(r.body),
           "content_type": r.h("content-type"), "x_robots": r.h("x-robots-tag"),
           "last_modified_header": r.h("last-modified"), "findings": []}
    F = Findings()
    def add(sev, cat, msg, fix="", evidence=""):
        F.add(sev, cat, msg, url, fix, evidence)

    if r.status != 200:
        add("high" if url in sitemap_set else "medium", "index", f"Status {r.status or r.error}" + (" (URL is in the sitemap)" if url in sitemap_set else ""))
        res["findings"] = F.items
        return res, None
    if len(r.chain) > 1:
        add("medium", "index", f"Redirect chain of {len(r.chain)} hops: {' -> '.join(str(s) for s, _ in r.chain)}", "Link and list the final URL directly")
    if r.chain and url in sitemap_set:
        add("medium", "index", "Sitemap lists a URL that redirects", "List only final 200 URLs in sitemaps")
    if "html" not in res["content_type"]:
        res["findings"] = F.items
        return res, None
    if r.ttfb_ms > 1800:
        add("high", "perf", f"Server response {r.ttfb_ms} ms; AI user-fetchers work under tight timeouts", "Cache HTML at the edge / SSG")
    elif r.ttfb_ms > 800:
        add("medium", "perf", f"Server response {r.ttfb_ms} ms (aim < 800 ms, ideally < 200 ms)")

    html = r.text
    p = parse_page(r.final_url, html)
    ptype = page_type(url, p)
    res["type"] = ptype
    text = " ".join(p.paragraphs) or p.text_sample

    # Indexability & snippet controls
    robots_meta = (p.meta.get("robots", "") + " " + p.meta.get("googlebot", "") + " " + res["x_robots"]).lower()
    res["robots_meta"] = robots_meta.strip()
    if "noindex" in robots_meta:
        add("high" if url in sitemap_set else "info", "index", "noindex" + (" on a URL listed in the sitemap" if url in sitemap_set else ""))
    if "nosnippet" in robots_meta:
        add("high", "index", "nosnippet: Google will not use this page's text in snippets, AI Overviews or AI Mode", "Remove nosnippet; use data-nosnippet on the specific elements you want hidden")
    m = re.search(r"max-snippet\s*:\s*(-?\d+)", robots_meta)
    if m and 0 <= int(m.group(1)) < 50:
        add("high", "index", f"max-snippet:{m.group(1)} starves AI features of quotable text", "Use max-snippet:-1")
    if "noarchive" in robots_meta or "noai" in robots_meta or "noimageai" in robots_meta:
        add("info", "index", f"Non-standard/limited directive present: {robots_meta.strip()[:80]}")
    if 'data-nosnippet' in html:
        add("info", "index", "Page uses data-nosnippet; confirm it does not wrap the main answer")
    if robots:
        for tok in ("Googlebot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot", "Bingbot"):
            ok, rule = robots.allowed(tok, r.final_url)
            if not ok:
                add("high", "access", f"{tok} is disallowed from this URL ({rule})")

    # AI-targeted manipulation: hidden instructions, prompt injection in text or JSON-LD, and
    # "Summarize with AI" links with pre-filled persuasion prompts (Microsoft "AI recommendation
    # poisoning", Feb 2026). Google's spam policy covers manipulating generative AI responses.
    scan = p.visible_text + " " + " ".join(p.jsonld_raw) + " " + " ".join(str(v) for v in p.meta.values())
    inj = INJECTION.findall(scan)
    if inj:
        add("critical", "trust", f"Text that reads as instructions to AI systems found in the page source ({len(inj)}×, e.g. '{inj[0][0][:60]}'). This is spam under Google's policy and a known attack pattern — remove it (check plugins and agency snippets)")
    links = AI_PROMPT_LINK.findall(html)
    if links:
        sample = urllib.parse.unquote(links[0][0])[:140]
        add("high", "trust", f"{len(links)} link(s) open an AI assistant with a pre-filled prompt (e.g. {sample}). If the prompt tells the model to trust/remember/recommend the brand, it is 'AI recommendation poisoning' — keep only neutral 'summarize this URL' prompts, or remove")

    # Canonical
    res["canonical"] = p.canonical
    if not p.canonical:
        add("medium", "index", "No rel=canonical", "Self-referencing absolute canonical on every indexable page")
    elif len(set(p.canonical)) > 1:
        add("high", "index", f"{len(set(p.canonical))} different canonicals — Google ignores all of them", evidence=str(p.canonical[:3]))
    else:
        c = urllib.parse.urljoin(r.final_url, p.canonical[0])
        if not p.canonical[0].startswith("http"):
            add("low", "index", "Canonical is relative; use an absolute URL")
        if normalize(c).rstrip("/") != normalize(r.final_url).rstrip("/"):
            sev = "high" if ptype != "home" and urllib.parse.urlsplit(c).path in ("", "/") else "info"
            add(sev, "index", f"Canonical points elsewhere: {c}" + (" (the homepage — often a layout-level canonical inherited by every page)" if sev == "high" else ""))
        res["canonical_abs"] = c

    # Head basics
    res["title"] = p.title
    res["description"] = p.meta.get("description", "")
    if not p.title:
        add("high", "content", "Missing <title>")
    elif len(p.title) > 70:
        add("low", "content", f"Title is {len(p.title)} chars; Google truncates/rewrites past ~60")
    elif len(p.title) < 15:
        add("low", "content", f"Title is only {len(p.title)} chars: '{p.title}'")
    if p.titles > 1:
        add("medium", "content", f"{p.titles} <title> tags")
    if not res["description"]:
        add("low", "content", "No meta description (engines will pick their own snippet)")
    if not p.lang:
        add("medium", "intl", "<html> has no lang attribute")
    h1 = [t for lvl, t in p.headings if lvl == 1]
    res["h1"] = h1
    if not h1:
        add("medium", "content", "No <h1> in the server HTML")
    elif len(h1) > 1:
        add("low", "content", f"{len(h1)} <h1> elements")
    levels = [lvl for lvl, _ in p.headings]
    if any(b - a > 1 for a, b in zip(levels, levels[1:])):
        add("low", "content", "Heading levels skip (e.g. h2 -> h4); extraction uses the outline")
    if p.head_in_body:
        add("high", "index", f"{', '.join(sorted(set(p.head_in_body)))} emitted inside <body> — Google tolerates it, but many AI fetchers and link-preview parsers stop at </head> and miss them (Next.js ≥15.2 streams generateMetadata into <body> for bots not in htmlLimitedBots)",
            "Next.js: add AI crawlers to htmlLimitedBots in next.config, or make metadata static; see references/implementation.md")
    if not (p.meta.get("og:title") and p.meta.get("og:image")):
        add("low", "content", "Missing og:title/og:image (link previews in chat apps and some AI surfaces use them)")

    # Rendering
    res["words"] = p.words_content
    res["root_shell"] = p.root_shell
    if p.root_shell:
        add("critical", "render", f"Client-rendered shell: only {p.words_content} words in the server HTML. Non-JS AI crawlers see an empty page", "SSR/SSG/prerender this route (references/implementation.md)")
    elif ptype not in ("utility", "contact") and p.words_content < 150:
        add("medium", "content", f"Thin server HTML: {p.words_content} words", "Add substantive, self-contained content or noindex/merge")
    if p.html_bytes > 2_000_000:
        add("high", "perf", f"HTML is {p.html_bytes//1024} KiB; Googlebot reads only the first 2 MB of HTML (since 2026) — content past that is not indexed", "Move inline data/scripts out, paginate, or trim hydration payloads")
    if p.html_bytes > 0 and p.script_bytes_inline > 0.6 * p.html_bytes and p.html_bytes > 300_000:
        add("low", "perf", f"Inline script is {p.script_bytes_inline//1024} KiB of {p.html_bytes//1024} KiB HTML (hydration payload bloat)")

    # Structured data
    types = sorted(set(all_types(p.jsonld)))
    res["schema_types"] = sorted({t for o in p.jsonld for t in types_of(o)})
    top = Counter(t for o in p.jsonld for t in types_of(o))
    for t in ("Organization", "Product", "ProductGroup", "WebSite", "BreadcrumbList", "LocalBusiness"):
        if top.get(t, 0) > 1:
            names = {str(o.get("name", "")) for o in p.jsonld if t in types_of(o)}
            add("medium", "schema", f"{top[t]} separate top-level {t} blocks" + (f" with different names {sorted(names)[:3]}" if len(names) > 1 else "") + " — usually theme + plugin/app both emitting it; keep one source, one @graph")
    res["microdata_types"] = sorted(set(p.microdata_types))
    for e in p.jsonld_errors:
        add("high", "schema", f"JSON-LD: {e}")
    for s in lint_schema(p.jsonld, r.final_url, p.visible_text):
        if s["severity"] != "info" or args.verbose:
            add(s["severity"], "schema", s["message"])
    if not types and not p.microdata_types:
        add("medium", "schema", "No structured data", f"Add JSON-LD appropriate to a {ptype} page (assets/schema/)")
    if ptype == "article" and not (set(types) & ARTICLEISH):
        add("medium", "schema", "Article-like page without Article/BlogPosting schema")
    if ptype == "product" and "Offer" not in types and "AggregateOffer" not in types:
        add("high", "schema", "Product without Offer (price, currency, availability) — AI shopping surfaces need it")
    if ptype != "home" and "BreadcrumbList" not in types:
        add("low", "schema", "No BreadcrumbList")

    # Content extractability (AEO)
    q_secs = [s for s in p.sections if is_question(s.heading)]
    res["sections"] = len(p.sections)
    res["question_headings"] = len(q_secs)
    weak_leads = []
    for s in p.sections:
        lead = s.first_para
        first = re.split(r"(?<=[.!?])\s+", lead)[0] if lead else ""
        if (is_question(s.heading) and (not first or words(first) > 45)) or FILLER.search(lead or ""):
            weak_leads.append(s.heading[:60])
        if s.words > 450 and s.lists == 0 and s.tables == 0:
            add("low", "content", f"Section '{s.heading[:50]}' runs {s.words} words with no list, table or sub-heading", "Split into self-contained sub-sections of ~1–3 short paragraphs each")
    if weak_leads:
        add("medium" if len(weak_leads) > 2 else "low", "content",
            f"{len(weak_leads)} section(s) do not open with a direct answer: {'; '.join(weak_leads[:4])}",
            "First sentence under a heading = the answer, ≤ 40 words, naming the subject explicitly")
    subheads = sum(1 for lvl, _ in p.headings if lvl in (2, 3))
    res["subheadings"] = subheads
    if p.words_content > 300 and subheads == 0 and ptype != "utility":
        add("medium", "content", f"No H2/H3 subheadings in {p.words_content} words — nothing for retrieval to match sub-queries against, no self-contained sections to lift",
            "Break the content into question- or topic-shaped H2/H3 sections, each opening with its answer")
    if p.letter_runs:
        add("medium", "content", f"{p.letter_runs} run(s) of text split into single-character elements — text extractors read 'S M O O T H'",
            "Keep real words in the server HTML; split letters at runtime in JS (after load) for the animation")
    if p.email_obfuscated:
        add("low", "trust", "Email address hidden from crawlers by Cloudflare Email Obfuscation — live AI fetchers can't read the contact email",
            "Turn off Email Obfuscation (Scrape Shield) or also show the address as plain text on the Contact/About page")
    if ptype not in ("utility", "contact") and p.words_content > 500 and not q_secs and subheads:
        add("low", "content", "No question-phrased headings; answer engines match sub-queries to headings", "Phrase key H2/H3s as the questions buyers ask")
    if ptype == "article" and p.words_content > 600 and p.lists + p.tables == 0:
        add("low", "content", "Long article with no lists or tables")
    nums = count_numbers(text)
    res["numbers_per_500w"] = round(nums / max(1, p.words_content) * 500, 1)
    ext = [l for l in p.links_external if not re.search(r"(facebook|instagram|twitter|x\.com|linkedin|tiktok|youtube|wa\.me|whatsapp|pinterest)\.", l[0])]
    res["outbound_citations"] = len(ext)
    if ptype == "article" and p.words_content > 600 and not ext:
        add("low", "trust", "No outbound links to sources; cited statistics and named sources measurably raise AI citation")

    # Trust: authorship and dates
    dates_schema = {k: o.get(k) for o in p.jsonld for k in ("datePublished", "dateModified") if o.get(k)}
    visible_date = bool(DATE_TEXT.search(text[:4000])) or bool(p.time_tags)
    res["dates"] = {"schema": dates_schema, "visible": visible_date, "meta_modified": p.meta.get("article:modified_time", "")}
    authored = any(o.get("author") for o in p.jsonld) or p.author_hints or p.meta.get("author")
    res["author"] = bool(authored)
    if ptype == "article":
        if not authored:
            add("medium", "trust", "No author (byline, schema author or rel=author)", "Byline linking to an author page with credentials; Person schema with sameAs")
        if not (dates_schema.get("dateModified") or dates_schema.get("datePublished") or visible_date):
            add("medium", "trust", "No published/updated date (schema or visible)", "Show 'Updated <date>' and set dateModified when content really changes")
        elif not visible_date:
            add("low", "trust", "Dates only in schema; show them on the page too")
        dm = dates_schema.get("dateModified") or dates_schema.get("datePublished")
        if dm:
            try:
                age = (dt.date.today() - dt.date.fromisoformat(str(dm)[:10])).days
                res["age_days"] = age
                if age > 365:
                    add("low", "trust", f"Last modified {age} days ago; AI engines favour fresh sources for time-sensitive queries", "Review and genuinely update, then bump dateModified")
            except ValueError:
                pass

    # Images, intl, agents
    if p.images_no_alt:
        add("low", "content", f"{p.images_no_alt}/{p.images} images have no alt attribute")
    if p.hreflang:
        langs = [l for l, _ in p.hreflang]
        bad = [l for l in langs if not re.fullmatch(r"x-default|[a-z]{2,3}(-[A-Z][a-z]{3})?(-([A-Z]{2}|\d{3}))?", l)]
        if bad:
            add("medium", "intl", f"Invalid hreflang code(s): {', '.join(sorted(set(bad))[:5])} (case matters: ms-MY, zh-Hans-MY; a region alone is invalid)")
        if any(l.lower().startswith("my") for l in langs):
            add("high", "intl", "hreflang 'my' is BURMESE, not Malay — Malay is 'ms' (ms-MY)")
        if any(l.lower() in ("en-uk",) for l in langs):
            add("medium", "intl", "hreflang 'en-UK' is invalid; use en-GB")
        if "x-default" not in [l.lower() for l in langs]:
            add("low", "intl", "hreflang set has no x-default")
        if not any(normalize(urllib.parse.urljoin(r.final_url, h)).rstrip("/") == normalize(r.final_url).rstrip("/") for _, h in p.hreflang):
            add("medium", "intl", "hreflang set does not include a self-reference")
    if not p.has_main:
        add("low", "agent", "No <main>/<article> landmark; agents and extractors use it to find the content")
    if p.inputs_unlabelled:
        add("low", "agent", f"{p.inputs_unlabelled} form field(s) without a label; browser agents cannot fill what they cannot name")
    if len({u for u, _ in p.links_internal}) < 3 and ptype != "utility":
        add("low", "index", "Fewer than 3 internal links out of this page")
    res["internal_links"] = len({u for u, _ in p.links_internal})
    res["alternates"] = p.alternates
    res["findings"] = F.items
    return res, p


# ------------------------------------------------------------------------------ scoring & report
def score(site_findings, pages):
    cat_pen = defaultdict(float)
    for f in site_findings:
        cat_pen[f["category"]] += SEV_W[f["severity"]]
    n = max(1, len(pages))
    for pg in pages:
        for f in pg.get("findings", []):
            cat_pen[f["category"]] += SEV_W[f["severity"]] / n * 1.0
    scores = {c: max(0, round(100 - cat_pen.get(c, 0) * 2)) for c in CATS}
    overall = round(sum(scores.values()) / len(scores))
    sev = [f["severity"] for f in site_findings] + [f["severity"] for pg in pages for f in pg.get("findings", [])]
    # A high average must not hide a blocker: any critical caps the headline at 49, any high at 79.
    if "critical" in sev:
        overall = min(overall, 49)
    elif "high" in sev:
        overall = min(overall, 79)
    return scores, overall


def write_report(out, site, pages, site_F, scores, overall, dup):
    L = []
    L.append(f"# GEO / AEO / SEO audit — {site['origin']}\n")
    L.append(f"Run {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · {len(pages)} pages sampled of {site.get('sitemap_url_count', 0)} in sitemaps · raw HTML only (no JavaScript)\n")
    L.append("Scores are a triage aid for ordering work, not a KPI. The KPI is measured citation/mention rate (ai_visibility.py).\n")
    if site.get("duplicate_clusters"):
        L.append(f"**⚠ {sum(len(g) for g in site['duplicate_clusters'])} URLs fall into {len(site['duplicate_clusters'])} near-duplicate content cluster(s)** — see HIGH findings. Distinct content per URL is a P0 condition.\n")
    L.append("| Area | Score |\n|---|---|")
    for c, name in CATS.items():
        L.append(f"| {name} | {scores[c]} |")
    L.append(f"| **Overall** | **{overall}** |\n")
    L.append("Overall is capped at 49 while any critical finding exists and at 79 while any high finding exists.\n")

    L.append("## AI crawler access (robots.txt, path `/`)\n")
    L.append("| Crawler | Purpose | Named in robots.txt | Allowed | Deciding rule |\n|---|---|---|---|---|")
    for tok, m in site["access_matrix"].items():
        L.append(f"| {tok} | {m.get('purpose','')} | {'yes' if m.get('named') else 'no'} | {'✅' if m['allowed'] else '⛔'} | `{m.get('rule') or '—'}` |")
    L.append("\nrobots.txt is only the first gate: a CDN/WAF can still 403 these bots. Run `bot_access.py`.\n")
    if site.get("content_signals"):
        L.append("Content-Signal lines: " + "; ".join(f"`{v}`" for _, v in site["content_signals"]) + "\n")

    allf = site_F + [f for pg in pages for f in pg.get("findings", [])]
    order = ["critical", "high", "medium", "low", "info"]
    grouped = defaultdict(lambda: defaultdict(list))
    for f in allf:
        grouped[f["severity"]][(f["category"], f["message"] if not f["url"] else re.sub(r"\d+", "#", f["message"]))].append(f)
    L.append("## Findings\n")
    for sev in order:
        if not grouped[sev]:
            continue
        L.append(f"### {sev.upper()}\n")
        for (cat, _msg), fs in sorted(grouped[sev].items(), key=lambda kv: -len(kv[1])):
            f0 = fs[0]
            urls = [f["url"] for f in fs if f["url"]]
            where = f" — {len(urls)} page(s): " + ", ".join(urls[:3]) + (" …" if len(urls) > 3 else "") if urls else ""
            L.append(f"- **[{CATS[cat]}]** {f0['message']}{where}" + (f"\n  - Fix: {f0['fix']}" if f0.get("fix") else ""))
        L.append("")
    if dup:
        L.append("### Duplicates\n")
        for kind, items in dup.items():
            for val, urls in items[:10]:
                L.append(f"- Duplicate {kind} ({len(urls)}×): `{val[:80]}` — {', '.join(urls[:3])}")
        L.append("")

    L.append("## Pages\n")
    L.append("| URL | Type | Status | Words | H2/H3 | Schema | Q-heads | Author | Dates | Issues |\n|---|---|---|---|---|---|---|---|---|---|")
    for pg in pages:
        d = pg.get("dates") or {}
        L.append(f"| {pg['url']} | {pg.get('type','')} | {pg['status']} | {pg.get('words','')} | {pg.get('subheadings','')} | {', '.join(pg.get('schema_types', []))[:60]} | {pg.get('question_headings','')} | {'✓' if pg.get('author') else ''} | {'✓' if (d.get('schema') or d.get('visible')) else ''} | {len(pg.get('findings', []))} |")
    L.append("\n## Site facts\n")
    for k in ("home_final", "http_redirect", "alt_host", "soft404_status", "markdown_negotiation", "llms.txt", "llms-full.txt", "sitemap_url_count"):
        L.append(f"- {k}: `{json.dumps(site.get(k))}`")
    L.append("\n## Not measured here\n")
    L.append("- JavaScript-rendered content → `node scripts/render_diff.mjs <url>`")
    L.append("- CDN/WAF blocking of AI bots → `python3 scripts/bot_access.py <url>`")
    L.append("- Core Web Vitals field data → PageSpeed Insights / CrUX (references/seo-foundations.md)")
    L.append("- What AI engines actually say about the brand → `python3 scripts/ai_visibility.py`")
    L.append("- Off-site authority (mentions, reviews, Wikipedia/Wikidata, Reddit, YouTube) → references/offsite-authority.md")
    with open(os.path.join(out, "audit.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--pages", type=int, default=40)
    ap.add_argument("--out", default="docs/geo/audit")
    ap.add_argument("--urls", help="file of URLs to audit instead of sampling")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--delay", type=float, default=0.0, help="seconds to wait before each page fetch (per worker)")
    ap.add_argument("--insecure", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    url = args.url if args.url.startswith("http") else "https://" + args.url
    os.makedirs(args.out, exist_ok=True)

    t0 = time.time()
    F = Findings()
    print(f"[site] {url}", file=sys.stderr)
    site = site_checks(url, args, F)
    robots = site.pop("_robots")
    home = fetch(site["home_final"] or url, insecure=args.insecure)
    home_page = parse_page(home.final_url, home.text) if home.status == 200 else None
    urls = pick_urls(site, home_page, args)
    sitemap_set = set(normalize(u) for u in site.pop("_sitemap_urls"))
    print(f"[pages] auditing {len(urls)}", file=sys.stderr)

    pages, parsed = [], {}
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(audit_page, u, args, robots, sitemap_set): u for u in urls}
        for fu in cf.as_completed(futs):
            try:
                res, p = fu.result()
            except Exception as e:  # never let one page kill the run
                res, p = {"url": futs[fu], "status": 0, "error": repr(e), "findings": []}, None
            pages.append(res)
            if p:
                parsed[res["url"]] = p
            print(f"  {res['status']} {res['url']}", file=sys.stderr)
    pages.sort(key=lambda x: urls.index(x["url"]) if x["url"] in urls else 999)

    # Site-level content signals from the sample
    dup = {}
    for key in ("title", "description"):
        c = defaultdict(list)
        for pg in pages:
            v = (pg.get(key) or "").strip()
            if v:
                c[v].append(pg["url"])
        d = [(v, us) for v, us in c.items() if len(us) > 1]
        if d:
            dup[key] = d
            F.add("medium" if key == "title" else "low", "content", f"{sum(len(u) for _, u in d)} pages share a duplicate {key}")
    home_types = set(pages[0].get("schema_types", [])) if pages else set()
    if not home_types & {"Organization", "Corporation", "LocalBusiness", "OnlineStore", "OnlineBusiness", "NewsMediaOrganization", "EducationalOrganization", "MedicalOrganization", "NGO", "GovernmentOrganization"} and not any(LOCAL_SUBTYPES.search(t) or t.endswith("Organization") for t in home_types):
        F.add("high", "schema", "Homepage has no Organization/LocalBusiness entity — the brand's canonical facts (name, logo, sameAs, contact) are not machine-declared", site["origin"], "assets/schema/organization-website.home.jsonld")
    if not home_types & {"WebSite"}:
        F.add("low", "schema", "Homepage has no WebSite entity (site name for Google)", site["origin"])
    internal = {u for p in parsed.values() for u, _ in p.links_internal}
    direct_contact = sum(p.contact_links for p in parsed.values())
    for label, rx in (("About", r"/(about|tentang|company|our-story|who-we-are)"), ("Contact", r"/(contact|hubungi)"), ("Privacy policy", r"/(privacy|privasi)")):
        if not any(re.search(rx, u, re.I) for u in internal):
            if label == "Contact" and direct_contact:
                F.add("low", "trust", "No dedicated Contact page (email/phone/WhatsApp links exist) — a page with full NAP, hours and registration number is still the canonical contact source", site["origin"])
                continue
            F.add("medium" if label != "Privacy policy" else "low", "trust", f"No {label} page linked from the sampled pages — trust pages are how engines and people verify who is behind a site", site["origin"])

    # Near-duplicate main content across distinct URLs (single-document sites, SSR shells,
    # templated city pages). Word 5-gram shingles, Jaccard.
    sh = {}
    for u, p in parsed.items():
        w = re.findall(r"\w+", p.content_text.lower())
        if len(w) >= 40:
            sh[u] = {" ".join(w[i:i + 5]) for i in range(0, len(w) - 4)}
    urls_sh = list(sh)
    clusters, seen = [], set()
    for i, a in enumerate(urls_sh):
        if a in seen:
            continue
        group = [a]
        for b in urls_sh[i + 1:]:
            if b in seen:
                continue
            inter = len(sh[a] & sh[b])
            jac = inter / max(1, len(sh[a] | sh[b]))
            if jac > 0.9:
                group.append(b)
        if len(group) > 1:
            seen.update(group)
            clusters.append(group)
    site["duplicate_clusters"] = clusters
    for g in clusters:
        F.add("critical" if len(g) >= max(3, 0.5 * len(parsed)) else "high", "content", f"{len(g)} URLs share >90% of their main content (e.g. {', '.join(g[:3])}) — engines see the same passages under every URL and nothing specific to cite on any of them",
              site["origin"], "Give each URL its own server-rendered primary content, or consolidate (301/canonical) pages that don't deserve to exist")
    types_seen = {t for pg in pages for t in pg.get("schema_types", [])}
    site["schema_types_seen"] = sorted(types_seen)
    if pages and sum(1 for pg in pages if pg.get("root_shell")) / len(pages) > 0.3:
        F.add("critical", "render", "Most sampled pages are client-rendered shells — the site is effectively invisible to non-JS AI crawlers", site["origin"])

    scores, overall = score(F.items, pages)
    out = {"site": site, "pages": pages, "site_findings": F.items, "scores": scores, "overall": overall,
           "generated": dt.datetime.now().isoformat(timespec="seconds"), "seconds": round(time.time() - t0, 1)}
    with open(os.path.join(args.out, "audit.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    write_report(args.out, site, pages, F.items, scores, overall, dup)
    crit = sum(1 for f in F.items + [x for pg in pages for x in pg.get("findings", [])] if f["severity"] == "critical")
    high = sum(1 for f in F.items + [x for pg in pages for x in pg.get("findings", [])] if f["severity"] == "high")
    print(f"\noverall {overall}/100 · {crit} critical · {high} high · report: {os.path.join(args.out, 'audit.md')}")


if __name__ == "__main__":
    main()
