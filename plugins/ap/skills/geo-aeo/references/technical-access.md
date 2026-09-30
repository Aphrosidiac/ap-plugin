# Technical access — can AI systems fetch, render, parse and trust the site?

P0 of every plan. If this layer fails, nothing else in the skill matters. Evidence, full UA
table, vendor docs and dates: `research/03-technical-access.md`; per-platform behaviour:
`research/02-platforms.md`. The registry the scripts use: `data/ai_bots.json` (re-verify
rows against owner docs quarterly — this list changes monthly).

---

## 1. Three kinds of crawler, three different decisions

| Kind | Examples | Blocking it costs | Default stance for GEO |
|---|---|---|---|
| **Search / answer index** | Googlebot, Bingbot, Applebot, OAI-SearchBot, Claude-SearchBot, PerplexityBot, meta-webindexer, Amzn-SearchBot, DuckAssistBot, MistralAI-Index | Citations on that engine (Googlebot/Bingbot: classic search too) | **Always allow** |
| **User-triggered fetch** | ChatGPT-User, Claude-User, Perplexity-User, Google-Agent, Meta-ExternalFetcher, Amzn-User, MistralAI-User | Being read when a user asks about you or pastes your URL; agent tasks | **Allow** (most ignore robots.txt anyway — only a WAF stops them) |
| **Training / control token** | GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended, meta-externalagent, Amazonbot, Bytespider | No live citations — except **Google-Extended also removes Gemini-app/Vertex grounding**. Slowly removes the brand from future models' built-in knowledge | **Owner's decision.** Explain the trade-off; default to allow for brands that need to be *known* (new/small brands), and Template B for publishers protecting content |

Facts that decide real cases:
- **Blocking Google-Extended does NOT remove a site from AI Overviews or AI Mode.** Those use
  Googlebot. The controls for Google AI surfaces are `nosnippet`, `data-nosnippet`,
  `max-snippet`, `noindex`, and (since 2026) a Search Console property toggle that removes the
  site from AIO, AI Mode and Discover AI features.
- **Microsoft has no AI robots token.** Copilot use is limited by `noarchive` (not used in
  answers) and `nocache` (URL/title/snippet only) meta. Both reduce GEO — check nothing sets
  them by accident.
- **Brave Search** (behind Claude and many API-grounded apps) has no distinct UA and obeys the
  **Googlebot** group. **Applebot** also falls back to Googlebot rules when not named. So a
  Googlebot-specific disallow leaks into Claude and Siri.
- **CCBot (Common Crawl)** is upstream of most open training sets; ~9.5% of the top 1M sites
  block it. Blocking it is a long-term entity-knowledge cost for small brands.
- Only **Googlebot and Applebot render JavaScript.** Treat every other AI fetcher as raw-HTML.
- AI crawlers crawled from **US data centres** in measured studies. Geo-blocking or
  geo-redirecting US traffic hides the site from them.

## 2. robots.txt

Templates (validated with `scripts/_robots.py`): `assets/robots/A-maximize-visibility.txt`,
`B-search-yes-training-no.txt`, `C-search-engines-only.txt`.

Semantics that bite (RFC 9309 + Google):
- A crawler obeys **one** group: its own name if present, otherwise `*`. **Naming a bot drops
  it out of `*`** — copy shared `Disallow`s into every named group.
- Consecutive `User-agent:` lines share the rules below them. Groups naming the same bot merge.
- Longest matching path wins; on a tie, Allow wins. `*` wildcard, `$` end anchor, no regex.
- Status matters: 4xx (not 429) = "no restrictions"; **5xx/429 = Google stops crawling the
  whole site** (12h, then cached copy up to 30 days). Serve `200 text/plain` to every UA —
  never let the WAF 403 or challenge `/robots.txt`.
- 500 KiB limit. One file per protocol+host(+port); subdomains need their own.
- `Crawl-delay` ignored by Google, honoured by Anthropic (and Bing). `Noindex:` in robots.txt
  is unsupported.
- robots.txt blocks crawling, not indexing. To remove from index/AI features use `noindex`
  (and leave the URL crawlable so the tag can be seen).
- Change latency: OpenAI search ~24h; Meta 24h; DuckDuckGo 72h; Amazon caches up to 30 days.

