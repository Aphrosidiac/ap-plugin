# 07 — Measuring AI Search Visibility and Business Impact (GEO + AEO)

Research dossier for the GEO+AEO skill. Compiled 2026-09-26. Every claim carries a source URL and the date of the source (or the date fetched, "f. 2026-09-26", when the page shows no date). Claims I could not confirm against a primary source are marked **unverified**.

The skill should use this to (1) set a baseline before changing a site, (2) prove or disprove improvement afterwards, and (3) tie visibility to money without overclaiming.

---

## 0. TL;DR for the agent

1. **Never report "rank in ChatGPT."** AI answers are non-deterministic. SparkToro/Gumshoe ran 12 prompts 60–100 times each (2,961 runs across ChatGPT, Claude, Google AI) and found **less than a 1-in-100 chance** of getting the same brand list twice, and about **1 in 1,000** of getting the same order. Fishkin: "any tool that gives a 'ranking position in AI' is full of baloney." What they found usable is **visibility %** (how often a brand appears across many runs of many prompts). [sparktoro.com/blog/new-research-ais-are-highly-inconsistent…, 2026-01-28]
2. **Four first-party data sources now exist. Use them before any paid tool:**
   - **Google Search Console, Generative AI performance report.** Impressions only, for AI Overviews and AI Mode (and a separate Discover report), broken down by page, country, device and date. No clicks, queries or position, and no API. Worldwide since 2026-08-31. [support.google.com/webmasters/answer/16984139, f. 2026-09-26; searchenginejournal.com/…/587836, 2026-09]
   - **Bing Webmaster Tools, AI Performance.** Citation counts, average cited pages, page-level citations, and sampled "grounding queries" across Copilot, Bing AI summaries and some partners. No clicks. [blogs.bing.com/webmaster/February-2026/…, 2026-02-10]
   - **GA4's native "AI Assistant" default channel** (since 2026-05-13). It sets medium to `ai-assistant` and campaign to `(ai-assistant)`. The documented sources are ChatGPT, Gemini, Deepseek, Copilot and Grok. **Perplexity is not listed, and Claude's inclusion is uncertain.** It is not retroactive. [support.google.com/analytics/answer/9756891, f. 2026-09-26; searchenginejournal.com/…/574974, 2026-05-14]
   - **Server logs.** `ChatGPT-User`, `Perplexity-User` and `Claude-User` are fetches triggered by a live user question. Treat them as a proxy for "my page was retrieved to answer someone."
