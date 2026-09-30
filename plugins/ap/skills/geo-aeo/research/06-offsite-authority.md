# 06 — Off-site signals: brand authority, mentions, and the sources LLMs cite and learn from

Research date: 2026-09-26. Every number carries its source URL and that source's publication date. Where a claim comes only from a vendor blog or aggregator with no visible method, it is marked **(vendor, method thin)**. Where I could not trace it to a primary source, it is marked **(unverified)**. Note: the web-search budget ran out partway through, so the Malaysia/SEA section relies more on reasoning than the rest. Those points are flagged.

---

## 0. The one-paragraph version (for the skill's decision logic)

AI answers are built from **what other sites say about a brand**, not mainly from the brand's own site. Several large correlation studies agree. Unlinked brand mentions (~0.66) and YouTube mentions (~0.74) track AI visibility 2–3x more strongly than backlinks (~0.22–0.30) (Ahrefs, 2025-05-26 and 2025-12-12). Earned media makes up 82–89% of AI citations (Muck Rack, 2026-05-07). Third-party "best X" listicles are the single biggest page type ChatGPT cites (43.8%) (Ahrefs, 2025-12-04). Which domains get cited is **unstable**. ChatGPT's Reddit share fell from ~60% to ~10% of responses in six weeks in Aug–Sep 2025 (Semrush, 2025-11-10). It fell again, from 3.8% to 0.5% of citations, in August 2026 (Semrush, 2026-08-26). So the durable strategy is to be **consistently described, by many independent credible sources, across many surfaces**, rather than to game one platform. The manipulative shortcuts now carry real enforcement. These include fake reviews (FTC civil penalties of $51,744 per violation), Reddit astroturfing (Reddit's AI removes about 25k spam items a day), and hidden prompt injection (Google spam policy updated 2026-08-28; Microsoft documented 31 companies doing "AI recommendation poisoning").

---

## 1. Brand mentions vs backlinks: the evidence

### 1.1 Ahrefs, 75k-brand study, round 1 (AI Overviews only)
- Source: https://ahrefs.com/blog/ai-overview-brand-correlation/ (2025-05-26, Louise Linehan and Xibeijia Guan).
- Method: 75,000 brands, domains with DR>40, each brand's top keyword at ≥800 searches/month. AIO mentions counted via Brand Radar. Spearman correlation.
- Spearman ρ with AI Overview brand mentions:
  - branded web mentions **0.664**
  - branded anchors 0.527
  - branded search volume 0.392
  - Domain Rating 0.326
  - referring domains 0.295
  - branded traffic 0.274
  - **backlinks 0.218**
  - ad traffic 0.216, ad cost 0.215
  - URL Rating 0.18
  - site pages 0.17
- The drop-off is steep. The top quartile by web mentions averages **169** AIO mentions; the next quartile averages **14**. The bottom 50% are near-invisible, and **26%** of brands had zero AIO mentions.
- Paid search spend barely correlates, at ~0.21.
- The authors' own caveat: "correlation ≠ causation". All the correlations are moderate to weak.

### 1.2 Ahrefs round 2 (ChatGPT, AI Mode, AIO): YouTube comes out on top
- Source: https://ahrefs.com/blog/ai-brand-visibility-correlations (2025-12-12). A press re-release was reported by TNW on 2026-05-27: https://thenextweb.com/news/ahrefs-youtube-mentions-ai-visibility-brand-search
- Correlations by platform (ChatGPT / AI Mode / AIO):

| Factor | ChatGPT | AI Mode | AIO |
|---|---|---|---|
| YouTube mentions (title, transcript, description) | 0.737 | 0.740 | 0.712 |
| YouTube mention impressions | 0.717 | 0.724 | 0.704 |
| Branded web mentions | 0.664 | 0.709 | 0.656 |
| Branded anchors | 0.511 | 0.628 | 0.527 |
| Branded search volume | 0.352 | 0.466 | 0.392 |
| Domain Rating | 0.266 | 0.285 | 0.326 |
| Backlinks | ~0.25 | ~0.30 | ~0.27 |

- Mention frequency beats reach. Many mentions in low-view videos correlate better than a single viral video (TNW summary, 2026-05-27).
- The three platforms name largely the same brands, with output overlap of 0.749–0.821.
- **AI Mode favours established brands. ChatGPT looks most open to emerging brands** (Ahrefs, 2025-12-12).

### 1.3 Google looks more brand-biased than ChatGPT or Perplexity
- Source: https://ahrefs.com/blog/branded-web-mentions-visibility-ai-search/ (2025-07-07).
- Top 50 brands. Data: ~76.7M AIOs, 957k ChatGPT prompts, 953.5k Perplexity prompts (June 2025).
- Web mentions vs visibility: **AIO ρ=0.65**, **Perplexity 0.30**, **ChatGPT 0.15**.
- Implication: for Google surfaces, off-site brand scale is close to table stakes. On ChatGPT, a small brand can still win specific prompts through topical and listicle presence.

### 1.4 Listicle inclusion as a mention signal
- Source: https://ahrefs.com/blog/best-lists-research/ (2025-12-04, Glen Allsopp).
- Method: 750 top-of-funnel prompts (software, products, agencies), 26,283 cited URLs.
- **43.8%** of cited page types were blog-format "best X" lists.
- **67.6%** of Google "best X software" SERPs contained a list where the publisher ranked itself first.
- 79.1% of 1,100 cited lists had been updated in 2025, and 26% within the previous two months.
- Brands ranked higher on third-party lists were more likely to be mentioned, though not linearly.
- Caveats: 35% of cited lists came from low-authority domains. Ahrefs caps its own self-promotional lists at <0.5% of its blog output and links to competitors in them.
- Secondary claim (unverified; aggregated in search snippets and attributed to Tim Soulo at Ahrefs): third-party lists take 80.9% of listicle citations vs 19.1% for self-promotional lists. Across 95 brands, category-listicle share correlates r=+0.64 with ChatGPT naming the brand. Could not open the primary page. Treat as directional.

### 1.5 Mentions ≠ citations (two separate visibility games)
- Semrush, 5 verticals: only **6–27%** of the most-mentioned brands are also among the most-cited sources. Zapier is the #1 cited source in digital tech but #44 in brand mentions. https://www.semrush.com/blog/ai-search-visibility-study-findings/ (2025-09-03).
- Semrush and Growth Memo "ghost citations": **61.7%** of source citations appear with no brand-name mention in the answer. Method: 3,981 domain appearances, 115 prompts, 14 countries.
  - ChatGPT cites 87% of the time but mentions only 20.7%. Gemini mentions 83.7% but cites 21.4%.
  - Comparative queries produce 2.4x more mentions than informational ones.
  - https://www.semrush.com/blog/the-ghost-citations-study/ (2026-06-09)
- Semrush AI Visibility Index: on Gemini, the overlap between mentioned brands and cited domains can be as low as 30%. Only 36 brands held top-100 visibility on every engine every month. https://www.semrush.com/news/463141-semrush-releases-expanded-2026-ai-visibility-index-analyzing-126-million-ai-search-prompts/ (2026-06-26; 126M US prompts, Jan–Apr 2026).
- **Skill rule:** track **mention share** (is the brand named?) and **citation share** (is the brand's URL used as evidence?) separately. Off-site work mostly moves mentions. On-site work mostly moves citations.

### 1.6 Co-occurrence, sentiment, and consensus
- Ahrefs describes ChatGPT selection as reflecting "consensus across authoritative sources". When multiple credible sites call a brand a strong option, the model repeats it. https://ahrefs.com/blog/how-to-rank-on-chatgpt (2026-03-13). This is a mechanism claim, supported only by correlations.
- Co-occurrence of brand + category term is the actual unit of a "branded web mention" in the Ahrefs studies, which count mentions tied to the brand's top keyword. That is the closest measured proxy for co-citation.
- Sentiment: tools such as Ahrefs Brand Radar and Semrush now score the sentiment of each AI mention and show the cited source. https://ahrefs.com/brand-radar/. I found no public study quantifying how sentiment on source pages changes the chance of being recommended **(gap)**. The mechanism is plausible because answers paraphrase their sources (see Semrush LinkedIn semantic similarity of 0.57–0.60, §2.4).

### 1.7 Why this works: parametric knowledge scales with document frequency
- Kandpal et al., "Large Language Models Struggle to Learn Long-Tail Knowledge": a model's accuracy on a fact depends on how many pre-training documents mention it, with correlational and causal evidence. Retrieval augmentation reduces that dependence. https://arxiv.org/abs/2211.08411 (v2 2023-07-27).
- This is the academic basis for "be mentioned many times, consistently, in many crawlable places". Rare entities are poorly known and more likely to be hallucinated.

---

## 2. Which domains AI engines cite, by platform, and how it shifted

Metrics differ between studies: "% of responses citing the domain" vs "share of all citations" vs "share of the top-10/top-50". Numbers are not comparable across rows.

### 2.1 Profound, the baseline (Aug 2024–Jun 2025, 680M citations)
Source: https://www.tryprofound.com/blog/ai-platform-citation-patterns (2025-06-05, updated Aug 2025)
- **ChatGPT:** Wikipedia 7.8% of all citations (47.9% of top-10 share), Reddit 1.8%, Forbes 1.1%.
- **Google AIO:** Reddit 2.2%, YouTube 1.9%, Quora 1.5%.
- **Perplexity:** Reddit 6.6% (46.7% of top-10), YouTube 2.0%, Gartner 1.0%.
- .com domains made up more than 80% of citations. ChatGPT leaned on encyclopedic sources, Perplexity on community sources, and Google on both.

### 2.2 The September 2025 shock (ChatGPT)
Source: Semrush, 230k+ prompts, ChatGPT Search / AI Mode / Perplexity, 2025-07-14 to 2025-10-12, 100M+ citations. https://www.semrush.com/blog/most-cited-domains-ai/ (2025-11-10)
- ChatGPT responses citing **Reddit: ~60% → ~10%**. Citing **Wikipedia: ~55% → <20%**. This happened between early August and mid-September 2025.
- AI Mode and Perplexity were stable. Reddit fell only 11% on AIO and 31% on AI Mode.
- Winners on ChatGPT: **PRNewswire, Forbes, Medium**. LinkedIn rose on every platform.
- Suspected causes: Google's removal of `num=100` around 2025-09-11, plus a deliberate de-concentration by OpenAI. Semrush's Sergei Rogulin suggested the latter. Neither is confirmed.
- Post-shock top 5:
  - ChatGPT: Reddit, Wikipedia, Medium, Forbes, LinkedIn
  - AI Mode: LinkedIn (~15%), YouTube, Reddit, Google, Google Blog
  - Perplexity: Reddit, LinkedIn, NIH, Microsoft, Google

### 2.3 The August 2026 second drop
- Reddit's share of ChatGPT citations went **3.8% (2026-07-18 to 08-07) → 0.5% (08-14 to 08-17)**, an 86% fall. Data is from Promptwatch. Promptwatch can't rule out a collection artefact. OpenAI says it sets no fixed per-site visibility and still cites Reddit. https://www.semrush.com/blog/reddits-citations-in-chatgpt-fall/ (2026-08-26)
- Context: Reddit's data licences are up for renewal in 2026. Google pays ~$60M/yr (Feb 2024) and OpenAI ~$70M/yr (est.). https://www.cjr.org/analysis/reddit-winning-ai-licensing-deals-openai-google-gemini-answers-rsl.php (2025-10-02). CNBC reported that Reddit may not renew the Google deal: https://www.cnbc.com/2026/07/22/reddit-stock-google-ai-content-deal.html (2026-07-22; page blocked from fetch, headline only).
- **Skill rule:** never make one platform the whole plan. Reddit's weight in AI answers depends on commercial deals that can change in a week.

### 2.4 Current Google AIO leaderboard (Sept 2026)
Source: Ahrefs Brand Radar, 3M+ US queries, share among the top-50 cited domains. https://ahrefs.com/blog/most-cited-domains-ai-overviews/ (2026-09-02)

| # | Domain | Share |
|---|---|---|
| 1 | YouTube | 22.9% |
| 2 | Reddit | 18.5% |
| 3 | Facebook | 10.1% |
| 4 | Google | 8.8% |
| 5 | Instagram | 5.6% |
| 6 | Quora | 4.7% |
| 7 | Wikipedia | 4.0% |
| 8 | TikTok | 3.3% |
| 9 | Amazon | 3.3% |
| 10 | Walmart | 1.0% |
| — | Forbes | 0.8% |
| — | Healthline | 0.8% |
| — | Edmunds | 0.7% |
| — | NerdWallet | 0.6% |
| — | TripAdvisor | 0.6% |
| — | LinkedIn | 0.6% |

- Facebook, Instagram and TikTok together pass 19%. Social and UGC surfaces dominate Google's AI answers.

### 2.5 LinkedIn is rising (ChatGPT and AI Mode)
Source: Semrush, 325k prompts, Jan–Feb 2026, 89k LinkedIn URLs. https://www.semrush.com/blog/linkedin-ai-visibility-study/ (2026-03-10)
- LinkedIn is #2 overall, appearing in ~11% of responses: **ChatGPT Search 14.3%**, **AI Mode 13.5%**, Perplexity 5.3%.
- What gets cited:
  - Articles make up 50–66% of LinkedIn citations; posts make up 15–28%.
  - 95% are original content, not reshares.
  - 54–64% are educational or advice content.
  - Best length is 500–2,000 words for articles and 50–299 words for posts.
- Who gets cited:
  - ~75% of cited authors post 5+ times per four weeks.
  - Median engagement on a cited post is only 15–25 reactions.
  - Accounts under 500 followers are cited as often as larger ones.
- ChatGPT and AI Mode favour individuals (59%). Perplexity favours company pages (59%).
- AI answers paraphrase LinkedIn text closely: semantic similarity 0.57–0.60, vs 0.53–0.54 for Reddit and 0.435 for Quora.

### 2.6 YouTube
Source: OtterlyAI, 100M+ citations, 30 days. https://otterly.ai/blog/youtube-ai-citation-study-2026/ (2026-03-02) **(vendor, method described)**
- Of all YouTube citations, 38.7% come from Perplexity, 36.6% from AIO, 19.6% from AI Mode, 4.4% from ChatGPT, and under 1% from Copilot and Gemini.
- 94% of cited videos are long-form, not Shorts. 32.1% run 10–20 minutes.
- Views and likes have near-zero correlation with citation (r≈−0.03). Description length r≈0.31. Recency r≈0.3.
- Timestamps/chapters matter on Google surfaces. 73% of timestamped citations appear in AIO.
- The Ahrefs claim that GPT-4 was trained on >1M hours of YouTube transcripts is repeated in https://ahrefs.com/blog/how-to-rank-on-chatgpt (2026-03-13). It originates in 2024 press reporting, which I did not re-verify here **(unverified)**.

### 2.7 Earned media, journalism, and press releases
- **Muck Rack "What is AI Reading?"**: earned media is **82–89%** of citations across three editions (Jul 2025 → May 2026). Latest: **84%**. Journalism is **27%**. Paid or advertorial content is **0.3%**. Method: 25M+ links from ChatGPT, Claude and Gemini across 17 industries. https://muckrack.com/blog/what-is-ai-reading-may-2026 (2026-05-07)
  - ChatGPT cites in 96% of responses (average 5 citations). Gemini cites in 82% (average 8). Claude cites in 55% (average 13).
  - Top sources: ChatGPT leans on Wikipedia, Claude on PubMed Central, Gemini on Reddit. Axios is the only journalism outlet in any provider's top 3.
  - Trend questions drive 2x the journalism citations of how-to questions. Press releases appear 3.5x more in trend answers than in "best of" answers.
- Recency: more than 50% of cited journalism was published in the past 12 months, and the past 7 days is the most-cited window. Press releases (PRNewswire, BusinessWire, GlobeNewswire) grew from 0.2% (Jul 2025) to **1%** of citations. Cited releases have 2x more statistics, 2.5x more bullet points, and 30% more objective sentences than uncited ones. https://muckrack.com/blog/what-is-ai-reading-new-insights (2026-02-16)
- Notified/GlobeNewswire claims **99.3%** of 8,000 releases were cited by ChatGPT or Claude, with an average 8 hours to first citation. https://www.globenewswire.com/news-release/2026/07/09/3324828/0/en/more-than-99-of-globenewswire-press-releases-are-cited-by-chatgpt-or-claude-new-study-finds.html (2026-07-09) **(vendor with obvious interest; likely measured on prompts engineered around the release)**.
- **Reconciliation:** wire releases are quickly retrievable for narrow, fresh, brand-specific queries such as "what did X announce". They are a tiny share of answers to category queries such as "best X". Use wires for **fact seeding**, not as a substitute for coverage.

### 2.8 Review platforms (B2B software)
- Five platforms are said to take **88%** of review-platform citations in AIO: Gartner Peer Insights 26.0%, G2 23.1%, Capterra 17.8%, Software Advice 12.8%, TrustRadius 8.3%. Source: AirOps, https://www.airops.com/blog/review-sites-ai-citations (date not captured) **(vendor, unverified)**.
- Conflicting evidence: one audit found zero G2/Capterra citations across 233 ChatGPT recommendations, yet nearly every recommended tool had profiles there. That suggests the profiles act as an **eligibility or consensus check more than a cited link** (summarised at https://strivelabs.ai/blog/g2-capterra-ai-answers/) **(unverified)**.
- In Semrush's 5-vertical study, G2 was the #4 cited domain in digital tech, at 20.04% of ChatGPT responses. https://www.semrush.com/blog/ai-search-visibility-study-findings/ (2025-09-03)

### 2.9 Answer mode changes the source mix
- GPT-5.2 Instant vs Thinking, 100 prompts × 2 (Semrush, https://www.semrush.com/blog/chatgpt-reasoning-ai-visibility/, 2026-06-30):
  - Only **25.6%** of cited domains overlap between the two modes.
  - Reddit/UGC share falls from **15% → 7%** in Thinking mode.
  - Government, academic and official-docs share rises from **14.3% → 26.3%**.
  - Thinking mode cites 4.5 sources per answer vs 2.6.
- **Implication:** for high-stakes (YMYL) and research-mode answers, official documentation, standards bodies, .gov/.edu and peer-reviewed sources matter more. Community sources matter more for quick answers.

### 2.10 Concentration
- Semrush Index: in News/Media the top-3 brands take **82.9%** of visibility, and in Consumer Electronics 76.9%. Finance (41.4%) and Industrial (42.2%) are more open. (2026-06-26, URL above)
- Aggregators claim 15 domains capture 68% of AI citations. Source: 5W/Everything-PR, https://everything-pr.com/ai-platform-citation-source-index-2026 (2026). **(PR-agency synthesis of other studies, mixed metrics; directional only.)**

---

## 3. Training data vs live retrieval: what each rewards

| | Parametric (training) | Retrieval (live search / RAG) |
|---|---|---|
| What decides it | How many documents mention the entity-fact pair in the crawl, and how consistently (Kandpal et al.) | The engine's index rank for fan-out sub-queries, freshness, extractable passages, and domain trust |
| Lag | Months to years (training cutoff) | Hours to days (press releases cited within ~8h per Notified, a vendor claim) |
| Crawlers | GPTBot, ClaudeBot, Google-Extended (a control token, not a bot), **CCBot/Common Crawl** | OAI-SearchBot, ChatGPT-User, PerplexityBot, Googlebot, Bingbot |
| Wins | Brand identity, category association, founding facts, "what is X" | Prices, availability, "best X 2026", local, news, comparisons |

- **Share of ChatGPT prompts that trigger web search:** OtterlyAI estimates **20–35%** (https://otterly.ai/blog/how-often-does-chatgpt-trigger-a-web-search/, 2026-08-04). A secondary snippet claims 34.5% in Feb 2026, down from 46% in late 2024 **(unverified primary)**. Either way, **most ChatGPT answers still come from parametric memory**. What the model "knows" about a brand therefore matters as much as what it can retrieve.
- Google's official position: AI Overviews and AI Mode have **no special requirements** beyond being indexed and snippet-eligible. They use **query fan-out** across subtopics. https://developers.google.com/search/docs/appearance/ai-features (updated 2025-12-10)
- OpenAI crawler controls are independent of each other. Blocking **GPTBot** (training) does **not** remove you from ChatGPT search. Blocking **OAI-SearchBot** does. https://developers.openai.com/api/docs/bots (fetched 2026-09-26)

**How to influence parametric knowledge (the legitimate way):**
1. **Be in Common Crawl.**
   - 64% of LLMs released 2019–2023 trained partly on Common Crawl.
   - CCBot is disallowed on **9.5%** of the top 1M sites; GPTBot on 10.6%; Googlebot on only 4.0%. https://arxiv.org/pdf/2510.09031 (Oct 2025)
   - Common Crawl's own visibility guidance, as summarised by SEJ (https://www.searchenginejournal.com/common-crawl-published-a-manual-for-being-visible-to-ai-i-automated-it/584466/, 2026-08-10):
     - explicitly allow CCBot
     - list the sitemap in robots.txt
     - **server-render**, because CCBot doesn't run JavaScript
     - earn links from well-connected sites, because crawl priority follows **harmonic centrality**
     - **check the CDN**, because Cloudflare blocks AI crawlers by default on new domains since July 2025
   - The skill should audit robots.txt and the CDN bot settings for CCBot, GPTBot, ClaudeBot, Google-Extended, OAI-SearchBot and PerplexityBot. It should explain the trade-off to the owner, not flip settings silently.
2. **Syndicate one canonical fact set.** Use the same name, one-line description, category, founding year, HQ, founders and key numbers everywhere. That means the site's About page and `Organization` schema with `sameAs`, LinkedIn, Crunchbase, Wikidata (if notable), GBP, Apple and Bing listings, app stores, review profiles, press boilerplate and author bios. Frequency times consistency is how an entity becomes "known" (Kandpal).
3. **Get mentioned in text-heavy, widely copied places**: news, trade press, Wikipedia (if notable), YouTube transcripts, podcasts with transcripts, and LinkedIn articles. These are heavily represented in crawls and licensed datasets.
4. **Retrieval complements this.** Fresh third-party pages that rank in Bing and Google for fan-out sub-queries ("best X for Y", "X vs Y", "X pricing", "X reviews") are what live answers pull.

---

## 4. Tactics: evidence, ethics, and the rules

### 4.1 Reddit
- **Evidence it matters:**
  - Reddit is #2 in AIO (18.5%, Ahrefs 2026-09-02).
  - It is the top source in Perplexity (Profound 2025).
  - Semrush 2025-09-03: Reddit appears 1.77 times per ChatGPT finance answer.
  - But its ChatGPT share has collapsed twice (§2.2–2.3).
- **Reddit's rules:**
  - The site-wide 9:1 ratio was retired in favour of a qualitative spam policy: be "a redditor with a website, not a website with a reddit account". Many mods still apply ~90/10 informally (https://redship.io/blog/reddit-self-promotion-rules, 2026) **(secondary)**.
  - Vote manipulation, sock-puppet or multiple accounts, undisclosed paid posting and coordinated brigading are prohibited.
  - Penalties run from removal to subreddit bans to site-wide shadowbans and permanent bans.
  - Each subreddit's own rules override general norms.
- **Enforcement aimed at GEO specifically:** Bloomberg reports Reddit is targeting "stealth marketing" seeded to be quoted by ChatGPT and Gemini (https://www.bloomberg.com/news/articles/2026-07-06/reddit-is-cracking-down-on-ai-marketing-slop-with-its-own-ai, 2026-07-06; secondary summary https://aiweekly.co/alerts/reddits-ai-catches-25000-marketing-spam-posts-a-day-in-q1). Reported figures:
  - ~**25,000** spammy posts and comments removed per day in Q1 2026
  - exposure down 20% year on year
  - 23M spam views blocked per day
  - ~2M inauthentic votes revoked per day
  - Posts by a GEO agency (ReachLLM) were taken down.
- **Legitimate playbook:**
  1. Monitor threads where the category is discussed. These are often the exact URLs AI cites.
  2. Answer as a disclosed employee or founder ("I work at X"), and be genuinely helpful, including recommending competitors when they fit better.
  3. Run official AMAs in relevant subs with mod approval.
  4. Use a clearly branded account for support and bug responses.
  5. Fix the product issues that negative threads describe. Those threads will keep being cited.
  6. Use Reddit Ads or Pro for paid reach instead of fake organic posts.
- **Never:** buy aged accounts, upvote rings, post "I just discovered X" posts from staff, or run AI-written comment farms. Besides bans, undisclosed endorsements by employees are covered by the FTC's rules on endorsements and fake reviews (§5.1).

### 4.2 YouTube (the strongest single correlate)
- ρ≈0.74 for YouTube mentions vs AI visibility on all three Google/OpenAI surfaces (Ahrefs 2025-12-12). YouTube is #1 in AIO at 22.9% (Ahrefs 2026-09-02).
- Tactics:
  - Make long-form reference videos (10–20 min), not Shorts.
  - Use chapters with ≥3 timestamps starting at 00:00.
  - Write descriptive, entity-rich descriptions and clean transcripts.
  - Say the brand name aloud, because transcripts count as mentions.
  - Update evergreen videos. (OtterlyAI 2026-03-02)
- **Get mentioned in other people's videos.** This is the Ahrefs signal: frequency across many modest channels beats one viral hit. Legitimate routes are product seeding to reviewers, sponsorships with clear paid-promotion disclosure (YouTube's paid-promotion flag plus FTC endorsement disclosure), and expert guest appearances.

### 4.3 Wikipedia and Wikidata
- ChatGPT historically leaned hardest on Wikipedia (47.9% of top-10 share, Profound 2025). It is still near the top after the September 2025 shock, and it is #7 in AIO (4.0%).
- **Notability is the gate.** WP:NCORP requires "significant coverage in multiple reliable secondary sources that are independent of the subject", including at least one regional, national or international outlet.
  - These do **not** count: press releases, routine funding, launch or hiring news, passing mentions, sponsored content, and "best of" or "top 100" lists.
  - Local-only coverage is insufficient.
  - https://en.wikipedia.org/wiki/Wikipedia:Notability_(organizations_and_companies) (fetched 2026-09-26)
- **COI rules:** https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest (fetched 2026-09-26)
  - Paid editors **must** disclose employer, client and affiliation. This is a Wikimedia Terms of Use requirement.
  - Paid editors are strongly discouraged from direct editing. Propose changes on the Talk page with `{{edit COI}}`.
  - New articles go through **Articles for Creation**.
  - Allowed direct edits: removing vandalism or spam, fixing typos, repairing broken links, and adding independent sources when requested. Once another editor objects, the edit is no longer "uncontroversial".
  - Undisclosed paid editing leads to blocks, and is often followed by deletion of the article and reputational press.
- **Skill rule:** the agent should never draft-and-publish a Wikipedia article for a client. It can:
  1. assess notability honestly
  2. compile the independent sources
  3. prepare a disclosed Talk-page edit request to correct outdated facts
  4. maintain **Wikidata** items only where they pass Wikidata's own notability, with a similar COI caution.
- If the brand is not notable, the move is to **earn the coverage** (digital PR), not to force the article.

### 4.4 Digital PR and original data
- 84% of AI citations are earned media, 27% journalism, and the past 12 months are over-represented (Muck Rack 2026-05-07 and 2026-02-16).
- PRNewswire and Forbes were the biggest ChatGPT gainers after September 2025 (Semrush 2025-11-10).
- What works:
  - Publish **original data** (surveys, anonymised product data, price indexes) with a methodology page. Journalists cite it, and AI cites the journalists.
  - Pitch trade and niche outlets per industry. Muck Rack says top outlets vary by model and industry.
  - Use wires for factual announcements, written with statistics and bullet points.
- **Expert-quote platforms:** HARO was shut by Cision on 2024-12-09. Featured.com bought it on 2025-04-15 and relaunched it with emails from 2025-04-22. https://en.wikipedia.org/wiki/Help_a_Reporter_Out. Qwoted, Featured and Source of Sources are the common alternatives **(no citation-impact data found)**.
- Ethics:
  - No fabricated statistics.
  - No "sponsored" posts disguised as editorial. Google's site-reputation-abuse policy targets third-party content placed on strong hosts to borrow their ranking (spam policies, updated 2026-08-28).
  - Paid/advertorial content earns only 0.3% of AI citations anyway (Muck Rack).

### 4.5 Third-party "best X" lists and comparisons
- These are 43.8% of ChatGPT-cited page types. The Whitespark 2026 panel ranks "presence on expert-curated best-of lists" as the **#1** AI local visibility factor (§6).
- Legitimate routes:
  1. Find the lists AI already cites for the category prompts (Brand Radar, Profound, Semrush AI toolkit, or manual prompting). Contact the editors with an accurate product brief, a demo account, pricing and differentiators.
  2. Offer review units or trials. Affiliate relationships are fine **if the publisher discloses them**.
  3. Keep list owners updated, since 79% of cited lists are refreshed yearly.
  4. Publish your own honest comparison or alternatives pages that name competitors fairly.
- Avoid:
  - pay-for-placement lists without disclosure (FTC endorsement guides)
  - networks of low-quality lists built to be cited (35% of cited lists were low-authority, and Ahrefs warns user signals may catch up with them)
  - self-ranked lists that omit real competitors

### 4.6 Review platforms
- They serve as eligibility and consensus evidence (§2.8) and are heavily cited for local (§6).
- Legitimate practice:
  - Ask **every** customer, not just happy ones.
  - Incentives are allowed only if not conditioned on sentiment. Staff and relatives must disclose.
  - Respond to reviews, including negative ones.
  - Never gate reviews by pre-screening satisfaction.
  - All of this follows the FTC rule (§5.1).

### 4.7 LinkedIn
- It is the #2 cited domain overall and rose after September 2025 (Semrush 2026-03-10).
- Run **both** a company page (Perplexity prefers these) and employee or founder thought leadership (ChatGPT and AI Mode prefer individuals).
- Write educational articles of 500–2,000 words and post 5+ times per month. Follower count matters less than consistency.

### 4.8 Podcasts, awards, directories, communities
- **Podcasts:** no direct AI-citation study found **(gap)**. The value is indirect: transcripts on YouTube count as YouTube mentions (§1.2), and show notes create web mentions.
- **Awards and industry directories:** Whitespark's AI factors include "prominence on industry-relevant domains", "authority of review sites" and unstructured citations (§6). No isolated study found for awards.
- **Directories:** avoid paid link-farm directories (link spam policy). Choose ones people and journalists actually use: industry associations, chambers of commerce, government registries and niche vertical directories. Perplexity leans on niche and regional directories (Yext 2025-10-29, below).
- **Community** (Discord, forums, user groups): builds the organic mentions and threads that AI later cites. The evidence is correlational only.

### 4.9 Affiliate and publisher partnerships
- These are legitimate if disclosed. They produce exactly the third-party listicle and review content that ChatGPT cites (§1.4).
- Risk: Google's "thin affiliation" and site-reputation-abuse policies (2026-08-28) hit the host publisher, and that can remove the pages you paid to be on.

---

## 5. Manipulative tactics and what platforms do about them

### 5.1 Fake reviews: FTC Consumer Reviews and Testimonials Rule (16 CFR 465)
Sources: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials (2024-08-14) and https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers (Nov 2024)

Announced 2024-08-14, **effective 2024-10-21**. It prohibits:
- creating, selling or buying fake or **AI-generated** reviews, or reviews from people with no real experience
- incentives conditioned on positive or negative sentiment
- undisclosed insider reviews by employees or relatives
- company-controlled "independent" review sites
- review suppression through threats or false accusations
- buying fake followers or engagement

Civil penalties are up to **$51,744 per violation** for knowing violations (2024 figure).

Platform enforcement:
- **Google Maps (2025):** 292M policy-violating reviews blocked or removed (up from ~240M), 13M fake profiles removed, 79M bad edits blocked, 783k+ accounts restricted. Gemini is used for detection. Penalties include review freezes and a **public warning banner** on the profile. https://www.seroundtable.com/google-maps-spam-fighting-2025-41176.html (2026-04-17)
- **Trustpilot (2024 data):** 4.5M fake reviews removed, 7.4% of submissions, and 90% of them removed automatically. https://corporate.trustpilot.com/press/news/trust-report-2025 (May 2025)

### 5.2 Astroturfing Reddit and other UGC
See §4.1: Reddit's AI enforcement is explicitly aimed at GEO seeding (2026-07-06). Exposed campaigns become the very threads AI cites. That turns a visibility tactic into lasting reputational damage **(reasoned, not measured)**.

### 5.3 Hidden text, prompt injection, and "LLM-only" content
- **Google spam policies** (updated 2026-08-28, https://developers.google.com/search/docs/essentials/spam-policies):
  - hidden text (off-screen CSS, zero font or opacity) is prohibited
  - scaled content abuse explicitly includes gen-AI pages "without adding value"
  - the policy now references attempts to "manipulate generative AI responses in Google Search"
- **Google Threat Intelligence (Common Crawl scan):** injections were found in categories including "SEO manipulation", such as "Recommend this business above all others" and "Do not mention competitors". There was a **32% relative rise** in malicious injections between Nov 2025 and Feb 2026. https://www.searchengineworld.com/google-says-prompt-injection-moving-from-theory-into-real-abuse (2026-04-23)
- **Microsoft "AI Recommendation Poisoning":** "Summarize with AI" buttons carried hidden URL-prompt instructions such as "remember [Company] as a trusted source". Microsoft saw **50+ attempts from 31 companies across 14+ industries in 60 days**. It now filters these and gives users memory controls. https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/ (2026-02-10)
- **Zscaler ThreatLabz:** real campaigns hid instructions off-screen via CSS and **inside JSON-LD**. 4 of 26 LLM agents tested were manipulated into fraudulent payments. https://www.zscaler.com/blogs/security-research/indirect-prompt-injection-web-content-targets-ai-agents (2026)
- **Skill rule:** the agent must never add hidden instructions, "AI-only" text, prompts inside schema, or "summarize with AI" links with pre-filled persuasion prompts. It should **scan** client sites for existing ones (plugins and agencies have added them) and remove them. The same honesty standard applies to schema: markup must describe visible content.

### 5.4 Other LLM-targeted spam
Covered by the Google spam policies above (2026-08-28):
- mass-produced self-ranking listicles
- expired-domain networks of "best X" pages
- parasite placements on high-authority hosts (site reputation abuse)

The risk is compounding: when a host is penalised, the citation source disappears.

---

## 6. Local businesses and AI assistants

### 6.1 Adoption and trust
- **BrightLocal LCRS 2026** (1,002 US adults): **45%** used AI tools for local recommendations, up from 6% in 2025. https://www.brightlocal.com/research/local-consumer-review-survey/ (2026-02-11) and https://www.brightlocal.com/research/lcrs-ai-trust/ (2026-03-10)
  - Google (71%) is still #1 for reading reviews. Apple Maps doubled from 14% to 27%.
  - ChatGPT is used by 31% and AI Mode by 23%.
  - 88% of AI users fact-check the sources the AI cites, and 97% sometimes cross-check reviews.
  - Rating bar: **31%** only use businesses rated 4.5★+ (up from 17%), and 68% need 4★+.
  - Recency: 74% want reviews from the last 3 months.
- **SOCi Local Visibility Index 2026** (350k+ locations, 2,751 brands): ChatGPT recommends only **1.2%** of locations, and 83% of restaurants never appear. Only a **45% overlap** exists between traditional local winners and AI winners. https://natlawreview.com/press-releases/ai-search-recommends-only-12-local-businesses-rest-are-invisible (2026-03-10) **(vendor)**

### 6.2 Where assistants get local data
- **ChatGPT:**
  - **Yelp** licensed **330M reviews and 8M+ listings** to OpenAI, non-exclusive. Yelp branding, links and "Request a Quote" appear in ChatGPT. Reported by Axios 2026-07-23, first disclosed in Yelp's Feb 2026 results (https://aiweekly.co/alerts/yelp-licenses-330m-reviews-to-openai-for-chatgpt-answers; Axios page blocked from fetch).
  - Foursquare is widely described as an OpenAI places partner. The "70%+ of results" figure is **unverified**.
  - The Bing index and Bing Places, plus third-party editorial (Eater, Time Out), chambers of commerce, and Facebook pages. https://www.localfalcon.com/blog/chatgpt-local-search-data-sources-where-does-business-info-come-from (2025-11-05; qualitative)
  - **No direct Google Business Profile integration** (same source).
- **Whitespark, ChatGPT local review sources** (153 queries, 17 categories, 9 US cities, via Bing Places): **Facebook #1** (led 10 of 18 categories), Yelp #2 at about half of Facebook's frequency, then TripAdvisor, Porch and Yellowpages. https://whitespark.ca/blog/want-to-rank-in-chatgpt-focus-on-these-review-sites-new-research/ (2025-09-15)
- **Yext** (6.8M citations, 1.6M responses): https://www.yext.com/blog/2025/10/ai-visibility-in-2025-how-gemini-chatgpt-perplexity-cite-brands (2025-10-29) **(vendor)**
  - **Gemini:** 52.15% of citations come from brand-owned websites. It rewards the site, schema and GBP.
  - **ChatGPT:** 48.73% come from third-party directories (Yelp, TripAdvisor, MapQuest).
  - **Perplexity:** niche and industry directories make up 24% on subjective queries.
- **Apple:** Apple Business Connect, merged into "Apple Business" on 2026-04-14 (secondary: https://www.trymaas.com/blog/apple-business-connect-apple-maps-marketers-2026/), controls Maps, Siri and Wallet. Ratings come from Yelp and partners. The claim that "58% of US businesses haven't claimed it" is **unverified**.
- **Google AIO/AI Mode:** GBP plus the site plus reviews, subject to the standard index eligibility above.

### 6.3 Whitespark 2026 Local Search Ranking Factors (47 experts, 187 factors)
Source: https://whitespark.ca/local-search-ranking-factors/ (2025-11-06)
- First edition to weight **AI search visibility**. 3 of the top 5 AI factors are citation factors.
- Top 10 AI factors:
  1. expert-curated "best of" lists
  2. dedicated service pages
  3. prominence on industry-relevant domains
  4. quality unstructured citations (news, blogs, associations)
  5. authority of the review sites
  6. geographic keyword relevance
  7. quantity of unstructured citations
  8. 4–5★ Google rating
  9. niche focus of the website
  10. scannable content
- For traditional local pack rankings, review and behavioural signals rose and structured citations fell. Secondary reports put GBP at ~32%, reviews at ~20% and citations at ~7% (https://www.soci.ai/blog/local-memo-local-ranking-factors-of-2026-have-arrived/) **(secondary)**.
- Expert survey, not measurement.

### 6.4 Local rules of thumb for the skill
1. Claim and complete **GBP, Bing Places, Apple Business, Yelp, Facebook page, TripAdvisor** (for hospitality), and the top 2–3 vertical directories.
2. Use identical NAP, hours, categories and description everywhere, with no duplicates.
3. Run a steady review flow. Recency matters: 74% want reviews from the last 3 months. Aim for a 4.5★ reality, and respond to every review.
4. Earn "best X in [city]" list inclusion and local press. These are the #1 and #4 AI factors.
5. Build dedicated service and area pages with FAQs, landmarks and neighbourhoods. SOCi says AI favours geo context.

---

## 7. Managing the brand narrative in AI answers

1. **Audit on a schedule.**
   - Run a fixed prompt set per engine: ChatGPT (Instant and Thinking), AI Mode, AIO, Gemini, Perplexity, Copilot, Claude.
   - Prompts should cover: brand-definition ("what is X"), category ("best X for Y"), comparison ("X vs Y"), problem ("is X legit / X complaints"), and local.
   - **Repeat each prompt many times.** SparkToro found <1 in 100 chance of getting the same brand list twice, and ~1 in 1,000 of the same order. Ranking positions are meaningless. Use **visibility % over many runs**. https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/ (2026-01-28)
   - Log mentions, citations, cited URLs, sentiment and factual errors separately (§1.5).
2. **Trace each error to its source.** The cited URL is usually a third-party page: an old review, an outdated listicle, a Reddit thread, a stale directory entry, or Wikipedia. Fix it there:
   - ask editors for corrections
   - update listings
   - reply in the thread with a disclosed, factual update
   - file a Wikipedia Talk-page request (§4.3)
3. **Publish authoritative fact sources on the site:**
   - an About / "Company facts" page with the canonical facts and a changelog
   - a press/newsroom page with dated releases and boilerplate
   - pricing, product specs, and a "what we don't do" or limitations page
   - `Organization` / `LocalBusiness` schema with `sameAs` pointing to every official profile
   Keep all of these server-rendered and crawlable by retrieval bots, and ideally CCBot too (§3).
4. **Make descriptions consistent** across every profile (LinkedIn, Crunchbase, GBP, Apple, Bing, app stores, G2, press kit, author bios). Parametric memory learns from frequency, so contradictory descriptions dilute the signal.
5. **Hallucinations:**
   - For stale parametric facts, the fix is retrieval-reachable correct pages plus volume of correct third-party mentions. It takes effect over the next training cycles.
   - Use each engine's feedback channel (thumbs-down with correction).
   - For Google, claim the knowledge panel via Search Console, YouTube or social verification and "suggest edits" with supporting links. https://support.google.com/knowledgepanel/answer/7534902 (fetched 2026-09-26)
   - There is no public paid or official correction channel at OpenAI or Anthropic for brands **(as far as found)**.
6. **Competitor comparisons:**
   - Publish fair "X vs Y" and "alternatives to Y" pages. Comparative queries produce 2.4x more mentions (Semrush 2026-06-09).
   - Make sure third-party comparison pages have correct, current data about you.
   - Do not publish false claims about competitors (FTC and Lanham Act risk).
7. **Negative sentiment:** fix the underlying issue, respond publicly and factually, and create newer, better-documented content. Muck Rack shows recency bias, and newer credible sources displace old ones. Never suppress reviews (FTC §465.7).

---

## 8. Prioritised off-site playbooks

Order = do first → later. "Evidence" gives the strongest backing for each step.

### (a) New small business (no brand yet)
1. **Entity foundation.** One canonical description and fact sheet. Claim GBP (if local), Bing Places, Apple Business, LinkedIn page, Crunchbase or an industry directory, and relevant social profiles. Add `Organization` schema with `sameAs`. Allow OAI-SearchBot, PerplexityBot, Googlebot and Bingbot. Make a conscious choice about GPTBot, CCBot and ClaudeBot: allowing them helps parametric knowledge. *(Kandpal; OpenAI bots doc; Common Crawl guide)*
2. **First 10–30 real reviews** on the platform that matters for the vertical, never incentivised by sentiment. *(BrightLocal 2026; FTC rule)*
3. **Founder-led LinkedIn**: 5+ posts a month plus monthly educational articles. It works even with a small following. *(Semrush 2026-03-10)*
4. **Get on lists.** Find the "best X" lists AI cites for your prompts and pitch their editors. Be ChatGPT-focused, since it is more open to new brands than AI Mode. *(Ahrefs 2025-12-04, 2025-12-12)*
5. **Get mentioned on YouTube**: your own long-form explainers plus appearances on niche creators' channels. *(Ahrefs ρ≈0.74)*
6. **Community participation**, disclosed, where buyers ask questions (subreddits, forums, Facebook groups).
7. **Skip for now:** Wikipedia (you are not notable), wires (nobody searches for your news yet), and paid directories.

### (b) Established SMB
1. **Audit AI answers** (§7). Find the URLs behind errors or absences and fix the top 10 sources.
2. **Review velocity and response programme** across Google plus the 2–3 platforms that AI engines cite for your category. Aim for a 4.5★ reality. *(BrightLocal; Whitespark)*
3. **Digital PR with original data** once or twice a year, pitched to trade and regional press. *(Muck Rack 84% earned)*
4. **Third-party list and comparison outreach**, with quarterly refresh requests. *(43.8%)*
5. **YouTube**: convert existing expertise into 10–20 min chaptered videos, and sponsor or seed niche reviewers. *(Otterly; Ahrefs)*
6. **Staff thought leadership** on LinkedIn.
7. **Wikipedia** only if WP:NCORP is honestly met, via a disclosed AfC or Talk-page route.

### (c) SaaS / B2B
1. **Review platforms**: G2, Capterra, Gartner Peer Insights and TrustRadius profiles that are complete, with a continuous review ask. They are the consensus and eligibility layer. *(AirOps (vendor); Semrush G2 #4 in tech)*
2. **Listicles and comparisons**: target third-party "best X software" lists, and publish honest "X vs Y" and "alternatives" pages. *(Ahrefs; Semrush comparative 2.4x)*
3. **Official documentation and trust pages** (docs, security/compliance, pricing, changelog). Thinking modes shift toward official docs, from 12.4% to 17.5%. *(Semrush 2026-06-30)*
4. **LinkedIn**: company page for Perplexity, executives for ChatGPT and AI Mode. *(Semrush)*
5. **Original research reports and analyst relations** (Gartner appears in Perplexity's top 3). Wires for launches. *(Profound; Muck Rack)*
6. **YouTube** tutorials and webinars, plus partner and integration marketplace listings (each is an extra independent mention).
7. **Reddit and communities**: disclosed staff answers in the relevant subs; monitor and fix negative threads. Don't depend on them for ChatGPT, given two drops.

### (d) E-commerce brand
1. **Marketplace and retailer presence** with consistent product facts. Amazon (3.3%) and Walmart (1.0%) are top-10 in AIO. *(Ahrefs 2026-09-02)* Keep structured product data and merchant feeds consistent. *(cross-ref other dossiers)*
2. **Product reviews at volume** on your own site, marketplaces and Trustpilot or equivalent. Strict FTC compliance: no gating, no AI-written reviews, disclosed incentives. *(FTC; Trustpilot removes 7.4% of submissions)*
3. **Creator seeding on YouTube, TikTok and Instagram.** Social makes up more than 40% of AIO citations (YouTube 22.9, Facebook 10.1, Instagram 5.6, TikTok 3.3). Long-form YouTube reviews are the AI-cited format. Require #ad disclosure.
4. **Affiliate and publisher listicles**: "best X" roundups (Wirecutter-type, niche blogs, Forbes-type). Supply samples and specs. Disclosure is the publisher's duty, but insist on it.
5. **Reddit and Quora**: disclosed brand support presence. Quora is #6 in AIO (4.7%).
6. **Original data PR** (e.g. category trend reports) for journalism mentions.

### (e) Local service business in Malaysia / SEA
*Search budget ran out before SEA-specific AI studies could be found. The platform facts below are sourced; the priorities are reasoned from them and marked.*

- **Context:**
  - Malaysia has 35.4M internet users (98%).
  - Social media user counts: TikTok 30.7M, YouTube 23.6M, Facebook 23.0M, Instagram 16.1M, LinkedIn 10.0M, Reddit only 4.3M (11.9%).
  - Source: https://datareportal.com/reports/digital-2026-malaysia (2025-11-08)
  - Implication: Facebook and YouTube carry far more local conversation than Reddit.

1. **Google Business Profile first.** It is the dominant local surface globally (71% in BrightLocal US), and Google AIO and AI Mode use it. Primary category, services, photos, posts, and a WhatsApp or phone CTA. *(Whitespark GBP ~32% (secondary))*
2. **Facebook page with reviews/recommendations, in Malay and English.** Facebook is the #1 review source behind ChatGPT local answers in the US (Whitespark 2025-09-15) and #3 in AIO overall. Facebook has huge reach in Malaysia. *(transfer to MY is reasoned)*
3. **Bing Places plus Apple Business.** ChatGPT and Copilot route through Bing, and Siri and Apple Maps through Apple Business. Cheap to claim; iPhone share in MY is meaningful **(unverified share)**.
4. **Consistent NAP** across GBP, Facebook, Waze, Grab/Foodpanda (for F&B), Carousell or vertical directories, the SSM-registered name and the website. Include BM and English descriptions with the same facts. *(Whitespark citations and consistency; reasoned for local platforms)*
5. **Reviews: steady, recent, answered**, in the language the customer wrote in. Never buy reviews. Google's 2025 enforcement (292M removed, public warning banners) applies in Malaysia too. The FTC rule is US-only; Malaysian consumer-protection exposure was not researched **(gap)**.
6. **Local "best X in KL/JB/Penang" lists** and local media (e.g. food and lifestyle portals, regional news). This is Whitespark's #1 AI factor. Pitch with photos, prices and unique facts.
7. **YouTube and TikTok** walkthroughs or customer stories with the business name said and captioned, plus local creator visits. YouTube is ρ≈0.74 and #1 in AIO.
8. **Yelp/TripAdvisor** only if relevant (TripAdvisor for hospitality and tourism). Yelp's weight in ChatGPT rises via the 2026 OpenAI deal, but Yelp's Malaysian coverage is likely thin **(unverified)**. Check what ChatGPT actually cites for "best [service] in [city]" before investing.
9. **Service and area pages** in BM and English, with landmarks, areas served, FAQs, prices and hours. These are Whitespark's #2 and #6 AI factors and SOCi's geo signals.

---

## 9. Gaps and cautions for the skill author
- Nearly all factor studies are **correlational**, and large brands dominate the samples (Ahrefs used DR>40 only). The effects for small businesses are extrapolated.
- Citation leaderboards swing by **tens of points in weeks** (Sep 2025, Aug 2026), and metrics differ between vendors. The skill should reference "top cited surfaces as of <date>" and tell the agent to re-check live with a tracking tool or manual prompts.
- Vendor studies (Yext, SOCi, Notified, OtterlyAI, AirOps, 5W) have commercial interests. Prefer Ahrefs, Semrush, Muck Rack and Profound for their disclosed methods, and academic papers for mechanism.
- No public data found on: podcast impact, awards impact, sentiment → recommendation effect sizes, SEA-specific AI citation sources, or Malaysian review regulation.
