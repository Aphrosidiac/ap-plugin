---
name: geo-aeo
description: >
  Transform a website so AI answer engines (Google AI Overviews and AI Mode, ChatGPT,
  Perplexity, Copilot, Claude, Gemini) can reach, understand, cite and recommend it, while
  making its classic SEO excellent. Covers GEO, AEO and technical SEO end to end: AI-crawler
  access (robots.txt, Cloudflare/WAF blocks, JS rendering), structured data and entities,
  answer-first content, fan-out coverage, off-site authority, agent-readiness, and measuring
  AI visibility with confidence intervals. Ships an auditor, bot-access prober, render diff,
  log analyzer, llms.txt drafter and multi-engine citation tracker. Use whenever someone wants
  a site to show up in AI answers or search: "optimize for GEO/AEO", "get cited by ChatGPT",
  "why doesn't Perplexity mention us", "AI Overviews", "LLM SEO", "AI visibility audit",
  "SEO audit", "fix our SEO", "are we blocking AI bots", "llms.txt", "track our brand in
  ChatGPT" — even when only "SEO" is said, if the job is auditing or transforming a site.
---

# GEO / AEO — make a site the source answer engines cite

An answer engine is a retrieval pipeline: it decides whether to search, fans the question out
into sub-queries, pulls candidate passages from an index, reranks them, writes an answer from
a few of them, and cites some. **Almost everything is decided at retrieval, and retrieval runs
on classic search signals.** So the work has an order — access, then entity, then extractable
answers, then coverage, then third-party consensus — and it is measured as rates, not ranks.

The evidence behind every rule here is in `research/` (nine dated, sourced dossiers compiled
2026-09-26); `references/evidence.md` is the ledger of what is proven, weak, or myth. Google's
own position (July 2026): AEO/GEO "are still SEO" — no llms.txt, no special schema, no
chunking, no AI-specific writing. Bing's is more prescriptive about structure. Both hold; this
skill does the part that serves both and refuses the tricks.

Four ways this fails, all of which look like success at the time:

- **Content theatre on a blocked site.** Beautiful answer-first rewrites, and Cloudflare is
  403ing OAI-SearchBot, or the pages are a React shell that GPTBot sees as an empty `<div>`.
  Nothing downstream of access matters until access is proven — with probes and logs, not by
  reading robots.txt. `references/technical-access.md`.
- **Myth-driven work.** llms.txt, FAQ schema, "chunking for LLMs", word-count targets, an
  "AI version" of pages, a promised "+40%". Time spent, nothing moved, and some of it is now
  spam. `references/evidence.md` — never recommend or promise anything tagged [myth].
- **Invented authority.** Fabricated statistics, fake reviews, made-up authors, bumped dates,
  hidden "note to AI" text, astroturfed Reddit, self-ranked listicles. They get sites demoted
  site-wide (Google's 2025–26 core and spam updates) and they are exactly what engines are
  building detectors for. Every fact must be true, sourced and visible.
- **Unmeasured claims.** One ChatGPT screenshot before, one after, "it works". Answers are
  stochastic — <1% chance of the same brand list twice. Baseline and re-measure as rates with
  confidence intervals, or say plainly that it wasn't measured.

---

## Step 0 — Intake (settle before touching anything)

Resolve these from the request, the repo and the live site; ask only what changes the work.

- **Target**: live URL, repo, or both. With a repo you implement; without one you audit and
  write the plan and code-ready snippets.
- **Business**: what, for whom, where; vertical (local · e-commerce · SaaS/B2B · publisher ·
  YMYL · professional services) → `references/verticals.md`.
- **Markets and languages** (Malaysia: EN + colloquial BM at minimum; `ms-MY`, never `my`).
- **Brand, aliases, 5–15 competitors** with domains.
- **Stack and host/CDN** (Next, Nuxt, Astro, WordPress, Shopify, Webflow… · Cloudflare,
  Vercel, Netlify…) → `references/implementation.md`.
- **Owner decisions** that must not be made silently: training-crawler policy (GPTBot,
  ClaudeBot, CCBot, Google-Extended), Cloudflare bot settings, HSTS preload, any deploy.
- **Access**: GSC / Bing Webmaster Tools / GA4 / server logs / CDN dashboard / API keys for
  measurement — note what exists; missing access is recorded, not guessed around.

AP workspace: resolve the project state (`apmemory/scripts/memory-project-state.sh resolve`)
before editing a project, and find the brand kit on disk if the work touches visuals. "No
questions" briefs: infer every field, write the reasoning into `docs/geo/brief.md`, and still
stop for credentials and anything outward-facing (deploys, public posts, sending email).

All outputs go in the repo under `docs/geo/` (or the scratchpad when there is no repo).

## Step 1 — Baseline (measure before changing anything)

Run from the skill's `scripts/` (stdlib Python; the `.mjs` needs Playwright in the project or
`PLAYWRIGHT_DIR` pointing at a folder that has it):

