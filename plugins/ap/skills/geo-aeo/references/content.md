# Content engineering — pages engines extract, trust and cite (AEO + GEO + SEO)

Evidence, studies and dates: `research/05-content-engineering.md` (and `01-evidence.md`).
The page skeletons in §8 are the ones to transform pages into.

**The governing rule: every change must make the page better for a human reader. If a change
exists only "for the AI", don't make it.** Google now treats manipulating AI answers as spam;
replication studies show generic GEO rewrites fail or cancel out; and body-only rewrites can
*lower* retrieval. What works is the structure good technical writers always used.

---

## 1. How a page gets used

Engines retrieve **passages**, not pages: fan-out sub-queries → candidate passages
(embeddings + lexical) → rerank → the generator lifts sentences under a budget (Google
grounding ≈ 2,000 words per query across all sources; the #1 source gets ~28%; a page under
1,000 words has ~61% of its text used, over 3,000 words ~13%). Text that survives: value
propositions, specific features, prices, steps, definitions, numbers. Text that's dropped:
navigation, promotional claims, boilerplate, verbose reviews.

So: **density over length, answer before context, one job per section, entity names over
pronouns, real numbers over adjectives.**

## 2. Answer-first rules (the AEO core)

1. **Question or topic as the heading; the direct answer in the first 1–2 sentences under
   it.** Definitive form: "X is a [category] that [differentiator].", "X costs RM… in…",
   "Yes — if…". Then conditions, then detail.
2. **Answer capsule ≈ 40–60 words, link-free**, naming the entity (72% of ChatGPT-cited posts
   had one; >90% of cited capsules had no links). Put links in the elaboration.
3. **Self-contained sections.** Each section must make sense pasted alone into an answer:
   repeat the subject noun in the first sentence (not "it/this/they"), name place, year and
   unit, never rely on "as mentioned above" or "the table below" for meaning.
4. **Front-load the page.** The H1 and first ~100 words state the answer/offer with named
   entities; the most citable facts sit in the top 30%.
5. **Entity density.** Proper names for products, standards, laws, places, people (cited text
   ≈ 20% proper nouns vs 5–8% typical).
6. **Decisive, conditional verdicts** ("Choose A if…; choose B if…") — not hype, not mush.
   Hedging and internal contradictions lose citations in controlled tests.
7. **Short paragraphs** (2–4 sentences); split sections over ~300 words; natural sections of
   ~100–300 words. **Don't micro-chunk** into fragments or separate micro-pages.
8. **Headings mirror real questions and sub-queries** (query-matching headings: 41% vs 29%
   cited). Logical H1→H2→H3 nesting, one H1.

Section skeleton:
```
## How much does <service> cost in <place>?          ← question-shaped heading
<Capsule: 40–60 words, definitive, entity-named, no links.>
<The key number / condition / exception sentence.>
<Elaboration: 2–4 short paragraphs, or a list/table. Sources linked here.>
<Evidence: sourced statistic with date, named expert quote, or first-hand result.>
```

## 3. Evidence and originality

- Add **real** statistics with source name, year and link ("According to DOSM (2025), …"),
  **attributed** expert quotes (name, credential), and citations to **primary** sources
  (government, standards bodies, peer-reviewed, manufacturer docs).
- **Never fabricate** a statistic, quote, review, author, credential, customer or date. When
  a claim needs a source you don't have, write `[NEEDS SOURCE: what]` and list it for the
  owner. Leftover markers block "done".
- Every important page carries at least one **non-commodity element** a competitor can't copy
  by paraphrase: original data, a test result, photos of your own work, a named expert quote,
  a real price table, a worked local example, a decision rule, a tool/calculator.
- What stays citable when AI answers the basics: proprietary data (with methodology and a
  downloadable CSV), tools, first-hand case studies, clear opinions with reasons, local and
  regulatory specifics with the year, freshness as a service (changelogs, "as of" dates).

## 4. Formats that get cited — and the listicle trap

| Format | Use |
|---|---|
| Comparison tables / X vs Y | Verdict in text above the table; real `<table>` with `<caption>` and "data as of"; name and link competitors |
| "Best X for Y" lists | ~44% of ChatGPT-cited page types — **and** self-promotional ones lost 29–49% of Google visibility after the Dec 2025 core update. Rules below |
| Definitions / glossary | One URL per important term; hub for minor ones |
| Statistics / original research | The most defensible asset; needs methodology, stable URL, citation line |
| How-to steps | Real `<ol>`; HowTo rich result is gone but steps survive grounding |
| FAQ blocks | Real questions from sales/support/PAA; answer capsule first; no Google rich result |
| Pros/cons | Include real cons, including your own product's |
| Video | YouTube is the #1 AIO-cited domain; long-form, chapters, transcripts, brand said aloud |

**"Best X" / comparison rules:** published methodology (criteria, weights, dates, testers);
competitors included on merit and linked; disclosure if you're on the list; don't auto-rank
yourself #1 — use "best for [segment]" with honest cons; real testing evidence; substantive
dated updates (never just "2026" in the title); cap the volume. Prefer *earned* placement on
third-party lists (see `offsite-authority.md`).

