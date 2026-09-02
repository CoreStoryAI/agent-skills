---
name: behavioral-verification
description: "Verify that a modernized component preserves approved legacy business behavior using CoreStory. Use for behavioral equivalence, regression comparison, rule-by-rule verification, or equivalence reports."
license: Proprietary
---

# CoreStory Behavioral Verification

When this skill activates, guide the user through the five-step workflow to produce a Behavioral Equivalence Report for a modernized component.

## Activation Triggers

Activate when user requests:
- Behavioral verification or equivalence checking
- Business rule verification for a modernized component
- Comparison between legacy and modernized implementations
- Verification report generation
- Any request containing "verify", "equivalence", "behavioral", "business rules preserved", "regression check"

## Prerequisites

- Completed Business Rules Inventory (Phase 2)
- Modernized component functionally complete (Transform phase done)
- CoreStory MCP server configured with completed ingestion

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Setup
1. Identify target project (`list_projects`)
2. Locate Business Rules Inventory conversation (`list_conversations`)
3. Retrieve the inventory and scope to the component under verification
4. Create conversation: "[Verification] SystemName - ComponentName"

## Step 2: Rule-by-Rule Verification
- Trace each business rule to its modernized implementation
- Compare behavioral semantics: conditions, logic, side effects, error handling, output
- Classify: Equivalent / Improved / Different / Missing
- Flag ambiguous rules for domain expert review

## Step 3: Edge Case & Invariant Testing
- Test boundary conditions: nulls, max/min values, concurrency, temporal edges
- Verify system invariants are preserved
- Identify implicit behaviors not captured in explicit rules

## Step 4: Integration Point Verification
- Compare API contracts (endpoints, formats, status codes)
- Verify data format consistency (encoding, dates, precision, nulls)
- Assess downstream consumer impact

## Step 5: Equivalence Report
- Compile rule-by-rule verification results
- Analyze behavioral differences (improvement / deviation / regression)
- Document missing rules with recommended actions
- Produce recommendation: Ready for Eliminate / Needs Remediation / Needs Review

**HITL Gate: Domain expert or engineering lead validates the report before the legacy component is retired.**

## Error Handling
- **Business Rules Inventory not found:** Direct user to complete Phase 2 first
- **Modernized code not yet complete:** Partial verification is possible but flag incomplete areas
- **Ambiguous legacy behavior:** Flag for domain expert — do not assume it's a bug
- **Rule cannot be verified statically:** Recommend runtime comparison testing

## When Static Analysis Is Insufficient

If Tier 1 (static verification) cannot establish equivalence for a rule, escalate:

- **Tier 2 (Characterization Testing):** Generate a golden master test suite. Use CoreStory to identify the input set, then run the legacy system to capture outputs.
  ```
  send_message: "What inputs should I use to create a comprehensive golden
  master for [ComponentName]? I need inputs that exercise every business rule,
  boundary condition, and error path identified in the inventory."
  ```
- **Tier 3 (Shadow Traffic):** Design a shadow traffic configuration. Use CoreStory to identify which endpoints to shadow and what comparison logic to apply.
  ```
  send_message: "Which endpoints in [ComponentName] handle the highest-risk
  business logic? What fields in the response should I compare between legacy
  and modern to detect behavioral differences?"
  ```
- **Tier 4 (Data Migration):** If applicable, generate a data reconciliation checklist.
  ```
  send_message: "What data integrity checks should I run after migrating
  [ComponentName]'s data? Include row counts, referential integrity checks,
  and validation of computed/derived fields."
  ```