3. **Programmatic sampling is cheap:** $10 per 1k searches on Anthropic; $10 per 1k calls (reasoning models) or $25 per 1k (non-reasoning) on OpenAI; $14 per 1k search queries on Gemini 3.x after 5,000 free a month; $2.50 per 1k on Perplexity's Agent API web_search. Token costs come on top in every case. **But API answers are not what consumers see**, so calibrate against a UI sample.
4. **Size the sample for the effect you want to detect.** Detecting a +10-point change in mention rate (30%→40%) at 80% power needs about **350 prompt-runs per period, per engine**. Detecting +5 points needs about 1,400.
5. **Impact context.** Ahrefs measured a −58% position-1 CTR when an AI Overview is present (Dec 2025 vs Dec 2023, 300k keywords). Seer found **cited** brands get about 2.07% organic CTR against 0.94% for uncited brands (+120%). AI referral conversion premiums range from −13% (a Marketing Science study of 973 ecommerce sites) to 23x (Ahrefs' own site). Treat any premium as a hypothesis for the specific site, not a law.

---

## 1. Metric dictionary (definitions + formulas)

Notation: P = prompt set, E = engines, R = runs per prompt per engine, and an *answer* is one run's output.

| Metric | Formula | Notes / source |
|---|---|---|
| **Mention rate** (brand visibility %) | answers mentioning brand ÷ total answers | The metric SparkToro endorses as the reasonable one. Mention means the brand name appears anywhere in the text. [SparkToro 2026-01-28] |
| **Citation rate** | answers containing ≥1 URL on your domain in citations/sources ÷ total answers | The same brand can be mentioned without a link. Ahrefs found **citation rates of 10.7% (AI Overviews) to 51.6% (Perplexity), about 28% on average**, among brand mentions. [ahrefs.com/blog/ai-citations-vs-impressions-study, 2025-11-26] |
| **Citation share** | your-domain citations ÷ all citations in the answer set | Also compute it per URL. This is the equivalent of Bing's "citations" count. |
| **Share of voice (SoV)** | your mentions ÷ mentions of all tracked brands in the category × 100 | Semrush's definition. Its Enterprise SoV also weights by position (and, for ChatGPT, by topic search volume). [semrush.com/blog/how-to-measure-ai-share-of-voice, 2026-07-17] |
| **Position-weighted SoV** | Σ over answers of 1/rank(brand) ÷ Σ over brands of Σ 1/rank | Use only aggregated over many runs, because order is close to random per run. [SparkToro 2026-01-28] |
| **Prominence score** | 3 = first entity or explicitly recommended, 2 = named in the body with a description, 1 = listed/footnote/source only, 0 = absent | Use an LLM-judge rubric and spot-check it by hand. |
| **Recommendation rate** | answers where the brand is explicitly recommended or ranked "best/top" ÷ answers for recommendation-intent prompts | Separate from mention rate. A negative mention is still a mention. |
| **Sentiment** | share of mentions that are positive, neutral or negative (LLM-judge, 3-class) | Semrush classifies mentions as favorable, general or negative. [Semrush 2026-07-17] |
| **Accuracy / hallucination rate** | answers with a factual error about the brand (price, features, location) ÷ answers mentioning the brand | Check against a fact sheet of ground-truth claims. |
| **Search-volume-weighted visibility** | Σ (mention × prompt's demand weight) | Ahrefs: "You might get linked only 20% of the time, but because those links appear on high-volume queries, way more than 20% of people actually see your citations." [Ahrefs 2025-11-26] |
| **AI referral sessions** | GA4 sessions in the AI channel (native + custom) | Treat as a **floor**. Seer calls custom-channel numbers a "directional floor rather than precise count." [seerinteractive.com/insights/are-ai-sites-like-chatgpt-sending-your-website-traffic, updated 2026-06-22] |
| **AI conversions / revenue** | key events or revenue in the AI channel; conversion rate compared with organic | Always compare against **non-brand organic** too, not just all organic. Visibility Labs used non-branded organic as its comparator. [relevantaudience.com summary, f. 2026-09-26] |
| **GSC AI impressions** | Generative AI report impressions (property or page level) | Property level counts several URLs in one response as one impression, so page-level impressions don't sum to the property total. [searchenginejournal.com/google-reports-ai-search-impressions-how-to-read-them/582824, 2026-06] |
| **Bing citations / cited pages** | BWT AI Performance | Sampled data, and "not ranking or page importance." [blogs.bing.com, 2026-02-10] |
| **AI retrieval fetches** | log hits by `ChatGPT-User`, `Perplexity-User`, `Claude-User` on verified IPs | This is a proxy (see §6.4). |

---

## 2. What the platforms themselves report (2026)

### 2.1 Google Search Console

- **The main Performance report already includes AI features.** Google: sites appearing in AI features "are included in the overall search traffic in Search Console … reported on in the Performance report, within the 'Web' search type." So AI Overview and AI Mode clicks and impressions are **blended into Web totals and can't be separated there.** [developers.google.com/search/docs/appearance/ai-features, last updated 2025-12-10]
- **Generative AI performance report.** Announced 2026-06-03 as a UK pilot, expanded in July, and rolled out to all sites worldwide on 2026-08-31. [developers.google.com/search/blog/2026/06/gen-ai-performance-reports, 2026-06; searchenginejournal.com/google-search-console-ai-reports-rolled-out-worldwide/587836, 2026-09]
  - **Metric:** impressions only, defined as "how many times links to your site were shown to a user in a generative AI feature on Google Search." [support.google.com/webmasters/answer/16984139, f. 2026-09-26]
  - **Dimensions:** Pages (canonical URL), Countries, Dates (daily, weekly or monthly, in Pacific Time), and Devices. Coverage is AI Overviews and AI Mode; Search Labs experiments are excluded. The usual 1,000-row limit applies, and there is an export button. [same]
  - There is a **separate Discover report** for generative AI features in Discover. [SEJ 587836]
  - **Not available:** clicks, CTR, queries, position, and API access. At the time of writing, the Search Analytics API `type` accepts only web, image, video, news, discover and googleNews. [cogny.com / SEJ summaries via search, 2026; **unverified** against the API reference] The UK CMA expects click data to be added, and has set March 2027 for page-level AI controls. [SEJ 587836]
  - **How to use it:** for each page, compare AI impressions with organic Web impressions and clicks from the main report, using the same page, country and date range. A page whose AI impressions are rising while Web clicks fall is a candidate for "cited but not clicked." SEJ's advice is to use it as "a diagnostic lens, not a new scoreboard." [SEJ 582824]
- **Google's own position.** Liz Reid (2025-08-06) said total organic click volume is "relatively stable year-over-year" and that "average click quality has increased." [blog.google/products/search/ai-search-driving-more-queries-higher-quality-clicks, 2025-08-06] Third-party data disagrees (§8).

### 2.2 Bing Webmaster Tools, AI Performance (public preview)

- Launched 2026-02-10 or 11. Metrics:
  - **Total Citations:** the number of times your pages are "displayed as sources in AI-generated answers."
  - **Average Cited Pages:** unique pages cited per day.
  - **Grounding Queries:** a sample of the internal queries the AI issued to retrieve your content. These are not the user's prompts.
  - **Page-level citation activity.**
  - It covers Microsoft Copilot, AI summaries in Bing, and "select partner integrations." There are no clicks, and the data is sampled. [blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview, 2026-02-10]
- **Practical use.** Export grounding queries and classify them as branded or non-branded and by funnel stage. Otterly's own domain showed 29.7% branded, 70.3% non-branded and 47% consideration-stage. Map them to content gaps and feed them into your prompt set. [otterly.ai/blog/bing-webmaster-tools-ai-performance-report, 2026]
- Bing recommends IndexNow to keep content fresh in its AI systems. [blogs.bing.com 2026-02-10]

### 2.3 Others

- **OpenAI, Perplexity, Anthropic and Gemini-app** do not offer publisher dashboards as of 2026-09. **Unverified** as a negative; I found no official publisher console.
- ChatGPT appends `utm_source=chatgpt.com` to links it cites from live search. Tagging expanded in June 2025 and is not universal: links recalled from training data may lack it. [rankshift.ai & lawrencehitches.com summaries via search, 2025–2026; **partly unverified**, no OpenAI primary page fetched]
- **ChatGPT UI change, May 2026:** brand names became clickable, and homepage referrals rose "from roughly 26–29% of all referral traffic … to about 62–63%." **Implication:** AI referral landings now skew to the homepage, so page-level attribution of AI traffic to cited articles is weakening. [aisearch.similarweb.com/blog/gen-ai-stats, 2026-07-29]

---

## 3. Building the prompt set

### 3.1 Derivation pipeline

1. **Seed from demand you already have:**
   - GSC queries (last 16 months). Keep **question-form and long queries (≥5 words)**, and comparison queries.
   - Bing grounding queries (§2.2).
   - Site search logs, sales-call and support transcripts.
   - "People also ask" questions.
2. **Convert keywords into conversational prompts.** Users write longer, contextual prompts to AI. Template it: `[persona context] + [task] + [constraints]`. For example, the keyword "crm for small business" becomes "I run a 6-person plumbing company in Leeds and need a CRM under £50/month that works on phones. What should I use?"
3. **Stratify by funnel stage and intent.** Suggested mix for a 100-prompt core set:

| Stratum | Share | Example | Primary metric |
|---|---|---|---|
| Category / problem discovery (unbranded, informational) | 30% | "how do I stop condensation on windows" | citation rate |
| Solution / "best X for Y" (unbranded, commercial) | 30% | "best dehumidifier for a small flat UK" | mention + recommendation rate |
| Comparison / alternatives | 15% | "Brand vs Competitor", "alternatives to Competitor" | SoV, sentiment |
| Branded fact checks | 15% | "does Brand ship to Ireland", "Brand pricing" | accuracy |
| Transactional / local | 10% | "where to buy X near Manchester" | citation + mention |

   Seer's AIO prevalence data supports weighting comparison and question prompts. AI Overview rate was 95.4% for comparison queries, 85.9% for question-format, 36% for informational overall, and 5% for transactional. [seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update, 2026-04-24]
4. **Personas.** Write 3–5 personas (role, geography, sophistication) and phrase each core intent 2–3 ways. SparkToro found humans phrase the same need very differently. [SparkToro 2026-01-28]
5. **Competitor set.** List 5–15 named competitors plus aliases and misspellings for entity matching.
6. **Freeze and version.** Store `prompts.csv` with columns `id, text, stratum, persona, locale, demand_weight, added_on`. **Never edit a prompt mid-experiment.** Add new ones as new IDs.

### 3.2 Sample size and repetitions (non-determinism)

- SparkToro recommends **60–100 runs per prompt** for stable per-prompt visibility. Visibility across "dozens to hundreds of prompts run multiple times" is a reasonable metric. [SparkToro 2026-01-28]
- A practical compromise: **many prompts × few runs** (for example 100 prompts × 5 runs × 4 engines = 2,000 answers per wave). This beats few prompts × many runs for estimating overall visibility, and it averages over phrasing variance.
- **Confidence intervals (Wilson or normal approximation), 95%, at p ≈ 0.5:**

| n answers | ± margin |
|---|---|
| 10 | ±31 pp |
| 30 | ±18 pp |
| 100 | ±10 pp |
| 500 | ±4.4 pp |
| 2,000 | ±2.2 pp |

- **Power for pre/post difference** (two-proportion, α = 0.05, power 0.8): n per period ≈ 7.84 × [p1(1−p1) + p2(1−p2)] ÷ (p2−p1)².
  - 30%→40% needs **about 353** answers per period.
  - 30%→35% needs **about 1,372**.
  - 10%→15% needs **about 686**.
  - Because runs of the same prompt are correlated, compute a **cluster-robust SE clustered by prompt**, or use a mixed model with a random intercept per prompt. (Standard statistics, derived here.)
- **Cadence.** Run a wave weekly, or at least biweekly, on the same weekday, with every engine in the same time window. Semrush's Brand Performance data updates weekly. [semrush.com/blog/how-to-measure-ai-share-of-voice, 2026-07-17]

### 3.3 Location, personalisation and surface effects

- **Location.** Every API exposes a location parameter: OpenAI `user_location`, Anthropic `user_location`, Perplexity `filters` location, and SerpApi and DataForSEO `location`. Fix the locale per prompt and record it. Semrush reports SoV across "68,000+ location-language combinations," which implies answers vary materially by locale. [semrush KB via search, 2026]
- **Personalisation.** Consumer ChatGPT, Gemini and Claude can use memory, custom instructions and chat history. APIs do not. Logged-out consumer sessions are closest to the API but still differ in model routing and search backend. **Unverified** as quantified; I found no public controlled study in this pass.
- **API vs UI.** Some vendors (for example Profound) collect via "browser-level answer collection that mimics real user sessions rather than leaning on APIs." Others use APIs or a hybrid. [geotoolbox.ai/blog/best-ai-visibility-tools, updated 2026-09-10] Treat API measurement as a **consistent instrument for trend**, not as ground truth for what consumers see. Calibrate each quarter by running 20–30 prompts by hand in logged-out UI sessions and checking whether the API-based mention rate and the UI-based rate move together.
- **Google AI Overviews and AI Mode cannot be queried via an official API.** The Gemini API's grounding is Google Search but not AIO. Use SERP APIs (§4.6) to observe the real surfaces.
- **Ads.** About 26% of ChatGPT responses contained ads in Similarweb's 2026 data. Exclude ad units when you extract organic mentions. [aisearch.similarweb.com/blog/gen-ai-stats, 2026-07-29]

---

## 4. Programmatic measurement: exact API shapes

All model names and prices below were fetched from official docs on 2026-09-26. **Re-check model IDs at run time**, because they change quickly.

### 4.1 OpenAI: Responses API + `web_search` tool

Source: developers.openai.com/api/docs/guides/tools-web-search (f. 2026-09-26). The docs' examples use `gpt-6-astra`. Pricing is at developers.openai.com/api/docs/pricing (f. 2026-09-26):
- **Reasoning models:** $10 per 1k web-search calls, plus search content tokens billed at model rates.
- **Non-reasoning models:** $25 per 1k calls, with search content tokens free.
- Flagship listings: gpt-6-astra at $10 in / $50 out per 1M tokens; gpt-6-luna at $0.10 in / $0.50 out.

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-6-luna",
    "input": "What are the best project management tools for a 10-person agency?",
    "tools": [{
      "type": "web_search",
      "search_context_size": "medium",
      "user_location": {"type":"approximate","country":"GB","city":"London","region":"London"}
    }],
    "include": ["web_search_call.action.sources"]
  }'
```

- **Inline citations:** `output[] → type:"message" → content[] → annotations[]` entries of `{"type":"url_citation","start_index":…,"end_index":…,"url":…,"title":…}`.
- **Full consulted list:** with `include:["web_search_call.action.sources"]`, the `web_search_call` output items carry `action.sources[]`. The docs say "Unlike inline citations, which show only the most relevant references," sources are the complete list the model consulted. Record **both**: cited means shown to the user, while sourced means retrieved.
- **Other options:** `filters.allowed_domains` accepts up to 100 domains (useful for "does my domain ever get picked" tests; not for baseline). There is a 128k-token search context cap. Web search is unavailable with `gpt-5` at `minimal` reasoning, and `web_search_preview` doesn't support filters.

Extraction (Python):
```python
cited, sourced = [], []
for item in resp.output:
    if item.type == "web_search_call" and getattr(item.action, "sources", None):
        sourced += [s.url for s in item.action.sources]
    if item.type == "message":
        for c in item.content:
            for a in (c.annotations or []):
                if a.type == "url_citation":
                    cited.append(a.url)
```
Also strip `?utm_source=openai` or similar before matching domains. Normalise with `urllib.parse`: lowercase host, drop `www.`.

### 4.2 Anthropic: Messages API + web search server tool

Source: platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool (f. 2026-09-26).
- **Versions:** `web_search_20250305` (basic), `web_search_20260209` (dynamic filtering via code execution), and `web_search_20260318` (adds `response_inclusion`).
- **Pricing:** **$10 per 1,000 searches** plus tokens. Batches API is supported at the same price, but web search is throttled per org there.

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-5-5",
    "max_tokens": 2048,
    "messages": [{"role":"user","content":"Best accounting software for UK sole traders?"}],
    "tools": [{
      "type": "web_search_20250305", "name": "web_search", "max_uses": 5,
      "user_location": {"type":"approximate","city":"London","country":"GB","timezone":"Europe/London"}
    }]
  }'
```

- **Retrieved sources:** `content[]` blocks of `type:"web_search_tool_result"` hold `content[]` entries `{type:"web_search_result", url, title, page_age, encrypted_content}`.
- **Cited:** `content[]` blocks of `type:"text"` with `citations[]` entries `{type:"web_search_result_location", url, title, cited_text (≤150 chars), encrypted_index}`.
- The queries issued are in the `server_tool_use.input.query` blocks. They are useful for learning the fan-out queries, similar to Bing grounding queries.
- **Errors return HTTP 200** with `web_search_tool_result_error` (`max_uses_exceeded`, `too_many_requests`, …). Detect and retry these, or the gap will silently read as "not cited."
- For measurement, use `web_search_20250305` or set `allowed_callers:["direct"]` on newer versions. That avoids dynamic filtering, which changes what gets surfaced. (Design recommendation.)

### 4.3 Google Gemini API: Grounding with Google Search

Sources: ai.google.dev/gemini-api/docs/google-search (Interactions API, f. 2026-09-26), ai.google.dev/gemini-api/docs/generate-content/google-search (legacy generateContent, f. 2026-09-26), and ai.google.dev/gemini-api/docs/pricing (f. 2026-09-26).
- **Models:** Gemini 3.8, 3.7 and 3.6 Flash; 3.5 Flash and Flash-Lite; 2.5 Pro, Flash and Flash-Lite; 2.0 Flash.
- **Pricing:**
  - **Gemini 3.x:** 5,000 free search requests per month shared across the family, then **$14 per 1,000 search queries**. Every query the model issues is billed, so one prompt can bill several.
  - **Gemini 2.5 Flash:** 1,500 RPD free, then **$35 per 1,000 grounded prompts**.
- Search suggestions (`searchEntryPoint` / `search_suggestions`) carry display requirements under the ToS if you **show** results to users. For internal measurement you only log them.

New Interactions API:
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"gemini-3.8-flash","input":"Best running shoes for flat feet?","tools":[{"type":"google_search"}]}'
```
The response has `steps` of type `google_search_call` (queries), `google_search_result`, and model output with `annotations` of `url_citation` (`start_index`, `end_index`).

Legacy generateContent (widely used, richer metadata):
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" -X POST \
  -d '{"contents":[{"parts":[{"text":"Best running shoes for flat feet?"}]}],"tools":[{"google_search":{}}]}'
```
Read `candidates[0].groundingMetadata`:
- `webSearchQueries[]`: the fan-out queries.
- `groundingChunks[].web.{uri,title}`: the sources.
- `groundingSupports[].{segment:{startIndex,endIndex,text}, groundingChunkIndices[]}`: which chunk supports which sentence.
- `searchEntryPoint.renderedContent`.

