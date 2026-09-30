# SEO foundations — the layer AI search stands on

Google: generative AI features are "rooted in our core Search ranking and quality systems".
A page that can't be crawled, rendered, canonicalised, indexed and snippeted can't be cited
by anything grounded on Google or Bing. Full detail, update timeline, commands and sources:
`research/08-seo-foundations.md`.

---

## 1. Ground truth (2026)

- Minimum technical eligibility: Googlebot not blocked · HTTP 200 · indexable text that
  complies with spam policies.
- Update context: core updates 2025-03, 2025-06, 2025-12, 2026-03-27, 2026-05-21; spam updates
  2026-03, 06, 08 and 09-24 (rolling out). Helpful content is part of core ranking since
  March 2024. Smaller core updates ship continuously, unannounced.
- Diagnosing a drop: wait for rollout end + 1 week, compare before/after in GSC by search
  type; small moves (2→4) need nothing, big ones (4→29) need a whole-site quality review;
  recovery can take months.
- Spam policies to respect (updated 2026-08-28): cloaking, doorways, expired-domain abuse,
  hacked content, hidden text/links, keyword stuffing, link spam, machine-generated traffic,
  malicious practices incl. **back-button hijacking** (enforced from 2026-06-15: never
  `history.pushState` fake entries on load or trap `popstate`), misleading functionality,
  **scaled content abuse** (AI, human or hybrid), scraping, **site reputation abuse**
  (no longer affects searchers inside the EEA since 2026-08-30; full effect in Malaysia),
  sneaky redirects, thin affiliation, UGC spam — and **attempts to manipulate generative AI
  responses** (added 2026-05-15).
- The 2024 API leak / DOJ trial: NavBoost uses ~13 months of click data; site-level quality
  spills over. Takeaways: titles/snippets that set accurate expectations and content that ends
  the search journey; prune or improve thin sections site-wide. Never manipulate clicks.
- Malaysia: Google ~93% share, Bing ~4.4% — Bing matters because it grounds Copilot and feeds
  ChatGPT, not for its own traffic.

## 2. Crawling and indexing

- **robots.txt** — see `technical-access.md` §2. Never block CSS/JS needed for rendering.
- **noindex vs Disallow**: keep out of the index → `noindex`, left crawlable; save crawl on
  infinite spaces → Disallow; consolidate duplicates → 301/308 or canonical; urgent removal →
  GSC Removals + noindex/404/410. Conflicts: the more restrictive rule wins. Robots meta is
  honoured outside `<head>` too (scan the body for stray `noindex` from widgets).
- **Canonicals**: absolute, self-referencing, in `<head>` of the server HTML, one per page;
  internal links, sitemap and hreflang all point at canonicals; never robots.txt or noindex to
  choose between duplicates; never JS-changed canonicals; don't canonicalise page 2+ to page 1.
  Check GSC "Duplicate, Google chose different canonical".
- **Redirects**: 301/308 server-side, single hop (host + protocol + slash normalisation
  collapsed into one), kept ≥1 year; Googlebot follows up to 10 hops, keep <3. Change of
  Address for every verified variant on domain moves.
- **Status codes**: 404/410 remove; 401/403 = unavailable; 5xx/429 throttle and eventually
  drop; a 200 "not found" is a soft 404. SPA unknown routes → real 404 or noindex.
- **Crawl budget** (sites >1M pages or >10k daily-changing): consolidate duplicates, disallow
  infinite spaces, kill soft 404s and chains, honest lastmod, fast responses. Faceted nav:
  disallow or fragment non-indexable facets; indexable facets use `&`, fixed parameter order,
  404 for empty combinations. Index bloat: crawlable indexable URLs vs GSC indexed vs pages
  you actually want ranking.
- **Pagination / infinite scroll**: `<a href>` to each page, self-canonicals, `?page=N`
  fallbacks for infinite scroll, no `#` page numbers. rel=next/prev is ignored by Google.
