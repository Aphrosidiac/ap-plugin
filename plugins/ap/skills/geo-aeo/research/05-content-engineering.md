# 05 — Content Engineering for AEO + GEO + Classic SEO

Research dossier, compiled 2026-09-26. Scope: how to write and structure pages so answer engines (Google AI Overviews / AI Mode, ChatGPT search, Perplexity, Copilot, Gemini) extract, trust and cite them, while classic Google search still ranks them.

Evidence tags:
- **[strong]**: primary source from the engine owner (Google/Bing documentation) or a peer-reviewed or controlled experiment that others have replicated.
- **[moderate]**: a large observational study with a stated method (thousands of URLs or citations), or a controlled study that has not been replicated.
- **[weak]**: a small sample, a single vendor claim, or an unverified report.
- **[practitioner consensus]**: widely agreed practice with no clean causal data behind it.

Dates are the publication date or the "last updated" date of each source.

---

## 0. The reconciling frame (read first)

There are two camps, and the skill has to hold both views at once.

1. **What Google says.** In its guide *Optimizing for generative AI features* (published about 2026-05-15, updated 2026-07-10), Google says: "optimizing for generative AI search is optimizing for the search experience, and thus still SEO." It then rejects several common GEO tactics outright:
   - "There's no requirement to break your content into tiny pieces for AI to better understand it."
   - "You don't need to write in a specific way just for generative AI search."
   - No llms.txt, no special Markdown, no special schema.
   - Manufacturing "mentions" does not help.
   [strong] https://developers.google.com/search/docs/fundamentals/ai-optimization-guide (updated 2026-07-10); coverage at https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/ (2026-05-15)
2. **What the measurements show.** AI answer engines are retrieval-augmented generation (RAG) pipelines. They pick passages, not pages.
   - They draw citations heavily from the top third of a document.
   - They prefer definitional, entity-dense, self-contained sentences.
   - They reward pages that rank for many *fan-out* sub-queries, not only the head query.
   - Google's grounding uses extractive summarization under a fixed word budget. (Sections 1–2 give the numbers.)
3. **How the two fit together.** Write for people first. Use the structure that good technical writers have always used: answer first, descriptive headings, one idea per section, tables for comparisons, sources for claims. That structure is also what a passage retriever extracts well. Do **not** produce "AI versions" of pages, micro-chunked fragments, keyword-variant pages or hidden instructions. Google now names manipulating generative AI responses as spam (Section 8). The 2025–2026 academic replication work also shows that "GEO tricks" mostly fail or cancel out once competitors adopt them (Section 1.5).

**Rule for the agent.** Every transformation must make the page better for a human reader. If a change only exists "for the AI", don't make it.

---

## 1. How retrieval works, and what it implies for writing

### 1.1 Passage-level ranking and retrieval

- **Google has scored passages independently since 2021.** Passage ranking launched on 2021-02-10 for US English and affected about 7% of queries. Martin Splitt describes it as a *ranking* change, not an indexing change. Google can "score different parts of a page independently", so a strong section buried in a long page can rank. [strong] https://www.searchenginejournal.com/google-passage-ranking-martin-splitt/388206/ (2021)
- **AI features use the same index and ranking systems.** Google: "There are no additional requirements to appear in AI Overviews or AI Mode." A page must be indexed and eligible for a snippet. Snippet controls (`nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`) also govern what AI features may use. [strong] https://developers.google.com/search/docs/appearance/ai-features (updated 2025-12-10)
- **Google's grounding is extractive and budgeted.** DEJAN analysed 7,060 queries with 3 or more sources:
  - Gemini grounding receives a roughly fixed budget of about 2,000 words per query (median 1,929), split by relevance rank.
  - The #1 source gets about 531 words (28%); the #5 source gets about 266 words (13%).
  - The median page contributes 377 words. Contribution plateaus at about 540 words.
  - Coverage falls with length: pages under 1,000 words have 61% of their text used; pages over 3,000 words have 13% used.
  - Text that gets selected: value propositions, specific features, pricing, process steps. Text that gets dropped: navigation, promotional claims, legal boilerplate, verbose review text.

  [moderate] https://dejan.ai/blog/how-big-are-googles-grounding-chunks/ and https://dejan.ai/blog/sro-grounding-snippets/ (series Sep 2025 – Feb 2026)

  **Implication.** Density beats length. Put the extractable facts (definition, numbers, steps, prices) in plain declarative sentences. Don't pad them.
- **Other engines.** ChatGPT, Perplexity and Copilot follow the same general pattern: they search (Bing, their own index, or both), chunk, embed or rerank, then synthesize with citations. Bing's AI Performance report (public preview since 2026-02-10) exposes "grounding queries", the phrases the AI used to retrieve content that it then cited. That is direct evidence that retrieval runs on sub-queries. [strong] https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/
- **Dense retrieval in practice.** Queries and passages become embeddings, and the passages with the highest cosine similarity are reranked and passed to the LLM. iPullRank's "relevance engineering" recommends "atomic, synthesizable passages" under query-shaped headings, each with stand-alone value, tested by simulating retrieval (embed the likely sub-queries and check which passage wins). [practitioner consensus] https://ipullrank.com/ai-search-manual/relevance-engineering (2025)

### 1.2 Query fan-out: why topical coverage now matters more than the head term

- **Google's description.** AI Overviews and AI Mode may issue "multiple related searches across subtopics and data sources". [strong] https://developers.google.com/search/docs/appearance/ai-features
- **Robby Stein (Google VP Search) on AI Mode.** It "makes a plan, breaks it down into related subtopics, and runs multiple Google searches". Deep Search can run dozens to hundreds of searches. [strong] https://www.searchenginejournal.com/query-fan-out-technique-in-ai-mode-new-details-from-google/552532/ (2025-07)
- **Ahrefs, 863K SERPs and 4M AI Overview URLs (2026-03-02).** Only 37.9% of cited pages rank in the top 10 for the query. 31.2% rank 11–100, and 31.0% rank beyond 100. In Ahrefs' mid-2025 version of the study the top-10 share was 76%. Ahrefs attributes the drop to heavier use of fan-out after AI Overviews moved to Gemini 3 in January 2026. YouTube supplies 5.6% of all AI Overview citations. [moderate] https://ahrefs.com/blog/ai-overview-citations-top-10/
- **Surfer, 173,902 URLs across 10,000 keywords with about 33K fan-out queries generated by Gemini.**
  - Spearman correlation of 0.77 between the number of fan-out queries a page ranks for and its AI Overview citation likelihood.
  - Pages that rank for the main query plus a fan-out are 161% more likely to be cited.
  - Pages that rank *only* for fan-outs are 49% more likely to be cited than pages ranking only for the main query.

  [moderate, correlational] https://surferseo.com/blog/query-fan-out-impact/ (about late 2025)

