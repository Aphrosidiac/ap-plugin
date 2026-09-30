# SITE mode

A marketing site, brand site, portfolio, docs or editorial site. Little auth, little state.
The value is entirely in fidelity, motion, performance and findability — which means the bar
is *higher* than it looks, because there is nothing else to hide behind.

## Spec sections — `docs/reference-spec.md`

1. **Snapshot** — reference URL, date crawled, what device/width, whether you saw a variant.
2. **Sitemap** — every reachable page, with URL pattern, purpose, and template. Include
   404, the legal pages, and any page only reachable from the footer.
3. **Page anatomy** — for each page, the section stack in order: hero, feature rows,
   testimonial, CTA, footer. Note which sections repeat across pages; those are components.
4. **Component inventory** — nav (desktop and mobile), buttons and their variants and states,
   cards, forms, accordions, tabs, carousels, modals, toasts, footer. Every state:
   default / hover / active / focus-visible / disabled / loading / error.
5. **Design tokens** — the reconciled measured set (`references/measurement.md`).
6. **Motion spec** — entrance animations and their triggers and thresholds, scroll-driven
   effects, hover timings, page transitions, the load sequence. Durations and easings as
   numbers.
7. **Content model** — if there is a blog/case-study/product index: what one item contains,
   how the index paginates, filters, and sorts. This is the CMS schema.
8. **Responsive behaviour** — what changes at each breakpoint, not just "it stacks". Nav
   collapse, type scale shifts, image crops, section reordering, what gets hidden entirely.
9. **SEO and social surface** — title/description patterns, canonical strategy, OG and
   Twitter tags, structured data (which schema types), sitemap.xml, robots.txt, RSS.
10. **Performance profile** — LCP element, image formats and sizes served, font loading
    strategy, whether it is static/SSR/SPA, roughly what the page weight is.
11. **Accessibility** — landmarks, heading order, focus visibility, contrast, reduced-motion
    handling, alt text discipline. Note where the reference fails; we will not.
12. **Provenance** — what we took from the reference and what still ships as theirs, per `references/reuse.md`.

## Build notes

- **Static-first.** If the reference is a marketing site, ours should render as static HTML
  with hydration only where it earns it. Do not import an SPA's architecture for a brochure.
- **Motion must not own resting state.** An element's correct final appearance belongs in
  CSS; the animation moves *to* it. Otherwise a route change, a paused document, a throttled
  tab or `prefers-reduced-motion` leaves a fully rendered page invisible at `opacity: 0`, and
  a screenshot of it looks like a legitimate fade.
- **A mount-once reveal observer will hide every page after the first** in a client-routed
  app. Re-run it per navigation or do not use one.
- **Fonts.** Self-host, preload the one face used above the fold, `font-display: swap`, and
  set a metric-matched fallback stack — an unmatched fallback is where CLS comes from. Avoid
  `ch` sizing on anything that must not move.
- **Images.** Modern formats, explicit width/height or aspect-ratio on every image, sized to
  the layout, lazy below the fold and eager for the LCP element.
- **Scroll-lock must not shift layout.** Hiding overflow widens the page by the scrollbar
  width unless you compensate; measure and pad.
- **Sticky, clamp and `100vh`** are the usual suspects for "the feature works but the layout
  is wrong on this one device". Check sticky offsets against anchor links, `clamp()` at both
  ends of its range, and mobile viewport units against the real browser chrome.
- **Horizontal overflow** is almost never the element you think. Find the actual widest node
  before fixing anything. The usual cause is `min-width: auto` on a grid or flex item: a
  code block's intrinsic width sets the track, and `overflow-x: auto` on the child does
  nothing until the track gets `min-width: 0`.
- **Line-split reveals** ("lines rise out of a mask"). Measure lines with **one text node and
  Ranges** (`Range.getClientRects()` per word), never a span per word: spans drop cross-word
  kerning and wrap differently from the real render. Split only after
  `document.fonts.load('<weight> 16px <family>')` for every face (`fonts.ready` resolves
  early). A fallback-metric split locks a `w-fit` box to the wrong width forever. Round
  nothing: use `getBoundingClientRect().width` as-is and render lines `white-space: nowrap`.
- **three.js colour.** `new THREE.Color('#888')` converts sRGB to linear (r152+). A shader
  ported from a reference that fed raw components comes out darker; use
  `setRGB(r, g, b, LinearSRGBColorSpace)`.
- **A `position: fixed; z-index: -1` canvas** paints under any later section's background
  unless it sits inside a positioned ancestor's stacking context.
- **A persistent WebGL canvas in a Next layout** mounts twice in dev. An imperative
  `createRoot` needs `extend(THREE)` and its own `advance()` loop.
- **UI sound**, if the reference has it: one tick per item change, never per sub-mark.
  Dense UI audio reads as noise.

## Shipping a static demo (Cloudflare Pages direct upload)

The FF demos ship this way. Pushing to GitHub deploys nothing; `npm run deploy` does. Only on
explicit instruction.

- **25 MiB per-file cap** rejects the whole upload. Run `find dist public -size +25M` before
  building and re-encode media (`ffmpeg -c:v libx264 -crf 23`).
- **Next `output: "export"`**: `app/sitemap.ts` and `app/robots.ts` need `export const
  dynamic = "force-static"`. `next build` hangs silently on `.next/lock` while `next dev`
  runs for the same project, so stop dev first.
- **wrangler ≥4.132** routes `pages` through Workers and fails with "Missing entry-point".
  `--force` keeps the legacy Pages path.
- Copy a working `scripts/deploy.sh` from RemyClone or EthanClone (size check, clean
  build) rather than writing a new one.

## Verification additions

Beyond the standard passes in `references/verification.md`:

- Every page at 320 / 375 / 768 / 1024 / 1440 / 1920, and check for horizontal scroll at each.
- Both colour schemes if the reference has them, and `prefers-reduced-motion: reduce`.
- Every internal link and every anchor resolves; no 404 in the nav or the footer.
- Meta and OG tags render per page — not one root canonical applied site-wide, which
  de-indexes everything below it.
- Real Lighthouse or field numbers for LCP/CLS/INP on the heaviest page, against the
  reference's own numbers where you can get them.
- Keyboard-only pass through the whole site: visible focus, sensible order, no traps, skip
  link works.
- Load the site cold on a throttled connection and watch the entrance sequence run once.
- Every capture of a scroll-animated page — reference or ours — goes through
  `scripts/wake_page.js` first. On our own build, run it with `reveal: false`: if it reports
  most text invisible while the tab **is** rendering, our resting state is broken, which is
  the defect that leaves a route blank after a client-side navigation.
