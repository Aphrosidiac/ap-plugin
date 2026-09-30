# 08 — Classic & Technical SEO Foundations (state as of 2026-09-26)

> Researcher 8 of 9. Scope: everything a site must get right in classic/technical SEO, because Google says its generative AI features "are rooted in our core Search ranking and quality systems". Every claim carries a source URL and the date the page was last updated or published (the "as of" date). A claim that could not be checked against a primary source is marked **unverified**.
>
> Access notes: fetched 2026-09-26. The session hit its web-search quota about a third of the way through, so later facts come from direct WebFetch of primary docs. Where a secondary source (SEL, SER, SEJ) is the only evidence, this file says so.

---

## 0. The ground truth to build the skill on

1. **AI search sits on classic SEO.** Google's generative-AI optimization guide says: "the best practices for SEO continue to be relevant because our generative AI features on Google Search are rooted in our core Search ranking and quality systems". It names RAG over the Search index and "query fan-out" as the retrieval mechanisms. Source: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide (updated 2026-07-10).
2. **There are no extra technical requirements for AI features.** A page "must be indexed and eligible to be shown in Google Search with a snippet". "There are no additional technical requirements." And: "You don't need to create new machine readable files, AI text files, or markup to appear in these features." Source: https://developers.google.com/search/docs/appearance/ai-features (updated 2025-12-10).
3. **llms.txt, chunking and AI-specific rewriting.** The 2026-06-15 mythbusting section says llms.txt and special markup are not used: "Google Search itself doesn't use them", and they neither help nor harm. It also says "There's no requirement to break your content into tiny pieces" and "Structured data isn't required for generative AI search". Source: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting (updated 2026-07-10); changelog entry at https://developers.google.com/search/updates (2026-06-15).
4. **Minimum technical eligibility.** Google Search needs three things: (1) Googlebot isn't blocked, (2) the page returns HTTP 200, (3) the page has indexable text content that complies with spam policies. Source: https://developers.google.com/search/docs/essentials/technical (updated 2025-12-18).
5. **Snippet controls apply to AI too.** `nosnippet` "applies to all forms of search results", AI Overviews included. `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex` are the controls for AI features. Google-Extended does **not** control inclusion in Search AI features. Sources: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag (2026-03-24) and https://developers.google.com/search/docs/appearance/ai-features (2025-12-10).
6. **Market context for Malaysia (MY).** Google had 92.99%, Bing 4.42%, Yahoo 1.59%, Yandex 0.52% and DuckDuckGo 0.35% (Aug 2026). For MY sites, Google is the foundation, and Bing matters mainly because it grounds Copilot and ChatGPT-style answers. Source: https://gs.statcounter.com/search-engine-market-share/all/malaysia (Aug 2026 data).

**Implication for the skill:** a technical SEO failure is also a GEO/AEO failure. If a page cannot be crawled, rendered, canonicalised, indexed and snippeted, no AI answer engine that grounds on Google or Bing will cite it.

---

## 1. Algorithm, core and spam updates, 2024 to 2026

### 1.1 Official ranking-update timeline

Source for dates and durations: Google Search Status Dashboard, ranking incident history, https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history (fetched 2026-09-26).