**What "semantic completeness" means in practice** [practitioner consensus, grounded in the above]:
1. For each target query, list the sub-questions a planner would generate:
   - definition
   - how it works
   - cost / price
   - comparison vs alternatives
   - pros and cons
   - who it's for / not for
   - steps / how to
   - risks
   - local or regulatory specifics
   - recent changes / "in 2026"
   - troubleshooting
2. Give each sub-question its own heading and a self-contained answer on the pillar page, or on a linked child page when the answer needs more than about 300 words.
3. Build hub-and-spoke clusters so the site ranks for many fan-outs. Don't build one giant page (grounding coverage collapses past about 2–3K words, per DEJAN).
4. Google's own position is that you don't need "every long-tail keyword variation" (ai-optimization-guide). Cover *intents and facts*, not phrasings. Never create near-duplicate pages per variant (scaled content abuse, doorways; see Section 8).

### 1.3 Information gain and originality

- **The patent.** US20200349181A1, "Contextual estimation of link information gain" (filed 2018, published 2020; granted as US12013887B2). It describes scoring a document by how much information it adds beyond documents the user has already seen, and using that score to rerank. Google has not confirmed use in ranking. [weak as a ranking claim; strong as a documented concept] https://patents.google.com/patent/US20200349181A1/en ; explainer https://www.searchenginejournal.com/how-google-may-understand-unique-content/581959/ (2026-07-15)
- **Google's documented stance aligns with the idea:**
  - Its helpful-content questions ask whether content provides "original information, reporting, research, or analysis" and "substantial value when compared to other pages". [strong] https://developers.google.com/search/docs/fundamentals/creating-helpful-content (updated 2025-12-10)
  - Its AI guidance asks for "unique, non-commodity content". [strong] https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search (2025-05-21)
- **Why this matters more for AI.** When fan-out retrieves 10–30 near-identical passages, a synthesizer has little reason to cite the tenth paraphrase. It has every reason to cite the one passage with a unique number, a named source, first-hand results or a clear verdict.

**Operational definition for the agent.** Each page must contain at least one element a competitor page cannot copy by paraphrasing:
- original data
- a test result
- a photo or screenshot of your own work
- a named expert quote
- a pricing table
- a worked local example
- a decision rule or verdict
- a tool

### 1.4 Position-in-page effects

- **Kevin Indig, ChatGPT: 1.2M answers, 18,012 verified citations (published about 2026-02).**
  - 44.2% of citations come from the first 30% of a document, 31.1% from 30–70%, and 24.7% from the final 30%.
  - Cited text is about 2× more likely to contain definitive phrasing ("is defined as", "refers to", "X is Y"): 36.2% vs 20.2%.
  - Question-mark headings are about 2× as likely among cited sections.
  - Cited text has high entity density: about 20.6% proper nouns vs 5–8% in typical prose.
  - Cited text has a balanced subjectivity of about 0.47 (analytical, not purely neutral or purely opinion).
  - Readability of about Flesch-Kincaid grade 16 beat grade 19+ academic prose.

  [moderate] summary https://almcorp.com/blog/chatgpt-citations-study-44-percent-first-third-content/ ; https://searchengineland.com/chatgpt-citations-content-study-469483
- **CXL, 100 AI Overview citations.** 55% of cited passages came from the first 30% of the page, 24% from 30–60%, and 21% from the last 40%. The 10–20% zone was the single hottest band. [weak, small n] https://cxl.com/blog/google-ai-overview-citation-sources/
- **DEJAN.** Positional bias in grounding extraction is strong; front-load. [moderate]
- **Critical survey (July 2026).** Across the GEO literature, "relevance and position" are "the two most robust factors". The 252,000-trial factorial experiment by Vishwakarma et al. (2026) found them to be the primary determinants of the first citation. [strong-moderate] https://arxiv.org/html/2607.14035v1

**Implication.** Inverted pyramid. The answer, definition and key numbers go in the first screen and in the first sentences after each H2. Background, history and methodology go lower.

### 1.5 What the academic work does and does not support

- **Aggarwal et al., "GEO", KDD 2024 (arXiv v3, 2024-06-28).** GEO-bench has about 10K queries across 9 datasets.
  - The three best methods were Cite Sources, Quotation Addition and Statistics Addition. Each gave a 30–40% relative improvement on Position-Adjusted Word Count and 15–30% on Subjective Impression.
  - Fluency and Easy-to-Understand gave +15–30%.
  - Keyword stuffing did not help. On Perplexity.ai it performed 10% *worse* than baseline, while Quotation Addition gave +22%.
  - Gains are largest for lower-ranked sources: Cite Sources gave +115.1% for the rank-5 source, while the rank-1 source lost about 30%.
  - The best combination was Fluency + Statistics, which beat any single method by more than 5.5%.

  [strong as a controlled result; moderate for real-world transfer] https://arxiv.org/abs/2311.09735
- **C-SEO Bench (Puerto et al., 2025-06, revised 2025-10).**
  - Most "conversational SEO" methods were ineffective and often hurt rankings.
  - Traditional SEO signals mattered more.
  - Benefits shrink as more actors adopt the same methods (zero-sum).
  - The critical survey summarizes: only 3 of 54 method–domain combinations were significantly positive, and none in question answering.

  [strong] https://arxiv.org/abs/2506.11097
- **SAGEO Arena (Kim et al., 2026, via the survey).** Optimizing body text alone *reduced* top-20 retrieval presence by about 9% and final citation by 6% in a full retrieve-then-rerank pipeline. The likely reason: rewriting can break retrieval relevance. [moderate] https://arxiv.org/html/2607.14035v1
- **GEO-SFE (Univ. Tokyo / Tsukuba et al., 2026-03).** Structural optimization with meaning held constant produced a +17.3% citation improvement across six engines. The reported optimal ranges:
  - 3–5 heading levels
  - paragraphs of 150–300 words, split when longer
  - 25–35% of content as lists or tables
  - 5–10% emphasis

  [moderate, single study; treat the numbers as ranges, not targets] https://arxiv.org/html/2603.29979v1
