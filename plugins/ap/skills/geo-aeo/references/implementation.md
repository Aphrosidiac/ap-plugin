# Implementation — making the changes in the codebase, per stack

Full per-framework notes and sources: `research/09-verticals-frameworks.md` Part B;
rendering rules: `technical-access.md` §4. Universal acceptance test after every change:

```bash
curl -sA "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot" \
  https://site/page | grep -E "<title>|rel=\"canonical\"|ld\+json|<h1"     # empty = AI crawlers see nothing
node scripts/render_diff.mjs https://site/page      # <10% words missing without JS, head tags identical
```

Work in the project's own idiom; one source of truth for site URL, name and canonical logic;
never hard-code the production origin in more than one place.

---

## Next.js (App Router)

```ts
// app/layout.tsx — root: site-wide defaults ONLY. Never alternates.canonical here.
export const metadata: Metadata = {
  metadataBase: new URL(process.env.SITE_URL!),          // one origin, set per environment
  title: { default: 'Acme', template: '%s | Acme' },
  openGraph: { siteName: 'Acme', type: 'website' },
  robots: { index: true, follow: true, 'max-snippet': -1, 'max-image-preview': 'large', 'max-video-preview': -1 },
}

// lib/seo.ts — per-page helper so every page sets its own canonical/og fields
export function pageMeta({ path, title, description, image, type = 'website', published, modified }): Metadata {
  return {
    title, description,
    alternates: { canonical: path, types: { 'text/markdown': `${path}.md` } },
    openGraph: { title, description, url: path, type, images: [{ url: image ?? '/og.png', width: 1200, height: 630 }],
                 ...(published && { publishedTime: published, modifiedTime: modified }) },
  }
}

// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const { slug } = await params; const post = await getPost(slug)
  if (!post) notFound()                                    // real 404, before any output
  return pageMeta({ path: `/blog/${slug}`, title: post.title, description: post.excerpt, type: 'article',
                    published: post.publishedAt, modified: post.updatedAt })
}
export async function generateStaticParams() { return (await allSlugs()).map(slug => ({ slug })) }
export const revalidate = 3600

// components/JsonLd.tsx — server component, native <script>, never next/script
export function JsonLd({ data }: { data: object }) {
  return <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }} />
}
```

- `app/robots.ts` → `{ rules: [...], sitemap }` (template from `assets/robots/`; Content-Signal
  lines need a plain `app/robots.txt/route.ts` returning `text/plain` since the typed API has no
  field for them). `app/sitemap.ts` → `lastModified` from the content's real `updatedAt`
  (never `new Date()`); `generateSitemaps()` above 50k URLs.
- Redirects: `next.config` `redirects()` (`permanent: true` = 308) or `permanentRedirect()`.
  X-Robots-Tag via `headers()` (e.g. `noindex` on preview/staging hosts).
- **Traps** (each has bitten a real build):
  1. **Canonical/openGraph in a layout is inherited verbatim** → every page claims to be the
     homepage. Metadata merges shallowly: a child setting `openGraph.title` wipes the layout's
     `openGraph.images`. Set per page through one helper.
  2. **Streaming metadata (≥15.2):** dynamic `generateMetadata` output is appended to `<body>`
     for any UA not in `htmlLimitedBots` — the default list has **no AI crawlers**. Make
     metadata static/cached so it prerenders into `<head>`, or override the list (overriding
     REPLACES the default, so re-include it):
     ```ts
     htmlLimitedBots: /Googlebot|[\w-]+-Google|Google-[\w-]+|Bingbot|applebot|facebookexternalhit|Twitterbot|LinkedInBot|Slackbot|Discordbot|WhatsApp|GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-User|Claude-SearchBot|PerplexityBot|Perplexity-User|meta-webindexer|CCBot|Amazonbot|Amzn-SearchBot|DuckAssistBot|MistralAI-User/i,
     ```
     audit.py flags head tags found inside `<body>`.
  3. `'use client'` pages fetching content in `useEffect` are empty to AI crawlers.
  4. `opengraph-image.tsx` inside a route group gets a hashed URL and only attaches to pages
     with no `openGraph` of their own — once pages set their own og fields, use a plain route
     (`app/og.png/route.tsx`, `dynamic = 'force-static'`) referenced from the helper.
  5. React 19 emits `<link rel=preload as=image>` for every non-lazy `<img>` streamed — mark
     decorative images `loading="lazy"` or `fetchPriority="low"` so the LCP image wins.
  6. `trailingSlash`: pick one; canonical, sitemap and links must agree.
  7. Prerendered metadata bakes in the **build-time** origin — build and serve with the same
     SITE_URL or canonicals won't match the host.
  8. Large `__NEXT_DATA__`/RSC payloads can push HTML past Googlebot's 2 MB cut.
