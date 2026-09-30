# Measurement

The reason clones look like clones is that every number is slightly wrong. Nobody can point
at it; everybody can feel it. Impressions do not survive translation — numbers do.

The rule: **if a value ends up in our code, it came from a measurement or a deliberate
decision, never from looking.** "About 24px" is not a measurement.

---

## The instrument

`scripts/extract_tokens.js` runs inside the page (via the browser tool's JS execution) and
walks every rendered element, returning:

- **Type scale** — every distinct `font-size` / `weight` / `line-height` / `letter-spacing` /
  family combination, with a count and an example selector for each. The heading scale falls
  out of the frequency table.
- **Colour census** — every computed colour, background, and border colour by frequency. The
  five most frequent are the palette; the long tail is noise and one-off states.
- **Spacing rhythm** — the distribution of margins, paddings and flex/grid gaps. Look for the
  base unit: if the top values are 8/16/24/32/48 you have an 8px system, if they are
  10/20/30 you do not, and building on the wrong unit misplaces everything downstream.
- **Radii, borders, shadows** — verbatim strings, because a two-layer shadow is a signature.
- **Motion** — transition and animation durations and timing functions by frequency. The most
  common pair is the product's motion signature; copy the *shape*, pick your own if it is
  distinctive.
- **Breakpoints** — parsed from every same-origin stylesheet's media queries.
- **Layout** — container max-widths, grid template columns, and the z-index layer stack.

Run it headless across pages and widths with `scripts/tokens.mjs` (same extractor, no hidden
tab), or paste it into a fronted tab. Run it on **at least three structurally different pages**
— a marketing page, a dense list or dashboard, and a form or article — plus once at mobile
width. A single page gives you that
page's tokens, not the system's. Reconcile into one token set and write it into the spec; the
values that appear on all three are the system, the rest are local.

Cross-origin stylesheets throw on `cssRules`. The script swallows those; if breakpoints come
back empty, that is why — read them from the network tab instead.

## Measure every state, not the default one

A page in its resting state hides much of its own design system. Before claiming a scale:
visit every page, trigger every mode/tab/filter, hover the interactive things, open every
menu and modal, and scroll each page to the end, capturing as you go (`scripts/states.mjs`
makes this repeatable). On Obys the 8rem project title was parked below the fold inside an
`overflow:hidden` mask until hover, so a single-state read concluded "one type size" and
produced a build with no large type at all. The extractor walks every element with a box,
masked or not, so trust its census over what the screen shows.

A reference is a set of **dated** observations. Sites get redesigned (Obys went from dark to
white). Re-open the reference and measure it before designing against a memory of it.

**Check `meta.viewportSuspect` and `meta.visibilityState` in every result before trusting a
width-dependent number.**
The in-app Browser pane has been measured reporting `innerWidth === 0` and
`documentElement.clientWidth === 0` on a normal live site — type, colour and motion still
come back correctly, but line length, container widths, grid tracks and overflow detection
are all meaningless in that state. The extractor flags it rather than returning a plausible
zero. When it fires, re-measure in a real Chrome window at a real width.

## Waking a scroll-animated page first

**A page whose content enters on scroll will photograph as an empty dark rectangle in any
tab that is not actually rendering.** Reporting "the reference is just a dark blank theme"
is the single most common false finding in this work, and it is the instrument, not the site.

Run `scripts/wake_page.js` before any screenshot or token extraction. It probes the
environment, picks a strategy from what it finds, and tells you what you may conclude:

- **Front the tab first** where you can. In the Browser pane that is `tabs_select`. In
  claude-in-chrome it is `scripts/front_tab.sh <url-substring>`, because the MCP cannot
  front a tab that sits behind the Claude window. That is the actual fix, and the only state
  in which motion can be judged at all. The script cannot un-hide itself. For evidence,
  prefer headless capture, which never has the problem.
- If the tab **is** rendering, it step-scrolls the full height with a dwell at each stop,
  which is what drives IntersectionObserver, ScrollTrigger, AOS and friends. It also forces
  `scroll-behavior: auto`, because a site with `html{scroll-behavior:smooth}` turns every
  `scrollTo` into an animation — the exact thing that will not run.
- If the tab is **not** rendering, it skips the scroll entirely (no amount of dwelling can
  make an observer fire without a render loop) and instead walks up from every invisible
  text node to the ancestor actually suppressing it, pinning that to its resting state.
  Targeted on purpose: a global `*{opacity:1!important}` would also reveal every closed
  modal and dropdown and produce a screenshot that is wrong in a new way.

Measured on lewix.ai in the hidden in-app pane, 2026-09-03: `visibilityState "hidden"`,
`rafFires false`, viewport 0×0, **`setTimeout(50)` actually took 788–879ms across runs — a 16–18× clamp**, and
**85 of 103 text elements invisible**. After the wake pass: 0. A naive step-scroll-with-dwell
loop in that environment blows the tool's own 45-second timeout before it achieves anything,
which is why the script measures the clamp first and budgets against it.

Read `verdict` before anything else. When it says the tab is not rendering, you have content,
structure and layout — and you have **nothing** about motion, lazy images, or anything
time-based. Those need a real window.

## What the script cannot see

- **Scroll behaviour and scroll-driven motion.** Watch it. Note: is scroll smoothed (Lenis,
  Locomotive) or native? Does content enter on scroll, and at what threshold, with what
  stagger, once or every time? Is there parallax, and at what rate relative to scroll?
- **Load sequence.** What paints first, what animates in, in what order, how long the whole
  entrance takes. Record it and count frames if it matters.
- **Hover and focus states**, and their transition timing — measure by hovering with the
  element inspected, not from the stylesheet.
- **Page transitions**, and whether they are real transitions or a fade over a hard nav.
- **The reference's own bugs.** Notice them, list them, do not reproduce them.

Measure motion in a real browser window at a real width. Automation panes throttle heavy
pages: lazy images never load, `scrollTo({behavior:'smooth'})` silently does nothing, and a
hidden tab never fires `requestAnimationFrame` at all — three false findings in a row have
come from exactly that.

## Two findings no eye would have guessed

On elevenlabs.io the display type is **weight 300**, and the h1 **does not grow past 48px**
on a wider viewport. A 400-weight h1 that scales makes an otherwise identical layout read as a
template. Clamp ceilings and light display weights are the numbers most often "corrected" by
eye. Measure them at 1440 and 1920.

## Layout numbers worth taking by hand

- **Measure (line length)** of body copy in characters — the single strongest driver of
  whether an editorial layout feels right. Beware `ch` units; they shift when the font
  swaps and have caused 100% of a page's CLS before.
- **Optical rhythm**: the vertical gap between a heading and its paragraph, versus between
  paragraphs, versus between sections. Three numbers, and they are rarely the same ratio you
  would guess.
- **Grid**: column count, gutter, and outer margin at each breakpoint.
- **Nav height, footer height, and the sticky offset** — a sticky header with the wrong
  offset breaks every anchor link on the site.

## Network as a data-model instrument (SYSTEM mode)

The browser's network log is the highest-value research surface in the whole job. With an
account, click through the app once with the log open and keep every JSON response body.

- **Response shapes are the schema.** Field names, types, nullability, nesting, ID format
  (uuid / cuid / sequential / prefixed like `inv_`), timestamps and their timezone handling,
  enum values in full, and computed-vs-stored fields.
- **Request shapes are the write model.** What the client is allowed to send, which fields
  are optional, what validation comes back on a deliberate bad request.
- **Query strings are the index requirements** — every filter, sort and pagination style
  (offset vs cursor) is a database decision you are about to have to make too.
- **Error bodies** give you the real validation rules and error taxonomy.
- **A CSV export is a free schema dump.** So is a public API reference, a webhook payload
  doc, and an OpenAPI/GraphQL introspection endpoint if one is exposed.

Click through everything the account can reach and keep the log — the more of the app you
exercise, the more of the model you get for free. If a fetch loop is faster than clicking,
run it. The only practical brake is that being rate-limited or blocked mid-research costs
more time than pacing would have, so back off when a 429 shows up rather than pushing
through it. Stay inside our own account's data; other customers' records are not part of
the model you are reconstructing.

## Recording it

Write the reconciled token set into the spec as an actual token block — the thing you will
paste into `tailwind.config`, `:root`, or the theme file — not a prose description. Save the
raw extractor JSON into `docs/reference/tokens/<page>.json` with a date. When the build looks
off later, the diff between our computed styles and those files is the answer, and
`references/verification.md` uses exactly that.
