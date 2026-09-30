# Structured data, entities, feeds and meta

Evidence, complete property lists and every example: `research/04-structured-data-entities.md`.
Ready JSON-LD: `assets/schema/*.jsonld` (valid, lint-clean). Lint: `scripts/_schema.py`
(run by audit.py).

---

## 1. What schema does and does not do in 2026

- **Does:** Google rich results and merchant listings; logo / knowledge-panel details;
  entity disambiguation (Organization, sameAs, identifiers); Bing/Copilot understanding
  (Microsoft's stated position); feeds validation against the site.
- **Does not:** lift AI citations on its own (Ahrefs diff-in-diff: no gain), and **live-
  fetching assistants ignore JSON-LD** — a fact that exists only in schema is invisible to
  ChatGPT/Claude/Perplexity/Gemini/AI Mode on fetch.
- **Rule:** every fact goes in visible HTML text first; schema mirrors it. audit.py flags
  JSON-LD prices, ratings and authors that aren't visible.

## 2. Google rich-result status (re-check `developers.google.com/search/updates`, RSS available)

Still live: Article, Breadcrumb (desktop only since 2025-01), carousels via ItemList, Course
*list*, Discussion forum, Education Q&A, Employer rating, Event, Image metadata, Job posting,
Local business, Math solver, **Merchant listing / Product snippet / Product variants**,
Return + Shipping policy + Loyalty program, Movie, Organization, Profile page, QAPage (user
Q&A only), Recipe, Review snippet, Software app, Speakable (beta), Paywalled content,
Vacation rental, Video (+ key moments), Site names (WebSite on the home page).

Retired: HowTo (2023-09), sitelinks search box / SearchAction (2024-11), Course Info,
ClaimReview in Search, Estimated Salary, Learning Video, Special Announcement, Vehicle
Listing (2025-06/09), Practice problem (2025-11), **FAQ (2026-05-07)**. Dataset → Dataset
Search only. Unused markup is harmless: keep FAQPage/HowTo only where the content really is a
FAQ or steps (Bing names FAQ as useful) and **never promise a rich result from them**.

Growth areas (where Google keeps adding): Product/Offer properties, Organization-level return
and shipping policies, loyalty programs, forum/QA, video (`creator`, `interactionStatistic`
2026-09-24). Google picks thumbnails from both schema `image` and `og:image` (2026-03).

## 3. The pattern: one connected @graph per page

- One `<script type="application/ld+json">` with a single `@graph`, server-rendered.
- Stable `@id`s: canonical URL + fragment (`#organization`, `#website`, `#webpage`,
  `#breadcrumb`, `#article`, `#person-<slug>`). **Reuse the same site-wide IDs on every page**
  so everything points at one Organization and one WebSite.
- Reference, don't repeat: `"publisher": {"@id": "https://example.com/#organization"}`.
- Home page: Organization (or LocalBusiness subtype / OnlineStore) + WebSite + WebPage →
  `assets/schema/organization-website.home.jsonld`.
- Article pages: WebPage + ImageObject + BreadcrumbList + BlogPosting/Article + Person →
  `assets/schema/article.graph.jsonld`.
- Escape `<` as `\u003c` when serialising CMS data into a script tag (XSS and broken-markup
  guard). In JSX use a native `<script>`, not `next/script`.

## 4. Type choices and required properties (Google)

| Page | Type(s) | Required / critical | Asset |
|---|---|---|---|
| Home / About | Organization (+ subtype), WebSite, AboutPage | Org: no required props — add name, url, logo (≥112×112, crawlable), description, sameAs, contactPoint, address, legalName, identifiers (taxID, leiCode, duns, iso6523Code, naics — used "to disambiguate"). WebSite: name, url, alternateName **on the domain/subdomain home page only** | organization-website.home |
| Article / guide | BlogPosting / Article / NewsArticle | headline; author = Person/Organization object(s), **one per author, name only (no "By", titles, or "A and B")**, with url/sameAs; datePublished/dateModified with time **and timezone**, matching the visible byline | article.graph |
| Author page | ProfilePage + Person | mainEntity with name; jobTitle, worksFor, sameAs (LinkedIn, ORCID, Scholar), hasCredential | profile-page.author |
| Product (sells) | Product / ProductGroup + Offer | name, image, offers.price (number) + priceCurrency; availability; gtin/mpn/sku, brand; shippingDetails; hasMerchantReturnPolicy (applicableCountry, returnPolicyCountry, returnPolicyCategory). Variants: ProductGroup + hasVariant + variesBy + productGroupID = each variant's inProductGroupWithID | product, product-group.variants, store-policies.org-level |
| Review page (doesn't sell) | Product snippet / Review | name + one of review / aggregateRating / offers; Review needs author, itemReviewed, reviewRating | — |
| Local location | most specific LocalBusiness subtype | name, **real** address; geo (≥5 decimals), openingHoursSpecification, telephone, url = location page, priceRange, areaServed, sameAs (Maps CID, Facebook, Waze) | local-business |
| Service-area / online-only business | Organization or ProfessionalService with areaServed | no fake address | service |
| Service page | Service | name, provider → Org @id, areaServed, offers with price | service |
| SaaS | SoftwareApplication / WebApplication | name, offers.price (0 allowed), aggregateRating **or** review; applicationCategory, operatingSystem | software-application |
| Video watch page | VideoObject | name, thumbnailUrl, uploadDate; contentUrl/embedUrl, duration, Clip key moments, creator | video |
| Event | Event | name, startDate, location (Place + address); eventStatus, offers, organizer | event |
| Stats / research page | Article + Dataset | Dataset name + description (Dataset Search only) | statistics-page.dataset |
| YMYL medical | MedicalWebPage | reviewedBy (Person + credential), lastReviewed — **visible on page too** | ymyl-medical-webpage |
| Forum / community | DiscussionForumPosting / QAPage | author, datePublished, text | research/04-structured-data-entities.md §3.9–3.10 |
| Real FAQ block | FAQPage | Q&A visible on the page, answers identical | faq |

Self-serving review stars (a business marking up reviews of itself with LocalBusiness/
Organization) are not eligible. Fake or undisclosed-incentive reviews are banned (guideline
2026-07-24; FTC rule in the US).

## 5. Validation (automated first, then Google's tools)

audit.py / `_schema.py` checks: JSON parse (incl. trailing commas), required properties,
graph wiring, author form, ISO dates + timezone, price format, visible parity for price /
rating / author / FAQ questions, retired types (info), LocalBusiness without address.

Also check by hand or script:
1. Raw vs rendered: JSON-LD present **without JS** (render_diff.mjs compares).
2. One Organization with one name; no duplicate Product blocks (theme + app + plugin is the
   usual cause on WordPress/Shopify/Wix).
3. Cross-source parity: `<title>` ≈ `og:title` ≈ `headline` ≈ H1; canonical = `og:url` =
   `@id` base; `article:modified_time` = `dateModified`; **feed price = schema price =
   visible price**.
4. `sameAs` URLs resolve and link back.
5. Rich Results Test (Google features) + validator.schema.org (generic).

## 6. Entity SEO

- **Canonical fact set.** One brand string, one-line description, category, founding year,
  HQ, founders, key numbers — identical on the About page, Organization schema, GBP, Bing
  Places, Apple Business, LinkedIn, Crunchbase, app stores, review profiles, press
  boilerplate, author bios. Variants go in `alternateName`. Keep `docs/geo/facts.md` as the
  source of truth; ai_visibility.py accuracy checks compare against it.
- **sameAs**: only profiles about *this* entity that you control or that are authoritative
  (Wikidata, Wikipedia if it exists, LinkedIn, Crunchbase, GitHub, YouTube, X, Instagram,
  Facebook, TikTok, Google Search profile, app-store developer page, registry/LEI record,
  Maps CID). Make them reciprocal. Never competitors or review sites you don't own.
- **Ambiguous names**: pair the name with its category in visible copy ("Tapis, the WhatsApp
  order-capture app"), a distinctive description, Wikidata sameAs, knowsAbout/areaServed.
- **Knowledge panel**: claim via Search Console / YouTube / X / Facebook verification;
  suggest edits with supporting links. **Google Search profiles** (2026,
  profile.google.com/@handle): if one exists, link it and add it to sameAs.
- **Wikidata**: only if it meets notability (serious public references) — disclosed account,
  every statement referenced. **Wikipedia: never write or edit a client's article.** Assess
  notability honestly (WP:NCORP needs significant independent secondary coverage; press
  releases and funding news don't count); if not notable, earn coverage; if notable, a
  disclosed Talk-page edit request or Articles for Creation.
- **Author entities**: an author page per writer (ProfilePage + Person, credentials, photo,
  sameAs); bylines link to it; articles reference the Person by `@id`.
- Why this matters for LLMs: a model's recall of a fact scales with how many training
  documents state it (Kandpal et al.). Consistent, repeated, crawlable facts become "known";
  contradictory ones make models hedge.

## 7. Feeds are structured data too (commerce)

Order of work for e-commerce: (1) Google Merchant Center feed with free listings, no
disapprovals; `product_highlight`/`product_detail`; the 2026 conversational attributes for
top SKUs (`question_and_answer` up to 30 Q&As, `document_link`, `related_product`,
`item_group_title`, `variant_option`, `popularity_rank`); (2) matching on-page Product/Offer;
(3) Organization-level return and shipping policies; (4) consistent GTINs; (5) OpenAI feed
(JSONL or Google-format; required `item_id, title ≤150, description ≤5000, url, brand,
seller_name, image_url, availability, price "18.00 USD"`; approved partners); (6) Microsoft
Merchant Center + IndexNow; (7) Perplexity Merchant Program; (8) Shopify: leave Agentic
Storefronts on, fill taxonomy category + metafields + GTINs. Details: `verticals.md`.

## 8. Meta tags

| Tag | Rule |
|---|---|
| `<title>` | Unique, descriptive, brand once with a delimiter; consistent with H1 and og:title (best defence against Google rewrites) |
| meta description | Unique, specific (price, who-for, key number); not a ranking factor, often the snippet |
| robots | `index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1`. `nosnippet`/`max-snippet` also limit AI Overviews/AI Mode input; `noarchive`/`nocache` limit Copilot |
| `data-nosnippet` | Surgical exclusion (Google + Bing). Never around the main answer |
| canonical | One, absolute, self-referencing, in `<head>` of the server HTML, per page (never inherited from a layout) |
| hreflang | Self + reciprocal + x-default; valid codes (`ms-MY` — **`my` is Burmese**; `en-GB` not `en-UK`; `zh-Hans-MY`); targets canonical 200s; never canonicalise across languages |
| Open Graph | og:title, og:type, og:image (+ width/height/alt), og:url, og:site_name; article:published_time / modified_time / author |
| Twitter | `summary_large_image`, falls back to OG |

Full head template: `assets/head-template.html`.