- **JavaScript SEO**: critical content + all head tags in server HTML; `<a href>` links; History
  API routing; fingerprinted assets; no noindex-then-JS-remove; lazy-load only below the fold;
  dynamic rendering is a workaround. **2 MB cap** per HTML/JS/CSS file (Feb 2026).
- **Sitemaps**: ≤50k URLs / 50 MB per file; only 200 canonical indexable URLs; honest
  `lastmod` (real content change, full ISO 8601); priority/changefreq ignored; image
  (`image:loc` only), video and news (last 2 days, ≤1,000) sitemaps where relevant.
- **IndexNow** for Bing & co (not Google) from publish/update/delete hooks.
- **Verify crawlers** by reverse+forward DNS or the published JSON ranges; don't WAF-block
  Google's user-triggered fetchers (incl. Google-Agent) if you want to be agent-operable.

## 3. Core Web Vitals and page experience

Thresholds unchanged: **LCP ≤2.5 s · INP ≤200 ms · CLS ≤0.1** at p75, mobile and desktop
separately. ~56% of origins pass all three (Aug 2026). CWV are used in ranking but relevance
wins — treat them as a tiebreaker and a conversion win. Field data (CrUX, 28-day window)
decides; Lighthouse is diagnosis only (measures TBT, not INP). SPA soft navigations don't
count in CrUX yet.

- **LCP**: server-render the LCP element as `<img>` (not CSS background, not JS-injected);
  `fetchpriority="high"`, never `loading="lazy"` on it; AVIF/WebP with correct
  `srcset`/`sizes`; CDN + immutable caching; cut TTFB (edge-cached SSG/ISR, no redirect hops);
  inline critical CSS, `defer` scripts, no sync third-party scripts in `<head>`.
- **INP**: break long tasks and yield (`scheduler.yield()` fallback `setTimeout`); visual
  feedback first, heavy work after paint; shrink DOM; `content-visibility:auto`; audit
  third-party scripts (tag managers, chat widgets, A/B tools).
- **CLS**: width/height or aspect-ratio on media; reserve space for embeds/ads/banners; no
  content inserted above; `font-display` with metric-matched fallbacks; animate transform/
  opacity only.
- **bfcache**: no `unload` (use `pagehide`); no `Cache-Control: no-store` on public HTML.
- **Speculation rules** for likely next pages (exclude logout/cart/admin).
- **Mobile-first**: mobile HTML must carry the same content, structured data, meta, links.

Commands (CrUX API, PSI API, Lighthouse, Unlighthouse): research/08-seo-foundations.md §3.3 and §11.

## 4. On-page

- **Title**: unique, descriptive, brand once; title ≈ H1 ≈ og:title (Google rewrites when
  titles are half-empty, stale-dated, mismatched, boilerplate or with no clear main heading).
  ~50–60 characters is a heuristic, not a rule.
- **Meta description**: unique, specific (price, author, date, specs).
- **Headings**: one clear H1; logical hierarchy (Google doesn't care about order; extraction
  and accessibility do). Semantic landmarks.
- **URLs**: readable words, hyphens, lowercase, no session IDs, no fragments for content,
  consistent trailing slash with 301s for the other form.
- **Internal linking**: every page you care about linked from at least one other page (no
  orphans); descriptive anchors (not "click here"); money pages ≤3 clicks deep; hub ↔ spokes ↔
  siblings; visible breadcrumbs + BreadcrumbList; never nofollow internal links.
- **Images**: `<img>` with `srcset`, descriptive alt and filenames, `og:image` set, image
  sitemaps for CDN-hosted images, width/height.
- **Video**: indexed only as the main content of an indexed watch page; VideoObject + key
  moments; stable thumbnail/content URLs.
- **Site name**: WebSite JSON-LD on the home page, consistent with title/og:site_name/H1.
- **Favicon**: square, ≥48×48 ideal, crawlable, `<link rel="icon">` on the home page.

## 5. International

