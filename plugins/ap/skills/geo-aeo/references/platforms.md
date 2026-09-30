# Platforms — how each answer engine finds, picks and cites sources

State as of 2026-09-26; this file goes stale fastest. Full fact tables with dates and
sources: `research/02-platforms.md`. Re-verify model names, crawler behaviour and reporting
features before telling an owner anything specific.

---

## The map: five retrieval backbones cover almost everything

1. **Google index** → AI Overviews, AI Mode, Gemini app, Gemini API grounding (and Brave-less
   parts of the long tail via SERP APIs).
2. **Bing index** (exposed to AI as passage-level "Web IQ") → Copilot, Bing AI answers, one of
   ChatGPT's providers, many enterprise agents.
3. **OpenAI's own indexes** ("Labrador" family: web, news by recency, YouTube, Wikipedia,
   local via Yelp/TripAdvisor, shopping…) plus Bing, Google-derived results and others →
   ChatGPT search.
4. **Perplexity's own index** (200B+ URLs, sub-document retrieval) → Perplexity, Comet, its API.
5. **Brave's independent index** → Claude, "Ask Brave", many API-grounded apps. Obeys
   Googlebot's robots rules; no distinct UA.

Meta (meta-webindexer) and Apple (Applebot) are building their own. **A site that is
server-rendered, indexed in Google + Bing + Brave, and doesn't block the search-purpose AI
bots covers nearly the whole market.** Check Brave directly (search.brave.com) — ranking on
Google does not guarantee presence there; submit missing URLs at search.brave.com/submit-url.

Traffic reality (2026): ChatGPT sends ~75% of AI referral clicks; Gemini ~12% and growing
fast; Perplexity ~7% (flat); Copilot ~3.5%; Claude ~2.6% but +320% YoY. AI referrals ≈ 0.3% of
all site visits. Google's AI surfaces reach far more people (AIO >2.5B, AI Mode >1B monthly
users) but report impressions, not clicks. Since a May 2026 ChatGPT UI change, ~62% of
ChatGPT referrals land on **homepages** — the homepage must say plainly what the entity is.

---

## Google AI Overviews & AI Mode
- Index: Google Search, "rooted in core ranking and quality systems"; **query fan-out** (many
  sub-queries in parallel; Deep Search can run hundreds). AI Mode default model: Gemini 3.5
  Flash (May 2026). AIO triggers on ~65% of question-form queries, ~95% of comparison queries,
  ~5% of transactional.
- Eligibility: indexed + snippet-eligible. Nothing else. Controls: `nosnippet`,
  `data-nosnippet`, `max-snippet`, `noindex`, Search Console "Search generative AI" toggle
  (property-level opt-out of AIO, AI Mode and Discover AI; takes 1–2 days; may also lose Top
  Stories inside AIO). Google-Extended does **not** apply.
- Reporting: Search Console **Generative AI performance report** (impressions only; pages,
  countries, devices, dates; no clicks/queries/API; worldwide since 2026-08-31). AI clicks
  are blended into "Web" in the main Performance report. GA4 files AIO/AI Mode traffic under
  Organic Search.
