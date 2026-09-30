# Identity, assets and content

The reference is always demoed at its best: real photography, real copy, a full database, a
typeface someone paid for. Ours will be judged against that, and the gap is usually not the
code — it is empty tables and placeholder art.

## Palette

Derive, do not copy. Take the measured colour census, identify the *roles* (surface,
elevated surface, border, body text, muted text, primary action, and the semantic four), then
build our own values into those roles.

- Keep the relationships: if their body text sits at 13:1 on the background and their muted
  text at 4.8:1, hold those ratios with our hues. The contrast structure is what makes a
  palette feel professional, and it is a number you can check.
- Echo the mood, not the hex. "Muted editorial", "saturated dark", "warm neutral" survives
  translation; `#0A5AFF` does not.
- Define light and dark together, as tokens, before any component. Retrofitting dark mode
  costs several times what including it does.
- Watch asset polarity when restyling: art baked on a white plate will show its plate on a
  dark surface, and it looks like a rendering bug rather than an asset problem.

## Typography

If the reference uses a licensed or proprietary face, substitute — and substitute by
measurement, not by reputation:

1. Identify the face (the extractor returns the family; `@font-face` src names confirm it).
2. Shortlist open alternatives with a similar classification and skeleton.
3. Render the same string at the same size in each candidate and compare **x-height,
   cap-height, and the width of a fixed string**. Metric closeness is what keeps the layout
   from moving; a face that "looks similar" but sets 6% wider breaks every line break.
4. Record which you chose and why, in the spec.

Take the font file if you can get it and self-host it — a paid face served from a licensing
CDN is often domain-locked and will 403 from our origin, so render it on our domain before
assuming it works. Either way: self-host, subset, preload the above-the-fold face, and set a
metric-adjusted fallback stack — the fallback is where CLS lives.

Wordmarks are frequently custom-drawn or heavily modified and are not recoverable by matching
a Google font. If ours needs a wordmark and the kit has none, draw or generate one rather
than pretending a stock face is a logo. When a kit lockup replaces a reference wordmark, size
its box to keep the reference's cap height, not its width, or every line around it moves.

## Logo and icons

- **Find the kit first.** Every brand Fakhrul owns or works for has a kit on disk. FF:
  `ffdevstudio/brand-system/assets/svg` (the `//FF` lockup and mark). Ascend:
  `AscPeps/brand`, which is versioned, so read `production/…/VERSION.md` and use the current
  masters verbatim. Others turn up with `find ~/Desktop/dev -maxdepth 3 -type d -iname
  '*brand*' -not -path '*/node_modules/*'`. Use its mark, lockup, favicons and OG template as
  they are. ExoApeClone shipped a generated pill mark and an Outfit wordmark while a
  complete Ascend kit sat in the workspace, and it had to be redone.
- Logo: on a rebuild, use the client's existing mark — pull the SVG, and ask for the source
  file if the web copy is a raster. Only when no kit exists, generate or design one that
  belongs to us:
  simple, works at 16px, works in one colour, works on both backgrounds. Ship the favicon set and the OG image with it — an
  otherwise finished site with a default favicon reads as unfinished at a glance.
- Icons: use a licensed set (Lucide, Phosphor, Heroicons, Radix) matched to the reference's
  *style* — line weight, corner radius, whether they are filled. Do not mix sets.

## Imagery and illustration

- On a rebuild, the existing photography is the client's — take it at full resolution and
  reuse it. Otherwise download theirs as working material, and decide at Gate 2 what stays;
  generated or licensed imagery is usually the better answer by ship time, because their
  photography is what makes our build look like a re-skin of theirs.
- Generated art has failure modes worth naming: transparency must be asked for explicitly or
  you get a white plate; transparent PNGs of glossy objects look like slop on dark
  backgrounds; and a "set" of objects only reads as a set if the prompt locks the suffix —
  same camera angle, same light, same line weight, same palette — across every generation.
- Whatever the medium, the images must be consistent with each other before they are good
  individually. One off-style hero ruins a page of correct ones.
- Respect the reference's *density* of imagery. A layout designed around full-bleed
  photography collapses when you fill it with icons.

## Copy

Read theirs to learn what each screen has to accomplish; write ours — their sentences are
about their company, and shipping them makes our product sound like a stranger's. Headlines, subheads,
empty states, error messages, button labels, tooltips, email subjects, the 404. Match the
register — terse and technical, or warm and conversational — not the sentences.

Placeholder copy is a defect that ships. `Lorem ipsum` and "Feature one" in a committed
build always reach a demo eventually.

## Seed data — the most underrated step

A clone with three rows of test data cannot be compared to a reference shown full, and worse,
it hides real defects: pagination, sorting, truncation, overflow, N+1 queries, and every
layout break that only appears at length.

Seed:

- **Volume** — hundreds of rows in the main tables, not five.
- **Every state** — one record in each status, including the terminal and error ones.
- **Realistic extremes** — the longest plausible name, the largest plausible number, the
  customer with 400 orders and the one with zero.
- **Plausible content** — real-shaped names, dates spread across months, amounts that vary.
  Uniform seed data hides sorting and grouping bugs.

Keep it in a re-runnable seed script, and keep a demo dataset separate from a test fixture
set; they have different jobs and merging them makes both worse.