hreflang: one method (HTML, HTTP header or sitemap), self + reciprocal, fully qualified
canonical 200 targets, ISO codes, `x-default`. Errors: `en-UK`, **`my` (Burmese) for Malay**,
missing return links, targets redirected/noindexed, cross-language canonicals. Structure:
subdirectories (least maintenance) > subdomains > parameters (not recommended); ccTLD is the
strongest geo signal. **Never auto-redirect by IP or Accept-Language** — Googlebot crawls from
the US; offer a visible switcher. Malaysia: `ms-MY`, `en-MY`, `zh-Hans-MY`, `ta-MY`; RM
currency, +60 phones, local address; mixed-language queries are normal ("servis aircond murah
shah alam").

## 6. Security and trust

One-hop http→https; HSTS (ramp max-age; **never enable preload without the owner's explicit
yes** — it can't easily be undone); no mixed content; `X-Content-Type-Options: nosniff`;
`Referrer-Policy: strict-origin-when-cross-origin`. Trust pages linked site-wide: About,
Contact (address, phone, email), Privacy (PDPA in MY), Terms, returns/shipping for e-com,
author pages for YMYL, business registration number (SSM) in the footer. Monitor GSC Security
Issues; keep CMS and plugins patched.

## 7. Search Console and Bing Webmaster Tools

GSC: Domain property; sitemap index submitted; GA4 linked. Check in order: Manual actions +
Security issues → Page indexing (5xx, redirect errors, robots-blocked, noindex, **soft 404**,
"Google chose different canonical", "Crawled/Discovered – not indexed", "Indexed though
blocked") → Sitemaps (indexed vs submitted per template sitemap) → CWV → HTTPS → Performance
(branded filter, annotations) → **Generative AI report** → Links (orphans) → Enhancements →
Crawl stats → URL Inspection on each key template (Google-selected canonical, rendered HTML,
detected structured data). URL Inspection API: 2,000/day, 600/min per property, indexed
version only.
BWT: verify (import from GSC), sitemaps, IndexNow, **AI Performance**, URL Inspection, Site
Scan, robots tester.

## 8. Prioritised audit (automatable) — condensed

**P0 critical**: robots.txt 200/404 (never 5xx), <500 KiB · no site-wide or rendering-asset
block · key pages 200, not soft 404 · no accidental noindex (meta head/body, X-Robots-Tag) ·
correct canonical in raw HTML · https + single host in one hop · content in server HTML ·
HTML <2 MB · no manual action/security issue · staging not indexable (and production not
carrying staging's noindex) · no spam patterns (UA cloaking diff, hidden text, back-button
traps, doorways).

**P1 high**: valid sitemaps with honest lastmod · no redirect chains or internal links to
3xx/4xx · unique titles and one H1 · CWV field data passing · mobile parity · no orphans, money
pages ≤3 deep · hreflang valid · real 404s · faceted/parameter control · no "Loading…"
placeholders in rendered DOM · indexed/submitted ≥~90% on main sitemaps.

**P2 medium**: LCP image best practice · CLS guards · bfcache · meta descriptions · image alt
and og:image · structured data valid (Organization/WebSite on home, Breadcrumb, page types) ·
pagination · IndexNow wired · security headers · trust pages · accessibility basics (Lighthouse
a11y ≥90, lang, link text, 24 px targets) · compression + caching + conditional requests.

**P3 low**: URL style · speculation rules · favicon + site name · video indexing · anchor text
quality · llms.txt (optional) · Bing parity.

audit.py covers most P0/P1 and many P2 checks from outside; the rest need GSC/BWT access,
CrUX/PSI, a full crawl (Screaming Frog, SEOnaut, or a Playwright crawler) or the repo.

## 9. Myths — do not recommend

Meta keywords · word-count or keyword-density targets · exact-match domains · sitemap
priority/changefreq · rel=next/prev for Google · crawl-delay for Google · canonicalising
pagination to page 1 · noindex for canonicalisation · robots.txt to deindex · JS-removed
noindex / JS-changed canonicals · llms.txt / "AI files" / special markup for Google · chunking
or rewriting for AI · buying mentions · DA/DR as Google metrics · FAQ rich results · scaled
programmatic or unreviewed machine-translated pages · expired-domain redirects · renting
subfolders · back-button interstitials · CTR bots.
