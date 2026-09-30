# Build brief — <NEW PRODUCT NAME>

Copy this to `docs/brief.md` and resolve every field before writing code. Fill in what you
can infer or measure yourself; ask the user only for what genuinely changes the work.

## Identity

- **Product name:**
- **Owner / brand:**
- **Whose site is the reference?** ours / the client's (a rebuild — take the assets, they are
  already theirs) / a third party's (take them as working material; decide what ships at Gate 2)
  / a third party's kept whole for an FF portfolio demo (Case C — disclaimer required)
- **Brand kit found at:** `<path>` @ version `<x>` — searched `~/Desktop/dev` first
  *(If none exists, generate — see `references/assets-brand.md`. Never generate when a kit exists.)*
- **Disclaimer slot** (Case C only): entry screen / hero headline / label on every page —
  owner named as: `<proper name>`
- **Tone of the product voice:** (terse & technical / warm / editorial / playful)

## Reference

- **Reference URL(s):**
- **What specifically do we want from it:** (the whole product / this flow / just the look)
- **Access:** signed in already / credentials to be supplied / public surface only
- **If an account is needed and none is signed in:** ask Fakhrul before proceeding — say what
  cannot be seen without it
- **Snapshot date:**
- **Assets pulled to:** `docs/reference/<date>/assets/` (manifest.tsv has the provenance)

## Mode

- **Fidelity:** exact (their CSS + DOM verbatim, behaviour ported, brand swapped —
  `references/exact-recreation.md`) / translate (our identity, measured tokens)
- **Reference stack fingerprint:** framework, CMS, video host, motion libs + versions
- **Questions allowed?** yes / "no questions" (gates become logged self-reviews)
- **Mode:** SITE / SYSTEM / SYSTEM + SITE
- If both: which first, and are they one repo or two?

## Scope line

- **In scope (the loop the product exists for):**
  1.
  2.
  3.
- **Explicitly NOT building** (list it — this is the field that saves the most time):
  -
  -
- **Parity target:** MVP that stands alone / feature parity / parity plus our own additions
- **Deadline or demo date, if any:**

## Technical

- **Repo:** name, public/private, owner
- **Stack:** (or "propose and justify")
- **Auth:** email+password / OAuth (which) / magic link / SSO
- **Multi-tenancy:** none / org / workspace / branch — decide now, not later
- **Data volume expected:**
- **Integrations that must exist:** payments, email, storage, marketplaces, other
- **Hosting target:** — self-hosted VPS preferred unless the user says otherwise
- **Domain:**

## Environment and safety

- **Is this environment safe to test in freely?** yes / no
- **Actions requiring confirmation before running:** real email, real payment, public post,
  anything writing to production, any deploy
- **Deployment:** approval required before any deploy; push to GitHub first

## Deliverables

- `docs/brief.md` — this file
- `docs/reference-spec.md` — the measured spec, with `[measured]/[observed]/[inferred]` markers
- `docs/reference/<date>/` — snapshots, hydrated DOM, screenshots, token JSON
  (shots/ and states/ git-ignored from the first commit)
- `docs/qa/shots`, `docs/qa/states` — our captures + `diff/` heat images (git-ignored)
- `docs/qa-log.md` — verification narrative
- `docs/parity.json` + `docs/parity.md` — the countable ledger
- The build itself, committed in readable steps

## Gates (do not pass without showing the user)

- [ ] **Gate 1** — spec + token set reviewed
- [ ] **Gate 2** — one complete surface, real tokens, real content, desktop + mobile
- [ ] **Gate 3** — spine + core loop working end to end
- [ ] **Gate 4** — full verification pass, parity ledger, honest close