- **Markdown for agents** (Vercel pattern):
  ```ts
  // next.config.ts
  async rewrites() { return { beforeFiles: [
    { source: '/blog/:path*', has: [{ type: 'header', key: 'accept', value: '(.*)text/markdown(.*)' }],
      destination: '/md/blog/:path*' } ] } }
  // app/md/blog/[...slug]/route.ts
  export async function GET(_req: Request, { params }) {
    const { slug } = await params
    return new Response(await postAsMarkdown(slug.join('/')), { headers: {
      'Content-Type': 'text/markdown; charset=utf-8', 'Vary': 'Accept',
      'Link': `<${process.env.SITE_URL}/blog/${slug.join('/')}>; rel="canonical"` } })
  }
  ```
  Plus `app/llms.txt/route.ts` (text/plain) if the owner wants one.

## Nuxt 3/4

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo'],   // robots (meta + X-Robots-Tag), sitemap, og-image, schema-org, link-checker
  site: { url: 'https://ex.com', name: 'Acme', defaultLocale: 'en' },   // single source of truth
  schemaOrg: { identity: { type: 'Organization', name: 'Acme', logo: '/logo.png' } },
  routeRules: { '/blog/**': { prerender: true }, '/admin/**': { robots: false },
                '/old': { redirect: { to: '/new', statusCode: 301 } } },
})
```
Pages: `useAsyncData`/`useFetch` (never `onMounted`), `useSeoMeta`, per-page canonical via
`useHead`, `useSchemaOrg([defineArticle(...)])`. Nuxt AI Ready module: llms.txt, .md
alternates, Content-Signal. **Traps:** `ssr:false` / `.client.vue` / `<ClientOnly>` content is
invisible · **only `NUXT_*` env vars override runtimeConfig at runtime** — `process.env` read in
`nuxt.config` is baked at build (wrong origin in canonicals/sitemaps; also leaks build-box
secrets into `.output`) — set `NUXT_SITE_URL` / `NUXT_PUBLIC_SITE_URL` in production ·
`nuxi generate` needs every dynamic route linked or listed in `nitro.prerender.routes`.

## Astro

Static by default (ideal). `site` in `astro.config` is required. Head in a base layout with
per-page `canonical = new URL(Astro.url.pathname, Astro.site)`, JSON-LD via
`<script type="application/ld+json" set:html={JSON.stringify(ld).replace(/</g,'\\u003c')} />`.
`@astrojs/sitemap` (can't list dynamic routes in SSR mode). Endpoints for `robots.txt`,
`llms.txt`, `[...slug].md` from `getCollection()`. **Traps:** `client:only` islands render
nothing server-side · `trailingSlash` + `build.format` must agree · static `redirects` emit
meta-refresh pages — use host rules (`_redirects`, `vercel.json`) for real 301s.

## SvelteKit

`export const prerender = true` (+ `entries()`), never `ssr = false` on content routes;
`<svelte:head>` for title/meta/canonical/JSON-LD (escape `<`); `+server.ts` routes for
sitemap/robots/llms with `prerender = true`; `setHeaders({'x-robots-tag': …})`;
`redirect(301, …)` in `load`. `trailingSlash` default `'never'`; `/x` ≠ `/x/`.

## React Router 7 / Remix (framework mode)

`meta` export per route (leaf routes don't merge parents — spread `matches`), React 19 head
hoisting works too; `prerender` in `react-router.config.ts`. With `ssr:false` + prerender,
un-prerendered paths fall back to `__spa-fallback.html` — **an empty shell for crawlers**.
Resource routes for sitemap/robots; `throw redirect('/new', 301)`; `headers` export for
X-Robots-Tag.

## Plain Vite React/Vue SPA (highest risk)

A pure SPA ships `<div id="root"></div>` to GPTBot, ClaudeBot, PerplexityBot. Options, best
first: (1) move the marketing/docs/product surface to a meta-framework (Next, Nuxt, Astro, RR7
framework mode) and keep the app as an SPA; (2) build-time prerender — **Vike** (`prerender:
true`), **vite-ssg** for Vue, RR7 `prerender`; (3) build-time Playwright snapshot of the route
list; (4) prerender service / dynamic rendering only as a stop-gap (Google calls it a
workaround; Rendertron is archived; add AI UAs to the service's bot list). react-snap is
unmaintained. Head managers (react-helmet-async, React 19 `<title>`, @unhead/vue) only help
once prerendered. Every route must return correct status codes — SPA hosts answering 200 with
`index.html` for unknown paths create soft 404s.

## Gatsby

`Head` export (4.19+), `gatsby-plugin-sitemap`, robots plugin or `static/robots.txt`,
`createRedirect` (host adapter must support it). SSG output is fine; for new builds prefer
Astro or Next.

## WordPress

Server-rendered PHP is fine; check page builders, review plugins and AJAX tabs that lazy-render
content. Yoast (llms.txt in Free+, schema graph linked by `@id`, extend via
`wpseo_schema_graph` filter rather than adding separate blobs) or Rank Math (LLMS Txt module) —
**one** SEO plugin. robots.txt is virtual (plugin editor or `robots_txt` filter; a physical file
overrides both). One sitemap (core `wp-sitemap.xml` or the plugin's), not both. Redirects:
plugin or nginx. **Traps:** "Discourage search engines" left on after launch · attachment pages
indexed · duplicate Organization/Product JSON-LD from theme + plugin · WooCommerce product
schema without `hasMerchantReturnPolicy`/`shippingDetails` · security plugins blocking bots ·
plugins injecting "AI" prompt text (audit.py flags it).

## Shopify

Agentic Storefronts / Shopify Catalog syndicate to ChatGPT, Copilot, AI Mode, Gemini (Settings
› Sales Channels › Agentic Storefronts) — leave on; fill Standard Product Taxonomy category,
category metafields, GTIN/barcode, real variant options. JSON-LD: `{{ product |
structured_data }}` or hand-written with ProductGroup, return and shipping policy — check theme
+ review apps don't output duplicate Product blocks. robots: `templates/robots.txt.liquid`,
iterate `robots.default_groups` and append, don't hard-code. Sitemap automatic. Redirects in
Navigation › URL Redirects (fire only when the old path 404s). Collection-scoped product URLs
canonicalise to `/products/…` — link the canonical form. Markets outputs hreflang. `seo.hidden`
metafield noindexes a resource. Developer: UCP + Catalog/Cart/Checkout/Order MCP servers.

## Webflow · Wix · Squarespace · Framer · Ghost

- **Webflow**: per-page SEO + CMS field binding; global + per-page canonical; robots editor;
  auto sitemap; 301s with wildcards; JSON-LD in page custom code (CMS embeds); **noindex the
  `*.webflow.io` staging domain**; hreflang only with Webflow Localization.
- **Wix**: SEO patterns per page type, robots editor, custom JSON-LD per page — watch for
  duplicates with Stores/Bookings-generated blocks.
- **Squarespace**: robots.txt not editable; "Block known AI crawlers" toggle blocks retrieval
  bots too — keep it off for GEO; JSON-LD via Code Injection; URL Mappings for 301s.
- **Framer**: static output; check animation components that mount text client-side.
- **Ghost**: `{{ghost_head}}` required (canonical, OG, JSON-LD); theme robots.txt overrides;
  `redirects.yaml`; members-only posts serve truncated bodies — public preview + paywall markup.

## Hugo · Jekyll · 11ty

Hugo: `enableRobotsTXT`, built-in multilingual sitemap, `.Permalink` canonicals, hreflang over
`.Translations`, **custom output format `text/markdown` writes `index.md` beside `index.html`**.
Jekyll: `jekyll-seo-tag` + `jekyll-sitemap`. 11ty: permalink templates for robots/sitemap/
llms. Shared: meta-refresh "redirects" aren't 301s — use host rules; X-Robots-Tag via host
`_headers`; per-environment `baseURL` or canonicals point at localhost/staging.

## Cross-stack snippets

IndexNow on publish (any stack; key file at `/<key>.txt`):
```ts
await fetch('https://api.indexnow.org/indexnow', { method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: 'www.example.com', key: KEY, keyLocation: `https://www.example.com/${KEY}.txt`,
                         urlList: changedUrls }) })   // 200/202 ok; 403 bad key; 422 host mismatch; 429 slow down
