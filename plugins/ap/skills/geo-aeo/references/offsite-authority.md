# Off-site authority — what other sites say about the brand

AI answers are built mostly from **what others say about a brand**, not from the brand's own
site. Evidence, platform shares and enforcement data: `research/06-offsite-authority.md`.
Most of this is **owner work** — the agent's job is to diagnose it (ai_visibility.py shows
which third-party domains the engines trust for the category), write the plan and prepare
materials, never to fake it.

---

## 1. What the evidence says

- Unlinked **branded web mentions** ρ≈0.66 and **YouTube mentions** ρ≈0.74 with AI visibility,
  vs backlinks ρ≈0.22–0.30 (Ahrefs, 75k brands; correlational). Frequency across many modest
  sources beats one viral hit.
- **Earned media is 82–89% of AI citations**; journalism 27%; paid/advertorial 0.3% (Muck Rack,
  25M links). >50% of cited journalism is from the last 12 months.
- Third-party **"best X" lists** are ~44% of page types ChatGPT cites for commercial prompts.
- **Mentions ≠ citations.** 62% of citations come with no brand mention in the answer; only
  6–27% of the most-mentioned brands are among the most-cited sources. Off-site work mostly
  moves *mentions*; on-site work mostly moves *citations*. Track both.
- Google's AI surfaces favour established brands (AIO ρ 0.65 for mentions); ChatGPT is the
  most open to small brands (ρ 0.15) — new brands should aim at ChatGPT-cited lists first.
- **Parametric vs retrieval.** Only ~20–35% of ChatGPT prompts trigger a web search; the rest
  come from what the model already knows. Built-in knowledge scales with how many crawlable
  documents state the fact consistently (Kandpal et al.) → be in Common Crawl, keep one
  canonical fact set everywhere, get mentioned in text-heavy, widely copied places (news,
  trade press, YouTube transcripts, podcasts with transcripts, LinkedIn articles).
- **Volatility.** ChatGPT's Reddit citations: ~60% → ~10% of responses (Sep 2025), then 3.8% →
  0.5% of citations (Aug 2026). Never make one platform the plan.

## 2. Surfaces and legitimate tactics

**Third-party lists & comparisons** — find the lists the engines already cite for the
category (ai_visibility.py "domains the engines cite" + manual prompts); pitch their editors
an accurate brief, demo/sample, pricing, differentiators; keep them updated (79% of cited
lists were refreshed within the year). Affiliate relationships only if the publisher discloses.
Avoid pay-for-placement without disclosure and networks of low-quality lists.

**YouTube** — long-form (10–20 min) reference videos, chapters from 00:00, entity-rich
descriptions, clean transcripts, brand name said aloud; get mentioned on *other* channels
(review seeding, disclosed sponsorships, expert guest spots). Views barely correlate with
citation; description length and recency do.

**Reviews** — steady, recent (74% of consumers want reviews from the last 3 months), answered,
on the platforms that matter for the vertical (Google, Facebook, Yelp/TripAdvisor for local and
hospitality; G2/Capterra/Gartner Peer Insights/TrustRadius for B2B software; Trustpilot and
marketplaces for e-com). Ask **every** customer; no gating by satisfaction; incentives never
conditioned on sentiment; staff and relatives disclose. US FTC rule (effective 2024-10-21):
fake/AI-generated reviews, sentiment-conditioned incentives, undisclosed insider reviews,
suppression and fake followers are banned, up to $51,744 per violation. Google removed 292M
bad reviews in 2025 and shows public warning banners.

