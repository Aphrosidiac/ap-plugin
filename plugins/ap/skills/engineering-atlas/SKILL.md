---
name: engineering-atlas
description: >
  Produce a publication-grade engineering document about a real codebase, published as a
  private Artifact with hand-drawn SVG mechanism diagrams, exhaustive function/endpoint
  indexes, and honest callouts of traps and open questions. Two modes: ATLAS maps an
  existing system (every pipeline, workflow, state machine and function); CHANGE SPEC
  decodes new requirements — client notes, a meeting transcript, a feature request — against
  the real code and says precisely how to wire them in, what breaks, and what to ask before
  building. Use this whenever someone wants to understand, document, hand over, onboard onto,
  audit the structure of, or plan changes to a codebase — including phrasings like "explore
  the codebase", "map the pipelines", "how does this system work", "document our
  architecture", "list all the functions", "build a graph of the workflows", "here are new
  requirements, how do we implement this", "what will this change break", "turn these notes
  into a plan", or "write a spec for this". Reach for it even when the user does not say
  "document" or "artifact" — if the answer is a map of a real system rather than a code
  edit, this is the skill.
---

# Engineering Atlas

You are documenting a system that people will make decisions from. The value is not the
prose and not the styling — it is that **every claim in the document is true of the code on
disk right now**, and that the reader can see mechanisms they would otherwise have to
assemble themselves from thirty files.

Two failure modes to design against, both of which read as competent:

- **Plausible fiction.** Describing what a system like this usually does instead of what
  this one does. A function name you half-remember, a flow that "must" exist, a count you
  estimated. Every one of these is worse than an omission, because the reader has no way to
  tell it apart from the parts you verified.
- **Inventory without insight.** A wall of tables listing everything and explaining nothing.
  Correct, exhaustive, and useless — the reader still cannot answer "why does production
  unlock here" or "what happens if I change this."

The whole method below exists to avoid those two.

---

## Step 1 — Pick the mode

**ATLAS** — the user wants to understand or document what exists.
*"explore the codebase", "map the pipelines", "how does X work", "document this for handover",
"list all the functions", "build a graph of the workflows"*
→ Read `references/mode-atlas.md`

**CHANGE SPEC** — the user has new requirements and wants to know how they land.
*"here are the client's notes", "how do we implement this", "what will this break",
"turn this meeting into a plan", "write a spec"*
→ Read `references/mode-changespec.md`

If genuinely both — "map the system and then tell me how this change fits" — do ATLAS first
and publish it, then CHANGE SPEC as a second artifact that links to it. They are different
documents with different readers; merging them produces something that serves neither.

Both modes then use the same design system (`references/design-system.md`) and diagram
conventions (`references/diagrams.md`).

---

## Step 2 — Ground yourself in the source, exhaustively, before writing a word

This is where the quality comes from. Budget most of your effort here.

**Start wide and structural.** Entry point, route/module registration, data model, directory
tree, file counts. You are looking for the shape of the thing, not details yet.

**Then run the inventory script.** It extracts every function and every HTTP endpoint with
its role guards into JSON you can embed directly:

```bash
python3 scripts/inventory.py --root <repo> --out <scratchpad>
```

It handles TS/JS, Python, Go and Vue; it is a starting point, not gospel. If the project has
a routing convention it does not know, read a couple of route files and extend the regexes
inline rather than hand-counting.

**Then read the code that actually decides things.** Not every file — the ones where control
flow branches and state changes:

- the state machines: status enums, transition functions, the guards on them
- the gates: what has to be true before the next step is allowed
- the write paths: what is the single door to each important table, and who calls it
- the schedulers, workers, hooks: what happens without a user asking
- the money, stock, or safety-critical arithmetic

**Verify the specific things you plan to assert.** If you are about to write "X is the only
writer of Y", grep for the callers and count them. If you are about to name a function, make
sure it exists with that name. If you are about to say a role can do something, find the
guard. This is cheap and it is the difference between a document people trust and one they
spot-check twice and then stop reading.

Two habits that repeatedly turn up the best material in a document:

- **Follow the comments that explain a decision.** A comment saying *why* a number is 3 ×
  3 rather than 9, or why a field is Decimal(14,6) rather than (14,2), is usually load-bearing
  domain knowledge that exists nowhere else. Quote it, and say what it prevents.
- **Notice what does not match.** A declared type that omits a value the code passes. A
  comment calling something "the final stage" when the sequence has one after it. An exported
  helper with zero callers. A role assigned work it has no route to reach. These are the
  findings the reader could not have got from reading the code linearly, and they are what
  makes the document worth publishing rather than just correct.

**Run the thing when you can.** Reading tells you what the code says; running tells you what
it does. Standing up a local database, booting the dev server and issuing one request turns
the sharpest claims from inferred to measured — and, just as valuable, lets you *withdraw* a
finding that looked real on the page and is not. A document that says "I verified this against
a running instance" and "I could not, so this is inferred from the repo alone" is worth far
more than one that quietly mixes the two.