## 5. Trust: E-E-A-T, authorship, dates

- **Who / How / Why** (Google): bylines linking to author pages with real credentials; how the
  content was produced (testing, and AI use where readers would expect to know); exists to
  help people. Trust is the most important part. E-E-A-T is not a ranking factor itself —
  raters' judgments train the systems.
- Author page: real name, photo, role, years, verifiable credentials/licences, topics, selected
  work, contact, sameAs. Editorial policy page (sourcing, fact-checking, corrections, AI use,
  conflicts, affiliate disclosure) linked from bylines and footer.
- YMYL (health, finance, legal, civic): named credentialed reviewer + last-reviewed date, visible.
- **Dates**: visible "Published" / "Updated" labels + matching `datePublished`/`dateModified`
  (ISO 8601 + timezone). **Honest-refresh protocol:** bump `dateModified` only when facts,
  data, recommendations or a substantial part changed; add a visible changelog line; re-verify
  every statistic and link; keep the URL; never change the year in a title without changing
  the content (fake freshness is named by Google and was the pattern behind the listicle losses).

## 6. HTML semantics and media

- Content in `<main>`/`<article>`; chrome in `<nav>`/`<aside>`/`<footer>` (grounding strips it —
  no key facts there). Real lists and tables (`<thead>`, `<th scope>`, `<caption>`), `<dl>` for
  specs/glossaries, `<details>` for FAQs (content stays in the DOM), `<time datetime>`,
  `<blockquote cite>`, `<figure>` + `<figcaption>`.
- Never images of tables or CSS "fake tables" for data. Charts need a caption **and** a
  sentence stating the key number — engines cite text, not pixels.
- Images: `<img>` not CSS backgrounds, descriptive alt, descriptive filenames, near relevant
  text, width/height. AI-generated product images need IPTC `DigitalSourceType`.
- Video: dedicated watch pages, VideoObject, chapters (key moments), on-page transcript.
- Answers must not live only in client-loaded tabs, accordions, PDFs or images.

## 7. Coverage: fan-out and question research

For each target query, list what a planner would fan out to: definition · how it works · cost/
price · comparison vs alternatives · pros/cons · who it's for / not for · steps · risks ·
local/regulatory specifics · what changed recently · troubleshooting. Give each its own heading
on the pillar, or a linked child page when it needs >~300 words (hub + spokes). Cover intents
and facts, not phrasing variants — **never near-duplicate pages per keyword variant**.

Question sources: People Also Ask (AlsoAsked), autocomplete, GSC long question queries, BWT
grounding queries, ai_visibility.py fan-out queries, Reddit/Facebook-group phrasing, sales and
support logs, YouTube comments. Conversational prompts are long and situational (65–85% don't
match keywords): cover constraints ("for a 3-bedroom terrace in JB with a RM300 TNB bill").

## 8. Page skeletons

Every page: byline or "Reviewed by", visible Published/Updated dates, breadcrumb, schema that
matches visible content, 600–2,000 words typical (split bigger topics). `[CAPSULE]` = 40–60
words, link-free, definitive, entity-named. `[EVIDENCE]` = sourced stat, named quote or
first-hand proof.

**Service page** — H1 `<Service> in <Area> — <outcome>` · [CAPSULE] what, for whom, "from RM X",
area, turnaround · trust strip (years, jobs, licence no., rating with source, warranty) · H2
What's included (list) · H2 How much does it cost in <area>? (capsule + price table + what
changes the price) · H2 How the process works (ol with durations) · H2 <Service> vs
<alternative> (verdict + table) · H2 Results (2–3 mini cases: problem → what we did → measured
result → captioned photo) · H2 Who does the work (named lead, credentials) · H2 Areas we serve
(no doorway pages) · H2 Questions customers ask (5–8 real, each capsule-first) · CTA + NAP.
Schema: Service + provider, BreadcrumbList.

**Product page** — H1 `<Brand> <Model> <variant>` · [CAPSULE] + one true, sourced
differentiator · visible price, stock, delivery, returns (= schema = feed) · H2 Key specs
(table/dl with units) · H2 Best for / not for (honest) · H2 How it compares (table vs 2–3 named
alternatives) · H2 Tested by us (measurements, photos, test date) · H2 Reviews (genuine, server-
rendered) · H2 Setup/care/warranty · H2 FAQs. Schema: Product/Offer (+ genuine ratings).

**Comparison page** — H1 `<X> vs <Y> (<year>): <decision>` · disclosure box · [CAPSULE] verdict
with conditions · H2 Quick comparison (table, "as of" date) · H2 How we evaluated · H2 per
option (strengths, weaknesses, best for — entity named in first sentence) · H2 Which should you
choose? (decision rules) · H2 Alternatives (link out) · changelog.

**How-to** — H1 `How to <task> (<context>)` · [CAPSULE] outcome, time, cost, difficulty, key
tool · what you need + safety/regulatory warning · H2 Steps (ol, imperative + specific values,
figure per critical step) · H2 Common mistakes · 3–6 H2 fan-out sub-questions (capsule each) ·
H2 When to call a professional · video with chapters + transcript.

