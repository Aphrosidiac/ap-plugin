# Reuse — what to take, and what ships

**Default posture: take everything.** Download the images, the fonts, the stylesheets, the
video, the icons, the whole rendered page. You cannot rebuild what you have not got a copy
of, and working from local originals beats working from a screenshot every time. Fetch at
full resolution, keep the originals untouched, and record where each file came from.

The only question worth asking is not *may I download this* — it is **whose site is this,
and what ships in the final build**. Ask it once, at brief time, and write the answer in
`docs/brief.md`.

---

## Case A — the reference is ours, or the client's

A redesign, a rebuild, a migration, a fork of a site the client already owns. **This is the
most common case**, and here there is nothing to decide: the photography, the logo, the
product shots, the copy and the brand are already theirs. Take all of it and ship it.

- Pull assets at the highest resolution the site serves. Check for a `srcset`, an
  `?w=2000`-style CDN parameter, or an uncompressed original behind the thumbnail — sites
  routinely serve a 400px version of a 4000px file.
- Grab the things that are easy to forget and annoying to recreate: favicon set, OG images,
  team photos, client logos, certificates, product PDFs, embedded video posters.
- If the old site is dying or already broken, the static tree often still serves even when
  the app 500s — and the Wayback Machine has the rest. Recover before it is gone.
- Keep originals in `docs/reference/<date>/assets/` and derive optimised copies into the
  build. Never optimise over the only copy you have.

## Case B — the reference is a third party

Download freely for reference, comparison, measurement, and as working material while you
build. That is research, and it is how the job gets done.

The decision is only about **what remains in the shipped product**, and it is the user's
call, not yours. Raise it once, as a short list, at Gate 2 — not as a running commentary:

- **Their logo and wordmark** — this one is not really a legal question, it is a branding
  one: our product cannot carry their mark and be our product. Replace it.
- **Photography and illustration** — usually worth replacing, because it is theirs, it is
  often licensed per-site, and it makes our build look like a re-skin of theirs rather than
  its own thing. Generate or source ours (`references/assets-brand.md`).
- **Icons, UI chrome, textures, generic imagery** — take them if they help; swap to a
  licensed set (Lucide, Phosphor, Heroicons) when it is no more effort than not.
- **Fonts** — download and self-host. Practical note: a paid webfont served from a licensing
  CDN is often domain-locked and will 403 from our origin, so check it actually renders on
  our domain before assuming it works. If it does not, substitute by measurement.
- **Copy** — read theirs to learn what each screen has to say, and write ours. Not for
  legal reasons: their sentences are about their company, and shipping them makes our
  product sound like a stranger's.

Say plainly which of these you kept, which you replaced, and which are still theirs at ship
time, in the spec's **Provenance** section. The point is that nobody discovers it later.

## Case C — FF portfolio demo (a third party, kept whole, disclosed)

Fakhrul has chosen this shape every time an FF demo recreated an award-level site (RemyClone,
StanzzaClone, EthanClone, AspenClone): keep the reference's photography, film, marks and
copy so the recreation is exact, swap only the brand identity to FF Dev Studio, and publish
it openly with a prominent disclaimer written into the page. The demo exists to show FF can
reproduce the motion exactly. Replacing the assets would defeat the comparison, so the
honesty goes in the disclaimer.

- Plan the disclaimer slot at brief time: the entry screen, the hero headline or a label on
  every page. Name the owner properly ("Stanzza Design"). State that the assets are theirs,
  that the demo is not affiliated, and that it is not a live site.
  `references/exact-recreation.md`, Step 5, has the specifics.
- Do not generate replacement imagery unless asked.
- Fictional content added to fill a demo (team, testimonials) says so on the page.
- Public repo and deploy only on his explicit instruction, like every deploy.

## The one thing that is genuinely not ours to do

Do not present the build as *them* — their name, their mark, their identity, or anything
implying it is their product or endorsed by them. In Case C their marks appear *as theirs*,
under a disclaimer naming them; that is the opposite of presenting the build as theirs. Everything else in this file is a
preference you can override; this one is what separates *our version of it* from something
nobody wants to have shipped.

---

## Working method

Use `scripts/fetch_assets.py`. It reads a live URL or a saved HTML file, resolves every
image, `srcset` candidate, video, poster, stylesheet, icon, preload and OG image, follows
one level into CSS for `url()` fonts and background images, downloads the lot, and writes
`manifest.tsv` with source URL, HTTP status, bytes, content-type and local path.

```bash
python3 scripts/fetch_assets.py https://reference.example -o docs/reference/2026-09-03/assets
```

Two practical habits:

- **Keep the manifest.** When someone asks in three months where a photo came from, or the
  client wants the original of a hero image, the answer is one file lookup.
- **Pull the whole set in one go**, then work offline from the copies. The script sleeps
  briefly between requests; the only reason to slow it further is that a rate-limit or block
  mid-research costs more than the pacing would have. Back off on a 429, otherwise go.

## Code

Reading their compiled JS/CSS to understand a behaviour is normal and often the fastest way
to answer a question — do it. Pasting a minified bundle into our repo is a different thing,
and not because of ownership: it is unreadable, unmaintainable, coupled to their build, and
you will never be able to change it. Take the *behaviour* and write it in our stack. The
exception is anything genuinely generic — a well-known algorithm, a snippet that is the only
sane way to do the thing — which you would have written the same way anyway.
