# Measurement — baseline first, prove it after

Full metric dictionary, API shapes, GA4 regex, tool landscape and experiment design:
`research/07-measurement.md`. Instrument: `scripts/ai_visibility.py`. Templates:
`assets/measurement-plan.md`, `assets/prompts-template.csv`.

**Never report a "rank in ChatGPT".** SparkToro (2,961 runs): <1% chance of the same brand
list twice, ~1 in 1,000 of the same order. Report **rates with confidence intervals** over
many prompts and runs.

---

## 1. Metrics

| Metric | Definition |
|---|---|
| Mention rate | answers naming the brand ÷ answers |
| Citation rate | answers citing ≥1 URL on the domain ÷ answers (cited = shown; *sourced* = retrieved — record both) |
| Citation share | your citations ÷ all citations in the answer set |
| Share of voice | your mentions ÷ mentions of all tracked brands |
| Recommendation rate | explicitly recommended/"best" ÷ recommendation-intent answers |
| Prominence (0–3) | 3 first/explicitly recommended · 2 described in body · 1 listed/source only · 0 absent (LLM-judge, hand spot-checked) |
| Sentiment | pos/neutral/neg share of mentions |
| Accuracy | answers with a factual error about the brand ÷ answers mentioning it (against `docs/geo/facts.md`) |
| GSC AI impressions | Generative AI report (impressions only; page-level doesn't sum to property) |
| Bing citations | BWT AI Performance (sampled; citations, cited pages, grounding queries, citation share) |
| Retrieval fetches | `*-User` log hits per URL per week (log_bots.py) — proxy, not proof |
| AI referral sessions | GA4 native AI Assistant + custom AI channel — a **floor** |
| AI conversions | key events/revenue from AI sessions vs **non-brand** organic |

## 2. First-party sources (use before any paid tool)

- **Google Search Console → Generative AI performance report** (worldwide since 2026-08-31):
  impressions for AI Overviews + AI Mode by page, country, device, date; separate Discover
  report; no clicks, queries, position or API. AI clicks are blended into "Web" in the main
  report. Use it as a diagnostic: rising AI impressions + falling Web clicks = "cited but not
  clicked".
- **Bing Webmaster Tools → AI Performance** (public preview since 2026-02-10; intents, topics,
  citation share, compare since June 2026): the only first-party citation report. Export
  grounding queries → classify → feed into the prompt set and the content plan.
- **GA4 native "AI Assistant" channel** (since 2026-05-13, not retroactive): ChatGPT, Gemini,
  DeepSeek, Copilot, Grok. **Excludes Perplexity, Google AIO/AI Mode; Claude uncertain.** Add a
  custom channel group (applies to history), placed **above Referral**:
  - Session source matches regex:
    `^(chatgpt\.com|chat\.openai\.com|perplexity(\.ai)?|www\.perplexity\.ai|claude\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|copilot\.cloud\.microsoft|edgeservices\.bing\.com|chat\.deepseek\.com|deepseek\.com|grok\.com|meta\.ai|you\.com|poe\.com|phind\.com|kagi\.com|chat\.mistral\.ai|duck\.ai)$`
  - OR session manual source matches `^(chatgpt\.com|perplexity|claude|gemini|copilot)`
    (catches `utm_source=chatgpt.com` when the referrer is stripped).
  - Test in DebugView before trusting it. BigQuery version in research/07-measurement.md §6.2.
- **Server logs** (log_bots.py): user-triggered fetches per URL; index-bot recrawl latency.
- **Dark AI traffic**: apps often send no referrer. Proxies: direct sessions landing on deep
  article URLs; "How did you hear about us?" with an AI option (often the biggest B2B signal);
  branded-search lift in GSC; homepage "direct" spikes (≈62% of ChatGPT referrals now land on
  homepages).

## 3. The prompt set

1. Seed from real demand: GSC question queries (≥5 words) and comparisons, BWT grounding
   queries, site search, sales/support transcripts, PAA.
2. Rewrite keywords as conversational prompts: `[persona context] + [task] + [constraints]`.
3. Stratify (100-prompt core): discovery 30% · best-for 30% · comparison 15% · branded-fact 15%
   · local/transactional 10%. Add BM variants for Malaysian brands.
4. 3–5 personas; phrase each core intent 2–3 ways.
5. 5–15 competitors with aliases/misspellings and domains.
6. **Freeze and version** `prompts_vN.csv`; never edit a prompt mid-experiment — add new IDs.
   Refresh ~20% per quarter as new IDs.

Sample size: at p≈0.5, ±31 pp at n=10, ±18 at 30, ±10 at 100, ±4.4 at 500. To detect 30%→40%
at 80% power ≈ 350 answers per period per engine; 30%→35% ≈ 1,400. Prefer many prompts × few
runs (e.g. 100 × 3–5 per API engine; SERP engines 1 run). Cluster SEs by prompt.

## 4. Running ai_visibility.py

```bash
export OPENAI_API_KEY=… ANTHROPIC_API_KEY=… GEMINI_API_KEY=… SERPAPI_API_KEY=…   # any subset
python3 scripts/ai_visibility.py --prompts docs/geo/prompts_v1.csv --brand "Acme" \
  --aliases "Acme Co,acme.my" --domain acme.my --competitors "Globex:globex.com,Initech:initech.my" \
  --engines openai,anthropic,gemini,serp_aio,serp_aimode --runs 3 --out docs/geo/visibility/<date>
python3 scripts/ai_visibility.py --summarize docs/geo/visibility/<new> --compare docs/geo/visibility/<old>
```

- Resumable (raw JSON per call is kept; re-running skips finished calls). Raw responses are
  immutable so a better parser can re-score history.
- Engines: OpenAI Responses + `web_search` (inline `url_citation` + full `sources`); Anthropic
  Messages + `web_search_20250305` (errors arrive **inside HTTP 200** — counted as errors, not
  "not cited"); Gemini grounding (`groundingChunks.web.uri` are **redirects** — resolved once);
  Perplexity **Agent API** (Sonar chat-completions retired 2026-09-27; needs
  `--perplexity-model`); SerpApi `google_ai_overview` / `google_ai_mode` — the only way to see
  Google's real AI surfaces (AIO needs a second call within ~1 minute via `page_token`).
- Costs (Sep 2026): ~$10/1k searches Anthropic; $10–25/1k OpenAI; $14/1k Gemini 3.x after 5k
  free/month; $2.50/1k Perplexity web_search; + tokens. A 100 × 3 × 4 wave ≈ 1,200 calls.
- Model IDs in the script were current on 2026-09-26; pass `--openai-model` etc. and log them.
  A model change is an instrument change — annotate it.
- **APIs are a trend instrument, not what consumers see** (memory, routing, ads). Calibrate
  quarterly by running 20–30 prompts by hand in logged-out apps.
- If no keys: run a manual sample (20–30 prompts × 3 engines, logged-out, fixed locale), record
  in the same CSV columns, and say so in the report.

The summary's two most useful sections: **domains the engines cite for the category** (the
off-site target list) and **fan-out queries the engines ran** (content gaps).