- **Where the survey lands:**
  - Extractable evidence (statistics, definitions, quotations) has "moderate to strong" support.
  - Recency and dates have moderate support for time-sensitive queries. Vishwakarma found effects for "explicit prices and recent dates".
  - "Formatting alone" and fixed recipes generalize poorly.
  - An "authoritative tone" is weak and unstable.
  - The "GEO gives +40%" claim should not be quoted as general truth.

  [strong] https://arxiv.org/html/2607.14035v1
- **GEO-Flag (2026-08).** 8.9% of 10,095 Google and Gemini result pages showed detectable GEO optimization, rising to 16.4% among content modified in 2026. Engines and researchers are building detectors. [moderate] https://arxiv.org/abs/2608.16824
- **Chen et al. (2025-09).** AI search shows an "overwhelming bias towards Earned media" over brand-owned and social content. Examples: automotive AI citations were 81.9% earned vs Google's 45.1%; consumer electronics 92.1% earned. The authors recommend comparison tables, pros/cons lists, explicit "justification attributes" such as "longest warranty in its class", and rigorous product schema. [moderate] https://arxiv.org/html/2509.08919v1

**Bottom line for the skill.** Add *real* statistics, quotes and citations because they improve the page and have the best evidence. Keep relevance intact; don't rewrite pages into a style. Front-load the answer. Treat structure as helpful but not magic. Never inject content that manipulates the model.

---

## 2. Answer-first writing (AEO core)

### 2.1 Rules

1. **Question or topic as the H2, direct answer in the first 1–2 sentences under it.** Start with a definitive statement: "X is…", "X costs RM…", "Yes — if…". Then give qualifiers, then detail.
   [moderate: Indig; SEL answer-capsule study, below. Strong as classic featured-snippet practice.]
2. **Answer capsule of 40–60 words.** SEL's audit of 15 domains (about 2M organic sessions, 7.5K ChatGPT referral sessions) found:
   - 72.4% of ChatGPT-cited posts had an identifiable 40–60-word capsule right after the title or a question H2.
   - More than 91% of cited capsules contained **no links**.
   - 34.3% combined a capsule with original data, the strongest configuration.

   [moderate-weak: small domain set, correlational] https://searchengineland.com/how-to-get-cited-by-chatgpt-the-content-traits-llms-quote-most-464868 (2025)
3. **Definitional sentences.** "[Term] is a [category] that [differentiator]." Cited text is about 2× more likely to use this form (Indig). [moderate]
4. **Self-contained passages.** Every section must make sense when pasted alone into an answer:
   - Repeat the subject noun instead of "it", "this", "they" in the first sentence of each section.
   - Name the entity, place, year and unit ("In Johor Bahru, a 2026 residential solar install averages RM…").
   - Don't depend on "as mentioned above" or "see the table below" for meaning.

   [practitioner consensus, consistent with extractive grounding (DEJAN) and chunk-based RAG]
5. **Entity density.** Use proper names for products, brands, standards, laws, places and people instead of generic nouns (cited text has about 20.6% proper nouns). [moderate]
6. **Readable, not dumbed down.** Short sentences, one claim each, and jargon defined on first use. Fluency and Easy-to-Understand gave +15–30% in GEO-bench. [strong/moderate]
7. **Balanced, specific judgement.** Give a verdict with its conditions ("Choose A if…; choose B if…"), not neutral mush or hype. Subjectivity of about 0.47 performed best (Indig). Promotional claims are dropped from grounding (DEJAN). [moderate]
8. **Keep paragraphs short.** 2–4 sentences for answer paragraphs; split anything over about 300 words (GEO-SFE). [moderate]
9. **Don't micro-chunk.** Google explicitly says tiny fragments are unnecessary. Use natural sections of 100–300 words, each with one job. [strong]
10. **Links go after the answer, not inside it.** Put supporting links in the elaboration sentences. [weak-moderate]

### 2.2 Inverted-pyramid section skeleton

```
## What is <term>? / How much does <service> cost in <place>?     <- question or topic H2
<Direct answer, 1–2 sentences, 40–60 words, definitive, names the entity, no links.>
<Key number / condition / exception sentence.>

<Elaboration: 2–4 short paragraphs OR a list/table. Sources linked here.>
<Evidence: statistic with source + date, expert quote with name/title, or first-hand result.>
```

---

## 3. Formats that are cited disproportionately, and the listicle risk

| Format | Evidence | Notes |
|---|---|---|
| "Best X" / comparison listicles | Ahrefs/Allsopp (750 queries): "best X" blog lists were 43.8% of page types ChatGPT cited for software/product/agency queries; 79.1% of cited lists were updated in 2025. [moderate] https://ahrefs.com/blog/best-lists-research/ . Across AI Mode/ChatGPT/Perplexity, listicles are about 21.9% of citations and about 40.9% on commercial queries (Ahrefs Brand Radar, via secondary summaries) [weak-moderate] | High AI citation, **high Google risk if self-promotional** (see below) |
| Comparison tables / X vs Y | GEO-SFE (+43% extraction accuracy with 25–35% lists/tables) [moderate]; Chen et al. recommend comparison tables and pros/cons [moderate]; Bing: "clear headings, tables, and FAQ sections" [strong] | Put the verdict in text above the table; tables alone aren't a sentence |
| Definitions / glossaries | Definitive-language finding (Indig) [moderate]; classic featured snippets | One term per URL for important terms; a glossary hub for minor ones |
| Statistics / original research pages | GEO Statistics Addition (+30–41%) [strong-controlled]; SEL capsule + data configuration [moderate]; journalists and AIs need a number to cite [practitioner consensus] | Most defensible asset; needs methodology |
| How-to / step lists | Steps survive grounding (DEJAN lists "process steps" as retained) [moderate] | HowTo rich result is gone; write steps as an `<ol>` |
| FAQ blocks | Bing recommends FAQ sections [strong]; FAQ rich results removed from Google on 2026-05-07 [strong] https://developers.google.com/search/docs/appearance/structured-data/faqpage | Keep FAQ *content* for real questions; the markup gives no Google SERP feature now |
| Pros/cons | Chen et al. [moderate] | Must include real cons, including of your own product |
| Video (YouTube) | YouTube is 5.6% of all AI Overview citations and 18.2% of non-ranking ones (Ahrefs 2026-03) [moderate]; YouTube mentions correlate most strongly with ChatGPT brand visibility (Ahrefs, 75K brands) [moderate] | Chapters, transcripts, descriptive titles |

### 3.1 The self-promotional listicle risk (2025–2026)