**Content-Signal** (Cloudflare's deployed preference syntax, inside robots.txt groups):
`search` = index + links/short excerpts (explicitly *not* AI summaries); `ai-input` = RAG /
grounding / AI answers; `ai-train` = training. For GEO, write `ai-input=yes` explicitly —
Cloudflare's managed default omits it. The IETF aipref draft (`Content-Usage: train-ai=n`) has
no documented consumers yet.

## 3. The CDN / WAF / platform layer — the most common silent blocker

`scripts/bot_access.py` probes with each bot's UA and flags 403s, challenges and stub pages.
Read its docstring: spoofed UAs test UA rules only; IP-verified allowlists behave differently.
Confirm in the dashboard and in logs (`scripts/log_bots.py`).

- **Cloudflare.** New domains have blocked AI crawlers by default since 2025-07-01. Since
  2026-09-15 the new-domain default is *Training + Agent blocked on pages with ads, Search
  allowed*. Cloudflare's 2026-07-01 post says choosing "block Training" **also blocks
  multi-purpose crawlers such as Googlebot, Applebot and Bingbot** — a classic-SEO landmine;
  confirm in the dashboard before advising. Check: Security › Bots / AI Crawl Control
  (per-crawler allow/block, robots-compliance tab), Bot Fight Mode (challenges unverified
  fetchers like Claude-User), managed robots.txt (prepends a training block), Pay-per-crawl
  (HTTP 402), Crawler Hints (IndexNow pings), Markdown for Agents (see §5 — it stamps
  `ai-train=yes` unless the origin sends its own `Content-Signal` header). Cloudflare
  de-listed Perplexity as a verified bot (Aug 2025) — its managed rules may block
  Perplexity-User.
- **Vercel.** AI Bots managed ruleset off by default ("Deny" blocks GPTBot, Claude and all).
  Bot Protection in *Challenge* mode JS-challenges non-browsers. Custom *Bypass* rules run first.
- **Netlify.** User Agent Blocker extension, off by default; presets block AI and SEO bots.
- **Squarespace.** One toggle "Block known AI crawlers" blocks retrieval bots too (off by default).
- **Wix / Shopify / WordPress security plugins / ModSecurity** — frequent hidden blockers;
  check each.
- A 200 "Just a moment…" challenge page is **worse than a 403**: it can be ingested as your
  content. bot_access.py greps for challenge markers.
- Rate limits: 429s on crawl bursts lose pages. Prefer caching and `Crawl-delay` for Anthropic.
- **Web Bot Auth** (RFC 9421 signatures, `Signature-Agent` header): ChatGPT agent signs;
  Google-Agent is experimenting. Don't strip or reject `Signature*` headers; allowlist
  verified signatures rather than UA strings.

## 4. Rendering — what raw HTML must contain

`scripts/render_diff.mjs` loads each page with JS off and on and diffs the main content and
head tags. Pass = <10% of main-content words missing without JS and identical head tags.

Must be in the **initial server HTML**: `<title>`, meta description, canonical, meta robots,
hreflang, JSON-LD, H1, the answer paragraphs, prices/specs, reviews summary, author, dates,
internal `<a href>` links, pagination links.

Breaks for AI fetchers: CSR SPAs (`<div id="root"></div>`); data fetched in `useEffect`/
`onMounted`/SWR; `'use client'` article bodies; `ssr:false`; `client:only` islands; tabs/
accordions whose content is fetched on click (CSS-hidden but present is fine); infinite scroll
without `?page=N` links; `onClick` navigation or `<div>` links; lazy text behind
IntersectionObserver; consent managers that swap the body; head tags set client-side;
**Next.js ≥15.2 streaming dynamic `generateMetadata` into `<body>` for bots not in
`htmlLimitedBots`** (the default list has no AI crawlers) — fixes in `implementation.md`.

Also: SPA hosts that answer 200 with `index.html` for unknown paths create soft 404s; JS that
removes an initial `noindex` never runs (Google may skip rendering noindexed pages); only
200-status pages are queued for rendering; Googlebot reads only the **first 2 MB** of HTML
(and of each JS/CSS file) — giant hydration blobs can push content past the cut.

**Distinct content per URL.** Server-rendered is not enough if every URL serves the same
document (single-document WebGL/motion sites, SPA shells with SSR'd chrome, templated city
pages): engines see identical passages under every URL and nothing specific to cite.
audit.py clusters near-duplicate bodies (5-gram Jaccard > 0.9). **UA switching** (`Vary:
User-Agent`, a Worker choosing documents by UA): bot_access.py warns; the bot and user
documents must carry the same substance or it is cloaking — and it defeats edge caching.
Display type split into one element per letter reads as "S M O O T H" to extractors; split at
runtime, keep real words in the server HTML.

Acceptance test: `curl -sA "GPTBot" URL | sed 's/<[^>]*>//g'` shows the H1, the first answer
paragraph, prices/specs, FAQ answers, author and date.

## 5. llms.txt and markdown for agents

- **llms.txt** (llmstxt.org): H1 name (required) → blockquote summary → optional prose → H2
  link lists `- [name](url): note` → `## Optional`. `llms-full.txt` is a community convention.
  Evidence: no citation effect (see `evidence.md`). **Do**: ship it cheaply on docs/dev-tool/
  SaaS sites (coding agents read it) — `scripts/llms_txt.py` drafts one from the sitemap; the
  human edits it. **Don't**: sell it as GEO, or spend time on it before P0–P2 are done.
- **Markdown content negotiation** is what agents actually request (Claude was 35% of
  markdown requests in one 44-day log study). Serve `text/markdown` when `Accept:
  text/markdown` arrives; send `Vary: Accept`, a `Link: <html-url>; rel="canonical"` header,
  identical substance to the HTML (else cloaking), optionally `<link rel="alternate"
  type="text/markdown">` and a `/sitemap.md`. Cloudflare "Markdown for Agents" (Pro+) does it
  at the edge (set your own `Content-Signal` header if you refuse training); Next.js recipe in
  `implementation.md`. Payload drops ~99% — good for agents with tight context budgets.

## 6. Agentic web — operable, not just readable

Browser agents (ChatGPT agent, Perplexity Comet, Claude in Chrome, Gemini/Google-Agent) read
the DOM and accessibility tree. Rules: native elements (`<a href>`, `<button>`, `<form>`,
`<label for>`, `<select>`, inputs with `name`/`autocomplete`); a stable accessible name on
every control; landmarks and one H1; state in native attributes (`disabled`,
`aria-expanded`, `aria-invalid`); URL-addressable states (filters in query strings); prices,
stock and options as DOM text; no hover-only menus, drag-only controls or canvas-only UIs; no
CAPTCHA on read paths; don't challenge signed agents. Native semantics beat ARIA.

Protocols (platform integrations, not page edits — only when the owner's stack fits):
**MCP** server for product/docs search; **WebMCP** (Chrome origin trial, declarative
`toolname`/`tooldescription` on forms); **NLWeb** (`/ask` over schema.org + RSS);
**ACP** (OpenAI+Stripe checkout; feeds limited to approved partners; native Instant Checkout
wound down Mar 2026); **UCP** (Google, `/.well-known/ucp`, checkout live US/CA/AU via Merchant
Center `native_commerce`); **AP2** (agent payments); **Web Bot Auth**.

## 7. Discovery and freshness plumbing

- **Sitemaps**: ≤50k URLs/50 MB per file, index above that; only canonical 200 indexable URLs;
  `<lastmod>` from the content's real `updated_at` (never build time — audit.py flags >90%
  identical values); `priority`/`changefreq` ignored; referenced from robots.txt.
- **IndexNow** (Bing, Yandex, Seznam, Naver, Yep, Internet Archive, Amazonbot — not Google):
  key file `/{key}.txt`, POST added/updated/deleted URLs to `api.indexnow.org` from the
  publish hook. Fastest freshness lever for Copilot and Bing-grounded answers.
- **RSS/Atom** with full text and real `updated` dates (Google FeedFetcher, NLWeb).
- **HTTP**: single-hop 301/308 for moves; real 404/410; 503 + `Retry-After` for maintenance;
  ETag/Last-Modified + 304; cacheable HTML at the edge (TTFB < ~500 ms); HTML < 2 MB.
- **Paywalls/logins**: content behind login is invisible. Public lead/answer + gated body with
  `isAccessibleForFree:false` + `hasPart.cssSelector`. Serving full text only to Googlebot
  without markup is cloaking. Cookie walls must not replace the HTML body.
- AI crawlers waste ~35% of fetches on 404s and ~14% on redirects — fix broken internal links,
  keep redirects for moved URLs (LLMs also hallucinate URLs; redirect the common ones).

## 8. Logs — the ground truth

`scripts/log_bots.py access.log --verify` classifies hits per bot, verifies IPs against the
owners' published ranges (+ forward-confirmed reverse DNS for Google/Apple/Bing/Common
Crawl), reports status mixes (403/429/5xx = being refused), 404 waste, and **the pages fetched
by user-triggered agents — the closest first-party proxy for "cited in an answer"**.
Opt-out tokens (Google-Extended, Applebot-Extended) never appear in logs.
Metrics per bot: hits/day, unique URLs, status mix, sitemap vs orphan share, first-seen lag
after publish, robots.txt fetch frequency.

## 9. P0 checklist (fail any → fix before content work)

- [ ] `/robots.txt` 200 text/plain for every UA, <500 KiB, no stray `Disallow: /`, named groups repeat shared rules, no Googlebot/Bingbot/Applebot in AI block lists
- [ ] Search + user AI bots allowed; training-bot policy is an explicit owner decision, written in the plan
- [ ] bot_access.py: no BLOCKED/CHALLENGED/DIFFERENT for search/user bots (confirmed in CDN dashboard + logs)
- [ ] render_diff.mjs: main content and head tags present without JS on every key template
- [ ] Each indexable URL has its own distinct primary content (audit.py: no near-duplicate cluster); no UA-switched documents with different substance
- [ ] No unintended `noindex`, `nosnippet`, `max-snippet` < ~160, `noarchive`, `nocache`, `data-nosnippet` around answers (head **or body** — Google honours robots meta outside `<head>` since Mar 2026)
- [ ] Real 404s for unknown URLs; single-hop redirects; one host, https
- [ ] No geo-block/geo-redirect of US traffic; no cookie wall replacing content; no challenge page served with 200
- [ ] Sitemap valid, honest lastmod, referenced in robots.txt; IndexNow wired
