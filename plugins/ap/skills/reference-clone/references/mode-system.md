# SYSTEM mode

A SaaS product, dashboard, internal tool, marketplace — anything with accounts and persistent
state. Visual fidelity is the easy half. The hard half is invisible in every screenshot: the
data model, who is allowed to do what, which transitions are legal, what happens when two
people act at once, and what the money does.

A clone that looks identical and gets the stock ledger wrong is worth less than nothing,
because it will be trusted.

## Spec sections — `docs/reference-spec.md`

1. **Snapshot and access tier** — what you could actually see, what you could not, dated.
2. **Sitemap by role** — every route, and which roles reach it. Logged-out, each user role,
   admin, and any impersonation or support view. Include settings, billing, empty states,
   404/500, and anything only reachable from a dropdown.
3. **Feature inventory** — per surface, every control and what it does. Give each item a
   stable ID (`ORD-04`); these IDs become the parity ledger and are how "done" is counted.
4. **Data model** — entities, fields, types, nullability, relations, cardinality. Reconstruct
   from response bodies, form fields, filter options, CSV exports and API docs
   (`references/measurement.md`). Mark every field `[measured]` or `[inferred]`. Include:
   - **ID scheme** — uuid / sequential / prefixed / human-readable document numbers, and the
     format of any numbering series (`INV{YYMM}/{seq}`) plus who guarantees uniqueness.
   - **Enums in full.** A status enum with one missing value is a state machine that hangs.
   - **Money** — currency, precision, where rounding happens, tax model, whether prices are
     tax-inclusive. Never floats.
   - **Time** — timezone handling and storage type. A timestamp shifted on write and shifted
     back on read looks correct everywhere and is wrong in every export and every report.
   - **Soft delete, archival, and audit trail** — and whether the audit rows are real or
     just written alongside the mutation by the same code that could have skipped it.
5. **Tenancy model** — single-tenant, org/workspace, or per-branch. Which entities are scoped
   to which. This is the hardest thing to retrofit, so decide it in the spec.
6. **Permission matrix** — a literal table: roles down, actions across, cell = allowed/denied,
   plus the condition when it is conditional ("own records only"). Everything the UI hides
   must also be denied server-side; assume the UI is decoration.
7. **State machines** — for each entity with a status: the states, the legal transitions, who
   can perform each, what side effects fire on each, and what is immutable once past a state.
   Draw it. A quotation that can be edited after acceptance is a real-money bug.
8. **Core flows end to end** — sign-up, verification, onboarding, invite a teammate, the
   product's main loop, password reset, plan change, cancellation, account deletion. Include
   the failure branches, not just the happy path.
9. **The invisible product** — transactional emails and their triggers; webhooks; scheduled
   jobs, digests and reminders; search and its scope; notifications and preferences; imports
   and exports; API keys and rate limits; file storage and size/type limits; bulk actions.
10. **Billing and gating** — plans, what each unlocks, quotas and what happens at the limit,
    trials and what expiry does to existing data, proration, dunning, invoices. Even if we
    are not building payments yet, the *gates* must exist in the model or they never will.
11. **Concurrency and integrity rules** — which operations must be atomic, what is a real
    race (stock, seats, balances, slots, sequence numbers), and where a uniqueness or check
    constraint belongs.
12. **Non-functional** — expected data volume, list page sizes, what needs an index, retention,
    backups, and any compliance surface (PII, export, deletion).
13. **Provenance** — what we took from the reference and what still ships as theirs, per `references/reuse.md`.

## Build notes

- **Schema and tenancy first.** Everything else is cheaper to change than these two.
- **Gates ship with the feature.** A permission check added in a later pass is a permission
  check that was missing in production.
- **The write path for anything that matters is a single door.** One function that changes
  stock, one that changes a balance, one that issues a document number — enforced at the
  database, not by convention.
- **Concurrency is not a later concern.** Read-then-write on a shared quantity oversells the
  moment two people click at the same time. Conditional updates, transactions, row locks or
  unique constraints — pick one per contended resource in the spec, not in a hotfix.
- **Ledgers append, balances are derived-and-stored, and a test asserts `SUM(ledger) ==
  balance`.** Anything that can go negative in reality must be allowed to go negative in the
  model; clamping at zero is how a system quietly gives money away.
- **Seed realistic data.** The reference is always demoed full. Seed hundreds of rows across
  every state — including the ugly ones — or you will not see the pagination bug, the sort
  bug, the N+1, or the layout break until a customer does.
- **Migrations, from the first commit.** Not `db push` against a shared database.

## Verification additions

Beyond `references/verification.md`:

- **Role matrix pass.** Log in as every role and attempt every action, including by typing a
  forbidden URL directly and by calling the endpoint without the UI. Every cell in the
  permission table gets tested; the denied cells are the ones that matter.
- **State machine pass.** Attempt every illegal transition. Each must be refused server-side
  with a sensible message, not a 500.
- **Concurrency pass.** Two sessions, one record: simultaneous edits, simultaneous purchase
  of the last unit, double-submit of the same form, back-button resubmit, two tabs holding
  stale versions.
- **Data-shape pass.** Empty, exactly one, many, and pathological — very long strings, unicode
  and emoji, zero and negative quantities, far-future and far-past dates, a decimal with more
  precision than the column holds.
- **Money pass.** Recompute at least one total by hand. Check rounding at each step, tax, and
  what the PDF/export says versus what the screen says.
- **Job pass.** Every scheduled job and email trigger fired manually at least once, with the
  result inspected — not just "the cron is registered".
- **The green-suite caution.** A passing test proves the test ran. Break the thing on purpose
  and watch the test fail before you trust it; a mutation that does not fail is a mutation you
  did not actually apply.