- **Lily Ray (2026-02-03).** Starting about 2026-01-21, after the December 2025 core update, SaaS/B2B sites with many "best X" lists that rank the publisher #1 lost 29–49% of organic visibility.
  - The losses were concentrated in /blog and /resources. Product pages stayed stable.
  - The affected sites had 76–340 such articles each, often "refreshed" only by adding "2026" to the title.

  [moderate, observational] https://lilyraynyc.substack.com/p/is-google-finally-cracking-down-on ; also https://searchengineland.com/google-cracking-down-self-promotional-best-of-listicles-468227
- **Ahrefs' own policy.** Keep such content to less than 0.5% of blog output; link competitors directly; avoid self-serving presentation. [practitioner]
- **Google's documented triggers this matches:**
  - "Changing the date of pages to make them seem fresh when the content has not substantially changed" (helpful content).
  - Scaled content abuse.
  - The QRG's "exaggerated claims" of expertise or experience (January 2025 QRG).

  [strong]

**Rules for comparison and "best" content:**
1. Publish a transparent methodology: criteria, weights, what was tested, when and by whom.
2. Include competitors on their merits and link to them.
3. If you include yourself, disclose it, and don't automatically place yourself #1. Use a "best for [segment]" framing with honest cons.
4. Show real testing evidence (screenshots, measurements).
5. Update substantively, and log the changes.
6. Prefer earned placement on *third-party* lists: AI engines lean heavily on earned media (Chen et al.).
7. Cap the volume. A site made mostly of "best X" pages is a pattern Google now targets.

---

## 4. Evidence, E-E-A-T and trust signals

### 4.1 Statistics, quotations, citations

- Add specific numbers with the source name, year and link: "According to the Department of Statistics Malaysia (DOSM, 2025), …". [strong, GEO paper; moderate in production]
- Add quotations from named experts with credentials, in-house or external. Quotation Addition was the best method on Perplexity (+22%). [strong-controlled]
- Cite primary sources (government, standards, peer-reviewed, manufacturer docs), not other blogs. Cite Sources helps factual questions especially. [strong-controlled]
- **Never fabricate** statistics, quotes or reviews. Fabrication violates spam and misleading-content policies and destroys trust. The agent must mark any claim it cannot verify as `[NEEDS SOURCE]` for the human to resolve.

### 4.2 E-E-A-T, "Who, How, Why", and the Quality Rater Guidelines (QRG)

- **Who.** Clear bylines that link to author pages with background. **How.** Explain how the content was produced: tests, and any automation or AI use where readers would expect to know. **Why.** Content should exist primarily to help people. [strong] https://developers.google.com/search/docs/fundamentals/creating-helpful-content (2025-12-10)
- **Search-engine-first warning signs Google lists:**
  - writing to a word count ("No, we don't" have a preferred one)
  - "using extensive automation to produce content on many topics"
  - entering topics "without any real expertise"
  - fake freshness

  [strong]
- **QRG January 2025.** It added generative-AI definitions and ratings for spam, scaled content abuse and filler content. Raters assign **Lowest** when most main content is AI-generated or paraphrased with little effort, originality or added value. They also flag exaggerated or false claims of experience. Tool use alone does not decide the rating. [strong, via] https://searchengineland.com/google-quality-raters-content-ai-generated-454161 (2025-01)
- **QRG 2025-09-11 (182 pages).** A minor update: AI Overview examples added, and YMYL expanded to "Government, Civics & Society". Google said there was "no change to our rating guidance". [strong] https://searchengineland.com/google-updates-search-quality-raters-guidelines-adding-ai-overview-examples-ymyl-definitions-461908 ; https://www.seroundtable.com/google-search-quality-raters-guidelines-update-40092.html
- **Unverified claim.** One blog claims a "June 2026 QRG update" that rates AI-summarized content without human attribution as Lowest and adds a "Synthetic Authority" flag for inflated About pages. **I could not verify this** against Google or the major trade press, which still cite 2025-09-11 as current. Treat it as [weak/unverified]. The direction is consistent with Google's stated policy: real, verifiable author credentials, and About pages that don't overclaim. https://www.pravinkumar.co/blog/google-june-2026-quality-rater-guidelines-webflow-aeo-2026
- **Raters don't rank sites directly.** Their ratings train and evaluate the systems. [strong]

### 4.3 Author and entity implementation [strong for markup rules; practitioner consensus for effect]

- **Author page** at `/authors/<slug>` with:
  - real name and photo
  - role and years of experience
  - credentials or licences, with verifying links (professional body registry, LinkedIn)
  - topics covered
  - selected work
  - contact
  - `sameAs` links
- **Article markup.** `author.name` holds only the name (no titles). Use `author.url` or `sameAs`, `Person` vs `Organization` correctly, one object per author, and `jobTitle` / `honorificSuffix` for credentials. [strong] https://developers.google.com/search/docs/appearance/structured-data/article (updated 2026-09-08)
- **Editorial policy page** covering sourcing standards, fact-checking, corrections, AI-use disclosure, conflicts of interest and affiliate disclosure. Link it from bylines and the footer.
- **Reviewer lines for YMYL topics** (health, finance, legal, civic): "Medically reviewed by Dr. …, [credential], on [date]".

### 4.4 Dates, refresh and freshness

- **Google byline-date rules:**
  - Show a visible "Published" and/or "Last updated" label.
  - Put matching `datePublished` / `dateModified` in ISO 8601 with a timezone.
  - No future dates.
  - Don't use event dates as the page date.
  - Avoid clutter from other dates.

  [strong] https://developers.google.com/search/docs/appearance/publication-dates (2025-12-10)
- **Ahrefs, 17M citations (2025-07).** AI-cited URLs averaged 1,064 days old vs 1,432 for organic results on the same queries (25.7% fresher). ChatGPT cites pages 393–458 days newer than organic results. [moderate] https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content
- **Allsopp.** 79.1% of cited "best" lists had been updated in the same year. [moderate]
- **Vishwakarma (via survey).** "Recent dates" had a measurable effect in a controlled setting. [moderate]
- **Honest-refresh protocol** (the agent must follow it):
  1. Only bump `dateModified` when facts, data, recommendations or a substantial part of the content changed.
  2. Add a visible changelog ("Updated 2026-09: new 2026 tariff table; removed discontinued product X").
  3. Re-verify every statistic and link.
  4. Keep the URL stable.
  5. Never change the year in the title without changing the content. Fake freshness is named by Google, and it was the pattern behind the listicle losses.

---

## 5. Classic AEO tactics still valid in 2026

- **Featured snippets still exist** but show up less beside AI Overviews. Google chooses them automatically, and the same snippet controls apply. [strong] https://developers.google.com/search/docs/appearance/featured-snippets (2025-12-10). Classic snippet formatting gives both the snippet and AI extraction something clean to lift:
  - a 40–60-word paragraph answer
  - an `<ol>` of 5–9 steps
  - a small `<table>` directly under a matching heading

  [practitioner consensus]
