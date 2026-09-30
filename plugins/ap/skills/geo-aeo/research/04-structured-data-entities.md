# 04: Structured data, entity optimization and knowledge graphs for AI search

Research dossier for the GEO + AEO skill. Compiled 2026-09-26. Every factual claim has a source URL and a date: the publish date, the doc's "last updated" date, or "accessed 2026-09-26". Anything I could not confirm from a primary or clearly dated source is marked **unverified**.

---

## 0. Summary for the skill author

1. **Schema is not a ranking factor and not a requirement for AI features.** Google says: "Structured data isn't required for generative AI search, and there's no special schema.org markup you need to add." It also says to keep using it because it enables rich results ([Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), last updated 2026-07-10). The page on AI features says the same thing: "no special schema.org structured data that you need to add" ([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), last updated 2025-12-10).
2. **Microsoft is the only major engine that has said on record that schema helps its LLMs.** Fabrice Canel said at SMX Munich that "schema markup helps Microsoft's LLMs understand your content" ([SERoundtable, 2025-03-20](https://www.seroundtable.com/schema-llms-copilot-bing-microsoft-39093.html)). Microsoft Advertising's guide adds: "Schema is a type of code that helps search engines and AI systems understand your content" ([Microsoft, 2025-10-08](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers)).
3. **Controlled tests show no measurable citation lift from adding JSON-LD.** Ahrefs compared 1,885 pages that added schema against 4,000 matched controls. The results were AIO −4.6%, AI Mode +2.4% and ChatGPT +2.2%, and the positive changes were statistically indistinguishable from zero ([Ahrefs, 2026-05-11](https://ahrefs.com/blog/schema-ai-citations/)). In searchVIU's test, ChatGPT, Claude, Perplexity, Gemini and AI Mode read only visible HTML when fetching a page live and ignored JSON-LD ([searchVIU, Oct 2025](https://www.searchviu.com/en/schema-markup-and-ai-in-2025-what-chatgpt-claude-perplexity-gemini-really-see/)). The **practical rule**: any fact you want AI to cite must appear in visible HTML text. Schema mirrors that text. It does not replace it.
4. **Where structured data does matter for AI:** (a) Google rich results and merchant listings, which still feed classic SERPs; (b) entity disambiguation (Organization, sameAs, identifiers, logo, knowledge panel); (c) **product feeds**. Merchant Center feeds help products show "in both AI responses and other Google Search results" ([AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)). ChatGPT Shopping ingests its own feed format ([OpenAI feed spec](https://developers.openai.com/commerce/specs/feed), accessed 2026-09-26). (d) Bing/Copilot freshness through IndexNow combined with Product/Offer schema ([Bing, 2025-05-19](https://blogs.bing.com/webmaster/2025/5/IndexNow-Enables-Faster-and-More-Reliable-Updates-for-Shopping-and-Ads/)).
5. **Google's rich result set has been shrinking since 2023.** HowTo is gone (2023). FAQ is gone (2026-05-07). Seven types were retired in June 2025 (Book Actions was later restored), and practice problems in November 2025. Section 1 has the exact list.

---

## 1. Google-supported structured data in 2026: what still shows, what was retired

### 1.1 Current Google Search Gallery (feature docs live on 2026-09-26)

Source: the [Search Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) (last updated 2026-06-15) and the structured-data doc sidebar, accessed 2026-09-26. Most feature pages say "last updated 2026-09-08".

| Feature | Schema.org type(s) | Notes |
|---|---|---|
| Article | Article, NewsArticle, BlogPosting | No required props; recommended: author, datePublished, dateModified, headline, image |
| Breadcrumb | BreadcrumbList | **Desktop only since 2025-01-22** ([updates](https://developers.google.com/search/updates)) |
| Carousel (host carousels via ItemList) | ItemList + Recipe/Course/Movie/Restaurant | |
| Structured data carousels (beta) | ItemList + summary pages | EEA, Turkey, South Africa ([carousels-beta](https://developers.google.com/search/docs/appearance/structured-data/carousels-beta), 2026-09-11) |
| Course list | Course + ItemList | "Course info" was retired; course *list* stays |
| Dataset | Dataset | **Dataset Search only, not Google Search** (clarified 2025-11-05) |
| Discussion forum | DiscussionForumPosting | New properties added 2026-03-24 |
| Education Q&A | Quiz / flashcards | |
| Employer aggregate rating | EmployerAggregateRating | |
| Event | Event | Online-event properties removed 2025-06-05 |
| Fact check | ClaimReview | **Being phased out in Search**; the doc says it "remains supported by the Factcheck Explorer Tool" ([factcheck](https://developers.google.com/search/docs/appearance/structured-data/factcheck), 2026-09-08) |
| Image metadata | ImageObject (license) | |
| Job posting | JobPosting | |
| Local business | LocalBusiness subtypes | |
| Math solver | MathSolver | |
| Merchant listing / Product snippet / Product variants | Product, ProductGroup, Offer | Actively extended in 2026 (see 1.3) |
| Return policy / Shipping policy / Loyalty program | MerchantReturnPolicy, OfferShippingDetails/ShippingService, MemberProgram | Organization-level preferred |
| Movie | Movie + ItemList | |
| Organization (incl. logo) | Organization and subtypes | No required props |
| Profile page | ProfilePage | |
| Q&A | QAPage | For user-generated Q&A only |
| Recipe | Recipe | |
| Review snippet | Review, AggregateRating | New guideline on fake or undisclosed incentivized reviews, 2026-07-24 |
| Software app | SoftwareApplication | |
| Speakable (beta) | speakable on Article/WebPage | Google Assistant news TTS |
| Subscription & paywalled content | isAccessibleForFree + hasPart | |
| Vacation rental | VacationRental | |
| Video | VideoObject, Clip, BroadcastEvent | creator + interactionStatistic updated 2026-09-24 |
| Book actions | Book (feeds) | Partner-only; deprecation banner removed 2025-11-05 |
| Site names | WebSite (name, alternateName) | Home page only ([site names](https://developers.google.com/search/docs/appearance/site-names), 2025-12-10) |

### 1.2 Retired or restricted (with dates)

| Date | Change | Source |
|---|---|---|
| 2023-08-08 | FAQ rich results limited to "well-known, authoritative government and health websites"; HowTo limited to desktop | [Google blog](https://developers.google.com/search/blog/2023/08/howto-faq-changes) |
| 2023-09-13 | **HowTo rich results removed on desktop too, so the type is deprecated.** Search Console report and Rich Results Test support dropped after 30 days, API after 180 days | same post, update of 2023-09-14 |
| 2024-11-21 | **Sitelinks search box** removed globally (WebSite `potentialAction` SearchAction no longer displays) | [Google blog, Oct 2024](https://developers.google.com/search/blog/2024/10/sitelinks-search-box) |
| 2025-01-22 | Breadcrumbs appear only on desktop results | [updates](https://developers.google.com/search/updates) |
| 2025-04-23 | Special announcement (COVID) deprecation notice | [updates](https://developers.google.com/search/updates) |
| 2025-06-12 | Phase-out announced for **Book Actions, Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing**. Henry Hsu: "not commonly used in Search… no longer providing significant additional value". The post also says "use of these structured data types outside of Google Search… is not affected" | [Google blog](https://developers.google.com/search/blog/2025/06/simplifying-search-results) |
| 2025-09-08/09 | Search Console reports and Rich Results Test support removed for Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing; docs deleted 2025-09-09 | same blog (update note) + [updates](https://developers.google.com/search/updates) |
| 2025-11-05 | **Practice problem** deprecated (docs removed 2026-01-06). **Dataset** clarified as Dataset Search only. **Book actions restored** ("there's still a feature using the markup"). Non-markup SERP features also dropped: nutrition facts, nearby offers, bikeshare status and others | [Google blog (Mueller)](https://developers.google.com/search/blog/2025/11/update-on-our-efforts), [updates](https://developers.google.com/search/updates), [SERoundtable 2025-11-06](https://www.seroundtable.com/google-drops-support-structured-data-types-40386.html) |
| 2026-01 | Search Console and its API stop supporting the retired types | [Google blog 2025-11-05](https://developers.google.com/search/blog/2025/11/update-on-our-efforts) |
| **2026-05-07** | **FAQ rich results stop appearing entirely.** Google's note: "We will be dropping the FAQ search appearance, rich result report, and support in the Rich results test in June 2026… support… in the Search Console API will be removed in August 2026." Docs removed 2026-06-15 | [updates](https://developers.google.com/search/updates) (entries 2026-05-08, 2026-06-15); [SEJ 2026-05-10](https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/) |

**Understood but not displayed.** Google says unused markup is harmless: "Structured data that's not being used does not cause problems for Search, but also has no visible effects" ([2023 FAQ/HowTo post](https://developers.google.com/search/blog/2023/08/howto-faq-changes)). The general intro also says Google uses markup "to gather information about the web and the world in general, such as information about the people, books, or companies that are included in the markup" ([intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), 2025-12-10). John Mueller put it this way: "markup types come and go, but a precious few you should hold on to (like title, and meta robots)" ([SEJ, 2025-11-11](https://www.searchenginejournal.com/google-is-not-diminishing-the-use-of-structured-data-in-2026/560516/)).

**Skill rule:** You can keep FAQPage and HowTo markup where the content really is a FAQ or a set of steps. They are harmless, Bing and Microsoft name FAQ as a useful type, and other consumers may read them. Never promise that they produce Google rich results. Do not add FAQ blocks just to win SERP real estate.

### 1.3 Types being extended in 2025–2026 (these are the growth areas)

All on [updates](https://developers.google.com/search/updates):
- 2025-02-13: price-type encoding (sale, strikethrough, member prices).
- 2025-06-10: loyalty programs (MemberProgram); return policy moved to its own page.
- 2025-07-11: Organization-level return policies preferred; offer-level supports only a subset.
- 2026-03-02: Google uses **both schema.org `image` and `og:image`** to pick thumbnails in Search and Discover.
- 2026-03-24: discussion forum and QAPage get more properties (e.g., `digitalSourceType`, `sharedContent`).
- 2026-05-20: `hasAdultConsideration` added to Product.
- 2026-07-07: `Product.category` accepts Text or CategoryCode, aligned with Merchant Center `product_type`/`google_product_category`. Sale duration documented via `validFrom`, `validThrough`, `priceValidUntil`.
- 2026-09-24: VideoObject `creator` and `interactionStatistic`.

Schema.org itself is at **v30.1, released 2026-09-16**. It adds EU Digital Product Passport vocabulary and `consumerNotice`, `isOftenBoughtWith` and `specification`. v30.0 (2026-03-19) added Open Graph/GS1/Dublin Core equivalences and `Credential` ([schema.org releases](https://schema.org/docs/releases.html)).

---

## 2. Evidence: does schema affect AI citations?

### 2.1 Official statements

| Who | Statement | Source/date |
|---|---|---|
| Google | "Structured data isn't required for generative AI search, and there's no special schema.org markup you need to add. However, it's a good idea to continue using it… as it helps with being eligible for rich results" | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), 2026-05-15 (updated 2026-07-10) |
| Google | "Structured data is useful for sharing information about your content in a machine-readable way that our systems consider… make sure that all the content in your markup is also visible on your web page" | [Google blog 2025-05-21 "Top ways to ensure your content performs well in Google's AI experiences"](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) |
| Google | To be a supporting link in AIO/AI Mode, "a page must be indexed and eligible to be shown in Google Search with a snippet" | [AI features](https://developers.google.com/search/docs/appearance/ai-features), 2025-12-10 |
| Google | llms.txt: not needed for Google Search, "won't negatively or positively impact your visibility", fine to keep for other systems | [updates](https://developers.google.com/search/updates), 2026-06-15 |
| Google | Merchant Center feeds and Business Profiles "can help your products and services to be visible in both AI responses and other Google Search results" | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) |
| Microsoft (Canel) | "Schema markup helps Microsoft's LLMs understand your content"; fresh content matters, so push updates via IndexNow | [SERoundtable 2025-03-20](https://www.seroundtable.com/schema-llms-copilot-bing-microsoft-39093.html); [Search Engine Land](https://searchengineland.com/microsoft-bing-copilot-use-schema-for-its-llms-453455) |
| Microsoft (Madhavan) | Schema "helps search engines and AI systems understand your content"; names product, review, FAQ and event; "page title, description, and H1… are important signals AI systems use" | [Microsoft Advertising blog 2025-10-08](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers) |
| Microsoft (Bing) | Its AI Performance report guidance stresses depth, headings/tables/FAQ sections, evidence and freshness via IndexNow, and does not emphasize schema | [Bing blog 2026-02-10](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/) |
| Microsoft (Bing) | IndexNow signals *that* something changed and Product/Offer schema says *what* changed, for Bing Shopping, Copilot and Ads | [Bing blog 2025-05-19](https://blogs.bing.com/webmaster/2025/5/IndexNow-Enables-Faster-and-More-Reliable-Updates-for-Shopping-and-Ads/) |

OpenAI, Perplexity and Anthropic: I found **no primary statement** that on-page JSON-LD influences citation. **Unverified** either way.

### 2.2 Experiments

- **Ahrefs (published 2026-05-11).** A matched difference-in-differences study: 1,885 pages that added JSON-LD between Aug 2025 and Mar 2026, against 4,000 controls, with 30-day windows. AIO −4.6% (small, statistically significant), AI Mode +2.4% (n.s.), ChatGPT +2.2% (n.s.). Caveats: only pages that were already heavily cited, all schema types pooled, JSON-LD only ([Ahrefs](https://ahrefs.com/blog/schema-ai-citations/)).
- **OtterlyAI (published 2026-03-23).** Ran Dec 2025 to Mar 2026 across 7 platforms. Only Gemini retrieved schema when asked directly, and AI Mode hallucinated schema. No platform answered with information that existed only in schema. Coverage swings matched those of competitors who made no schema changes ([Otterly](https://otterly.ai/blog/schema-markup-real-impact-ai-search/)).
- **searchVIU (Oct 2025).** A price that existed only in JSON-LD (€8.99) was found by none of ChatGPT, Claude, Perplexity, Gemini or AI Mode on a live fetch. The authors note schema may still matter at index time or in training ([searchVIU](https://www.searchviu.com/en/schema-markup-and-ai-in-2025-what-chatgpt-claude-perplexity-gemini-really-see/)).
- **GEO paper (Aggarwal et al., KDD 2024).** On-page content changes such as citations, statistics and quotations raised visibility "by up to 40%" in generative engine responses. Schema was not the lever ([arXiv 2311.09735](https://arxiv.org/abs/2311.09735)).

### 2.3 What is proven vs not

- **Proven:** schema makes pages eligible for Google rich results and merchant listings. Organization markup influences the logo and knowledge panel details ([Organization doc](https://developers.google.com/search/docs/appearance/structured-data/organization)). Live-fetch LLM agents read visible HTML, not JSON-LD (searchVIU).
- **Stated by the vendor but not independently measured:** schema helps Bing/Copilot LLMs understand content.
- **Not supported by evidence:** adding schema to an already-visible page increases AI citations (Ahrefs, Otterly).
- **Plausible mechanism, not proven:** schema improves entity resolution in the index, and the index then grounds AI answers. This mechanism is indirect.

---

## 3. JSON-LD best practice

### 3.1 Principles (from [Google general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), last updated 2026-07-10)

- Use JSON-LD. It is recommended, and Google can read it when injected by JavaScript ([intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)). **For non-Google AI crawlers, server-render it**, because many AI crawlers do not execute JS. That last point is an inference from searchVIU/Otterly and is **unverified** per crawler.
- "Don't mark up content that is not visible to readers of the page." Don't impersonate. Keep time-sensitive data current. Image URLs must be crawlable and indexable.
- Mark up the **main entity** of the page, and add the secondary ones (Video, Review, Breadcrumb) in the same graph.
- Rich results are never guaranteed, even with valid markup.
- If a page has both `max-snippet` and structured data, the structured data is still usable for rich results. Google's robots doc says that where "the publisher supplies content in the form of in-page structured data… this setting does not interrupt those more specific permitted uses" ([robots meta](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), 2026-03-24).

### 3.2 The @id graph pattern

Emit **one `<script type="application/ld+json">` per page containing a single `@graph`**. Give every node a stable `@id`: the canonical URL plus a fragment such as `#organization`, `#website`, `#webpage`, `#breadcrumb`, `#article` or `#person-jane`. Reference nodes with `{"@id": "…"}` instead of repeating them. Reuse the **same site-wide IDs** (`https://example.com/#organization`, `https://example.com/#website`) on every page, so every page points to one entity.

Complete site-wide graph (home page or any article page):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example Analytics",
      "legalName": "Example Analytics Sdn. Bhd.",
      "alternateName": ["ExampleAI", "Example Analytics MY"],
      "url": "https://www.example.com/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.example.com/#logo",
        "url": "https://www.example.com/assets/logo-512.png",
        "contentUrl": "https://www.example.com/assets/logo-512.png",
        "width": 512,
        "height": 512,
        "caption": "Example Analytics"
      },
      "image": {"@id": "https://www.example.com/#logo"},
      "description": "Example Analytics builds demand-forecasting software for Southeast Asian retailers.",
      "foundingDate": "2019-04-01",
      "founder": {"@id": "https://www.example.com/about/jane-tan/#person"},
      "numberOfEmployees": {"@type": "QuantitativeValue", "value": 42},
      "email": "hello@example.com",
      "telephone": "+60-3-1234-5678",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Level 8, 1 Jalan Example",
        "addressLocality": "Kuala Lumpur",
        "addressRegion": "Wilayah Persekutuan",
        "postalCode": "50450",
        "addressCountry": "MY"
      },
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "support@example.com",
          "telephone": "+60-3-1234-5679",
          "availableLanguage": ["en", "ms"]
        }
      ],
      "vatID": "MY-SST-000000",
      "leiCode": "5493000000000000000X",
      "iso6523Code": "0199:5493000000000000000X",
      "naics": "511210",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q000000000",
        "https://www.linkedin.com/company/example-analytics",
        "https://www.crunchbase.com/organization/example-analytics",
        "https://github.com/example-analytics",
        "https://www.youtube.com/@exampleanalytics",
        "https://x.com/exampleanalytics"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "url": "https://www.example.com/",
      "name": "Example Analytics",
      "alternateName": ["ExampleAI"],
      "publisher": {"@id": "https://www.example.com/#organization"},
      "inLanguage": "en"
    },
    {
      "@type": "WebPage",
      "@id": "https://www.example.com/blog/forecasting-ramadan-demand/#webpage",
      "url": "https://www.example.com/blog/forecasting-ramadan-demand/",
      "name": "How to forecast Ramadan demand for grocery retail",
      "isPartOf": {"@id": "https://www.example.com/#website"},
      "about": {"@id": "https://www.example.com/#organization"},
      "primaryImageOfPage": {"@id": "https://www.example.com/blog/forecasting-ramadan-demand/#primaryimage"},
      "breadcrumb": {"@id": "https://www.example.com/blog/forecasting-ramadan-demand/#breadcrumb"},
      "datePublished": "2026-02-10T09:00:00+08:00",
      "dateModified": "2026-09-20T14:30:00+08:00",
      "inLanguage": "en"
    },
    {
      "@type": "ImageObject",
      "@id": "https://www.example.com/blog/forecasting-ramadan-demand/#primaryimage",
      "url": "https://www.example.com/img/ramadan-demand-16x9.jpg",
      "contentUrl": "https://www.example.com/img/ramadan-demand-16x9.jpg",
      "width": 1600,
      "height": 900,
      "caption": "Weekly unit sales of dates, 2023–2026"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.example.com/blog/forecasting-ramadan-demand/#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.example.com/blog/"},
        {"@type": "ListItem", "position": 3, "name": "How to forecast Ramadan demand"}
      ]
    },
    {
      "@type": "BlogPosting",
      "@id": "https://www.example.com/blog/forecasting-ramadan-demand/#article",
      "mainEntityOfPage": {"@id": "https://www.example.com/blog/forecasting-ramadan-demand/#webpage"},
      "headline": "How to forecast Ramadan demand for grocery retail",
      "description": "A step-by-step method using three years of POS data, with benchmarks.",
      "image": [
        "https://www.example.com/img/ramadan-demand-1x1.jpg",
        "https://www.example.com/img/ramadan-demand-4x3.jpg",
        "https://www.example.com/img/ramadan-demand-16x9.jpg"
      ],
      "datePublished": "2026-02-10T09:00:00+08:00",
      "dateModified": "2026-09-20T14:30:00+08:00",
      "author": [{"@id": "https://www.example.com/about/jane-tan/#person"}],
      "publisher": {"@id": "https://www.example.com/#organization"},
      "isPartOf": {"@id": "https://www.example.com/#website"},
      "inLanguage": "en",
      "wordCount": 2150,
      "about": [{"@type": "Thing", "name": "Demand forecasting", "sameAs": "https://www.wikidata.org/wiki/Q1195964"}],
      "citation": ["https://www.dosm.gov.my/"]
    },
    {
      "@type": "Person",
      "@id": "https://www.example.com/about/jane-tan/#person",
      "name": "Jane Tan",
      "url": "https://www.example.com/about/jane-tan/",
      "image": "https://www.example.com/img/jane-tan.jpg",
      "jobTitle": "Head of Data Science",
      "worksFor": {"@id": "https://www.example.com/#organization"},
      "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universiti Malaya"},
      "knowsAbout": ["Demand forecasting", "Retail analytics", "Time series"],
      "sameAs": [
        "https://www.linkedin.com/in/janetan-example",
        "https://scholar.google.com/citations?user=EXAMPLE",
        "https://orcid.org/0000-0000-0000-0000"
      ]
    }
  ]
}
```

Notes, cited:
- Organization has **no required properties**. Google recommends adding "as many properties that are relevant", and says some (iso6523, naics) are used "behind the scenes to disambiguate" ([Organization doc](https://developers.google.com/search/docs/appearance/structured-data/organization), 2026-09-08). Put it on the home page or an About page.
- Logo must be **at least 112×112 px**, crawlable and indexable, and look right on white (same doc).
- The recommended Organization properties are: address, alternateName, contactPoint, description, duns, email, foundingDate, globalLocationNumber, hasMerchantReturnPolicy, hasMemberProgram, hasShippingService, iso6523Code, legalName, leiCode, naics, name, numberOfEmployees, sameAs, taxID, telephone, url, vatID (same doc).
- **Site name** preference comes from WebSite `name`/`alternateName` **on the domain or subdomain home page only**. A subdirectory home page is not supported ([site names](https://developers.google.com/search/docs/appearance/site-names)).
- Do **not** add a `potentialAction` SearchAction expecting a sitelinks search box. That feature was removed on 2024-11-21 ([Google blog](https://developers.google.com/search/blog/2024/10/sitelinks-search-box)).
- **Author best practice** ([Article doc](https://developers.google.com/search/docs/appearance/structured-data/article), 2026-09-08): include every visible author. Use one object per author and never "A, B" in a single name. Use `@type` Person or Organization. Use `url` or `sameAs` ("Google can understand both sameAs and url when disambiguating authors"). `author.name` holds only the name, with no title, honorific or "posted by".
- **Dates:** give a date plus time plus timezone, keep them consistent with the visible byline, and use `datePublished`/`dateModified` ([byline dates](https://developers.google.com/search/docs/appearance/publication-dates), 2025-12-10).
- BreadcrumbList requires `itemListElement` with `position`, `name` and `item`. The last item's `item` is optional ([breadcrumb](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)). It is displayed on desktop only.
- For AboutPage and ContactPage, set the WebPage node's `@type` to `["WebPage","AboutPage"]` or `"ContactPage"`. On the About page, add `"mainEntity": {"@id": "…#organization"}`. Neither produces a rich result, and both are "understood" only.
- NewsArticle: same shape as above. Pair it with `speakable` (see 3.14) and `isAccessibleForFree`/`hasPart` for paywalls ([paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content)).

### 3.3 Person / ProfilePage (author entity pages)

ProfilePage requires `mainEntity` (Person or Organization) with `name`. The recommended properties are `dateCreated`, `dateModified`, `alternateName`, `description`, `identifier`, `image`, `sameAs`, `interactionStatistic` and `agentInteractionStatistic`. Valid uses include forum user pages, author pages and "about me" pages. A store's home page is not a valid use ([profile page](https://developers.google.com/search/docs/appearance/structured-data/profile-page), 2026-09-08).

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "@id": "https://www.example.com/about/jane-tan/",
  "dateCreated": "2021-03-01T08:00:00+08:00",
  "dateModified": "2026-09-01T10:00:00+08:00",
  "mainEntity": {
    "@type": "Person",
    "@id": "https://www.example.com/about/jane-tan/#person",
    "name": "Jane Tan",
    "alternateName": "jtan",
    "identifier": "author-0042",
    "description": "Head of Data Science at Example Analytics; 12 years in retail forecasting.",
    "image": "https://www.example.com/img/jane-tan.jpg",
    "jobTitle": "Head of Data Science",
    "worksFor": {"@id": "https://www.example.com/#organization"},
    "sameAs": [
      "https://www.linkedin.com/in/janetan-example",
      "https://orcid.org/0000-0000-0000-0000"
    ],
    "interactionStatistic": {
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/WriteAction",
      "userInteractionCount": 87
    }
  },
  "hasPart": [
    {"@type": "BlogPosting", "headline": "How to forecast Ramadan demand for grocery retail", "url": "https://www.example.com/blog/forecasting-ramadan-demand/", "datePublished": "2026-02-10T09:00:00+08:00"}
  ]
}
```

### 3.4 Product + Offer + ratings + shipping + returns (merchant listing)

Merchant listing requires `name`, `image` and `offers` (with `price` and `priceCurrency`). The recommended properties are aggregateRating, review, gtin*/isbn, mpn, sku, brand, color, material, size, pattern, audience, `isVariantOf`/`inProductGroupWithID`, and on the Offer `hasMerchantReturnPolicy`, `itemCondition`, `shippingDetails` and `url`. Shipping requires `shippingDestination.addressCountry`, `shippingRate` (value + currency) and `deliveryTime`. A return policy needs `applicableCountry` and `returnPolicyCategory`. If both `offers.price` and `priceSpecification` are present, `price` wins ([merchant listing](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing), 2026-09-08). Google prefers **Organization-level** return and shipping policies. Product-level ones override them ([return policy](https://developers.google.com/search/docs/appearance/structured-data/return-policy), [shipping policy](https://developers.google.com/search/docs/appearance/structured-data/shipping-policy)).

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://shop.example.com/p/trail-runner-x/#product",
  "name": "Trail Runner X – Men's trail running shoe",
  "description": "Lightweight trail shoe with 4 mm lugs and a recycled mesh upper.",
  "image": [
    "https://shop.example.com/img/trx-1x1.jpg",
    "https://shop.example.com/img/trx-4x3.jpg",
    "https://shop.example.com/img/trx-16x9.jpg"
  ],
  "sku": "TRX-BLK-42",
  "mpn": "TRX2026-42",
  "gtin13": "9555000000012",
  "brand": {"@type": "Brand", "name": "Northline"},
  "color": "Black",
  "material": "Recycled polyester mesh",
  "size": "EU 42",
  "category": "Apparel & Accessories > Shoes",
  "inProductGroupWithID": "TRX",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.6,
    "bestRating": 5,
    "ratingCount": 312,
    "reviewCount": 128
  },
  "review": [
    {
      "@type": "Review",
      "author": {"@type": "Person", "name": "Aisha R."},
      "datePublished": "2026-08-14",
      "reviewRating": {"@type": "Rating", "ratingValue": 5, "bestRating": 5},
      "reviewBody": "Grippy on wet laterite and dries fast."
    }
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://shop.example.com/p/trail-runner-x/?size=42",
    "price": 389.00,
    "priceCurrency": "MYR",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {"@id": "https://shop.example.com/#organization"},
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "MYR"},
      "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MY"},
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
        "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"}
      }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "MY",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }
  }
}
```

Product variants: wrap the variants in a `ProductGroup` with `productGroupID` and `variesBy`, and point each variant back with `isVariantOf` ([product variants](https://developers.google.com/search/docs/appearance/structured-data/product-variants)). For editorial review pages that do not sell anything, use the **product snippet** instead. It requires `name` plus one of `review`, `aggregateRating` or `offers` ([product snippet](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)).

### 3.5 Review snippets

A Review requires `author`, `itemReviewed` (with `name`), `reviewRating` and `reviewRating.ratingValue`. An AggregateRating requires `itemReviewed`, `ratingValue`, and `ratingCount` or `reviewCount`. Since 2025-11-12, Google has asked sites not to use multiple ways of stating what is being reviewed. Since 2026-07-24 there is a guideline against fake or undisclosed incentivized reviews ([review snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet); [updates](https://developers.google.com/search/updates)). **Self-serving reviews** (a business marking up reviews of itself on its own site with LocalBusiness/Organization) are not eligible for stars. That is a long-standing policy; I did not re-fetch its exact wording this session.

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {"@type": "SoftwareApplication", "name": "Acme Forecast", "applicationCategory": "BusinessApplication", "operatingSystem": "Web"},
  "author": {"@type": "Person", "name": "Jane Tan", "url": "https://www.example.com/about/jane-tan/"},
  "datePublished": "2026-09-01",
  "reviewRating": {"@type": "Rating", "ratingValue": 4, "bestRating": 5, "worstRating": 1},
  "reviewBody": "Accurate weekly forecasts; weak on promotions.",
  "publisher": {"@type": "Organization", "name": "Example Analytics"}
}
```

### 3.6 LocalBusiness

Requires `name` and `address`. Recommended: `geo` (lat/long), `openingHoursSpecification`, `telephone`, `url`, `priceRange`, `servesCuisine`/`menu` for restaurants, `aggregateRating`, `review` and `department` ([local business](https://developers.google.com/search/docs/appearance/structured-data/local-business), 2026-09-08). Use the most specific subtype (Dentist, AutoRepair, Restaurant and so on). Short day names ("Monday") are accepted.

```json
{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "@id": "https://www.dreamgarage.example/#localbusiness",
  "name": "Dream Garage Puchong",
  "image": "https://www.dreamgarage.example/img/storefront.jpg",
  "url": "https://www.dreamgarage.example/",
  "telephone": "+60-3-8000-0000",
  "priceRange": "RM",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12 Jalan Industri 3",
    "addressLocality": "Puchong",
    "addressRegion": "Selangor",
    "postalCode": "47100",
    "addressCountry": "MY"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": 3.0245, "longitude": 101.6170},
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "00:00", "closes": "00:00", "validFrom": "2026-12-25", "validThrough": "2026-12-25"}
  ],
  "areaServed": ["Puchong", "Subang Jaya", "Putrajaya"],
  "parentOrganization": {"@id": "https://www.dreamgarage.example/#organization"},
  "sameAs": ["https://maps.google.com/?cid=0000000000000000000", "https://www.facebook.com/dreamgarage.example"]
}
```

(The closed-holiday pattern, opens = closes = 00:00 inside a validFrom/validThrough window, comes from Google's local-business doc examples. It is recalled from that doc, not re-quoted here.)

### 3.7 Service (no rich result; understood only)

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://www.example.com/services/forecast-audit/#service",
  "name": "Forecast accuracy audit",
  "serviceType": "Demand forecasting consulting",
  "description": "Two-week audit of your forecasting pipeline with a MAPE baseline and remediation plan.",
  "provider": {"@id": "https://www.example.com/#organization"},
  "areaServed": [{"@type": "Country", "name": "Malaysia"}, {"@type": "Country", "name": "Singapore"}],
  "offers": {"@type": "Offer", "price": 15000, "priceCurrency": "MYR", "url": "https://www.example.com/services/forecast-audit/"}
}
```

### 3.8 SoftwareApplication

Requires `name`, `offers.price`, and **either** `aggregateRating` **or** `review`. Recommended: `applicationCategory` and `operatingSystem` ([software app](https://developers.google.com/search/docs/appearance/structured-data/software-app), 2026-09-08). Use `WebApplication`/`MobileApplication` subtypes where they fit.

```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Acme Forecast",
  "url": "https://acme.example/",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web browser",
  "offers": {"@type": "Offer", "price": 0, "priceCurrency": "USD", "description": "Free tier; paid plans from USD 49/month"},
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.5, "ratingCount": 220, "bestRating": 5},
  "publisher": {"@type": "Organization", "name": "Acme Inc.", "url": "https://acme.example/"}
}
```

### 3.9 FAQPage, QAPage and HowTo

- **FAQPage:** rich result retired 2026-05-07 (§1.2). It is still valid schema.org. Keep it only where there is a real visible FAQ, and make the visible Q&A text the answer.
- **QAPage:** for pages where *users* post a question and answers (forums, community Q&A). Requires `mainEntity` (Question) with `name`, `answerCount`, and `acceptedAnswer` and/or `suggestedAnswer` (each with `text`). Recommended: author and author.url, upvoteCount, datePublished and url per answer ([QAPage](https://developers.google.com/search/docs/appearance/structured-data/qapage), 2026-09-08).
- **HowTo:** rich result deprecated 2023-09-13. Recipe still uses `HowToStep`/`HowToSection` inside `recipeInstructions`.

```json
{
  "@context": "https://schema.org",
  "@type": "QAPage",
  "mainEntity": {
    "@type": "Question",
    "name": "Why does my Prisma migration hang on Postgres 16?",
    "text": "Running prisma migrate deploy hangs forever on a DO managed Postgres 16 cluster.",
    "answerCount": 2,
    "datePublished": "2026-09-01T10:00:00Z",
    "author": {"@type": "Person", "name": "devuser42", "url": "https://forum.example.com/u/devuser42"},
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "An idle-in-transaction session holds the advisory lock. Set idle_in_transaction_session_timeout and kill the stale PID.",
      "upvoteCount": 31,
      "datePublished": "2026-09-01T11:05:00Z",
      "url": "https://forum.example.com/t/123#answer-1",
      "author": {"@type": "Person", "name": "pgwizard", "url": "https://forum.example.com/u/pgwizard"}
    },
    "suggestedAnswer": [{
      "@type": "Answer",
      "text": "Check that the connection string does not point at the pgbouncer transaction pool.",
      "upvoteCount": 4,
      "datePublished": "2026-09-01T12:00:00Z",
      "url": "https://forum.example.com/t/123#answer-2",
      "author": {"@type": "Person", "name": "opsgal", "url": "https://forum.example.com/u/opsgal"}
    }]
  }
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do you ship to East Malaysia?",
      "acceptedAnswer": {"@type": "Answer", "text": "Yes. Sabah and Sarawak orders ship in 3–5 working days for a flat RM15."}
    },
    {
      "@type": "Question",
      "name": "What is your return window?",
      "acceptedAnswer": {"@type": "Answer", "text": "30 days from delivery, free return by mail."}
    }
  ]
}
```

### 3.10 DiscussionForumPosting

Requires `author` (with `name`), `datePublished`, and `text` (or an image/video). Recommended: `headline`, `url`, `comment`, `commentCount`, `interactionStatistic`, `dateModified`, `creativeWorkStatus`, `isPartOf`, `sharedContent` and `digitalSourceType` ([discussion forum](https://developers.google.com/search/docs/appearance/structured-data/discussion-forum), 2026-09-08). Use DiscussionForumPosting for general threads and QAPage for question-and-answer threads.

```json
{
  "@context": "https://schema.org",
  "@type": "DiscussionForumPosting",
  "headline": "Best tyres for Myvi under RM200?",
  "text": "Looking for quiet tyres for daily KL traffic, 175/65 R14.",
  "url": "https://forum.example.com/t/456",
  "datePublished": "2026-09-10T08:00:00+08:00",
  "author": {"@type": "Person", "name": "kl_driver", "url": "https://forum.example.com/u/kl_driver"},
  "interactionStatistic": {"@type": "InteractionCounter", "interactionType": "https://schema.org/LikeAction", "userInteractionCount": 12},
  "commentCount": 1,
  "comment": [{
    "@type": "Comment",
    "text": "Try the eco line; quieter than stock.",
    "datePublished": "2026-09-10T09:12:00+08:00",
    "author": {"@type": "Person", "name": "tyreguy", "url": "https://forum.example.com/u/tyreguy"}
  }]
}
```

### 3.11 Event

Google requires `name`, `startDate` and `location`. For a physical venue, `location` is a Place with `name` and `address`. Recommended: `description`, `endDate`, `eventStatus`, `image`, `offers` and `organizer`/`performer`. Don't remove `startDate` when the status changes. Online-event properties were removed from Google's doc on 2025-06-05 ([event](https://developers.google.com/search/docs/appearance/structured-data/event); [updates](https://developers.google.com/search/updates)).

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "KL Retail Analytics Meetup #14",
  "description": "Talks on promo-aware forecasting and shelf analytics.",
  "startDate": "2026-11-12T19:00:00+08:00",
  "endDate": "2026-11-12T21:30:00+08:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Common Ground Bukit Bintang",
    "address": {"@type": "PostalAddress", "streetAddress": "Jalan Bukit Bintang", "addressLocality": "Kuala Lumpur", "postalCode": "55100", "addressCountry": "MY"}
  },
  "image": ["https://www.example.com/img/meetup14-16x9.jpg"],
  "organizer": {"@id": "https://www.example.com/#organization"},
  "offers": {"@type": "Offer", "url": "https://www.example.com/events/meetup-14/", "price": 0, "priceCurrency": "MYR", "availability": "https://schema.org/InStock", "validFrom": "2026-10-01T00:00:00+08:00"}
}
```

### 3.12 Course (course list)

A Course requires `name` and `description`, and `provider` is recommended. The list form is an `ItemList` of `ListItem` with `position` and `url` ([course](https://developers.google.com/search/docs/appearance/structured-data/course), 2026-09-08). Note that the richer "Course info" markup was retired in 2025.

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Time-series forecasting for retail",
  "description": "Six-week practical course on ARIMA, gradient boosting and hierarchical reconciliation.",
  "provider": {"@type": "Organization", "name": "Example Analytics Academy", "sameAs": "https://www.example.com/academy/"}
}
```

### 3.13 Recipe, VideoObject, ImageObject, Dataset

Recipe requires `name` and `image`. It recommends author, datePublished, description, prep/cook/totalTime (ISO 8601), recipeIngredient, recipeInstructions (HowToStep), recipeYield, nutrition.calories, aggregateRating and video ([recipe](https://developers.google.com/search/docs/appearance/structured-data/recipe)).

Video requires `name`, `thumbnailUrl` and `uploadDate`. It recommends `description`, `contentUrl` (preferred) or `embedUrl`, `duration`, `expires`, `hasPart` (Clip, with `name`, `startOffset` and `url`), `interactionStatistic`, `regionsAllowed`/`ineligibleRegion`, and since 2026-09-24 `creator`. Livestreams use BroadcastEvent `publication` ([video](https://developers.google.com/search/docs/appearance/structured-data/video), 2026-09-24).

Image license metadata requires `contentUrl` plus one of `creator`, `creditText`, `copyrightNotice` or `license`. Structured data wins over IPTC when they conflict ([image metadata](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata)).

Dataset requires `name` and `description` (50–5000 chars). It is used **only by Dataset Search** ([dataset](https://developers.google.com/search/docs/appearance/structured-data/dataset), 2026-09-08).

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Recipe",
      "name": "Nasi lemak with sambal ikan bilis",
      "image": ["https://food.example.com/img/nasi-lemak-1x1.jpg", "https://food.example.com/img/nasi-lemak-16x9.jpg"],
      "author": {"@type": "Person", "name": "Siti Aminah"},
      "datePublished": "2026-08-31",
      "description": "Coconut rice with a sweet-spicy anchovy sambal.",
      "prepTime": "PT30M",
      "cookTime": "PT45M",
      "totalTime": "PT1H15M",
      "recipeYield": "4 servings",
      "recipeCategory": "Main course",
      "recipeCuisine": "Malaysian",
      "keywords": "nasi lemak, sambal",
      "nutrition": {"@type": "NutritionInformation", "calories": "640 calories"},
      "recipeIngredient": ["2 cups rice", "400 ml coconut milk", "3 pandan leaves", "1 cup dried anchovies"],
      "recipeInstructions": [
        {"@type": "HowToStep", "name": "Cook rice", "text": "Cook rice with coconut milk and pandan until fluffy.", "url": "https://food.example.com/nasi-lemak#step1"},
        {"@type": "HowToStep", "name": "Make sambal", "text": "Fry blended chilli paste until oil separates, add anchovies.", "url": "https://food.example.com/nasi-lemak#step2"}
      ],
      "video": {"@id": "https://food.example.com/nasi-lemak#video"}
    },
    {
      "@type": "VideoObject",
      "@id": "https://food.example.com/nasi-lemak#video",
      "name": "How to make nasi lemak",
      "description": "Full walkthrough of coconut rice and sambal.",
      "thumbnailUrl": ["https://food.example.com/img/nasi-lemak-thumb.jpg"],
      "uploadDate": "2026-08-31T08:00:00+08:00",
      "duration": "PT8M12S",
      "contentUrl": "https://food.example.com/video/nasi-lemak.mp4",
      "embedUrl": "https://food.example.com/embed/nasi-lemak",
      "creator": {"@type": "Person", "name": "Siti Aminah", "url": "https://food.example.com/about/siti/"},
      "interactionStatistic": {"@type": "InteractionCounter", "interactionType": "https://schema.org/WatchAction", "userInteractionCount": 15230},
      "hasPart": [
        {"@type": "Clip", "name": "Coconut rice", "startOffset": 20, "endOffset": 190, "url": "https://food.example.com/nasi-lemak?t=20"},
        {"@type": "Clip", "name": "Sambal", "startOffset": 191, "endOffset": 480, "url": "https://food.example.com/nasi-lemak?t=191"}
      ]
    },
    {
      "@type": "ImageObject",
      "contentUrl": "https://food.example.com/img/nasi-lemak-16x9.jpg",
      "license": "https://food.example.com/image-license",
      "acquireLicensePage": "https://food.example.com/licensing",
      "creditText": "Food Example",
      "creator": {"@type": "Person", "name": "Siti Aminah"},
      "copyrightNotice": "© 2026 Food Example"
    },
    {
      "@type": "Dataset",
      "name": "Malaysian grocery weekly sales 2023–2026",
      "description": "Anonymised weekly unit sales for 1,200 SKUs across 40 Klang Valley stores, used in our Ramadan forecasting study.",
      "url": "https://www.example.com/data/grocery-weekly/",
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "creator": {"@type": "Organization", "name": "Example Analytics", "url": "https://www.example.com/"},
      "temporalCoverage": "2023-01-01/2026-06-30",
      "spatialCoverage": "Klang Valley, Malaysia",
      "isAccessibleForFree": true,
      "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": "https://www.example.com/data/grocery-weekly.csv"}]
    }
  ]
}
```

### 3.14 Speakable (beta)

Speakable is a beta feature used by Google Assistant to read news aloud. It takes `cssSelector` or `xPath` on an Article/WebPage ([speakable](https://developers.google.com/search/docs/appearance/structured-data/speakable), 2026-09-08). I believe availability is limited to English-language news publishers in the US, but I could not re-confirm that this session (**unverified**). It carries low priority for general sites.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Budget 2027: what changes for SMEs",
  "url": "https://news.example.com/budget-2027-smes",
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".article-headline", ".article-summary"]}
}
```

### 3.15 Common validation errors (what automated checks should flag)

These come from Google's docs above and general practice.
1. Markup describes content that is **not visible** on the page, including prices that exist only in JSON-LD ([sd-policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)).
2. Several disconnected nodes for the same entity, such as an Organization repeated with different names, or blocks that contradict each other (for example Product price ≠ visible price ≠ feed price).
3. `author.name` containing "By …", a job title, or several names ([article](https://developers.google.com/search/docs/appearance/structured-data/article)).
4. Dates without a timezone, or a `dateModified` that doesn't match the visible "Updated" date, or `dateModified` bumped with no real content change.
5. Enum values given as plain words ("InStock") where full URLs are expected (`https://schema.org/InStock`). Google accepts both in many places, but the Schema Markup Validator and some consumers are stricter (**unverified** per consumer).
6. Relative or blocked image URLs, or a logo under 112×112 ([organization](https://developers.google.com/search/docs/appearance/structured-data/organization)).
7. Self-serving review stars on LocalBusiness/Organization, and fake or incentivized reviews ([review snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)).
8. Reliance on retired features: SearchAction, HowTo, FAQ for rich results, Course info, ClaimReview in Search, Vehicle listing, Estimated salary, Learning video, Practice problem.
9. WebSite site-name markup placed on a subdirectory "home page" ([site names](https://developers.google.com/search/docs/appearance/site-names)).
10. `offers.price` together with `priceSpecification` giving different prices (price wins) ([merchant listing](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing)).
11. JSON syntax errors: trailing commas, unescaped quotes in `text`, or HTML inside JSON strings.
12. Markup injected only client-side on sites that also target non-Google AI crawlers.

---

## 4. Entity SEO: Knowledge Graph, Wikidata, sameAs, authors

### 4.1 How the entity layer works

- Google's Knowledge Graph Search API returns entities with `kg:/m/…` or `/g/…` IDs, types and a `resultScore`. Google calls it "not suitable for use as a production-critical service", and it is being migrated to Cloud Enterprise Knowledge Graph ([KG Search API](https://developers.google.com/knowledge-graph), last updated 2024-04-26). An agent can use it to check whether a brand already has a KG entity and which ID it has.
- **Knowledge panels.** Claim one via "Claim this knowledge panel", verifying through a Google-recognized official profile: YouTube, Search Console, X/Twitter or Facebook. Not all panels can be claimed. Local businesses use Business Profile instead ([Google Help](https://support.google.com/knowledgepanel/answer/7534902?hl=en), accessed 2026-09-26).
- **Search profiles (new, 2026).** A Search profile "brings together your content from across the web and social platforms into a single destination on Google" at `https://profile.google.com/@handle`. Followers see linked content more in Discover. Google published badge markup on 2026-09-16 ([Search profiles](https://developers.google.com/search/docs/appearance/search-profiles)). **Skill action:** if the brand or creator has a claimed Search profile, add the badge link and include the profile URL in `sameAs`. Treat the `sameAs` part as a recommendation: Google does not document it.
- **Preferred sources** (users pin favourite sites) expanded to AI Overviews and AI Mode on 2026-05-27. A custom button is available since 2026-08-20 ([updates](https://developers.google.com/search/updates)).
- Organization markup can influence "which logo is shown in Search results and your knowledge panel" and merchant knowledge panel details such as returns and contact ([Organization doc](https://developers.google.com/search/docs/appearance/structured-data/organization)).

### 4.2 Wikidata and Wikipedia (legitimately)

- **Wikidata notability.** An item qualifies if it has a Wikimedia sitelink, **or** "refers to an instance of a clearly identifiable conceptual or material entity that can be described using serious and publicly available references", **or** it fulfils a structural need ([Wikidata:Notability](https://www.wikidata.org/wiki/Wikidata:Notability), accessed 2026-09-26). A company with independent press coverage and official registry entries can therefore have a Wikidata item without a Wikipedia article. Items without serious public references get deleted.
- **How to create one properly:** log in with a disclosed account; if you are paid or affiliated, disclose it under Wikimedia's paid-contribution rules. Add label, description and aliases in each relevant language. Add statements: instance of (P31, e.g. business Q4830453), official website (P856), inception (P571), country (P17), headquarters (P159), founded by (P112), industry (P452), logo (P154, Commons only), and social IDs (LinkedIn company ID P4264, X username P2002, Crunchbase organization ID P2088, GitHub P2037). Give **each statement a reference** to an independent source. The property numbers are from my knowledge of Wikidata and should be checked in the UI (**unverified this session**).
- **Wikipedia** is much harder. Company notability requires significant, independent, reliable, secondary coverage from several sources. Press releases, funding and launch announcements, and local-only coverage don't count ([WP:NCORP](https://en.wikipedia.org/wiki/Wikipedia:Notability_(organizations_and_companies))). Anyone with a conflict of interest "must disclose who is paying you" and should propose changes via talk-page edit requests or Articles for Creation, not edit directly ([WP:COI](https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest)). **Skill rule:** never have the agent write or edit a client's Wikipedia article. Recommend earning independent coverage first.
- **Why it matters for LLMs.** Kandpal et al. show that a model's ability to answer a factual question "relates to how many documents associated with that question were seen during pre-training", and that long-tail entities are poorly learned ([arXiv 2211.08411](https://arxiv.org/abs/2211.08411), ICML 2023). Wikipedia and Wikidata are heavily represented in training corpora. That is common knowledge rather than a sourced figure, so **unverified** for any specific model. Retrieval-augmented answers depend on the index instead, which is why being indexed and consistent matters.

### 4.3 sameAs strategy

- The definition: "URL of a reference Web page that unambiguously indicates the item's identity" ([schema.org/sameAs](https://schema.org/sameAs); v30.1).
- Include only profiles that are **about this exact entity and that you control or that are authoritative**: Wikidata, Wikipedia (if one exists), LinkedIn company page, Crunchbase, GitHub org, YouTube, X, Instagram, Facebook, TikTok, Google Search profile, app store developer page, official registry pages (companies registry, LEI record at `https://search.gleif.org/#/record/<LEI>`), Google Maps CID for local entities.
- Make the links **reciprocal**: every profile should link back to the canonical website, using the same name, logo and one-line description.
- Use identifiers where you have them: `leiCode`, `duns`, `vatID`, `taxID`, `iso6523Code`, `naics`, `globalLocationNumber`. Google says some are used "behind the scenes to disambiguate" ([Organization doc](https://developers.google.com/search/docs/appearance/structured-data/organization)).
- Don't put competitors, review sites you don't own, or generic topic pages in `sameAs`. Use `about`/`mentions` for topics.

### 4.4 Consistent naming, NAP and disambiguation

- Google Business Profile rules: the name must be the "real-world name, as used consistently on your storefront, website, stationery", with no keywords, taglines or phone numbers. Use as few categories as possible. The address must be a real location, not a PO box or virtual office. Use a local phone number ([GBP guidelines](https://support.google.com/business/answer/3038177?hl=en), accessed 2026-09-26).
- Use one canonical brand string everywhere: title tag suffix, `og:site_name`, WebSite `name`, Organization `name`, GBP, LinkedIn and Wikidata label. Put variants in `alternateName`. Google's site-name system reads WebSite data, `og:site_name`, `<title>` and headings ([site names](https://developers.google.com/search/docs/appearance/site-names)).
- If the brand name is ambiguous (a common word, or shared with another company), put category context next to it in visible copy ("Tapis, the WhatsApp order-capture app"), write a distinctive `description`, add `sameAs` to Wikidata, and use `knowsAbout`/`areaServed`. This is common practice; I found no primary source that it helps disambiguation (**unverified**).
- For local businesses, also claim **Bing Places**. Bing's AI Performance guidance cites it for location accuracy in AI answers ([Bing 2026-02-10](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/)).

### 4.5 Author entities

- Each author gets a dedicated page (ProfilePage + Person) with a bio, credentials, headshot and links out. Articles reference the author by `@id`, and the article byline links to that page.
- Author `sameAs` should point to LinkedIn, ORCID, Google Scholar, Muck Rack or their own site. Google disambiguates authors using `url`/`sameAs` ([Article doc](https://developers.google.com/search/docs/appearance/structured-data/article)).

### 4.6 Strengthening entity associations in LLMs (what an agent can actually do)

1. **Put facts in visible, crawlable text.** The About page should state: who, what, since when, where, founders, product categories, key numbers. Use sentences that pair the brand name with its category and attributes, because live-fetch LLMs read only visible HTML (searchVIU).
2. **Get the same facts published on independent, well-crawled sources**: press, industry directories, Wikidata, association member lists, podcast show notes. Co-occurrence frequency in training data drives recall (Kandpal et al.). Mention quality, frequency and the exact phrasing of the co-occurrence are **unverified** as ranking inputs for any specific AI engine.
3. **Keep facts consistent** across site, schema, GBP, Wikidata, LinkedIn and Crunchbase. Contradictions make models hedge. That is an inference, **unverified**.
4. **Make freshness visible.** Keep an accurate visible "Updated" date, `dateModified`, sitemap `lastmod` reflecting "the true last modification time of the page content" ([Bing 2025-07-31](https://blogs.bing.com/webmaster/2025/7/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search/)), and IndexNow pings.

---

## 5. Feeds are structured data too, and for shopping AI they matter more

### 5.1 Google Merchant Center → AI Mode / Shopping Graph

- Google says: "Using products like Merchant Center (such as Merchant Center feeds) and Google Business Profiles can help your products and services to be visible in both AI responses and other Google Search results" ([AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)). The May 2025 post also says to keep Merchant Center and Business Profile "up-to-date" for multimodal AI ([Google blog 2025-05-21](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search)).
- The Shopping Graph has ">50 billion product listings, 2 billion of which are updated every hour". AI Mode shopping and agentic checkout via Google Pay launched with eligible merchants ([Google blog 2025-11-13](https://blog.google/products-and-platforms/products/shopping/agentic-checkout-holiday-ai-shopping/)).
- On **2026-01-11**, Google announced the **Universal Commerce Protocol (UCP)** for agentic checkout in AI Mode and Gemini, co-developed with Shopify, Etsy, Wayfair, Target and Walmart. It also announced **new Merchant Center attributes for conversational commerce** (product Q&As, accessory compatibility), a Merchant Center-activated **Business Agent**, and **Direct Offers** ads in AI Mode ([Google blog](https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/); [UCP docs](https://developers.google.com/merchant/ucp), accessed 2026-09-26).
- Feeds vs markup: structured data "can improve the accuracy of Google's understanding of… price, discount, and shipping" and helps Merchant Center verify feeds against the site. Merchant Center is mandatory for some surfaces, such as the Shopping tab. Feeds give "greater control over the timing of updates" ([Google ecommerce doc](https://developers.google.com/search/docs/specialty/ecommerce/share-your-product-data-with-google), 2025-12-10). `Product.category` now aligns with feed `product_type`/`google_product_category` (2026-07-07).
- **Skill rule:** for ecommerce, the order of work is (1) a Merchant Center feed with free listings enabled, (2) matching on-page Product/Offer markup, (3) Organization-level return and shipping policies, (4) consistent GTINs.

### 5.2 OpenAI (ChatGPT shopping / Agentic Commerce Protocol)

- The ChatGPT product feed spec ([developers.openai.com/commerce/specs/feed](https://developers.openai.com/commerce/specs/feed), accessed 2026-09-26) accepts **JSONL** in OpenAI format, or **Google-compatible** delimited files (UTF-8 TSV/TXT or CSV, optionally gzipped). Required fields: `item_id`, `title`, `description`, `url`, `brand`, `seller_name`, `image_url`, `availability`, `price` (e.g. `"18.00 USD"`). Recommended fields include `group_id`, `listing_has_variations`, `variant_dict`, `offer_id`, `gtin`, `mpn`, `condition`, `product_category`, `sale_price`, `accepts_returns`, `return_deadline_in_days`, `review_count` and `star_rating`. Flags: `is_eligible_search` (default true), `is_eligible_checkout` (needs separate integration) and `is_ads_eligible`. Legacy `enable_search`/`enable_checkout` are still accepted. Google-compatible uploads get search enabled and checkout disabled. Delivery is by API or SFTP file upload ([commerce overview](https://developers.openai.com/commerce)). Keep titles to 150 characters or fewer and descriptions to 5,000 or fewer.
- Minimal JSONL row (from the spec):

```json
{"item_id": "MUG-350-BLUE", "title": "Blue ceramic mug, 350 mL", "description": "Dishwasher-safe glazed ceramic mug with a handle.", "url": "https://example.com/products/mug-blue", "brand": "Northline", "seller_name": "Northline Home", "image_url": "https://example.com/images/mug-blue.jpg", "price": "18.00 USD", "availability": "in_stock"}
```

- The protocol surfaces are Search (discovery), Instant Checkout (Agentic Checkout Spec), Ads, and Delegated Payments via PSPs ([commerce overview](https://developers.openai.com/commerce)). The merchant application URL (chatgpt.com/merchants) and OpenAI help articles returned 403 to my fetcher, so eligibility details are **unverified** this session.

### 5.3 Microsoft (Bing/Copilot)

- Microsoft Merchant Center Content API product required fields include `offerId`, `title`, `link`, `imageLink`, `price`, `availability`, `condition`, `brand`, `channel`, `contentLanguage` and `targetCountry`, plus `gtin`/`mpn` when the manufacturer assigns them. Feeds are largely Google-compatible ([Microsoft Learn](https://learn.microsoft.com/en-us/advertising/shopping-content/products-resource), updated 2026-01-02).
- IndexNow combined with Product/Offer schema (title, description, price, URL, image, shipping, SKU/GTIN, brand, dateModified) gives faster Shopping and Copilot updates. Shopify has this natively ([Bing 2025-05-19](https://blogs.bing.com/webmaster/2025/5/IndexNow-Enables-Faster-and-More-Reliable-Updates-for-Shopping-and-Ads/)).

### 5.4 Perplexity

- Perplexity launched shopping ("Buy with Pro") and a free **Merchant Program** in Nov 2024, where merchants share product specs and data for better placement. Every Perplexity URL I tried returned 403, so this is **unverified this session**. It is based on prior knowledge of the 2024-11-18 announcement.

---

## 6. Meta tags that matter (and their role in AI snippets)

| Tag | What to do | Evidence |
|---|---|---|
| `<title>` | Unique, descriptive, brand-suffixed. Google's title-link sources are `<title>`, the main visual title, `<h1>`, `og:title`, prominent text, anchors and WebSite data | [title links](https://developers.google.com/search/docs/appearance/title-link) (2025-12-10). Microsoft: title, description and H1 "are important signals AI systems use", with the H1 matching the title ([MS 2025-10-08](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers)) |
| `meta description` | A summary of value or outcome, no stuffing. Google snippets are "primarily created from the page content itself" and use the description when it's more accurate | [snippets](https://developers.google.com/search/docs/appearance/snippet) (2026-04-20) |
| robots `nosnippet` | Also blocks use "as a direct input for AI Overviews and AI Mode" | [robots meta](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) (2026-03-24) |
| robots `max-snippet:N` | Limits text snippets **and** AIO/AI Mode input. Doesn't block rich results fed by structured data. For AI visibility use `max-snippet:-1` | same |
| `max-image-preview:large` | Allows large thumbnails (Discover, AI Mode images). Recommended default | same |
| `data-nosnippet` attribute | Excludes page sections from snippets and AI summaries. **Bing added support on 2025-10-15**, covering Copilot | [Bing blog](https://blogs.bing.com/webmaster/2025/10/Bing-Introduces-Support-for-the-data-nosnippet-HTML-Attribute/) |
| Robots meta outside `<head>` | Google documented how it handles these on 2026-03-24 (behaviour unchanged). Still, put it in `<head>` | [updates](https://developers.google.com/search/updates) |
| Open Graph | Required: `og:title`, `og:type`, `og:image`, `og:url`. Use `og:site_name`, `og:description`, `og:image:width/height/alt`, and for articles `article:published_time`, `article:modified_time`, `article:author`, `article:section`, `article:tag` | [ogp.me](https://ogp.me) (accessed 2026-09-26). Google uses `og:image` **and** schema `image` for thumbnails ([images doc](https://developers.google.com/search/docs/appearance/google-images), 2026-03-02) and `og:site_name` for site names. Schema.org v30.0 added OG equivalences |
| Twitter/X cards | `twitter:card=summary_large_image`, `twitter:site`, and `twitter:title`/`description`/`image` falling back to OG | developer.x.com docs returned 402 to my fetcher, so current details are **unverified** |
| `rel=canonical` | One canonical per cluster. Self-referencing. Consistent with sitemap, hreflang and internal links | [Google canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls). Bing: AI systems "cluster similar pages" and pick one, so clear canonicals keep the wrong version from being cited ([Bing 2025-12-19](https://blogs.bing.com/webmaster/2025/12/Does-Duplicate-Content-Hurt-SEO-and-AI-Search-Visibility/)) |
| `hreflang` | Reciprocal alternates plus `x-default`. Language or language-region codes | [Google localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions); Bing same post |
| Dates | Visible byline date + `datePublished`/`dateModified` + `article:modified_time`, all consistent | [byline dates](https://developers.google.com/search/docs/appearance/publication-dates) |

**Head template the agent can emit:**

```html
<title>How to forecast Ramadan demand for grocery retail | Example Analytics</title>
<meta name="description" content="A step-by-step method using three years of POS data, with benchmark MAPE by category.">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.example.com/blog/forecasting-ramadan-demand/">
<link rel="alternate" hreflang="en" href="https://www.example.com/blog/forecasting-ramadan-demand/">
<link rel="alternate" hreflang="ms" href="https://www.example.com/ms/blog/ramalan-permintaan-ramadan/">
<link rel="alternate" hreflang="x-default" href="https://www.example.com/blog/forecasting-ramadan-demand/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Example Analytics">
<meta property="og:title" content="How to forecast Ramadan demand for grocery retail">
<meta property="og:description" content="A step-by-step method using three years of POS data.">
<meta property="og:url" content="https://www.example.com/blog/forecasting-ramadan-demand/">
<meta property="og:image" content="https://www.example.com/img/ramadan-demand-16x9.jpg">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="900">
<meta property="og:image:alt" content="Weekly unit sales of dates, 2023–2026">
<meta property="article:published_time" content="2026-02-10T09:00:00+08:00">
<meta property="article:modified_time" content="2026-09-20T14:30:00+08:00">
<meta property="article:author" content="https://www.example.com/about/jane-tan/">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ "...": "single @graph from §3.2" }</script>
```

---

## 7. Validation tools and automated checks

- **Rich Results Test** (search.google.com/test/rich-results) shows which *Google* rich results a URL or snippet qualifies for. It dropped HowTo (2023), the retired 2025 types (2025-09-09), practice problem (2026-01) and FAQ (June 2026). **Schema Markup Validator** (validator.schema.org) does generic schema.org validation "without Google-specific validation" and replaced the old Structured Data Testing Tool ([Google: Test your structured data](https://developers.google.com/search/docs/appearance/structured-data), accessed 2026-09-26).
- **Search Console**: rich result reports, URL Inspection (rendered HTML, to confirm JS-injected JSON-LD), and Merchant listings/Product snippets reports. AI Mode traffic has counted in Search Console totals since 2025-06-16 ([updates](https://developers.google.com/search/updates)).
- **Bing Webmaster Tools**: the AI Performance report (citations, grounding queries, cited pages) is in public preview since 2026-02-10 ([Bing](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/)). BWT has historically included a markup validator, but its current status could not be fetched (the help page is JS-only), so treat it as **unverified**.
- **Automated checks the skill should run** (CI or agent):
  1. Fetch **raw HTML** (no JS) and parse every `application/ld+json` block. Fail if JSON is invalid or if JSON-LD appears only after rendering (compare raw vs rendered).
  2. Build the graph. Flag duplicate entities with conflicting `name`/`url`, dangling `@id` references, and more than one Organization with different names.
  3. For each type, check Google's required properties (tables in §3) and warn on missing recommended ones.
  4. **Visible-parity check:** every string or number in `name`, `headline`, `price`, `ratingValue`, `datePublished`, `dateModified`, `author.name` and FAQ answer text must appear in the visible DOM text (after normalisation).
  5. Cross-source parity: `<title>` ≈ `og:title` ≈ `headline` ≈ H1; `canonical` = `og:url` = `@id` base; `article:modified_time` = `dateModified`; feed price = schema price = visible price.
  6. Flag retired or deprecated usage (SearchAction, HowTo, FAQ-for-rich-results, ClaimReview, CourseInfo and so on) as "no Google display" (info, not error).
  7. Robots: warn if `nosnippet`, `max-snippet` less than about 160, `noindex`, or `data-nosnippet` covers key answer passages. Warn if `max-image-preview` is not `large`.
  8. Images: the logo is at least 112 px and returns 200. `og:image` and schema `image` are absolute, crawlable, and not the site logo (Google advises against a generic logo as the preferred image, [images doc](https://developers.google.com/search/docs/appearance/google-images)).
  9. `sameAs` URLs resolve (200) and link back to the site where possible.
  10. Optionally submit to validator.schema.org and the Rich Results Test (the RRT has no official public API; **unverified**).

---

## 8. Priority checklist for the skill (by impact on AI + SEO)

1. Indexable, snippet-eligible pages (no over-restrictive robots). This is Google's only hard AI eligibility rule.
2. Visible, fact-dense text: entity facts on About, answers in body copy, visible dates.
3. A site-wide `@graph` with Organization (logo, legalName, sameAs, identifiers) and WebSite (site name), plus a per-page WebPage/Article/Person linked by `@id`.
4. Author pages (ProfilePage/Person) with sameAs, linked from bylines.
5. Commerce: a Merchant Center feed plus Product/Offer markup with Organization-level shipping and returns, an OpenAI-format or Google-compatible feed for ChatGPT, and IndexNow for Bing.
6. Local: GBP and Bing Places with an identical NAP, plus a LocalBusiness subtype with geo and hours.
7. Entity footprint: Wikidata item (if it meets notability, with references), consistent LinkedIn/Crunchbase/GitHub profiles, and a Google Search profile or knowledge panel claim.
8. Meta: title/description/OG/canonical/hreflang consistent, `max-snippet:-1, max-image-preview:large`.
9. Keep FAQ/HowTo markup only where the content is real. Never promise rich results from them.
10. Validate in CI (§7), and re-check Google's [updates changelog](https://developers.google.com/search/updates) (RSS: `https://developers.google.com/search/updates/search_docs_updates.rss`) because types keep being retired.
