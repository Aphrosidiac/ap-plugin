# Verification

Two things are being proved, and they need different instruments: **does it behave as
specified**, and **does it look as measured**. A click-through proves neither on its own.

Before any of it: *verify the instrument*. Every wrong conclusion in this kind of work has
come from a measuring device that was quietly not looking.

## Instrument traps — read once, remember forever

- **A screenshot of a page stuck at `opacity: 0` looks like a fade in progress.** Check
  `document.getAnimations().length` and the computed opacity, not the picture.
- **A hidden or backgrounded tab never fires `requestAnimationFrame`.** Animations never
  start, transitions sit at `currentTime: 0`, lazy images never load, smooth scroll no-ops.
  Three "bugs" in one session have come from this. Front the tab, or measure differently.
- **A scroll-animated page in such a tab photographs as an empty dark rectangle**, and the
  conclusion "it's just a dark blank theme" writes itself. Run `scripts/wake_page.js` before
  any screenshot: it reports whether the tab renders at all and reveals the resting state
  when it does not. Never conclude "blank" from a picture — `read_page` / `get_page_text`
  return the text no matter what the opacity is, so the DOM settles it in one call.
- **Timers are clamped in a hidden tab too** — a measured 16–18× on `setTimeout(50)`. Any
  wait-and-look loop takes far longer than you budgeted and will hit the tool timeout, which
  reads as "the page hung" rather than "the tab is asleep".
- **Automation panes throttle heavy pages** the same way. Verify motion and above-the-fold
  behaviour in a real window at a real width.
- **An occluded Chrome tab is a hidden tab.** claude-in-chrome does not front its tab. Behind
  the Claude window it gets about one rAF per screenshot, and a 4-second preloader "takes"
  over a minute. Run `scripts/front_tab.sh`, then check `visibilityState`. `resize_window`
  can report success with `innerWidth` unchanged, so read it back.
- **A sleeping display hides every tab.** When the Mac display sleeps, every Chrome tab
  reports `hidden` with a ~17× timer clamp. Headless Playwright (`scripts/capture.mjs`) is
  unaffected. Use it as the evidence instrument.
- **Headless `--window-size` clamps below ~400px** and crops the capture. Phone widths need
  viewport emulation (`browser.mjs` does this below 700px). When a phone picture shows
  overflow the DOM denies, the DOM is right.
- **The dev server can 404 a new route directory** until it restarts. Three "broken" pages
  were fine.
- **An 800px pane hides real defects** — a missing header, a missing button, wrong labels.
  Verify at the width the user actually has.
- **A perfect score is a red flag.** If a comparison returns 100% or a metric returns exactly
  the expected value on the first try, suspect the harness before believing the result.
- **A stale page measures beautifully.** If you are sampling the same route repeatedly,
  confirm the content actually changed between samples.
- **`curl` is not a browser.** A route that returns 200 can render blank. Click it.
- **Verify the shipped artefact**, not a stand-in that renders differently — the production
  build, the real PDF, the real email, at the real URL.

## Pass 1 — Functional, per surface

Walk the feature inventory for that surface, item by item, and mark each one in the parity
ledger as you go. For every control: the action happens, the right thing persists (reload and
confirm), the wrong input is refused with a useful message, and the loading and error states
both actually appear. Include the empty state and the "one item" state.

## Pass 2 — Measured visual

Not "screenshot both and squint". Diff numbers, two kinds:

**Screenshots, numerically.** `scripts/capture.mjs` with identical arguments on both sites
(same paths, widths, `--init`/`--ready` intro bypass, `--scroll` mode, seed), then
`scripts/diff.py <ref> <ours> --side`. For interaction states, use one scenario file for both
with `scripts/states.mjs`, naming mid-transition frames by time offset (`menu-0.4s`), and diff
the folders the same way. Reading it:

- ≤1 mean is identical bar anti-aliasing and brand copy. 1–3 is small real differences,
  usually brand-copy reflow. >3 means something is actually different, or the instrument is.
- Before calling a spike a defect, open the side-by-side. Common false alarms: a reference
  that lazy-loads photographs placeholder plates; timed elements (a rotating logo, a clock, a
  video frame) need `--mask`; two captures running at once stretch GSAP's clock (always
  capture sequentially); and a height difference in full-page shots is its own finding
  (`--crop` compares the shared part).
- Capture the reference once, into the dated `docs/reference/<date>/shots`, and re-capture
  only ours. The reference can change under you; the dated folder is the fixed point.

**Computed styles.**

1. Load our page and the reference at the same fixed width with equivalent content.
2. Run `scripts/tokens.mjs` (or `extract_tokens.js`) on ours; diff against the saved
   reference token JSON.
3. Investigate every difference in type scale, spacing rhythm, radii, and the top five
   colours. Some differences are deliberate identity choices — those get recorded as
   deliberate, in the spec, not silently kept.
4. Then look at the screenshots, for the things numbers do not carry: alignment, optical
   balance, hierarchy, crowding.

Do this at desktop and mobile. Fix, re-measure, repeat until the deltas are all explained
rather than merely small.

## Pass 3 — Adversarial

The passes a happy-path click-through cannot reach. SYSTEM mode has the fuller list in
`references/mode-system.md`; the universal core:

- **Every role against every route**, including forbidden ones by direct URL and by calling
  the endpoint with the UI bypassed.
- **Two sessions, one record.** Race the writes.
- **Data shapes**: none, one, many, pathological. Long strings, unicode, emoji, zero,
  negative, far dates, high precision.
- **Hostile input in every field** — the point is a clean rejection, not a stack trace. Be
  careful reading the results: escaped, harmless output frequently matches the regex you were
  using to detect an attack, and reads as a vulnerability when it is the defence working.
- **Network reality**: offline, slow, a request that fails mid-flow, a double submit, the
  back button after a submit.
- **Refresh on every screen**, and deep-link to every screen cold. Client-routed apps hide a
  lot of state that only exists if you arrived from somewhere else.

## Pass 4 — Full sweep

After all surfaces are built, walk every flow in the spec end to end in one sitting, in a
production build, as a new user with no seeded session. Things that pass individually fail in
sequence — this is where you find the onboarding step that assumes data the previous step
did not create.

## The log and the ledger

`docs/qa-log.md` — narrative: surface, date, what you checked, how, what you found, what you
fixed. Written as you go, not reconstructed at the end.

`docs/parity.json` — the countable answer. One row per inventory ID:

```json
{ "id": "ORD-04", "surface": "orders", "feature": "Bulk status change",
  "status": "partial", "evidence": "Functional pass 2026-09-03; single-select works, multi-select not built",
  "notes": "Deferred per scope line" }
```

`status` is one of `done`, `partial`, `deferred`, `omitted`, `improved`. `evidence` says how
you know — which pass, what date, what you observed. `scripts/parity.py` refuses any `done`
without evidence, which is precisely the lie this exists to catch.

## Reporting

State what is finished, what is partial, what was deliberately omitted, where you diverged
from the reference on purpose, and which parts of the spec were `[inferred]` rather than
measured. If a check could not be run, say that instead of implying it passed. A build
reported at 100% when it is 85% costs more than the missing 15%, because the next person
builds on top of the claim.