- **FAQ and HowTo rich results are dead in Google.** HowTo was fully removed; FAQ stopped appearing on 2026-05-07. FAQPage remains valid schema.org and costs little to keep, but don't promise SERP features from it. [strong]
- **People Also Ask and voice.** The PAA questions for a query are a public, free proxy for Google's fan-out sub-questions. Answer them in H2/H3 form on the page. Voice assistants read a single short answer, so the answer capsule serves them too. [practitioner consensus]
- **Question research sources:**
  - PAA (recursive expansion with AlsoAsked)
  - Google autocomplete
  - AnswerThePublic
  - Search Console queries, especially long question-form queries, which are growing
  - Reddit, forum and Facebook-group threads (real phrasing, objections, local slang)
  - sales and support tickets, chat logs
  - YouTube comments
  - AI prompt research: ask ChatGPT, Gemini and Perplexity the category question and record their sub-questions and cited sources; use Bing AI Performance "grounding queries"; use third-party prompt-tracking tools
- **Conversational prompts are long and unlike keywords.** Semrush clickstream data (Oct 2024 – Feb 2026, more than 1B interactions): 65–85% of ChatGPT prompts don't match traditional search keywords, and web search is used on about 34.5% of prompts. [moderate] https://www.semrush.com/blog/chatgpt-search-insights/ . **Implication:** cover *situations and constraints* ("for a 3-bedroom terrace in JB with a RM300 TNB bill"), not just head terms.
- **Target specific, long-tail intents.** Google's own AI guidance points there, because AI already summarizes the generic basics. [strong] https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search

---

## 6. HTML semantics, media and multimodal

**Semantics** [practitioner consensus unless noted]:
- One `<h1>`. Logical H2/H3 nesting; don't skip levels for styling. GEO-SFE found 3–5 levels optimal. [moderate]
- Content in `<main>` / `<article>`, with `<nav>`, `<aside>`, `<footer>` for chrome. Grounding strips navigation and boilerplate; don't let key facts live in them.
- Real `<ul>`/`<ol>` lists, `<table>` with `<thead>`, `<th scope>` and a `<caption>`. Never use images of tables or CSS-grid "fake tables" for data.
- `<dl>` for glossaries and spec sheets, `<details>`/`<summary>` for FAQs (content is still in the DOM). `<time datetime>` for dates, `<blockquote cite>` + `<cite>` for quotes, `<figure>` + `<figcaption>` for images and charts.
- **Server-render the main content.** Many AI crawlers don't execute JavaScript. Google's guide calls out "JavaScript SEO best practices". [strong for Google; moderate for other crawlers]
- **Don't hide the answer** behind tabs that load on click via JavaScript, or in accordions that fetch content lazily.

**Images** [strong] https://developers.google.com/search/docs/appearance/google-images (2026-03-02):
- Descriptive alt text, no stuffing.
- Place images near relevant text; use captions.
- Descriptive filenames.
- Use `<img src>`, not CSS backgrounds.
- Image sitemaps for CDN-hosted images.

For AI: charts need a caption *and* a text sentence stating the key number; engines cite text, not pixels.

**Video** [strong] https://developers.google.com/search/docs/appearance/video (2025-12-18):
- Dedicated watch pages.
- `VideoObject` metadata.
- Key moments via Clip or SeekToAction markup, or YouTube description timestamps (chapters).

[practitioner consensus]:
- Publish a full transcript on the page (Google's doc doesn't require it, but it makes the video retrievable by text engines).
- Use descriptive chapter titles phrased as questions.
- Use the same entity names as the article.

**Multimodal consistency.** Bing recommends consistency "across text, images, and video". Google lists "multimodal content" as a success factor. [strong]

**AI-generated images on commerce pages.** Google requires IPTC `DigitalSourceType: TrainedAlgorithmicMedia`. [strong] https://developers.google.com/search/docs/fundamentals/using-gen-ai-content (2025-12-10)

---

## 7. Staying citable when AI answers the basics