**Glossary term** — `/glossary/<term>` · H1 `What is <term>?` · [CAPSULE] "<Term> is a <category>
that <differentiator>." + why it matters · aka / Malay term / abbreviation · H2 How it works ·
H2 Example (concrete, local, numeric) · H2 <Term> vs <confusable> (table) · H2 Related terms ·
sources. Schema: DefinedTerm (+ DefinedTermSet on the hub).

**FAQ hub** — H1 `<Brand> FAQs` · who answers, last reviewed · themed H2s, H3 per question ·
capsule first; link to the deep page for answers >150 words (don't duplicate pages) · questions
from real tickets/sales/PAA only.

**About / entity page** — H1 `About <name>` · [CAPSULE] who, what, where, since when, for whom ·
facts block (`<dl>`: legal name, registration no. e.g. SSM, founded, HQ, service area,
founders, headcount, licences with verifying links, awards with sources) · H2 Our story (why) ·
H2 Leadership & experts (links to author pages) · H2 How we work / standards (editorial
policy, methodology, AI-use statement) · H2 In the press / independent reviews (links out) ·
H2 Contact (NAP, WhatsApp, hours, map). Every credential verifiable elsewhere; no inflation.

**Statistics / research page** — `/research/<topic>-statistics-<year>` (stable, updated in
place with changelog) · H1 `<Topic> statistics (<year>): <N> data points on <scope>` · [CAPSULE]
1–3 headline findings with numbers, scope, date · key-stats list (each bullet one self-
contained sentence: number + unit + population + place + period + source) · H2 Methodology
(sample, dates, method, limitations, who) · finding clusters (figure + caption stating the
number + table + interpretation) · H2 Download the data (CSV, licence) · H2 How to cite.
Schema: Article + Dataset.

**Local landing page** (only with a real local presence or unique local substance) — H1
`<Service> in <Suburb>` · [CAPSULE] service + locality + price-from + response time + local
proof ("312 jobs in Skudai since 2021") · H2 prices in <city> (real local data) · H2 recent jobs
there (2–4 cases, photos) · H2 local rules/conditions (council, utility, climate, building
type) · H2 team/branch (named staff, GBP-matched NAP, hours) · H2 nearby areas · local FAQs ·
local reviews. **Doorway test:** >~70% identical text across city pages or no local facts →
consolidate into one service-area page.

## 9. Hard rules (non-negotiable)

1. No mass-generated pages from a template + swapped variable unless each has unique,
   verifiable, useful data (scaled content abuse; August 2026 spam update hit such sites
   site-wide).
2. No unreviewed AI text presented as expert content; no invented authors or credentials.
3. No hidden, "AI-only", instruction-like or cloaked content — scan for and **remove** any
   that exists (plugins and agencies add it; audit.py flags it).
4. No fake freshness.
5. No hosting third-party content to exploit the domain (site reputation abuse — fully
   enforced outside the EEA).
6. Before and after bulk changes, count pages per template and flag >80%-similar clusters for
   consolidation (301 or canonical).
7. **Don't rewrite pages that are already cited or ranking #1 wholesale** — GEO rewrites cost
   the top-ranked source 20–30% in the original study. Improve them surgically (add the
   missing capsule, evidence, date, table) and measure.
8. Preserve the brand voice in elaboration and examples; keep answer sentences plain.

## 10. Multilingual (Malaysia)

AI Overviews and AI Mode run in Malay. Engines localise sources differently, and one test got
Indonesian back for 66% of Malay prompts — so publish **real Malay pages** with their own URLs
and `hreflang="ms-MY"` (never `my`). Write colloquial Malaysian Malay with the English trade
words people actually type ("servis aircond", "harga", "percuma quotation"), not *bahasa baku*
and never Indonesian vocabulary (false friends: *percuma* = free in MY / useless in ID;
*kereta* = car / train). Localise facts (RM, SST, local regulators, place names, WhatsApp).
Put both terms on first mention ("pemasangan panel solar (solar panel installation)").
Unreviewed machine translation at scale is scaled-content risk. Add Chinese/Tamil only when
they can be maintained.

## 11. Page QA checklist (run after transforming any page)

1. H1 + first 100 words state the answer/offer with named entities; best facts in top 30%.
2. Every H2 is a question or clear topic; first 1–2 sentences answer it without links;
   passages survive being pasted alone.
3. ≥1 non-commodity element.
4. Every stat sourced + dated + linked; quotes named; zero `[NEEDS SOURCE]` left.
5. Real HTML tables/lists with captions and "as of" dates.
6. Byline → author page; reviewer on YMYL; visible dates = schema dates; changelog on refresh.
7. Main content in server HTML; no restrictive snippet controls.
8. Nothing hidden, AI-only, cloaked, instruction-like; nothing mass-templated; no self-serving
   "best" list without methodology.
9. Language versions: hreflang + localised facts + natural register.
10. Images alt + captions; charts state their number in text; videos chaptered + transcribed.
11. Length fits the job; >2,500 words → hub + spokes.
12. The page or its cluster covers definition, cost, how, comparison, pros/cons, who-for,
    local specifics and risks.
