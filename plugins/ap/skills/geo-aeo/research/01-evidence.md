# 01 — The Evidence Base: What Actually Changes Whether Content Is Cited by Generative Engines

Compiled 2026-09-26. Every figure carries its source URL and publication date. "Unverified" means the figure was seen only in secondary coverage or the primary page was inaccessible. "(via survey)" means the figure comes from the July 2026 critical survey (arXiv 2607.14035), not from the original paper, which I did not open.

Reading guide. There are two kinds of evidence, and they answer different questions:
- **Controlled / causal** studies (academic): the researcher changes one thing in a document and measures citation. These give clean effects, but in artificial settings: fixed 2–10 document contexts, LLM judges, no real retrieval.
- **Observational / correlational** studies (industry: Ahrefs, Semrush, SE Ranking, AirOps, BrightEdge, Seer, Profound): large samples of real engines, but confounded. Big brands have everything at once. Vendors also sell tools that benefit from the conclusion.

A claim is **strong** only when both kinds agree, or when replicated controlled evidence is backed by an official platform statement.

---

## 1. Key conclusions ranked by evidence strength

### Strong

1. **[strong] You can't be cited if you aren't retrieved, and retrieval runs on classic search signals.** Relevance to the query, and where the document lands in the retrieved set, are the main causes of citation.
   - C-SEO Bench: moving a document to the top of the LLM context gained 1.60–2.77 ranks. That beat every one of 10 content-rewriting methods ([arXiv 2506.11097](https://arxiv.org/html/2506.11097), 2025-06/2025-10).
   - A 252,000-trial factorial study ranked topic mismatch and lower list position among four "gatekeeper" factors (OR ≫ 10,000 in all 6 LLMs) ([arXiv 2605.25517](https://arxiv.org/html/2605.25517), SIGIR 2026).
   - AirOps: citation rate is 58% at ChatGPT retrieval position 1 vs 14% at position 10 ([AirOps](https://www.airops.com/report/the-fan-out-effect-what-happens-between-a-query-and-a-citation), 2026-04-13).
   - Wan et al.: LLMs "rely heavily on the relevance of a website to the query" and largely ignore credibility cues ([arXiv 2402.11782](https://arxiv.org/abs/2402.11782), ACL 2024).
   - Sharma: in 112 startups, traditional SEO signals (referring domains r=+0.319, community presence r=+0.395) predicted LLM discovery; GEO optimization showed no correlation ([arXiv 2601.00912](https://arxiv.org/abs/2601.00912), 2026-01-01).

2. **[strong] Google says AI Overviews and AI Mode need no special optimization.** Eligibility = indexed and snippet-eligible. No llms.txt, no special schema, no chunking, no special writing style, no ideal length ([Google AI features doc](https://developers.google.com/search/docs/appearance/ai-features), updated 2025-12-10; [Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), updated 2026-07-10).

3. **[strong] Keyword stuffing does not work in generative engines.**
   - GEO paper: position-adjusted word count fell from 19.3 to 17.7 (−8%) on GEO-bench; on Perplexity it fell from 24.1 to 21.9 ([arXiv 2311.09735](https://arxiv.org/abs/2311.09735), KDD 2024).
   - Google: "You don't need to write in a specific way just for generative AI search" (guide, 2026-07-10).

4. **[strong] Real clicks fall when an AI summary appears. Being cited softens the fall but does not undo it.**
   - Pew: 8% vs 15% of visits clicked a result, and 1% clicked a link inside the summary ([Pew](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/), 2025-07-22).
   - Ahrefs: position-1 CTR −34.5% ([Ahrefs](https://ahrefs.com/blog/ai-overviews-reduce-clicks/), 2025-04-17), rising to −58% in an update using Dec 2025 data (secondary coverage, [Medianama](https://www.medianama.com/2026/02/223-google-ai-overviews-click-through-rates-58-study/), 2026-02).
   - Seer: cited brands get 120% more organic clicks per impression than uncited ones, but still 38% fewer than on non-AIO queries ([Seer](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update), 2026-04).

5. **[strong] AI engines are stochastic, so one-off checks mean nothing.**
   - Visibility is "a distribution rather than a single-point outcome" ([Schulte et al., arXiv 2604.07585](https://arxiv.org/abs/2604.07585), 2026-04-08).
   - Engine overlap over 45 days had Jaccard 0.34–0.42. 7–8 repetitions per prompt are recommended. 57.8% of ChatGPT repetitions did not trigger web search (via survey, [arXiv 2607.14035](https://arxiv.org/html/2607.14035v1), 2026-07-15).
   - CITECHOICE: 15% of binary citation decisions flipped on fresh decoding ([arXiv 2609.15164](https://arxiv.org/abs/2609.15164), 2026-09-14).

6. **[strong] Each engine cites a different source ecosystem, with low overlap.**
   - Only 12% of URLs cited by ChatGPT, Gemini, Copilot and Perplexity rank in Google's top 10. Perplexity is highest at 28.6%; ChatGPT and Gemini are about 8% ([Ahrefs](https://ahrefs.com/blog/ai-search-overlap/), 2025-08-11).
   - Google Search, AI Overviews and Gemini have "substantially different" sources ([Grossman et al., arXiv 2604.27790](https://arxiv.org/abs/2604.27790), SIGIR 2026).
   - AI engines lean heavily toward earned media ([Chen et al., arXiv 2509.08919](https://arxiv.org/html/2509.08919v1), 2025-09).

### Moderate

7. **[moderate] Genuine, verifiable, extractable evidence raises citation and "absorption":** statistics, quotations, named sources, definitions, comparisons and procedural steps.
   - GEO paper: Quotation Addition +41%, Statistics Addition +31%, Cite Sources +27% relative (GPT-3.5, 5-source context).
   - "Claims With Evidence" was significant in 4+ of 6 models (OR 2.09 to ≫10,000) (Vishwakarma 2026).
   - High-absorption pages carry "definitions, numerical facts, comparisons, procedural steps" ([Zhang et al., arXiv 2604.25707](https://arxiv.org/abs/2604.25707), 2026-04-28).
   - **Caveat:** in C-SEO Bench, LLM-inserted statistics lowered ranking in 19 of 24 settings. Fabricated or padded statistics do not work. Real evidence does.

8. **[moderate] Real freshness matters, especially for time-sensitive and commercial queries.**
   - "Recent vs Old Timestamp" was a gatekeeper factor (OR ≫ 10,000 in all 6 models) (Vishwakarma 2026).
   - LLM rerankers push dated-fresh passages up by as many as 95 ranks, and date injection reversed up to 25% of pairwise preferences ([Fang et al., arXiv 2509.11353](https://arxiv.org/abs/2509.11353), SIGIR-AP 2025).
   - AI-cited URLs are 25.7% fresher than Google organic results ([Ahrefs](https://ahrefs.com/blog/fresh-content), 2025-12-22).
   - "No timestamp vs old timestamp" was *not* consistent (Vishwakarma). A date helps only when it is recent and true.

9. **[moderate] Early-in-document, query-matching answers get cited more.**
   - 44.2% of ChatGPT citations come from the first 30% of a page (Kevin Indig, 1.2M responses / 18,012 verified citations; secondary via [Search Engine Land](https://searchengineland.com/chatgpt-citations-content-study-469483), 2026, exact date unverified).
   - Headings that closely match the query are cited 41% of the time vs 29% for weak matches (AirOps 2026-04-13).
   - This is consistent with the "lost in the middle" U-shape ([Liu et al., arXiv 2307.03172](https://arxiv.org/abs/2307.03172), TACL).

10. **[moderate] Off-site brand presence (earned media, mentions, reviews, community, YouTube) predicts AI visibility more than backlinks.** This evidence is correlational.
    - Spearman 0.664 for branded web mentions vs 0.218 for backlinks across 75k brands ([Ahrefs](https://ahrefs.com/blog/ai-overview-brand-correlation/), 2025-05-26).
    - AI engines cite earned media at 69–92% vs Google's 32–54% (Chen et al. 2025).
    - Google warns that *inauthentic* mentions don't help (guide, 2026-07-10).

11. **[moderate] Metadata and structural fields (title, headings, meta description, structured fields) matter at the retrieval stage. Rewriting body text alone can hurt.**
    - SAGEO Arena: body-only GEO rewriting cut top-20 retrieval 9%, top-10 reranking 16% and citation 6%. Structural-field optimization raised retrieval hit rate 22% ([arXiv 2602.12187](https://arxiv.org/html/2602.12187), 2026-02, rev. 2026-08). Figures come from a model summary of the HTML; treat exact values as needing a check against the paper tables.

12. **[moderate] Formatting alone (bullets, restructuring) has weak or no effect on what the LLM chooses once the page is in context.**
    - "Content Structure" OR 0.79–1.68, not significant (Vishwakarma 2026).
    - Structured rendering *redistributes* citation (+0.50 target citations per answer) but does not expand it (CITECHOICE 2026).

### Weak

13. **[weak] "Authoritative / persuasive tone" helps.** GEO paper: +10% on the word-count metric (21.3 vs 19.3); the authors called it "no significant improvement". Vishwakarma: hedged language hurts (OR 2.67–754), but "Overly Promotional" was inconsistent.
14. **[weak] Fluency / readability rewrites help.** GEO: +28% relative. C-SEO Bench: Fluency and Simple Language were not significant with modern models. Indig/AirOps: Flesch-Kincaid ~16 correlates with citation (observational).
15. **[weak] JSON-LD / schema lifts AI citation.** AirOps reports a +6.5 pp association (observational). SE Ranking found FAQ schema negligible. Google says no special schema is needed. CITECHOICE found structured rendering redistributes credit.
16. **[weak] Citation leads to traffic or conversions.** The only quasi-experiment has an interrupted-time-series multiplier of 1.82 but placebo p=0.16 (Watanabe & Nakayashiki 2026, via survey). Semrush's "AI visitor worth 4.4×" is a vendor conversion-rate estimate ([Semrush](https://www.semrush.com/blog/ai-search-seo-traffic-study/), 2025, date unverified).

### Myth / rejected

17. **[myth] "GEO boosts visibility by 40%" as a general rule.** The 40% is a relative gain on one metric (position-adjusted word count) for a source already inside a fixed 5-document context, with GPT-3.5 as engine. For already top-ranked sources, the same methods *reduced* visibility by 20–30% (GEO Table 2). C-SEO Bench: only 3 of 54 method-domain combinations were significantly positive, and none in question answering.
18. **[myth] llms.txt as a citation or ranking lever.**
    - No relationship across 300k domains; removing the variable improved the model ([SE Ranking](https://seranking.com/blog/llms-txt/), 2025-11-07).
    - Mueller: AI services don't even fetch it and it is "comparable to the keywords meta tag" (2025-04-17, [SEJ](https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/)).
    - Google guide (2026-07-10): no "AI text files … or Markdown" needed.
19. **[myth] Chunking content into bite-sized pieces for LLMs.** Sullivan: "We don't want you to do that" (Search Off the Record, [SERoundtable](https://www.seroundtable.com/google-content-bite-sized-chunks-40728.html), 2026-01-09). Google guide: "There's no requirement to break your content into tiny pieces." Clear sections still help humans and retrieval; the myth is *fragmenting* pages for machines.
20. **[myth] Fixed word-count or "optimal passage length" targets.** Google: "There's no ideal page length." Industry length findings conflict (see §3).
21. **[myth] FAQ schema gives an AI citation lift.** No causal evidence. SE Ranking found it negligible. E-GEO's "FAQ" rewriting heuristic (content, not schema) gained only +0.05.

---

## 2. Per-study notes

### 2.1 Academic: foundational

**Aggarwal et al., "GEO: Generative Engine Optimization"** — Princeton / IIT Delhi / Allen AI. [arXiv 2311.09735](https://arxiv.org/abs/2311.09735). v1 2023-11-16, v3 2024-06-28. KDD 2024 (Barcelona). Figures below were read from the v3 PDF.
- **Setup:**
  - GEO-bench has 10K queries (8K/1K/1K split) from 9 datasets, including MS MARCO, ORCAS, Natural Questions, ELI5, LIMA and Perplexity Discover, tagged by domain and intent.
  - Engine: 2-step. Top-5 Google results are the sources; GPT-3.5-turbo writes the answer.
  - One source is rewritten by a GEO method and its visibility is measured.
- **Metrics:**
  - Position-Adjusted Word Count (PAWC): words attributed to the source, decayed by citation position.
  - Subjective Impression: an LLM-judged composite of relevance, influence, uniqueness and similar.
- **Table 1 results (PAWC overall; baseline 19.3).** Relative change is my arithmetic from the table values.

  | Method | PAWC overall | Relative change | Subjective Impression avg (baseline 19.3) |
  |---|---|---|---|
  | Keyword Stuffing | 17.7 | −8.3% | 20.2 |
  | Unique Words | 20.5 | | |
  | Easy-to-Understand | 22.0 | | |
  | Authoritative | 21.3 | | 22.9 |
  | Technical Terms | 22.7 | | |
  | Fluency Optimization | 24.7 | +28% | |
  | Cite Sources | 24.6 | +27% | |
  | Statistics Addition | 25.2 | +31% | 23.7 |
  | Quotation Addition | 27.2 | +41% | 24.7 |

- **Perplexity.ai (Table 5, source text uploaded as files):**
  - PAWC: baseline 24.1, Keyword Stuffing 21.9, Quotation 29.1, Statistics 26.2.
  - Subjective Impression: baseline 24.7, Quotation 32.1, Statistics 33.9.
- **Rank-dependence (Table 2), relative visibility change by original rank:**

  | Method | Rank-1 | Rank-5 |
  |---|---|---|
  | Cite Sources | −30.3% | +115.1% |
  | Quotation Addition | −22.9% | +99.7% |
  | Statistics Addition | −20.6% | +97.9% |
  | Authoritative | −6.0% | +6.1% |

  GEO helps low-ranked sources and **hurts the top-ranked one** in a zero-sum context.
- **Domain fit (Table 3, top categories per method):**
  - Authoritative: Debate, History, Science.
  - Fluency: Business, Science, Health.
  - Cite Sources: Statement, Facts, Law & Government.
  - Quotation: People & Society, Explanation, History.
  - Statistics: Law & Government, Debate, Opinion.
- **Combinations (Fig. 4, 200-example subset):** Fluency + Statistics was best, reported as the best pair at 35.8% average relative improvement per the heatmap. Averages by method: statistics 32.1%, fluency 31.4%, quotes 29.7%, citation 26.0%.
- **Limits** (the paper's design; see survey critique):
  - Fixed 5-document context, so the source is already retrieved.
  - LLM judge from the same model family.
  - No truthfulness constraint on added statistics or quotes.
  - No clicks, and a single time snapshot.
  - GPT-3.5 only, for the main table.

**Liu et al., "Lost in the Middle"** — [arXiv 2307.03172](https://arxiv.org/abs/2307.03172), 2023-07-06, TACL. Performance is highest when relevant information sits at the start or end of the context and "significantly degrades" in the middle. This is the mechanistic basis for position bias.

**Wan, Wallace, Klein, "What Evidence Do Language Models Find Convincing?"** — [arXiv 2402.11782](https://arxiv.org/abs/2402.11782), ACL 2024. On the ConflictingQA dataset, models "rely heavily on the relevance of a website to the query, while largely ignoring stylistic features that humans find important such as whether a text contains scientific references or is written with a neutral tone."

### 2.2 Academic: replications and critiques (2025–2026)

**Puerto et al., "C-SEO Bench: Does Conversational SEO Work?"** — [arXiv 2506.11097](https://arxiv.org/abs/2506.11097), 2025-06-06 (final 2025-10-20). NeurIPS 2025 per the survey.
- **Methods:** 10 in total — Authoritative, Statistics, Citations, Fluency, Unique Words, Technical Terms, Simple Language, Quotes, Content Improvement, LLM Guidance.
- **Models:** gpt-4o-mini, claude-3.5-haiku, o3, o4-mini.
- **Tasks:** question answering and product recommendation, 3 domains each.
- **Results:**
  - Only **3 of 54** cases were significantly positive: LLM Guidance on retail and video games, Content Improvement on retail. None were positive for question answering, and none for Haiku 3.5.
  - The Statistics method **decreased** rankings in 19 of 24 settings. On Haiku, 26 of 30 product-recommendation cases were negative.
  - Placing a document first in context gained 2.77 ±2.31 ranks (retail), 1.89 (video games) and 1.60 (books).
  - Gains "decrease steadily" as more actors adopt C-SEO, so the game is zero-sum.
- **Credibility:** high. It is multi-model and multi-domain, includes a multi-actor protocol, and uses newer models than the GEO paper.

**Kim et al., "SAGEO Arena"** — [arXiv 2602.12187](https://arxiv.org/abs/2602.12187), 2026-02-12, rev. 2026-08-07. A realistic pipeline: retrieval, then reranking, then generation.
- The abstract says existing approaches "often degrade performance in retrieval and reranking" and that "structural information helps mitigate these limitations".
- The HTML body, via model summary, gives:

  | Condition | Retrieval (H@20) | Reranking (H@10) | Citation |
  |---|---|---|---|
  | Body-only rewriting | −9% | −16% | −6% |
  | Structural fields only | +22% (+2.72 avg rank) | | +2% |
  | Stage-aware combined | +28% | | |

  AutoGEO-style rewriting dropped retrieval 36%.
- **Takeaway:** GEO body rewrites optimized for the generator can hurt the embedding and ranking stages that decide whether you are seen at all.

**Vishwakarma, Kumar, Jamidar, "What Gets Cited: Competitive GEO in AI Answer Engines"** — [arXiv 2605.25517](https://arxiv.org/html/2605.25517), SIGIR 2026 (Melbourne, July 2026).
- **Design:** 252,000 trials; 6 LLMs (Gemini-2.5-Flash, GPT-5-Nano, GPT-5-Mini, GPT-5.2, Claude-3.5-Sonnet, Kimi-K2-Thinking); 18 factors; 1,440 scenarios × 3 paraphrases = 4,320 instances. It is a two-document RAG testbed with counterbalanced order.
- **"Gatekeepers"** (OR ≫ 10,000 in all models): Topic Mismatch, Price Not Mentioned, Recent vs Old Timestamp, Lower List Position.
- **Significant in 4+ models** (OR ranges):
  - Keyword Gap 5.99–40.0
  - Missing Specifications 8.63–243
  - No Comparisons 1.61–7.45
  - Hedged Language 2.67–754
  - Claims With Evidence 2.09–≫10,000
  - Internal Contradictions 1.74–4.09
  - Weaker Value Proposition 1.53–7.24
  - Less Comprehensive 3.98–≫10,000
- **Inconsistent or null:** Content Structure 0.79–1.68 (n.s.), Scattered Information, Overly Promotional, Weaker Social Proof, No vs Old Timestamp, Recent vs No Timestamp.
- Formatting "had no impact, suggesting LLMs parse content regardless of visual organization."
- Model sensitivity varies: Kimi flagged 83% of factors, Claude-3.5 50%, Gemini-2.5 33%.
- **Caveat:** a 2-document context exaggerates effects (hence ORs ≫ 10,000). Scenarios are mostly commercial.

**Selvam & Ghosh, "CITECHOICE"** — [arXiv 2609.15164](https://arxiv.org/abs/2609.15164), 2026-09-14.
- Structured rendering raised target citations by +0.50 per answer (95% CI +0.20 to +0.84), through redistribution rather than more total citations.
- Rank 1 vs rank 5 showed a 42.3 pp gap.
- 15% of binary decisions changed on re-decoding.
- The authors do not claim a pure formatting mechanism or better source admission.

**Chen, Wang, Chen, Koudas, "Generative Engine Optimization: How to Dominate AI Search"** — [arXiv 2509.08919](https://arxiv.org/html/2509.08919v1), 2025-09.
- **Design:** 1,000 consumer ranking prompts (10 categories × 100). Engines: Perplexity sonar-pro, claude-3.5-sonnet, gemini-2.5-flash, gpt-4o-search vs Google via the Programmable Search API. Plus 5 extra languages.
- **Earned-media share:**

  | Vertical | AI engine | Google |
  |---|---|---|
  | Automotive, US | GPT 81.9% | 45.1% |
  | Consumer electronics, US | 92.1% | not stated |
  | Software, US | 72.7% | 45.4% |
  | Software, Canada | 74.2% | 31.8% |

  Social (Reddit etc.) was near 0% in these API-based engines, versus 10–23% on Google.
- Top-10 domain overlap with Google was only 20–41% for electronics. Local search overlap was as low as 2.5% (auto repair).
- GPT switches source ecosystems by language more than Google; Claude is most stable across languages.
- **Caveat:** observational snapshot using API models. Consumer ChatGPT and AI Overviews do cite Reddit heavily (see Profound and Semrush), so the "no social" finding does not generalize to consumer UIs.

**Wu, Zhong, Kim, Xiong, "AutoGEO: What Generative Search Engines Like…"** — [arXiv 2510.11438](https://arxiv.org/abs/2510.11438), 2025-10-13.
- LLM-extracted preference rules: attribute factual claims to credible sources; cover the topic comprehensively; be factually accurate and verifiable; use logical structure with headings and lists; use clear, concise language.
- Domain-specific rules: e-commerce favours step-by-step, actionable content; research favours explanatory depth.
- Visibility gains averaged 35.99% (up to 50.99% over Fluency Optimization) "while maintaining utility".
- **Caveat:** fixed 5-document context. SAGEO found AutoGEO-style rewrites cut retrieval 36% in a realistic pipeline.

**Bagga et al., "E-GEO"** — [arXiv 2511.20867](https://arxiv.org/abs/2511.20867), 2025-11-25, rev. 2026-07-14.
- **Design:** 13,747 product queries, 10 Amazon listings each, 5 engines, 15 heuristics.
- With GPT-4.1 as rewriter, only 4 of 15 heuristics beat baseline (trick +0.14, FAQ +0.05, competitive +0.03, format +0.02). Storytelling (−4.36), advertisement (−1.82), language (−1.66) and minimalist (−1.49) failed badly.
- Meta-optimized prompts converge on one playbook: user-intent alignment, opening summary, section headings, scannable lists, use-case documentation, FAQ content, synonyms without stuffing, and a factuality clause.

**Fang, Tao, Chen, Chang, Sakai, "Do LLMs Favor Recent Content?"** — [arXiv 2509.11353](https://arxiv.org/abs/2509.11353), 2025-09-14, SIGIR-AP 2025.
- Artificial dates were prepended to TREC DL21/22 passages, across 7 models (GPT-3.5/4/4o, Llama-3 8B/70B, Qwen-2.5 7B/72B).
- Top-10 mean publication year moved forward by up to 4.78 years; single items moved up to 95 ranks; up to 25% of pairwise preferences reversed.
- Larger models reduce the effect but none remove it.

**Zhang, He, Yao, "From Citation Selection to Citation Absorption"** — [arXiv 2604.25707](https://arxiv.org/abs/2604.25707), 2026-04-28.
- **Sample:** 602 prompts; 21,143 citations; 18,151 fetched pages; 72 features; ChatGPT, Google AIO/Gemini and Perplexity.
- ChatGPT cites fewer sources but each has higher influence. Perplexity and Google cite more.
- High-absorption pages are longer and structured, semantically aligned with the query, and rich in "definitions, numerical facts, comparisons, procedural steps."
- Correlational; the survey calls its composite score noncausal.

**Liu & Xu, "Think Before Writing" (FeatGEO)** — [arXiv 2604.19113](https://arxiv.org/abs/2604.19113), 2026-04-21, ACL 2026 per survey. "Citation behavior is more strongly influenced by document-level content properties than by isolated lexical edits."

**Schulte, Bleeker, Kaufmann, "Don't Measure Once"** — [arXiv 2604.07585](https://arxiv.org/abs/2604.07585), 2026-04-08. Visibility should be treated as a distribution. The survey reports Jaccard 0.34–0.42 over 45 days across 4 engines, with 7–8 repetitions per prompt recommended.

**Grossman et al., "How Generative AI Disrupts Search"** — [arXiv 2604.27790](https://arxiv.org/abs/2604.27790), 2026-04-30, SIGIR 2026.
- **Sample:** 11,500 queries.
- AIO appears on over half of queries (51.5% via survey), especially controversial ones.
- Sources barely overlap: URL Jaccard 0.11–0.18 among Google, AIO and Gemini (via survey). AI systems surface Google-owned properties more.
- **Sites blocking Google's AI crawler lose AI-result visibility.** AIO is less consistent across repeats.

**Kirsten et al. (ACL 2026)** — via survey only. 4,706 queries: AIO page overlap with organic is 18% vs 45% organic-to-organic; 53% of AIO domains are absent from the organic top 100; temperature-0 reruns change 9–28% of decisions. Unverified at source.

**Xu et al. (arXiv 2605.08474 per survey; that ID resolved to an unrelated paper when fetched, so the ID is wrong or unverified)** — via survey: 55,393 queries; AIO fires on 13.7% overall but 64.7% of question-phrased queries; ~11% of AIO claims are insufficiently supported.

**Sharma, "The Discovery Gap"** — [arXiv 2601.00912](https://arxiv.org/abs/2601.00912), 2026-01-01.
- **Sample:** 112 Product Hunt startups × 2,240 queries.
- Name queries were recognised 99.4% (ChatGPT) and 94.3% (Perplexity). Discovery queries: 3.32% and 8.29%.
- GEO optimization had no correlation with discovery. Referring domains r=+0.319 and community presence r=+0.395 did.
- Advice: "build the SEO foundation first and LLM visibility will follow."

**Adversarial / manipulation papers** (these prove the attack surface; they are not a strategy):
- **Kumar & Lakkaraju**, "Manipulating LLMs to Increase Product Visibility" — [arXiv 2404.07981](https://arxiv.org/abs/2404.07981), 2024-04-11. An optimized "strategic text sequence" pushed a fictitious coffee machine to top recommendation. Fictitious catalogue only; no commercial engine.
- **Nestaas, Debenedetti, Tramèr**, "Adversarial SEO for LLMs" — [arXiv 2406.18382](https://arxiv.org/abs/2406.18382), 2024-06-26, ICLR 2025 per survey.
  - Preference-manipulation attacks worked on Bing, Perplexity, GPT-4 plugins and Claude.
  - A fictitious camera's recommendation rate rose from 34.0% to 59.4%; plugin selection rose up to 7.2× (via survey).
  - It is a prisoner's dilemma: adoption degrades everyone.
- **Pfrommer et al.** (EMNLP 2024, via survey): prompt injection moved results about 3 ranks on Perplexity.
- **Smirnov**, "Exploring LLM biases to manipulate AI search overview" — [arXiv 2605.00012](https://arxiv.org/abs/2605.00012), 2026. RL-rewritten snippets raise selection. Selection is *comparative*, not absolute.
- **Defence:** GRADA cut attack success by up to about 80% (Zheng et al. 2025, via survey). Engines are hardening, and Google explicitly blocks inauthentic signals.

**Jinadu et al., "Authority Bias in Conversational Search Engines"** — [arXiv 2609.00248](https://arxiv.org/abs/2609.00248), 2026-08-31, EMNLP 2026. Across 8 LLMs recommending papers with identical content, prestige cues (author, venue, citation count) shift recommendations. The effect is "substantial and directional" and only partially debiasable. This implies that credential and authority *signals* can matter in LLM judgement, even though Wan et al. found relevance dominates.

**Critical survey, "Optimizing Visibility in Generative Engines: A Critical Survey of GEO (2023–2026)"** — [arXiv 2607.14035](https://arxiv.org/html/2607.14035v1), v1 2026-07-15. The best single overview.
- **Pipeline:** activation → retrieval → reranking → generation → absorption → behaviour.
- **Replicates:** in-context documents can change their citation share; relevance and position dominate; engines differ; content is an attack surface; extractable evidence often helps in controlled settings.
- **Rejected:** "GEO +40%" as a universal claim; generic heuristics generalizing; citation predicting clicks or conversions.
- **Conclusion:** "no technique with a stable, longitudinal, cross-platform causal effect on organic discoverability or downstream clicks and conversions."

### 2.3 Industry: citation sources and ranking overlap

**Ahrefs — AI Overview citations vs top 10** (via [SEJ](https://www.searchenginejournal.com/google-ai-overview-citations-from-top-ranking-pages-drop-sharply/568637/), 2026-03-02).
- **Sample:** 863,000 keywords; 4M AIO URLs.
- 38% of cited pages rank in the top 10 (down from 76% in Ahrefs' July 2025 study); 31.2% rank 11–100; 31.0% rank beyond 100.
- YouTube is 5.6% of all AIO citations and 18.2% of non-top-100 citations.
- Ahrefs says improved parsing makes the datasets "not directly comparable". Query fan-out is the stated mechanism.

**Ahrefs — AI assistant overlap** ([ahrefs.com/blog/ai-search-overlap](https://ahrefs.com/blog/ai-search-overlap/), 2025-08-11).
- **Sample:** 15,000 long-tail queries.
- 12% of cited URLs rank in Google's top 10; 80% don't rank anywhere for the original query.
- Perplexity 28.6%; ChatGPT and Gemini about 8%. Bing top-10 overlap 10% (Copilot 16.6%).

**BrightEdge.**
- 16-month study ([BrightEdge](https://www.brightedge.com/resources/weekly-ai-search-insights/rank-overlap-after-16-months-of-aio), 2025-09-18): AIO citations overlapping with "organic rankings" rose from 32.3% to 54.5%.
  - By industry: healthcare 75.3%, education 72.6%, B2B tech 71.0%, insurance 68.6%, finance 32.2%, e-commerce 22.9%, restaurants 19.2%.
  - "Organic rankings" appears to mean any organic rank, not just the top 10.
- Feb 2026 BrightEdge figure: about 17% top-10 overlap, flat over the period, and AIO coverage +58% year over year (secondary via SEJ; unverified at source).

**Profound — citation patterns** ([tryprofound.com](https://www.tryprofound.com/blog/ai-platform-citation-patterns), 2025-06-05, updated 2025-08).
- **Sample:** 680M citations, Aug 2024–Jun 2025. Shares are of *all* citations.
- ChatGPT: Wikipedia 7.8%, Reddit 1.8%, Forbes 1.1%.
- Google AIO: Reddit 2.2%, YouTube 1.9%, Quora 1.5%.
- Perplexity: Reddit 6.6%, YouTube 2.0%, Gartner 1.0%.

**Semrush — most-cited domains** ([semrush.com](https://www.semrush.com/blog/most-cited-domains-ai/), 2025-11-10).
- **Sample:** 230k+ prompts; 100M+ citations; ChatGPT, AI Mode and Perplexity; 2025-07-14 to 2025-10-12.
- In mid-September 2025, ChatGPT's Reddit citations fell from about 60% to about 10% of responses, and Wikipedia from about 55% to under 20%. PR Newswire, Forbes and Medium gained.
- AI Mode's top sources were LinkedIn, YouTube, Reddit and Google.
- **Lesson:** platform source mixes shift within weeks.

**Semrush — AI search SEO traffic study** ([semrush.com](https://www.semrush.com/blog/ai-search-seo-traffic-study/), 2025, date unverified).
- The average AI search visitor is "4.4 times as valuable" (conversion rate). This is a vendor estimate.
- ChatGPT cites pages ranking position 21+ about 90% of the time.
- AI search visitors are forecast to pass organic by about 2028.

**Pew Research** ([pewresearch.org](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/), 2025-07-22). Wikipedia, YouTube and Reddit made up 15% of AI summary sources (see §2.5 for the click findings).

### 2.4 Industry: content-feature correlations

**AirOps, "The Fan-Out Effect"** ([airops.com](https://www.airops.com/report/the-fan-out-effect-what-happens-between-a-query-and-a-citation), 2026-04-13).
- **Sample:** 16,851 queries; 353,799 pages; 50,553 ChatGPT responses (3 runs each); 815,484 coverage rows.
- **Retrieval position:** 58% citation at position 1 vs 14% at position 10.
- **Headings:** strong query match 41% vs weak 29%.
- **Fan-out coverage:** pages covering 26–50% of ChatGPT's fan-out sub-queries beat pages covering 100%.
- **Authority:** "DA and backlinks show no positive correlation … slightly inversely correlated" (conditional on being retrieved).
- **Length:** 500–2,000 words best; over 5,000 words underperforms.
- **Structure and schema:** 7–20 H2–H4 headings; JSON-LD +6.5 pp.
- **Readability:** Flesch-Kincaid 16–17 best (35.9%).
- **Freshness:** 30–89 days old is best (32.8%); under 30 days 25.3%.
- **Answer position:** 41% of citations fall in the first third of the answer.
- Related SEL coverage (403 when fetched): ChatGPT retrieves about 6× more pages than it cites (85% never cited); 43.2% of Google #1 pages were cited; biggest length lift at 5,000–10,000 characters. Unverified at source.

**Kevin Indig / Growth Memo** (secondary via [Search Engine Land](https://searchengineland.com/chatgpt-citations-content-study-469483), 2026; primary [growth-memo.com](https://www.growth-memo.com/p/the-science-of-how-ai-picks-its-sources) is paywalled).
- **Sample:** 1.2M ChatGPT responses; 18,012 verified citations.
- 44.2% of citations come from the first 30% of the text (a "ski ramp").
- Cited text is 2× likelier to contain a question mark; 78.4% of question-tied citations came from headings.
- Proper nouns: 20.6% in cited text vs 5–8% in typical text.
- Flesch-Kincaid 16 (cited) vs 19.1 (not cited).
- The "Shorter, focused content wins" follow-up (815k query-page pairs, which appears to be the AirOps dataset) found "ultimate guides" underperform focused pages.

**SE Ranking — ChatGPT citation factors** (via [SEJ](https://www.searchenginejournal.com/new-data-top-factors-influencing-chatgpt-citations/561954/), ~late 2025, date unverified).
- **Sample:** 129k domains; 216,524 pages; 20 niches.
- **Authority:** referring domains were the strongest correlate (350k+ referring domains → 8.4 average citations vs 1.6–1.8 at ≤2,500).
- **Traffic:** gains appear only above about 190k monthly visitors.
- **Length:** over 2,900 words → 5.1 citations vs 3.2 under 800 words.
- **Freshness:** updated within 3 months → 6 citations.
- **Data points:** 19+ → 5.4 citations. Expert quotes 4.1 vs 2.4 (secondary).
- **Community and reviews:** Reddit and Quora presence and review-platform listings (4.6–6.3) correlate.
- **Speed:** FCP under 0.4 s → 6.7 citations vs 2.1 above 1.13 s.
- **No or negligible effect:** FAQ schema, keyword URLs and titles, llms.txt.
- All raw means, not controlled. Big-site confounding is severe.

**SE Ranking — llms.txt** ([seranking.com](https://seranking.com/blog/llms-txt/), 2025-11-07).
- **Sample:** 300k domains; 10.13% adoption. Method: XGBoost + Spearman + SHAP.
- No relationship with citations; removing the feature *improved* model accuracy.
- Only 1 of the 50 most AI-cited domains had the file (secondary via SEJ).

**Ahrefs — brand factors** ([ahrefs.com](https://ahrefs.com/blog/ai-overview-brand-correlation/), 2025-05-26).
- **Sample:** 75k brands (DR>40), Spearman correlation with AIO brand mentions.
- Branded web mentions 0.664; branded anchors 0.527; branded search volume 0.392; DR 0.326; backlinks 0.218; ad traffic 0.216.
- Top-quartile mention brands average 169 AIO mentions vs 14 in the next quartile (secondary).
- A 2026 follow-up reportedly found YouTube mentions the strongest signal (BusinessWire 2026-05-26; unverified, not fetched).
- Ahrefs itself says "correlation ≠ causation."

**Ahrefs — freshness** ([ahrefs.com/blog/fresh-content](https://ahrefs.com/blog/fresh-content), 2025-12-22). Across 17M citations, AI-cited content is 25.7% fresher than organic results. ChatGPT shows the strongest preference: 393–458 days newer than organic. AIO behaves most like organic.

### 2.5 Industry: clicks and zero-click behaviour

**Pew Research** (2025-07-22).
- **Sample:** 900 US adults' real browsing; 68,879 searches in March 2025, of which 12,593 had an AI summary (about 18%).
- Result clicks: 8% with a summary vs 15% without. Links inside the summary: 1%.
- Session ended: 26% vs 16%.
- Median summary 67 words.
- Summary appears for 53% of 10+ word queries and 60% of question queries.

**Ahrefs CTR** (2025-04-17).
- **Sample:** 300k keywords (150k with AIO, 150k informational without), GSC desktop data, March 2024 vs March 2025.
- Position-1 CTR on AIO keywords fell from 0.073 to 0.026; modeled effect −34.5%.
- 2026 update (Dec 2025 data, 300k keywords): −58% (via [Medianama](https://www.medianama.com/2026/02/223-google-ai-overviews-click-through-rates-58-study/), 2026-02; BusinessWire 403).

**Seer Interactive**.
- Sept 2025 study (secondary): organic CTR on AIO queries fell from 1.76% to 0.61% (−61%); paid from 19.7% to 6.34% (−68%).
- 2026 update ([seerinteractive.com](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update), 2026-04):
  - **Sample:** 53 brands; 5.47M queries; 2.43B impressions; Jan 2025–Feb 2026.
  - CTR rebounded from 1.3% (Dec 2025) to 2.4% (Feb 2026).
  - Cited brands: +120% organic clicks per impression vs uncited, still −38% vs non-AIO queries.
  - AIO appears on 36% of informational, 8% of commercial and 5% of transactional queries; over 85% for comparison and question queries.

**Similarweb** (via [SERoundtable](https://www.seroundtable.com/similarweb-google-zero-click-search-growth-39706.html), 2025-07). Zero-click grew from 56% to 69% between May 2024 and May 2025. News organic visits fell from over 2.3B to under 1.7B. ChatGPT referrals to news rose 25× year over year.

**SparkToro / Datos** ([sparktoro.com](https://sparktoro.com/blog/2024-zero-click-search-study-for-every-1000-us-google-searches-only-374-clicks-go-to-the-open-web-in-the-eu-its-360/), 2024-07-02). Zero-click: 58.5% (US) and 59.7% (EU). Clicks to the open web per 1,000 searches: 374 (US) and 360 (EU), per the article title. The model summary inverted these, so the title figures are used. This is the pre-AIO-expansion baseline.

**Bain & Company** ([bain.com](https://www.bain.com/about/media-center/press-releases/20252/consumer-reliance-on-ai-search-results-signals-new-era-of-marketing--bain--company-about-80-of-search-users-rely-on-ai-summaries-at-least-40-of-the-time-on-traditional-search-engines-about-60-of-searches-now-end-without-the-user-progressing-to-a/), 2025-02). A survey (Dynata) plus clickstream. About 80% of users rely on AI summaries for at least 40% of searches; about 60% of searches end without a click; estimated organic traffic loss 15–25%. Survey-based, so self-reported.

### 2.6 Official platform statements

**Google, "AI features and your website"** ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features), updated 2025-12-10).
- No "additional requirements … nor other special optimizations".
- AI features use **query fan-out** ("multiple related searches across subtopics and data sources").
- Eligibility = indexed and snippet-eligible.
- nosnippet, data-nosnippet, max-snippet and noindex control display.
- Traffic is reported under Web in Search Console.
- Google's claim: AIO clicks are "higher quality".

**Google, "Optimizing your website for generative AI features on Google Search"** ([developers.google.com](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), updated 2026-07-10). Verbatim:
- "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search"
- "There's no requirement to break your content into tiny pieces for AI to better understand it."
- "You don't need to write in a specific way just for generative AI search."
- "Seeking inauthentic 'mentions' across the web isn't as helpful as it might seem."
- "Structured data isn't required for generative AI search, and there's no special schema.org markup"
- "There's no ideal page length"
- Plus: use the Search Console **Generative AI performance report**, and be wary of tools claiming "internal" Google metrics.

Positive guidance:
- Unique, non-commodity content ("first-hand review"; "Don't just recycle what others … have already said").
- Clear headings and sections; images and video.
- Crawlability and JS SEO; page experience; less duplication.
- Merchant Center feeds and Business Profile.

**Google Search Central blog, "Top ways to ensure your content performs well in Google's AI experiences"** ([developers.google.com](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search), 2025-05). Unique content; technical requirements; page experience; structured data that matches visible content; preview controls; multimodal. Summarized by a model; exact wording unverified.

**Individual Google staff statements.**
- **Danny Sullivan**, Search Off the Record ([SERoundtable](https://www.seroundtable.com/google-content-bite-sized-chunks-40728.html), 2026-01-09): on bite-sized chunking, "We don't want you to do that. We really don't. We don't want people to have to be crafting anything for Search specifically." He framed any current gains as temporary.
- **John Mueller**, Reddit ([SEJ](https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/), 2025-04-17): "none of the AI services have said they're using LLMs.TXT (and you can tell when you look at your server logs that they don't even check for it)… comparable to the keywords meta tag."
- **Gary Illyes**, Search Central Live APAC (2025-07-23, secondary): Google does not support llms.txt; normal SEO is enough for AIO.

---

## 3. Conflicts and how to resolve them

| Topic | Finding A | Finding B | More credible reading |
|---|---|---|---|
| **Do statistics help?** | GEO: +31% (GPT-3.5, fixed 5-doc context) | C-SEO Bench: Statistics method *lowered* rank in 19/24 settings (modern models) | C-SEO is newer, multi-model, multi-domain, so it wins on *LLM-inserted* statistics. Vishwakarma "Claims With Evidence" and Zhang absorption show *genuine, specific* evidence helps. Rule: add real, sourced numbers that answer the query; never pad. |
| **Does the "40%" lift exist?** | GEO abstract "up to 40%" | Survey: rejected as universal; C-SEO 3/54 positive; SAGEO body rewrites −9% retrieval | The 40% holds only in-context, on one metric, for low-ranked sources. For rank-1 sources the same methods cost 20–30%. |
| **AIO citations vs top-10 rankings** | Ahrefs 76% (Jul 2025) | Ahrefs 38% (Mar 2026; parser changed); BrightEdge ~17% (Feb 2026); Kirsten 18% page overlap | The definition drives the number (top-10 vs any organic rank; URL vs domain; parser). The consensus direction: ranking helps a lot, but most AIO citations are *not* the top-10 URL for the head query, because fan-out sub-queries retrieve other pages. BrightEdge's 54.5% "organic overlap" likely counts any organic rank. |
| **Do authority and backlinks matter?** | SE Ranking: referring domains strongest; Sharma r=0.319; Ahrefs DR 0.326 | AirOps: DA/backlinks slightly *negative*; Ahrefs: backlinks 0.218 vs mentions 0.664 | Different stages. Domain authority governs *getting into the retrieved pool* (index, rank, fan-out). AirOps conditions on already-retrieved pages, where page-level relevance decides. Both are true. |
| **Content length** | SE Ranking: >2,900 words 5.1 vs <800 words 3.2 | AirOps: 500–2,000 words best, >5,000 worse; Indig: focused beats "ultimate guide"; Google: "no ideal page length" | All observational and confounded (big sites write long). No length target is defensible. Cover the question completely, front-load the answer, split genuinely distinct intents into separate pages. |
| **Formatting and structure** | Vishwakarma: Content Structure null; formatting "no impact" | CITECHOICE: structured rendering +0.50 citations per answer; AirOps headings 41% vs 29%; SAGEO structural fields +22% retrieval | Visual formatting barely affects the LLM's reading. *Query-aligned headings, titles and metadata* affect retrieval and matching. Use headings as query-shaped signposts, not decoration. |
| **Freshness** | Vishwakarma: recent vs old OR ≫ 10k; Fang: up to 95-rank moves; Ahrefs: 25.7% fresher; SE Ranking: updated <3 months best | AirOps: <30 days (25.3%) underperforms 30–89 days (32.8%); Vishwakarma: "no timestamp vs old" inconsistent | Freshness is a real bias, strongest for time-sensitive and commercial queries. Brand-new pages haven't been indexed and linked yet. Keep content *genuinely* current with visible, accurate dates. Fake date bumps are manipulation (Google spam policies) and risky. |
| **Reddit share** | Semrush Jun 2025: Reddit in 40.1% of LLM citations (secondary) | Profound: Reddit 1.8% of ChatGPT citations; Semrush Nov 2025: ChatGPT Reddit fell from ~60% to ~10% of responses | Denominators differ ("% of responses citing" vs "% of all citations"), and platforms change policy mid-stream. Community presence matters for Perplexity and AIO, but mixes are volatile. |
| **Earned vs social** | Chen et al.: AI engines ~0% social | Profound/Semrush: Reddit top domain on Perplexity and AIO | Chen used API models (sonar-pro, gpt-4o-search), which cite differently from consumer UIs. Trust consumer-UI studies for real-world mix. |
| **CTR impact size** | Ahrefs −34.5% → −58%; Seer −61% | Seer 2026: rebound to 2.4%; Google: clicks "higher quality" | Pew (real panel behaviour, n=900) is the most neutral: clicks roughly halve (15% → 8%). Vendor GSC studies agree on direction. The magnitude moves with AIO design changes. Google's "higher quality" claim is unaudited. |
| **Does schema help AI citation?** | AirOps: JSON-LD +6.5 pp (observational) | Google: no special schema needed; SE Ranking: FAQ schema negligible | No causal evidence of an AI citation lift. Keep schema for rich results and entity clarity, not as a GEO lever. |

---

## 4. Actionable rules for a website, derived from the evidence

Ordered by evidence strength. Each rule cites its basis.

### A. Retrieval first: classic SEO is the precondition

1. **Be crawlable, indexable and snippet-eligible for Google, and do not block the search/answer crawlers you want citations from.**
   - Snippet eligibility is Google's only AIO/AI Mode requirement ([Google](https://developers.google.com/search/docs/appearance/ai-features), 2025-12-10).
   - Grossman et al. found sites blocking Google's AI crawler lose AI visibility ([2604.27790](https://arxiv.org/abs/2604.27790), 2026-04-30).
   - Server-rendered HTML with no JS-only content (Google guide 2026-07-10; Semrush traffic study 2025).
2. **Rank for the head query and its fan-out sub-queries.** Map each target query's sub-questions (comparisons, pricing, specs, "how to", "vs", "best for X") and make sure the site has a strong page for each.
   - Evidence: fan-out ([Google](https://developers.google.com/search/docs/appearance/ai-features)); [Ahrefs](https://ahrefs.com/blog/ai-search-overlap/) 2025-08-11 (80% of assistant citations don't rank for the original query); [AirOps](https://www.airops.com/report/the-fan-out-effect-what-happens-between-a-query-and-a-citation) 2026-04-13 (retrieval rank 1 = 58% vs rank 10 = 14% citation).
3. **Keep building links and authority, because they get you into the candidate pool.** Referring domains predict ChatGPT citation (SE Ranking via [SEJ](https://www.searchenginejournal.com/new-data-top-factors-influencing-chatgpt-citations/561954/)) and LLM discovery of startups (r=0.319, [Sharma 2601.00912](https://arxiv.org/abs/2601.00912)). C-SEO Bench: improving position in context beats every content rewrite ([2506.11097](https://arxiv.org/abs/2506.11097)).

### B. Page content: what the generator selects and absorbs

4. **Answer the query directly near the top of the page.** Lead with the definition, conclusion or recommendation, then support it.
   - 44.2% of ChatGPT citations come from the first 30% of text (Indig via [SEL](https://searchengineland.com/chatgpt-citations-content-study-469483), 2026).
   - U-shaped position bias ([Liu et al. 2307.03172](https://arxiv.org/abs/2307.03172)).
5. **Make headings mirror real user questions and sub-queries** (H2 as the question, the next paragraph as the answer). Headings that closely match the query: 41% vs 29% cited ([AirOps](https://www.airops.com/report/the-fan-out-effect-what-happens-between-a-query-and-a-citation), 2026-04-13). Structural fields drive retrieval ([SAGEO 2602.12187](https://arxiv.org/abs/2602.12187)).
6. **Write clear, query-aligned titles, meta descriptions and H1s.** Structural-field optimization gave +22% retrieval hit rate, while body-only rewrites *lost* 9% ([SAGEO](https://arxiv.org/html/2602.12187), 2026). Title and snippet text is what retrieval and rerank stages see first.
7. **Include real, specific, sourced evidence:** statistics with their source, attributed expert quotations, and citations to primary sources.
   - GEO: Quotation +41%, Statistics +31%, Cite Sources +27% ([2311.09735](https://arxiv.org/abs/2311.09735)).
   - "Claims With Evidence" significant in 4+/6 LLMs ([2605.25517](https://arxiv.org/html/2605.25517)).
   - Absorption favours numerical facts ([2604.25707](https://arxiv.org/abs/2604.25707)).
   - **Never fabricate or pad.** LLM-inserted statistics hurt in 19/24 settings ([C-SEO](https://arxiv.org/html/2506.11097)).
8. **Include decision-critical specifics for commercial pages:** price, specs, comparisons against alternatives, a clear value proposition, and who it's for.
   - Price Not Mentioned is a gatekeeper (OR ≫ 10,000); Missing Specifications OR 8.63–243; No Comparisons OR 1.61–7.45 ([Vishwakarma 2605.25517](https://arxiv.org/html/2605.25517)).
   - Merchant Center feeds for products ([Google guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)).
9. **Include definitions, comparisons and procedural steps** where the intent calls for them. These are the extractable units generators absorb ([Zhang 2604.25707](https://arxiv.org/abs/2604.25707); AutoGEO e-commerce "step-by-step", research "in-depth" [2510.11438](https://arxiv.org/abs/2510.11438)).
10. **Write decisively; avoid hedging and internal contradictions.** Hedged Language OR 2.67–754 and Internal Contradictions OR 1.74–4.09 against the hedged or contradictory document ([2605.25517](https://arxiv.org/html/2605.25517)). Being decisive does not mean being promotional: "Overly Promotional" was inconsistent, and "advertisement" rewrites scored −1.82 in [E-GEO](https://arxiv.org/html/2511.20867).
11. **Use named entities explicitly** (product names, people, organisations, places) instead of vague pronouns. Cited text is about 20.6% proper nouns vs 5–8% baseline (Indig, observational). Clear entities also reduce topic-mismatch risk.
12. **Provide original, non-commodity information:** first-hand testing, proprietary data, unique perspective. This is Google's primary stated lever ([guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-07-10). Chen et al. show engines prefer sources that *justify* claims ([2509.08919](https://arxiv.org/abs/2509.08919)).

### C. Freshness

13. **Keep time-sensitive pages genuinely updated, and show accurate visible "published" and "updated" dates**, mirrored in `datePublished`/`dateModified`. Update the substance, not just the date.
    - Recent vs old timestamp is a gatekeeper ([2605.25517](https://arxiv.org/html/2605.25517)).
    - Recency bias in LLM rerankers ([2509.11353](https://arxiv.org/abs/2509.11353)).
    - AI citations are 25.7% fresher than organic ([Ahrefs](https://ahrefs.com/blog/fresh-content), 2025-12-22).
    - Do not fake dates. "No timestamp vs old" is inconsistent, so remove stale dates rather than lie.

### D. Off-site presence

14. **Earn independent coverage:** reviews, comparisons by third parties, press, analyst mentions, YouTube, and authentic community discussion.
    - Earned media is 69–92% of AI citations in consumer verticals ([Chen 2509.08919](https://arxiv.org/html/2509.08919v1)).
    - Branded mentions 0.664 vs backlinks 0.218 ([Ahrefs](https://ahrefs.com/blog/ai-overview-brand-correlation/), 2025-05-26).
    - Community presence r=0.395 ([Sharma](https://arxiv.org/abs/2601.00912)).
    - Authentic only: Google says inauthentic mentions are unhelpful ([guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)).
15. **Maintain accurate Business Profile, Merchant Center, and review-platform listings.** These are Google guide items; review-platform listings correlate with ChatGPT citations (SE Ranking).

### E. Page shape

16. **Keep one page per intent, focused and complete. Don't pad toward a word count, and don't fragment into micro-pages.**
    - Google: "no ideal page length"; chunking not required.
    - Sullivan 2026-01-09: "We don't want you to do that."
    - Focused pages beat "ultimate guides" in ChatGPT (Indig/AirOps). Pages covering 26–50% of fan-out beat pages covering 100%, which argues for a hub plus focused spokes.
17. **Use normal semantic HTML structure** (paragraphs, headings, lists, tables where the data is tabular), but don't expect formatting alone to move citations. Content Structure was null ([2605.25517](https://arxiv.org/html/2605.25517)); CITECHOICE found structured rendering redistributes credit but doesn't expand it.
18. **Add valid schema.org that matches visible content**, for rich results and entity clarity. Do *not* expect FAQ schema or special markup to lift AI citation (Google 2025-12-10 and 2026-07-10; SE Ranking FAQ schema negligible).
19. **Keep pages fast.** Speed correlates with citation (FCP under 0.4 s → 6.7 vs 2.1 citations, SE Ranking, observational) and it is a Google page-experience item.

### F. What not to do

20. **Don't keyword-stuff.** −8% on GEO-bench and worse on Perplexity ([2311.09735](https://arxiv.org/abs/2311.09735)).
21. **Don't treat llms.txt as a visibility lever.** It is optional and harmless, but has shown no effect ([SE Ranking](https://seranking.com/blog/llms-txt/) 2025-11-07; Mueller 2025-04-17; Google guide 2026-07-10).
22. **Don't use hidden prompt injections, "strategic text sequences", or LLM-manipulation text.** They work in labs ([2404.07981](https://arxiv.org/abs/2404.07981), [2406.18382](https://arxiv.org/abs/2406.18382)), but defences cut attack success by up to about 80% (via [survey](https://arxiv.org/html/2607.14035v1)), and gains erode as others adopt them ([C-SEO](https://arxiv.org/abs/2506.11097)). They are spam under Google policy.
23. **Don't mass-rewrite already-ranking pages with generic GEO templates.** GEO methods cut visibility of rank-1 sources by 20–30% ([GEO Table 2](https://arxiv.org/abs/2311.09735)). Body-only rewrites cut retrieval ([SAGEO](https://arxiv.org/abs/2602.12187)).
24. **Don't use persuasive or "authoritative" tone as a tactic.** It made no significant improvement in GEO; prefer substantive evidence.

### G. Measurement

25. **Measure AI visibility as a distribution.**
    - Run each tracked prompt 7–8+ times per engine, across paraphrases and over time ([Schulte 2604.07585](https://arxiv.org/abs/2604.07585); via [survey](https://arxiv.org/html/2607.14035v1)).
    - Track Google via the Search Console Generative AI performance report ([guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)).
    - Expect week-scale volatility (ChatGPT's Reddit share fell from ~60% to ~10% in Sept 2025, [Semrush](https://www.semrush.com/blog/most-cited-domains-ai/)).
    - Don't claim traffic or conversion effects from citation share alone; the causal evidence is weak (survey).