| Update | Start | Duration | Notes |
|---|---|---|---|
| March 2024 core update | 2024-03-05 | 45 days | The helpful content system was folded into core ranking. Google expected 40–45% less unhelpful content in results. Three new spam policies were launched (below). Source: https://developers.google.com/search/blog/2024/03/core-update-spam-policies (Mar 2024). |
| March 2024 spam update | 2024-03-05 | 14d 21h | Site reputation abuse enforcement began 2024-05-05. |
| June 2024 spam update | 2024-06-20 | 7d 1h | |
| August 2024 core update | 2024-08-15 | 19d 4h | |
| November 2024 core update | 2024-11-11 | 23d 13h | Site reputation abuse was also clarified in Nov 2024: first-party oversight does **not** exempt third-party content (see §1.2). |
| December 2024 core update | 2024-12-12 | 6d 4h | |
| December 2024 spam update | 2024-12-19 | 7d 2h | |
| March 2025 core update | 2025-03-13 | 13d 21h | |
| June 2025 core update | 2025-06-30 | 16d 18h | |
| August 2025 spam update | 2025-08-26 | 26d 15h | |
| December 2025 core update | 2025-12-11 | 18d 2h | On 2025-12-09 the docs added a section on "smaller, continuous core updates". |
| February 2026 Discover update | 2026-02-05 | 21d 17h | Discover only. |
| March 2026 spam update | 2026-03-24 | 19h 30m | |
| March 2026 core update | 2026-03-27 | 12d 4h | |
| May 2026 core update | 2026-05-21 | 11d 21h | Complete 2026-06-02. Google's line: "a regular update designed to better surface relevant, satisfying content for searchers from all types of sites". There was no companion blog post (SEL/SER, https://www.seroundtable.com/google-may-2026-core-update-done-41435.html). |
| June 2026 spam update | 2026-06-24 | 2d 1h | |
| August 2026 spam update | 2026-08-18 | 2d 16h | |
| September 2026 spam update | 2026-09-24 | ongoing | Google did not name a target. SEL reports it is **not** a link-spam update and is the 4th spam update of 2026 (https://searchengineland.com/google-releases-september-2026-spam-update-491267, 2026-09-24; secondary source). |

### 1.2 Current core-update guidance

Source: https://developers.google.com/search/docs/appearance/core-updates (updated 2025-12-10).

- Core updates are broad. They are "not targeted at specific sites". Google also releases smaller core updates "continually", without announcement.
- **How to diagnose a drop:** confirm the rollout is complete, wait **one week** after completion, then compare before and after in Search Console. Segment by search type (web, image, video, news). Google treats small moves (for example position 2 to 4) as no action needed and large moves (4 to 29) as grounds for a deeper review.
- **Recovery:** "Some changes can take effect in a few days, but it could take several months". There is no guarantee.
- **Evaluate the whole site**, not just individual pages, against "helpful, reliable, people-first content".

### 1.3 The Helpful Content system in 2026

- The system no longer runs separately. Since March 2024 it has been part of core ranking (https://developers.google.com/search/blog/2024/03/core-update-spam-policies).
- The self-assessment framework still stands: people-first content, E-E-A-T (with trust as the most important element), and Who/How/Why disclosure, including transparency about AI or automation use. Source: https://developers.google.com/search/docs/fundamentals/creating-helpful-content (updated 2025-12-10).
- E-E-A-T is **not** itself a ranking factor. The SEO Starter Guide answers "No, it's not" (https://developers.google.com/search/docs/fundamentals/seo-starter-guide, 2025-12-10).

### 1.4 Spam policies, the current list

Source: https://developers.google.com/search/docs/essentials/spam-policies (updated 2026-08-28).

The policies are: cloaking, doorway abuse, expired domain abuse, hacked content, hidden text and links, keyword stuffing, link spam, machine-generated traffic, malicious practices (which now include **back button hijacking**), misleading functionality, scaled content abuse, scraping, site reputation abuse, sneaky redirects, thin affiliation, and user-generated spam.

Key definitions (quoted from the page above):

- **Scaled content abuse:** "many pages are generated for the primary purpose of manipulating search rankings and not helping users … no matter how it's created". The policy covers AI, human and hybrid production alike.
- **Site reputation abuse:** "Third-party content published on a host site mainly because of that host's already-established ranking signals". Third-party content explicitly includes "freelancers, white-label services, and content created by people not employed directly by the host site".
- **Expired domain abuse:** buying an expired domain and repurposing it "primarily to manipulate search rankings".
- **Back button hijacking:** announced 2026-04-13, enforced from 2026-06-15. It covers interfering with browser history so that Back sends users to pages they never visited, or to interstitial recommendations or ads. The penalty is a manual action or an automated demotion. Source: https://developers.google.com/search/blog/2026/04/back-button-hijacking (2026-04-13). Fix for the skill: never `history.pushState` fake entries on load, and never trap `popstate`.
- **Spam policies now cover AI responses.** Added 2026-05-15 per the changelog (https://developers.google.com/search/updates).
- **Spam reports can now lead to manual actions.** Clarified 2026-04-14 and 2026-04-23 (same changelog).

**Site reputation abuse in the EEA.** On 2025-11-12 the European Commission opened a Digital Markets Act (DMA) investigation into the policy. From **2026-08-30**, site reputation abuse manual actions still show in Search Console for EEA sites but have **no effect for searchers inside the EEA**. Outside the EEA the policy is unchanged. The Google docs changelog records this on 2026-08-28, and the blog post is at https://developers.google.com/search/blog/2026/08/update-site-reputation-policy (body not fetchable). Secondary sources: https://www.seroundtable.com/google-site-reputation-policy-eea-41968.html and https://ppc.land/google-drops-parasite-seo-penalties-in-europe-under-commission-mandate/. For Malaysia, the full policy applies.

### 1.5 2026 ranking-documentation changes that matter to a technical skill

Source: https://developers.google.com/search/updates (fetched 2026-09-26).

| Date | Change | Skill action |
|---|---|---|
| 2025-12-15/17/18 | JS: noindex handling with JS, canonical best practice for JS, and "JavaScript execution on non-200 HTTP status codes". Crawling docs moved to developers.google.com/crawling. | Serve noindex and canonical in the initial HTML. Don't rely on JS for error pages. |
| 2026-02-03 | Googlebot reads only the **first 2MB** of an HTML or other supported file. Each subresource has the same 2MB cap. PDFs get 64MB. The general Google crawler default is 15MB. | Flag any HTML over 2MB uncompressed. Put `<head>` metadata and main content early. |
| 2026-03-02 | Preferred image via metadata (`primaryImageOfPage`, `og:image`). | Set `og:image` on every page. |
| 2026-03-24 | Robots meta tags are honoured **outside `<head>`** too. | Scan the body for stray `noindex`, for example from CMS widgets. |
| 2026-04-13 | Back button hijacking policy. | Audit `pushState` and `popstate` usage. |
| 2026-04-20 | "Read more" deep links in snippets. | Keep content visible, don't reset scroll on load, preserve hash fragments. |
| 2026-05-08 / 06-15 | FAQ rich result deprecated, then docs removed. | Don't promise FAQ rich results. FAQPage markup is harmless but no longer produces a rich result. |
| 2026-05-15 | Generative AI optimization guide published. | See §0. |
| 2026-06-05 | Guidance on third-party SEO tools: "Third-party tools don't have access to our internal ranking data." (https://developers.google.com/search/docs/fundamentals/third-party-seo) | Don't optimise for DA/DR-type scores. |
| 2026-06-15 | llms.txt clarified: no effect on Google Search. | Optional; its only value is for non-Google agents. |
| 2026-06-17 / 08-20 | Site move docs add domain variants: file Change of Address for every verified variant. | Include this in the migration checklist. |
| 2026-07-10 | Canonicalization troubleshooting adds re-evaluation timing. | |
| 2026-08-28 | Supported favicon formats are listed. Site reputation abuse changes in the EEA. | |
| 2026-09-24 | VideoObject gains `creator`; `interactionStatistic` updated. | Update the video schema template. |

### 1.6 The May 2024 API leak and the DOJ trial: use with caution

- **What leaked:** Google Content Warehouse API docs were accidentally published to GitHub. Rand Fishkin (SparkToro) and Mike King (iPullRank) analysed them publicly from 2024-05-27. Source: https://sparktoro.com/blog/an-anonymous-source-shared-thousands-of-leaked-google-search-api-documents-with-me-everyone-in-seo-should-see-them/ (2024-05-27).
- **Attributes discussed:** `siteAuthority`, NavBoost and click data (good clicks, bad clicks, last longest click), Chrome-derived signals, a "hostAge"/sandbox-like attribute, title-match features, and demotions. Summary: https://www.hobo-web.co.uk/the-google-content-warehouse-leak-2024/ (secondary).
- **Corroboration from the DOJ trial:** Pandu Nayak's testimony confirmed that **NavBoost** uses about 13 months of aggregated click data and that **Glue** does the same for SERP features. Summaries: https://www.hobo-web.co.uk/navboost-how-google-uses-large-scale-user-interaction-data-to-rank-websites/ and https://www.kopp-online-marketing.com/what-we-can-learn-from-doj-trial-and-api-leak-for-seo (secondary).
- **Caveats for the skill:**
  - The documents list attributes, not weights. Many may be deprecated or experimental.
  - Google's public response called the documents out of context and possibly outdated (**unverified wording**).
  - No attribute should be "optimised" directly.
  - Two practical takeaways hold up: (a) satisfying the click matters, so titles and snippets that accurately set expectations, and content that ends the search journey, beat bait; (b) site-level quality spills over to all of a site's pages, so prune or improve thin sections rather than only fixing single URLs.
  - **Never** recommend click manipulation. It is "machine-generated traffic" spam.

---

## 2. Crawling and indexing

### 2.1 robots.txt

Source: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt (updated 2026-08-31).

- The file must sit at the root of each **protocol + host + port**. A subdomain needs its own file.
- **Size limit is 500 KiB.** Anything after that is ignored. Google caches the file for up to 24 hours.
- How the status code of robots.txt itself is handled:
  - **2xx:** parsed normally.
  - **3xx:** at least 5 hops are followed, after which it is treated as 404.
  - **4xx other than 429:** treated as if there is no robots.txt, so everything may be crawled.
  - **5xx (and 429):** crawling stops for 12 hours. Google then uses the cached copy for up to 30 days, and after that assumes there is no file. A 5xx on robots.txt effectively halts crawling of the whole site.
- **Supported fields:** `user-agent`, `allow`, `disallow`, `sitemap`. `crawl-delay` and `noindex` are ignored by Google. Bing honours `crawl-delay` (**unverified this session**, long-standing Bing behaviour).
- **Precedence:** the most specific (longest) matching path wins. On a tie, the least restrictive rule wins. `*` matches any sequence of characters and `$` anchors the end of the URL.
- **Blocking a URL in robots.txt does not deindex it.** Google may still index it without content if it is linked. See the noindex rules in §2.2.

Baseline template for the skill (adapt the paths per site; never block CSS or JS needed for rendering):

```txt
# https://example.com/robots.txt
User-agent: *
Disallow: /cart
Disallow: /checkout
Disallow: /account
Disallow: /*?*sort=
Disallow: /*?*sessionid=
Allow: /*?page=            # keep pagination crawlable if paginated via params

Sitemap: https://example.com/sitemap_index.xml
```

The per-AI-bot allow/deny policy (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended and others) is covered by researcher 03. Only one point matters here: Google Search AI features are controlled by **Googlebot** rules, not by Google-Extended.

### 2.2 Meta robots, X-Robots-Tag and noindex

Sources: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag (2026-03-24) and https://developers.google.com/search/docs/crawling-indexing/block-indexing (2025-12-10).

- **Rules:** `noindex`, `nofollow`, `none`, `nosnippet`, `max-snippet:N`, `max-image-preview:none|standard|large`, `max-video-preview:N`, `notranslate`, `noimageindex`, `unavailable_after:<date>`, `indexifembedded`. The `data-nosnippet` attribute works on `span`, `div` and `section`. Bing added `data-nosnippet` support on 2025-10-15 (https://blogs.bing.com/webmaster/).
- **Conflicts:** "the more restrictive rule applies."
- **noindex must be crawlable.** "For the noindex rule to be effective, the page or resource must not be blocked by a robots.txt file."
- **noindex in the initial HTML may stop rendering.** If the initial HTML has `noindex`, Google may skip rendering, so JS **cannot** remove it later (https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics, 2026-03-04).
- For non-HTML files (PDF, images), use the header: `X-Robots-Tag: noindex`.
- The recommended default for content pages is `max-image-preview:large`. It is needed for large images in Discover (**Discover requirement from memory; unverified this session**).

```html
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
```

**noindex or Disallow: decision table**

| Goal | Use | Don't |
|---|---|---|
| Keep a page out of the index | `noindex`, and leave it crawlable | Disallow (it can still be indexed from links) |
| Save crawl on infinite or low-value URL spaces (filters, search results, calendars) | Disallow in robots.txt | noindex (Google still has to crawl each URL to see it) |
| Consolidate duplicates | 301/308, or `rel=canonical` | noindex, or Disallow |
| Remove something urgently | Search Console Removals (temporary), plus noindex, 404 or 410 | Disallow alone |

### 2.3 Canonicalization

Source: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (updated 2026-07-10).

- **Signal strength:** redirects (strong) and `rel=canonical` (strong) outrank sitemap inclusion (weak). Using several methods together strengthens the signal.
- **Do:**
  - Use absolute URLs.
  - Put `<link rel="canonical">` **only in `<head>`**.
  - Include a self-referencing canonical on canonical pages.
  - Link internally to the canonical URL.
  - Prefer HTTPS.
  - Use `Link: <url>; rel="canonical"` HTTP headers for PDFs.
  - List only canonical URLs in sitemaps.
  - Keep hreflang targets canonical.
- **Don't:**
  - Use robots.txt for canonicalization.
  - Use the URL removal tool for it.
  - Use `noindex` to choose between duplicates within a site.
  - Declare conflicting canonicals through different methods.
  - Use fragments.
  - Use JS to **change** a canonical to a different URL. Put it in the initial HTML (https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics, 2026-03-04).
- **Pagination:** don't canonicalize page 2+ to page 1 (§2.7).
- **Diagnosis:** in URL Inspection, compare "User-declared canonical" with "Google-selected canonical". In the Page indexing report, watch "Duplicate, Google chose different canonical than user".

### 2.4 Redirects

Sources: https://developers.google.com/search/docs/crawling-indexing/301-redirects (2026-04-14) and https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes (2026-08-20).

- **Permanent** redirects make the target the one shown in results: 301, 308, meta refresh with 0 seconds, and JS `location`.
- **Temporary** redirects keep the source shown: 302, 303, 307, and meta refresh with a delay above 0.
- **Order of reliability:** server-side, then meta refresh, then JS, then a "crypto" link.
- Googlebot follows **up to 10 hops**. Site-move guidance says to avoid chains longer than 5 and ideally keep them under 3. Keep redirects "for as long as possible, generally at least 1 year".
- Use the Change of Address tool for domain moves, for **all** verified variants (www, non-www, subdomains). It is not needed for HTTP to HTTPS or www changes on the same domain.
- **Skill rule:** every legacy URL goes to its final destination in a single 301/308 hop. Host and protocol normalisation (http→https, non-www→www, trailing slash) should be collapsed into one hop.

### 2.5 Status codes and soft 404s

Source: https://developers.google.com/search/docs/crawling-indexing/http-network-errors (updated 2026-02-04).

- **2xx:** eligible for indexing. A 200 with an error or empty body is flagged as a **soft 404**.
- **4xx:** 404 and 410 remove the URL from the index; the two behave practically the same. 401 and 403 are also treated as "not available" and **do not** reduce crawl rate. **429** is treated like a server error.
- **5xx and 429:** crawl rate drops in proportion to the errors. If they persist, URLs are removed from the index.
- **SPAs:** for unknown routes, either redirect to a URL that returns a real 404 from the server, or inject `noindex`. Since Dec 2025 Google has said pages with non-200 status may not be rendered at all (https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics). So a JS-built 404 page on a 404 status is fine, but a 200 "not found" page is a soft 404.
- **Emergency throttling:** return 503 or 429 temporarily, for hours not days. The Search Console crawl-rate limiter tool was retired in Jan 2024 (**unverified this session**).

### 2.6 Crawl budget, faceted navigation, parameters and index bloat

Sources: https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget (2026-07-22) and https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation (2025-12-18).

- **Who needs to care:** sites with 1M+ pages that change weekly, sites with 10k+ pages that change daily, or sites with a large "Discovered – currently not indexed" count. Everyone else mostly needs clean URL hygiene rather than budget management.
- **Crawl budget** = the crawl capacity limit (driven by host health and speed) × crawl demand (popularity, staleness, perceived quality).
- **What helps:**
  - Consolidate duplicates.
  - Disallow infinite spaces.
  - Return 404 or 410 for removed content.
  - Kill soft 404s and redirect chains.
  - Keep sitemaps with accurate `lastmod`.
  - Make pages faster and use HTTP caching.
- **What doesn't help:** `noindex` (the URLs are still fetched), and toggling robots.txt to "reallocate" budget.
- **Faceted navigation**, if the facets should **not** be indexed:
  - Disallow them, for example `Disallow: /*?*products=` with `Allow: /*?products=all$`.
  - Or put filter state in URL fragments.
  - Or use `rel="nofollow"` on filter links.
- **Faceted navigation**, if some facets **should** be indexed:
  - Use `&` as the separator and a consistent parameter order.
  - Return **404** for filter combinations with no results; do not redirect them to a generic page.
  - Canonicalize near-duplicates.
- **Index bloat check:** compare the count of indexable URLs your crawler finds with the "Indexed" count in the Page indexing report and with the number of pages you actually want ranking. Treat thin tag/archive pages, internal search results, parameter duplicates, staging hosts and printer versions as bloat.
  - Consolidate them with 301 or canonical.
  - Or noindex them and leave them crawlable.
  - Or disallow them if the URL space is infinite.

### 2.7 Pagination and infinite scroll

Source: https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading (updated 2025-12-10).

- Link each page to the next with `<a href>`. Give each page **its own canonical**, not page 1. Don't use `#` for page numbers.
- **`rel=next/prev` is not used by Google.** It is harmless, and other engines may use it.
- Infinite scroll and "load more" need crawlable paginated URLs as the fallback, for example `?page=2`, updated with the History API as the user scrolls, with each page listed in sitemaps or feeds.
- Keep filter and sort variants out of the index (§2.6).

### 2.8 JavaScript SEO

Source: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics (updated 2026-03-04).

- **Pipeline:** crawl, then a render queue (headless evergreen Chromium), then index. Only 200 pages are queued for rendering.
- **Rules for the skill:**
  1. Ship critical content, `<title>`, meta description, canonical, robots meta, hreflang and JSON-LD in the **server HTML**. Use SSR, SSG or ISR for public pages. Google: "server-side or pre-rendering is still a great idea because it makes your website faster for users and crawlers, and not all bots can run JavaScript". Most AI crawlers do not execute JS (see researcher 03).
  2. Real links only: `<a href="/path">`. `onclick`, `routerLink`-only and `<span href>` are not crawlable (https://developers.google.com/search/docs/crawling-indexing/links-crawlable, 2025-12-10).
  3. Use History API routing, not `#/` fragments.
  4. Give static assets fingerprinted filenames. Googlebot caches aggressively and may ignore cache headers.
  5. Don't put `noindex` in the initial HTML with the plan of removing it with JS.
  6. Lazy-load only below-the-fold content, using native `loading="lazy"` or IntersectionObserver. Never gate primary content on scroll or click.
  7. Dynamic rendering is a workaround, not a recommendation.
- **Size:** Googlebot processes only the first **2MB** of HTML and of each JS or CSS resource (https://developers.google.com/search/docs/crawling-indexing/googlebot, 2026-02-03). Giant inline JSON hydration blobs, such as `__NEXT_DATA__` over 1MB, put content at risk of being cut off.
- **Verification:** use URL Inspection → "View crawled page" (rendered HTML plus screenshot), or the Rich Results Test. Locally, `curl` the raw HTML and diff it against the rendered DOM (§12).

### 2.9 XML sitemaps

Source: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap (updated 2026-07-08).

- Limits are **50MB uncompressed or 50,000 URLs** per file. Use a sitemap index beyond that. Bing notes an index can reach 2.5B URLs (https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search, 2025-07-31).
- Files must be UTF-8 with absolute, canonical, 200-status, indexable URLs only.
- **`<lastmod>`** is used only if "consistently and verifiably accurate". It should reflect significant changes to main content, structured data or links, not copyright dates or build time. Bing calls lastmod "a key signal" for recrawl and wants full ISO 8601 date-time (same Bing blog).
- **`<priority>` and `<changefreq>` are ignored** by Google.
- **Submit** through Search Console, a `Sitemap:` line in robots.txt, or the Search Console API. The sitemap ping endpoint is deprecated (retired 2023, **unverified this session**).
- **Image sitemaps:** only `<image:image>` and `<image:loc>` are supported, up to 1,000 images per page. `caption`, `title`, `geo_location` and `license` were removed in 2022. Source: https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps (2025-12-10).
- **Video sitemaps:** require `thumbnail_loc`, `title`, `description`, and one of `content_loc` or `player_loc`. `duration` ranges from 1 to 28,800. `category`, `gallery_loc`, `price` and `tvshow` are removed. Source: https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps (2026-05-20).
- **News sitemaps:** only articles from the **last 2 days**, at most 1,000 `<news:news>` entries. Required: `publication/name`, `language`, `publication_date` and `title`. Source: https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap (2025-12-10).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemaps/pages.xml</loc><lastmod>2026-09-20T08:15:00+08:00</lastmod></sitemap>
  <sitemap><loc>https://example.com/sitemaps/products-1.xml</loc><lastmod>2026-09-25T02:00:00+08:00</lastmod></sitemap>
</sitemapindex>
```

**Skill rule:** generate `lastmod` from the content's real `updated_at`, never from the build time. A sitemap URL that is non-200, noindexed, non-canonical or redirected is a failure.

### 2.10 IndexNow (Bing and others, not Google)

Sources: https://www.indexnow.org/documentation, https://www.indexnow.org/searchengines.json (fetched 2026-09-26) and https://www.bing.com/indexnow/getstarted.

- **Participating engines:** Bing, Yandex, Seznam, Naver, Yep, Internet Archive and **Amazonbot**. **Google is not listed.**
- **Key:** 8–128 characters from `[a-zA-Z0-9-]`, hosted at `/{key}.txt`, or elsewhere and pointed to with `keyLocation`.
- **Submit** only URLs that were added, updated or deleted. Up to 10,000 URLs per POST. A submission to one engine is shared with all of them.
- **Responses:** 200 OK, 202 (key validation pending), 400, 403 (bad key), 422 (URL doesn't match host), 429 (possible spam).
- **Integrations:** Yoast, Rank Math, AIOSEO, Wix, Duda, Shopify, and Cloudflare Crawler Hints.

```bash
curl -s -X POST https://api.indexnow.org/indexnow \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{"host":"example.com","key":"a1b2c3d4e5f6a7b8","keyLocation":"https://example.com/a1b2c3d4e5f6a7b8.txt",
       "urlList":["https://example.com/new-page","https://example.com/updated-page"]}' -w '%{http_code}\n'
```

Wire it to publish, update and delete hooks in the CMS or deploy pipeline. Bing recommends combining sitemaps (for coverage) with IndexNow (for real time) (Bing blog, 2025-07-31).

### 2.11 Verifying crawlers

Sources: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot (2026-03-20) and https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers (2026-08-19).

- **Verify Googlebot** with reverse DNS on the IP (it must resolve to `googlebot.com`, `google.com` or `googleusercontent.com`), then a forward DNS lookup that matches the IP. Alternatively, check against the JSON range files at `https://developers.google.com/static/crawling/ipranges/{common-crawlers,special-crawlers,user-triggered-fetchers,user-triggered-fetchers-google,user-triggered-agents}.json`.
- **User-triggered fetchers generally ignore robots.txt.** This group now includes **`Google-Agent`**, which "navigates web and performs actions on user request", as well as `Google-GeminiNotebook`, `Google-Pinpoint`, `Google-Read-Aloud` and `Google-CWS`. **WAF rules must not block these by user-agent heuristics** if the site wants to be agent-operable.
- **Protocols and compression:** crawlers use HTTP/1.1 or HTTP/2 and support gzip, deflate and **Brotli** (https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers, 2026-06-12).

```bash
host 66.249.66.1            # → crawl-66-249-66-1.googlebot.com
host crawl-66-249-66-1.googlebot.com   # → 66.249.66.1  (must match)
```

---

## 3. Core Web Vitals and page experience (2026)

### 3.1 Metrics and thresholds (unchanged since March 2024)

Source: https://web.dev/articles/vitals (updated 2024-10-31). INP replaced FID on 2024-03-12 (https://web.dev/blog/inp-cwv-march-12).

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 |

- Measure at the **75th percentile** of page loads, separately for mobile and desktop.
- New metrics move through an experimental → pending (at least 6 months) → stable lifecycle. Stable metrics change at most once a year.
- **2026 status:**
  - No threshold changes, and no new Core Web Vital, in any primary source found.
  - Some blogs claim a 2026 change to how INP is computed (https://monstermegs.com/blog/core-web-vitals-update/). This is **unverified**: the CrUX release notes don't mention it.
  - The August 2026 CrUX release flagged an INP regression "cause for concern" with no explanation (https://developer.chrome.com/docs/crux/release-notes, released 2026-09-08).
- **Web-wide pass rates:** about 55.6% of origins pass all three CWV (Aug 2026 CrUX, 18.29M origins). Good LCP is around 68%, and good CLS around 81% (Feb 2026). Same release-notes source.
- **CrUX changes:**
  - Jan 2025: LCP image subparts, LCP resource type and RTT were added. The ECT dimension was retired.
  - Nov 2025: the CrUX Dashboard (Looker Studio) was deprecated. Use **CrUX Vis** or the API.
  - Mar 2025: DevTools shows CrUX field data in the Performance panel.
- **Soft navigations (SPAs):** the final origin trial ran in Chrome 147–149, with launch "later this year". Google says the trial is "to evaluate the new API and not how this data will be used in CrUX". SPA route changes therefore **do not** yet count in CrUX or ranking. Source: https://developer.chrome.com/blog/final-soft-navigations-origin-trial (2026-04-20).

### 3.2 How CWV are used in ranking

Source: https://developers.google.com/search/docs/appearance/page-experience (updated 2026-09-22).

- "Core Web Vitals are used by our ranking systems". There is **no single page experience signal**.
- Relevance wins: Google "always seeks to show the most relevant content, even if the page experience is sub-par".
- Other aspects Google weighs: HTTPS, mobile-friendliness, no intrusive interstitials, no excessive ads, and main content that is easy to tell apart from the rest.
- Treat CWV as a **tiebreaker plus a user and conversion win**, not a lever that beats relevance.

### 3.3 Field data vs lab data

- **CrUX** comes from real Chrome users who opted in. It is a 28-day rolling window, updated daily around 04:00 UTC. Page-level data exists only for URLs with enough traffic; otherwise Google falls back to origin level. Search Console's CWV report groups similar URLs.
- **Lighthouse and PSI lab data** is a single synthetic run. It measures TBT, not INP, so it is only a diagnostic. **Pass or fail is decided by field data.**

```bash
# CrUX API (page, phone). 150 QPM per project. Source: https://developer.chrome.com/docs/crux/api
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com/","formFactor":"PHONE",
       "metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift",
                  "experimental_time_to_first_byte","largest_contentful_paint_image_resource_load_delay"]}' \
 | jq '.record.metrics | map_values(.percentiles.p75)'
# Falls back: if 404 NOT_FOUND for url, query {"origin":"https://example.com"}.
# History (up to ~40 weekly points): POST .../v1/records:queryHistoryRecord  (endpoint name from memory — verify)

# PageSpeed Insights API v5 (lab + field). Source: https://developers.google.com/speed/docs/insights/v5/get-started (2025-08-28)
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fexample.com%2F&strategy=mobile&category=performance&category=seo&category=accessibility&category=best-practices&key=$PSI_KEY" \
 | jq '{field: .loadingExperience.metrics, origin: .originLoadingExperience.overall_category,
        perf: .lighthouseResult.categories.performance.score, seo: .lighthouseResult.categories.seo.score}'
```

PSI quotas (25k/day with a key) are **unverified**.

### 3.4 Practical fixes, ranked by typical impact

**LCP.** Source: https://web.dev/articles/optimize-lcp (2025-03-31). Break LCP into subparts: TTFB about 40%, resource load delay under 10%, load duration about 40%, render delay under 10%.

- Server-render the LCP element. The hero `<img>` must be in the HTML, not injected by JS or set as a CSS background.
- Use `fetchpriority="high"` on the LCP image. **Never** put `loading="lazy"` on it. Preload it only if it is discovered late, for example through CSS or JS.
- Use AVIF or WebP with a correctly sized `srcset`/`sizes`, served from a CDN, with long-lived immutable cache headers.
- Cut TTFB: edge caching of HTML (SSG/ISR), no redirect hops, and no cache-busting query parameters.
- Remove render-blocking resources: inline critical CSS, `defer` scripts, and no synchronous third-party scripts in `<head>`.

```html
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
<img src="/hero-1200.avif" srcset="/hero-800.avif 800w, /hero-1200.avif 1200w, /hero-1600.avif 1600w"
     sizes="(max-width: 768px) 100vw, 1200px" width="1200" height="630"
     fetchpriority="high" decoding="async" alt="Technician calibrating a CNC lathe in our Shah Alam workshop">
```

**INP.** Source: https://web.dev/articles/optimize-inp (2025-09-02). INP has three phases: input delay, processing, and presentation delay.

- Break up long tasks and yield to the main thread (`scheduler.yield()` where supported, otherwise `setTimeout`).
- Keep event handlers minimal. Defer non-visual work to after the next paint.
- Avoid layout thrashing.
- Reduce DOM size. Use `content-visibility: auto` for off-screen sections.
- Audit third-party scripts (tag managers, chat widgets, A/B testing). They are the most common INP killer on marketing sites (common practice, not a Google quote).

```js
async function onFilterClick(e) {
  updateSelectedChipUI(e.target);             // visual feedback first
  await (globalThis.scheduler?.yield?.() ?? new Promise(r => setTimeout(r, 0)));
  applyFiltersAndRerenderList();              // heavy work after paint
}
```

**CLS.** Source: https://web.dev/articles/optimize-cls (2025-02-07).

- Put `width`/`height` or `aspect-ratio` on all images, videos and iframes.
- Reserve space for ads, embeds and banners with `min-height`.
- Don't insert content above existing content unless the user asked for it.
- Fonts: `font-display: optional` (or `swap` with a metric-matched fallback using `size-adjust`, `ascent-override` and `descent-override`), and preload the critical WOFF2.
- Animate only `transform` and `opacity`.

**bfcache.** Source: https://web.dev/articles/bfcache (2026-07-02).

- Never use `unload`; use `pagehide`.
- Avoid `Cache-Control: no-store` on public pages. Use `no-cache` or `max-age=0` instead.
- Close WebSockets and IndexedDB connections on `pagehide`.
- Test in the DevTools Back/forward cache panel or with Lighthouse. The `NotRestoredReasons` API explains failures.
- The CrUX release notes (Mar 2025) credit better bfcache eligibility for web-wide LCP gains.

**Speculation rules.** Source: https://developer.chrome.com/docs/web-platform/prerender-pages (2026-01-23). These make next-page navigations near-instant in Chromium (Chrome and Edge 109+; Safari behind a flag; not Firefox).

- Exclude logout, cart-mutation and admin URLs.
- Analytics must handle `document.prerendering`.

```html
<script type="speculationrules">
{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/logout"}},
  {"not":{"href_matches":"/cart/*"}},{"not":{"selector_matches":"[rel~=nofollow]"}}]},"eagerness":"moderate"}]}
</script>
```

### 3.5 Mobile-first indexing

Source: https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing (updated 2025-12-10).

- Google indexes the **mobile** version. Content, structured data, title, meta description, robots meta and alt text must match the desktop version.
- Don't hide primary content behind interaction on mobile. Tabs and accordions are fine if the content is in the DOM.
- Resources must be crawlable, image and video URLs must be stable, and mobile pages must not rely on fragments.
- **Skill check:** fetch the page with the Googlebot Smartphone UA and diff it against desktop.

---

## 4. On-page

### 4.1 Title elements

Source: https://developers.google.com/search/docs/appearance/title-link (updated 2025-12-10).

- **Every page** needs a unique, descriptive, concise `<title>` in the page's language. Brand it once, with a delimiter, at the start or end. No keyword stuffing and no boilerplate.
- **Google may rewrite titles** using the `<title>`, the main visual title or `<h1>`, other headings, `og:title`, prominent text, anchor text, inbound link text, or `WebSite` structured data.
- **Rewrite triggers:**
  - half-empty titles (just the site name);
  - obsolete dates;
  - titles that don't match the content;
  - micro-boilerplate (for example "Page 3 of …" repeated across pages);
  - no clear main title (several equal-weight headings);
  - a language or script mismatch;
  - a redundant site name.
- **Length:** Google has no limit and truncates by pixel width. The common heuristic is about 50–60 characters / 600px (**practitioner heuristic, unverified**).
- **Skill rule:** make `<title>`, `<h1>` and `og:title` semantically consistent. This is the strongest defence against rewrites.

### 4.2 Meta descriptions and snippets

Source: https://developers.google.com/search/docs/appearance/snippet (updated 2026-04-20).

- Snippets come mainly from page content. The meta description is used when it describes the page more accurately.
- Write a unique description for each page, with specifics (price, author, date, specs). Programmatic generation is fine if the result stays page-specific. There is no length limit; practitioners aim for about 150–160 characters (**heuristic**).
- **"Read more" deep links (2026)** appear more often when the content is visible (not collapsed), the page does not jump scroll on load, and hash fragments survive History API calls.

### 4.3 Headings and semantic HTML

- Use one clear main heading (`<h1>`) that visually dominates. Order: "From Google Search perspective, it doesn't matter if you're using them out of order" (https://developers.google.com/search/docs/fundamentals/seo-starter-guide, 2025-12-10). A logical hierarchy still matters for accessibility and for how AI systems chunk passages (see §8).
- Use semantic landmarks (`<main>`, `<article>`, `<nav>`, `<header>`, `<footer>`). Google's AI guide asks for "semantic HTML when possible" (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, 2026-07-10).

### 4.4 URL structure

Source: https://developers.google.com/search/docs/crawling-indexing/url-structure (updated 2025-12-10).

- Use readable words in the audience's language, with **hyphens** between words. Use lowercase, because URLs are case-sensitive. Percent-encode non-ASCII characters.
- Use `=` and `&` for parameters. No session IDs. No fragments for content changes.
- Avoid additive filter parameters and endless calendar URLs.
- Keywords in the domain or path "have hardly any effect beyond appearing in breadcrumbs" (SEO Starter Guide).
- **Skill rule:** stable, short, lowercase, hyphenated paths. Redirect case and trailing-slash variants to one form.

### 4.5 Internal linking and site architecture

Source: https://developers.google.com/search/docs/crawling-indexing/links-crawlable (updated 2025-12-10).

- "Every page you care about should have a link from at least one other page on your site." Orphan pages are a failure.
- **Anchor text** should be descriptive and concise, not "click here" or "read more", and not keyword-stuffed. Give links surrounding context and don't chain links back to back.
- **rel values:** use `nofollow` only for untrusted links, `sponsored` for paid links and `ugc` for user content. Don't nofollow internal links.
- **Architecture:**
  - Keep money pages within about 3 clicks of the home page (**practitioner heuristic**).
  - Use a hub-and-spoke (pillar and cluster) structure: the hub links to every spoke, spokes link back to the hub and to sibling spokes where relevant.
  - Add BreadcrumbList markup plus visible breadcrumbs. Note that since Jan 2025 Google shows only the domain, not the breadcrumb path, in mobile results (https://developers.google.com/search/updates, 2025-01-22). Breadcrumbs still help internal linking and desktop display.
  - Use HTML footer and sitemap links sparingly.
- **Topical authority:** Google documents "topic authority" only for **news** (**from memory, 2023; unverified this session**). For general sites, the evidence-backed mechanism is site-level quality assessment (§1.2 "evaluate the whole site") plus internal linking that concentrates relevance. Build complete clusters instead of scattered one-off posts. Don't create "separate content for every possible variation" (AI guide), because that edges into scaled content abuse.

### 4.6 Image SEO

Source: https://developers.google.com/search/docs/appearance/google-images (updated 2026-03-02).

- Use `<img>` elements, not CSS backgrounds, for content images. Use `srcset` or `<picture>` with a fallback `src`.
- **Formats:** BMP, GIF, JPEG, PNG, WebP, SVG and **AVIF**.
- Write descriptive, contextual alt text without stuffing. Give files semantic names (`dalmatian-puppy.jpg`).
- Declare the preferred image with `og:image` or `primaryImageOfPage` (2026).
- Use image sitemaps for images that JS or a CDN would otherwise hide. The CDN domain must be verified if it differs from the site's.
- Keep image URLs stable. Always give `width` and `height` (CLS).
- Favicon: square, at least 8×8 and ideally 48×48 or larger. Supported formats: BMP, GIF, ICO, PNG, JPEG, PPM, TIFF (SVG is not listed in the fetched summary; **verify**). Declared with `<link rel="icon">` on the home page; one per hostname; crawlable by Googlebot and Googlebot-Image. Source: https://developers.google.com/search/docs/appearance/favicon-in-search (formats added 2026-08-28).

### 4.7 Video SEO

Source: https://developers.google.com/search/docs/appearance/video (updated 2025-12-18).

- A video is indexed only if it is **the main content of a watch page** and that page is itself indexed.
- Use `VideoObject` with a unique `name`, `description`, `thumbnailUrl` and `uploadDate`, plus `contentUrl` or `embedUrl`. `creator` is supported from 2026-09-24.
- Add key moments with `Clip` (manual timestamps) or `SeekToAction` (automatic). Mark livestreams with `BroadcastEvent`.
- Thumbnails must be at least 60×30. Thumbnail and video URLs must be stable and fetchable by Googlebot.
- Use video sitemaps (§2.9).

```json
{"@context":"https://schema.org","@type":"VideoObject","name":"How we install racking in 3 hours",
 "description":"Step-by-step installation of selective pallet racking at a Klang warehouse.",
 "thumbnailUrl":["https://example.com/v/racking-1x1.jpg","https://example.com/v/racking-16x9.jpg"],
 "uploadDate":"2026-08-14T09:00:00+08:00","duration":"PT4M12S",
 "contentUrl":"https://example.com/v/racking.mp4","embedUrl":"https://example.com/embed/racking",
 "hasPart":[{"@type":"Clip","name":"Marking the floor","startOffset":30,"endOffset":95,
             "url":"https://example.com/videos/racking?t=30"}]}
```

### 4.8 Site names and branding in the SERP

Source: https://developers.google.com/search/docs/appearance/site-names.

- Put `WebSite` JSON-LD on the **home page** of each domain or subdomain (subdirectories are not supported), with `name`, optional `alternateName` and `url`.
- Keep it consistent with the home page `<title>`, `og:site_name` and `<h1>`. This also feeds title-link generation (§4.1).

```json
{"@context":"https://schema.org","@type":"WebSite","name":"Sunlight Supplies","alternateName":["Sunlight","SSSB"],"url":"https://example.com/"}
```

---

## 5. International SEO, including Malaysia

### 5.1 hreflang rules

Source: https://developers.google.com/search/docs/specialty/international/localized-versions (updated 2026-09-21).

- **Three equivalent methods:** HTML `<link rel="alternate" hreflang>`, an HTTP `Link` header (for PDFs), or `<xhtml:link>` in a sitemap. Pick one and apply it consistently.
- **Rules:**
  - Every version lists **itself and all alternates**, and links must be **reciprocal**. Annotations without a return link may be ignored.
  - URLs must be fully qualified and canonical.
  - Language uses ISO 639-1; region uses ISO 3166-1 alpha-2.
  - A region alone is invalid. Use `en-GB`, not `UK`.
  - Script subtags follow ISO 15924, for example `zh-Hans` and `zh-Hant`.
  - `x-default` is the fallback or selector page.
- **Common errors:**
  - wrong codes (`en-UK`, `my` for Malay; `my` is actually Burmese);
  - missing return links;
  - hreflang pointing at redirected, non-canonical or noindexed URLs;
  - a canonical pointing across languages (for example the `ms` page canonicalised to the `en` page), which cancels the hreflang.

### 5.2 URL structure for international sites

Source: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites (updated 2025-12-10).

- **ccTLD:** the clearest geotarget, but costly and limited to one country.
- **Subdomain:** easy, but a weaker signal.
- **Subdirectory:** the least maintenance, with signals shared across the site.
- **URL parameters:** "Not recommended".
- The Search Console international targeting report no longer exists. Geo signals are the ccTLD, hreflang, local address, phone number, currency and language.
- **Don't auto-redirect by IP or Accept-Language.** Googlebot mostly crawls from the US and will never see the variants. Offer a visible language switcher instead.
- Google ignores code-level `lang` attributes when detecting language and uses the visible content. Still set `<html lang>` for accessibility and screen readers.

### 5.3 Malaysia specifics

Codes are from ISO/BCP 47 conventions; the Google source is §5.1.

- **Malay** is `ms`, so `ms-MY`. **Do not use `my`** (Burmese) and don't use `bm`.
- **English (Malaysia)** is `en-MY`, or plain `en` if the English pages also serve Singapore and elsewhere.
- **Chinese (Malaysia)** uses Simplified script: `zh-Hans-MY`, or `zh-Hans` if not region-specific. Google's docs show script subtags; `zh-MY` is also accepted, but the script is ambiguous (**verify** in testing).
- **Tamil** is `ta-MY`.
- Recommended structure for an MY business is subdirectories on `.my` or `.com.my`, or on a `.com` with hreflang:

```html
<link rel="alternate" hreflang="en-MY" href="https://example.com.my/en/servis-aircond/">
<link rel="alternate" hreflang="ms-MY" href="https://example.com.my/ms/servis-aircond/">
<link rel="alternate" hreflang="zh-Hans-MY" href="https://example.com.my/zh/servis-aircond/">
<link rel="alternate" hreflang="x-default" href="https://example.com.my/en/servis-aircond/">
```

- **Malaysians search in mixed language.** Queries blend English and Malay ("servis aircond murah shah alam"). Each language version should use the real mixed-register vocabulary people type: colloquial Malaysian Malay with English trade words, not textbook Bahasa baku or Indonesian phrasing. This is a practitioner observation that matches the user's own stored preference; it is **not** a Google statement.
- Machine-translated pages at scale with no review risk being treated as **scaled content abuse** (§1.4).
- Localise currency (RM/MYR), the phone format (+60), the address, and `LocalBusiness` structured data. Keep Google Business Profile consistent (see the local SEO researcher).
- Market: Google has about 93% share in MY (§0). Bing Webmaster Tools and IndexNow are still worth setting up because Bing grounds Copilot, and via partners feeds other AI assistants (see researcher 02).

---

## 6. Accessibility, SEO and agent-operability

- **Overlap:** alt text, descriptive link text, a heading hierarchy, `<html lang>`, semantic landmarks, visible labels, adequate tap targets and no intrusive interstitials help screen readers, Googlebot and AI agents alike. Google's AI guide explicitly recommends semantic HTML "for accessibility" (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, 2026-07-10).
- **Standards:**
  - WCAG 2.2 (W3C Recommendation, 2023-10-05) added 2.4.11 Focus Not Obscured (AA), 2.5.7 Dragging Movements (AA), 2.5.8 Target Size Minimum 24×24 (AA), 3.2.6 Consistent Help (A), 3.3.7 Redundant Entry (A), 3.3.8 Accessible Authentication (AA), and removed 4.1.1 Parsing. Source: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/.
  - The European Accessibility Act covers e-commerce with the harmonised standard EN 301 549, updated in 2026 per the Commission page (https://commission.europa.eu/…/european-accessibility-act_en). It applies from 2025-06-28 (**from the directive text, not re-verified this session**).
- **Agents are now real traffic:**
  - `Google-Agent` is a user-triggered fetcher that "navigates web and performs actions on user request" and generally ignores robots.txt (https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers, 2026-08-19).
  - At Google I/O 2026 (2026-05-19), AI Mode passed 1B monthly users and Google announced agentic booking and checkout (https://blog.google/products-and-platforms/products/search/search-io-2026/).
  - **WebMCP** (early preview, 2026-02-10) lets sites expose structured tools to agents through declarative HTML forms or an imperative JS API (https://developer.chrome.com/blog/webmcp-epp).
  - Lighthouse 13.x (v13.5.0, "Sep 18", mapped to Chrome 156 DevTools; the fetched page showed the year as 2024, but the Chrome-version mapping implies 2026, so **verify**) adds an **agentic-browsing / agent discovery** grouping with llms.txt, Agent Resource Discovery (`.well-known` ai-catalog) and WebMCP form-coverage audits (https://github.com/GoogleChrome/lighthouse/releases/tag/v13.5.0). The public README still lists only 4 categories.
- **Agent-operability checklist** (derived from the above; partly practitioner inference):
  - Real `<form>`, `<label for>`, `<button type>`, `autocomplete` tokens and native `<select>`.
  - Accessible names on every control.
  - No CAPTCHA on read-only flows.
  - Deterministic URLs for states such as search, filters and product variants.
  - No hover-only menus.
  - Critical actions reachable without drag gestures (WCAG 2.5.7).
  - Don't WAF-block verified Google fetchers.

---

## 7. Security and trust

- **HTTPS everywhere.** HTTPS is part of page experience (https://developers.google.com/search/docs/appearance/page-experience, 2026-09-22).
  - Redirect http to https in one 301/308 hop.
  - Make HTTPS URLs the canonicals, sitemap entries and hreflang targets.
  - No **mixed content** (http subresources on https pages). Check with `curl` plus grep, or the Lighthouse best-practices category.
- **HSTS.** Source: https://hstspreload.org/.
  - Ramp `max-age` from 300 to 604800 to 2592000 seconds, then to at least 31536000.
  - Preload requires `max-age` of at least 31536000, `includeSubDomains`, `preload`, a valid certificate, HTTPS on every subdomain, and the header also on redirect responses. "Inclusion in the preload list cannot easily be undone". **Do not auto-enable preload in the skill without the user's confirmation.**

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: upgrade-insecure-requests
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

- **Trust pages** (evidence for the "Who/How/Why" framework and the trust part of E-E-A-T, https://developers.google.com/search/docs/fundamentals/creating-helpful-content, 2025-12-10):
  - About page, with the real entity, people and history.
  - Contact page, with address, phone and email.
  - Privacy policy and terms. In Malaysia these must follow PDPA 2010 as amended in 2024 (**legal detail not verified here**).
  - Returns and shipping pages for e-commerce, backed by `MerchantReturnPolicy` and `ShippingService` structured data (Google docs 2025-06-11 and 2025-11-11 per the changelog).
  - Author pages with credentials for YMYL topics.
  - Business registration number in the footer (for example the SSM number in MY; practitioner convention).
  - `Organization` JSON-LD with `name`, `url`, `logo`, `sameAs`, `contactPoint` and `address`.
- **Hacked content and malware** are spam (§1.4). Monitor the Search Console Security Issues report and keep the CMS and plugins patched.
- **Reviews:** a new guideline on 2026-07-24 targets fake and incentivised reviews in review snippets (changelog). Never mark up reviews the business wrote itself or paid for.

---

## 8. Content-structure notes that are also classic SEO

This section overlaps with other researchers; only the classic-SEO angle is covered here.

- Google says you **don't** need to chunk or rewrite content for AI (§0). Well-organised pages ("well written and easy to follow") are still what it recommends: descriptive headings, answer-first paragraphs, tables for comparisons, and original data, images and video.
- **Duplicate content** is not penalised: "inefficient, but it's not something that will cause a manual action" (SEO Starter Guide). It dilutes signals and crawl, so consolidate it (§2.3). Bing (2025-12-19) says duplicate content also hurts AI search visibility (https://blogs.bing.com/webmaster/, post title only fetched).
- **Content length:** "there's no magical word count target" (SEO Starter Guide).

---

## 9. Search Console and Bing Webmaster Tools

### 9.1 Google Search Console setup

- Use a **Domain property** (DNS TXT) so every protocol and subdomain is covered. Add URL-prefix properties for sections if needed.
- Submit the sitemap index. Link GA4. Add users by role.
- **New in 2025–2026** (https://developers.google.com/search/blog, listing fetched 2026-09-26):
  - Query groups in Insights (Oct 2025).
  - **Branded queries filter** and custom **annotations** (Nov 2025).
  - Weekly and monthly views, social channels, and AI-powered report configuration (Dec 2025).
  - **Generative AI performance report** (Jun 2026) for AI Overviews and AI Mode. Its exact metrics are **unverified**: the post body fetched thinly.
  - AI Mode traffic has counted in Performance totals since 2025-06-16 (changelog), and AI-feature traffic is included under "Web" (https://developers.google.com/search/docs/appearance/ai-features).

### 9.2 Reports to check, in order

1. **Manual actions and Security issues.** Anything listed here is a blocker.
2. **Page indexing** (https://support.google.com/webmasters/answer/7440203). These reasons are actionable:
   - Server error (5xx), Redirect error, Blocked by robots.txt, Excluded by noindex, **Soft 404**, 401/403/other 4xx.
   - **Duplicate, Google chose different canonical**, which means fix the signals.
   - **Crawled/Discovered – currently not indexed**, which means quality or internal-link demand. Not directly fixable, but a large volume here signals quality or crawl-budget problems.
   - **"Indexed, though blocked by robots.txt"**, which means you should switch to noindex.
3. **Sitemaps:** status, discovered URLs, and indexed vs submitted per sitemap (split sitemaps by template to diagnose).
4. **Core Web Vitals:** mobile and desktop URL groups.
5. **HTTPS report**, **Performance** (queries, pages, countries, devices; use the branded filter), the **Generative AI performance** report, **Links** (top linked pages and internal link counts, to find orphans), **Enhancements** (structured-data rich result reports), and **Crawl stats** (Settings: host status, response codes, file types, Googlebot type, average response time).
6. **URL Inspection** for key templates: coverage, Google-selected vs user canonical, crawled-as (smartphone), rendered HTML and screenshot, detected structured data. "Test live URL" checks the live page; "Request indexing" is rate-limited.

**URL Inspection API.** Source: https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect. Limits are **2,000 queries per day and 600 per minute per property** (https://developers.google.com/webmaster-tools/limits). It returns only the indexed version and cannot test a live URL.

```bash
curl -s -X POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" -H 'Content-Type: application/json' \
  -d '{"inspectionUrl":"https://example.com/page","siteUrl":"sc-domain:example.com"}' \
| jq '.inspectionResult.indexStatusResult | {verdict,coverageState,robotsTxtState,indexingState,pageFetchState,googleCanonical,userCanonical,crawledAs,lastCrawlTime}'
```

### 9.3 Bing Webmaster Tools

- Import directly from Search Console to set it up quickly (common practice; **unverified this session**). Submit sitemaps and enable IndexNow (§2.10).
- **AI Performance report**, public preview since 2026-02-10 (https://blogs.bing.com/webmaster/, title and date only). It shows the site's presence in Copilot and Bing AI answers. Details are **unverified**.
- Also check URL Inspection, Site Explorer, SEO Reports, the robots.txt tester and Crawl Control.
- Bing emphasises accurate `lastmod` for recrawl in AI search (2025-07-31 blog).

---

## 10. Prioritised technical SEO audit checklist (automatable)

Legend: **P0 = critical** (blocks indexing; fix before anything else), **P1 = high**, **P2 = medium**, **P3 = low**. Each row has a pass condition and a check.

### P0 — Critical

| # | Check | Pass criterion | How to check |
|---|---|---|---|
| 0.1 | robots.txt reachable | 200 (or 404), never 5xx, under 500 KiB | `curl -s -o /dev/null -w '%{http_code} %{size_download}\n' https://$H/robots.txt` |
| 0.2 | Not blocking the site or rendering assets | No `Disallow: /` for `*` or Googlebot. CSS and JS paths allowed | Parse robots.txt. Test key URLs with a robots parser (`python -c "import urllib.robotparser…"`; Google's own parser is `github.com/google/robotstxt`) |
| 0.3 | Key pages return 200 | Home, top templates and money pages return 200 and are not soft 404s | `curl -s -o /dev/null -w '%{http_code}\n' -A 'Mozilla/5.0 (Linux; Android 10; K) … Googlebot/2.1' URL` |
| 0.4 | No accidental noindex | No `noindex` in meta (head **or body**, since Mar 2026) or in X-Robots-Tag on indexable pages | `curl -sI URL \| grep -i x-robots-tag`; `curl -s URL \| grep -io '<meta[^>]*robots[^>]*>'` |
| 0.5 | Canonical correct | One absolute, self-referencing (or intentional) canonical in `<head>` in the **raw HTML**, pointing to a 200 URL | grep the raw HTML. Compare with the rendered DOM (Playwright). URL Inspection shows Google's choice |
| 0.6 | HTTPS and a single host | http→https and alt-host→primary in **one** 301/308 hop. Valid certificate | `curl -sIL -o /dev/null -w '%{num_redirects} %{url_effective}\n' http://$H/` (expect 1) |
| 0.7 | Content in server HTML | Main content, title, H1 and links present without JS | `curl -s URL \| sed 's/<[^>]*>//g' \| wc -w`, compared with the rendered word count |
| 0.8 | HTML under 2MB | Uncompressed HTML and each critical JS/CSS resource under 2MB | `curl -s --compressed URL \| wc -c` |
| 0.9 | No manual action or security issue | GSC shows none | GSC UI (no public API for manual actions) |
| 0.10 | Staging not indexable | Staging is behind auth or has an X-Robots-Tag noindex. Production does **not** carry staging's noindex | curl both hosts |
| 0.11 | No spam-policy patterns | No cloaking (UA diff), no hidden text, no back-button hijacking, no doorway or scaled pages | Diff Googlebot UA vs browser UA responses. grep JS for `history.pushState` on load and `popstate` traps |

### P1 — High

| # | Check | Pass criterion | How to check |
|---|---|---|---|
| 1.1 | XML sitemap valid | Index plus children, each ≤50k URLs and ≤50MB, UTF-8. Every URL 200, canonical and indexable. Referenced in robots.txt. Submitted in GSC and Bing | Script: fetch the sitemap, then `HEAD` each `loc`, check status, canonical and robots |
| 1.2 | lastmod honest | lastmod changes only when content changes, and is not every URL's build time | Count distinct lastmod values. If more than 90% are identical, fail |
| 1.3 | Redirect hygiene | No chains (at most 1 hop from internal links), no loops, no internal links to 3xx/4xx | Crawler (§11). Every internal link target returns 200 |
| 1.4 | Unique titles and H1s | Every indexable page has a unique `<title>` (non-empty and not just the brand), one visible H1, and title≈H1≈og:title | Crawler export: duplicate and missing counts |
| 1.5 | Core Web Vitals field data | p75 LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 on phone, at URL or origin level | CrUX API (§3.3), GSC CWV report |
| 1.6 | Mobile parity | Mobile-UA HTML contains the same main content, structured data, meta and links as desktop | Fetch with both UAs and diff |
| 1.7 | Internal linking | No orphan indexable pages. Money pages ≤3 clicks deep. Links are `<a href>` | Crawler depth report, cross-checked against the sitemap list (in the sitemap but not found by the crawl = orphan) |
| 1.8 | hreflang (if multilingual) | Valid codes, self plus reciprocal references, targets are 200 and canonical, x-default present | Crawler hreflang report, or a script (§11) |
| 1.9 | Soft 404 and error handling | Unknown URLs return a real 404 (not 200, not a redirect to home). Empty facet combinations return 404 | `curl -s -o /dev/null -w '%{http_code}' https://$H/this-should-not-exist-$RANDOM` must be 404 or 410 |
| 1.10 | Faceted and parameter control | Infinite parameter spaces are disallowed or canonicalised. Crawl stats aren't dominated by parameter URLs | GSC Crawl stats; log analysis (§11) |
| 1.11 | JS rendering sanity | Rendered DOM contains no "Loading…" placeholders and no client-only critical content | Playwright render + GSC "View crawled page" |
| 1.12 | Page indexing health | Indexed/submitted ≥ ~90% for the main-content sitemaps. No growth in 5xx or soft 404 | GSC Page indexing per sitemap |

### P2 — Medium

| # | Check | Pass criterion | How to check |
|---|---|---|---|
| 2.1 | LCP image best practice | LCP `<img>` in the HTML with `fetchpriority=high`, not lazy, AVIF or WebP, with correct `sizes` | Lighthouse `largest-contentful-paint-element` / LCP insights |
| 2.2 | CLS guards | All img, video and iframe elements have dimensions. Fonts metric-matched | Lighthouse `unsized-images` (and `layout-shifts` insights in v13) |
| 2.3 | bfcache eligible | No `unload`. No `Cache-Control: no-store` on public HTML | Lighthouse bfcache audit; `curl -sI URL \| grep -i cache-control` |
| 2.4 | Meta descriptions | Present, unique and specific on key templates | Crawler |
| 2.5 | Image SEO | Meaningful `alt` on content images. Semantic filenames. `og:image` set | Crawler, plus Lighthouse `image-alt` |
| 2.6 | Structured data valid | Organization/WebSite on home, BreadcrumbList, plus Product/Article/LocalBusiness/VideoObject as relevant. No errors | Rich Results Test, `validator.schema.org`, GSC Enhancements (details in the schema researcher's file) |
| 2.7 | Pagination | Sequential `<a href>` links, self-canonicals, no `#` page numbers | Crawler |
| 2.8 | IndexNow wired | Key file 200. Publish, update and delete hooks POST to api.indexnow.org and get 200/202 | curl the key file; check deploy logs |
| 2.9 | Security headers | HSTS present, no mixed content, TLS ≥1.2 | `curl -sI`; Lighthouse best-practices; `testssl.sh` |
| 2.10 | Trust pages | About, Contact, Privacy and Terms each linked site-wide and returning 200. Organization JSON-LD with a logo and sameAs | Crawler plus grep |
| 2.11 | Accessibility basics | Lighthouse accessibility ≥ 90. `<html lang>` set. Link text descriptive. Tap targets ≥ 24px | `lighthouse --only-categories=accessibility` / `axe-core` CLI |
| 2.12 | Compression and caching | Brotli or gzip on HTML, CSS and JS. Immutable caching on fingerprinted assets. Conditional requests (ETag/Last-Modified) supported | `curl -sI -H 'Accept-Encoding: br,gzip' URL`; `curl -sI -H 'If-None-Match: "<etag>"' URL` gives 304 |

### P3 — Low

| # | Check | Pass criterion | How to check |
|---|---|---|---|
| 3.1 | URL style | Lowercase, hyphenated, no session IDs, trailing-slash consistent (variants 301 to the canonical) | Crawler URL report |
| 3.2 | Speculation rules | Present for likely next pages. Excludes state-changing URLs | grep for `type="speculationrules"` |
| 3.3 | Favicon and site name | `<link rel=icon>` crawlable and square. WebSite JSON-LD `name` matches the brand | curl plus grep |
| 3.4 | Video indexing | Watch pages with VideoObject, key moments, video sitemap | GSC Video indexing report |
| 3.5 | Anchor-text quality | No "click here" or "read more" anchors (Lighthouse `link-text`) | Lighthouse SEO |
| 3.6 | llms.txt (optional) | Present if the user wants it for non-Google agents. No Google effect either way | curl |
| 3.7 | Bing parity | Bing Webmaster Tools verified, sitemap submitted, no Bing-specific crawl errors | BWT UI |

---

## 11. Tooling: commands and open-source options

### 11.1 Quick curl battery (single URL)

```bash
URL="https://example.com/some-page/"; H=$(echo "$URL" | awk -F/ '{print $3}')
UA_M='Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
# status, redirects, final URL, size, TTFB
curl -s -A "$UA_M" -L -o /tmp/p.html -w 'code=%{http_code} redirs=%{num_redirects} final=%{url_effective} bytes=%{size_download} ttfb=%{time_starttransfer}\n' "$URL"
# headers that matter
curl -sI -A "$UA_M" "$URL" | grep -iE '^(HTTP|x-robots-tag|link|cache-control|content-encoding|strict-transport|vary|location)'
# head signals from RAW html (pre-JS)
grep -ioE '<title>[^<]*</title>|<meta[^>]+name="(robots|googlebot|description)"[^>]*>|<link[^>]+rel="(canonical|alternate)"[^>]*>|<h1[^>]*>' /tmp/p.html
# JSON-LD blocks
grep -o '<script type="application/ld+json">[^<]*' /tmp/p.html | sed 's/<script type="application\/ld+json">//' | jq -c '.["@type"]' 2>/dev/null
# robots.txt + sitemap
curl -s "https://$H/robots.txt" | grep -iE '^(user-agent|disallow|allow|sitemap)'
# soft-404 probe
curl -s -o /dev/null -w '%{http_code}\n' "https://$H/zz-not-a-page-$RANDOM"
```

### 11.2 Sitemap validator (Node, no deps beyond fetch)

```js
// node validate-sitemap.mjs https://example.com/sitemap_index.xml
const root = process.argv[2]; const seen = []; const bad = [];
const locs = x => [...x.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map(m => m[1]);
async function walk(u){ const x = await (await fetch(u)).text();
  if (x.includes('<sitemapindex')) for (const s of locs(x)) await walk(s); else seen.push(...locs(x)); }
await walk(root);
for (const u of seen.slice(0, 2000)) {             // sample; raise for full runs
  const r = await fetch(u, { redirect: 'manual' }); const h = r.status === 200 ? await r.text() : '';
  const canon = h.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)/i)?.[1];
  const noidx = /<meta[^>]+robots[^>]+noindex/i.test(h) || /noindex/i.test(r.headers.get('x-robots-tag') || '');
  if (r.status !== 200 || noidx || (canon && canon !== u)) bad.push({ u, s: r.status, canon, noidx });
}
console.log(`${seen.length} URLs, ${bad.length} failing`); console.table(bad.slice(0, 50));
```

### 11.3 Lighthouse and Unlighthouse

```bash
npx lighthouse https://example.com/ --only-categories=performance,seo,accessibility,best-practices \
  --form-factor=mobile --output=json --output-path=./lh.json --chrome-flags="--headless=new"
jq '.categories | map_values(.score)' lh.json
npx unlighthouse --site https://example.com   # whole-site Lighthouse, Node ≥22.18
```

- **Lighthouse** needs Node 22+ (https://github.com/GoogleChrome/lighthouse/blob/main/readme.md). v13 replaced many legacy performance audits with "insights" (release notes).
- **The SEO category is shallow.** It checks meta description, link text, hreflang, canonical, status code, robots.txt validity, plugins and tap targets (https://developer.chrome.com/docs/lighthouse/seo/, doc dated 2019, likely stale). It cannot stand in for a crawl.
- **Unlighthouse:** https://github.com/harlan-zw/unlighthouse.

### 11.4 Crawlers (alternatives to Screaming Frog)

| Tool | Type | Notes |
|---|---|---|
| **SEOnaut** (github.com/StJudeWasHere/seonaut) | OSS, Go + MySQL, Docker | Broken links, redirects, duplicate or missing meta, heading order, severity levels. MIT. `docker compose up`, then :9000 |
| **Unlighthouse** | OSS, Node | Lighthouse on every page |
| Custom **Playwright** or **Crawlee** crawler | OSS | Best for JS sites: store raw HTML and rendered DOM per URL, then diff |
| `linkinator`, `lychee` | OSS CLI | Broken-link checks in CI (tool names from memory; **verify versions**) |
| Screaming Frog SEO Spider | Commercial, free up to 500 URLs (**unverified limit**) | The industry standard. JS rendering, custom extraction, CrUX/PSI/GSC API integration |
| Sitebulb, JetOctopus, Lumar | Commercial | Log analysis and large-site crawling |

### 11.5 Log-file analysis (for crawl budget)

```bash
# Googlebot hits by status and top paths (verify IPs separately, §2.11)
grep -i 'googlebot' access.log | awk '{print $9}' | sort | uniq -c | sort -rn
grep -i 'googlebot' access.log | awk '{print $7}' | sed 's/?.*//' | sort | uniq -c | sort -rn | head -50
grep -i 'googlebot' access.log | awk '{print $7}' | grep -c '?'   # parameter crawl share
```

### 11.6 hreflang reciprocity script (sketch)

```js
// For each URL: collect {hreflang: href}; assert self-reference, reciprocal return, 200 targets, valid codes.
const valid = /^(x-default|[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?)$/; // e.g. ms-MY, zh-Hans-MY
```

---

## 12. Myths and anti-patterns the skill must NOT recommend

Each item is backed by a Google source.

- Meta keywords: "Google Search doesn't use the keywords meta tag" (SEO Starter Guide, 2025-12-10).
- Word-count targets, keyword density, or exact-match domains (same source).
- `<priority>` and `<changefreq>` in sitemaps (ignored; build-sitemap doc 2026-07-08).
- `rel=next/prev` as a Google signal (pagination doc 2025-12-10).
- `crawl-delay` for Google (robots.txt doc 2026-08-31).
- Canonicalising paginated pages to page 1. Using noindex for canonicalisation. Using robots.txt to deindex.
- JS-injected noindex removal, or JS-changed canonicals.
- llms.txt, "AI text files" or special markup as a Google ranking or AI Overviews lever (AI guide mythbusting, 2026-06-15).
- Chunking or rewriting content "for AI", or buying inauthentic "mentions" (same guide).
- Third-party authority scores (DA/DR/AS) as Google metrics (third-party SEO doc, 2026-06-05).
- FAQ rich results as a tactic (removed June 2026).
- Scaled programmatic or AI pages, unreviewed machine translation, expired-domain redirects, or renting a subfolder to third parties (spam policies 2026-08-28).
- Back-button interstitials, "you may also like" history traps (policy enforced from 2026-06-15).
- Click manipulation or CTR bots (machine-generated traffic spam), even if the leak shows clicks matter.

---

## 13. Source index (URL: date as observed)

**Google Search Central (primary)**

- Search Status Dashboard, ranking history: https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history (fetched 2026-09-26)
- Documentation changelog: https://developers.google.com/search/updates (fetched 2026-09-26)
- Core updates: https://developers.google.com/search/docs/appearance/core-updates (2025-12-10)
- Spam policies: https://developers.google.com/search/docs/essentials/spam-policies (2026-08-28)
- March 2024 core update and spam policies: https://developers.google.com/search/blog/2024/03/core-update-spam-policies (2024-03)
- Back button hijacking: https://developers.google.com/search/blog/2026/04/back-button-hijacking (2026-04-13)
- Site reputation policy update (EEA): https://developers.google.com/search/blog/2026/08/update-site-reputation-policy (2026-08; body not fetched)
- Generative AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide (2026-07-10)
- AI features: https://developers.google.com/search/docs/appearance/ai-features (2025-12-10)
- Third-party SEO tools: https://developers.google.com/search/docs/fundamentals/third-party-seo (2026-06-05)
- Helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content (2025-12-10)
- SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide (2025-12-10)
- Technical requirements: https://developers.google.com/search/docs/essentials/technical (2025-12-18)
- robots.txt: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt (2026-08-31)
- Robots meta: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag (2026-03-24)
- Block indexing: https://developers.google.com/search/docs/crawling-indexing/block-indexing (2025-12-10)
- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (2026-07-10)
- Redirects: https://developers.google.com/search/docs/crawling-indexing/301-redirects (2026-04-14)
- Site moves: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes (2026-08-20)
- HTTP and network errors: https://developers.google.com/search/docs/crawling-indexing/http-network-errors (2026-02-04)
- Crawl budget: https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget (2026-07-22)
- Faceted navigation: https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation (2025-12-18)
- Pagination: https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading (2025-12-10)
- JavaScript SEO: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics (2026-03-04)
- Googlebot (2MB limit): https://developers.google.com/search/docs/crawling-indexing/googlebot (2026-02-03)
- Crawlers overview: https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers (2026-06-12)
- User-triggered fetchers (Google-Agent): https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers (2026-08-19)
- Verifying Googlebot: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot (2026-03-20)
- Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap (2026-07-08)
- Image sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps (2025-12-10)
- Video sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps (2026-05-20)
- News sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap (2025-12-10)
- Page experience: https://developers.google.com/search/docs/appearance/page-experience (2026-09-22)
- Mobile-first indexing: https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing (2025-12-10)
- Title links: https://developers.google.com/search/docs/appearance/title-link (2025-12-10)
- Snippets: https://developers.google.com/search/docs/appearance/snippet (2026-04-20)
- Links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable (2025-12-10)
- URL structure: https://developers.google.com/search/docs/crawling-indexing/url-structure (2025-12-10)
- Images: https://developers.google.com/search/docs/appearance/google-images (2026-03-02)
- Video: https://developers.google.com/search/docs/appearance/video (2025-12-18)
- Favicon: https://developers.google.com/search/docs/appearance/favicon-in-search (formats updated 2026-08-28)
- Site names: https://developers.google.com/search/docs/appearance/site-names
- hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions (2026-09-21)
- Multi-regional sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites (2025-12-10)
- Page indexing report: https://support.google.com/webmasters/answer/7440203
- URL Inspection API: https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect; limits: https://developers.google.com/webmaster-tools/limits
- Search Central blog index (GSC features 2025–26, Gen AI report): https://developers.google.com/search/blog; https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports (2026-06)
- Google I/O 2026 Search: https://blog.google/products-and-platforms/products/search/search-io-2026/ (2026-05-19)

**Chrome, web.dev and W3C**

- Web Vitals: https://web.dev/articles/vitals (2024-10-31); INP launch: https://web.dev/blog/inp-cwv-march-12 (2024)
- Optimize LCP: https://web.dev/articles/optimize-lcp (2025-03-31)
- Optimize INP: https://web.dev/articles/optimize-inp (2025-09-02)
- Optimize CLS: https://web.dev/articles/optimize-cls (2025-02-07)
- bfcache: https://web.dev/articles/bfcache (2026-07-02)
- CrUX release notes: https://developer.chrome.com/docs/crux/release-notes (through the Aug 2026 dataset, released 2026-09-08)
- CrUX API: https://developer.chrome.com/docs/crux/api
- PSI API: https://developers.google.com/speed/docs/insights/v5/get-started (2025-08-28)
- Speculation rules: https://developer.chrome.com/docs/web-platform/prerender-pages (2026-01-23)
- Soft navigations: https://developer.chrome.com/blog/final-soft-navigations-origin-trial (2026-04-20)
- WebMCP: https://developer.chrome.com/blog/webmcp-epp (2026-02-10)
- Lighthouse: https://github.com/GoogleChrome/lighthouse/releases/tag/v13.5.0 (Sep 18; year to verify) and https://github.com/GoogleChrome/lighthouse/blob/main/readme.md
- Lighthouse SEO audits: https://developer.chrome.com/docs/lighthouse/seo/ (2019, stale)
- WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ (Rec 2023-10-05)
- HSTS preload: https://hstspreload.org/

**Bing and IndexNow**

- IndexNow docs: https://www.indexnow.org/documentation; engines: https://www.indexnow.org/searchengines.json (fetched 2026-09-26)
- Bing IndexNow: https://www.bing.com/indexnow/getstarted
- Bing Webmaster blog index: https://blogs.bing.com/webmaster/ (AI Performance report 2026-02-10; data-nosnippet 2025-10-15; duplicate content and AI 2025-12-19)
- Bing sitemaps in AI search: https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search (2025-07-31)

**Secondary sources (lower confidence)**

- SEL, September 2026 spam update: https://searchengineland.com/google-releases-september-2026-spam-update-491267 (2026-09-24)
- SER, May 2026 core update done: https://www.seroundtable.com/google-may-2026-core-update-done-41435.html
- SER, site reputation abuse in the EEA: https://www.seroundtable.com/google-site-reputation-policy-eea-41968.html; https://ppc.land/google-drops-parasite-seo-penalties-in-europe-under-commission-mandate/
- SparkToro, API leak: https://sparktoro.com/blog/an-anonymous-source-shared-thousands-of-leaked-google-search-api-documents-with-me-everyone-in-seo-should-see-them/ (2024-05-27)
- Hobo, leak and NavBoost: https://www.hobo-web.co.uk/the-google-content-warehouse-leak-2024/ ; https://www.hobo-web.co.uk/navboost-how-google-uses-large-scale-user-interaction-data-to-rank-websites/
- Kopp, DOJ and the leak: https://www.kopp-online-marketing.com/what-we-can-learn-from-doj-trial-and-api-leak-for-seo
- StatCounter Malaysia: https://gs.statcounter.com/search-engine-market-share/all/malaysia (Aug 2026)
- Unverified INP-methodology claim: https://monstermegs.com/blog/core-web-vitals-update/
- SEOnaut: https://github.com/StJudeWasHere/seonaut ; Unlighthouse: https://github.com/harlan-zw/unlighthouse
