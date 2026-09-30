# Mode: ATLAS

The reader is a competent engineer who does not know this system. They will use the document
to answer real questions — where do I change this, what does this break, why is it like
that — so it has to be *navigable*, not just complete.

## Shape

Sixteen sections is right for a large system (100+ source files, several subsystems). Six is
right for a small one. The structure below scales by dropping sections, not by thinning them.

**Masthead.** Eyebrow naming the repo, branch and commit you read. An `<h1>` that states the
system's central fact. A lede of two or three sentences that names the *tension* the system
resolves — the thing that makes it non-trivial. Then measured counts: models, modules,
endpoints, functions, states, roles, pages.

Run `scripts/inventory.py` for those counts and keep the definition it prints. The strip shows
the short label; the section that owns each number spells out what was counted. "Endpoints"
alone is ambiguous enough that two careful readers will disagree by a factor of two — server
routes, or those plus every client wrapper?

**Foundations** (2–3 sections)
- *Shape of the system* — stack, process model, what is deliberately absent. Then the seam
  worth knowing: the boundary where two parts of the system meet and could fight.
- *Request path / execution path* — the middleware, hooks and guards wrapping every unit of
  work, and which of them write to a database. Small horizontal diagram.
- *Domain model* — the hub-and-satellites picture, plus a table of the enums that gate
  behaviour with a "what a transition costs" column. Not every enum: the ones that decide.

**Pipelines** (3–7 sections, one per real flow)
Each is: a one-line dek, two or three paragraphs on the mechanism, one diagram, and a table
of every function in that pipeline with file and a one-line "does". Where a pipeline has a
non-obvious rule, follow it with a `.note` explaining what it prevents.

Find the pipelines by asking what a unit of work *is* in this system and what has to happen to
one, end to end. Name them by what they do, not by module — "order becomes jobs", not "the
sales-orders module".

**The engine** (if there is one — a state machine, scheduler, orchestrator)
Deserves its own two or three sections: the full topology as one large diagram, a table of
every state with its entry effect and its exit effect, and the engine's own functions. This
is usually the part nobody has ever seen whole.

**Cross-cutting** (2–4 sections)
The invariants. The single write door and its callers. What happens without a user — workers,
hooks, cascades. Roles and where they are actually enforced, which is usually more than one
layer and they usually disagree.

**Indexes** (2–3 sections)
Every endpoint with its guards. Every function with kind and file. The frontend or client
surface. Filterable, at the end.

**Lead with a structural insight if there is one.** The best atlases open with the single fact
that reorganises everything else — "this repo contains two order systems and the README
documents the dead one", "production unlocks on two booleans and nothing else". Look for it
before you start writing: it usually falls out of noticing which subsystem every other
subsystem defers to. If there genuinely isn't one, organise by pipeline and say so plainly
rather than manufacturing a thesis.

## What lifts an atlas above a correct one

**Answer "why is it like that".** When the code carries a comment explaining a decision —
the geometry that made a live job look impossible, the decimal precision that was silently
truncating a price, the standard a sample size is drawn from — put it in a `.note` with what
it prevents. This is the knowledge that leaves when a person does.

**Report the defects you find, in place.** An exported helper with zero callers whose rows
look identical to real ones. A sequence lookup missing one of its branches. A role with work
assigned and no route to reach it. Put each next to the mechanism it affects and say what it
would cost. A document that only says nice things about the code is not a document anyone
consults twice.

**Be exact about instruments.** If a table or a metric cannot distinguish two states people
assume it can, say so loudly — that is often the single most valuable paragraph in the file.

## Terminal report

Three or four things, chosen by whether they would change a decision:
- the central mechanism, in one line
- each real defect found, with the file and what it costs
- anything contradicting what the user believed — including their own notes and memory
- what you inventoried versus what you read closely