```bash
S=~/.claude/skills/geo-aeo/scripts
python3 $S/audit.py https://site --pages 40 --out docs/geo/audit          # site + per-page, raw HTML, scored
python3 $S/bot_access.py https://site https://site/<key-page>             # CDN/WAF blocks per AI bot
node    $S/render_diff.mjs https://site/<one URL per template> --json docs/geo/render.json
python3 $S/presence.py site.com --brand "Name" --from-page https://site/<portfolio|clients|press>  # CC, Wayback, back-mentions
python3 $S/log_bots.py /path/access.log* --verify --json docs/geo/bots.json  # if logs are reachable
python3 $S/ai_visibility.py --prompts docs/geo/prompts_v1.csv --brand … --domain … \
        --competitors … --runs 3 --out docs/geo/visibility/<date>          # if API keys exist
```

audit.py's overall score is capped at 49 while any critical finding exists and 79 while any
high exists — read the findings, never just the number. Small or fragile sites:
`--workers 2 --delay 0.5`.

- Draft `docs/geo/prompts_v1.csv` from `assets/prompts-template.csv` (50–100 prompts,
  stratified; `references/measurement.md` §3) — freeze it when the first wave actually runs —
  and `docs/geo/facts.md` (the canonical fact set answers are checked against). Competitors:
  prefer the owner's own research, label it as positioning evidence, and replace it with the
  engines' cited-brand list after wave 0.
- Every engine you were asked about must be measured or explicitly listed as not measured
  (ai_visibility.py prints `SKIPPED …` lines; Perplexity needs `--perplexity-model`).
- No API keys → `ai_visibility.py --manual-template` writes a fill-in sheet for a logged-out
  sample (20–30 prompts × ChatGPT, Perplexity, Gemini/AI Mode); `--ingest-manual` scores it
  with the same parser. **If you cannot run logged-out sessions yourself, record "not
  measured", hand the sheet to the owner, and never substitute one anecdotal query or your own
  model's guess about what the engines say.**
- Pull what the owner can give: GSC Generative AI report + Page indexing, BWT AI Performance
  (grounding queries are gold), GA4 AI channel, CDN bot analytics.
- Read audit.md's "Not measured here" section and close each gap or record it.

Write `docs/geo/baseline.md`: scores, blockers, the access matrix, render gaps, visibility
rates with CIs, the domains engines cite for the category, the fan-out queries they ran.

## Step 2 — Diagnose and plan, in this order

Copy `assets/geo-plan-template.md` to `docs/geo/plan.md`. Each item: what · why (evidence tag
+ reference) · who (agent | owner) · effort · how it will be verified. The order is the point —
later layers are worthless while earlier ones fail.

| Tier | Layer | Reference |
|---|---|---|
| **P0** | **Access & eligibility** — search/user AI bots allowed; no CDN/WAF blocks or challenges; content + head tags in server HTML; **each indexable URL has its own distinct primary content** (no near-duplicate bodies, no UA-switched documents); indexable; no restrictive snippet controls; real 404s; single-hop https host; honest sitemaps | technical-access.md, seo-foundations.md |
| **P1** | **Entity & trust foundation** — one canonical fact set; Organization/WebSite `@graph` with sameAs + identifiers; About/facts, Contact, author pages, editorial policy; consistent names across profiles | structured-data.md §3–6 |
| **P2** | **Page extractability** — per template: answer-first capsules under question-shaped headings, self-contained sections, real tables/lists, sourced evidence, visible honest dates, bylines, matching schema | content.md §2–6 |
| **P3** | **Coverage** — pages missing for the fan-out: pricing with numbers, comparisons/alternatives, use cases, integrations, glossary, statistics/original data, real location pages; hub ↔ spoke linking | content.md §7–8, verticals.md |
| **P4** | **Technical SEO polish** — CWV, internal linking, hreflang, IndexNow, image/video, security headers | seo-foundations.md |
| **P5** | **Agent readiness** — markdown negotiation, semantic operable forms, optional llms.txt, commerce feeds/protocols where the stack fits | technical-access.md §5–6 |
| **P6** | **Off-site program** — reviews, third-party lists the engines already cite, YouTube, LinkedIn, digital PR/original data, directories, Wikidata where notable | offsite-authority.md |
| **P7** | **Measurement cadence** — waves, holdout, guard metrics, reporting | measurement.md |

