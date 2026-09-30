# Vertical playbooks — e-commerce, local, SaaS/B2B, publishers, YMYL, Malaysia

Detail, dated timelines and sources: `research/09-verticals-frameworks.md` Part A;
off-site angle per vertical: `offsite-authority.md` §5. Apply the universal P0–P2 work first;
this file adds what each vertical needs on top.

---

## E-commerce

**State of AI shopping (Sep 2026)** — checkout protocols are *platform integrations*, not page
edits: OpenAI's ACP (native Instant Checkout wound down Mar 2026; purchases via merchant apps
or click-out; product feeds for approved partners); Google's **UCP** (Cart, Catalog, Identity
Linking; checkout live US/CA/AU for Merchant Center `native_commerce` listings; Universal Cart
and AP2 from I/O 2026); **Shopify Agentic Storefronts** (on by default; syndicates to ChatGPT,
Copilot, AI Mode, Gemini via Shopify Catalog); Perplexity Merchant Program + PayPal Instant
Buy; Amazon **Alexa for Shopping** replaced Rufus (2026-05-13).

What the agent controls, and it feeds all of them:
1. **Feeds**: Google Merchant Center (free listings, zero disapprovals, `product_highlight`,
   `product_detail`, and the 2026 conversational attributes on the top 20% of SKUs:
   `question_and_answer` ≤30 pairs, `document_link` ≤5 PDFs, `related_product`,
   `item_group_title`, `variant_option`, `popularity_rank`). OpenAI feed (JSONL or
   Google-format). Microsoft Merchant Center. Consistent GTINs everywhere.
2. **Server-rendered PDPs** with the passages answers lift, each a crawlable text block (not a
   JS tab): spec table (`<table>`/`<dl>` with units, compatibility, model numbers) · "who it's
   for / use cases" · comparison vs sibling SKUs and the obvious rival · **reviews in the
   initial HTML** (third-party widgets loaded client-side are invisible) · shipping and
   returns on the PDP · product Q&A (mirrored into Merchant Center) · identifiers.
3. **Markup**: ProductGroup + variants, Offer (price as number, currency, availability,
   condition, priceValidUntil), **Organization-level** MerchantReturnPolicy (incl.
   `returnPolicyCountry`) and ShippingService, genuine AggregateRating/Review only.
   Visible price = schema price = feed price. AI-generated product images: IPTC
   `DigitalSourceType`; AI-generated product data labelled.
4. **Category pages**: a short server-rendered intro that answers the buying question, a
   comparison table, crawlable `<a href>` pagination; facets canonicalised or noindexed and
   out of the sitemap.
5. An honest "best X for Y" buying guide that includes competitors is legitimate (listicles
   are the top ChatGPT-cited page type) — methodology, disclosure, real cons.
6. robots: allow OAI-SearchBot, PerplexityBot, Googlebot, Bingbot, Applebot, Amzn-SearchBot;
   training bots are the owner's call.

Checklist: PDP/category/policy pages SSR with price, stock, specs, reviews in raw HTML ·
ProductGroup/Product/Offer matching visible data · org-level policies + human policy pages
linked from every PDP · Merchant Center clean + conversational attributes · Shopify: Agentic
Storefronts on, Standard Product Taxonomy category + metafields filled, real variant options.

## Local businesses

**How engines source local answers** — Gemini/AI Mode/Maps: Google Business Profile + site
(Gemini: ~52% of local citations from the brand's own site). ChatGPT: Yelp (licensed 330M
reviews / 8M listings), Bing Places, Facebook (#1 review source behind ChatGPT local in US
data), TripAdvisor, directories — no direct GBP integration. Apple: Apple Business (Maps,
Siri). Google's AI can phone businesses for prices (US; opt-out in GBP advanced settings).

