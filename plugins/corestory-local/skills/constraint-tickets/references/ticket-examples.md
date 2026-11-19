# Ticket examples — what converted, what did not

**Read this after writing your tickets, not before.** Example 1 is the measured exemplar for one
specific constraint in one specific repository (Shopizer at `6a4a0a6`). A writer decomposing a
Shopizer spec who has seen it is reproducing the exemplar, not deriving a ticket, and a demonstration
of this skill on Shopizer is not independent derivation.

All texts are verbatim from CoreStory's August–September 2026 measurement program on Shopizer,
GitHub Copilot CLI, `claude-sonnet-5` at `--effort high` unless stated. The program's evidence file
is internal and not published; every number here is quoted from it.

## 1. The constraint as the whole ticket — converted 5 of 5

593 bytes. Decomposed from an 85 KB CoreStory-generated spec by the prompt in `SKILL.md` Phase 2,
with no source tree available to the writer. Names the area ("one payment gateway"), never the file.
All five diffs were identical, which means the task admitted exactly one patch — reassuring for
correctness, and no basis for a rate.

```
## Ticket 10 — Fix incorrect transaction type recorded by one payment gateway's refund

One of the supported payment gateway integrations records a completed refund using the wrong internal transaction type, tagging it the same way a capture would be tagged instead of as a refund. This is a concrete correctness bug: any order refunded through this gateway will show inaccurate transaction history, which will confuse reporting and any downstream logic that relies on transaction type to determine order state. Correct the transaction type so it accurately reflects that a refund occurred.
```

Register to copy: **what is wrong → why it matters → the ask.** No code, no path, no line. The
engineer (or agent) is expected to locate it.

## 2. A second measured ticket — 13 of 15 addressed the hazard (`gpt-5.6-sol`, 15 runs)

632 bytes. Same decomposition, different constraint. It describes a required *behavior*, not a
bug — constraints include both. The comparator arm, which received the same ticket with one sentence
appended naming the defective selection logic, read the method in 15 of 15 runs and addressed the
hazard in 9 of 15; that difference is not statistically significant at these counts.

**Measured, and would fail the Phase 2 review as written.** Its ask — "needs to be reviewed and
likely strengthened" — is an order to investigate, not a stated property of the finished system, so
rule 4 rejects it. It is kept here as the measured artifact, not as a model to copy.

```
## Ticket 8 — Improve refundable-transaction selection for repeat and partial refunds

The logic that decides whether an order has a transaction eligible for refund currently just looks for a prior captured payment; it has no awareness of partial refunds or of an order being refunded more than once. As the refund feature goes live, this selection logic needs to be reviewed and likely strengthened so that repeated or partial refund attempts against the same order behave predictably and don't rely on assumptions that were never validated. This is foundational to correct refund eligibility decisions across the whole feature.
```

## 3. The same constraint as example 1, attached to a feature task — converted 2 of 5

This is what **not** to do, and it is the thing most teams reach for first. The task was
"guarantee an order can never be refunded for more than the customer paid." The constraint below
was placed in `.github/instructions/payment-refund.instructions.md`, and Copilot's own system prompt
ordered the agent to read it before changing code. Every run read it first, about three seconds in.
Three of five then built the exact defect it describes. At five runs, 2 of 5 is indeterminate and is
reported as such.

```
Role in current flow: This provider implements refund(...), but the retrieved implementation sets
  transaction.setTransactionType(TransactionType.CAPTURE); inside the refund method.
Required change: This file must be inspected and likely corrected if Stripe3Payment is used for
  refunded orders, because the retrieved refund-path transaction type appears inconsistent.
```

Accurate. Names the file, the method, the line. Did not convert, because it was information beside
the job rather than the job. The same fact as an 85 KB spec in the working tree: 1 of 5, identical to
no document at all. Scope and dilution are confounded with packaging in these measurements — 593
bytes that are entirely this constraint against 85 KB where it is about half a percent — and the
program's own reading is that dilution is probably most of the effect.

## 4. A hand-written constraint ticket for an off-path defect (provenance: person, not spec)

Written 2026-09-07 from a frozen assertion, because the generated spec did not name this hazard at
constraint level. Included to show the style applied to an invariant the code violates today, and to
show what an honest provenance note looks like: **this ticket is not spec-derived, and says so.**

```
## Ticket — Fix sales tax being calculated on the undiscounted order amount

When a promotion or discount is applied to an order, the discount is subtracted from the subtotal but the sales tax is still calculated from the original, undiscounted item prices. The customer is charged tax on money they did not pay: a 25% promotion on a $100 item at a 10% tax rate produces $10.00 of tax instead of $7.50. Correct the tax calculation so that the taxable base reflects any discount applied to the subtotal, while orders without a discount continue to be taxed exactly as they are today.
```

## The four checks, applied

| check | example 1 | example 2 | example 3 |
|---|---|---|---|
| one constraint | yes | arguably two (partial *and* repeat refunds) | yes, but riding on a different task |
| the whole ticket | yes | yes | no — attached |
| area, not site | "one payment gateway" | "the logic that decides…" | file, method, line |
| symptom → consequence → ask | yes | symptom and consequence, then an order to investigate — fails | hedged description, no ask |