Also list "Deliberately not doing" with reasons (llms.txt as a lever, FAQ schema for rich
results, doorway city pages, rewriting pages that are already cited…).

**Owner constraints and parked scope win.** If the project state or the owner says, for
example, "the founder is not named" or "campaigns are parked", skeleton fields and tiers that
conflict (named leadership on About, P6 outreach) become owner decisions in
`docs/geo/owner-todo.md` — not defaults you apply. Start `owner-todo.md` here (decisions,
access, `[NEEDS SOURCE]` items); Step 6 completes it.

Get the owner's go-ahead on the plan when changes are large or outward-facing; small,
clearly-in-scope fixes in a repo the user asked you to change can proceed.

## Step 3 — Implement (in the codebase)

Work the plan top-down. For each change, use the stack's idiom
(`references/implementation.md`) and the asset library:

- robots: `assets/robots/{A,B,C}-*.txt` — pick per the owner's training decision; B is the
  common default. Never put Googlebot/Bingbot/Applebot in a block list.
- JSON-LD: `assets/schema/*.jsonld` — one connected `@graph` per page, stable `@id`s,
  server-rendered, every fact also visible in the HTML.
- Head: `assets/head-template.html` — per page, never inherited from a layout.
- Sitemap `lastmod`, visible "Updated", and `dateModified` from one `updatedAt` field.
- IndexNow on publish/update/delete.
- Markdown negotiation and llms.txt (`scripts/llms_txt.py` drafts; a human edits) last.

