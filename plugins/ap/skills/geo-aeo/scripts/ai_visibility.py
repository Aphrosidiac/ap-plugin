#!/usr/bin/env python3
"""ai_visibility.py — measure how often answer engines mention and cite a brand, across a
frozen prompt set, several engines and repeated runs. The KPI instrument for GEO work.

    python3 ai_visibility.py --prompts docs/geo/prompts.csv --brand "Acme" --aliases "Acme Co,acme.io" \
        --domain acme.io --competitors "Globex:globex.com,Initech:initech.com" \
        --engines openai,anthropic,gemini,serp_aio,serp_aimode --runs 3 --out docs/geo/visibility/2026-09-26

    python3 ai_visibility.py --summarize docs/geo/visibility/2026-10-24 --compare docs/geo/visibility/2026-09-26

No API keys? Manual sample, scored by the same parser so it is comparable with later API waves:
    python3 ai_visibility.py --manual-template docs/geo/visibility/manual-2026-09-26 --prompts … --brand … \
        --domain … --competitors … [--manual-engines chatgpt-ui,perplexity-ui,gemini-ui,aimode-ui] [--runs 1]
    # paste each answer's text and cited URLs (space-separated) into manual.csv, then:
    python3 ai_visibility.py --ingest-manual docs/geo/visibility/manual-2026-09-26
If nobody can run logged-out sessions, record "not measured" — never substitute one anecdotal
query or a model's opinion of what the engines would say.

prompts.csv columns: id,text,stratum,persona,locale,weight   (locale = ISO country, e.g. MY)
Keys come from the environment: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY,
PERPLEXITY_API_KEY (+ --perplexity-model), SERPAPI_API_KEY. Engines without a key are skipped.

Why repeated runs: answers are non-deterministic — SparkToro (Jan 2026, 2,961 runs) found a
<1% chance of the same brand list twice. Report RATES with confidence intervals, never a
"rank in ChatGPT". Detecting 30%→40% needs ~350 answers per period per engine.

Why these engines: the APIs are a consistent instrument for TREND, not a copy of what a
logged-in consumer sees (memory, routing, ads). SerpApi's google_ai_overview / google_ai_mode
engines are the only way to observe Google's real AI surfaces. Calibrate quarterly by running
20–30 prompts by hand in logged-out apps.

Model IDs below were current on 2026-09-26 per vendor docs. Re-check them; pass --*-model.

Outputs in --out: raw/<engine>/<prompt>-<run>.json (immutable), results.csv, summary.md.
The summary includes the domains the engines cite for your category — that list is the
off-site target list (who to get mentioned by) — and the fan-out queries they issued, which
are the content gaps to cover.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _net import _ssl_context, fetch  # noqa: E402

DEFAULT_MODELS = {
    "openai": "gpt-6-luna",          # cheap non-reasoning tier; web_search tool
    "anthropic": "claude-sonnet-5",  # web_search_20250305 server tool
    "gemini": "gemini-3.8-flash",    # grounding with Google Search
    "perplexity": "",                # Agent API needs an explicit model id (docs.perplexity.ai)
}


# ------------------------------------------------------------------------------ http
def post_json(url, body, headers, timeout=180, retries=4):
    data = json.dumps(body).encode()
    ctx = _ssl_context()
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504, 529) and attempt < retries:
                time.sleep(2 ** attempt * 3)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                time.sleep(2 ** attempt * 3)
                continue
            raise RuntimeError(str(e))


def get_json(url, timeout=120, retries=3):
    for attempt in range(retries + 1):
        r = fetch(url, timeout=timeout, extra_headers={"Accept": "application/json"})
        if r.status == 200:
            return json.loads(r.text)
        if r.status in (429, 500, 502, 503) and attempt < retries:
            time.sleep(2 ** attempt * 3)
            continue
        raise RuntimeError(f"HTTP {r.status}: {r.text[:300]}")


# ------------------------------------------------------------------------------ engines
# Each returns {"text", "cited": [urls], "sourced": [urls], "queries": [..], "model", "error"}
def eng_openai(prompt, locale, a):
    body = {"model": a.openai_model, "input": prompt,
            "tools": [{"type": "web_search", "search_context_size": "medium",
                       **({"user_location": {"type": "approximate", "country": locale}} if locale else {})}],
            "include": ["web_search_call.action.sources"]}
    raw = post_json("https://api.openai.com/v1/responses", body, {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"})
    text, cited, sourced, queries = [], [], [], []
    for item in raw.get("output", []):
        if item.get("type") == "web_search_call":
            act = item.get("action") or {}
            sourced += [s.get("url") for s in act.get("sources", []) or [] if s.get("url")]
            if act.get("query"):
                queries.append(act["query"])
            queries += act.get("queries", []) or []
        elif item.get("type") == "message":
            for c in item.get("content", []):
                text.append(c.get("text", ""))
                cited += [x.get("url") for x in c.get("annotations", []) or [] if x.get("type") == "url_citation" and x.get("url")]
    return raw, {"text": "\n".join(text), "cited": cited, "sourced": sourced, "queries": queries, "model": raw.get("model", a.openai_model)}


def eng_anthropic(prompt, locale, a):
    tool = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}
    if locale:
        tool["user_location"] = {"type": "approximate", "country": locale}
    body = {"model": a.anthropic_model, "max_tokens": 2048, "messages": [{"role": "user", "content": prompt}], "tools": [tool]}
    raw = post_json("https://api.anthropic.com/v1/messages", body,
                    {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
    text, cited, sourced, queries, err = [], [], [], [], ""
    for b in raw.get("content", []):
        t = b.get("type")
        if t == "server_tool_use":
            q = (b.get("input") or {}).get("query")
            if q:
                queries.append(q)
        elif t == "web_search_tool_result":
            c = b.get("content")
            if isinstance(c, dict) and c.get("type", "").endswith("error"):
                err = c.get("error_code", "search error")  # arrives inside HTTP 200 — do not read as "not cited"
            elif isinstance(c, list):
                sourced += [x.get("url") for x in c if x.get("url")]
        elif t == "text":
            text.append(b.get("text", ""))
            cited += [x.get("url") for x in b.get("citations", []) or [] if x.get("url")]
    return raw, {"text": "".join(text), "cited": cited, "sourced": sourced, "queries": queries, "model": raw.get("model", a.anthropic_model), "error": err}


_redirects: dict = {}


def _resolve(uri: str) -> str:
    """Gemini grounding URIs are vertexaisearch redirect links that expire; resolve once."""
    if "grounding-api-redirect" not in uri:
        return uri
    if uri not in _redirects:
        r = fetch(uri, method="HEAD", max_hops=0, timeout=15)
        _redirects[uri] = r.final_url if r.final_url and r.final_url != uri else uri
    return _redirects[uri]


def eng_gemini(prompt, locale, a):
    body = {"contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{a.gemini_model}:generateContent"
    raw = post_json(url, body, {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    cand = (raw.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts", []))
    gm = cand.get("groundingMetadata") or {}
    chunks = gm.get("groundingChunks") or []
    urls = []
    for ch in chunks:
        w = ch.get("web") or {}
        u = _resolve(w.get("uri", "")) if w.get("uri") else ""
        if not u or "grounding-api-redirect" in u:
            u = "https://" + w.get("title", "") if w.get("title") else u  # title is usually the domain
        urls.append(u)
    used = sorted({i for s in gm.get("groundingSupports", []) or [] for i in s.get("groundingChunkIndices", [])})
    cited = [urls[i] for i in used if i < len(urls)]
    return raw, {"text": text, "cited": cited, "sourced": urls, "queries": gm.get("webSearchQueries", []) or [], "model": a.gemini_model}


def _walk_urls(o, out):
    if isinstance(o, dict):
        if isinstance(o.get("url"), str):
            out.append(o["url"])
        for v in o.values():
            _walk_urls(v, out)
    elif isinstance(o, list):
        for v in o:
            _walk_urls(v, out)


def eng_perplexity(prompt, locale, a):
    if not a.perplexity_model:
        raise RuntimeError("set --perplexity-model (Agent API model id from docs.perplexity.ai)")
    tool = {"type": "web_search", "max_results": 10}
    if locale:
        tool["filters"] = {"country": locale}
    body = {"model": a.perplexity_model, "input": prompt, "tools": [tool]}
    raw = post_json("https://api.perplexity.ai/v1/agent", body, {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"})
    text = raw.get("output_text") or ""
    if not text:
        for item in raw.get("output", []) or []:
            for c in item.get("content", []) or []:
                text += c.get("text", "") if isinstance(c, dict) else ""
    sourced = []
    _walk_urls(raw.get("search_results") or raw.get("output") or [], sourced)
    cited = []
    _walk_urls([c.get("annotations") for item in raw.get("output", []) or [] for c in (item.get("content") or []) if isinstance(c, dict)], cited)
    return raw, {"text": text, "cited": cited or sourced, "sourced": sourced, "queries": [], "model": a.perplexity_model}


def _serp_text(blocks):
    out = []
    for b in blocks or []:
        if b.get("snippet"):
            out.append(b["snippet"])
        for li in b.get("list", []) or []:
            out.append(li.get("snippet", "") if isinstance(li, dict) else str(li))
        for r in b.get("rows", []) or []:
            out.append(" | ".join(map(str, r)) if isinstance(r, list) else str(r))
    return "\n".join(out)


def eng_serp_aimode(prompt, locale, a):
    q = urllib.parse.urlencode({"engine": "google_ai_mode", "q": prompt, "api_key": os.environ["SERPAPI_API_KEY"],
                                "no_cache": "true", **({"gl": locale.lower()} if locale else {})})
    raw = get_json("https://serpapi.com/search?" + q)
    refs = [r.get("link") for r in raw.get("references", []) or [] if r.get("link")]
    return raw, {"text": _serp_text(raw.get("text_blocks")), "cited": refs, "sourced": refs, "queries": [], "model": "google-ai-mode"}


def eng_serp_aio(prompt, locale, a):
    key = os.environ["SERPAPI_API_KEY"]
    q = urllib.parse.urlencode({"engine": "google", "q": prompt, "api_key": key, "no_cache": "true", **({"gl": locale.lower()} if locale else {})})
    raw = get_json("https://serpapi.com/search?" + q)
    aio = raw.get("ai_overview") or {}
    if aio.get("page_token"):  # loaded async: must be fetched within ~1 minute
        aio = get_json("https://serpapi.com/search?" + urllib.parse.urlencode({"engine": "google_ai_overview", "page_token": aio["page_token"], "api_key": key})).get("ai_overview", {}) or {}
    refs = [r.get("link") for r in aio.get("references", []) or [] if r.get("link")]
    organic = [r.get("link") for r in raw.get("organic_results", []) or [] if r.get("link")][:10]
    return {"ai_overview": aio, "organic_top10": organic}, {"text": _serp_text(aio.get("text_blocks")), "cited": refs, "sourced": refs,
                                                           "queries": [], "model": "google-ai-overview", "aio_present": bool(aio), "organic": organic}


ENGINES = {"openai": (eng_openai, "OPENAI_API_KEY"), "anthropic": (eng_anthropic, "ANTHROPIC_API_KEY"),
           "gemini": (eng_gemini, "GEMINI_API_KEY"), "perplexity": (eng_perplexity, "PERPLEXITY_API_KEY"),
           "serp_aimode": (eng_serp_aimode, "SERPAPI_API_KEY"), "serp_aio": (eng_serp_aio, "SERPAPI_API_KEY")}
SINGLE_RUN = {"serp_aimode", "serp_aio"}  # index snapshots: repeated runs add cost, not information


# ------------------------------------------------------------------------------ matching & stats
def host(u: str) -> str:
    h = (urllib.parse.urlsplit(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def on_domain(u: str, d: str) -> bool:
    h = host(u)
    d = d.lower().lstrip(".")
    return h == d or h.endswith("." + d)


def mentions(text: str, names: list[str]) -> int:
    """Position of the first mention (char offset) or -1."""
    best = -1
    for n in names:
        if not n:
            continue
        m = re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", text, re.I)
        if m and (best < 0 or m.start() < best):
            best = m.start()
    return best


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, c - h), min(1.0, c + h))


def pct(t):
    p, lo, hi = t
    return f"{p*100:.0f}% ({lo*100:.0f}–{hi*100:.0f})"


# ------------------------------------------------------------------------------ run
def load_prompts(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("text") or "").strip()]
    for i, r in enumerate(rows):
        r["id"] = r.get("id") or f"p{i+1:03d}"
        r["locale"] = (r.get("locale") or "").strip().upper()
    return rows


def parse_comp(s):
    out = []
    for part in [p for p in (s or "").split(",") if p.strip()]:
        name, _, dom = part.partition(":")
        out.append({"name": name.strip(), "aliases": [name.strip()], "domain": dom.strip()})
    return out


def run(a):
    prompts = load_prompts(a.prompts)
    engines = [e for e in a.engines.split(",") if e]
    live = []
    for e in engines:
        fn, key = ENGINES[e]
        if not os.environ.get(key):
            print(f"SKIPPED {e}: ${key} not set — this engine is NOT measured in this wave", file=sys.stderr)
        elif e == "perplexity" and not a.perplexity_model:
            print("SKIPPED perplexity: set --perplexity-model (Agent API model id, docs.perplexity.ai) — NOT measured", file=sys.stderr)
        else:
            live.append(e)
    if not live:
        sys.exit("no engine has an API key")
    os.makedirs(os.path.join(a.out, "raw"), exist_ok=True)
    brand = {"name": a.brand, "aliases": [a.brand] + [x.strip() for x in (a.aliases or "").split(",") if x.strip()], "domain": a.domain}
    comps = parse_comp(a.competitors)
    meta = {"brand": brand, "competitors": comps, "engines": live, "runs": a.runs, "prompts": a.prompts,
            "models": {e: getattr(a, f"{e}_model", e) for e in live}, "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with open(os.path.join(a.out, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)

    jobs = [(e, p, r) for e in live for p in prompts for r in range(1 if e in SINGLE_RUN else a.runs)]
    print(f"{len(jobs)} calls: {len(prompts)} prompts × {live} × {a.runs} runs", file=sys.stderr)
    rows = []

    def one(job):
        e, p, r = job
        path = os.path.join(a.out, "raw", e, f"{p['id']}-{r}.json")
        if os.path.exists(path):  # resumable
            with open(path) as f:
                saved = json.load(f)
            return e, p, r, saved["parsed"]
        try:
            raw, parsed = ENGINES[e][0](p["text"], p["locale"], a)
        except Exception as ex:
            return e, p, r, {"error": str(ex)[:300], "text": "", "cited": [], "sourced": [], "queries": []}
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"prompt": p, "run": r, "engine": e, "at": time.strftime("%Y-%m-%dT%H:%M:%S"), "parsed": parsed, "raw": raw}, f)
        return e, p, r, parsed

    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, (e, p, r, parsed) in enumerate(ex.map(one, jobs), 1):
            rows.append(score_row(e, p, r, parsed, brand, comps))
            if i % 10 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)}", file=sys.stderr)
    write_results(a.out, rows)
    summarize(a.out, a.compare)


def score_row(e, p, r, parsed, brand, comps):
    text = parsed.get("text", "") or ""
    cited = [u for u in parsed.get("cited", []) if u]
    sourced = [u for u in parsed.get("sourced", []) if u]
    pos = {brand["name"]: mentions(text, brand["aliases"])}
    for c in comps:
        pos[c["name"]] = mentions(text, c["aliases"])
    order = [n for n, x in sorted(pos.items(), key=lambda kv: kv[1]) if x >= 0]
    row = {"engine": e, "prompt_id": p["id"], "stratum": p.get("stratum", ""), "locale": p["locale"], "run": r,
           "model": parsed.get("model", ""), "error": parsed.get("error", ""),
           "brand_mentioned": int(pos[brand["name"]] >= 0),
           "brand_rank": (order.index(brand["name"]) + 1) if brand["name"] in order else "",
           "brands_mentioned": len(order),
           "brand_cited": int(any(on_domain(u, brand["domain"]) for u in cited)) if brand["domain"] else "",
           "brand_sourced": int(any(on_domain(u, brand["domain"]) for u in sourced)) if brand["domain"] else "",
           "cited_domains": " ".join(sorted({host(u) for u in cited})),
           "queries": " || ".join(parsed.get("queries", [])[:10]),
           "aio_present": parsed.get("aio_present", "")}
    for c in comps:
        row[f"m:{c['name']}"] = int(pos[c["name"]] >= 0)
        if c["domain"]:
            row[f"c:{c['name']}"] = int(any(on_domain(u, c["domain"]) for u in cited))
    return row


def write_results(out, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(os.path.join(out, "results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def _load(out):
    with open(os.path.join(out, "results.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(os.path.join(out, "meta.json")) as f:
        meta = json.load(f)
    return rows, meta


def summarize(out, compare=None):
    rows, meta = _load(out)
    prev = _load(compare)[0] if compare else None
    ok = [r for r in rows if not r["error"]]
    errs = len(rows) - len(ok)
    comps = [c["name"] for c in meta["competitors"]]
    L = [f"# AI visibility — {meta['brand']['name']}\n",
         f"Wave {os.path.basename(out.rstrip('/'))} · {len(ok)} answers ({errs} errors) · engines {', '.join(meta['engines'])} · models {meta['models']}\n",
         "Rates are share of answers, with 95% Wilson intervals. Runs of one prompt are correlated, so treat intervals as optimistic.\n",
         "| Engine | n | Mentioned | Cited (shown link) | Retrieved (sourced) | Avg rank when mentioned | Share of voice |",
         "|---|---|---|---|---|---|---|"]
    by_e = defaultdict(list)
    for r in ok:
        by_e[r["engine"]].append(r)
    for e, rs in sorted(by_e.items()) + [("ALL", ok)]:
        n = len(rs)
        m = sum(int(r["brand_mentioned"]) for r in rs)
        c = sum(int(r["brand_cited"] or 0) for r in rs)
        s = sum(int(r["brand_sourced"] or 0) for r in rs)
        ranks = [int(r["brand_rank"]) for r in rs if r["brand_rank"]]
        tot = m + sum(int(r.get(f"m:{x}", 0) or 0) for r in rs for x in comps)
        sov = f"{m/tot*100:.0f}%" if tot else "—"
        L.append(f"| {e} | {n} | {pct(wilson(m, n))} | {pct(wilson(c, n))} | {pct(wilson(s, n))} | {sum(ranks)/len(ranks):.1f} | {sov} |" if ranks else
                 f"| {e} | {n} | {pct(wilson(m, n))} | {pct(wilson(c, n))} | {pct(wilson(s, n))} | — | {sov} |")
    if prev:
        pv = [r for r in prev if not r["error"]]
        L.append("\n## Change vs " + os.path.basename(compare.rstrip("/")) + "\n")
        L.append("| Engine | Mentioned before → now | Cited before → now | Significant (95%)? |\n|---|---|---|---|")
        for e in sorted(by_e):
            a = [r for r in pv if r["engine"] == e]
            b = by_e[e]
            if not a:
                continue
            ma, mb = sum(int(r["brand_mentioned"]) for r in a), sum(int(r["brand_mentioned"]) for r in b)
            ca, cb = sum(int(r["brand_cited"] or 0) for r in a), sum(int(r["brand_cited"] or 0) for r in b)
            sig = _two_prop(ma, len(a), mb, len(b))
            L.append(f"| {e} | {ma/len(a)*100:.0f}% → {mb/len(b)*100:.0f}% | {ca/len(a)*100:.0f}% → {cb/len(b)*100:.0f}% | {sig} |")
    if comps:
        L.append("\n## Competitors (mention rate, all engines)\n")
        L.append("| Brand | Mentioned | Cited |\n|---|---|---|")
        n = len(ok)
        L.append(f"| **{meta['brand']['name']}** | {pct(wilson(sum(int(r['brand_mentioned']) for r in ok), n))} | {pct(wilson(sum(int(r['brand_cited'] or 0) for r in ok), n))} |")
        for x in comps:
            L.append(f"| {x} | {pct(wilson(sum(int(r.get(f'm:{x}', 0) or 0) for r in ok), n))} | {pct(wilson(sum(int(r.get(f'c:{x}', 0) or 0) for r in ok), n))} |")
    strata = sorted({r["stratum"] for r in ok if r["stratum"]})
    if strata:
        L.append("\n## By stratum (all engines)\n")
        L.append("| Stratum | n | Mentioned | Cited |\n|---|---|---|---|")
        for s in strata:
            rs = [r for r in ok if r["stratum"] == s]
            L.append(f"| {s} | {len(rs)} | {pct(wilson(sum(int(r['brand_mentioned']) for r in rs), len(rs)))} | {pct(wilson(sum(int(r['brand_cited'] or 0) for r in rs), len(rs)))} |")
    dom = Counter(d for r in ok for d in r["cited_domains"].split() if d)
    L.append("\n## Domains the engines cite for this category — the off-site target list\n")
    L.append("Get the brand onto these pages (lists, reviews, comparisons, threads, videos). They are what the engines already trust here.\n")
    own = meta["brand"].get("domain", "")
    comp_dom = {c["domain"]: c["name"] for c in meta["competitors"] if c.get("domain")}
    if own and dom.get(own.lower()):
        L.append(f"(Own domain {own} cited {dom[own.lower()]}× — excluded below.)\n")
    for d, k in [(d, k) for d, k in dom.most_common(40) if not (own and (d == own.lower() or d.endswith("." + own.lower())))][:30]:
        tag = f" — competitor ({comp_dom[d]})" if d in comp_dom else ""
        L.append(f"- {d} — {k}{tag}")
    q = Counter(x.strip().lower() for r in ok for x in r["queries"].split("||") if x.strip())
    if q:
        L.append("\n## Fan-out queries the engines ran — content gaps to cover\n")
        for x, k in q.most_common(40):
            L.append(f"- {x} ({k})")
    gaps = defaultdict(set)
    for r in ok:
        if not int(r["brand_mentioned"]) and any(int(r.get(f"m:{x}", 0) or 0) for x in comps):
            gaps[r["prompt_id"]].add(r["engine"])
    if gaps:
        L.append("\n## Prompts where a competitor appears and the brand does not\n")
        for pid, es in sorted(gaps.items()):
            L.append(f"- {pid}: {', '.join(sorted(es))}")
    aio = [r for r in ok if r["engine"] == "serp_aio"]
    if aio:
        present = sum(1 for r in aio if str(r["aio_present"]) in ("True", "1"))
        L.append(f"\nGoogle AI Overview shown on {present}/{len(aio)} prompts.")
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L[:12 + len(by_e)]))
    print(f"\nsummary: {os.path.join(out, 'summary.md')}")


def _meta_for(a, engines):
    return {"brand": {"name": a.brand, "aliases": [a.brand] + [x.strip() for x in (a.aliases or "").split(",") if x.strip()], "domain": a.domain},
            "competitors": parse_comp(a.competitors), "engines": engines, "runs": a.runs, "prompts": a.prompts,
            "models": {e: "manual-ui" for e in engines}, "started": time.strftime("%Y-%m-%dT%H:%M:%S")}


def manual_template(a):
    engines = [e for e in a.manual_engines.split(",") if e]
    os.makedirs(a.manual_template, exist_ok=True)
    meta = _meta_for(a, engines)
    meta["prompt_rows"] = load_prompts(a.prompts)
    with open(os.path.join(a.manual_template, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    path = os.path.join(a.manual_template, "manual.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["engine", "prompt_id", "run", "locale", "prompt", "answer_text", "cited_urls", "collected_by", "collected_at", "notes"])
        for e in engines:
            for p in meta["prompt_rows"]:
                for r in range(a.runs):
                    w.writerow([e, p["id"], r, p["locale"], p["text"], "", "", "", "", ""])
    print(f"wrote {path}: {len(engines)} engines × {len(meta['prompt_rows'])} prompts × {a.runs} runs.\n"
          "Use logged-out sessions, a fixed locale, a fresh chat per prompt. Paste the full answer text and every cited URL "
          "(space-separated). Leave rows you could not collect empty — they are excluded, not counted as 'not mentioned'.")


def ingest_manual(d, compare=None):
    with open(os.path.join(d, "meta.json")) as f:
        meta = json.load(f)
    prompts = {p["id"]: p for p in meta.get("prompt_rows", [])}
    rows = []
    with open(os.path.join(d, "manual.csv"), newline="", encoding="utf-8") as f:
        for m in csv.DictReader(f):
            if not (m.get("answer_text") or "").strip():
                continue
            p = prompts.get(m["prompt_id"], {"id": m["prompt_id"], "locale": m.get("locale", ""), "stratum": ""})
            urls = (m.get("cited_urls") or "").split()
            parsed = {"text": m["answer_text"], "cited": urls, "sourced": urls, "queries": [], "model": "manual-ui"}
            rows.append(score_row(m["engine"], p, int(m.get("run") or 0), parsed, meta["brand"], meta["competitors"]))
    if not rows:
        sys.exit("manual.csv has no filled answer_text rows — nothing to score (report: not measured)")
    write_results(d, rows)
    summarize(d, compare)


def _two_prop(k1, n1, k2, n2):
    if not n1 or not n2:
        return "—"
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return "no"
    z = (k2 / n2 - k1 / n1) / se
    return f"{'yes' if abs(z) >= 1.96 else 'no'} (z={z:.2f})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts")
    ap.add_argument("--brand")
    ap.add_argument("--aliases", default="")
    ap.add_argument("--domain", default="")
    ap.add_argument("--competitors", default="", help="Name:domain,Name:domain")
    ap.add_argument("--engines", default="openai,anthropic,gemini,perplexity,serp_aio,serp_aimode")
    ap.add_argument("--manual-template", help="write a fill-in manual.csv for a logged-out UI sample into this dir")
    ap.add_argument("--manual-engines", default="chatgpt-ui,perplexity-ui,gemini-ui,aimode-ui")
    ap.add_argument("--ingest-manual", help="score a filled-in manual.csv in this dir and summarize")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=f"docs/geo/visibility/{time.strftime('%Y-%m-%d')}")
    ap.add_argument("--compare", help="previous wave dir for a before/after table")
    ap.add_argument("--summarize", help="re-summarize an existing wave dir and exit")
    for e, m in DEFAULT_MODELS.items():
        ap.add_argument(f"--{e}-model", default=os.environ.get(f"{e.upper()}_MODEL", m))
    a = ap.parse_args()
    if a.summarize:
        summarize(a.summarize, a.compare)
        return
    if a.ingest_manual:
        ingest_manual(a.ingest_manual, a.compare)
        return
    if a.manual_template:
        if not (a.prompts and a.brand):
            ap.error("--manual-template needs --prompts and --brand")
        manual_template(a)
        return
    if not (a.prompts and a.brand):
        ap.error("--prompts and --brand are required")
    run(a)


if __name__ == "__main__":
    main()