**Reality check** — AI recommends far fewer locations than the map pack: ChatGPT 1.2%, Gemini
11%, Perplexity 7.4% vs 35.9% in Google's 3-pack (SOCi, 350k locations). ChatGPT and Gemini
named the same top business in 4.2% of identical queries. Recommended businesses averaged
4.3★; 31% of consumers only use 4.5★+. SOCi's FACTS: Freshness, Authority (ratings, reviews,
responses), Consistency (NAP), Trust, Semantic relevance. Whitespark's top AI local factors:
expert-curated best-of lists · dedicated service pages · prominence on industry domains ·
quality unstructured citations · review-site authority · geographic relevance.

Agent does (site): one server-rendered page per **physical** location (unique NAP, map,
hours, services, parking/transit, area served, staff, local photos, location FAQs) ·
LocalBusiness subtype JSON-LD per location (geo ≥5 decimals, hours incl. seasonal, url = the
location page, sameAs to GBP/Apple/Yelp/Facebook) · service-area businesses: `areaServed`, no
fake street address, service pages per *service* not doorway pages per suburb — a city page
only with real local proof · **visible prices** ("from RM X") · NAP identical character for
character everywhere.

Owner does (the skill outputs a checklist): complete GBP (categories, services with prices,
attributes, products, weekly photos, posts, Q&A, reply to every review) · claim Apple
Business, Bing Places, Yelp, Facebook; **Waze** and Grab/Foodpanda in Malaysia · steady recent
reviews · local "best X in <city>" lists and local press · decide the AI-calls setting.

## SaaS / B2B

Evidence: ChatGPT B2B citations — listicles 18.8%, product/service pages 18.6%, documentation
12.5%, review platforms 1.6%; **66% of brand recommendations happen without ChatGPT citing the
brand's site** (be recommended *and* be cited are separate jobs); pages naming 6+ brands get
cited more; docs are cited even when old (17-month median). Comparison pages dominate
evaluation-stage citations; decision-stage citations need concrete numbers.

Build, in order: 1 **pricing page with numbers in HTML** (tiers, limits, what "contact sales"
means) · 2 **"X vs <competitor>" and "<competitor> alternatives"** pages, one per real
competitor, fair feature table, who should pick them, migration steps, date stamp · 3
**integration pages**, one per integration (what syncs, direction, setup, limits) · 4 use-case
/ industry pages with a customer quote and a metric · 5 **public SSR docs** — stable URL per
concept, `lastUpdated`, `/llms.txt` + `/llms-full.txt`, `.md` alternates / `Accept:
text/markdown`, copyable code; optionally a docs/product MCP server (nextjs.org/docs is the
reference pattern) · 6 dated changelog · 7 trust pages (security/compliance, status,
customers) · 8 SoftwareApplication + Organization sameAs (G2, LinkedIn, GitHub, Crunchbase).
Keep G2/Capterra profiles accurate — table stakes for "[brand] reviews" prompts, not the lever.

## Publishers, blogs, media

Impact: Pew — result clicks 15% → 8% when an AI summary shows; Chartbeat — Google traffic to
~2,500 publishers −33% globally in a year, small publishers −60% over two years; chatbot
referrals growing but <1% of referrals. Licensing deals are for the big players; small
publishers' levers are crawler policy (Template B), Cloudflare pay-per-crawl/blocking,
Content-Signal.

What still earns citations and visits: original reporting, data, first-hand testing, expert
quotes; honest freshness (visible Updated + `dateModified` on substantive edits only); named
authors with author pages and "how we tested" boxes; **Preferred Sources** button; direct
channels (newsletter, app, community); technical: SSR article HTML, paywall markup
(`isAccessibleForFree` + `hasPart`) rather than scripts that hide text, Google News sitemap.

## YMYL (health, finance, legal, civic)

Rater guidelines (2025-09-11): four harm types — Health or Safety; Financial Security;
Government, Civics & Society; Other. "Very high Page Quality rating standards"; some YMYL
advice "must come from experts"; first-hand experience counts only when consistent with expert
consensus. Trust is the most important part of E-E-A-T. Reasoning modes cite official and
.gov/.edu sources more — this is where they matter most.

