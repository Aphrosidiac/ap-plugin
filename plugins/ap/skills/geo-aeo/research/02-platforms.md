# 02 — How each answer engine retrieves, selects and cites sources (as of 2026-09-26)

Researcher dossier for the GEO + AEO skill. Every claim carries a URL and a source date (the date the source was published or last updated; "n.d." = no date on the page, accessed 2026-09-26). Anything I could not verify from a primary or reputable secondary source is marked **unverified**. Vendor and agency studies are labelled as such; treat their numbers as directional.

**The main finding:** in late 2026 there are really **five retrieval backbones** behind the answer engines: (1) the **Google index** (AI Overviews, AI Mode, Gemini app, Gemini API grounding), (2) the **Bing index**, now exposed as passage-level "Web IQ" (Copilot, Bing AI answers, and one of ChatGPT's providers), (3) **OpenAI's own index family** plus third-party providers (ChatGPT search), (4) **Perplexity's own index** (Perplexity, Comet, Sonar/Search API customers), and (5) **Brave's independent index** (Claude, plus many API-grounded LLM apps). Meta and Apple are building their own. A site that is crawlable, server-rendered and indexed in **Google + Bing + Brave**, and does not block the search-purpose AI bots, covers almost all of the market.

---

## 0. Market context: where AI traffic comes from

Two different metrics get confused all the time:

| Metric | Latest figure | Source (date) |
|---|---|---|
| **Visits *to* gen-AI chatbot sites** (Similarweb, worldwide) | June 2026 dataset: ChatGPT 52.7% (from 76.4% a year earlier), Gemini 27.3%, Claude 8.9%, DeepSeek 4.0%, Grok 2.8%, Copilot 2.0%, Perplexity 1.3% | https://ppc.land/chatgpt-drops-to-52-7-as-claude-triples-its-ai-traffic-share/ (2026-06-11). Explicitly *not* referral traffic |
| Same, August 2026 update | ChatGPT 55.5%, Gemini 25.6%, Claude 9.3%, DeepSeek 3.4%, Grok 2.4%, Copilot 1.6%, Perplexity 0.9% | Similarweb X post, https://x.com/Similarweb/status/2096878021378466096 (Sept 2026). Figures taken from a search-result snippet; **unverified** against the post itself |
| **Referrals *from* AI platforms to websites** (SE Ranking panel) | ChatGPT 74.78%, Gemini 11.56% (+231% YoY), Perplexity 7.23% (flat), Copilot 3.51%, Claude 2.62% (+320% YoY). AI referrals ≈ 0.32% of all site visits (1 in 312), 16× since 2024. AI visitors spend ~68% more time on site | https://seranking.com/blog/ai-traffic-research-study/ (2026; exact date **unverified**) |
| ChatGPT link behaviour change | After a May 2026 ChatGPT UI update, 62–63% of ChatGPT referral traffic lands on **homepages** (up from 26–29%) | https://aisearch.similarweb.com/blog/gen-ai-stats/ (2026-07-29) |
| Google AI surfaces scale | AI Overviews >2.5B monthly users; AI Mode >1B monthly users | https://blog.google/products-and-platforms/products/search/new-controls-website-owners/ (2026-06-03, upd. 2026-08-31) |

**What this means for the skill:** ChatGPT still sends most AI referral clicks. Gemini and Claude are the fastest-growing. Perplexity sends fewer clicks than its brand profile suggests. Google's AI surfaces reach far more users than any chatbot, but they report impressions, not clicks (see §1). And since ChatGPT now links homepages much more often, the homepage has to state clearly what the entity is and what it offers.

---

## 1. Google AI Overviews and AI Mode (plus Discover gen-AI)

### Fact table

| Item | Detail | Source (date) |
|---|---|---|
| Index | Google Search index. "Rooted in our core Search ranking and quality systems." No separate AI index | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide (upd. 2026-07-10) |
| Retrieval technique | **Query fan-out**: "issuing a multitude of queries simultaneously" across subtopics. Deep Search "can issue hundreds of searches" | https://blog.google/products/search/google-search-ai-mode-update/ (2025-05-20); https://developers.google.com/search/docs/appearance/ai-features (upd. 2025-12-10) |
| Model | AI Mode default = **Gemini 3.5 Flash** globally (I/O, May 2026). AI Overviews upgraded to Gemini 3 in Jan 2026 | https://blog.google/products-and-platforms/products/search/search-io-2026/ (2026-05-19); https://www.searchenginejournal.com/google-ai-overview-citations-from-top-ranking-pages-drop-sharply/568637/ (2026-03-02) |
| Eligibility | Indexed + eligible to show a snippet. "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary" | ai-features doc (2025-12-10) |
| Crawler | Googlebot (full JS rendering via WRS). Gemini inherits Googlebot's rendering | https://vercel.com/blog/the-rise-of-the-ai-crawler (2024-12) |
| Agent UA | `Google-Agent`: "web navigation for agents on Google infrastructure". It is a user-triggered fetcher and **ignores robots.txt** | https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers (upd. 2026-08-19) |
| Controls | `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`; **new Search Console "Search generative AI" toggle** (property-level opt-out of AIO, AI Mode and Discover gen-AI features; not a ranking signal for classic results; takes 1–2 days) | new-controls post (2026-06-03/08-31); https://www.searchenginejournal.com/what-opting-out-of-googles-ai-search-features-means-now/584321/ (2026-08-01) |
| Google-Extended | Controls **training** of future Gemini models *and* **grounding in Gemini Apps / Vertex AI "Grounding with Google Search"**. Does NOT control AI Overviews or AI Mode, and "does not impact a site's inclusion in Google Search nor is it used as a ranking signal" | https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers (upd. 2026-07-14) |
| Reporting | **Search Console → Generative AI performance report**: impressions only (no clicks or CTR); dimensions: pages, countries, devices, dates; filter web vs multimodal; excludes Search Labs; site must have enough impressions and not be opted out. Rolled out globally by 2026-08-31. The UK CMA requires Google to add click data by Dec 2026 and page-level controls by Mar 2027 | https://support.google.com/webmasters/answer/16984139 (n.d., accessed 2026-09-26); SEJ 2026-08-01; https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports (2026-06) |
| Regulatory driver | UK CMA conduct requirement (2026-06-03) ordering genuine publisher opt-out controls | SEJ 2026-08-01; https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/ (2026-05-15) |
| UX features | More inline links; **Preferred Sources** now applies inside AIO/AI Mode; subscription labels; follow-ups from AIO continue into AI Mode | new-controls post (2026-06-03); I/O post (2026-05-19) |
| Commerce | **Universal Commerce Protocol (UCP)** (Jan 2026, co-developed with Shopify, Etsy, Wayfair, Target, Walmart). "Buy" button in AI Mode and Gemini only for listings with Merchant Center attribute `native_commerce(checkout_eligibility)`; live in US/CA/AU, UK next. Business Agent (brand chat on Search), "dozens of new" conversational Merchant Center attributes (product FAQs, compatible accessories, substitutes), **Direct Offers** ad pilot in AI Mode; Merchant Center "AI performance insights" | https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/ (2026-01-11); https://support.google.com/merchants/answer/16837055 (n.d.); https://blog.google/products-and-platforms/products/shopping/shopping-updates-google-marketing-live/ (2026-05-20) |

### Google's official position (July 2026 guide)
The "Optimizing your website for generative AI features on Google Search" guide (published 2026-05-15, updated 2026-07-10) is the most important primary document in this whole topic:
- AEO/GEO "are still SEO". The fundamentals are relevance, quality, usefulness and trust ([SEJ, 2026-05-15](https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/)).
- **Explicit myth-busting.** Google Search does not use `llms.txt` or special AI markup, and they "neither harm nor help". There is "no requirement to break your content into tiny pieces". AI-specific rewrites are not needed. Manufacturing inauthentic mentions doesn't work. "Structured data isn't required for generative AI search", although it still matters for rich results.
- **Do this instead:** "non-commodity", "unique expert or experienced takes that go beyond common knowledge", good images and video, technical indexability, JavaScript SEO, page experience, less duplication, Merchant Center feeds and Business Profile for commerce and local. Mass-producing content variants to game AI is **scaled content abuse**.
- **Agentic:** browser agents read both the visual rendering and the DOM. Google points to agent-friendly best practices and UCP.
- Measure with the Search Console gen-AI report. Distrust third-party tools that claim "internal" Google metrics.

### How sources get chosen: empirical evidence
- Fan-out decouples citations from ranking for the head query. Ahrefs (863k keywords, 4M AIO URLs) found **only 38%** of AIO-cited pages rank in the top 10 for that query (76% in July 2025); 31.2% rank 11–100 and 31.0% rank beyond 100. YouTube is 5.6% of all AIO citations and 18.2% of the citations that don't rank ([SEJ, 2026-03-02](https://www.searchenginejournal.com/google-ai-overview-citations-from-top-ranking-pages-drop-sharply/568637/)). BrightEdge measured ~17% top-10 overlap (Feb 2026, per [ALM Corp summary](https://almcorp.com/blog/google-ai-overview-citations-drop-top-ranking-pages-2026/), date **unverified**).
- Academic audit, 55,393 trending queries, Mar–Apr 2026: AIO triggers on 13.7% of queries overall but **64.7% of question-form queries**. AIOs cite more credible domains than the co-displayed organic results, yet ~30% of cited pages are not on page one at all. 11.0% of atomic claims are unsupported by the cited page, mostly through omission ([Xu, Iqbal, Montgomery, arXiv 2605.14021, 2026-05-13](https://arxiv.org/abs/2605.14021)).
- NewzDash: ~1 in 6 US trending-news queries now show **Top Stories inside AIO**, so opting out may also remove news carousel exposure (via SEJ 2026-08-01).

### What to do for Google AIO / AI Mode
1. Keep **classic technical SEO** clean: indexable, canonicalised, rendered HTML with the main content, fast. It is the only door in.
2. **Cover the fan-out, not just the keyword.** Build topic clusters that answer the sub-questions a fan-out would generate (comparisons, "for X use case", costs, alternatives, how-to steps). Question-form queries trigger AIO about 65% of the time.
3. Publish **non-commodity** material: first-party data, original photos and video (a YouTube presence helps, since YouTube is a large and rising AIO citation source), expert bylines, experience.
4. Do **not** spend effort on llms.txt, chunk-rewriting or "AI schema" *for Google*. Keep structured data accurate for rich results and Merchant/local.
5. Commerce: complete Merchant Center feeds including the new conversational attributes. Evaluate UCP (`native_commerce` attribute) and Business Agent. Local: complete Google Business Profile.
6. Use `data-nosnippet` surgically for text you don't want quoted. Use the Search Console gen-AI toggle only as a deliberate business decision: you lose AIO, AI Mode and Discover gen-AI exposure, and possibly Top Stories inside AIO.
7. Leave `Google-Extended` allowed if you want **Gemini app / Vertex grounding** citations. Blocking it doesn't affect AIO/AI Mode.
8. Monitor weekly in the **Search Console Generative AI performance report**. Track which pages gain AI impressions and pair that with GA4 landing-page data, since the report has no clicks yet.

---

## 2. Gemini app and Gemini API grounding

| Item | Detail | Source (date) |
|---|---|---|
| Index | Google Search via "Grounding with Google Search". The model decides whether to search, generates one or more queries and returns `groundingMetadata` (queries, web results, citations) | https://ai.google.dev/gemini-api/docs/google-search (n.d., accessed 2026-09-26) |
| Opt-out | Pages that disallow **Google-Extended** are not used for grounding (Vertex/Agent Platform and Gemini Apps) | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-google-search (n.d.); common-crawlers doc (2026-07-14) |
| Crawler / JS | Googlebot (renders JS). User-supplied URLs in Gemini notebooks are fetched by `Google-GeminiNotebook`, which ignores robots.txt | user-triggered fetchers doc (2026-08-19) |
| Alt grounding | Google Cloud added "Grounding with Parallel Web Search" as a non-Google option for enterprise agents | https://developers.googleblog.com/expanding-choice-in-gemini-enterprise-agent-platform-introducing-grounding-with-parallel-web-search/ (date **unverified**) |
| Reporting | No publisher-facing Gemini-app report. The Search Console gen-AI report covers Search AIO/AI Mode only. Referrals show as `gemini.google.com` in analytics | support.google.com/webmasters/answer/16984139 |

**Actions:** allow `Google-Extended` if Gemini citations matter; the only cost is training use. Everything in §1 applies. Gemini is #2 by chatbot traffic (25–27%) and the fastest-growing referrer after Claude, so it's worth a dedicated referral segment in analytics.

---

## 3. ChatGPT search (OpenAI)

### Fact table

| Item | Detail | Source (date) |
|---|---|---|
| Index | **Mixed, trending toward its own index.** OpenAI runs "Labrador", a family of indexes (general web, PDF, YouTube, recency-tiered news, arXiv, Wikipedia, local, finance, legal, medical, shopping, images). It also pulls from at least eight providers: its own crawler, Bright Data, Oxylabs, Yelp, TripAdvisor, Microsoft **Web IQ**, and anonymous channels. Google and Bing remain active sources. A `result_source` field leaked in SSE from 2026-05-21 to 2026-07-21 | https://peec.ai/blog/chatgpt-built-its-own-search-index (2026-09-25; vendor research) |
| Google via SerpApi | Reports in 2025 said ChatGPT's answers used Google results obtained through SerpApi. Google sued SerpApi on 2025-12-19 | https://searchengineland.com/openai-chatgpt-serpapi-google-search-results-461226 (2025; fetch blocked, from snippet); https://cloro.dev/blog/bing-search-api-key/ (2026) |
| Bing | Bing Search API retired 2025-08-11. Microsoft now sells Bing grounding as Web IQ (Build 2026). Whether ChatGPT uses Web IQ is **conflicting**: Peec lists it as a provider, SEJ says Microsoft didn't name any platform | https://www.searchenginejournal.com/microsoft-web-iq-gives-ai-agents-bing-grounding-apis/577736/ (2026-06-02) |
| Crawlers | **OAI-SearchBot/1.4** (search inclusion; respects robots.txt; ~24h to take effect; IPs at openai.com/searchbot.json). **GPTBot/1.4** (training; robots.txt; gptbot.json). **ChatGPT-User/1.0** (user-initiated fetches and GPT Actions; "robots.txt rules may not apply"; chatgpt-user.json). **OAI-AdsBot/1.0** (ad landing-page safety; not robots-governed). If both OAI-SearchBot and GPTBot are allowed, "we may use the results from just one crawl for both" | https://developers.openai.com/api/docs/bots (n.d., current July 2026 per PPC Land); https://ppc.land/openai-revises-chatgpt-crawler-documentation-with-significant-policy-changes/ (2025-12-09) |
| JS rendering | None observed for GPTBot (and by implication OAI-SearchBot). Vercel: GPTBot fetches JS files (11.5%) but never executes them. 34.8% of its fetches hit 404s | Vercel (2024-12); 2026 claims of "500M fetches, zero JS" are from agency blogs, **unverified** |
| Opt-out semantics | Blocking OAI-SearchBot removes the site from ChatGPT search answers. Blocking GPTBot only affects training | OpenAI bots doc |
| Tracking | Outbound links carry `utm_source=chatgpt.com` | OpenAI Publishers FAQ https://help.openai.com/en/articles/12627856-publishers-and-developers-faq (403 on fetch; via search snippet, n.d.) |
| Shopping | Merchant **product feeds** (CSV/JSON: IDs, descriptions, price, inventory, media, fulfilment; reviews "enhance ranking"). Onboarding is limited to approved partners. The shopping index is being A/B tested on 8–20% of chats | https://developers.openai.com/commerce/guides/key-concepts (n.d.); https://explodingtopics.com/blog/agentic-commerce-protocol (2026); Peec (2026-09-25) |
| Checkout | Instant Checkout + **Agentic Commerce Protocol** (with Stripe, Apache-2.0) launched Sept 2025. OpenAI wound down the first Instant Checkout in **March 2026** ("did not offer the level of flexibility…") and lets merchants use their own checkout. In-chat buying came back via Shopify's agentic stack; Visa Intelligent Commerce was added 2026-06-10. ACP lives on; the merchant stays merchant of record | explodingtopics (2026); https://opascope.com/insights/ai-shopping-assistant-guide-2026-agentic-commerce-protocols/ (2026) |
| Ads | Announced 2026-01-17, testing to logged-in adult US free users. OpenAI says advertisers cannot influence answers. ~$1B ad revenue by Aug 2026 (Wikipedia; **unverified**) | https://en.wikipedia.org/wiki/ChatGPT (accessed 2026-09-26) |
| Atlas browser | Launched 2025-10-21 (macOS). Its UA is identical to desktop Chrome, so it can't be told apart in logs. OpenAI told site owners to use **ARIA roles/labels** so the agent works reliably. **Discontinued 2026-08-09**; its agentic browsing moved into the unified ChatGPT/Codex desktop app | https://en.wikipedia.org/wiki/ChatGPT_Atlas (accessed 2026-09-26); https://help.openai.com/en/articles/20001371 (title only; fetch blocked) |
| Apps | Apps in ChatGPT (Apps SDK on MCP) launched Sept/Oct 2025. Wikipedia says they were renamed "plugins" in July 2026 (**unverified**) | Wikipedia ChatGPT |
| Scale | ~900M weekly active users (Feb 2026) | Wikipedia ChatGPT |

### How sources get chosen
OpenAI publishes no ranking factors. What we can infer: the answer comes from the union of provider results plus Labrador verticals, and citation eligibility depends on OAI-SearchBot access and on being indexed by the upstream providers (Google, Bing/Web IQ). Vertical indexes (news by recency, Wikipedia, YouTube, local via Yelp and TripAdvisor) explain why those domains show up so often in ChatGPT citations. Ahrefs/Semrush-type studies consistently put Wikipedia and Reddit at the top of ChatGPT citations (Wikipedia in 26–48% of top-10 answers per aggregated indices; [everything-pr index, 2026](https://everything-pr.com/ai-platform-citation-source-index-2026), secondary aggregation, directional only).

### What to do for ChatGPT
1. **Allow `OAI-SearchBot`** (required for citation). Decide on `GPTBot` separately (training). Don't rely on robots.txt for `ChatGPT-User`; use WAF rules if you truly must block it.
2. **Server-render** all primary content. Assume OpenAI's bots see only the raw HTML response.
3. Get indexed in **Bing and Google** (ChatGPT still draws on both) and keep IndexNow pings flowing (§5).
4. Local: keep **Yelp and TripAdvisor** profiles complete; they are named ChatGPT providers.
5. Commerce: apply for the product-feed program. Keep price and availability fresh; include reviews and all identifiers. Implement ACP only if on Shopify or a supported partner.
6. With homepages now getting ~62% of ChatGPT referrals, make the homepage entity-clear (what you are, for whom, key facts, prices, links to deep pages).
7. Agent readiness: semantic HTML, ARIA labels on interactive controls, forms that work without hover or JS-only tricks.
8. Monitor with a GA4 segment on `utm_source=chatgpt.com` plus referrer `chatgpt.com`, and server-log counts for OAI-SearchBot and ChatGPT-User (verify against OpenAI's IP JSON). OpenAI has no official citation report.

---

## 4. Perplexity (incl. Comet, Sonar / Search API)

| Item | Detail | Source (date) |
|---|---|---|
| Index | **Own index**: "hundreds of billions of webpages" exposed via the Search API. More than 200B unique URLs tracked, 400+ PB hot storage, tens of thousands of index updates per second, AI-generated parsing logic. **Sub-document retrieval**: pages are split into fine-grained units and scored individually. Hybrid lexical + semantic retrieval with multi-stage ranking; 358 ms median latency | https://www.perplexity.ai/hub/blog/introducing-the-perplexity-search-api (2025-09); research article via https://www.pymnts.com/artificial-intelligence-2/2025/perplexity-says-new-search-api-accesses-same-infrastructure-as-public-search-engine/ (2025) and search summaries; primary research page returned 403 |
| Crawlers | **PerplexityBot/1.0** (surfaces and links sites; not used for training; respects robots.txt; perplexitybot.json). **Perplexity-User/1.0** (user-initiated; "generally ignores robots.txt"; perplexity-user.json) | https://docs.perplexity.ai/guides/bots (n.d., accessed 2026-09-26) |
| Stealth dispute | Cloudflare (2025-08-04): declared Perplexity-User made 20–25M requests/day, and an undeclared Chrome-on-macOS UA made 3–6M requests/day from rotating IPs and ASNs to get around blocks. Cloudflare de-listed Perplexity as a verified bot and shipped managed-rule signatures to all plans. Perplexity blamed BrowserBase traffic (<45k/day). No resolution found as of Sept 2026 | https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/ (2025-08-04); https://www.theregister.com/2025/08/05/perplexity_vexed_by_cloudflares_claims/ (2025-08-05) |
| JS rendering | No JS execution observed for PerplexityBot | Vercel (2024-12) |
| API | Sonar models (Chat Completions) are superseded by the Agent API, "supported until September 27, 2026"; the Search API returns ranked sub-document snippets | search summary citing Perplexity docs, **unverified** exact wording |
| Comet | Chromium AI browser: Win/macOS 2025-07-09, free from Oct 2025, Android 2025-11-20, iOS 2026-03-18 | https://en.wikipedia.org/wiki/Comet_(browser) (accessed 2026-09-26) |
| Publisher economics | Publisher Program (July 2024, ad rev-share). **Perplexity dropped AI-integrated advertising in Feb 2026** (subscription-first). Comet Plus ($5, included in Pro/Max) passes revenue to participating publishers minus compute costs (commonly reported as 80%; **unverified**) | https://en.wikipedia.org/wiki/Perplexity_AI (accessed 2026-09-26); https://suprmind.ai/hub/perplexity/pricing/ (2026) |
| Legal | Suits from News Corp (2024), Reddit (Oct 2025), plus BBC, Yomiuri, Asahi, Nikkei claims | Wikipedia Perplexity AI |
| Reporting | No publisher dashboard. Referrer `perplexity.ai`; log PerplexityBot and Perplexity-User | — |

**How it ranks sources:** Perplexity's own statements stress passage-level scoring (sub-document units), freshness from high-rate index updates, and multi-stage reranking. Community reverse-engineering claims (manual domain boosts, L3 XGBoost reranker, time-decay) circulate widely but are **unverified**.

**Actions:** allow `PerplexityBot`. Write **self-contained passages** (each H2/H3 section answers one question with the facts inline), since Perplexity scores sub-document units. Keep pages fresh with visible, accurate dates. Server-render. If you use Cloudflare, check whether managed rules are blocking Perplexity-User when you actually want user-triggered fetches. Perplexity sends only about 1–7% of AI referrals depending on panel, so weight effort accordingly.

---

## 5. Microsoft Copilot and Bing AI answers

| Item | Detail | Source (date) |
|---|---|---|
| Index | **Bing index.** Web IQ (Build 2026) is a set of grounding APIs on Bing's index that return **passages and structured evidence objects**, not full pages; "a search engine for AI systems"; sub-165 ms p95; honors robots.txt | https://www.searchenginejournal.com/microsoft-web-iq-gives-ai-agents-bing-grounding-apis/577736/ (2026-06-02) |
| Crawler | Bingbot. It renders JS, but assume a render budget; exact 2026 behaviour **unverified** | — |
| Controls | `NOARCHIVE` → not included or linked in Bing Chat/Copilot answers and not used for training. `NOCACHE` → only URL, title and snippet used. Classic Bing results are unaffected | https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat (2023-09-22) |
| Freshness | **IndexNow** (Bing, Naver, Seznam, Yandex, Yep; Amazon and Shopify adopted May 2025). Microsoft explicitly recommends it "for faster content discovery across search and AI systems" | https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview (2026-02-10) |
| Reporting | **Bing Webmaster Tools → AI Performance** (public preview 2026-02-10): Total Citations, Average Cited Pages/day, **Grounding Queries**, page-level citation activity, covering Copilot, Bing AI summaries and "select partner integrations". June 2026 added **Intents, Topics, Citation Share** (your share of all citations for a grounding query) and **Compare**. No click data | BWT blog (2026-02-10); https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/ (2026-06-16) |

### Microsoft's official content guidance (the most prescriptive of any vendor)
"Optimizing Your Content for Inclusion in AI Search Answers", Krishna Madhavan, Principal PM, Bing ([Microsoft Advertising blog, 2025-10-08](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers)): AI assistants "break content down into smaller, structured pieces" and assemble answers from several sources.
- **Do:** clear titles, H1s and descriptions matched to intent; H2/H3 that "define clear content slices"; Q&A formats; lists, numbered steps and comparison tables; **JSON-LD schema** (Product, Review, FAQ, Event); concise, self-contained answers of 1–2 sentences; claims anchored in measurable facts; synonyms; fresh, authoritative content with evidence; the same entity shown consistently across text, images and video.
- **Don't:** long walls of text; answers hidden in **tabs/accordions**; core information only in **PDFs**; key facts only in **images**; vague superlatives; decorative symbols (→ ★★★ !!!); overloaded sentences; excessive em dashes.
- Also: register in **Bing Places** for local; strengthen depth and FAQ sections (BWT AI Performance post, 2026-02-10).

Note the **tension with Google**, which says chunking and special rewrites are unnecessary *for Google*. A universal skill should write passages that are self-contained and well structured (which helps Bing, Copilot and Perplexity passage retrieval) without fragmenting pages or duplicating content, which Google penalises as scaled abuse.

**Actions:** verify the site in BWT. Submit sitemaps. Implement **IndexNow** on publish, update and delete. Watch AI Performance → Grounding Queries to learn how Copilot phrases retrieval, and use Citation Share per topic as the KPI. Follow the do/don't list above. Use `NOARCHIVE` only if you mean to leave Copilot answers entirely. Bing coverage also feeds ChatGPT (partly) and many API-grounded products, so it counts for far more than Copilot's ~2% chatbot share.

---

## 6. Anthropic Claude

| Item | Detail | Source (date) |
|---|---|---|
| Search provider | **Brave Search**, listed on Anthropic's subprocessor list as the "Web Search" vendor for all products (search.brave.com) | https://ryandoser.com/what-search-engine-does-claude-use/ (n.d.) quoting Anthropic's subprocessor list; the primary list is paginated and I could not fetch it, so primary confirmation is **unverified** by me |
| Crawlers | **ClaudeBot** (training; robots.txt; honors `Crawl-delay`). **Claude-User** (user-directed fetches; **respects robots.txt**). **Claude-SearchBot** (indexes content "to enhance search result quality"; robots.txt). IPs at `https://claude.com/crawling/bots.json` | https://support.claude.com/en/articles/8896518 (upd. 2026-04-07) |
| JS rendering | ClaudeBot downloads JS (23.8% of fetches) but doesn't execute it; heavy on images (35%); ~34% of fetches are 404s | Vercel (2024-12) |
| API behaviour | Claude decides when to search (current, changing or entity-specific information) and runs 1–3 searches for simple facts, 10+ for research. Results carry `url`, `title`, **`page_age`**. Citations are always on, with `cited_text` up to 150 chars. Dynamic filtering (`web_search_20260209`+) lets Claude run code that filters results before they reach context. Domain allow and block lists; $10 per 1,000 searches | https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool (accessed 2026-09-26) |
| Consumer | Web search on all plans globally since 2025-05-27 | https://claude.com/blog/web-search (2025-05-27) |
| Reporting | None. Referrer `claude.ai`; log Claude-User and Claude-SearchBot | — |

**Actions:** allow **Claude-SearchBot and Claude-User**. Blocking ClaudeBot (training) is separate and harmless to citation. **Check your visibility in Brave Search** (search.brave.com): a site that ranks on Google can be missing from Brave. Keep `page_age` signals honest (visible and structured dates) and put quotable facts in short sentences, since citations quote ≤150 chars. Claude is the fastest-growing referrer (+320% YoY per SE Ranking; ~9% of chatbot visits).

---

## 7. Brave Search (and the long tail of LLM apps grounded on it)

| Item | Detail | Source (date) |
|---|---|---|
| Index | Independent index of **40B+ pages** (Brave's figure, per search summary; **unverified** exact number) | https://brave.com/search/api/ (n.d.) |
| Crawler | **No distinct UA**; it identifies as a normal browser "to avoid discrimination from websites that allow only Google". Follows **Googlebot's** robots.txt rules ("if a domain or page is not crawlable by Googlebot, then Brave Search's bot will not crawl it either"). robots.txt doesn't prevent *indexing*, so use `noindex`. Partly fed by the opt-in Web Discovery Project. Removal via search.brave.com/submit-url | https://search.brave.com/help/brave-search-crawler (n.d., accessed 2026-09-26) |
| AI API | **LLM Context API** (since 2026-02-06): web search, then HTML converted to "smart chunks", then chunk ranking; token budget 1,024–32,768; <500 ms p90; $5 per 1k requests. Used by Claude, "Ask Brave" (Qwen3) and many agent frameworks | https://brave.com/blog/most-powerful-search-api-for-ai/ (2026, updated with June 2026 tests); https://api-dashboard.search.brave.com/documentation/services/llm-context (n.d.) |

**Actions:** don't block Googlebot-equivalent crawling for any path you want in AI answers (Brave inherits it). Search your key queries on search.brave.com and submit missing URLs. Clean HTML with tables and code blocks survives chunking best.

---

## 8. Apple (Siri, Spotlight, Safari, Apple Intelligence)

| Item | Detail | Source (date) |
|---|---|---|
| Crawler | **Applebot** powers Spotlight, Siri, Safari and Apple Intelligence answers. Verify via reverse DNS `*.applebot.apple.com` or applebot.json. Falls back to Googlebot rules if no Applebot group. **Does render JS** ("browser rendering"), so don't block JS/CSS/XHR. The support page says crawl-delay is not followed; a June 2026 rewrite reportedly added crawl-delay support (**conflicting**) | https://support.apple.com/en-us/119829 (accessed 2026-09-26); https://ppc.land/apple-rewrites-applebot-rules-to-feed-siri-ai-what-publishers-must-know/ (2026-06) |
| Training control | **Applebot-Extended** doesn't crawl; it only governs whether Applebot-crawled data trains Apple foundation models. Disallowing it isn't a Search ranking factor and doesn't remove you from results (clarified around 2026-09-07) | Apple support; https://www.relevantaudience.com/geo/apple-applebot-extended-blocking-does-not-affect-search-ranking/ (2026-09) |
| Answer control | `nosnippet` (meta or X-Robots-Tag) blocks use as context in AI-generated answers. Paywalled content should use `isAccessibleForFree: false` JSON-LD to keep it out of AI context | Apple support page |

**Actions:** allow Applebot and don't block JS/CSS. Keep paywall markup correct. Use `nosnippet` only where you truly don't want Siri or Apple Intelligence answers to use the text.

---

## 9. Meta AI

| Item | Detail | Source (date) |
|---|---|---|
| Index | Building its own index via **Meta-WebIndexer** ("improve Meta AI search result quality"; respects robots.txt; token `meta-webindexer`). It previously relied on Google and Bing for news, stocks and sports, and has a Reuters content deal | https://developers.facebook.com/documentation/sharing/webmasters/web-crawlers (n.d.); https://ppc.land/meta-webindexer/ (2026-08) |
| Other bots | `Meta-ExternalAgent` (training / product indexing; robots.txt). `Meta-ExternalFetcher` (user-initiated and agentic fetches; "may bypass robots.txt"). `facebookexternalhit` (link previews) | Meta crawler docs |
| Activity | WebIndexer passed Meta's training crawler in June 2026 and reached 37.8% of tracked AI-crawler requests by 2026-08-09 (from ~2.2% in mid-July); vendor telemetry | ppc.land (2026-08) |

**Actions:** allow `meta-webindexer` if you want Meta AI (WhatsApp, Instagram, Facebook, Messenger) citations. Block `Meta-ExternalAgent` separately if you object to training. Watch server load, because WebIndexer is currently aggressive; rate-limit rather than block.

---

## 10. xAI Grok

| Item | Detail | Source (date) |
|---|---|---|
| Retrieval | Two tools: **Web Search** (supports allowed/excluded domains, max 5) and **X Search** (live posts). No documented index provider | https://docs.x.ai/developers/tools/web-search (n.d., accessed 2026-09-26); https://docs.x.ai/developers/tools/x-search (n.d.) |
| Crawler | **No published xAI crawler or robots token**, so robots.txt can't govern Grok fetches | https://organikpi.com/blog/geo-ai-search/grok-xai-seo-guide/ (2026, agency) and other secondary sources; **unverified** by a primary source |
| Source mix | X posts are reportedly ~45% of Grok citations; one dataset had 40,624 X citations vs 12,507 Wikipedia; ~4.7 sources per answer | https://presenc.ai/research/grok-citation-patterns-2026 and https://contextbolt.com/blog/grok-seo/ (2026, vendor; **unverified**) |

**Actions:** keep an active, ideally verified, **X account** that posts the same facts as the site, since X is Grok's biggest source. Otherwise normal web visibility applies. Grok is ~2.4–2.8% of chatbot visits.

---

## 11. DeepSeek, You.com, Amazon (Rufus / Alexa+)

- **DeepSeek:** ~3.4–4.0% of chatbot visits (Similarweb, June–Aug 2026). No published crawler, robots token or search-provider disclosure found. Retrieval stack **unverified**. No site-owner action beyond general web visibility.
- **You.com:** now mainly an **LLM search-API vendor** (Web Search, Contents, Answer, Research, and Finance APIs with a finance-optimised index; MCP server at api.you.com/mcp), with its own index implied ([you.com/apis](https://you.com/apis), n.d.). Crawler UA not documented (**unverified**).
- **Amazon:** `Amazonbot/0.1` (products and **AI training**), **`Amzn-SearchBot/0.1`** (search experiences such as **Alexa**; *not* used for training), `Amzn-User/0.1` (live user fetches for Alexa; not training). All respect robots.txt (cached up to 30 days, ~24h to apply) and ignore crawl-delay. Meta support: `noindex`, `noarchive` (= no model training), `none`, `rel=nofollow` ([developer.amazon.com/amazonbot](https://developer.amazon.com/amazonbot), 2026). Whether Amzn-SearchBot feeds **Rufus** is claimed by secondary sources but not stated in Amazon's doc (**unverified**). Rufus mainly draws on Amazon catalogue data, so for sellers, listing quality is the lever.

---

## 12. Cross-cutting facts the skill must encode

1. **JavaScript:** only Google (Googlebot/Gemini) and Applebot are documented to render JS. Treat OpenAI, Anthropic, Perplexity, Meta, ByteDance and similar as **raw-HTML-only**; Vercel measured none of them executing JS ([Vercel, 2024-12](https://vercel.com/blog/the-rise-of-the-ai-crawler)). Brave and Bingbot render to some extent (**unverified** for 2026). **Rule: SSR/SSG every indexable page; primary content, headings, prices, dates and JSON-LD must be in the initial HTML.**
2. **Three kinds of bot per vendor:** *training* (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent, Amazonbot), *search index* (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Meta-WebIndexer, Amzn-SearchBot, Googlebot, Bingbot, Applebot), and *user-triggered* (ChatGPT-User, Claude-User, Perplexity-User, Meta-ExternalFetcher, Amzn-User, Google-Agent). Blocking training bots does **not** cost citations, with one exception: Google-Extended also gates Gemini-app grounding. Blocking search-index bots removes you. User-triggered fetchers mostly ignore robots.txt; Claude-User and Amzn-User are the exceptions and respect it.
3. **404 waste:** AI crawlers spend ~34% of fetches on 404s (Vercel). Keep redirects for moved URLs and fix broken internal links; hallucinated URLs from LLMs are a known source of this.
4. **Passage-level retrieval is now explicit** at Perplexity (sub-document units), Bing/Web IQ (passage evidence objects), Brave (smart chunks) and Claude (150-char `cited_text`). Google says you needn't chunk *for Google*. The shared answer: well-headed sections whose first 1–2 sentences answer the heading's question on their own.
5. **Freshness signals:** Claude exposes `page_age`; Perplexity updates its index at very high frequency; ChatGPT has a recency-tiered news index; Microsoft recommends IndexNow. Show accurate `datePublished`/`dateModified` (visible and in JSON-LD), update sitemaps' `lastmod` truthfully, and ping IndexNow.
6. **Third-party presence matters by platform:** YouTube (Google AIO), Reddit and Wikipedia (everywhere, esp. ChatGPT), Yelp/TripAdvisor (ChatGPT local), X (Grok), Bing Places / Google Business Profile (local), Merchant Center / OpenAI feeds (commerce). Across multiple 2026 aggregations the top cited domains are Reddit, Wikipedia, YouTube, LinkedIn and Forbes ([everything-pr 2026 index](https://everything-pr.com/ai-platform-citation-source-index-2026), secondary aggregation; directional only).

---

## 13. Cross-platform comparison table

| Platform | Retrieval index | Search-index bot (allow to be cited) | Training bot (can block safely) | User-triggered fetcher (robots?) | Renders JS | Answer-level controls | First-party reporting | Referral ID |
|---|---|---|---|---|---|---|---|---|
| Google AIO / AI Mode | Google index + query fan-out (Gemini 3 / 3.5 Flash) | Googlebot | Google-Extended (does **not** affect AIO/AI Mode) | Google-Agent (ignores) | Yes | nosnippet, data-nosnippet, max-snippet, noindex, **Search Console gen-AI toggle** | **SC Generative AI report** (impressions only) | google.com (mixed into organic) |
| Gemini app / API | Google Search grounding | Googlebot | Google-Extended (**also removes grounding**) | Google-GeminiNotebook (ignores) | Yes | Google-Extended | None | gemini.google.com |
| ChatGPT | Own "Labrador" indexes + Bing/Web IQ, Google (SerpApi), Yelp, TripAdvisor, others | OAI-SearchBot | GPTBot | ChatGPT-User (may ignore) | No | robots only | None (utm_source=chatgpt.com) | chatgpt.com |
| Perplexity | Own index (200B+ URLs, sub-document) | PerplexityBot | (n/a; PerplexityBot is not training) | Perplexity-User (ignores; stealth dispute) | No | robots only | None | perplexity.ai |
| Copilot / Bing AI | Bing index / Web IQ passages | Bingbot | (NOARCHIVE/NOCACHE meta) | n/a | Partial (**unverified**) | NOARCHIVE, NOCACHE, IndexNow for freshness | **BWT AI Performance** (citations, grounding queries, citation share) | copilot.microsoft.com, bing.com |
| Claude | Brave Search | Claude-SearchBot | ClaudeBot | Claude-User (**respects**) | No | robots only | None | claude.ai |
| Brave / Brave-API LLMs | Brave independent index | Undifferentiated UA, follows Googlebot rules | n/a | n/a | **unverified** | noindex (robots.txt doesn't stop indexing) | None | search.brave.com |
| Apple Intelligence / Siri | Applebot index | Applebot | Applebot-Extended | n/a | Yes | nosnippet, isAccessibleForFree | None | n/a |
| Meta AI | Own index (building) + Google/Bing legacy | meta-webindexer | Meta-ExternalAgent | Meta-ExternalFetcher (may ignore) | **unverified** (likely no) | robots only | None | meta.ai, in-app |
| Grok | Web Search + X Search | None published | None published | None published | **unverified** | None | None | grok.com, x.com |
| Amazon Alexa+ / Rufus | Amazon index + catalogue | Amzn-SearchBot | Amazonbot | Amzn-User (respects) | **unverified** | noindex, noarchive | None | n/a |
| DeepSeek | **unverified** | none published | none published | none published | **unverified** | — | None | chat.deepseek.com |

### Minimum universal robots.txt stance for "be cited everywhere"
Allow: Googlebot, Bingbot, Applebot, OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, meta-webindexer, Amzn-SearchBot, Amzn-User, Google-Extended (if Gemini grounding matters). Optional to block: GPTBot, ClaudeBot, Applebot-Extended, Meta-ExternalAgent, Amazonbot, CCBot. Check that the CDN/WAF (Cloudflare "AI bots" managed rules, bot-fight mode) isn't silently overriding robots.txt for the search-purpose bots. This is a frequent hidden cause of zero AI citations (inference from the Cloudflare/Perplexity case and Cloudflare's managed-rule rollout; **no single primary source**).

### Monitoring stack by platform
- Google: Search Console Generative AI report (impressions) + GA4 landing pages.
- Microsoft: BWT AI Performance (citations, grounding queries, citation share, intents, topics).
- Everyone else: server logs by verified UA/IP JSON (OpenAI, Perplexity, Anthropic, Apple, Amazon publish IP lists), GA4 referral segments (chatgpt.com, perplexity.ai, claude.ai, gemini.google.com, copilot.microsoft.com, meta.ai, grok.com, chat.deepseek.com), and periodic prompt sampling with third-party trackers (label these as estimates; Google warns against tools that claim internal Google data).

---

## Source list (primary first)
- Google: ai-features doc (2025-12-10); AI optimization guide (2026-05-15 / upd. 2026-07-10); common crawlers (2026-07-14); user-triggered fetchers (2026-08-19); SC gen-AI report help (n.d.); SC blog gen-AI reports (2026-06); new controls post (2026-06-03 / 2026-08-31); I/O 2026 Search post (2026-05-19); I/O 2025 AI Mode post (2025-05-20); UCP/agentic commerce (2026-01-11); GML 2026 shopping (2026-05-20); Merchant UCP help (n.d.); Gemini API grounding doc (n.d.); Vertex grounding doc (n.d.).
- OpenAI: bots doc (n.d., ~July 2026); commerce key concepts (n.d.); publishers FAQ (n.d., 403).
- Microsoft: AI content guidance (2025-10-08); BWT AI Performance (2026-02-10); BWT AI visibility insights (2026-06-16); NOCACHE/NOARCHIVE (2023-09-22).
- Anthropic: crawler help (2026-04-07); web search tool docs (accessed 2026-09-26); web search blog (2025-05-27).
- Perplexity: bots doc (n.d.); Search API blog (2025-09). Cloudflare stealth-crawling report (2025-08-04).
- Brave: crawler help (n.d.); LLM Context API blog (2026). Apple: Applebot support page (accessed 2026-09-26). Meta: crawler docs (n.d.). Amazon: Amazonbot page (2026). xAI: web search docs (n.d.). You.com APIs (n.d.).
- Research and press: arXiv 2605.14021 (2026-05-13); Ahrefs via SEJ (2026-03-02); SEJ opt-out analysis (2026-08-01); SEJ Google guide (2026-05-15); SEJ Web IQ (2026-06-02); Peec AI ChatGPT index (2026-09-25); PPC Land OpenAI crawlers (2025-12-09), Similarweb June data (2026-06-11), Meta-WebIndexer (2026-08), Applebot (2026-06); Similarweb AI stats (2026-07-29); SE Ranking AI traffic (2026, date unverified); Vercel AI crawler study (2024-12); Wikipedia ChatGPT / ChatGPT Atlas / Perplexity AI / Comet (accessed 2026-09-26); explodingtopics ACP (2026); The Register (2025-08-05).
