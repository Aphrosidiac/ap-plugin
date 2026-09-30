# Exact recreation

The method behind every clone that measured ≤0.5 mean diff against its reference (RemyClone,
StanzzaClone, EthanClone, ExoApeClone, AspenClone). Use it when the brief's **fidelity** is
`exact` — "recreate it exactly, every animation". For `translate` (our own product, our own
identity, their structure), the measured-token path in `measurement.md` is the method instead.

The difference in one line: **translate** measures their numbers and writes our own CSS;
**exact** keeps their CSS and DOM as the fixed baseline and rewrites only the behaviour
and the brand.

---

## Step 1 — Fingerprint the stack before measuring anything

Many references ship their design and motion data in a form you can extract, and doing that
beats hours spent watching. Check `view-source`, the script URLs, `window` globals and response
headers:

| Signal | Stack | What you can extract |
| --- | --- | --- |
| `webflow.<hash>.js`, `w-` classes, `data-wf-page` | Webflow | IX2/IX3 interaction JSON: every trigger, timeline, ease and breakpoint. See below. |
| `/_nuxt/`, `window.__NUXT__` | Nuxt | Prerendered routes are static HTML. Client-only routes need `dom_capture.mjs`. Scoped CSS modules are per component. |
| `/_next/`, `self.__next_f` | Next (App Router) | RSC payload has the content model. `/_next/image?url=` points at the originals. |
| `/_astro/`, `astro-island` | Astro | Mostly static HTML. Islands mark exactly what is interactive. |
| `a.storyblok.com`, `cdn.sanity.io`, `images.ctfassets.net`, `prismic` | Headless CMS | Originals at full resolution via URL params (drop the resize segment, or set `w=`). |
| `stream.mux.com`, `player.vimeo.com`, `.m3u8` | Hosted video | Renditions you can re-mux to self-hosted mp4 (`ffmpeg -i <m3u8> -c copy`). |
| `window.gsap`, `ScrollTrigger`, `Lenis`, `Swiper`, `THREE` | Motion libs | The exact versions (`gsap.version`, bundle banner). **Pin the same versions.** Easing defaults and scroll maths change between minors. |

Write the fingerprint into the spec's Snapshot section. Build in the reference's own stack
when it is reasonable (Astro for an Astro site, Next for a Next site, static Vite for a Webflow
export). You get their idioms for free and nothing has to be translated.

### Webflow IX extraction

- **IX3** (GSAP-based). Slice the text between `t.register(` and
  `window.dispatchEvent(new CustomEvent("__wf_ix3_ready"))`, then `eval('['+body+']')`. That
  gives interactions (scope, `wf:scroll` triggers with ScrollTrigger configs including
  `clamp(...)` strings, and `conditionalPlayback` breakpoints to skip) and timelines (targets
  `wf:class` / `wf:attribute` / `wf:inst`; the last maps to `data-wf-target`).
  `timing.ease` is an index into `["none","power1.in",…,"sine.inOut"]` (5 = `power2.out`),
  `tt: 2` = fromTo, `tt: 3` = set. Text splits are Webflow's `.gsap_split_word` /
  `.gsap_split_letter` spans.
- **IX2** (legacy). The `init({events, actionLists, site})` object. Breakpoints: main ≥992,
  medium 768–991, small 480–767, tiny ≤479. Group 0 of an action list is the reset state.
  `easeOut` = `cubic-bezier(0,0,.58,1)`. Initial states are applied inline at runtime, so
  copy them into CSS.
- **Dropdowns.** `w--open` goes on the toggle and the list. Hover mode applies only with
  `data-hover=true` on a non-touch device. The close class is removed after `data-delay` ms,
  and opening one dropdown closes the others.

Extract first, then measure only what the JSON cannot tell you: which of two duplicate
timelines wins (the later one) and real timings under the smooth scroll.

## Step 2 — Capture the hydrated DOM and every resource

```bash
node <skill>/scripts/dom_capture.mjs --base https://ref.example --out docs/reference/<date>/dom \
     --paths /,/about,/work,/work/a-project --scroll
python3 <skill>/scripts/fetch_assets.py https://ref.example \
     --urls docs/reference/<date>/dom/resources.txt -o docs/reference/<date>/assets
```

The server HTML of any JS-rendered site is missing the client-only surfaces. The hydrated
outerHTML and the resource list include them. Prettify the bundles (`npx prettier --parser babel`)
into `docs/reference/<date>/js/` so behaviour can be read.

