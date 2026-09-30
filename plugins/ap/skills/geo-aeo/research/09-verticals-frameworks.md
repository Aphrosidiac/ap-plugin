# 09 — Vertical playbooks + framework implementation guide (GEO / AEO / SEO)

Researcher 9 of 9. Compiled 2026-09-26. Every claim has a URL and a date (publication or "last updated", or the date fetched when the page shows none). Claims I could not confirm against a primary or first-hand source are marked **unverified**. Vendor and agency blogs count as secondary. I cite them only where no primary source exists and label them as secondary.

---

## 0. Findings that apply to every vertical (read first)

1. **Google says AI Overviews and AI Mode need nothing special.** The page must be indexed and eligible to show with a snippet. Google says: "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary". You do not need to "create new machine readable files, AI text files, or markup". The controls are `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` and `Google-Extended`. The listed best practices are: allow crawling, link internally, give a good page experience, keep content as text, use good images and video, keep structured data accurate, and keep business/merchant info current. — https://developers.google.com/search/docs/appearance/ai-features (last updated 2025-12-10)
2. **Non-Google AI crawlers do not run JavaScript.** Vercel and MERJ looked at GPTBot, ClaudeBot and PerplexityBot. These bots fetch JS files but do not execute them. Only Gemini (on Googlebot's infrastructure) and Applebot render JS. ChatGPT's and Claude's crawlers hit 404s on about 34–35% of requests, against 8.22% for Googlebot. — https://vercel.com/blog/the-rise-of-the-ai-crawler (2024-12-17). **Consequence for every framework below:** anything that only appears after client-side rendering is invisible to ChatGPT, Claude and Perplexity crawlers. This includes content, title, canonical and JSON-LD. SSR or SSG is therefore required for AI visibility, not just for Google.
3. **Google calls dynamic rendering "a workaround and not a long-term solution".** Use SSR, static rendering or hydration instead. — https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering (last updated 2025-12-10). Rendertron was deprecated and archived on 2022-10-06. — https://github.com/GoogleChrome/rendertron
4. **JS SEO rules that matter most for SPAs.** Links must be `<a href>`. Use the History API, not `#` fragments. Put the canonical in HTML; if JS changes it, it must match the original. Do not rely on JS to remove `noindex`, because Google "may skip rendering" once it sees `noindex`. Avoid soft 404s by redirecting to a real 404 or adding `noindex` via JS. — https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics (fetched 2026-09-26)
5. **llms.txt is useful for coding agents, not for AI search.** Ahrefs checked 137,210 domains (May 2026). 28% publish llms.txt, but **97% of those files got zero requests**. Only 1.1% of requests came from AI retrieval bots, and "Slackbot alone fetched llms.txt files more often than PerplexityBot did". The real audience appears to be coding agents such as Claude Code. — https://ahrefs.com/blog/llmstxt-study/ (May–June 2026). **Skill guidance:** ship llms.txt cheaply on docs and developer sites. Never promise that it lifts citations.
6. **Markdown by content negotiation is the newer pattern for agents.** Cloudflare "Markdown for Agents" converts HTML to markdown when a request carries `Accept: text/markdown`. Claude Code and OpenCode already send that header. Cloudflare cites an 80% token reduction. It launched 2026-02-12 as a beta on Pro/Business/Enterprise. — https://blog.cloudflare.com/markdown-for-agents/. Vercel describes the same pattern in Next.js: a rewrite on the Accept header, `.md` routes, `/sitemap.md`, and `<link rel="alternate" type="text/markdown">` as a fallback. The HTML page is about 500 KB; the markdown is 3 KB. — https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation (2026-02-03)

---

# PART A — Vertical playbooks

## A1. E-commerce

### A1.1 Where AI shopping is in Sept 2026 (dated timeline)

| Date | Event | Source |
|---|---|---|
| 2024-11 | Perplexity "Buy with Pro" (first mover among the answer engines) | secondary: https://www.shopify.com/blog/how-agentic-commerce-works and others |
| 2025-09 | OpenAI launches Instant Checkout plus the Agentic Commerce Protocol (ACP), starting with Etsy | https://openai.com/index/buy-it-in-chatgpt/ |
| 2025-11-25 | PayPal × Perplexity "Instant Buy". PayPal merchants become discoverable, with checkout in the chat | https://newsroom.paypal-corp.com/2025-11-PayPal-and-Perplexity-Launch-Instant-Buy |
| 2026-01 (NRF) | Google launches the Universal Commerce Protocol (UCP), co-developed with Shopify, Etsy, Wayfair, Target and Walmart. It is open, carries no transaction fees, and the retailer stays merchant of record | https://developers.google.com/merchant/ucp ; https://support.google.com/merchants/answer/16837055 |
| 2026-03 | **OpenAI retires native Instant Checkout.** Purchases move to merchant Apps (Apps SDK, merchant-side payment) or to a redirect to the merchant site. ChatGPT now concentrates on discovery. Walmart reportedly saw in-ChatGPT checkout convert about 3× worse than a click-out, and fewer than 15 Shopify merchants ever went live (both figures secondary) | https://www.checkout.com/blog/openai-agentic-commerce-shift (2026-04-20); CNBC 2026-03-24 https://www.cnbc.com/2026/03/24/openai-revamps-shopping-experience-in-chatgpt-after-instant-checkout.html (403 on fetch; carried by several secondaries) |
| 2026-03-19 | UCP adds **Cart**, **Catalog** (real-time variants, inventory and price pulled from the retailer) and **Identity Linking** (loyalty). Merchant Center onboarding is simplified | https://blog.google/products-and-platforms/products/shopping/ucp-updates/ |
| 2026-03 (late) | Shopify **Agentic Storefronts** switches on automatically for eligible merchants. Products are syndicated through **Shopify Catalog** to ChatGPT, Copilot, Google AI Mode and Gemini with no app install. Settings live at Settings › Sales Channels › Agentic Storefronts | https://www.shopify.com/blog/how-agentic-commerce-works (2026-06-18) |
| 2026-05 (Google Marketing Live) | Merchant Center adds **6 "conversational attributes"** for AI Mode, Gemini and Business Agent | https://www.productsup.com/blog/google-introduces-six-conversational-attributes-in-merchant-center-here-what-you-need-to-know/ (secondary) |
| 2026-05-13 | **Amazon retires Rufus.** "Alexa for Shopping" takes over the search bar, results and PDPs for all signed-in US customers. Amazon says Rufus reached 300M customers and about $12B in annualised incremental sales | CNBC https://www.cnbc.com/2026/05/13/amazon-ditches-rufus-ai-chatbot-in-favor-of-alexa-shopping-agent.html ; Axios https://www.axios.com/2026/05/13/amazon-alexa-ai-shopping-assistant |
| 2026 (Google I/O, May) | **Universal Cart** across merchants on Search and Gemini, US, summer 2026. It checks compatibility (e.g. PC parts), tracks price history and applies Wallet perks. The **AP2** agent-payments protocol is added. UCP checkout expands to Canada and Australia, then the UK. Nike, Sephora, Target, Ulta, Walmart and Wayfair support it | https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/ |

**What this means for the skill:** the checkout protocols (ACP, UCP, AP2, Shopify Catalog) are platform integrations, not website edits. An agent editing a site can control three things that feed all of them:
- (a) the product feed / Merchant Center data
- (b) crawlable, server-rendered PDPs with accurate Product/Offer markup
- (c) policy pages and policy markup (shipping and returns).

A clean feed gets you into discovery. Checkout requires separate onboarding (UCP in Merchant Center; OpenAI Apps; Shopify handles it automatically).

### A1.2 How each engine picks products

- **ChatGPT.** The OpenAI help article "Shopping with ChatGPT Search" returned 403 on fetch. Secondary summaries that quote it say the factors are relevance to intent (including memory and custom instructions) and "structured metadata from first-party and third-party providers (e.g., price, product description)". Merchants are ranked on availability, price, quality, and whether they are the maker or primary seller. ChatGPT may rewrite titles and descriptions. — https://help.openai.com/en/articles/11128490-shopping-with-chatgpt-search (quoted via https://www.linkedin.com/posts/aleyda_how-chatgpt-product-results-are-selected-activity-7324369929263022080-k6pm; treat wording as secondary).
- **OpenAI product feed (current OpenAI docs).** Required fields: `item_id`, `title` (≤150 chars), `description` (≤5,000), `url`, `brand`, `seller_name`, `image_url`, `availability` (`in_stock|out_of_stock|pre_order|backorder|unknown`), and `price` written as `"79.99 USD"`. Recommended: `sale_price`, `additional_image_urls`, `condition`, `review_count`, `star_rating`, `accepts_returns`, `return_deadline_in_days`. Flags: `is_eligible_search` (default true), `is_eligible_checkout`, `is_ads_eligible`. Formats: JSONL (preferred), CSV, TSV. — https://developers.openai.com/commerce/specs/file-upload/products (fetched 2026-09-26). The community ACP spec site uses the older names `enable_search`/`enable_checkout`, accepts updates every 15 minutes, and formats shipping as `US:CA:Overnight:16.00 USD`. — https://agentic-commerce-protocol.com/docs/commerce/specs/feed. **The field names have changed; always check the live spec.**
- **Google AI Mode / Gemini.** The inputs are the Merchant Center feed plus the Shopping Graph plus crawled PDPs. The six new *optional* conversational attributes are: `question_and_answer` (up to 30 Q&A pairs per product, ≤1,000 chars each side), `document_link` (up to 5 PDFs: manuals, spec sheets, certifications), `related_product` (accessory, required part, substitute), `item_group_title`, `variant_option`, and `popularity_rank`. They do not affect approval. `product_highlight` and `product_detail` are also used by AI Mode. — productsup (secondary, 2026-05). A secondary source says to add Q&A first, then relationships, then crawlable PDFs.
- **Perplexity.** Runs a free Merchant Program with zero commission. You apply, pass business verification, and send a CSV or XML feed by API, SFTP or S3. Instant Buy goes through PayPal/Venmo and the merchant stays merchant of record. — secondary: https://alhena.ai/blog/perplexity-shopping-merchants-setup-guide/ ; PayPal press release above (2025-11-25).
- **Amazon Alexa for Shopping (formerly Rufus).** It rewrites queries, reads title, bullets, description, A+ content, reviews and Q&A, and places weight on use cases. AMALYTIX reports that listings under 4.0★ are usually left out (**unverified**, agency observation). A 75-character title cap from 2026-07-27 appears in agency blogs only: **unverified**. — https://www.amalytix.com/en/knowledge/ai/amazon-rufus-guide-2026/

### A1.3 On-site PDP content that AI answers use

These are the passages AI answers lift. Each one should be a separate, crawlable text block, not a tab loaded by JS:

1. **Spec table** as real `<table>` or `<dl>`. Include units, dimensions, materials, compatibility and model numbers. Answers to "does X fit Y" come from this.
2. **"Who it's for / use cases"** paragraph. Rufus-style and ChatGPT-style reasoning matches on scenarios (secondary: Amazon listing guides; Profound deep dive https://www.tryprofound.com/blog/chatgpt-shopping-deep-dive).
3. **Comparison block** against sibling SKUs and the obvious rival ("X vs Y: choose X if…").
4. **Reviews in server-rendered HTML** with counts, averages and a sample of text. Reviews loaded client-side through a third-party widget are invisible to non-JS crawlers (see §0.2).
5. **Shipping and returns shown on the PDP** plus policy markup (below). Both the OpenAI feed and Google read return windows.
6. **Product Q&A** on the page, mirrored into Merchant Center `question_and_answer`.
7. **Identifiers**: GTIN, MPN and brand, in markup and in the feed.

### A1.4 Structured data for e-commerce (Google, current)

- **Variants:** `ProductGroup` + `hasVariant` + `variesBy` (color, size, suggestedAge, suggestedGender, material, pattern as full schema.org URLs) + `productGroupID`, which must match each variant's `inProductGroupWithID`. There are two supported layouts. On a single page with query-param variants, the ProductGroup has one canonical. On one page per variant, each page carries the full ProductGroup. — https://developers.google.com/search/docs/appearance/structured-data/product-variants (last updated 2026-09-08)
- **Returns:** `MerchantReturnPolicy` can sit at Organization level (since June 2024) or per Offer. `returnPolicyCountry` (ISO 3166-1 alpha-2) has been required since March 2025. — https://developers.google.com/search/docs/appearance/structured-data/return-policy ; SEJ https://www.searchenginejournal.com/google-updates-structured-data-requirements-for-return-policies/542080/
- **Shipping:** organization-level `ShippingService` goes under `Organization` (Nov 2025). Shipping and returns can also be set in Search Console. Product-level settings override organization-level ones. — https://developers.google.com/search/docs/appearance/structured-data/shipping-policy ; https://developers.google.com/search/blog/2025/11/more-ways-to-share-shipping
- **AI-generated product data and images:** Google asks for AI-generated images to carry IPTC metadata. Product data must be "specified separately and labeled as AI-generated". — https://developers.google.com/search/docs/fundamentals/using-gen-ai-content (last updated 2025-12-10)

Minimal PDP JSON-LD (single-page variants):

```json
{
  "@context": "https://schema.org",
  "@type": "ProductGroup",
  "name": "Trail Runner 3",
  "productGroupID": "TR3",
  "brand": {"@type": "Brand", "name": "Acme"},
  "description": "Lightweight trail shoe with 6mm drop…",
  "variesBy": ["https://schema.org/size", "https://schema.org/color"],
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.6, "reviewCount": 312},
  "hasVariant": [{
    "@type": "Product",
    "sku": "TR3-42-BLK", "gtin13": "0123456789012",
    "name": "Trail Runner 3 – Black, EU 42",
    "size": "42", "color": "Black",
    "image": "https://ex.com/img/tr3-blk.jpg",
    "inProductGroupWithID": "TR3",
    "offers": {
      "@type": "Offer",
      "url": "https://ex.com/p/trail-runner-3?color=black&size=42",
      "price": 459.00, "priceCurrency": "MYR",
      "availability": "https://schema.org/InStock",
      "itemCondition": "https://schema.org/NewCondition"
    }
  }]
}
```
Organization-level policy lives once, on the home or about page:
```json
{"@context":"https://schema.org","@type":"OnlineStore","name":"Acme","url":"https://ex.com",
 "hasMerchantReturnPolicy":{"@type":"MerchantReturnPolicy","applicableCountry":"MY","returnPolicyCountry":"MY",
   "returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow","merchantReturnDays":14,
   "returnMethod":"https://schema.org/ReturnByMail","returnFees":"https://schema.org/FreeReturn"}}
```

### A1.5 Category pages and UGC

- Category and listing pages win "best X under Y" answers when they include a **short server-rendered intro that answers the buying question**, a **filterable comparison table**, and crawlable pagination (`<a href>`, not infinite scroll only). Facet URLs: canonicalise to the clean URL, or `noindex` the combinations, and keep them out of the sitemap. This is standard Google guidance; no 2026-specific source.
- Across B2B and B2C, **listicles are the most-cited page type in ChatGPT, at 18.8%** (position.digital, 3,508 citations, July–Aug 2026, https://www.position.digital/blog/chatgpt-ranking-factors/). An owned "best X for Y" guide that honestly includes competitors is a legitimate asset.
- **Review content must be in the initial HTML.** Moderated UGC Q&A counts as fresh text. Mark up `Review`/`AggregateRating` only for reviews collected on-site about your own products. Self-serving reviews on LocalBusiness/Organization are not eligible for review snippets.

### A1.6 E-commerce checklist for the agent

- [ ] PDP, category and policy pages SSR or SSG. Price, stock, specs and reviews present in the raw HTML (`curl` test).
- [ ] ProductGroup/Product/Offer JSON-LD matching the visible price and stock. GTIN, brand, `priceValidUntil` where relevant.
- [ ] Organization-level return and shipping policy markup. Human-readable policy pages linked from every PDP.
- [ ] Merchant Center feed free of disapprovals. `product_highlight`/`product_detail` filled. Conversational attributes added for the top 20% of SKUs.
- [ ] robots.txt allows `OAI-SearchBot`, `PerplexityBot`, `Googlebot`, `Bingbot`, `Applebot`. Whether to allow the training bots is a business decision.
- [ ] If on Shopify: Agentic Storefronts left on. Product taxonomy category and metafields filled. See the Shopify section in Part B.

---

## A2. Local businesses

### A2.1 How the engines source local answers (dated)

- **Gemini / AI Mode / Google Maps** use Google Maps and Business Profile data. SOCi found Gemini's profile data was 100% accurate, against about 68% for ChatGPT and Perplexity (secondary report of SOCi/BrightLocal data). Google Maps "Ask Maps" gives conversational, Gemini-powered local recommendations (secondary, 2026). Since June 2026, GBP owners can connect their profile to Gemini to manage hours, posts, review replies and insights (secondary: https://www.seroundtable.com/google-business-profile-integrated-gemini-41484.html).
- **"Have AI check pricing" / "Let Google call"** began as the 2025 "Ask for Me" experiment. Google's AI phones local businesses about price and availability on the user's behalf. It picks businesses from normal local rankings. It is US-only and excludes some states. Businesses can turn it on or off under Business Profile › Advanced settings › "Google automated calls and text messages". — https://support.google.com/business/answer/16190256 ; https://support.google.com/websearch/answer/16421135 ; SEJ https://www.searchenginejournal.com/google-search-can-now-call-local-businesses-using-ai/551294/
- **ChatGPT.** OpenAI licensed **Yelp** data under a non-exclusive deal: 330M reviews and 8M+ listings, with Yelp branding and links shown, and "Request a Quote" coming. Axios reported it on 2026-07-23; Yelp first disclosed it in its Feb 2026 results. — https://www.axios.com/2026/07/23/yelp-reviews-chatgpt-geo-partnership ; https://finance.yahoo.com/media-advertising/articles/exclusive-yelp-deal-pushes-local-130005436.html. Earlier "ChatGPT local = Foursquare" claims are disputed (https://www.steadydemand.com/chatgpts-local-results-arent-coming-from-foursquare-and-probably-never-really-were/). ChatGPT's maps are drawn with Mapbox (secondary).
- **Apple (Siri / Maps / Apple Intelligence).** In April 2026 Apple merged Business Connect, Business Manager and Business Essentials into "Apple Business" (secondary, **unverified** against Apple). Square syncs hours, address and phone into Apple Business and Apple Maps (2026-09-24, https://www.theapplepost.com/2026/09/24/72644/square-adds-apple-business-integration-for-managing-apple-maps-listings/). Apple Maps Ads and a "Suggested Places" section in iOS 26.5 appear only in secondary sources: **unverified**.

### A2.2 How much harder AI visibility is than the local pack

- **SOCi 2026 Local Visibility Index** (2026-03-06; about 350k locations across 2,751 multi-location brands). Locations were recommended **1.2% of the time by ChatGPT, 11% by Gemini and 7.4% by Perplexity**, against 35.9% appearance in Google's 3-pack. SOCi names five factors (FACTS): Freshness, Authority (ratings, reviews, response patterns), Consistency (NAP across platforms), Trust, Semantic relevance. Recommended ChatGPT businesses averaged 4.3★. — https://www.soci.ai/blog/the-challenge-of-ai-visibility-for-brands-part-1/ ; SEL summary https://searchengineland.com/ai-local-visibility-report-2026-468085
- Steady Demand ran 1,487 queries across 50 US metros. ChatGPT and Gemini named the same top business in only **4.2%** of identical queries (secondary). Treat every engine as a separate channel.
- BrightLocal's 2026 industry report: "AI is more likely to strongly recommend a brand when it's mentioned on many cited source pages" (secondary quote). Third-party mentions (best-of lists, local press, directories) matter more than the business's own site.

### A2.3 Local playbook (agent-actionable vs owner-actionable)

The agent can do these on the website:
- One **location page per physical location**, server-rendered. Each has a unique NAP, embedded map, hours, services, parking and transit, area served, staff, local photos and a few location-specific FAQs.
- `LocalBusiness` subtype JSON-LD per location. Required: `name`, `address`. Recommended: `telephone`, `url` (the location's URL), `geo` (≥5 decimals), `openingHoursSpecification` (seasonal via `validFrom`/`validThrough`), `priceRange`, `servesCuisine`/`menu`, `department` named "{store} {dept}". — https://developers.google.com/search/docs/appearance/structured-data/local-business (last updated 2026-09-08). Link to the GBP, Apple and Yelp profiles with `sameAs`.
- **Service-area businesses** (plumbers, movers): no street address shown if hidden on GBP. Use `areaServed` (City/AdministrativeArea) and service pages per *service*, not doorway pages per suburb. Only build a city page when it carries real local proof (jobs done there, local testimonials).
- **Prices on the site** ("from RM X"). This gives AI summaries and Google's AI caller data to answer from.
- Keep NAP identical, character for character, across the site, schema, GBP, Apple Business, Yelp and Facebook. SOCi's Consistency factor is exactly this.

The owner must do these (the skill should output them as a to-do list):
- Complete the GBP: categories, services with prices, attributes, products, weekly photos, posts, Q&A, and **reply to every review**.
- Claim Apple Business, Bing Places and Yelp; Waze and Grab for Malaysia (below).
- Run a steady review programme. Recency matters (the F in FACTS).
- Decide on the automated-calls setting.

### A2.4 Malaysia specifics

- **Maps apps.** Waze is the #1 Maps & Navigation Android app in Malaysia (Similarweb ranking, Sept 2026, https://www.similarweb.com/top-apps/google/malaysia/maps-navigation/). Survey results conflict: one shows Google Maps at 67% vs Waze 12%, another says Waze leads (secondary: https://www.rankpage.com.my/business/waze-vs-google-maps/). Waze has about 6M MAU in MY (secondary, **unverified**). **Action:** claim and verify both GBP (which also feeds Gemini and AI Mode) and the **Waze** listing (Waze Ads / Waze for Cities; pins are community-edited). Check the Grab and Foodpanda listings for F&B. Apple Maps has a small share in MY; claim it anyway at low cost.
- **Google AI Mode** reached Malaysia in August 2025 in English. On 2025-10-08 it expanded to 35 more languages **including Malay**. — https://www.lowyat.net/2025/368877/google-ai-mode-more-languages-regions-supports-malay/. AI Overviews have supported Malay since May 2025 (https://blog.google/products-and-platforms/products/search/ai-overview-expansion-may-2025-update/). A secondary report says Malay-language queries still trigger AIO less reliably than English in mid-2026 (**unverified**).
- **The Malay → Indonesian bias.** In a 100-prompt test (Hiroki Nomoto, TUFS, reported by Arfadia), only 31% of answers came back in Bahasa Melayu and **66% in Bahasa Indonesia**. Indonesian outweighs Malaysian Malay about 9:1 in training data. False friends change meaning: *percuma* = free (MY) / useless (ID); *kereta* = car (MY) / train (ID). — https://www.arfadia.com/blog/malaysia-ai-language-bias-bahasa-melayu-html/ (fetched 2026-09-26; secondary report of academic work). **Action:** publish a real BM version with its own URLs and `hreflang="ms-MY"`. Write it in colloquial Malaysian with English trade terms, not *baku* and never Indonesian-flavoured. Use Malaysian place and unit terms (taman, jalan, Lembah Klang, RM). Test prompts in BM on each engine.
- Mixed-language queries are the norm ("kedai tayar murah near Puchong", "klinik gigi buka Ahad Shah Alam"). Put both registers in headings and FAQs. Include Malaysian NAP conventions: postcode, "Jalan", "Seksyen", state.

---

## A3. SaaS / B2B

### A3.1 Evidence

- **position.digital ChatGPT B2B SaaS study** (July 2026, updated 2026-08-12). 278 prompts, 6 categories, 3,508 citations from 2,845 pages. **42.6%** of citations came from DR 80+ pages. About 58% of pages ranking top-10 on Google are also cited by ChatGPT, yet brand-new sites with no traffic still get cited 11% of the time. Cited pages average 3.9 months old and 69.7% are under 12 months old; **documentation is older (17-month median) and still cited**. Pages naming 6+ brands averaged 2.13 citations vs 1.21 for pages naming none. Page types: **listicles 18.8%, service/product pages 18.6%, documentation 12.5%, review platforms only 1.6%**. **"66% of brand recommendations happen without ChatGPT citing that brand's website"**, so being recommended and being cited need separate work. — https://www.position.digital/blog/chatgpt-ranking-factors/
- VisibleIQ (2,020 citations, 75 buyer queries, 4 engines): **comparison pages were 42% of evaluation-stage citations**. At the decision stage, 80% of cited pages had concrete pricing tiers, benchmarks, G2 scores or ROI numbers (secondary via https://www.averi.ai/…; **unverified**, as I did not reach the primary).
- **G2** bought Capterra, Software Advice and GetApp from Gartner in February 2026 (secondary: https://beomniscient.com/blog/g2-acquisition-ai-citation-share/). Semrush (2025-11-10) put G2 in the top 20 most-cited domains across AI platforms (secondary). Evidence that G2 profiles *directly* lift ChatGPT recommendations conflicts (https://strivelabs.ai/blog/g2-capterra-ai-answers/). position.digital found review platforms made up only 1.6% of citations. **Guidance:** keep the G2 profile current and accurate because it is read for "[brand] reviews" and proof prompts. It is table stakes, not the main lever.
- **Docs are AI fuel, and coding agents are the llms.txt audience** (Ahrefs, §0.5). Next.js's own docs now ship `/docs/llms.txt`, `/docs/sitemap.md` and markdown frontmatter with `version`/`lastUpdated` on every page. I confirmed this by fetching nextjs.org docs on 2026-09-26: the responses start with `docs_index: /docs/llms.txt` and `lastUpdated`. This is the reference pattern to copy.

### A3.2 Page types to build (in priority order)

1. **Pricing page with numbers in HTML.** Tier names, prices, limits, what "contact sales" means, and a comparison table. Decision-stage citations need concrete numbers.
2. **"X vs Competitor" and "Competitor alternatives" pages.** One per real competitor. Include a fair feature table, "who should pick them", migration steps, and a date stamp. These should name many entities (the entity-richness finding).
3. **Integration pages**, one per integration: what syncs, the direction, setup steps, limits. They answer "does X integrate with Y" prompts.
4. **Use-case / industry pages** built around a problem, with a customer quote and a metric.
5. **Documentation** that is public, SSR/SSG, and has a stable URL per concept. Add a `lastUpdated` date, `/llms.txt` + `/llms-full.txt`, `.md` alternates or `Accept: text/markdown` negotiation, and copyable code blocks. Optionally a hosted **MCP server** for docs or product search. Nuxt AI Ready and Mintlify-style stacks generate these.
6. **Changelog / release notes**, dated, as a freshness signal.
7. **Trust pages**: security/compliance (SOC 2, ISO), status page, customers.
8. `SoftwareApplication` JSON-LD (offers, operatingSystem, applicationCategory), plus `Organization` with `sameAs` to G2, LinkedIn, GitHub and Crunchbase.

---

## A4. Publishers, blogs and media

### A4.1 Traffic impact (dated)

- **Pew Research** (browsing data from 900 US adults, March 2025, published 2025-07-22). Users clicked a traditional result on **8%** of searches that showed an AI summary vs **15%** without one. They clicked a link *inside* the summary on **1%** of visits. They ended the session after a summary page 26% of the time vs 16%. AIO appeared on 8% of 1–2-word queries, 53% of 10+-word queries and 60% of question queries. — https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/
- **Chartbeat** (via Reuters Institute and Axios, 2026-03-17). Google organic traffic to about 2,500 publishers fell **33% globally and 38% in the US**, Nov 2024 → Nov 2025. Over two years, small publishers lost 60%, medium 47% and large 22%. Chatbot referrals grew more than 200% but are still **under 1%** of referrals. — https://www.axios.com/2026/03/17/chartbeat-search-traffic-ai-chatbots (403 on fetch; figures from https://ppc.land/small-publishers-lost-60-of-search-traffic-as-ai-reshapes-the-web/ and https://almcorp.com/blog/search-traffic-decline-small-publishers-chartbeat-data/)
- Ahrefs: position-1 CTR falls about 58% when an AIO is present (secondary citation).

### A4.2 Licensing landscape

- OpenAI has about 24 disclosed deals. The largest is News Corp, reportedly $250M over 5 years. Microsoft and Meta have about 12 each. Meta reportedly pays up to $50M/yr for 3 years from March 2026. NYT → Amazon is reportedly $20–25M/yr (May 2025). **Microsoft Publisher Content Marketplace** (Feb 2026) is a click-to-sign, pay-per-use marketplace (secondary; not verified against Microsoft). — https://llmpulse.ai/blog/ai-content-licensing-deals/ ; https://mediaandthemachine.substack.com/p/ai-content-licensing-deals-june-2026 ; https://digiday.com/media/meta-enters-ai-licensing-fray-striking-deals-with-people-inc-usa-today-co-and-more/
- For small publishers, licensing is not realistic. The levers they have are crawler policy (search bots vs training bots), Cloudflare pay-per-crawl or blocking, and `Content-Signal` lines in robots.txt (covered by other researchers).

### A4.3 What still earns citations and visits

- **Original reporting, data, first-hand testing and expert quotes.** The raters' E-E-A-T trust standard (A5) and the entity-rich, fresh pattern (A3) both favour this. Commodity explainers are what AIO absorbs (Pew: question queries trigger AIO 60% of the time).
- **Freshness and dates.** Visible "Updated" dates plus `dateModified` in `Article`/`NewsArticle` JSON-LD. Only change them on a substantive edit.
- **Named authors** with author pages (`Person`, `sameAs`, credentials), and "how we tested" or methodology boxes. This is Google's Who/How/Why (https://developers.google.com/search/docs/fundamentals/creating-helpful-content, last updated 2025-12-10).
- **Preferred Sources** (Google, 2025-08-12, US and India first). Publishers can embed an "Add as a preferred source on Google" button to gain Top Stories prominence among loyal readers. — https://blog.google/products/search/preferred-sources/
- **Direct channels** (newsletter, app, community) to hedge the fall in search clicks.
- **Technical:** SSR article HTML; no paywall script that hides the text from crawlers without `isAccessibleForFree`/`hasPart` paywall markup; fast AMP-free pages; a Google News sitemap for news sites.

---

## A5. Professional services / YMYL (health, finance, legal)

### A5.1 The bar (primary sources)

- **Search Quality Rater Guidelines, version dated 2025-09-11** (PDF downloaded and text-extracted 2026-09-26: https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf). There are four YMYL harm types: **Health or Safety; Financial Security; Government, Civics & Society** (explicitly election and voting information); **Other**. "Pages on clear YMYL topics require the most scrutiny". "For pages about clear YMYL topics, we have very high Page Quality rating standards". §3.4.1 *Experience or Expertise?*: first-hand life-experience pages on YMYL topics "may be considered to have high E-E-A-T as long as the content is trustworthy, safe, and consistent with well-established expert consensus… In contrast, some types of YMYL information and advice must come from experts".
- Google Search Central: "Of these aspects, trust is most important". YMYL is defined as topics "that could significantly impact the health, financial stability, or safety of people, or the welfare or well-being of society". It also asks whether "the use of automation, including AI-generation, [is] self-evident to visitors". — https://developers.google.com/search/docs/fundamentals/creating-helpful-content (2025-12-10)
- Mass-produced AI pages that add no value can count as "scaled content abuse". — https://developers.google.com/search/docs/fundamentals/using-gen-ai-content (2025-12-10)

### A5.2 Implementation pattern for YMYL pages

Visible on the page, server-rendered:
- **Byline** that links to an author page (credentials, licence numbers, registrations such as the MMC or MDC number in Malaysia, the Bar Council, a Securities Commission licence, or a BNM-licensed entity). Add a **"Medically / legally / financially reviewed by"** line naming a credentialed reviewer, plus a **last-reviewed date**.
- **Sources and citations** to primary literature, regulators and statutes, with dates.
- **Disclaimer** kept in context ("general information, not advice; consult…"). It should be specific, not boilerplate that swamps the content.
- **Who runs the site**: About page, physical address, regulator registrations, complaints process, editorial policy, corrections policy. The rater guidelines tell raters to look for these (§2.5.2, §2.5.3).
- For clinics and firms, **practitioner pages**: qualifications, memberships, languages, locations (links to A2).

JSON-LD pattern:
```json
{"@context":"https://schema.org","@type":"MedicalWebPage",
 "headline":"Dengue fever: warning signs in adults",
 "lastReviewed":"2026-09-01",
 "reviewedBy":{"@type":"Person","name":"Dr. Aisyah Rahman","jobTitle":"Consultant Physician",
   "hasCredential":{"@type":"EducationalOccupationalCredential","credentialCategory":"MMC registration"},
   "sameAs":["https://www.linkedin.com/in/…"]},
 "author":{"@type":"Organization","name":"Klinik Contoh","url":"https://ex.my"},
 "about":{"@type":"MedicalCondition","name":"Dengue fever"}}
```
`reviewedBy` and `lastReviewed` are properties of schema.org `WebPage`. Google does not produce a rich result for them. They make the review relationship machine-readable, but they **only help if the same facts are visible on the page**. For finance use `WebPage`/`Article` (plus `FinancialService` for the firm). For legal use `LegalService`/`Attorney` (Attorney is deprecated in schema.org; prefer `LegalService` plus `Person`).

---

# PART B — Framework implementation guide

Legend for each stack: **T/M** = title and meta; **C** = canonical; **RM** = robots meta; **R** = robots.txt; **S** = sitemap; **J** = JSON-LD; **OG** = OG images; **H** = hreflang; **SSR** = rendering; **L** = llms.txt / markdown alternates; **Rd** = redirects; **X** = response headers (X-Robots-Tag).

Universal test for any stack: `curl -sA "GPTBot" https://site/page | grep -E "<title>|canonical|ld\+json|<h1"`. If this is empty, AI crawlers see nothing (§0.2).

## B1. Next.js (App Router; docs version 16.3.6, fetched 2026-09-26)

```ts
// app/layout.tsx — root
import type { Metadata } from 'next'
export const metadata: Metadata = {
  metadataBase: new URL('https://ex.com'),       // required for relative URLs
  title: { default: 'Acme', template: '%s | Acme' },
  description: '…',
  openGraph: { siteName: 'Acme', type: 'website' },
  // NOTE: do NOT set alternates.canonical here (see traps)
}

// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `/blog/${slug}`,
      languages: { 'en-MY': `/blog/${slug}`, 'ms-MY': `/ms/blog/${slug}` },
      types: { 'text/markdown': `/blog/${slug}.md` },   // markdown alternate
    },
    robots: post.draft ? { index: false, follow: true } : undefined,
    openGraph: { title: post.title, type: 'article', publishedTime: post.date },
  }
}
export async function generateStaticParams() { return (await allSlugs()).map(slug => ({ slug })) }
export const revalidate = 3600 // ISR
```
- **J:** use a native `<script type="application/ld+json">` in the server component, with `JSON.stringify(jsonLd).replace(/</g, '\\u003c')` to prevent XSS. Type it with `schema-dts`. Do **not** use `next/script`. — https://nextjs.org/docs/app/guides/json-ld (lastUpdated 2026-03-02)
- **R / S:** `app/robots.ts` returns `{ rules: [{ userAgent: '*', allow: '/' }, { userAgent: 'GPTBot', disallow: '/' }], sitemap: 'https://ex.com/sitemap.xml' }`. `app/sitemap.ts` returns `[{ url, lastModified, alternates: { languages } }]`. For more than 50k URLs use `generateSitemaps()`.
- **OG:** `opengraph-image.tsx` with `ImageResponse` in a route segment.
- **Rd:** `redirects()` in `next.config` (`permanent: true` → 308), or `permanentRedirect()` in a server component. **X:** `headers()` in `next.config`, e.g. `{ source: '/admin/:path*', headers: [{ key: 'X-Robots-Tag', value: 'noindex' }] }`.
- **L / markdown negotiation** (Vercel pattern):
```ts
// next.config.ts
async rewrites() { return { beforeFiles: [
  { source: '/docs/:path*', has: [{ type: 'header', key: 'accept', value: '(.*)text/markdown(.*)' }],
    destination: '/md/docs/:path*' } ] } }
```
Add `app/llms.txt/route.ts` that returns `text/plain`, and `app/md/[...slug]/route.ts` that returns `text/markdown; charset=utf-8`.

**Next.js traps**
1. **Metadata merges shallowly.** Nested objects (`openGraph`, `robots`, `alternates`) are **replaced whole** by the last segment that sets them. A child that sets `openGraph.title` loses the layout's `openGraph.images`. — generate-metadata docs "Merging". **A canonical set in a layout is inherited by every child that doesn't override it, so every page canonicalises to the homepage.** Set canonical per page, never in the root layout.
2. **Streaming metadata (v15.2+).** When `generateMetadata` is dynamic, Next.js sends the UI first and **appends the metadata tags to `<body>`**. It only blocks, and puts tags in `<head>`, for UAs matching the `htmlLimitedBots` list. The default list covers Google-*, Bingbot, applebot, facebookexternalhit, Twitterbot, Slackbot, etc. **It does not include GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User or PerplexityBot** (list fetched from the canary `html-bots.ts` on 2026-09-26). Those bots don't run JS, so they get title and canonical in the body. **Fix:** make metadata static or `'use cache'`d so it prerenders into `<head>`, or override the list:
```ts
// next.config.ts — overriding REPLACES the default list, so re-include the defaults
htmlLimitedBots: /Googlebot|[\w-]+-Google|Google-[\w-]+|Bingbot|applebot|facebookexternalhit|Twitterbot|LinkedInBot|Slackbot|Discordbot|WhatsApp|GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-User|Claude-SearchBot|PerplexityBot|Perplexity-User|CCBot|Amazonbot|meta-externalagent|DuckAssistBot|MistralAI-User/i,
```
   (`/.*/` turns streaming off for everyone.) — https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots (2025-10-03)
3. **`'use client'` pages** that fetch content in `useEffect` are empty to AI crawlers. Move data fetching into server components.
4. **`trailingSlash`** defaults to false. Pick one value and make canonical, sitemap and internal links agree. `metadataBase` normalises slashes between base and path.
5. With **Cache Components**, runtime data in `generateMetadata` raises a build error unless it is cached or explicitly deferred. Under `'use cache'`, return `metadataBase` as a string, not a `URL`.
6. Put `notFound()` before any output so the page returns a real 404. Soft-404 "not found" UIs that return 200 get indexed.

## B2. Nuxt 3 / 4

- Install: `npx nuxt module add @nuxtjs/seo`. This bundles `@nuxtjs/robots` (robots.txt, `<meta name="robots">` **and `X-Robots-Tag` headers**), `@nuxtjs/sitemap` (i18n), `nuxt-og-image`, `nuxt-schema-org`, `nuxt-link-checker`, `nuxt-seo-utils`, `nuxt-site-config`. The separate **Nuxt AI Ready** module generates `/llms.txt`, `/llms-full.txt`, `.md` alternates (`/about.md`), an optional MCP server and Content Signals in robots.txt. — https://nuxtseo.com/docs/nuxt-seo/getting-started/introduction ; https://nuxtseo.com/docs/ai-ready/getting-started/introduction (fetched 2026-09-26)
```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo'],
  site: { url: 'https://ex.com', name: 'Acme', defaultLocale: 'en' }, // single source for canonical/sitemap/OG
  schemaOrg: { identity: { type: 'Organization', name: 'Acme', logo: '/logo.png', url: 'https://ex.com' } },
  robots: { groups: [{ userAgent: ['GPTBot'], disallow: ['/'] }] },
  routeRules: {
    '/blog/**': { prerender: true },              // or isr: 3600 / swr
    '/admin/**': { robots: false },               // → noindex meta + X-Robots-Tag
    '/old': { redirect: { to: '/new', statusCode: 301 } },
  },
})
```
```vue
<script setup lang="ts">
const { data: post } = await useAsyncData(() => $fetch(`/api/posts/${useRoute().params.slug}`))
useSeoMeta({ title: () => post.value?.title, description: () => post.value?.excerpt,
  ogTitle: () => post.value?.title, ogImage: () => post.value?.cover })
useHead({ link: [{ rel: 'canonical', href: `https://ex.com/blog/${useRoute().params.slug}` }] })
useSchemaOrg([defineArticle({ headline: () => post.value?.title, datePublished: () => post.value?.date })])
</script>
```
**Traps:**
- Use `useAsyncData`/`useFetch`, never `onMounted`, so data and meta exist during SSR.
- `ssr: false` or `.client.vue` content is invisible to AI crawlers.
- **runtimeConfig:** only `NUXT_*` environment variables override at runtime. `process.env` read inside `nuxt.config` is baked in at build time, so the wrong site URL can end up in canonicals and sitemaps. Set `NUXT_SITE_URL` / `NUXT_PUBLIC_SITE_URL` in production.
- For static hosting, `nuxi generate` needs every dynamic route discoverable by links or listed in `nitro.prerender.routes`.

## B3. Astro

- It is static by default, which is ideal for AI crawlers. `site` in `astro.config` is required. Sitemap: `npx astro add sitemap` (v3.7.4). Options include `filter`, `serialize`, `i18n`, `entryLimit` (45,000). It **cannot list dynamic routes in SSR mode**. — https://docs.astro.build/en/guides/integrations-guide/sitemap/ (fetched 2026-09-26)
```astro
---
// src/layouts/Base.astro
const { title, description, jsonLd, noindex = false } = Astro.props
const canonical = new URL(Astro.url.pathname, Astro.site)
---
<head>
  <title>{title}</title><meta name="description" content={description} />
  <link rel="canonical" href={canonical} />
  {noindex && <meta name="robots" content="noindex,follow" />}
  <link rel="alternate" hreflang="ms-MY" href={new URL(`/ms${Astro.url.pathname}`, Astro.site)} />
  {jsonLd && <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />}
</head>
```
- robots.txt: `public/robots.txt`, or `src/pages/robots.txt.ts` exporting `GET`. llms.txt and `.md`: endpoints `src/pages/llms.txt.ts` and `src/pages/[...slug].md.ts` built from `getCollection()`. Redirects go in `redirects: {}` in `astro.config` (static output writes meta-refresh pages unless the adapter supports real 301s). Headers come from the host (`_headers` on Netlify/CF, `vercel.json`).
- **Traps:**
  - `client:only` islands render nothing on the server.
  - Set `trailingSlash` (`'always'|'never'|'ignore'`) and `build.format` so they agree.
  - `set:html` with JSON-LD needs the same `<` escaping as Next.js when the data comes from users or a CMS.

## B4. SvelteKit

- Page options: `export const prerender = true | false | 'auto'`, with `entries()` for dynamic params. Pages with form actions cannot be prerendered. `ssr = false` gives an empty shell. `csr = false` ships no JS. `trailingSlash = 'never'` (default) | `'always'` | `'ignore'`, and "/x" and "/x/" are different URLs. — https://svelte.dev/docs/kit/page-options (fetched 2026-09-26)
```svelte
<!-- +page.svelte -->
<script>let { data } = $props();</script>
<svelte:head>
  <title>{data.post.title} | Acme</title>
  <meta name="description" content={data.post.excerpt} />
  <link rel="canonical" href={`https://ex.com/blog/${data.post.slug}`} />
  {@html `<script type="application/ld+json">${JSON.stringify(data.jsonLd).replace(/</g,'\\u003c')}</script>`}
</svelte:head>
```
- robots.txt, sitemap.xml and llms.txt: `src/routes/sitemap.xml/+server.ts` with `export const prerender = true`, returning a `Response` with the right `content-type`. X-Robots-Tag: `setHeaders({ 'x-robots-tag': 'noindex' })` in `load`, or in the `handle` hook. Redirects: `redirect(301, '/new')` from `load`.

## B5. Remix → React Router 7 (framework mode)

- Meta: `export const meta: Route.MetaFunction = ({ data }) => [{ title: data.post.title }, { name: 'description', content: … }, { tagName: 'link', rel: 'canonical', href: … }, { 'script:ld+json': jsonLd }]`. React 19 `<title>`/`<meta>` hoisting also works inside components.
- Prerender config in `react-router.config.ts`: `prerender: true | string[] | async ({ getStaticPaths }) => [...]`, with an optional `concurrency`. With `ssr: false` + `prerender` you get a static build, and non-prerendered paths fall back to `__spa-fallback.html`, which **is an empty shell for crawlers**. Output is `build/client/[url].html`. — https://reactrouter.com/how-to/pre-rendering (fetched 2026-09-26)
- Headers: `export const headers = () => ({ 'X-Robots-Tag': 'noindex' })` (needs SSR). Redirects: `throw redirect('/new', 301)` in the loader. robots.txt and sitemap: resource routes (`app/routes/sitemap[.]xml.ts` exporting `loader`).
- **Trap:** meta from a parent route is **not merged** automatically. Each leaf returns its full list; spread `matches` if you need the parent's tags.

## B6. Plain Vite React / Vue SPAs (the riskiest stack)

A pure SPA sends `<div id="root"></div>` to GPTBot, ClaudeBot and PerplexityBot (§0.2). Options, best first:
1. **Migrate the marketing, docs and product surface to a meta-framework** (Next, Nuxt, Astro, React Router 7 framework mode) and keep the app itself as an SPA.
2. **Build-time prerender inside Vite:**
   - **Vike** (formerly `vite-plugin-ssr`): `// pages/+config.js export default { prerender: true }`, then `vike build` writes `dist/client/*.html`. Partial prerender is supported. — https://vike.dev/pre-rendering (fetched 2026-09-26)
   - Vue: **vite-ssg** (static generation for Vue + vue-router, with `@unhead/vue` for head tags).
   - React: React Router 7's `prerender` also works for Vite SPAs moving to framework mode.
3. **Headless-browser snapshot at build time**, e.g. a Puppeteer/Playwright script that visits the route list and writes HTML. **react-snap is unmaintained** (last release 2019; **unverified** exact date). Avoid it for new work.
4. **Dynamic rendering / prerender services** (prerender.io, self-hosted Rendertron): these are workarounds. Google says dynamic rendering is not a long-term solution, and Rendertron is archived (§0.3). Use only as a stop-gap. You must include the AI bot UAs in the service's bot list, because many default lists only cover search and social bots.

In an SPA, meta can be managed with `react-helmet-async` or React 19 native `<title>`; for Vue, `@unhead/vue`. **These only help crawlers once the page is prerendered.** Every route must return correct status codes; SPA hosts that answer 200 with `index.html` for unknown paths create soft 404s.

## B7. Gatsby

- Use the `Head` export (Gatsby 4.19+; `react-helmet` is legacy): `export const Head = ({ data }) => (<><title>…</title><link rel="canonical" href=… /><script type="application/ld+json">{JSON.stringify(ld)}</script></>)`. Sitemap: `gatsby-plugin-sitemap`. robots.txt: `gatsby-plugin-robots-txt` or `static/robots.txt`. Redirects: `createRedirect` in `gatsby-node` (the host adapter must support it). Output is SSG, which is good. **Maintenance risk:** framework activity has been low since the Netlify acquisition (2023) (**unverified** current status). For new builds prefer Astro or Next.

## B8. WordPress

- **Rendering:** server-rendered PHP, so fine by default. Check page builders and block themes that lazy-render content with JS (Elementor "loop" widgets, review plugins, tabs that load over AJAX).
- **Yoast:** llms.txt is available in **Free, Premium, WooCommerce SEO, AI+, and Yoast for Shopify**. Enable it in Site features with one click. — https://yoast.com/features/llms-txt/ (fetched 2026-09-26). Yoast's schema graph outputs WebSite, Organization/Person, WebPage, Article and BreadcrumbList linked by `@id`. Extend it with the `wpseo_schema_graph` filter instead of adding separate blobs.
- **Rank Math:** "LLMS Txt" module. You choose post types and taxonomies and a limit (default 100), and can add custom content. — https://rankmath.com/kb/llms-txt/ (fetched 2026-09-26)
- **AIOSEO:** also generates llms.txt (**unverified**; not fetched).
- **robots.txt:** WordPress serves a virtual file. Edit it with the SEO plugin's editor or the `robots_txt` filter. A physical file in the web root overrides both. **Sitemap:** core `wp-sitemap.xml` (5.5+), or the plugin's sitemap. Use one, not both. **Redirects:** Redirection plugin or Yoast/Rank Math redirect managers (server-level on nginx for speed). **X-Robots-Tag:** `add_action('send_headers', …)` or the server config. **Traps:**
  - "Discourage search engines" left on after launch (Settings › Reading).
  - Attachment pages indexed.
  - Duplicate JSON-LD from theme plus plugin, e.g. two Organization nodes.
  - WooCommerce product schema without `hasMerchantReturnPolicy` / `shippingDetails`. Add these through the plugin's Woo module or a filter.

## B9. Shopify

- **AI channels:** Agentic Storefronts / Shopify Catalog syndicate products to ChatGPT, Copilot, AI Mode and Gemini, switched on automatically (Settings › Sales Channels › Agentic Storefronts). Discovery depends on "product titles, descriptions, images, pricing, inventory, shipping speeds". Catalog infers extra attributes. — https://www.shopify.com/blog/how-agentic-commerce-works (2026-06-18). For developers: UCP plus Catalog, Cart, Checkout and Order MCP servers (`npm i -g @shopify/ucp-cli`). — https://shopify.dev/docs/agents (fetched 2026-09-26). **Levers:** complete the **Standard Product Taxonomy category** and category metafields (color, material, size), GTIN/barcode, and real variant options.
- **JSON-LD:** in theme Liquid, `<script type="application/ld+json">{{ product | structured_data }}</script>` (the `structured_data` filter also covers `article`). Or hand-write it and add `hasMerchantReturnPolicy`/`shippingDetails` and the ProductGroup variant structure. Check that the theme and apps don't output duplicate Product blocks, which is common with review apps.
- **robots.txt:** create `templates/robots.txt.liquid`. Keep the Liquid default groups and add to them rather than hard-coding. — https://shopify.dev/docs/storefronts/themes/seo/robots-txt
```liquid
{% for group in robots.default_groups %}
  {{- group.user_agent }}
  {%- for rule in group.rules -%}
    {{ rule }}
  {%- endfor -%}
  {%- if group.user_agent.value == '*' -%}
    {{ 'Disallow: /*?*filter*' }}
  {%- endif -%}
  {%- if group.sitemap != blank -%}
    {{ group.sitemap }}
  {%- endif -%}
{% endfor %}
User-agent: GPTBot
Disallow: /checkouts/
```
- **Sitemap** is automatic (`/sitemap.xml`). **Redirects:** Admin › Navigation › URL Redirects (they only fire when the old path 404s). **Canonical:** themes output `{{ canonical_url }}`. **Trap:** collection-scoped product URLs (`/collections/x/products/y`) are canonicalised to `/products/y`. Keep internal links on the canonical form. **hreflang:** Shopify Markets outputs it automatically for market subfolders or domains. **Meta robots:** use `seo.hidden` metafield = 1 to noindex a resource. **llms.txt:** Yoast for Shopify can generate it. Shopify does not let you write arbitrary root files, so serve other formats through an app proxy (**unverified** whether Shopify now auto-serves `/llms.txt`).

## B10. Webflow

- Per-page SEO settings (title, description, OG). CMS templates bind these to fields. **Canonical:** global canonical in Site settings › SEO, plus a per-page override. **robots.txt:** Site settings › SEO editor. **Sitemap:** auto-generated, with a per-page "exclude from sitemap" option. **Redirects:** Site settings › Publishing › 301 redirects (wildcard capture groups supported). **JSON-LD:** page custom code "Inside <head>", using CMS field embeds for dynamic templates. **Rendering:** static HTML, good for AI crawlers. **llms.txt:** Webflow reportedly supports uploading llms.txt in SEO settings (**unverified**; help-centre fetch returned 403). **Traps:**
  - Localization: hreflang is auto-generated only with Webflow Localization.
  - The staging `*.webflow.io` domain must be noindexed (there is a setting). Otherwise it duplicates the live site.

## B11. Wix

- Server-rendered. SEO settings per page and per page type through "SEO patterns". There is a robots.txt editor and auto sitemap. Structured data: per-page "Advanced SEO › Structured data markup" (custom JSON-LD), and Wix Stores/Bookings output their own Product/LocalBusiness data. 301 manager in the SEO dashboard. Wix auto-generating llms.txt: **unverified** (help URL 404 on fetch). **Trap:** duplicate structured data when custom JSON-LD overlaps the app-generated blocks. Check with the Rich Results Test.

## B12. Squarespace

- **robots.txt is not directly editable.** The only control is Settings › Crawlers › "Block known artificial intelligence crawlers" (about 25 bots including GPTBot, ClaudeBot and Amazonbot). It is **off by default** because blocking can cut AI-search traffic. llms.txt is not mentioned. — https://support.squarespace.com/hc/en-us/articles/360022347072 (fetched 2026-09-26). JSON-LD goes in Code Injection (per-page header injection needs a Business plan or higher; **unverified** tier naming). URL Mappings handle 301s. **Trap:** a merchant who ticks the AI-crawler box blocks the retrieval bots too, not just the training bots, and falls out of ChatGPT and Perplexity answers.

## B13. Framer

- Static SSR output (good). Page SEO fields, CMS-bound meta, custom `<head>` code for JSON-LD, redirects in site settings, auto sitemap. Custom robots.txt and llms.txt support: **unverified** (help URL 404). **Trap:** heavy animation components that mount their text client-side. Check with `curl`.

## B14. Ghost

- "Themes can include a robots.txt which overrides the default". `{{ghost_head}}` is required in templates. It outputs canonical, OG, Twitter and Article/Person JSON-LD automatically. — https://docs.ghost.org/themes/structure/ (fetched 2026-09-26). Sitemap is automatic at `/sitemap.xml`. Redirects come from an uploaded `redirects.yaml` (Labs/Settings). Per-post meta and canonical override in the post settings. llms.txt: add it as a theme static file or through a proxy (**unverified**, no native feature seen). **Trap:** members-only posts serve a truncated body to crawlers. Use a public preview section and paywall markup.

## B15. Hugo / Jekyll / 11ty (static generators)

- **Hugo:** `enableRobotsTXT = true`. Custom template at `layouts/robots.txt`, or a static file in `/static` with the flag off. — https://gohugo.io/templates/robots/ (fetched 2026-09-26). The sitemap is built in (`sitemap.xml`, multilingual index). Use `{{ .Permalink }}` for canonical. hreflang: range over `.Translations`. Redirects: `aliases:` in front matter (meta-refresh) or a host `_redirects` file. **llms.txt / markdown alternates:** define custom **output formats** (`[outputFormats.markdown] mediaType="text/markdown" baseName="index"`) and add them to `outputs.page`. Hugo then writes `index.md` next to `index.html`.
- **Jekyll:** `jekyll-seo-tag` (title, canonical, OG, JSON-LD) plus `jekyll-sitemap`. Put robots.txt in the root with front matter to template it. Redirects via `jekyll-redirect-from` (meta-refresh; use host rules for real 301s).
- **11ty:** set `permalink: /robots.txt` / `/sitemap.xml` / `/llms.txt` in Nunjucks templates that iterate `collections.all`. `@11ty/eleventy-plugin-rss` for feeds. JSON-LD in the base layout with `{{ data | dump | safe }}`. Escape `<` if content can hold it.
- **Shared static-site traps:**
  - Meta-refresh "redirects" are not 301s. Use host rules (Netlify `_redirects`, Cloudflare Pages `_redirects`, `vercel.json`).
  - Set X-Robots-Tag through the host `_headers` file.
  - Keep `baseURL`/`url` correct per environment, or canonicals will point at localhost or staging.

## B16. Cross-framework trap register (use as a lint list)

| # | Trap | Where seen | Detect | Fix |
|---|---|---|---|---|
| 1 | Canonical set in a shared layout, inherited by all children → every page canonicalises to `/` | Next.js layouts; Nuxt `app.vue` `useHead`; Astro base layout with a hard-coded href | crawl and compare canonical to URL | compute per page from the route |
| 2 | Metadata in `<body>` for AI bots (Next streaming) | Next 15.2+ dynamic `generateMetadata` | `curl -A GPTBot` and check `<head>` | static or cached metadata, or extend `htmlLimitedBots` |
| 3 | Client-only content / reviews / JSON-LD | SPAs, `'use client'`, `ssr:false`, `client:only`, review widgets | `curl` without JS | SSR/SSG, or server-fetch the reviews |
| 4 | Trailing-slash mismatch between canonical, sitemap and links | all | sitemap vs canonical diff | one setting (`trailingSlash`) plus a 301 for the other form |
| 5 | Build-time env baked into canonicals and sitemaps (localhost, staging) | Nuxt `process.env` in config; SSGs | grep the built HTML for localhost or staging | runtime env (`NUXT_*`), per-env `site.url` |
| 6 | Soft 404s (200 + "not found") | SPAs, catch-all routes | fetch a random path and check the status | `notFound()`, `error(404)`, host 404 rules |
| 7 | JS-injected `noindex` removed later | SPAs | Google may skip rendering after noindex | decide noindex on the server |
| 8 | Duplicate JSON-LD (theme + plugin + app) | WordPress, Shopify, Wix | Rich Results Test, count `@type:Product` | one source of truth, `@id` graph |
| 9 | Staging domain indexed | Webflow `.webflow.io`, Vercel previews, Netlify deploy previews | `site:` search | `X-Robots-Tag: noindex` on non-prod hosts |
| 10 | Blocking all AI bots with one toggle (loses retrieval as well as training) | Squarespace toggle, Cloudflare "block AI bots" | read robots.txt | separate training UAs (GPTBot, ClaudeBot, CCBot, Google-Extended) from search and user UAs (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot) |
| 11 | Unescaped `</script>` in JSON-LD from CMS data → XSS or broken markup | all JSX, `set:html`, `{@html}` | fuzz with `</script>` | `.replace(/</g,'\\u003c')` |
| 12 | Nested metadata objects wiped by a child (lost OG image) | Next shallow merge | inspect og:image per route | shared constants spread into each page |

---

## Source list (by section; access date 2026-09-26 unless stated)

Primary / official:
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features (2025-12-10)
- Google helpful content / E-E-A-T: https://developers.google.com/search/docs/fundamentals/creating-helpful-content (2025-12-10)
- Google gen-AI content: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content (2025-12-10)
- Google JS SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Google dynamic rendering: https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering (2025-12-10)
- Google product variants: https://developers.google.com/search/docs/appearance/structured-data/product-variants (2026-09-08)
- Google LocalBusiness: https://developers.google.com/search/docs/appearance/structured-data/local-business (2026-09-08)
- Google shipping/returns: https://developers.google.com/search/blog/2025/11/more-ways-to-share-shipping ; https://developers.google.com/search/docs/appearance/structured-data/return-policy ; https://developers.google.com/search/docs/appearance/structured-data/shipping-policy
- Rater guidelines (2025-09-11): https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf
- Google UCP: https://developers.google.com/merchant/ucp ; https://blog.google/products-and-platforms/products/shopping/ucp-updates/ (2026-03-19) ; https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/ (I/O 2026) ; https://support.google.com/merchants/answer/16837055
- Google automated calls: https://support.google.com/business/answer/16190256 ; https://support.google.com/websearch/answer/16421135
- Google Preferred Sources: https://blog.google/products/search/preferred-sources/ (2025-08-12)
- AIO languages: https://blog.google/products-and-platforms/products/search/ai-overview-expansion-may-2025-update/
- OpenAI product feed: https://developers.openai.com/commerce/specs/file-upload/products ; https://openai.com/index/buy-it-in-chatgpt/ ; ACP spec: https://agentic-commerce-protocol.com/docs/commerce/specs/feed
- PayPal × Perplexity: https://newsroom.paypal-corp.com/2025-11-PayPal-and-Perplexity-Launch-Instant-Buy (2025-11-25)
- Shopify: https://www.shopify.com/blog/how-agentic-commerce-works (2026-06-18) ; https://shopify.dev/docs/agents ; https://shopify.dev/docs/storefronts/themes/seo/robots-txt
- Next.js: https://nextjs.org/docs/app/api-reference/functions/generate-metadata (16.3.6, 2026-08-25) ; https://nextjs.org/docs/app/guides/json-ld (2026-03-02) ; https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots ; https://raw.githubusercontent.com/vercel/next.js/canary/packages/next/src/shared/lib/router/utils/html-bots.ts
- Nuxt SEO: https://nuxtseo.com/docs/nuxt-seo/getting-started/introduction ; https://nuxtseo.com/docs/ai-ready/getting-started/introduction ; https://nuxtseo.com/docs/schema-org/guides/quick-setup
- Astro sitemap: https://docs.astro.build/en/guides/integrations-guide/sitemap/
- SvelteKit: https://svelte.dev/docs/kit/page-options
- React Router prerender: https://reactrouter.com/how-to/pre-rendering
- Vike: https://vike.dev/pre-rendering ; Rendertron: https://github.com/GoogleChrome/rendertron
- Yoast llms.txt: https://yoast.com/features/llms-txt/ ; Rank Math: https://rankmath.com/kb/llms-txt/
- Squarespace crawlers: https://support.squarespace.com/hc/en-us/articles/360022347072
- Ghost: https://docs.ghost.org/themes/structure/ ; Hugo: https://gohugo.io/templates/robots/
- Cloudflare Markdown for Agents: https://blog.cloudflare.com/markdown-for-agents/ (2026-02-12)
- Vercel: https://vercel.com/blog/the-rise-of-the-ai-crawler (2024-12-17) ; https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation (2026-02-03)
- Pew: https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/

Studies / press (secondary):
- Ahrefs llms.txt: https://ahrefs.com/blog/llmstxt-study/ (May 2026 data)
- position.digital ChatGPT B2B: https://www.position.digital/blog/chatgpt-ranking-factors/ (2026-08-12)
- SOCi LVI: https://www.soci.ai/blog/the-challenge-of-ai-visibility-for-brands-part-1/ (2026-03-06)
- Yelp × OpenAI: https://www.axios.com/2026/07/23/yelp-reviews-chatgpt-geo-partnership
- Amazon Alexa for Shopping: https://www.cnbc.com/2026/05/13/amazon-ditches-rufus-ai-chatbot-in-favor-of-alexa-shopping-agent.html ; https://www.amalytix.com/en/knowledge/ai/amazon-rufus-guide-2026/
- OpenAI checkout shift: https://www.checkout.com/blog/openai-agentic-commerce-shift (2026-04-20)
- Merchant Center conversational attributes: https://www.productsup.com/blog/google-introduces-six-conversational-attributes-in-merchant-center-here-what-you-need-to-know/
- Malaysia: https://www.lowyat.net/2025/368877/google-ai-mode-more-languages-regions-supports-malay/ (2025-10-08) ; https://www.arfadia.com/blog/malaysia-ai-language-bias-bahasa-melayu-html/ ; https://www.similarweb.com/top-apps/google/malaysia/maps-navigation/
- Publishers: https://ppc.land/small-publishers-lost-60-of-search-traffic-as-ai-reshapes-the-web/ ; https://llmpulse.ai/blog/ai-content-licensing-deals/ ; https://digiday.com/media/meta-enters-ai-licensing-fray-striking-deals-with-people-inc-usa-today-co-and-more/
- G2: https://beomniscient.com/blog/g2-acquisition-ai-citation-share/ ; https://strivelabs.ai/blog/g2-capterra-ai-answers/
- Apple/Square: https://www.theapplepost.com/2026/09/24/72644/square-adds-apple-business-integration-for-managing-apple-maps-listings/

Research gaps (the WebSearch budget ran out mid-session): Microsoft Publisher Content Marketplace (primary source), Webflow/Wix/Framer llms.txt specifics, AIOSEO llms.txt, react-snap last-release date, Apple Business April 2026 unification (primary source), Amazon title cap. All are marked unverified above.