Commit in small, described steps. Don't mix content rewrites with plumbing in one commit —
measurement needs to know which change did what (log each in the plan's intervention log).

## Step 4 — Transform content, page by page

For each key template and top page (`references/content.md`):

1. **Map the fan-out** for the page's target question (PAA, GSC long queries, BWT grounding
   queries, the engines' own fan-out queries from ai_visibility.py). Decide what this page
   answers and what gets its own linked page.
2. **Restructure to the matching skeleton** (service, product, comparison, how-to, glossary,
   FAQ hub, About/entity, statistics, local) — answer capsule first, question-shaped H2s,
   self-contained sections, entity names over pronouns, real tables.
3. **Add evidence that is true**: sourced statistics, named quotes, first-hand results, real
   prices and specs, a non-commodity element. Anything you can't source becomes
   `[NEEDS SOURCE: …]` in the owner list — never a plausible invention.
4. **Trust layer**: byline → author page, reviewer on YMYL, visible dates, changelog on
   refresh, schema that mirrors the visible text.
5. **Language versions** where the market needs them — natural register, localised facts.
6. **Surgical, not wholesale**, on pages already ranking #1 or already cited: add what's
   missing and measure; generic rewrites cost top sources 20–30% in the original GEO study.
7. Run the page QA checklist (`content.md` §11).

Keep the owner's voice. Answer sentences plain; personality lives in elaboration and opinions.

## Step 5 — Verify, adversarially

- Re-run `audit.py` (same `--urls` list as the baseline), `render_diff.mjs`, `bot_access.py`;
  diff against baseline. Zero critical/high left, or each remaining one explained.
- `curl -A GPTBot` acceptance test on every changed template (`implementation.md` top).
- Schema: audit.py lint clean + Rich Results Test on one URL per template + visible-parity.
- Build and run the site locally; check no regressions in titles, canonicals, status codes,
  redirects, hreflang, CWV-sensitive elements (LCP image, layout shifts).
- **Guard metrics**: nothing that helps AI extraction may cost classic SEO (canonicals,
  internal links, titles, indexability).
- Know the instrument: a green audit proves the checks ran, not that engines will cite. Only
  Step 7 answers that.

## Step 6 — Hand over what only the owner can do

Complete `docs/geo/owner-todo.md` (started in Step 2) and write `docs/geo/offsite-plan.md` (`offsite-authority.md` §6):
decisions (training bots, Cloudflare settings, Search Console AI toggle, HSTS preload), access
to grant, `[NEEDS SOURCE]` items, profiles to claim/align (GBP, Bing Places, Apple Business,
Waze, Yelp, Facebook, LinkedIn, G2…), the review programme, the list of third-party domains the
engines cite for the category with pitch drafts, PR/original-data idea, YouTube plan, Wikidata
(if notable). Deploying is the owner's call — ask, and push to GitHub before any deploy.

## Step 7 — Measure over time

Follow `assets/measurement-plan.md`: waves every 2–4 weeks on a frozen prompt set, treatment
vs control pages, difference-in-differences with prompt-clustered CIs, guard metrics, model
IDs logged. Expected lags: logs/Bing/Perplexity days–weeks; Google AI surfaces 2–8 weeks;
built-in model knowledge months to model generations. Report rung by rung (visibility →
retrieval → traffic → outcomes → halo); "no detectable change at this sample size" is an
honest result.

---

## Modes

| Request | Do |
|---|---|
| "Audit / how are we doing in AI search?" | Steps 0–2; publish baseline + plan (offer an Artifact if it will be shared) |
| "Make the site perfect for GEO/AEO" / "fix our SEO" | Steps 0–7 |
| "Is anything blocking AI bots?" | audit.py access matrix + bot_access.py + log_bots.py + CDN checklist (technical-access.md §9) |
| "Optimize this page / write a page that gets cited" | Step 4 on that page + schema + verify |
| "Track our brand in ChatGPT/Perplexity" | measurement.md: prompt set, ai_visibility.py, GA4 channel, BWT, logs |
| "Add llms.txt / schema for AI" | Do it if asked, and say plainly what the evidence says it will and won't do |

## Scripts

| Script | Job |
|---|---|
| `audit.py` | Site + page audit from raw HTML: RFC 9309 robots evaluation per AI bot (incl. Applebot→Googlebot fallback), Content-Signal, llms.txt, sitemaps + lastmod honesty, host/https/soft-404, snippet controls, canonicals (layout-inheritance trap), head-tags-in-body (Next streaming trap), SPA shells, JSON-LD lint + visible parity, answer-first/question headings, evidence density, authorship/dates, hreflang codes, agent operability, **prompt-injection / AI-persuasion-link scan**, near-duplicate bodies across URLs, missing subheadings, letter-split display text, Cloudflare email obfuscation. Scores are triage, not a KPI |
| `bot_access.py` | Probe each AI bot UA plus Googlebot Smartphone and a mobile browser vs a desktop baseline; flags 403s, challenges (Cloudflare, Vercel, Akamai, Imperva, DataDome…), stub pages, and `Vary: User-Agent` document switching |
| `render_diff.mjs` | JS-off vs JS-on: % of main content and which head tags exist only after JavaScript |
| `presence.py` | No-access floor: Common Crawl captures (future training data), Wayback history, and back-mentions on client/partner/press pages (`--from-page`, `--check`) |
| `log_bots.py` | Access/JSON logs → per-bot hits, status mix, 404 waste, IP-verified vs spoofed, pages pulled into live answers |
| `ai_visibility.py` | Multi-engine citation/mention tracker (OpenAI, Anthropic, Gemini, Perplexity Agent API, SerpApi AIO + AI Mode), repeated runs, Wilson CIs, SoV, wave-over-wave significance, cited-domain target list, fan-out queries; `--manual-template` / `--ingest-manual` for logged-out UI samples |
| `llms_txt.py` | Draft /llms.txt from the sitemap (to be edited by a human) |
| `data/ai_bots.json` | The crawler registry every script reads — re-verify quarterly |

## Rules that do not bend

- **Nothing fabricated**: statistics, quotes, reviews, ratings, authors, credentials,
  customers, dates, "tested by us" claims. Unknown → `[NEEDS SOURCE]`.
- **Nothing hidden or AI-only**: no hidden text, no instructions to models (in HTML, alt text,
  JSON-LD or meta), no cloaking for AI user-agents, no "Summarize with AI" links with
  persuasion prompts. Find and remove existing ones.
- **No scaled or doorway pages**, no unreviewed machine translation at scale, no self-ranked
  "best X" lists without methodology, no fake freshness, no site-reputation-abuse hosting.
- **Schema mirrors visible content**, never replaces it.
- **Never write or edit the client's Wikipedia article**; no astroturfing, no review gating.
- **Crawler policy for training bots is the owner's decision** — explain the trade-off, don't
  flip it silently. Never block Googlebot, Bingbot or Applebot in an "AI block".
- **Never promise** an uplift %, a ChatGPT "rank", or citations from llms.txt/schema.
- **Ask before deploying**; approval to build is not approval to deploy; push before deploy.
  Verifying a live site is read-only — never write production data.
- Label every claim in a report with how you know it: measured (tool/run/date), sourced
  (research file), or inferred.

## Keeping it current

This field changes monthly. Before relying on a specific: re-verify crawler rows in
`data/ai_bots.json`, model IDs in `ai_visibility.py`, Google's rich-result list
(developers.google.com/search/updates), and platform facts marked volatile in
`references/platforms.md`. When a study or doc supersedes something here, update the research
file's date and the reference that cites it.