- Do: clean technical SEO; cover the fan-out cluster (definition, cost, comparison, how-to,
  who-for, risks, local specifics); non-commodity material (first-party data, original
  photos/video — YouTube is the #1 AIO-cited domain at ~23%); Merchant Center feeds; Business
  Profile; accurate structured data for rich results. Don't: llms.txt, chunk rewrites or
  "AI schema" *for Google*.

## Gemini app / Gemini API grounding
- Google Search grounding; the model decides whether to search. **Google-Extended disallow
  removes pages from Gemini-app and Vertex grounding** — the one training token with a
  citation cost. Referrer `gemini.google.com` (in GA4's native AI Assistant channel).

## ChatGPT search
- Bots: **OAI-SearchBot** (index; required for citation; ~24h to apply), **ChatGPT-User**
  (live fetch; robots.txt "may not apply" since Dec 2025), **GPTBot** (training only), OAI-
  AdsBot (ad landing pages). None render JS.
- Sources: own index family + Bing/Web IQ + Google-derived results + Yelp (licensed 330M
  reviews, 8M listings, Jul 2026) + TripAdvisor + others. Only ~20–35% of prompts trigger web
  search — the rest is parametric memory, so off-site consensus and being in training data
  matter here more than anywhere.
- Citation mix: third-party "best X" lists ~44% of cited page types for commercial prompts;
  Wikipedia high; Reddit volatile (collapsed twice); LinkedIn rising (~14% of ChatGPT search
  answers). ChatGPT is the most open engine to small/new brands (mentions ρ 0.15 vs AIO 0.65).
- Links carry `utm_source=chatgpt.com`. No publisher dashboard. Shopping: product feeds for
  approved partners (OpenAI JSONL or Google-format files); in-chat checkout via merchant apps
  / Shopify agentic stack. Atlas browser discontinued 2026-08-09 (agentic browsing moved into
  the ChatGPT desktop app).
- Do: allow OAI-SearchBot; SSR everything; be indexed in Bing and Google; complete Yelp/
  TripAdvisor for local; entity-clear homepage; earn third-party list placements; fair
  comparison pages.

## Perplexity
- Own index, **sub-document (passage) scoring**, very high update rate, hybrid lexical +
  semantic retrieval, multi-stage rerank. PerplexityBot (index, not training), Perplexity-
  User (ignores robots.txt; Cloudflare de-listed Perplexity as verified after the 2025
  stealth-crawling report). No JS.
- Citation mix: Reddit, YouTube, niche/regional directories, Gartner-type analyst sources.
- Do: self-contained sections (each H2 answers one question with its facts inline); visible
  accurate dates; check the CDN isn't blocking Perplexity-User. Weight effort by its small
  referral share. Sonar chat-completions API retired 2026-09-27 → Agent API.

## Microsoft Copilot / Bing AI
- Bing index → Web IQ passages + structured evidence objects. Controls: `noarchive` (not used
  in answers), `nocache` (URL/title/snippet only); `data-nosnippet` supported since Oct 2025.
- **Bing Webmaster Tools AI Performance** (the only first-party citation report): total
  citations, cited pages, **grounding queries** (the sub-queries the AI actually ran — feed
  them into the prompt set and content plan), and since June 2026 intents, topics, citation
  share and compare.
- Microsoft's content guidance is the most prescriptive: clear titles/H1/descriptions matched
  to intent; H2/H3 that define content slices; Q&A formats; lists, steps, comparison tables;
  JSON-LD; concise self-contained 1–2 sentence answers; measurable facts; no walls of text;
  **no answers hidden in tabs/accordions, PDFs or images**; no decorative symbols or vague
  superlatives; IndexNow; Bing Places for local.

## Claude
- Web search via **Brave Search**. Claude-SearchBot (index), Claude-User (live; **honours
  robots.txt**), ClaudeBot (training; honours Crawl-delay). No JS. Results expose `page_age`
  (honest dates matter); citations quote ≤150 characters (short, quotable fact sentences).
- Fastest-growing referrer. Do: allow Claude-SearchBot + Claude-User; check Brave presence.

## Apple (Siri, Spotlight, Safari, Apple Intelligence)
- Applebot **renders JS**, falls back to Googlebot rules. Applebot-Extended = training
  opt-out only. `nosnippet` blocks use as AI-answer context. Apple Business (Maps/Siri
  listings; ratings from Yelp and partners). Don't block JS/CSS.

## Meta AI
- meta-webindexer (search index; now a large share of AI crawler traffic — rate-limit, don't
  block), Meta-ExternalAgent (training), Meta-ExternalFetcher (user; may bypass robots).
  Facebook is a top citation source for local answers.

## Grok (xAI)
- Web Search + X Search; no published crawler or robots token. X posts ≈45% of citations
  (vendor data). Do: an active X account stating the same facts as the site.

## Amazon (Alexa+, "Alexa for Shopping" — Rufus retired 2026-05-13)
- Amzn-SearchBot (search; not training), Amzn-User (live), Amazonbot (training + products;
  `noarchive` = no training). For sellers, listing quality (title, bullets, A+, reviews,
  Q&A, use cases) is the lever.

## DeepSeek, You.com, Mistral, DuckDuckGo
- DeepSeek: no published crawler/provider — general web visibility only. You.com: mainly a
  search-API vendor. Mistral: MistralAI-Index/-User/-Training. DuckAssistBot: not training.

---

## Cross-platform table

| Platform | Index | Allow (to be cited) | Safe to block | User fetcher | JS | First-party reporting |
|---|---|---|---|---|---|---|
| Google AIO / AI Mode | Google + fan-out | Googlebot | Google-Extended (no AIO effect) | Google-Agent (ignores robots) | yes | GSC Generative AI report (impressions) |
| Gemini app/API | Google grounding | Googlebot + **Google-Extended** | — | Google-GeminiNotebook | yes | none |
| ChatGPT | own + Bing + others | OAI-SearchBot | GPTBot | ChatGPT-User (may ignore) | no | none (utm_source=chatgpt.com) |
| Perplexity | own | PerplexityBot | — | Perplexity-User (ignores) | no | none |
| Copilot / Bing | Bing / Web IQ | Bingbot | (noarchive/nocache meta) | — | partial | **BWT AI Performance** |
| Claude | Brave | Claude-SearchBot (+ Googlebot rules for Brave) | ClaudeBot | Claude-User (respects) | no | none |
| Apple | Applebot | Applebot | Applebot-Extended | — | yes | none |
| Meta AI | own (building) | meta-webindexer | Meta-ExternalAgent | Meta-ExternalFetcher | likely no | none |
| Grok | web + X | — (none published) | — | — | ? | none |
| Amazon | own + catalogue | Amzn-SearchBot | Amazonbot | Amzn-User (respects) | ? | none |

## Where each platform's third-party trust comes from (volatile — re-check live)

- Google AIO (Sep 2026, share of top-50 cited domains): YouTube 22.9%, Reddit 18.5%,
  Facebook 10.1%, Google 8.8%, Instagram 5.6%, Quora 4.7%, Wikipedia 4.0%, TikTok 3.3%,
  Amazon 3.3%.
- ChatGPT: third-party listicles, Wikipedia, LinkedIn, Forbes/PR wires/Medium (post-2025),
  Yelp/TripAdvisor for local; Reddit volatile.
- Perplexity: Reddit, YouTube, LinkedIn company pages, niche directories, analysts.
- Local answers (US data): Facebook #1 review source behind ChatGPT local, then Yelp,
  TripAdvisor; Gemini leans on the brand's own site + GBP (52% own-site citations).
- Reasoning/"thinking" modes shift away from UGC toward official docs, .gov/.edu and
  standards bodies (government/academic/official share 14% → 26%).

The practical answer to "which platform first": get P0–P2 right once (it serves all of
them), then let `ai_visibility.py` show which engines and which third-party domains matter
for *this* category, and aim the off-site work there.