**Skip the intro before measuring.** A preloader or boot animation is not the page. Find the
flag that skips it (sessionStorage key, cookie, query param) and pass it via `--init`, or wait
it out with `--ready`. Capture the intro separately with `states.mjs` at timed offsets.

## Step 3 — Build: their CSS verbatim, their DOM converted, our behaviour

- **Stylesheet verbatim, class names 1:1.** It goes in one file (`webflow.css`, `exo.css`,
  `globals.css`) and nobody edits it, because it is the measurement baseline. Brand overrides
  go in a separate file loaded after it (`ff.css`, `brand.css`). When the build looks off,
  the diff between the two files tells you whether you or they caused it.
- **Pages generated, not hand-edited.** Write a converter (`tools/gen_pages.*`) that takes the
  captured HTML and produces our pages: asset URLs to local paths, brand strings swapped from
  a single BRAND map, their scripts stripped. Re-run it to change anything. A hand-edited page
  drifts from its siblings and from the reference, and nobody can say how.
- **Behaviour re-implemented** module by module from the prettified bundles, in readable code
  in our repo (`src/js/`, `components/`). Never paste their minified bundle in. The exception
  is a large, self-contained widget with no behaviour to reinterpret (EthanClone's 2.6k-line
  pricing calculator), which you vendor whole and record in Provenance.
- **Library versions pinned** to the reference's (GSAP, Lenis, Swiper, three).
- **Third-party embeds rebuilt on our origin.** HubSpot forms, booking portals and iframe
  forms are reproduced from their SSR markup and CSS with our own logic. A bundled (deferred)
  parent listener can miss an iframe's first `postMessage` that the reference's inline
  listener catches. Add a ready handshake.
- **Media self-hosted.** Regenerate the size variants the reference serves (sharp, ffmpeg).
  Where an original is dead, substitute a live alternate and note it in the spec.
- **Identity in one place.** One brand file (`lib/site.ts`, a BRAND map in the converter,
  `brand.css`). The mark comes from the owner's brand kit (`assets-brand.md`), never
  generated when a kit exists.

## Step 4 — Prove it numerically

```bash
# the reference, once (skip if the shots already exist)
node <skill>/scripts/capture.mjs --base https://ref.example --out docs/reference/<date>/shots \
     --paths /,/about --sizes 1440x900,390x844 --init "sessionStorage.setItem('intro','1')" --scroll wheel
# ours, same args
node <skill>/scripts/capture.mjs --base http://127.0.0.1:3160 --out docs/qa/shots \
     --paths /,/about --sizes 1440x900,390x844 --init "sessionStorage.setItem('intro','1')" --scroll wheel
python3 <skill>/scripts/diff.py docs/reference/<date>/shots docs/qa/shots --suffix 1440 --side
# interaction states, one scenario file for both sites
node <skill>/scripts/states.mjs --base https://ref.example --out docs/reference/<date>/states --file tools/states.scenarios.mjs
node <skill>/scripts/states.mjs --base http://127.0.0.1:3160 --out docs/qa/states --file tools/states.scenarios.mjs
python3 <skill>/scripts/diff.py docs/reference/<date>/states docs/qa/states --side
```

Run captures one at a time, never in parallel. A starved headless browser stretches animation
clocks. For a calculator, form or other logic surface, add a functional check that compares
outputs, not pixels (EthanClone matched six quotes to the dollar).

Targets from past builds: ≤1 mean on static route captures, ≤1.5 on states, with the residue
explained (brand-copy reflow). Then judge motion by eye in a **fronted** real Chrome tab
(`scripts/front_tab.sh`), side by side with the reference, because no diff sees easing
between the frames you sampled.

## Step 5 — Demo disclaimer (FF portfolio demos)

When the recreation keeps the reference's photography, film, marks or copy and will be
published as a demo (`reuse.md`, Case C), the disclaimer is load-bearing:

- Put it in the most prominent slot, planned from the start: the entry/loader screen
  (RemyClone), the hero headline (StanzzaClone) or a label on every page (EthanClone).
- Name the owner by their proper name ("Stanzza Design", not the domain). Say every image,
  film, mark and word is theirs, that the demo is not affiliated, and that it is not a live
  site. Plain text, not a link. Echo it in the meta description.
- Keep it whenever the hero, entry or footer changes. Grep the built HTML for it before any
  deploy.
- Do not spend time generating replacement imagery unless asked. Replacing the assets
  defeats the comparison the demo exists for.
