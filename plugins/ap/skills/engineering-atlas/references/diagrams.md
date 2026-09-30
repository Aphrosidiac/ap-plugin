# Diagrams

Hand-authored inline SVG. No libraries, no runtime, no external images. A diagram is worth
its space when it shows a mechanism the reader would otherwise assemble from several files —
a fork and rejoin, a gate and what it refuses, a before/after, a hub and its satellites. A
box labelled with a noun is not that.

## The palette — non-negotiable, and the reason scripts/contrast.py exists

SVG colours are literals. They do not follow the theme tokens, so each one has to be legible
on **both** grounds — `#FFFFFF`-ish surfaces in light, `#1B1A16` in dark. These six are
already balanced (≥3.7:1 both ways). Use them and nothing else:

| Hex | Reads as | Typical use |
|---|---|---|
| `currentColor` | the page's ink | structure, unremarkable boxes, arrows |
| `#A57A12` | gold | the accented path; one actor in a two-actor diagram |
| `#1A85A2` | cyan | a second track or actor |
| `#C4508F` | magenta | a third track; gates, blocks, new things |
| `#3E9159` | green | success, "released", a closed loop |
| `#CB5A57` | red | the breaking change, the failure path |
| `#AE7C22` | amber | warning, held, pending |

The obvious-looking picks — `#0E7490`, `#A81F6B`, `#2F7A45`, `#946A00` — all sit near 2.5:1
on a dark ground and turn to mud. They look right while you are working in light mode, which
is how they get into a document.

Run `scripts/contrast.py` on the finished file before publishing. It scans every hex in every
SVG, checks both grounds, and suggests a replacement for anything failing.

## Mechanics

- `viewBox="0 0 W H"` sized to the content, plus `role="img"` and an `aria-label` carrying
  the same claim as the caption. CSS already handles scaling.
- One `<defs><marker>` per arrow colour, referenced by `marker-end="url(#id)"`. Give ids a
  document-unique prefix — several SVGs on one page share an id namespace, and a duplicate
  silently points every arrow at the first definition.
- Text 8.5–11.5px at drawn scale, `font-family="IBM Plex Mono, monospace"`. Short labels;
  explanation belongs in the `<figcaption>`.
- **Label the arrows.** `writes`, `invalidates`, `polls every 30s`. An unlabelled arrow only
  says "related somehow".
- Align to a grid. Shared baselines and even gaps are most of what makes a hand-drawn diagram
  read as deliberate.
- Nothing inside the SVG but shapes and text: no `<script>`, `<style>` or `<foreignObject>`.

## Generate anything with more than about eight boxes from Python

Eyeballed coordinates drift, and a fourteen-stage column written by hand will have one box
40px out. Emit the SVG from a small script with the geometry as data — then adding a stage is
a list entry, not a re-layout:

```python
BW, BH, STEP, Y0 = 216, 34, 50, 144
def stage(cx, y, name, role, col):
    x = cx - BW/2
    tab = f'<rect x="{x}" y="{y}" width="5" height="{BH}" fill="{col}"/>' if role \
          else f'<rect x="{x+1.5}" y="{y+1.5}" width="5" height="{BH-3}" fill="none" stroke="{col}"/>'
    return (f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" fill="none" stroke="{col}" stroke-width="1.4"/>'
            f'{tab}<text x="{x+14}" y="{y+15}" fill="{col}">{name}</text>'
            f'<text x="{x+14}" y="{y+27}" font-size="8.5" fill="{col}">{role or "auto"}</text>')
```

Filled tab = a human gate, hollow = automatic, is a good encoding: it puts the "who has to
act" information into the shape, so the reader gets it without the legend.

Before finalising, check the arithmetic on the last row — `Y0 + (n-1)*STEP + BH` must be
above whatever sits below it, and the `viewBox` height must exceed it. Overlap here is the
most common defect and it is invisible until rendered.

## Five that keep earning their place

**Swimlanes** when two parties hand work back and forth. Two horizontal bands, a dashed rule
between; each crossing is a handoff, and drawing them makes the count undeniable.

**Parallel tracks with a rejoin gate** for anything forking and reconverging. Columns per
track, a wide bar for the gate with its conditions written inside it. The gate is the
interesting part — give it room.

**Before / after, stacked** for a timing or ordering change. Same horizontal scale, old on
top in muted `currentColor`, new below in `#CB5A57`. The reader sees what moved without
comparing two pictures.

**One door, many callers** for an invariant. Callers stacked on the left, curves converging
on a single accented box, effects fanning right. The picture *is* the argument that the
invariant holds.

**Hub and satellites** for a model everything hangs off. Hub accented in the centre, upstream
spine on the left, satellites in a right-hand column joined by curves, colour-coded by which
subsystem owns each.

## Captions

State the claim, and prefer one that adds something the picture alone does not: what the
arrangement costs, what it protects against, or what would break without it. "Two independent
pipelines each own one boolean; the gate is the only place they meet" beats "job status flow".
