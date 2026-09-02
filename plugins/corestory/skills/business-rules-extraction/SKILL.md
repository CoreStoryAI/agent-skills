---
name: business-rules-extraction
description: "Extract, document, and source-verify business rules with CoreStory. Use for business-logic inventories, validation and authorization rules, state transitions, invariants, acceptance-criteria mapping, or implicit-rule discovery."
license: Proprietary
---

# Business Rules Extraction Skill

When the user asks to extract or document business rules, follow this workflow:

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Phase 1: Setup
1. Call `list_projects` to find the target project
2. Call `create_conversation` with title "Business Rules Extraction — <scope>"
3. Confirm extraction scope with the user (single module, domain, or full system)

## Phase 2: Architectural Survey
1. Query CoreStory: "Where is business logic implemented in this codebase?
   Give me a map of which architectural layers enforce which types of rules."
2. Query CoreStory: "Based on the PRD and requirements for this project,
   what are the explicitly documented business rules? List them grouped
   by feature area or domain."
3. Query CoreStory: "List the user stories and their acceptance criteria,
   grouped by feature area. For each AC, note any associated business rules
   and the implementation evidence (file:line). Flag ACs that appear
   undocumented in code."
4. Query CoreStory: "Based on the technical specification, what are the
   key data model constraints — required fields, unique constraints, valid
   states, and relationships between entities?"
5. Query CoreStory: "What are the major categories of business rules in
   this system? Group by domain."

NOTE: Do NOT call `get_project_prd` or `get_project_techspec` and try to
read them in full — they are typically too large for context. Query
CoreStory about their contents via `send_message` instead.

## Phase 3: Deep Extraction
For each domain identified in Phase 2, run these query patterns:
- "What validation rules exist for [entity/module]?"
- "What authorization rules govern [feature area]?"
- "What state transitions exist for [entity]?"
- "What calculation/pricing rules exist for [domain]?"
- "List the user stories for [domain] and their acceptance criteria.
  Map each AC to the BR(s) that implement it, or flag as unmapped."
- "What invariants must hold for [entity]? Categorize as data-integrity,
  state-machine, referential, security, or temporal."
- "What implicit rules exist in [module] that aren't documented?"
- "Show me the exact code path for [critical workflow]."

IMPORTANT: Use specific entity/module names in every query. Broad
questions produce shallow answers. Capture both BRs AND their associated
ACs — they are sibling artifacts and downstream consumers (TDD,
behavioral verification) need both.

## Phase 4A: Code Verification
For each extracted rule, verify in local source code:
- Search for model/entity constraint declarations (annotations, schema
  definitions, validation rules — patterns vary by stack)
- Read service implementations for conditional business logic
- Check security/auth configs for authorization rules
- Look for rules CoreStory missed (config files, test assertions,
  frontend-only validation, third-party integrations)

## Phase 4B: Enforcement Verification
For every rule tagged Constraint, Validation, or Authorization, answer
three questions:

1. **Where is the enforcement point?** Not where the value is declared,
   but where the check is performed that rejects invalid input or blocks
   unauthorized access. If no enforcement point exists, downgrade the
   rule to "Declared but not enforced."

2. **What happens when the constraint is violated?** Exception? Error
   response? Silent ignore? If nothing happens, downgrade or correct.

3. **Is the scope accurately described?** Universal vs. conditional vs.
   presentation-only? Code-level vs. config-level vs. convention-level?

Use this CoreStory query pattern for each high-priority rule:
"For rule [BR-ID], which states [description], verify enforcement. Do
NOT confirm based on existence of fields or method signatures. Instead:
(1) find the line that rejects invalid input, (2) trace the execution
path to confirm it's reached, (3) describe what happens on violation.
If no enforcement point exists, say so explicitly."

Produce a verification matrix with columns: BR-ID, Claim Type,
Enforcement Point, Violation Behavior, Scope, Level, Status.

Watch for these anti-patterns:
- Dead fields (set but never read)
- Buggy validation (wrong variable compared)
- Setter-only constraints (no server-side enforcement)
- Inaction misread as enforcement (value was already set from init)
- Scope inflation (UI-only constraint reported as universal)

## Phase 4C: Flow-Trace Discovery
Find behaviors that domain extraction missed by tracing user flows:

1. Query CoreStory for all user-facing entry points (HTTP endpoints,
   form handlers, admin ops, scheduled jobs, message listeners).

2. For each critical flow, trace end-to-end:
   "Trace the complete execution path for [user action] from [entry
   point] through to all database writes, message sends, and response
   outputs. For each step: what data enters, what the code does, what
   comes out. Flag cases where: (a) user input is ignored/overwritten,
   (b) method behavior differs from its name, (c) errors are silently
   swallowed."

3. Compare traces against draft inventory: confirm matches, flag
   contradictions, add new rules with BR-IDs.

Watch for these anti-patterns:
- Input ignored (form accepts data, handler discards it)
- Overwrite vs. accumulate (add/append method actually replaces)
- Silent failures (caught and swallowed errors)
- Stub/test data in production paths (hardcoded overrides)

## Phase 5: Documentation
Produce the business rules inventory using the BR-XXX template format.
Include for each rule:
- Claim type, enforcement point, enforcement level, discovery method
- Confidence: Confirmed (verified via 4B), Corrected (revised via 4B),
  or New (discovered via 4C)
Include Appendix A (Declared But Not Enforced) and Appendix B
(Flow-Trace Evidence).

## Phase 6: Capture
Rename conversation with "RESOLVED — Business Rules Extraction — <scope>"

Key principle: specific queries beat broad queries. Always name the exact
module, entity, or workflow you're asking about.