**Trap:** `web.uri` is a `vertexaisearch.cloud.google.com/grounding-api-redirect/...` URL, not the real page. [github.com/googleapis/python-genai/issues/1512, f. 2026-09-26]
- Use `web.title`, which is usually the domain.
- Or resolve it with a HEAD request (don't follow) and read the `Location` header.
- Store the resolved URL, because the redirects expire. **Unverified** expiry window.

### 4.4 Perplexity: Agent API (Sonar is being retired)

- **Deprecation.** The Sonar API reference notes: "Sonar Chat Completions is now Agent API. Sonar will be supported until **September 27, 2026**." That is the day after this dossier's date. **Do not build new tooling on `/chat/completions` with `sonar` or `sonar-pro`.** [docs.perplexity.ai/api-reference/chat-completions-post, f. 2026-09-26]
- **Legacy Sonar response fields (for migrating old data):** a top-level `citations[]` of URLs, plus `search_results[]` of `{title,url,date,snippet}`. Models were `sonar`, `sonar-pro`, `sonar-reasoning-pro` and `sonar-deep-research`. [same]
- **Agent API:** `POST https://api.perplexity.ai/v1/agent`, with `/v1/responses` accepted as an OpenAI-SDK alias. It takes third-party models (for example `openai/gpt-5.6-sol`). [docs.perplexity.ai/getting-started/quickstart, f. 2026-09-26; docs.perplexity.ai/docs/agent-api/quickstart via search]
- **web_search tool:** [docs.perplexity.ai/docs/agent-api/tools/web-search, f. 2026-09-26]

```bash
curl https://api.perplexity.ai/v1/agent \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "<model id from docs.perplexity.ai/docs/getting-started/models>",
    "input": "Best CRM for UK tradespeople? Cite your sources inline using bracketed markers, one source per bracket, like [1][2].",
    "tools": [{"type":"web_search","search_type":"web","search_context_size":"medium","max_results":10,
               "filters":{"country":"GB"}}]
  }'
```
- **Options:** `search_type` is `web` ($2.50 per 1k) or `fast` ($1.00 per 1k). `search_context_size` is low (300 tokens), medium (1,000) or high (4,000). `max_results` is 1–50. `filters` covers domains (≤20, with a `-` prefix to exclude), recency, date ranges and location. The filter field names above are **partly unverified**; check the reference.
- **Results:** `search_results[]` entries are `{id,url,title,snippet,date,last_updated}`, and `annotations[]` carry `url`.
- Perplexity says inline markers depend on the prompt, and to "treat the id and url fields of each search_results entry as the source of truth for citations." [search summary of the Perplexity docs, 2026] **Note:** the Agent API with a non-Perplexity model does not reproduce perplexity.ai's consumer answers. For those, use a UI-collecting vendor.

### 4.5 Bing and Brave

- **Bing Search APIs were retired on 2025-08-11.** The replacement is "Grounding with Bing Search" inside Azure AI Agents. [learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement, 2025-05-15] For Copilot visibility, use BWT AI Performance (§2.2).
- **Brave Search API** has `/res/v1/web/search` and an **LLM Context API** at `/res/v1/llm/context`, with auth header `X-Subscription-Token`. It returns results (`title, url, description, extra_snippets`), not a consumer answer. It is useful as a retrieval-layer proxy (Claude's consumer search has been reported to use Brave; **unverified**). [api-dashboard.search.brave.com/app/documentation/web-search/get-started, f. 2026-09-26]

### 4.6 SERP APIs for Google AI Overviews and AI Mode (the real Google surfaces)

**SerpApi, AI Mode:** `GET https://serpapi.com/search?engine=google_ai_mode&q=...&api_key=...` [serpapi.com/google-ai-mode-api, f. 2026-09-26]
- It returns `text_blocks` and `references[]` of `{title, link, snippet, source, index}`, and text blocks carry `reference_indexes`.
- `device` can be desktop, tablet or mobile. Setting `continuable=true` returns a `subsequent_request_token` for multi-turn.
- Cached results last 1h and are free, so pass `no_cache=true` for fresh measurement.

**SerpApi, AI Overview:** [serpapi.com/google-ai-overview-api, f. 2026-09-26]
- Step 1: run `engine=google`. If the AIO loads asynchronously, the response gives `ai_overview.page_token`.
- Step 2: within **1 minute**, call `engine=google_ai_overview&page_token=...`.
- The response gives `references[]` (`title, link, snippet, source, index`) and `text_blocks[].reference_indexes`.
- Record "AIO present" (yes/no) as its own metric per keyword.

**DataForSEO:** [docs.dataforseo.com/v3/serp-google-ai_mode-overview, f. 2026-09-26; dataforseo.com/solutions/geo, f. 2026-09-26]
- **AI Mode:** `POST /v3/serp/google/ai_mode/live/advanced`, or `task_post` / `task_get` (cheaper). Up to 100 tasks per POST and 2,000 calls per minute.
- **AI Overviews:** the Organic SERP Advanced API (`/v3/serp/google/organic/live/advanced`) returns an `ai_overview` item with `references` (`url, domain, title, source`); field names are **partly unverified**.
- **Prices:** Google AI Mode SERP from $0.0012 per SERP.
- **AI Optimization API:**
  - **LLM Responses:** raw ChatGPT, Claude, Gemini and Perplexity answers for custom prompts, from $0.0006 per task.
  - **LLM Mentions:** mentions across ChatGPT and AIO from a large prompt database, from $0.001 per row.
  - **AI Keyword Data:** search volume, from $0.11 per 1k keywords.
- Example body:
```json
[{"keyword":"best crm for plumbers","location_code":2826,"language_code":"en","device":"desktop"}]
```
(2826 = United Kingdom.)

### 4.7 Minimal harness design (for the skill)

```
for wave in schedule:
  for prompt in prompts (frozen v-id):
    for engine in [openai, anthropic, gemini, perplexity, serp_aio, serp_aimode]:
      for r in range(R):          # R=3–5 API engines; R=1 for SERP (it is an index snapshot)
        raw = call(engine, prompt, locale)
        store raw JSON (immutable) + timestamp + model id + tool version
        parse -> {cited_urls[], sourced_urls[], fanout_queries[], answer_text}
        entity-match brands (aliases, case-insensitive, word boundaries) -> mentions[], first_position
        LLM-judge -> prominence(0–3), recommended(bool), sentiment(-1/0/1), factual_errors[]
aggregate by engine × stratum × wave with prompt-clustered CIs
```
Store raw responses, so a better parser can re-score history later. Pin the model ID per wave and log it. A **model change counts as an instrument change**, so annotate it on charts.

---

## 5. Tools landscape (2026-09)

Prices below are entry tiers as published; vendors repriced often in 2026. The geotoolbox comparison notes "several of these vendors repriced or repackaged within the last quarter." [geotoolbox.ai/blog/best-ai-visibility-tools, updated 2026-09-10; get-ryze.ai/blog/ai-visibility-tools-pricing-compared-2026, 2026-08-29]

| Tool | What it measures | Engines | Collection | Entry price (2026) |
|---|---|---|---|---|
| **Profound** | Answer Engine Insights (visibility score, SoV, citations, sentiment, competitor comparison); **Conversation Explorer** ("1.5B+ real user conversations," prompt volume); **Agent Analytics** (server-log AI bot and human-referral analytics via Cloudflare, Vercel, Akamai, AWS, GCP, Fastly, Netlify, WordPress, Shopify, Adobe, with GA4 integration) | ~10 answer engines | Browser-level UI collection | $99 / $399, annual only [tryprofound.com/features/agent-analytics, f. 2026-09-26; nicklafferty.com summaries; ryze 2026-08-29] |
| **Peec AI** | Mentions, citations/sources, position, sentiment, competitors | Pick 3 models at entry | **unverified** | €85–95 / $245 / $495 (50/150/350 prompts) [ryze; geotoolbox] |
| **Otterly.AI** | Mentions, citations, brand ranking, domain citations; Bing AIP guidance | 4 engines standard | **unverified** | $29 / $189 / $489 (15/100/400 prompts) [ryze] |
| **Semrush AI Visibility Toolkit / Enterprise AIO** | Mentions, citations, SoV (position-weighted in Enterprise), sentiment, topic coverage; weekly updates; 68k+ location-language combos | ChatGPT, AI Overviews, AI Mode, Gemini, Perplexity | Mixed | $99 per domain (25 prompts) [ryze; semrush.com/blog/how-to-measure-ai-share-of-voice 2026-07-17] |
| **Ahrefs Brand Radar** | Mentions and citations from a large pre-run prompt index (reported ~14M monthly ChatGPT prompts; "460M+" total in one review); citation types (owned/earned/social); demand-weighted impressions | ChatGPT, Perplexity, Gemini, Copilot, AIO, AI Mode (no Claude or Grok as of Jul 2026) | Pre-built index, **not your own prompts** by default | $199–$699 [ryze; search summaries of rankability/tryprofound reviews 2026] |
| **Scrunch** | Visibility, SoV, sentiment, crawler/agent reachability; "Agent Experience Platform" serving agent-readable pages | Multiple | **unverified** | $250–300 / $500 [geotoolbox; ryze] |
| **AthenaHQ** | Visibility, SoV, sentiment; content-optimisation agent | 5–11 models incl. Claude, DeepSeek, Mistral | **unverified** | Free tier (300 credits), then $295 ($245 annual) [ryze; geotoolbox] |
| **Goodie AI** | AI visibility monitoring + optimisation | **unverified** | **unverified** | **unverified** (no primary data found this pass) |
| **Conductor (AI Search Performance)** | AI visibility, mentions, sentiment, competitors inside the enterprise SEO suite | Multiple | **unverified** | Enterprise quote [conductor.com/platform/features/ai-search-performance, f. 2026-09-26] |
| **BrightEdge AI Catalyst** | Brand visibility across AIO, Copilot/Bing, ChatGPT, Claude, Perplexity | 6+ | **unverified** | Enterprise quote [brightedge.com/blog/introducing-brightedge-ai-catalyst…, f. 2026-09-26] |
| **Similarweb (AI Brand Visibility + AI Chatbot Traffic)** | Panel-based estimates of AI chatbot referrals to any domain (yours or competitors'), top referred pages, "top prompts"; brand visibility tracker | ChatGPT, Gemini, Perplexity, AI Mode | Clickstream panel + prompt tracking | Enterprise [aisearch.similarweb.com/ai-brand-visibility, f. 2026-09-26] |
| **Rankscale** | Mentions/citations across ~10 engines | 10 | **unverified** | €20 [geotoolbox] |
| **DataForSEO / SerpApi (DIY)** | Raw AIO, AI Mode and LLM responses | See §4.6 | API | Pay per call |
| **Free** | GSC Gen-AI report; BWT AI Performance; GA4 AI Assistant channel + custom group; server logs; Semrush free AI visibility checker [semrush.com/free-tools/ai-search-visibility-checker]; AthenaHQ free tier; DIY API harness (≈$10–30 per 1k answers) | — | — | $0 to low |

**Selection guidance.**
- If the brand needs **its own prompts** and a **UI-realistic** view, choose Profound, Peec, Otterly or Scrunch.
- If the goal is **market-level benchmarking** without authoring prompts, choose Ahrefs Brand Radar or Similarweb.
- If the goal is **traffic attribution**, use GA4 plus server logs, or Profound Agent Analytics.
- Fishkin's advice: before buying, demand vendor "stats-backed, publicly-reviewable research" on the variance question. [SparkToro 2026-01-28]

---

## 6. Analytics: attributing AI traffic

### 6.1 GA4 native "AI Assistant" channel

- Added **2026-05-13** and rolled out gradually. [searchenginejournal.com/google-analytics-adds-ai-assistant-as-default-channel-group/574974, 2026-05-14]
- **Definition:** "users arrive at your site from sources like ChatGPT, Gemini, Deepseek, Copilot, or Grok. It **excludes Google's AI Overviews and AI Mode**." The rule is that medium exactly matches `ai-assistant`. GA4 sets medium to `ai-assistant` and campaign to `(ai-assistant)` when the referrer matches its AI-assistant list. [support.google.com/analytics/answer/9756891, f. 2026-09-26]
- **Gaps:**
  - It is **not retroactive**.
  - **Perplexity is not in the documented list.** Claude was named at launch but is missing from the live definition. [terminusapp.com/blog/ai-traffic-channel-in-ga4, 2026-07-09; SEJ 574974]
  - Anything without a referrer still goes to Direct.
- **Traffic from AI Overviews and AI Mode lands in Organic Search** and can't be separated in GA4. Use GSC for it.

### 6.2 Custom channel group (keep it alongside the native one)

Admin → Data display → Channel groups → create "AI (custom)". Add a channel with **Session source matches regex**, and **place it above Referral** ("Rules evaluate top down and first match wins"). Custom channel groups apply to historical data; standard properties allow 2 custom groups. [terminusapp.com, 2026-07-09] GA4 uses RE2 and full-match semantics for "matches regex."

Source regex (Terminus, verbatim, 2026-07-09):
```
^(claude\.ai|perplexity\.ai|www\.perplexity\.ai|meta\.ai|you\.com|poe\.com|chatgpt\.com|chat\.openai\.com|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|chat\.deepseek\.com|grok\.com)$
```
Extended version recommended for the skill. It is my synthesis; test it in GA4 with DebugView before relying on it:
```
^(chatgpt\.com|chat\.openai\.com|openai|perplexity(\.ai)?|www\.perplexity\.ai|claude\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|copilot\.cloud\.microsoft|edgeservices\.bing\.com|chat\.deepseek\.com|deepseek\.com|grok\.com|x\.ai|meta\.ai|you\.com|poe\.com|phind\.com|kagi\.com|chat\.mistral\.ai|duck\.ai)$
```
- Include the bare `openai` source because `utm_source=openai` appears on some OpenAI-originated links (**unverified**). Remove it if it collides with non-citation traffic.
- Terminus deliberately excludes `openai.com`, `anthropic.com`, `google.com` and `x.ai`, which carry non-citation traffic such as docs readers and sign-ins. [terminusapp.com 2026-07-09]
- **Second rule (same channel, OR):** Session manual source matches regex `^(chatgpt\.com|perplexity|claude|gemini|copilot)`. This catches `utm_source=chatgpt.com`, which ChatGPT appends to search-cited links even when the referrer is stripped. [rankshift.ai / lawrencehitches.com summaries, 2025–2026]

Exploration or BigQuery check (GA4 export):
```sql
SELECT
  collected_traffic_source.manual_source AS utm_source,
  traffic_source.source AS first_user_source,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key='page_referrer') AS referrer,
  COUNT(DISTINCT CONCAT(user_pseudo_id, CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') AS STRING))) AS sessions
FROM `project.analytics_XXXX.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20260801' AND '20260925'
  AND event_name = 'session_start'
  AND REGEXP_CONTAINS(COALESCE((SELECT value.string_value FROM UNNEST(event_params) WHERE key='page_referrer'),'') || ' ' || COALESCE(collected_traffic_source.manual_source,''),
      r'(chatgpt\.com|chat\.openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|deepseek\.com|grok\.com|meta\.ai|you\.com|poe\.com)')
GROUP BY 1,2,3 ORDER BY sessions DESC;
```

### 6.3 Dark AI traffic

Sources of loss:
- In-app browsers and mobile apps (the ChatGPT, Perplexity and Gemini apps) often send no referrer.
- Users copy and paste URLs.
- Some free-tier or privacy contexts strip the referrer.
- Sensitive medical, legal and financial topics may drop UTMs.

[seerinteractive.com/insights/are-ai-sites-like-chatgpt-sending-your-website-traffic, updated 2026-06-22; SEJ 574974]

Estimation tactics (heuristics; **unverified** as validated methods):
1. **Direct-traffic anomaly on deep pages.** Direct sessions landing on long-tail article URLs (not the homepage) with no prior visit are unlikely to be typed in. Trend that segment against AI referral trends.
2. **"How did you hear about us?"** Add "ChatGPT / AI assistant" as an option on sign-up and lead forms. This is often the largest single signal for B2B.
3. **Branded search lift.** People who see a brand in AI answers later search it. Track GSC branded impressions against AI visibility waves.
4. **Homepage referrals.** Since ChatGPT's May 2026 clickable-brand-name change, about 62–63% of ChatGPT referrals land on homepages [Similarweb 2026-07-29]. So do not dismiss homepage "direct" spikes.
5. **Log-to-session join.** Where a `ChatGPT-User` fetch of URL X is followed within seconds by a human session landing on X, attribute that session probabilistically.

### 6.4 Server-log analysis: retrieval fetches as a citation proxy

| UA token | Operator | Purpose | robots.txt | IP list |
|---|---|---|---|---|
| `OAI-SearchBot/1.4` | OpenAI | index for ChatGPT search | yes | openai.com/searchbot.json |
| `ChatGPT-User/1.0` | OpenAI | user-initiated fetch in ChatGPT and Custom GPTs | "may not apply" | openai.com/chatgpt-user.json |
| `GPTBot/1.4` | OpenAI | training | yes | openai.com/gptbot.json |
| `OAI-AdsBot/1.0` | OpenAI | ad landing-page safety | n/s | openai.com/adsbot.json |
| `PerplexityBot/1.0` | Perplexity | index | yes | perplexity.com/perplexitybot.json |
| `Perplexity-User/1.0` | Perplexity | user-triggered fetch | "generally ignores" | perplexity.com/perplexity-user.json |
| `ClaudeBot` / `Claude-SearchBot` / `Claude-User` | Anthropic | training / search index / user fetch | all honour robots.txt | see support article |

Sources: developers.openai.com/api/docs/bots (f. 2026-09-26); docs.perplexity.ai/guides/bots (f. 2026-09-26); support.claude.com/en/articles/8896518 and searchengineland.com/anthropic-claude-bots-470171 (via search, 2026).

- **Interpretation.** A `*-User` hit means a live answer is being composed with your page in context. It is the closest first-party signal to "cited in ChatGPT, Perplexity or Claude." It is **not** a citation: the page may be read and then dropped, and cached content produces no hit.
- **Index-bot hits** (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`) are an eligibility signal. They tell you the pages are crawlable and fresh.
- **Verify IPs** against the published JSON ranges, because spoofing is common. Profound's Agent Analytics also advertises "AI crawler verification." [tryprofound.com/features/agent-analytics, f. 2026-09-26]

Quick log query (combined log format):
```bash
grep -E 'ChatGPT-User|Perplexity-User|Claude-User' access.log \
 | awk '{print $4, $7, $NF}' | sed 's/\[//' \
 | awk '{split($1,d,":"); print d[1], $2}' | sort | uniq -c | sort -rn | head -50
# -> daily fetch counts per URL
```
Metric: **retrieval fetches per URL per week**. Track it pre and post change, using the same URLs as the GSC and Bing page-level views.

---

## 7. Impact data (what AI does to clicks and conversions)

### 7.1 CTR when AI Overviews appear

| Study | Sample / period | Finding |
|---|---|---|
| **Ahrefs** (2026-02-04) | 300k keywords (150k with AIO / 150k without), GSC-aggregated, Dec 2023 vs Dec 2025, desktop | **Position-1 CTR −58%**. Position 2 −50.8%, position 3 −46.4%, positions 4–10 −38.8% to −19.4%. Up from −34.5% in the Apr 2025 study. [ahrefs.com/blog/ai-overviews-reduce-clicks-update, 2026-02-04; ahrefs.com/blog/ai-overviews-reduce-clicks] |
| **Seer Interactive** (2026-04-24) | 53 brands, 5.47M queries, 2.43B organic and 296.9M paid impressions, Jan 2025–Feb 2026 | Organic CTR on AIO queries went 3.19% (Jan 2025) → **1.31% (Dec 2025)** → **2.36% (Feb 2026)**, a partial recovery. No-AIO CTR is 3.82%. Informational CTR: **cited in AIO 2.07%, not cited 0.94%, no AIO 3.35%**, so citation gives +120% clicks per impression. Paid CTR with AIO is stable at 13–17%. Seer caveat: "Cannot prove causation." [seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update, 2026-04-24] |
| **Seer** (Sep 2025) | 3,119 terms, 42 orgs | Organic CTR −61% (1.76%→0.61%) and paid −68% on AIO queries. Cited brands got +35% organic and +91% paid CTR. [via search summaries of Seer, 2025-09] |
| **Pew Research** (2025-07-22) | 900 US adults' browsing, Mar 2025 | Users clicked a traditional result on **8%** of visits with an AI summary against **15%** without. They clicked a source inside the summary on **1%** of visits, and more often ended the session. [pewresearch.org/short-reads/2025/07/22/…, 2025-07-22] |
| **Amsive** | — | **Unverified.** The search budget ran out before I could fetch it. Amsive reported larger CTR drops on non-branded than branded AIO keywords (from memory, 2025); do not cite without verifying. |
| **Google** (2025-08-06) | — | Organic click volume "relatively stable," with "higher quality" clicks. [blog.google, 2025-08-06] |

### 7.2 Zero-click and referral volume

- **SparkToro/Similarweb (2026-06-09):** US zero-click searches were **68.01%** in Jan–Apr 2026, against 60.45% in 2024 (Datos). Clicks to the open web fell to **276 per 1,000 searches** from 374. The methodologies differ between years (Similarweb panel vs Datos). [digitalapplied.com/blog/sparktoro-zero-click-study-2026-68-percent-seo-analysis, 2026-06-11; SparkToro primary not fetched]
- **Similarweb:** GenAI platforms referred **226.8M US visits in Jan 2026, 15% below Oct 2025**, while AI platform visits grew 28.6% YoY. Referrals are flat while usage grows. [search summary of Similarweb data, 2026] ChatGPT's share of AI-platform web traffic was ~53% (from 76%), Gemini ~27–28% and Claude ~9%, for Jun 2025–May 2026. Sources appear in ChatGPT answers about **6.8%** of the time, up from 1.6%, ranging from 23% in travel to under 4% in professional services. [aisearch.similarweb.com/blog/gen-ai-stats, 2026-07-29]
- **Implication for the skill:** multi-engine coverage matters. Gemini's share has grown sharply, and single-platform coverage "misses a meaningful share." [same]

### 7.3 Conversion rate of AI referrals vs organic

| Study | Finding | Caveat |
|---|---|---|
| **Ahrefs, own site** (2025-06-16) | AI search was 0.5% of visits and 12.1% of signups, a **23x** higher conversion rate | Single SaaS site, their own analytics. [ahrefs.com/blog/ai-search-traffic-conversions-ahrefs, 2025-06-16] |
| **Semrush** (2025-07-21) | The average LLM visitor is "worth **4.4x**" an organic visitor, based on conversion rate | Digital-marketing topics; methodology summary only. [semrush.com/blog/ai-search-seo-traffic-study, 2025-07-21] |
| **INFORMS *Marketing Science*** (Aug 2024–Jul 2025) | 973 ecommerce sites ($20B revenue). ChatGPT was ~0.2% of sessions and **converted 13% below organic** | Peer-reviewed, per the secondary source; the primary was not fetched. [relevantaudience.com summary, f. 2026-09-26] |
| **Visibility Labs** (FY2025) | 94 ecommerce brands: ChatGPT **1.81% vs 1.39%** non-branded organic (+31%). Referral sessions grew 1,079% Jan→Dec | Via secondary source. [relevantaudience.com summary] |
| **Similarweb** | ChatGPT referrals: 15 min on site vs 8 min for Google, 12 vs 9 pageviews, 7% vs 5% transactional conversion | Panel data. [search summary, 2026] |
| **Shopify** (May 2026) | AI-referred sessions convert "nearly 50% higher" on product pages | **Unverified** (secondary). |

**Takeaway for the skill:** the premium is real in B2B and SaaS, modest or even negative in ecommerce, and small in absolute volume. Measure it for the site in question using the non-branded organic comparator and at least 90 days of data. Never quote 4.4x or 23x as a forecast.

---

## 8. Experiment design: proving that GEO changes worked

### 8.1 Principles

1. **Baseline before touching anything.** Take at least 2 measurement waves (ideally 4 weekly waves) to estimate the natural week-to-week variance of each metric per engine.
2. **Use a page-level holdout.** Split comparable target pages into **treatment** and **control** groups, stratified by template, topic cluster, traffic and current citation rate. Only treatment pages get the changes (answer-first rewrite, schema, freshness, stats and quotes, and so on). SearchPilot's SEO testing uses exactly this model: "statistically-similar buckets of control and variant pages," a counterfactual forecast, and Bayesian credible intervals. It now also advertises GEO/LLM-traffic testing. [searchpilot.com/features/seo-a-b-testing, f. 2026-09-26]
3. **Map prompts to pages.** Each prompt should target one page cluster, so prompts inherit treatment or control status. The primary outcome is then **difference-in-differences** in URL citation rate:
   `DiD = (cite_T,post − cite_T,pre) − (cite_C,post − cite_C,pre)`,
   with SEs clustered by prompt. Control pages absorb engine-wide drift, such as model updates, index changes or new competitors.
4. **Keep the instrument fixed.** Use the same prompt IDs, locales, model IDs, tool versions and run counts. If a vendor or model changes mid-test, re-baseline or annotate the change.
5. **Separate outcomes by the lag they need:**
   - **Fast (days to weeks):** index-bot recrawl of changed URLs (logs), `*-User` retrieval fetches, Bing citations (IndexNow helps), Perplexity citations (live retrieval).
   - **Medium (2–8 weeks):** Google AIO and AI Mode citations and GSC AI impressions, which follow crawling and indexing; ChatGPT search citations, which depend on the OAI-SearchBot and Bing-derived index.
   - **Slow (months or model generations):** unaided mentions in non-search model answers (parametric memory). These only change with retraining, so don't expect them in a quarter.
   - These lags are **working estimates, unverified.** No platform publishes a lag SLA. Measure your own by logging the first recrawl date for each changed URL.
6. **Pre-register** the hypothesis, primary metric, minimum detectable effect, sample size (§3.2) and stopping date. Do not peek-and-stop.
7. **Guard metrics.** Classic organic clicks, rankings and conversions on treatment pages must not fall. GEO changes must not cost SEO.

### 8.2 When a holdout is impossible (small site)

- **Interrupted time series.** Use ≥8 pre-waves and ≥8 post-waves, and fit level and slope changes.
- **Synthetic control.** Use competitors' visibility, or the unchanged sections of your own site, as the comparison series.
- **Report ranges and CIs, not point claims.** If the CI crosses zero, say "no detectable change at this sample size" and state the MDE.

### 8.3 Attribution ladder for business impact

1. **Visibility:** mention, citation and SoV (prompt harness) plus GSC AI impressions and Bing citations.
2. **Retrieval:** `*-User` fetches.
3. **Traffic:** GA4 AI channel sessions (native + custom) plus landing-page mix.
4. **Outcomes:** conversions and revenue from AI sessions, plus the "heard about us via AI" survey share.
5. **Halo:** branded-search impressions in GSC and direct-to-deep-page sessions.

Report each rung separately. Only rungs 3–4 are money, and they are a floor.

---

## 9. Ready-to-use measurement plan template

```markdown
# AI Search Measurement Plan — <site> — v<N> (<date>)

## 1. Scope
- Brand + aliases: …   Competitors (5–15) + aliases: …
- Markets/locales: GB-en, US-en …   Engines: ChatGPT(API+UI sample), Claude, Gemini, Perplexity, Google AIO (SERP API), Google AI Mode (SERP API), Copilot (BWT)
- Pages in scope: <list/cluster>, treatment vs control assignment file: pages_assignment.csv

## 2. Prompt set (frozen: prompts_v<N>.csv)
- 100 core prompts; strata: discovery 30 / best-for 30 / comparison 15 / branded-fact 15 / local-transactional 10
- Sources: GSC question queries, BWT grounding queries, sales/support FAQs, PAA
- Runs: API engines R=5 per wave; SERP engines R=1; UI calibration sample 25 prompts/quarter
- Cadence: weekly, <weekday>, 06:00–10:00 UTC; model IDs pinned & logged

## 3. Metrics (primary ★)
- ★ Citation rate of target URLs (treatment vs control) per engine
- ★ Mention rate / SoV vs competitors per engine
- Recommendation rate, prominence (0–3), sentiment, factual accuracy
- GSC Gen-AI impressions (page×country×device), GSC Web clicks/impressions (guard)
- BWT citations & cited pages; grounding-query themes
- Log: *-User fetches/URL/week; index-bot recrawl latency
- GA4: AI Assistant (native) + AI (custom) sessions, key events, revenue; conversion rate vs non-brand organic
- Survey: % "AI assistant" in how-did-you-hear

## 4. Baseline
- 4 weekly waves before any change; compute mean, SD, 95% CI per metric×engine
- MDE given n: <calc>; required n for target MDE: <calc>

## 5. Intervention log
| date | URL(s) | change type | deployed | recrawled (log) | indexed (GSC) |

## 6. Analysis
- DiD on citation rate, prompt-clustered SE; ITS if no holdout
- Annotate model/vendor changes, Google core updates, AIO UI changes
- Decision rule: ship-to-all if lower 95% bound of DiD > 0 and guard metrics not significantly negative

## 7. Reporting
- Monthly one-pager: visibility ladder (§8.3), top cited URLs, top lost prompts, competitor SoV, factual errors to fix
```

---

## 10. Scoring rubric (0–100 AI Search Visibility Score)

A composite for dashboards. Report the components too, never just the score.

| Component | Weight | Scoring (per engine, then demand- or engine-share-weighted) |
|---|---|---|
| Mention rate (unbranded prompts) | 25 | 0% → 0; ≥60% → 25 (linear) |
| Citation rate (any own URL, all prompts) | 20 | 0% → 0; ≥40% → 20 |
| Share of voice vs tracked competitors | 15 | SoV ÷ (1 / #brands), capped at 2× the fair share → 15 |
| Recommendation rate (best-for / comparison prompts) | 10 | 0% → 0; ≥50% → 10 |
| Prominence (mean 0–3 when mentioned) | 5 | mean ÷ 3 × 5 |
| Sentiment (net positive % when mentioned) | 5 | (pos − neg) ÷ mentions, mapped −1..1 → 0..5 |
| Factual accuracy (branded prompts) | 10 | (1 − error rate) × 10; any critical error (price, legal, safety) caps this at 3 |
| Google AI surfaces (GSC Gen-AI impressions trend + AIO/AI Mode citation rate via SERP API) | 5 | Rising QoQ with citation rate ≥20% → 5; flat → 2.5; falling → 0 |
| Traffic & outcome (AI sessions share of organic + AI conv. rate ≥ non-brand organic) | 5 | Both true → 5; one → 2.5 |

Engine weights: default to each engine's share of your AI referrals in GA4. If there are no referrals, use market share: ChatGPT 0.5, Gemini/AIO/AI Mode 0.3, Claude 0.1, Perplexity plus Copilot 0.1, adapted from Similarweb's Jun 2025–May 2026 traffic shares [aisearch.similarweb.com/blog/gen-ai-stats, 2026-07-29].

**Bands:**
- **0–20 Invisible:** fix crawl access, entity facts and citations first.
- **21–40 Emerging.**
- **41–60 Competitive.**
- **61–80 Leader.**
- **81–100 Dominant:** verify you are not overfitting to the prompt set; refresh 20% of prompts each quarter as new IDs.

**Reporting rule:** show every score with its 95% CI (bootstrap over prompts). A change of less than the CI width is "no change."

---

## 11. Traps checklist for the agent

- ❌ Reporting per-prompt "rank." ✅ Report visibility % with a CI. [SparkToro 2026-01-28]
- ❌ Treating Search Console Web clicks as "SEO only." AIO and AI Mode are inside them. [developers.google.com/…/ai-features, 2025-12-10]
- ❌ Expecting the GA4 AI Assistant channel to include Perplexity, Claude or Google AI Overviews. [GA4 help, f. 2026-09-26]
- ❌ Building on Perplexity Sonar `/chat/completions`, which is supported only until 2026-09-27.
- ❌ Using Gemini's `groundingChunks.web.uri` as the cited URL. It is a redirect.
- ❌ Counting a `web_search_tool_result_error` (returned with HTTP 200) as "not cited."
- ❌ Summing GSC page-level AI impressions to get the property total.
- ❌ Changing prompts, models or locales mid-test without re-baselining.
- ❌ Quoting 4.4x or 23x conversion as expected. Measure site-specific rates against non-brand organic.
- ❌ Dismissing homepage "Direct" traffic. ChatGPT's brand-name links now send about 62% of its referrals to homepages. [Similarweb 2026-07-29]

---

## 12. Source list (URL, date)

1. sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/ (2026-01-28)
2. mediapost.com/publications/article/412364 (2026-01-28), secondary
3. developers.google.com/search/blog/2026/06/gen-ai-performance-reports (2026-06)
4. support.google.com/webmasters/answer/16984139 (f. 2026-09-26)
5. searchenginejournal.com/google-search-console-ai-reports-rolled-out-worldwide/587836/ (2026-09)
6. searchenginejournal.com/google-reports-ai-search-impressions-how-to-read-them/582824/ (2026-06)
7. developers.google.com/search/docs/appearance/ai-features (updated 2025-12-10)
8. blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview (2026-02-10)
9. otterly.ai/blog/bing-webmaster-tools-ai-performance-report/ (2026)
10. developers.openai.com/api/docs/guides/tools-web-search (f. 2026-09-26)
11. developers.openai.com/api/docs/pricing (f. 2026-09-26)
12. platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool (f. 2026-09-26)
13. ai.google.dev/gemini-api/docs/google-search (f. 2026-09-26)
14. ai.google.dev/gemini-api/docs/generate-content/google-search (legacy, f. 2026-09-26)
15. ai.google.dev/gemini-api/docs/pricing (f. 2026-09-26)
16. github.com/googleapis/python-genai/issues/1512 (redirect URIs)
17. docs.perplexity.ai/api-reference/chat-completions-post (f. 2026-09-26; Sonar ends 2026-09-27)
18. docs.perplexity.ai/getting-started/quickstart (f. 2026-09-26)
19. docs.perplexity.ai/docs/agent-api/tools/web-search (f. 2026-09-26)
20. docs.perplexity.ai/guides/bots (f. 2026-09-26)
21. developers.openai.com/api/docs/bots (f. 2026-09-26)
22. support.claude.com/en/articles/8896518 (via search, 2026)
23. learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement (2025-05-15)
24. api-dashboard.search.brave.com/app/documentation/web-search/get-started (f. 2026-09-26)
25. serpapi.com/google-ai-mode-api (f. 2026-09-26)
26. serpapi.com/google-ai-overview-api (f. 2026-09-26)
27. docs.dataforseo.com/v3/serp-google-ai_mode-overview/ (f. 2026-09-26)
28. dataforseo.com/solutions/geo (f. 2026-09-26)
29. geotoolbox.ai/blog/best-ai-visibility-tools (2026-07-16, updated 2026-09-10)
30. get-ryze.ai/blog/ai-visibility-tools-pricing-compared-2026 (2026-08-29)
31. semrush.com/blog/how-to-measure-ai-share-of-voice/ (2026-07-17)
32. ahrefs.com/blog/ai-citations-vs-impressions-study (2025-11-26)
33. tryprofound.com/features/agent-analytics (f. 2026-09-26); tryprofound.com/blog/introducing-agent-analytics
34. conductor.com/platform/features/ai-search-performance/; brightedge.com/blog/introducing-brightedge-ai-catalyst… (f. 2026-09-26)
35. aisearch.similarweb.com/blog/gen-ai-stats/ (2026-07-29); aisearch.similarweb.com/ai-brand-visibility/
36. support.google.com/analytics/answer/9756891 (f. 2026-09-26)
37. searchenginejournal.com/google-analytics-adds-ai-assistant-as-default-channel-group/574974/ (2026-05-14)
38. terminusapp.com/blog/ai-traffic-channel-in-ga4/ (2026-07-09)
39. seerinteractive.com/insights/are-ai-sites-like-chatgpt-sending-your-website-traffic (updated 2026-06-22)
40. ahrefs.com/blog/ai-overviews-reduce-clicks-update (2026-02-04); ahrefs.com/blog/ai-overviews-reduce-clicks/ (2025-04)
41. seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update (2026-04-24)
42. pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/ (2025-07-22)
43. blog.google/products/search/ai-search-driving-more-queries-higher-quality-clicks/ (2025-08-06)
44. digitalapplied.com/blog/sparktoro-zero-click-study-2026-68-percent-seo-analysis (2026-06-11)
45. semrush.com/blog/ai-search-seo-traffic-study/ (2025-07-21)
46. ahrefs.com/blog/ai-search-traffic-conversions-ahrefs/ (2025-06-16)
47. relevantaudience.com/seo/why-chatgpt-traffic-converts-worse-than-google-search/ (f. 2026-09-26), secondary for INFORMS and Visibility Labs
48. searchpilot.com/features/seo-a-b-testing (f. 2026-09-26)

**Research gaps (marked unverified above):**
- Amsive's CTR study.
- A controlled API-vs-UI divergence study.
- Official per-platform lag times.
- Goodie AI specifics.
- The exact Perplexity Agent API filter field names.
- DataForSEO AIO reference field names.
- Primary INFORMS paper and Shopify data.

The web-search budget ran out mid-session, so these could not be closed.
