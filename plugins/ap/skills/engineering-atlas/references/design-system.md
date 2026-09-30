# Design system

The look is fixed on purpose. A team's atlas, change spec and audit should read as one
series — same rail, same type, same tables — so that a reader who has seen one can navigate
the next without relearning it. Treat this the way a publisher treats a book format.

## Assembling the page

`assets/shell.html` is the complete `<title>`, font links and stylesheet. It is the first
part of every document. Build the rest in numbered parts and concatenate:

```bash
S=<skill-dir>; SP=<scratchpad>
sed 's/__TITLE__/Payments Atlas/' $S/assets/shell.html > $SP/p1.html
cat > $SP/p2.html <<'PART'   # rail + masthead + first sections
...
PART
cat $SP/p1.html $SP/p2.html $SP/p3.html ... > $SP/doc.html
```

Write the page body directly — the Artifact tool supplies `<!doctype>`, `<head>` and
`<body>`. Do not add them.

To preview locally, wrap a copy with a minimal doctype and serve it over localhost; the
browser pane will not render a `file://` URL.

## Type

Three faces, each with one job. Never mix them up — the consistency is what makes dense
pages readable.

| Face | Role |
|---|---|
| **Archivo** 500/600/700 | headings, eyebrows, stat numbers, card titles |
| **Newsreader** 400/500/600 | all running prose. A serif body is what keeps a long technical page from reading like a config file |
| **IBM Plex Mono** 400/500/600 | every identifier: function names, endpoints, enum values, file paths, table bodies, rail links, diagram text |

Anything a reader might paste into a terminal or search for is mono. Anything explaining it
is Newsreader.

## Colour

Tokens are defined three times in `:root`, `@media (prefers-color-scheme: dark)` guarded by
`:root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. Never declare a colour
only inside a media or `[data-theme]` block. Style through the tokens.

Neutrals are warm-biased, not pure grey — `--paper: #F6F4EF` light, `#131210` dark. Accent is
gold (`--gold`). Semantic: `--good` `--warn` `--bad`. Track/domain hues `--k --c --m --y` are
available for categorising, and are the four process inks — they map naturally onto any
system with three or four parallel concerns.

**Diagram colours are different — see `diagrams.md`.** They are literals inside the SVG and
do not follow the tokens, which is exactly why `scripts/contrast.py` exists.

## Layout

`.wrap` is a 236px sticky rail plus the main column, collapsing to one column under 940px.

**Rail** — `.brand`, `.sub`, then `nav#toc` with `.grp` group labels and one `<a>` per
section carrying a two-digit `<span class="n">`. Group the sections into three or four named
groups; a flat list of sixteen links is unusable. The scrollspy script at the end of the
document adds `.on`.

**Masthead** — `.mast` with `.eyebrow` (what this is, and what it was built from), an `<h1>`
that states a *finding* rather than naming the document, a `.lede` of two or three sentences,
and a `.counts` strip of six or seven real measured numbers.

The h1 is worth care. "Every pipeline in the label ERP" and "The system now has two companies
in it" both tell the reader something before they scroll. "System Documentation" does not.

**Sections** — `<section id="…">` with `.shead` containing `.num` and an `<h2>`, then a
`.dek` one-liner, then prose. Prose is capped at 70ch by the stylesheet; let it be.

## Components

| Class | Markup | Use for |
|---|---|---|
| `.figbox` | `<figure><div class="figbox"><svg …></div><figcaption>…</figcaption></figure>` | every diagram |
| `.legend` | `<span><i class="sw fill"></i>label</span>` | only when an encoding repeats |
| `.tw` / `.tw.scrolltbl` | `<div class="tw"><table>…` | any table; add `scrolltbl` past ~25 rows |
| `.note` / `.note.warnbox` | `<div class="note"><span class="tag">…</span><p>…` | a trap, a decision, a thing that will bite |
| `.grid2` + `.card` | `<div class="grid2"><div class="card"><h4>…` | three to six parallel points |
| `.chip` | `<span class="chip m-GET">GET</span>` | HTTP methods (`.m-*`), tracks (`.t-*`) |
| `.req` | see `mode-changespec.md` | one decoded requirement |
| `.q` | `<div class="q"><span class="n">Q-01 · blocks R-08</span><p>…` | an open question |
| `.phase` | `<div class="phase"><h4>…<div class="meta">…` | one step of a build order |
| `<pre>` | `<b>` keyword, `<i>` new/changed, `<s>` removed, `<span class="c">` comment | schema and code |

## Indexes

Large inventories go at the end, in a `.tw.scrolltbl`, rendered from JSON embedded in a
trailing `<script>` with a text filter and a category `<select>`. Show a live "N of M" count —
it tells the reader the filter is working and how much they are looking at.

Keep the JSON compact (`separators=(',',':')`, short keys). A 600-row function index costs
about 60 KB, which is nothing against the 16 MB artifact ceiling.

## Things that go wrong

- **A colour defined only in a dark block.** The default "system" theme stamps no attribute;
  a token that only exists behind `[data-theme]` never applies, and the page renders one
  theme's text on the other's ground.
- **`body` without an explicit background.** The artifact host paints its own ground behind
  a transparent body.
- **A table wider than the page.** Always inside `.tw`; the body must never scroll sideways.
- **Emoji as section markers, centred everything, a giant hero.** This is a working document.