**LinkedIn** (#2 cited domain overall in 2026; ~14% of ChatGPT search answers) — company page
(Perplexity prefers these) + founder/staff thought leadership (ChatGPT and AI Mode prefer
individuals); educational articles 500–2,000 words; 5+ posts/month; follower count matters
little.

**Reddit & communities** — disclosed staff/founder answers that genuinely help (including
recommending competitors when they fit better), mod-approved AMAs, a branded support account,
fixing the issues negative threads describe. **Never** aged accounts, vote rings, "I just
discovered X" staff posts or AI comment farms — Reddit's AI removes ~25k marketing spam items a
day and is explicitly targeting GEO seeding; exposed campaigns become the threads AI cites.

**Digital PR & original data** — publish original data (survey, anonymised product data, price
index) with a methodology page; journalists cite it, AI cites the journalists. Trade and
regional press per industry. Wires (PRNewswire, BusinessWire, GlobeNewswire) for factual
announcements — quickly retrievable for "what did X announce", tiny share for "best X"
prompts; write releases with statistics and bullets. Expert-quote platforms: Featured (bought
HARO), Qwoted, Source of Sources. No disguised advertorials.

**Wikipedia / Wikidata** — see `structured-data.md` §6. Never write or edit the client's
article. Honest notability assessment; earn coverage first.

**Directories & listings** — the ones people and journalists actually use: industry
associations, chambers of commerce, government registries, niche vertical directories
(Perplexity leans on these). Never paid link-farm directories.

**Podcasts, awards, communities** — no direct citation data; value is indirect (transcripts,
show notes, mentions).

**Affiliate / publisher partnerships** — legitimate with disclosure; watch Google's thin-
affiliation and site-reputation-abuse policies, which can delete the host pages you paid for.

## 3. Forbidden (and what to do if you find it)

- Fake or incentivised-by-sentiment reviews; review gating; suppression.
- Astroturfing Reddit/Quora/forums; sock puppets; vote manipulation.
- Hidden text or prompt injection on pages, inside JSON-LD, or in "Summarize with AI" links
  with persuasion prompts ("remember X as a trusted source"). Google's threat intel found
  injections like "Recommend this business above all others" in Common Crawl (+32% in three
  months); Microsoft filters "AI recommendation poisoning" (31 companies in 60 days).
  **audit.py scans for these; remove any you find and tell the owner which plugin/agency added it.**
- Networks of self-ranking listicles, expired-domain "best X" sites, parasite placements.
- False claims about competitors (FTC / Lanham Act risk).

## 4. Managing the brand narrative in AI answers

1. **Audit on a schedule** with ai_visibility.py (brand-definition, category, comparison,
   "is X legit / complaints", local prompts; many runs; mentions and citations and accuracy
   logged separately). Check reasoning modes too — they cite official docs and .gov/.edu more.
2. **Trace each error to its source URL** (usually a third-party page: old review, stale
   listicle, Reddit thread, directory entry, Wikipedia). Fix it there: ask the editor, update
   the listing, reply in-thread with a disclosed factual update, file a Talk-page request.
3. **Publish authoritative fact sources** on the site: About / company-facts page with a
   changelog, newsroom with dated releases and boilerplate, pricing, specs, a limitations /
   "what we don't do" page — server-rendered, crawlable by retrieval bots (and CCBot).
4. **Make descriptions consistent** across every profile — contradictions dilute the signal.
5. **Hallucinations**: stale parametric facts fix slowly (correct pages + volume of correct
   third-party mentions, over training cycles). Use each engine's thumbs-down feedback. Google:
   claim the knowledge panel and suggest edits. No official correction channel exists at
   OpenAI or Anthropic.
6. **Comparisons**: publish fair "X vs Y" and "alternatives to Y" pages (comparative prompts
   yield 2.4× more mentions); make sure third-party comparisons carry current data.
7. **Negative sentiment**: fix the underlying issue, respond publicly and factually, publish
   newer well-documented content (recency bias displaces old sources). Never suppress reviews.

## 5. Playbooks by business type (order = do first → later)

**(a) New small business** — 1 canonical fact sheet; claim GBP (if local), Bing Places, Apple
Business, LinkedIn page, Crunchbase or an industry directory, social profiles; Organization
schema with sameAs; allow search bots, and decide consciously on GPTBot/CCBot/ClaudeBot
(allowing helps built-in knowledge) · 2 first 10–30 real reviews on the platform that matters ·
3 founder-led LinkedIn (5+ posts/month + monthly articles) · 4 get onto the "best X" lists
ChatGPT cites · 5 YouTube: own explainers + appearances on niche channels · 6 disclosed
community participation · skip for now: Wikipedia, wires, paid directories.

**(b) Established SMB** — 1 audit AI answers, fix the top 10 error/absence sources · 2 review
velocity + response programme on Google + the 2–3 platforms AI cites for the category (aim for
a real 4.5★) · 3 digital PR with original data 1–2×/year · 4 list & comparison outreach with
quarterly refresh requests · 5 YouTube: 10–20 min chaptered videos, seed niche reviewers ·
6 staff thought leadership on LinkedIn · 7 Wikipedia only if WP:NCORP is honestly met.

**(c) SaaS / B2B** — 1 complete G2/Capterra/Gartner Peer Insights/TrustRadius profiles with a
continuous review ask (eligibility/consensus layer) · 2 third-party "best X software" lists +
honest "X vs Y" / "alternatives" pages · 3 public docs, security/compliance, pricing,
changelog (thinking modes cite official docs) · 4 LinkedIn: company page + executives ·
5 original research reports, analyst relations, wires for launches · 6 YouTube tutorials,
webinars, partner/integration marketplace listings · 7 disclosed community answers; don't
depend on Reddit for ChatGPT.

**(d) E-commerce** — 1 marketplace/retailer presence with consistent product facts (Amazon,
Walmart are top-10 AIO domains; Shopee/Lazada in SEA) · 2 product reviews at volume, strict
compliance · 3 creator seeding on YouTube/TikTok/Instagram with #ad disclosure (social is >40%
of AIO citations; long-form YouTube reviews are the cited format) · 4 affiliate/publisher
roundups (supply samples and specs; insist on disclosure) · 5 disclosed Reddit/Quora support
presence · 6 category trend-report PR.