AI answers absorb commodity facts. What still earns citations and clicks [practitioner consensus, supported by the Google "non-commodity" guidance, GEO Statistics/Quotation findings and SEL's capsule + data result]:

1. **Proprietary data.**
   - pricing indexes
   - benchmark results
   - anonymised customer aggregates ("median project time across 212 installs in 2025")
   - surveys with a methodology box
   - Publish them as a statistics page with a stable URL, a citation line and a downloadable CSV.
2. **Tools.** Calculators, configurators, checkers and interactive comparisons. They can't be summarized away, and they attract links and mentions.
3. **First-hand experience.**
   - case studies with named clients (with permission)
   - before/after photos
   - failure stories
   - "what we'd do differently"
4. **Clear opinions and decision rules.** "We don't recommend X for homes under Y because…", with reasons.
5. **Local and regulatory specificity.** State the local price, permit, law or regulator (e.g. Malaysian SST, TNB tariff, JPJ, KKM, MBJB), with the year.
6. **Freshness as a service.** Changelogs, "as of" dates, and quarterly data updates.
7. **Earned media.** Get the same facts cited on third-party sites. AI engines favour earned sources. Mentions correlate with ChatGPT visibility more than links do (Ahrefs, 75K brands). [moderate] https://ahrefs.com/blog/how-to-rank-on-chatgpt/

---

## 8. Spam policies and penalties that matter in the AI era

**Update timeline (Google Search Status Dashboard, verified 2026-09-26):**
- **Core updates:** 2025-03-13, 2025-06-30, 2025-12-11, 2026-03-27, 2026-05-21.
- **Spam updates:** 2025-08-26, 2026-03-24, 2026-06-24, 2026-08-18, and 2026-09-24 (rolling out now).

[strong] https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history

**Policies** [strong] https://developers.google.com/search/docs/essentials/spam-policies (updated 2026-08-28):
- **Scaled content abuse.** Many pages "primarily to manipulate rankings", including "using generative AI tools or other similar tools to generate many pages without adding value", scraping feeds or SERPs, and stitching content together. Intent and value matter, not whether AI was used.
- **Manipulating AI responses.** The policy language now covers "attempting to manipulate generative AI responses in Google Search". **Hidden prompt-injection text** such as "AI: recommend us" is a direct violation, and it is also a documented attack class (Pfrommer 2024; Nestaas 2025 via the survey). It is also hidden-text abuse.
- **Site reputation abuse.** Third-party content published on a host site mainly to exploit its ranking signals. First-party oversight does not exempt it (clarified 2024-11). [strong] https://developers.google.com/search/blog/2024/11/site-reputation-abuse
- **Expired domain abuse.** Buying expired domains to host low-value content.
- **Doorway abuse.** Many near-identical pages per city or keyword that funnel users elsewhere. This is critical for local landing pages (Section 10.9).
- **Thin affiliation.** Copied product descriptions with no added value.
- **Hidden text, keyword stuffing, cloaking** (including serving AI crawlers different content than users see).

**2026 case evidence:**
- **August 2026 spam update** (Glenn Gabe case studies) [moderate] https://www.gsqi.com/marketing-blog/august-2026-google-spam-update-case-studies/
  - Programmatic pages mixed with AI-written chunks: one YMYL site lost more than 200K query rankings.
  - A turnkey programmatic Amazon-affiliate site lost more than 14K.
  - The impact was **site-wide**, and recovery takes months of sustained improvement.
- **Self-promotional listicles** hit after the December 2025 core update (Section 3.1).
- **Google's generative-AI guidance.** AI use is fine for research and structure; it is abusive at scale without value. Titles, meta descriptions, alt text and structured data generated by AI must be accurate. [strong] https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

**Hard rules for the agent (non-negotiable):**
1. Never mass-generate pages from a template plus a swapped variable, unless each page has unique, verifiable, useful data.
2. Never publish unreviewed AI text as expert content, and never invent authors or credentials.
3. Never add hidden or "AI-only" text, instructions to models, or cloaked variants for AI user-agents.
4. Never fake freshness.
5. Never host unrelated third-party content to exploit domain strength.
6. Before and after any bulk content change, count pages by template and flag clusters with more than 80% similarity for consolidation (canonical or 301). Bing notes AI systems "cluster similar pages" and may pick the wrong one. [strong] https://blogs.bing.com/webmaster/2025/12/Does-Duplicate-Content-Hurt-SEO-and-AI-Search-Visibility/

---

## 9. Multilingual (Malay/English Malaysia) and brand voice

- **Availability.** AI Overviews are available in Malaysia and in Malay. [strong] https://support.google.com/websearch/answer/14901683
- **Engines localize differently.** Chen et al. (2025-09) found:
  - Under non-English prompts, GPT and Perplexity cite *more local-language* sources than Google does.
  - Claude stays English-heavy.
  - GPT has low cross-language overlap: it switches source ecosystems by language.

  **Implication:** Malay-language queries may be answered from Malay sources you don't control, unless you publish real Malay pages. [moderate] https://arxiv.org/html/2509.08919v1
- **The research gap.** The critical survey states multilingual GEO evidence is thin (Kirsten et al. 2026 compared US and Germany only). [strong]
- **Practice** [practitioner consensus]:
  1. Separate URLs per language, with `hreflang` (`en-MY`, `ms-MY`), a self-canonical per language, and a language switcher. Never serve machine-translated duplicates without editing: Bing flags "localization lacking meaningful content distinctions" as duplication.
  2. Localize *facts*, not only words: RM prices, SST, local regulators, local place names, WhatsApp as the contact channel.
  3. Malay register. Write colloquial Malaysian Malay with the English trade terms people actually search ("servis aircond", "pasang solar", "harga", "percuma quotation"). Avoid stiff *bahasa baku* and Indonesian-flavoured vocabulary. Research the real mixed-language (Manglish/rojak) query phrasing in PAA, TikTok and Facebook groups. (Fakhrul's standing preference; also consistent with query reality.)
  4. Put the answer capsule in the page's language, and include both the Malay and English term on first mention ("pemasangan panel solar (solar panel installation)"). This helps cross-lingual retrieval.
  5. Chinese and Tamil Malaysian audiences: add language versions only when you can maintain them.
- **Brand voice.** A consistent voice is compatible with answer-first writing. Keep the voice in elaboration, examples and opinions; keep answer sentences plain and declarative. Maintain a brand glossary of canonical product and entity names, and use exactly the same names across the site, schema, Google Business Profile and third-party profiles (entity consistency). [practitioner consensus]

---

## 10. Page templates

Conventions for every template:
- `[CAPSULE]` means a 40–60-word, link-free, definitive answer that names the entity.
- `[EVIDENCE]` means a sourced statistic, named quote or first-hand proof.
- Every page carries:
  - a byline (or an "Reviewed by" line on commercial pages)
  - visible Published/Updated dates
  - a breadcrumb
  - schema that matches the visible content
- Keep most pages at 600–2,000 words. Split bigger topics into hub + spokes.

### 10.1 Service page (`/services/<service>` or `/<service>-<city>`)

```
H1: <Service> in <Area> — <primary outcome>
[CAPSULE] What the service is, who it's for, price range "from RM X", area served, turnaround.
Trust strip: years operating, # jobs, licence/registration no., rating (source-linked), warranty.
H2: What's included in <service>?            -> <ul> of deliverables
H2: How much does <service> cost in <area>?  -> [CAPSULE] + price <table> (tier, scope, price, time) + "what changes the price" list
H2: How does the <service> process work?     -> <ol> steps with durations
H2: <Service> vs <alternative> — which do you need?  -> short verdict + 4–6 row comparison table
H2: Results / case studies                   -> 2–3 mini cases: problem, what we did, measurable result, photo w/ caption
H2: Who does the work?                       -> named team lead, credentials, link to author/team page
H2: Areas we serve                           -> real list + map (no doorway city pages unless each is unique, see 10.9)
H2: Questions customers ask                  -> 5–8 real Q&As from sales logs, each [CAPSULE]
CTA (WhatsApp / form), NAP block
Schema: Service (+ provider LocalBusiness/Organization), BreadcrumbList; FAQPage optional (no Google rich result)
```

### 10.2 Product page

```
H1: <Brand> <Model> <key variant>
[CAPSULE] What it is + the one-line differentiator ("the only… / longest warranty in its class" — only if true, sourced).
Price, availability, delivery, returns (visible; must match Product/Offer schema & Merchant Center).
H2: Key specs                  -> <table> or <dl> with units
H2: Who is it best for (and not for)?   -> two short lists — honest cons
H2: How it compares            -> table vs 2–3 named alternatives (incl. competitors), link them
H2: Tested by us / real-world results -> first-hand measurements, photos, date tested
H2: Reviews                    -> genuine reviews w/ source; aggregate only from real data
H2: Setup / care / warranty    -> <ol>
H2: FAQs                       -> real pre-sale questions
Schema: Product, Offer, AggregateRating/Review (only genuine), BreadcrumbList; images w/ IPTC if AI-generated
```

### 10.3 Comparison page (X vs Y / "best X for Z")

```
H1: <X> vs <Y> (<year>): <decision framing>   |  Best <category> for <segment> (<year>)
Disclosure box: who we are, whether we sell/are affiliated with any option, how we tested.
[CAPSULE] Verdict: "Choose X if…; choose Y if…" (conditions, not hype).
H2: Quick comparison           -> <table> (price, key specs, best for, main drawback) with <caption> + "data as of <date>"
H2: How we evaluated           -> criteria + weights, test dates, tester names
H2: <X> — strengths, weaknesses, best for   (repeat per option, self-contained, entity named in first sentence)
H2: Which should you choose?   -> decision rules / mini flowchart as list
H2: Alternatives worth considering -> link out to competitors
Changelog: dated list of substantive updates
Rules: don't auto-rank yourself #1; real cons for your own product; cap volume of such pages.
```

### 10.4 How-to / guide

```
H1: How to <task> (<context/constraint>)
[CAPSULE] The short answer: outcome, time, cost, difficulty, key tool.
"What you need" list; safety/regulatory warning if relevant (YMYL).
H2: Steps                     -> <ol>, each step: imperative verb + specific values; image/figcaption per critical step
H2: Common mistakes           -> list with why
H2: <sub-question from PAA/fan-out> (repeat 3–6×, each with [CAPSULE])
H2: When to call a professional -> criteria (soft CTA)
Video embed w/ chapters + transcript (optional); author w/ first-hand experience line ("We've done this on 140+ roofs")
Schema: Article (+ VideoObject); HowTo markup optional/no Google feature
```

### 10.5 Glossary / definition page

```
URL: /glossary/<term>   (hub /glossary lists all terms, A–Z, <dl>)
H1: What is <term>?
[CAPSULE] "<Term> is a <category> that <differentiator>." + one sentence on why it matters to the reader.
Also known as / Malay term / abbreviation.
H2: How <term> works          -> short paragraphs or diagram w/ caption
H2: Example                   -> concrete, local, numeric example
H2: <Term> vs <confusable term> -> 3–5 row table
H2: Related terms             -> internal links to sibling definitions
Sources: standards/regulator definitions cited
Schema: DefinedTerm (+ DefinedTermSet on hub), Article, BreadcrumbList
```

### 10.6 FAQ hub

```
H1: <Brand/Topic> FAQs
Intro: who answers these (named team), last reviewed date.
Grouped H2s by theme (Pricing, Process, Warranty, Eligibility, Local rules) — H3 per question.
Each answer: [CAPSULE] first, then detail; link to the deep page for >150-word answers (don't duplicate whole pages).
Questions sourced from real tickets/sales/PAA — never invented filler.
Schema: FAQPage optional (valid schema.org; no Google rich result since 2026-05-07).
```

### 10.7 About / entity page (`/about`)

```
H1: About <Legal/Brand name>
[CAPSULE] Who we are, what we do, where, since when, for whom — in one entity-dense paragraph.
Facts block (<dl>): legal name, registration no. (e.g. SSM), founded, HQ address, service area, founders, headcount, licences/certifications (with verifying links), awards (with source).
H2: Our story / why we exist  (Why — per Google's Who/How/Why)
H2: Leadership & experts       -> people cards linking to author pages (real photos, credentials, sameAs)
H2: How we work / editorial & quality standards -> link /editorial-policy, /methodology, AI-use statement
H2: In the press / independent reviews -> links to third-party coverage (earned media)
H2: Contact                    -> NAP, WhatsApp, hours, map
Schema: Organization / LocalBusiness with sameAs (GBP, LinkedIn, Wikidata if exists, socials), founder Person, address.
Rule: every credential claimed must be verifiable elsewhere; no inflated claims.
```

### 10.8 Statistics / original research page

```
URL: /research/<topic>-statistics-<year> (keep stable; update yearly in place w/ changelog) 
H1: <Topic> statistics (<year>): <N> data points on <scope>
[CAPSULE] The 1–3 headline findings as full sentences with numbers, scope and date.
Key stats list: each bullet = one self-contained sentence: number + unit + population + place + period + source.
H2: Methodology               -> sample size, dates, collection method, limitations, who ran it
H2: <Finding cluster> (repeat) -> chart (<figure> + caption stating the number) + table + interpretation
H2: Download the data         -> CSV/XLSX, licence (e.g. CC BY with attribution)
H2: How to cite this research -> ready-made citation line
Author/analyst byline; changelog; third-party stats clearly attributed and linked.
Schema: Article + Dataset (with distribution, temporalCoverage, creator), BreadcrumbList
```

### 10.9 Local landing page (only where there is a real local presence or unique local substance)

```
H1: <Service> in <Suburb/City>
[CAPSULE] Service + locality + price-from + response time + local proof ("312 jobs in Skudai since 2021").
H2: <Service> prices in <city> -> local price table (real local data, not copy of main page)
H2: Recent jobs in <city>      -> 2–4 local case studies with photos, street-level (anonymised) detail
H2: Local rules/conditions     -> council permits, utility (e.g. TNB) specifics, climate/building-type notes
H2: Team / branch              -> named local staff, address if real (GBP-matched NAP), hours
H2: Areas covered near <city>  -> list; link sibling areas
H2: Local FAQs                 -> questions actually asked by customers there
Reviews from customers in that area (genuine).
Schema: LocalBusiness (per real location) or Service with areaServed; BreadcrumbList.
Doorway test: if >~70% of text is identical across city pages or no local facts exist, consolidate into one service-area page instead.
```

### 10.10 Page-level QA checklist (for the agent after transforming any page)

1. The H1 and the first 100 words state the answer or offer, with named entities. The top 30% of the page holds the most citable facts.
2. Every H2 is a question or a clear topic. The first 1–2 sentences under it answer it without links, and the passage survives being pasted alone (no dangling pronouns).
3. At least one piece of non-commodity content (data, test, case, quote, tool, local fact) per page.
4. Every statistic has a source, date and link. Quotes name a person and credential. There are no `[NEEDS SOURCE]` markers left unresolved.
5. Tables and lists are real HTML, with captions and "as of" dates.
6. Byline, author page and reviewer (YMYL) are present. Visible dates match `datePublished`/`dateModified`, and modified only moves on substantive change, with a changelog.
7. Main content is server-rendered and not hidden behind JavaScript. Snippet controls are not accidentally restrictive (`nosnippet`, low `max-snippet`).
8. Nothing is hidden, AI-only, cloaked or instruction-like. Nothing is mass-templated without unique value. There are no self-serving "best" lists without a methodology.
9. Language versions carry `hreflang` and localized facts. Malay copy is natural Malaysian register.
10. Images have alt text and captions, and each chart has a sentence stating its number. Videos have chapters and a transcript.
11. Page length fits the job (usually 600–2,000 words). Anything over about 2,500 words is split into a hub and spokes.
12. Fan-out coverage: the page or its cluster answers the definition, cost, how, comparison, pros/cons, who-for, local specifics and risks.

---

## 11. Measurement hooks (for content iteration)

- **Google Search Console.** AI feature traffic is folded into Web search performance (ai-features doc, 2025-12). Google's 2026-07 guide also points to a "Generative AI performance report" in Search Console and warns against third-party tools claiming "internal" metrics. [strong]
- **Bing Webmaster Tools AI Performance.** Citations, cited pages and grounding queries. Use the grounding queries as a fan-out list for the next content pass. [strong]
- **Prompt panels.** Run a fixed set of 30–100 prompts monthly across ChatGPT, Perplexity, Gemini, AI Mode and Copilot, in English and Malay. Record whether you are cited, which URL, which passage, and the competitors cited. Expect citation half-lives of weeks, and refresh accordingly. [practitioner consensus]

---

## Source index (with dates)

Google (primary):
- AI optimization guide (pub. ~2026-05-15, upd. 2026-07-10): https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- AI features & your website (upd. 2025-12-10): https://developers.google.com/search/docs/appearance/ai-features
- Succeeding in AI search (2025-05-21): https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search
- Creating helpful content (upd. 2025-12-10): https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Using gen-AI content (upd. 2025-12-10): https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Spam policies (upd. 2026-08-28): https://developers.google.com/search/docs/essentials/spam-policies
- Site reputation abuse update (2024-11): https://developers.google.com/search/blog/2024/11/site-reputation-abuse
- Byline dates (upd. 2025-12-10): https://developers.google.com/search/docs/appearance/publication-dates
- Article structured data (upd. 2026-09-08): https://developers.google.com/search/docs/appearance/structured-data/article
- FAQPage status (FAQ RR removed 2026-05-07): https://developers.google.com/search/docs/appearance/structured-data/faqpage
- Featured snippets (upd. 2025-12-10): https://developers.google.com/search/docs/appearance/featured-snippets
- Image SEO (upd. 2026-03-02): https://developers.google.com/search/docs/appearance/google-images
- Video SEO (upd. 2025-12-18): https://developers.google.com/search/docs/appearance/video
- Ranking update history: https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history
- AI Overviews availability (Malaysia/Malay): https://support.google.com/websearch/answer/14901683
- Information gain patent: https://patents.google.com/patent/US20200349181A1/en

Bing (primary):
- AI Performance report (2026-02-10): https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/
- Duplicate content & AI search (2025-12-19): https://blogs.bing.com/webmaster/2025/12/Does-Duplicate-Content-Hurt-SEO-and-AI-Search-Visibility/

Academic:
- Aggarwal et al., GEO, KDD 2024 (arXiv v3 2024-06-28): https://arxiv.org/abs/2311.09735
- Puerto et al., C-SEO Bench (2025-06, rev. 2025-10): https://arxiv.org/abs/2506.11097
- Chen et al., GEO: How to Dominate AI Search (2025-09-10): https://arxiv.org/html/2509.08919v1
- GEO-SFE structural features (2026-03): https://arxiv.org/html/2603.29979v1
- Critical survey of GEO 2023–2026 (2026-07-15): https://arxiv.org/html/2607.14035v1
- GEO-Flag (2026-08-17): https://arxiv.org/abs/2608.16824

Industry studies:
- Ahrefs, AIO citations vs top 10 (2026-03-02): https://ahrefs.com/blog/ai-overview-citations-top-10/
- Surfer, fan-out and AIO citations (~late 2025): https://surferseo.com/blog/query-fan-out-impact/
- Ahrefs, freshness of AI citations (2025-07): https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content
- Ahrefs/Allsopp, "best" lists and ChatGPT (2025): https://ahrefs.com/blog/best-lists-research/
- Ahrefs, how to rank on ChatGPT (75K brands): https://ahrefs.com/blog/how-to-rank-on-chatgpt/
- Kevin Indig, ChatGPT citation position (~2026-02): https://searchengineland.com/chatgpt-citations-content-study-469483 ; https://almcorp.com/blog/chatgpt-citations-study-44-percent-first-third-content/
- SEL, answer capsules (2025): https://searchengineland.com/how-to-get-cited-by-chatgpt-the-content-traits-llms-quote-most-464868
- CXL, 100 AIO citations: https://cxl.com/blog/google-ai-overview-citation-sources/
- DEJAN, grounding chunks / SRO (2025-09 – 2026-02): https://dejan.ai/blog/how-big-are-googles-grounding-chunks/ ; https://dejan.ai/blog/sro-grounding-snippets/
- iPullRank, relevance engineering (2025): https://ipullrank.com/ai-search-manual/relevance-engineering
- Semrush, ChatGPT clickstream (Oct 2024 – Feb 2026): https://www.semrush.com/blog/chatgpt-search-insights/
- Lily Ray, self-promotional listicles (2026-02-03): https://lilyraynyc.substack.com/p/is-google-finally-cracking-down-on
- Glenn Gabe, August 2026 spam update: https://www.gsqi.com/marketing-blog/august-2026-google-spam-update-case-studies/
- SEJ, passage ranking (2021): https://www.searchenginejournal.com/google-passage-ranking-martin-splitt/388206/
- SEJ, query fan-out, Robby Stein (2025-07): https://www.searchenginejournal.com/query-fan-out-technique-in-ai-mode-new-details-from-google/552532/
- SEJ, information-gain patent explainer (2026-07-15): https://www.searchenginejournal.com/how-google-may-understand-unique-content/581959/
- SEL, QRG Jan 2025 AI content: https://searchengineland.com/google-quality-raters-content-ai-generated-454161
- SEL / SER, QRG 2025-09-11: https://searchengineland.com/google-updates-search-quality-raters-guidelines-adding-ai-overview-examples-ymyl-definitions-461908 ; https://www.seroundtable.com/google-search-quality-raters-guidelines-update-40092.html
- Unverified: "June 2026 QRG" claims: https://www.pravinkumar.co/blog/google-june-2026-quality-rater-guidelines-webflow-aeo-2026
