---
name: reference-clone
description: >
  Rebuild an existing website or software product as our own — studying a reference closely,
  measuring it instead of eyeballing it, pulling its assets down to work from, and
  re-implementing the experience under our own identity. Two modes: SITE rebuilds a marketing or
  brand website (design fidelity, motion, performance, SEO, CMS); SYSTEM rebuilds a SaaS or
  internal application (data model, roles, state machines, billing, concurrency). Use this
  whenever someone points at a product and wants their own version of it — "clone this site",
  "copy this SaaS", "rebuild X for us", "build our own Notion/Medium/Linear", "make me
  something like <url>", "recreate this landing page", "recreate it exactly, every
  animation", "1:1 demo of this site for the portfolio", "we want what they have but branded
  for us", "reverse-engineer this app". Reach for it even when the word "clone" never appears:
  if there is a reference product and the deliverable is our own working version of it, this
  is the skill.
---

# Reference Clone

Someone has pointed at a product and said *build me that*. The job is to reproduce the
**experience** — the information architecture, the flows, the interaction rhythm, the rules
that make it feel finished — under an identity the brief names.

How much of *them* comes across is set by one field in the brief, **fidelity**:

- **`exact`** — "recreate it exactly, every animation". Their stylesheet and DOM are kept
  verbatim as the measurement baseline, behaviour is re-implemented from their bundles, and
  only the brand is swapped. Proven ≤0.5 mean screenshot diff on five builds.
  → `references/exact-recreation.md`
- **`translate`** — our own product with their structure. Measure their numbers, write our
  own CSS, copy and imagery. → `references/measurement.md`

Neither mode pastes their minified JS into our repo; the difference is the CSS, the DOM and
the assets.

Four ways this fails, all of which look like success at the time:

- **Vibes translation.** You looked at the reference, formed an impression, and built the
  impression. It is 15% off on every number — type scale, spacing rhythm, easing, line length
  — and the result reads as a knock-off in a way nobody can point at. *The fix is measurement,
  not more looking.* See `references/measurement.md`.
- **The happy-path shell.** Every page exists and every button is present. None of the gates,
  role rules, state transitions, empty states, error paths, or concurrency behaviour exist.
  It demos beautifully and falls over on contact with a second user. This is the default
  failure of SYSTEM mode.
- **The unowned re-skin.** The build ships still wearing their photography, their wordmark
  and their sentences, because those went in as working material and nobody ever decided what
  replaces them. Take everything you need — then track it, and decide at Gate 2 what stays.
  See `references/reuse.md`.
- **The invented feature set.** You could not see behind their login, so you guessed, and now
  half the spec is a description of how products like this usually work. A guess presented at
  the same confidence as a measurement is the single most expensive thing you can put in a
  spec. Label every claim with how you know it.

---

## Step 0 — Fill the brief before anything else

Copy `assets/brief-template.md` into the repo as `docs/brief.md` and resolve every field.
Infer what you can from the reference and the user's message; ask only for what genuinely
changes the work — name, stack constraints, hosting, and the scope line (parity vs. MVP).
Do not ask questions whose answer you can measure.