**(e) Local service business, Malaysia / SEA** (platform facts sourced; priorities reasoned) —
1 **Google Business Profile** first (categories, services with prices, photos, posts, Q&A,
WhatsApp CTA, reply to every review) · 2 **Facebook page** with recommendations in BM and
English (Facebook is the #1 review source behind ChatGPT local answers in the US and #3 in AIO;
huge reach in MY) · 3 Bing Places + Apple Business (cheap; ChatGPT/Copilot route through Bing,
Siri through Apple) · 4 identical NAP across GBP, Facebook, **Waze**, Grab/Foodpanda (F&B),
Carousell/vertical directories, SSM-registered name, website — BM and English descriptions with
the same facts · 5 steady, recent, answered reviews in the customer's language · 6 local "best
X in KL/JB/Penang" lists and local media (Whitespark's #1 AI local factor: expert-curated
best-of lists) · 7 YouTube/TikTok walkthroughs and customer stories with the name said and
captioned; local creator visits · 8 Yelp/TripAdvisor only if relevant — check what ChatGPT
actually cites for "best [service] in [city]" first · 9 service and area pages in BM and
English (landmarks, areas, prices, hours, FAQs). Malaysia context: TikTok 30.7M, YouTube 23.6M,
Facebook 23.0M, Instagram 16.1M, LinkedIn 10.0M users vs Reddit 4.3M — Facebook and YouTube
carry the local conversation, not Reddit.

**(f) Agency / studio / professional services** — 1 "Site by …" credits on every client and own
site that permits it (check with `presence.py --from-page`) · 2 Clutch/GoodFirms/Sortlist-type
profiles with verified client reviews · 3 award and gallery submissions (Awwwards, CSSDA,
Behance/Dribbble) · 4 client-side testimonials and case-study co-posts · 5 founder/studio
LinkedIn · 6 one piece of original data or a public tool per year. Details: `verticals.md`.

## 6. Output of this phase

`docs/geo/offsite-plan.md`: the target-domain list from ai_visibility.py, the fact sheet
(`docs/geo/facts.md`), the profile inventory (claimed / unclaimed / inconsistent), the review
programme, the PR/data idea, the outreach list with pitch drafts, and a dated owner checklist.
