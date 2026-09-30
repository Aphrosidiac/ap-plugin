# AI Search Measurement Plan — <site> — v<N> (<date>)

## 1. Scope
- Brand + aliases: …   Competitors (5–15) + aliases + domains: …
- Markets/locales: MY-en, MY-ms …   Engines: ChatGPT (API + UI sample), Claude, Gemini, Perplexity, Google AIO (SERP API), Google AI Mode (SERP API), Copilot (Bing Webmaster Tools)
- Pages in scope + treatment/control assignment: docs/geo/pages_assignment.csv

## 2. Prompt set (frozen: docs/geo/prompts_v<N>.csv — never edit a prompt mid-experiment; add new IDs)
- Core size: 50–100 prompts. Strata: discovery 30% / best-for 30% / comparison 15% / branded-fact 15% / local-transactional 10%
- Sources: GSC question queries (≥5 words), BWT grounding queries, sales/support questions, PAA, Reddit/Facebook-group phrasing, engine fan-out queries from the last wave
- Runs: API engines R=3–5 per wave; SERP engines R=1; manual UI calibration 20–30 prompts/quarter (logged-out)
- Cadence: every 2–4 weeks, same weekday and time window; model IDs pinned and logged (a model change = instrument change)

## 3. Metrics (primary ★)
- ★ Citation rate of target URLs (treatment vs control), per engine
- ★ Mention rate and share of voice vs competitors, per engine (mentions and citations are different games — track both)
- Recommendation rate, prominence (0–3), sentiment, factual accuracy against docs/geo/facts.md
- GSC Generative AI report impressions (page × country × device) + GSC Web clicks/impressions (guard metric)
- BWT AI Performance: citations, cited pages, grounding-query themes, citation share
- Logs: *-User fetches per URL per week; index-bot recrawl latency after each change
- GA4: AI Assistant (native) + AI (custom channel) sessions, key events, revenue; conversion vs NON-BRAND organic
- Lead forms: "How did you hear about us?" includes "ChatGPT / AI assistant"

## 4. Baseline
- ≥2 (ideally 4) waves before any change; mean, SD, 95% CI per metric × engine
- MDE at current n: … ; n needed for the target MDE: n ≈ 7.84·[p1(1−p1)+p2(1−p2)]/(p2−p1)²

## 5. Intervention log
| date | URL(s) | change type | deployed | recrawled (log) | indexed (GSC) |
|---|---|---|---|---|---|

## 6. Analysis
- Difference-in-differences on citation rate with prompt-clustered SE; interrupted time series if no holdout
- Annotate model/vendor changes, Google core/spam updates, AI surface UI changes
- Ship-to-all rule: lower 95% bound of DiD > 0 AND guard metrics not significantly worse

## 7. Reporting
- One page per wave: visibility ladder (visibility → retrieval → traffic → outcomes → halo), top cited URLs,
  prompts lost to competitors, domains the engines trust for this category, factual errors to fix
