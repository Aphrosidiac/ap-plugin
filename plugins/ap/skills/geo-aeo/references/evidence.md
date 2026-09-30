# Evidence ledger — what moves AI citation, what doesn't, and how sure we are

State as of 2026-09-26. Full studies, sample sizes and URLs: `research/01-evidence.md`
(academic + industry), `research/05-content-engineering.md` §1, `research/06-offsite-authority.md` §1–3.
Re-check anything marked volatile before quoting it to an owner.

Tags: **[strong]** = controlled evidence and observational evidence agree, or a platform's own
documentation says so · **[moderate]** = large observational study or one controlled study ·
**[weak]** = small, vendor-only, or contradicted · **[myth]** = rejected by the platform or by replication.

---

## The model in one paragraph

An answer engine is a retrieval pipeline: activation (does it search at all?) → retrieval
(which pages enter the candidate pool, driven by the engine's index and its fan-out
sub-queries) → reranking → generation (which passages get used) → citation → click. **Almost
everything that matters happens at retrieval**, and retrieval runs on classic search signals:
crawlability, indexation, relevance to the sub-query, authority. Content tricks act only on
the last stages and only once you are already in the pool. So: get in the pool first (P0–P1
of the plan), then make the page easy to extract and worth citing (P2–P3), then earn the
third-party consensus that decides recommendations (P6).

## Ranked conclusions

### Strong
1. **No retrieval, no citation; retrieval is classic SEO.** Moving a document to the top of
   the context beat all 10 content-rewrite methods (C-SEO Bench 2025). Citation rate is 58% at
   ChatGPT retrieval position 1 vs 14% at position 10 (AirOps 2026). Referring domains and
   community presence predicted startup discovery by LLMs; "GEO optimization" did not
   (Sharma 2026).
2. **Google needs nothing AI-specific.** AI Overviews / AI Mode eligibility = indexed +
   snippet-eligible. No llms.txt, no special schema, no chunking, no special writing style,
   no ideal length (Google AI features doc 2025-12-10; AI optimization guide 2026-07-10).
3. **Keyword stuffing hurts** (−8% GEO-bench, worse on Perplexity).
4. **Clicks fall when an AI summary shows; being cited softens the fall.** Pew: 15% → 8% of
   visits click a result; 1% click inside the summary. Seer: cited brands get ~2.07% CTR vs
   0.94% uncited on the same AIO queries.
5. **Answers are stochastic.** <1% chance of the same brand list twice (SparkToro, 2,961
   runs); 15% of citation decisions flip on re-decoding. Measure rates over many runs.
6. **Engines cite different ecosystems.** Only 12% of URLs cited by ChatGPT/Gemini/Copilot/
   Perplexity rank in Google's top 10 for the prompt; engine-to-engine overlap is low.

### Moderate
7. **Real, specific, sourced evidence gets cited and absorbed**: statistics with a source,
   attributed quotes, definitions, comparisons, procedural steps, prices, specs. Invented or
   LLM-padded statistics *hurt* (19/24 settings in C-SEO Bench).
8. **Real freshness matters**, strongest for time-sensitive and commercial queries. LLM
   rerankers move dated passages up to 95 ranks; AI-cited pages are ~26% fresher than organic
   results. A recent *and true* date helps; a fake bump is spam.
9. **Front-loaded, query-matching answers get cited more.** 44% of ChatGPT citations come from
   the first 30% of a page; headings that closely match the query are cited 41% vs 29%.
10. **Off-site mentions predict AI visibility more than backlinks.** Branded web mentions
    ρ≈0.66, YouTube mentions ρ≈0.74, backlinks ρ≈0.22–0.30 (Ahrefs, 75k brands). Earned media
    is 82–89% of AI citations (Muck Rack). Correlational; inauthentic mentions don't count.
11. **Titles, headings and meta fields matter at the retrieval stage; body-only rewrites can
    hurt.** Structural-field optimization +22% retrieval; body-only GEO rewriting −9%
    retrieval, −6% citation (SAGEO Arena 2026).
12. **Fan-out coverage predicts AI Overview citation** (ρ≈0.77 between the number of fan-out
    sub-queries a page ranks for and its citation likelihood; Surfer). Only ~38% of AIO
    citations rank top-10 for the head query (Ahrefs, Mar 2026).