**Never fill a gap by inference.** If you cannot determine something, the document says so —
as an open question in CHANGE SPEC, or as a plainly flagged unknown in ATLAS. Recorded
uncertainty is useful; a confident guess is a landmine.

---

## Step 3 — Write it

Read the mode reference for the section structure, and the design system for the HTML.

Author into a scratchpad file. These documents run 100–250 KB; build them in parts with
heredocs and concatenate, rather than one enormous write that is painful to fix.

The writing itself:

- **Lead each section with the mechanism, not the inventory.** "Two booleans and nothing
  else" before the table of everything that sets them. The reader should be able to stop
  after the first paragraph and still have learned the thing that matters.
- **Prefer the specific.** "231 endpoints" not "many endpoints". "`jobs.controller.ts:188`"
  not "in the jobs controller". "3.5 ml/m² by default, overridable per branch" not
  "configurable".
- **Every count states what it counted.** "124 endpoints" is not a fact until it says whether
  that is backend routes, or backend routes plus client wrappers, or route files. Three
  readers will assume three different things and one of them will quote your number back at a
  client. Write "59 backend HTTP routes across 30 route files (frontend API wrappers excluded)"
  — in the masthead strip, use the short label and put the definition in the section that owns
  it. The same applies to "functions": say whether tests, generated code and node_modules are
  in or out.
- **Say what a thing costs or prevents**, not just what it is. A gate is interesting because
  of what it refuses.
- **Use structure that encodes something true.** Number a sequence only when order carries
  information. Colour-code only when the colour means something a reader can look up.
- Include the exhaustive indexes — every function, every endpoint — but put them at the
  *end*, filterable, after the parts that explain. They are reference material; the earlier
  sections are the document.

---

## Step 4 — Verify before publishing

Three checks, all fast, each catching a class of error the others miss.

```bash
python3 scripts/validate.py <file.html>      # tag balance, structure counts, TOC/section match
python3 scripts/contrast.py <file.html>      # every SVG colour, against both theme grounds
```

`contrast.py` matters more than it sounds. Diagram colours are literals inside the SVG, so
they do not follow the theme tokens — a hue that reads beautifully on the dark ground can be
almost invisible on the light one, and you will not notice because you only looked at one.
Anything it reports below ~3.5:1 on either ground needs shifting; it suggests replacements.

Run those checks on the **finished** file, and re-run them after any edit. Checking a draft
tells you about the draft: a colour you already fixed still shows as failing, and a colour you
introduced afterwards never gets seen. If you sampled a file while it was still being written,
say so or check again — reporting a defect that the finished document does not have is its own
kind of fabrication.

Then **look at it rendered**, at a realistic desktop width, in both themes. Serve the
scratchpad over localhost and open it in the browser pane — an artifact iframe often will not
scroll under automation, and a hidden or throttled pane can paint blank sections that are
actually fine. Scroll gradually with a short wait between steps; a single huge jump reliably
screenshots an unpainted page and sends you chasing a bug that is not there.

Then publish with the Artifact tool. Set a real name (two to four words, no explainer), a
one-sentence description, and a favicon on first publish.

---

## Step 5 — Report, and remember

**In the terminal**, do not summarise the document — the user has the link. Give them the
three or four things they would want to know *before* opening it: what the system's central
mechanism turned out to be, the real defects you found, and anything that contradicts what
they or their notes believed. Lead with whatever would change a decision.

**Then write what you learned to memory** — the non-obvious findings, not the structure the
repo already records. The trap that would have cost hours, the assumption that turned out
false, the artifact URL so the document can be updated later rather than duplicated. Correct
anything the index already records wrongly; a stale memory is worse than a missing one.

Skip the write, and say you skipped it, when it would do harm rather than good: an evaluation
or harness run whose findings are about a test fixture, or an index already at its size limit —
in that case consolidate an existing entry instead of appending a new one.

---

## Judgement notes

**Scale the document to the system.** A 145-file backend with a 27-stage state machine earns
sixteen sections and ten diagrams. A 12-file CLI earns four sections and two. Padding a small
system to look thorough is as much a failure as compressing a large one.

**A diagram earns its place by showing a mechanism prose cannot.** Where data flows, what
state a thing moves through, which of two designs adds an edge. A box labelled "cache" says
less than the sentence it replaced. If a sentence is faster, write the sentence.

**Keep the house style stable across documents.** The design system in
`references/design-system.md` is deliberately fixed so that a team's atlas, change spec and
audit read as one series — like a publisher's format. Adapt the accent to the domain when it
genuinely helps (a print shop's four process inks legitimately map to four workflow tracks),
but do not redesign the page each time. Consistency here is a feature, not laziness.

**Be honest in the terminal about what you did not check.** If you inventoried 145 files and
read 30 of them closely, the coverage claim is "structure of all, mechanism of the thirty
that decide things" — say that, rather than implying you read everything.
