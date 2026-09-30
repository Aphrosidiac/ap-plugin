# Mode: CHANGE SPEC

The input is loose — meeting notes, a voice-memo transcript, a client's bullet list, a
paragraph describing a flow. The output has to be precise enough to build from, honest about
what it cannot resolve, and grounded in the code that exists rather than the code you imagine.

The reader is the person who has to implement it, and usually also the person who has to go
back to the client with questions.

## Before writing: find the structural insight

Read all the notes, then read the code they land on, then ask: **what one fact do these notes
assume that the system does not model?** A second organisation. A second currency. A state
that exists on the floor but not in the schema. An actor who is currently just a notification.

There is almost always one, and it explains a third of the individual bullets at once.
Leading with it turns twenty-three unrelated requests into four structural moves plus a list
of fields — which is the difference between a plan someone can sequence and a backlog.

If you genuinely cannot find one, say so and organise by subsystem instead. Do not invent a
unifying theory that is not there.

## Shape

**Masthead.** Eyebrow: what the notes are, dated, and the commit you decoded them against.
An `<h1>` stating the structural insight. A lede that names it and says how much of the notes
it explains. Counts: requirements, new models, breaking changes, new endpoints, new pages,
open questions.

**§00 What actually changes.** Three to five `.card`s, each a structural move. Then a `.note`
with the one-line summary the reader can repeat to their client.

**§01 The new flow.** One diagram of the whole thing — swimlanes if two parties are involved,
which they usually are. Every crossing of a boundary is a handoff needing a record, a
notification and a waitable state; the diagram makes that count undeniable.

**§02–07 The decoded register.** Every note becomes a `.req` card, grouped into themed
sections. Never drop one — a bullet you silently ignored is a bullet the client will ask
about.

```html
<div class="req">
  <header><span class="id">R-07</span><h4>Hold the PO until it is worth sending</h4>
    <span class="sev breaks">changes PO lifecycle</span></header>
  <p class="said">"hold PO for a certain supplier/product until it reach a certain amount"</p>
  <div class="body">
    <p>One or two sentences: what this actually means in system terms.</p>
    <dl>
      <dt>Touches</dt><dd><code>real/file/paths.ts</code>, real function names</dd>
      <dt>Add</dt><dd>the concrete field, model or enum value</dd>
      <dt>Logic</dt><dd>where it goes and when it runs</dd>
      <dt>Careful</dt><dd>the thing that will bite</dd>
    </dl>
  </div>
</div>
```

Quote the client verbatim in `.said` — including the ungrammatical parts. It is how they
recognise their own request, and how you prove you did not paraphrase away a constraint.

Severity chips: `.new` `.extend` `.breaks` `.ask`. Where two notes contradict each other, say
so in the card, give your reading and why, and raise a question rather than silently picking.

**§08 Schema changes, in full.** Actual Prisma/SQL/migration syntax in `<pre>`, new fields
marked with `<i>`, removed with `<s>`. Then a table of columns added to existing models with
the requirement id that drives each. Then a `.note` on migration ordering and which backfills
must be separate scripts.

**§09 Engine changes** if there is a state machine. The new topology as a diagram with new
states visually distinct, then exactly what to change in which file, then the new
handlers/hooks as a table.

**§10 What this breaks.** A numbered table: change / consequence if you just ship it /
mitigation. This is the section that earns the document. Every row must be about data that
already exists — in-flight records stalling at a new gate, a reassignment that strands open
work, an idempotency guard that does not exist yet. Close with sequencing advice: which of
these go behind a flag.

**§11 API additions**, **§12 Frontend work.** Tables, grouped by module, with roles.

**§13 Questions.** Ten to fifteen `.q` blocks. Mark which requirement each blocks and whether
it changes the data model. Include the client's own unanswered questions — if they wrote
"how do they decide?", that is a question, not a requirement. State your assumption for each
so work is not fully blocked.

**§14 Build order.** `.phase` blocks, each independently deployable, sequenced so nothing sits
half-wired. Phase 0 is usually "settle the blocking questions" with no code. Put the engine
rewrite last — it calls into everything the earlier phases build. Close with "if you only ship
three things", chosen for daily impact over completeness.

## The discipline that makes it trustworthy

**Check what already exists before proposing it.** Half of any note list is usually already
built, sometimes better than the note assumes. Saying "this is already done and here is where"
is more valuable than a plan to build it again.

**Read the note against the code, not against the domain.** "Deduct stock when the job
starts" only becomes a real finding once you have found the line where it is deducted today.

**Name the collisions.** New requirements reuse words the codebase already has for something
else. When "tooling" means a job state machine in the code and a shelf of cutters in the
notes, say so in a `.note` and insist on a separate model — that one paragraph prevents a
week of confusion.

**Estimate honestly in the counts.** If a note might be one field or might be a six-month
integration depending on an answer, that is a question, not an estimate.

## Terminal report

Lead with the structural insight — it is the thing they did not know they had told you. Then
the traps found in the existing code, then the questions that block schema work. Close with
scale: models, endpoints, pages, phases.