13. **Decision-critical specifics are gatekeepers for commercial prompts**: price not
    mentioned, missing specs, no comparison, hedged language and internal contradictions all
    lose the citation (252,000-trial study, SIGIR 2026).

### Weak
14. "Authoritative / persuasive tone" — no significant effect; promotional rewrites score
    negative.
15. Fluency/readability rewrites — helped GPT-3.5, not significant with modern models. Write
    clearly for humans; don't rewrite for a readability score.
16. **Schema lifts AI citation** — no. Ahrefs diff-in-diff (1,885 pages): AIO −4.6%, AI Mode
    and ChatGPT ≈ 0. Live-fetching assistants ignore JSON-LD; a price only in JSON-LD was found
    by none of five engines. Keep schema for rich results, merchant listings and entity
    clarity. Microsoft alone says schema helps its LLMs understand content.
17. Citation → traffic/revenue causality — unproven. Measure per site.

### Myth — never recommend, never promise
- **"GEO boosts visibility 40%."** One metric, GPT-3.5, fixed 5-document context; the same
  methods *cost* the rank-1 source 20–30%. Only 3/54 method-domain cells replicated.
- **llms.txt as a citation/ranking lever.** 300k domains: no relationship. 97% of llms.txt
  files got zero requests in May 2026; Slackbot fetched them more than PerplexityBot. Google
  Search ignores it. It is a cheap courtesy for coding agents — nothing more.
- **Chunking pages into bite-sized pieces for LLMs.** Google: "We don't want you to do that."
  Clear sections help; fragmenting a page into micro-pages is scaled-content risk.
- **Word-count / "optimal passage length" targets.** No defensible number exists.
- **FAQ schema for AI citation or rich results.** FAQ rich results ended 2026-05-07; no lift
  in any study.
- **Hidden text / prompt injection / "note to AI" / "Summarize with AI" persuasion links.**
  Work in labs, are defended against in production, and are spam under Google's policy
  (updated 2026-08-28). Microsoft caught 31 companies doing it in 60 days.
- **Rank tracking "position in ChatGPT."** Order is near-random per run.
- **Optimising third-party authority scores (DA/DR).** Google: third-party tools have no
  access to its ranking data.

## Conflicts, resolved (use these readings)

| Question | Reading to use |
|---|---|
| Do statistics help? | Real, sourced numbers that answer the query: yes. Inserted/padded numbers: no, they hurt. |
| AIO citations vs top-10 rank (76% → 38% → 17%?) | Definitions differ. Direction is settled: ranking helps a lot, but most citations come from fan-out sub-queries, so cover the cluster, not just the head term. |
| Backlinks: strong or useless? | Different stages. Authority gets you into the candidate pool; once retrieved, page-level relevance decides. Both true. |
| Long or short pages? | No target. Answer the question completely, front-load it, split distinct intents into separate pages (hub + spokes). Google grounding uses ~2,000 words per query across sources, and coverage of a page falls from 61% (<1k words) to 13% (>3k). |
| Does formatting matter? | Visual formatting barely moves the model once the page is in context. Query-shaped headings, titles and metadata move retrieval. Tables/lists help extraction and humans. |
| Freshness | Real bias. Honest updates with visible dates. Never bump dates without substantive change. |
| Reddit share of citations | Volatile (ChatGPT: ~60% → ~10% of responses in Sep 2025; 3.8% → 0.5% of citations in Aug 2026). Never make one platform the plan. |
| Google says "just SEO"; Bing says "structure for AI" | Both hold. Write self-contained, well-headed sections (helps Bing/Perplexity/Brave passage retrieval) without fragmenting pages or making AI-only variants (Google scaled-content risk). |

## What you may tell an owner (and what you may not)

May say: "These changes remove the reasons engines can't or won't use your pages, and put
the facts they need in a form they extract. Effects show first in crawl logs and Bing/
Perplexity citations (days–weeks), then Google AI surfaces (weeks), and only slowly in
models' built-in knowledge (model generations). We'll measure mention and citation rates
with confidence intervals before and after."

Never say: a percentage uplift; "rank #1 in ChatGPT"; that llms.txt or schema will get them
cited; that any tactic is guaranteed; that AI traffic will convert at N× (studies range from
−13% to 23×).