```

Organization-level JSON-LD belongs on the home page (and About); every page's graph references
it by `@id`. Visible "Updated" date and `dateModified` come from the same `updatedAt` field that
feeds the sitemap `lastmod` — one field, three outputs, no drift.

## Cross-framework trap register (lint list)

| # | Trap | Detect | Fix |
|---|---|---|---|
| 1 | Canonical in a shared layout → every page canonicalises to `/` | audit.py "Canonical points elsewhere … homepage" | compute per page |
| 2 | Head tags in `<body>` for AI bots (Next streaming) | audit.py "emitted inside <body>" | static/cached metadata or `htmlLimitedBots` |
| 3 | Client-only content / reviews / JSON-LD | render_diff.mjs | SSR/SSG, server-fetch reviews |
| 4 | Trailing-slash mismatch canonical/sitemap/links | sitemap vs canonical diff | one setting + 301 |
| 5 | Build-time env baked into canonicals/sitemaps | grep built HTML for localhost/staging | runtime env, per-env site URL |
| 6 | Soft 404s | audit.py soft-404 probe | `notFound()`, `error(404)`, host 404 rules |
| 7 | JS-removed noindex | raw HTML has noindex | decide on the server |
| 8 | Duplicate JSON-LD (theme + plugin + app) | count `@type` per page | one source, one `@graph` |
| 9 | Staging/preview domains indexed | `site:` search, headers | `X-Robots-Tag: noindex` on non-prod |
| 10 | One toggle blocks all AI bots (Squarespace, Cloudflare) | bot_access.py, robots | separate training from search/user bots |
| 11 | Unescaped `</script>` in JSON-LD from CMS data | fuzz with `</script>` | `.replace(/</g,'\\u003c')` |
| 12 | Child metadata wipes nested layout fields (lost og:image) | audit.py OG check per route | shared helper spread per page |
| 13 | Sitemap `lastmod` = build time | audit.py ">90% same day" | real `updatedAt` |
| 14 | "Summarize with AI" / hidden prompt text from a plugin | audit.py injection scan | remove; tell the owner the source |