**Brand assets are found, not asked for and never generated first.** Before anything else,
search the workspace for the owner's kit — `find ~/Desktop/dev -maxdepth 3 -type d \( -iname
brand -o -iname 'brand-system' -o -iname 'brand-kit' \) -not -path '*/node_modules/*'` (FF:
`ffdevstudio/brand-system`; Ascend: `AscPeps/brand`, versioned — read its `VERSION.md`). A
generated mark when a kit existed cost ExoApeClone a full redo.

**"No questions" briefs.** Fakhrul often says "no questions". Then nothing in this skill
stops to ask: resolve every field from inference and defaults, write the reasoning into
`docs/brief.md`, and treat Gates 1 and 2 as self-reviews recorded in `docs/qa-log.md` rather
than pauses. The two exceptions still hold: credentials, and anything outward-facing
(deploy, push to a public repo, real email or money).

Three fields decide most of the rest, so settle them explicitly:

- **Fidelity** — `exact` or `translate` (above). "Exactly the same", "every animation", "reuse
  the assets" mean `exact`.

- **Identity** — the new product's name, and whose site the reference actually is: ours or
  the client's (a rebuild — take the assets, they are already theirs), a third party's
  (take them as working material, decide what ships at Gate 2), or a third party's kept
  whole for an **FF portfolio demo** (ships with an in-page disclaimer naming the owner).
  `references/reuse.md`.
- **Scope line** — "the whole product" is almost never the real answer. Get an explicit list
  of what we are *not* building. Written down in the brief, at the top, before code.

---

## Step 1 — Pick the mode

**SITE** — a marketing site, brand site, portfolio, docs site, editorial site, landing page.
The value is design fidelity, motion, performance, and SEO. Little or no auth, little or no
persistent state.
→ Read `references/mode-site.md`

**SYSTEM** — a SaaS product, dashboard, internal tool, marketplace, anything with accounts.
The value is the data model, the permission matrix, the state machines, and the money. Visual
fidelity matters, but a pixel-perfect app with a wrong stock ledger is worthless.
→ Read `references/mode-system.md`

Most real jobs are **SYSTEM with a SITE attached** — the app plus its marketing front. Treat
them as two builds with two specs and two verification passes. Do the SITE last unless the
user says otherwise; it is the part that can be finished in a day and the part that changes
most after they see the app.

Both modes then use `references/measurement.md`, `references/assets-brand.md`, and
`references/verification.md`; at `exact` fidelity, `references/exact-recreation.md` replaces
most of the token work.

**Fingerprint the stack first** (Webflow, Nuxt, Next, Astro, headless CMS, Mux/Vimeo,
GSAP/Lenis versions — table in `references/exact-recreation.md`). Many references ship their
motion and content as extractable data; a Webflow export hands you every interaction as JSON.
Extract before you observe.

SITE mode has run on six real clones. SYSTEM mode has not yet been exercised end to end —
treat its checklist as sound but unproven, and add what the first real run teaches.

---

## Step 2 — Get access, then use it hard

Research is not a survey, it is evidence-gathering, and the amount of evidence is what
decides whether the spec is `[measured]` or `[inferred]`. So go wide and go deep: crawl every
page, snapshot the whole site, run the extractor on everything that renders, drive the app
with the browser tools, click every control, and keep every response body. Raise the caps on
the scripts rather than sampling — `MAX_PAGES` on `snapshot.sh` and `--max` on
`fetch_assets.py` exist to stop a runaway, not to limit you.

**Credentials — the one thing to get right:**

- **Already signed in in the browser, or prefilled in a form?** Use it. That session is the
  access, and driving the app with it is the single most valuable research you can do.
- **Nothing signed in, and you need an account to see the surface that matters?** Ask
  Fakhrul. He will either hand over credentials or tell you to make an account. Ask once,
  early, with a sentence on what you cannot see without it — do not spend an hour inferring
  something an account would have shown you in five minutes.
- **Never guess, brute force, or reuse credentials from another service.** Not a moral
  point: a lockout costs the whole research window and it is his account that gets locked.

**The public surface reaches further than people expect** — worth exhausting before you even
need an account: marketing site, pricing page (the best single source of a feature matrix and
plan gating), docs, help centre, changelog, public API reference, status page, RSS, sitemap,
open-source SDKs, job postings (they leak the stack), G2/Capterra screenshot galleries,
YouTube walkthroughs and demo videos, review-site feature matrices. A pricing page plus a docs
site plus an API reference will usually reconstruct 70% of a data model.

**Still no access?** Say so in the spec, at the top. Build from the public surface and mark
every inferred item as inferred. Do not smooth over the gap.

Two things that are not research, and stay out regardless: defeating CAPTCHA or bot
protection, and pulling other people's account data. Neither helps the build.

**Snapshot as you go.** The reference will change, and it may be A/B testing you into a
variant nobody else sees. Save raw HTML, screenshots, assets and a dated URL list into
`docs/reference/` (`scripts/snapshot.sh` for the server-rendered surface,
`scripts/dom_capture.mjs` for the hydrated DOM and every resource the page loaded, then
`scripts/fetch_assets.py --urls` to pull them all). Every later claim
should be traceable to something on disk with a date on it.

**Tooling on this machine.** Two instruments, for different jobs:

- **Headless Playwright — the default for evidence.** `scripts/capture.mjs`, `states.mjs`,
  `tokens.mjs`, `dom_capture.mjs` (shared launcher `scripts/browser.mjs`; run from the repo
  root after `npm i -D playwright`). rAF runs, timers are not clamped, the viewport is what
  you asked for, and nothing depends on a window being in front. When the Mac display slept
  mid-build, this was the only instrument that still told the truth.
- **Chrome (claude-in-chrome) — for sessions and for judging motion by eye.** It holds the
  logins. But a tab behind the Claude window is throttled to ~1 frame per screenshot, and
  `tabs_select` does not front it: run `scripts/front_tab.sh <url-substring>` and confirm
  `document.visibilityState === 'visible'` first. `resize_window` can report success while
  `innerWidth` stays stale — read it back. Resize the window back when done.

**Before any screenshot of a site with entrance or scroll animations, front the tab and run
`scripts/wake_page.js`.** A page whose content reveals on scroll renders fully, sits at
`opacity: 0` in a tab that is not painting, and photographs as an empty dark rectangle — the
report "the reference is just a dark blank theme" is the instrument talking. The script says
whether the tab is rendering at all, drives the reveals when it is, and forces the resting
state when it is not. Panes also report a zero viewport and clamp timers ~17×, so judge
motion and width-dependent values in a real window at a real width.

## Step 3 — Research, and produce a spec that is measured

Write `docs/reference-spec.md`. The mode file gives you the section list. Three rules that
apply to both modes:

**Every claim carries its provenance.** Use one of three markers and never mix them silently:
`[measured]` — I extracted this value from the page or a response body.
`[observed]` — I saw this behaviour happen but did not measure it.
`[inferred]` — I am reasoning from the public surface; this may be wrong.
A spec that is 60% measured and honest about the other 40% is worth more than one that is
uniformly confident and 20% fiction.

**Numbers come from the extractor, not from your eyes.** Run `scripts/tokens.mjs` (headless,
many pages and widths in one go) or paste `scripts/extract_tokens.js` into a fronted tab, on
at least three structurally different pages, plus at mobile width. **Measure every state**,
not the default one: trigger every mode, tab, filter and hover, and scroll each page to the
end. Obys's largest type (8rem) sat below the fold in a mask until hover, and a single-state
read concluded the site had one type size. It returns the type scale, the colour frequency table, the spacing
rhythm, radii, shadows, transition durations and easings, breakpoints, container widths and
z-index layers. Reconcile the three runs into one token set. See `references/measurement.md`.

**Inventory the invisible product too.** The parts nobody screenshots and everybody forgets:
transactional email templates and when each fires; webhooks; scheduled jobs and digests;
imports and exports (CSV shape is a free data-model dump); API keys and rate limits; search
and its filters; notification preferences; audit trail; plan gating and quota enforcement;
trial expiry behaviour; onboarding seed data; the legal footer; 404/500; the empty state for
every list; the "one item" state; the "10,000 items" state.

**GATE 1 — show the spec and the token set to the user before writing code** (on a
"no questions" brief: self-review it against the reference and log that you did). This is the
cheapest place to cut scope, and the only place where "we don't need that" costs nothing.

---

## Step 4 — Identity, then tokens

At `translate` fidelity: re-implement the reference's *structure* (grid, spacing rhythm,
type hierarchy, component anatomy, interaction patterns, page composition) and replace its
*identity* (palette, typeface, logo, copy, imagery, iconography, motion signature if it is
distinctive). At `exact` fidelity the identity swap is only what the brief names, usually
the wordmark, the contact details and the name, kept in one brand file
(`references/exact-recreation.md`).

How much of their identity survives is a decision, not a rule. On a rebuild for the site's
own owner, all of it does. On a third-party reference, the wordmark goes and the rest is the
user's call — put the list in front of them at Gate 2 rather than quietly deciding.

The mark always comes from the owner's brand kit when one exists (Step 0), used verbatim at
the kit's current version. `references/assets-brand.md` covers palette derivation, metric-compatible font substitution
(measured, not guessed), logo/wordmark generation, imagery, and — importantly — seeding
realistic content volume, because a reference site is always shown full and a clone with three
lorem rows will never look like it.

**GATE 2 — build one page or one screen to completion and show it.** Not a skeleton: one
real surface with real tokens, real content, real states, at desktop and mobile. Getting
agreement on one page is worth more than agreement on a description of forty.

---

## Step 5 — Build in dependency order, not page order

Page-by-page is the wrong order for SYSTEM mode and a trap in SITE mode too. Build:

1. **The spine** — schema, auth, tenancy, roles, the layout shell, the design tokens. Nothing
   else can be right until these are.
2. **The gates** — the rules that decide what is allowed: permission checks, state machine
   transitions, validation, quota and plan enforcement. Build them with the feature, never
   "after". Retrofitted permissions are how systems leak.
3. **The core loop** — the two or three flows the product exists for. End to end, including
   the error paths.
4. **Everything else**, ranked by the user's scope line.
5. **The surface** — marketing pages, empty-state art, polish, motion.

Commit in small, described steps so the history is readable. Follow the repo's existing
conventions if there are any; where the reference's implementation and the framework's idiom
disagree, follow the framework. You are reproducing behaviour, not their DOM.

**Do not clone their mistakes.** A reference is not a specification. Where it has broken
accessibility, a dark pattern, a dead end, a confusing label, or a legacy decision that only
makes sense given their history — fix it, and note the deviation in the spec. Deliberate
divergence is a feature; unrecorded divergence is a defect.

---

## Step 6 — Verify against the spec, adversarially

Read `references/verification.md` in full before the first pass. The short version:

- **Functional pass** per surface: every control, every state, every error path.
- **Measured visual pass**: computed styles diffed against the captured token set, **and**
  a numeric screenshot diff — `capture.mjs` run identically on both sites, then `diff.py`
  (mean absolute difference per capture, heat images, side-by-sides). Not "screenshot both
  and squint". Numbers, then eyes on the worst ones.
- **Adversarial passes** that a happy-path click-through cannot reach: every role against
  every route (including forbidden ones, by direct URL), two sessions racing one record,
  empty/one/many/huge data, offline and slow network, and a hostile input in every field.
- **Know your instrument.** A screenshot of a page stuck at `opacity: 0` looks like a fade —
  and a scroll-animated page in a sleeping tab looks like a blank dark theme. Run
  `scripts/wake_page.js` first, and read the DOM before believing a picture. A green test
  suite proves the tests ran, not that the feature works.

Log as you go in `docs/qa-log.md` — page, what you checked, how, what you fixed.

---

## Step 7 — Close honestly with a parity ledger

`docs/parity.json` is the deliverable that answers "are we done?". One row per item from the
feature inventory: `id`, `surface`, `feature`, `status` (`done` | `partial` | `deferred` |
`omitted` | `improved`), `evidence` (how you verified it), `notes`. Prose QA logs cannot be
counted; this can.

```bash
python3 scripts/parity.py docs/parity.json --markdown docs/parity.md
```

It fails on any `done` without evidence, which is the exact lie this step exists to prevent.

Then tell the user, in plain words: what is finished, what is partial, what you deliberately
left out, where you made a judgement call, and where the spec is inferred rather than
measured. A build reported as 100% when it is 85% costs more than the missing 15%.

---

## Scripts

| Script | Job |
| --- | --- |
| `snapshot.sh` | robots, sitemap, llms.txt, raw server HTML of every URL, dated |
| `dom_capture.mjs` | hydrated outerHTML + every loaded resource URL, per route (headless) |
| `fetch_assets.py` | download every asset (from HTML and/or `--urls`), largest srcset, manifest.tsv |
| `extract_tokens.js` | design-token census, pasted into a page |
| `tokens.mjs` | the same extractor headless across pages × widths, JSON out |
| `wake_page.js` | probe a tab's rendering state; drive or force scroll reveals before a capture |
| `front_tab.sh` | bring a claude-in-chrome tab to the front (AppleScript) so rAF and timers run |
| `capture.mjs` | top / mid-scroll / full-page captures at fixed widths, seeded, intro-bypassed |
| `states.mjs` | interaction-state captures from a per-project scenario file |
| `diff.py` | numeric screenshot diff: mean per capture, heat images, side-by-sides, masks |
| `parity.py` | validate and render the parity ledger |

The `.mjs` tools share `browser.mjs` and resolve Playwright from the project you run them in.

---

## Rules that do not bend

- Take what you need — assets, fonts, media, whole pages — and record where each came from
  (`references/reuse.md`, `scripts/fetch_assets.py`). What *ships* is decided at Gate 2 with
  the user, not assumed in either direction.
- Do not present the build as the reference's product, and do not ship under their mark.
- Use a session that is already signed in. If none exists and you need one, ask Fakhrul
  rather than guessing credentials or working around the login.
- Serve everything from our own origin. Never leave the build pointed at their live API, CDN
  or endpoints — not "just for now during development", because it never gets removed, and
  it breaks the day they change something.
- Ask before deploying. Approval to build is not approval to deploy, and push to GitHub before
  any deploy.
- Git-ignore `docs/reference/*/shots`, `docs/reference/*/states`, `docs/qa/shots` and
  `docs/qa/states` in the first commit. Captures run to gigabytes (EthanClone: 1.1 GB, purged
  from history before its first push).
- Test freely in dev; confirm with the user before anything that sends real email, real money,
  or a public post.
- If you cannot verify a claim, mark it `[inferred]`. Never launder a guess into a measurement.