## 5. Proving a change worked

1. **Baseline** ≥2 waves (ideally 4) before touching anything.
2. **Holdout**: split comparable pages into treatment/control (stratified by template, topic,
   traffic, current citation). Map prompts to pages so prompts inherit the assignment.
3. **Difference-in-differences** on URL citation rate, SEs clustered by prompt:
   `DiD = (T_post − T_pre) − (C_post − C_pre)`. Control pages absorb engine-wide drift.
4. Keep the instrument fixed (prompt IDs, locales, models, run counts).
5. Expected lags (working estimates, not SLAs): **days–weeks** — recrawl in logs, `*-User`
   fetches, Bing citations (IndexNow), Perplexity; **2–8 weeks** — Google AIO/AI Mode citations,
   GSC AI impressions, ChatGPT search; **months / model generations** — unaided mentions from
   built-in knowledge.
6. Pre-register hypothesis, primary metric, MDE, sample size, stop date. No peek-and-stop.
7. **Guard metrics**: organic clicks, rankings and conversions on treatment pages must not
   fall — GEO changes must not cost SEO.
8. Small site, no holdout: interrupted time series (≥8 pre and post waves) or synthetic
   control (competitors / untouched sections). If the CI crosses zero: "no detectable change
   at this sample size", with the MDE.

Attribution ladder, reported rung by rung: visibility → retrieval → traffic → outcomes →
halo (branded search, direct-to-deep-page). Only traffic and outcomes are money, and they are
a floor.

## 6. Impact context (for setting expectations, not forecasts)

Position-1 CTR −58% when an AIO shows (Ahrefs, Dec 2025 vs 2023); cited brands ~2.07% vs 0.94%
uncited (Seer); US zero-click 68% (2026); AI referrals flat while usage grows. AI-referral
conversion ranges from −13% vs organic (973 e-com sites, peer-reviewed) to 23× (one SaaS) —
measure the site's own, against non-brand organic, over ≥90 days.

## 7. Composite score (dashboards only — always show the parts)

Mention rate on unbranded prompts 25 · citation rate 20 · SoV vs fair share 15 ·
recommendation rate 10 · prominence 5 · sentiment 5 · factual accuracy 10 (any critical error
caps it at 3) · Google AI surfaces trend 5 · traffic & outcome 5. Engine weights = the site's
own GA4 AI referral mix, else ChatGPT .5 / Google .3 / Claude .1 / Perplexity+Copilot .1.
Bands: 0–20 invisible (fix access, entity facts, citations first) · 21–40 emerging ·
41–60 competitive · 61–80 leader · 81–100 dominant (check you aren't overfitting the prompt set).
Show a bootstrap CI; a move smaller than the CI is "no change".

## 8. Traps

Per-prompt ranks · treating GSC Web clicks as "SEO only" · expecting the GA4 AI channel to
include Perplexity/Claude/AIO · building on Perplexity Sonar · using Gemini redirect URIs as
the cited URL · counting Anthropic's in-200 search errors as "not cited" · summing page-level
GSC AI impressions · changing prompts/models mid-test · quoting 4.4× or 23× conversion ·
dismissing homepage "direct" traffic.