On the page, server-rendered: byline → author page with credentials and licence/registration
numbers (Malaysia: MMC/MDC, Bar Council, Securities Commission, BNM-licensed entity) · a
"Medically/Legally/Financially reviewed by <credentialed person> on <date>" line · sources to
primary literature, regulators, statutes with dates · specific in-context disclaimer · who runs
the site (About, address, registrations, complaints process, editorial and corrections
policies) · practitioner pages. Schema: `MedicalWebPage` with `reviewedBy` + `lastReviewed`
(`assets/schema/ymyl-medical-webpage.jsonld`); finance `WebPage`/`Article` + `FinancialService`;
legal `LegalService` + `Person` (Attorney is deprecated). The markup only helps if the same
facts are visible. Never generate YMYL advice at scale; never invent reviewers.

## Professional services, agencies and studios

The prompts that matter are "best web design agency in KL", "who built <client site>", "<studio>
reviews", "<studio> vs <competitor>". Answers lean on third-party lists and directories, so a new
studio's own site is necessary but not sufficient.

On the site (agent): one real **case study per project** — client, problem, what was built,
stack, measurable outcome (only with the client's permission and a source), dated, with
screenshots framed as work shown; a **services + pricing page with numbers** ("from RM X",
typical ranges, what changes the price); a **process page**; honest "vs freelancer / vs
template / vs big agency" comparison; About with verifiable facts (registration no., founding
date, location) — naming people is the owner's call; `ProfessionalService` (or Organization)
with `areaServed`, **no fake address**; each case study as its own URL with distinct content
(single-document portfolio sites fail this — see technical-access.md §4).

Off the site (owner): **"Site by <studio>" credits on client and own sites** — the most
legitimate mentions a young studio has; `presence.py --from-page <portfolio>` shows which built
sites already credit you · agency directories people actually use (Clutch, GoodFirms, Sortlist,
DesignRush; local chambers/associations) with verified reviews · design galleries and awards
(Awwwards, CSS Design Awards, Behance, Dribbble) — mentions plus links from well-crawled
domains · client testimonials published on the client's side (LinkedIn recommendations, their
case-study posts) · founder/studio LinkedIn with educational posts · talks, podcasts and
write-ups with transcripts. Avoid pay-to-list "top agencies" pages that don't disclose payment.

## Malaysia specifics (cuts across verticals)

- AI Overviews support Malay (May 2025); AI Mode reached Malaysia Aug 2025 (English) and added
  Malay on 2025-10-08.
- **Malay → Indonesian bias**: in a 100-prompt test only 31% of answers came back in Bahasa
  Melayu, 66% in Bahasa Indonesia (training data ≈ 9:1 Indonesian). Publish a real BM version
  with its own URLs and `hreflang="ms-MY"`; colloquial Malaysian register with English trade
  terms; Malaysian place/unit terms (taman, jalan, seksyen, Lembah Klang, RM, postcode, state);
  watch false friends (*percuma*, *kereta*); test prompts in BM on each engine.
- Mixed-language queries are the norm ("kedai tayar murah near Puchong", "klinik gigi buka
  Ahad Shah Alam") — use both registers in headings and FAQs.
- Maps: claim both GBP (feeds Gemini/AI Mode) and **Waze**; Apple Maps is small but cheap to
  claim; Grab/Foodpanda for F&B.
- Social reach: TikTok, YouTube, Facebook ≫ Reddit (4.3M users). Facebook and YouTube carry
  local conversation.
- Trust: SSM registration number visible; PDPA-compliant privacy policy; RM prices incl.
  SST where applicable; WhatsApp as a contact channel.
- Google ~93% search share; set up Bing Webmaster Tools + IndexNow anyway (Copilot/ChatGPT).
