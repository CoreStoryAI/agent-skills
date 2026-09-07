---
name: feature-gap-analysis
description: "Run a CoreStory-grounded feature gap analysis to identify existing capabilities, missing pieces, affected files, dependencies, risks, and implementation order before building a feature."
license: MIT
---

# Feature Gap Analysis with CoreStory

When this skill activates, execute the four-phase gap analysis workflow.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Activation Triggers

Activate when user requests:
- Gap analysis or pre-implementation analysis
- Implementation surface area assessment
- "What needs to change to build [feature]?"
- Any request containing "gap analysis", "what's missing", "what needs to change"

## Prerequisites

- CoreStory MCP server configured
- At least one CoreStory project with completed ingestion
- Feature specification available (PRD, user story, or design doc)

## Phase 1: Context Loading

1. **Select CoreStory Project**
   ```
   Use CoreStory MCP: list_projects
   ```
   - Multiple projects → ask user which one
   - Single project → auto-select
   - Verify status is "completed"

2. **Create Gap Analysis Conversation**
   ```
   Use CoreStory MCP: create_conversation
   Title: "Gap Analysis: [Feature Name]"
   ```
   Store conversation_id for all subsequent queries.

3. **Load Architectural Context**
   ```
   Use CoreStory MCP: get_project_prd
   Use CoreStory MCP: get_project_techspec
   ```
   If either document is too large, use `send_message` to query specific sections.

4. **Orient CoreStory to the Feature**
   ```
   I'm preparing to implement a new feature and need to understand how it
   interacts with the existing codebase. Here is the feature specification:

   [Paste or summarize the feature specification]

   Before we begin the gap analysis, confirm:
   1. Which major subsystems or modules are most relevant to this feature?
   2. Are there existing features with similar patterns I should be aware of?
   3. What are the primary architectural patterns in this codebase?
   ```

**Report:**
```
Starting gap analysis for [Feature Name]
Project: [project name]
CoreStory conversation: [conversation-id]
Relevant subsystems: [list from CoreStory response]
Similar existing features: [list from CoreStory response]
```

## Phase 2: Gap Identification

**Send the seven-category gap analysis query:**
```
I need to implement the following feature in the existing codebase:

[Feature specification]

Provide a detailed gap analysis across these categories:

1. EXISTING CAPABILITIES: What parts are already supported? What can be reused as-is?
2. DATA MODEL GAPS: New fields, tables, enums, or structures to add? Existing structures to modify?
3. UI GAPS: New screens, forms, or components to create? Existing UI to modify?
4. BUSINESS LOGIC GAPS: New validation rules, calculations, or logic to implement? Existing logic to extend?
5. RENDERING/OUTPUT GAPS: New rendering or output logic needed? Existing rendering to update?
6. INTEGRATION GAPS: Existing integration points (APIs, events, workflows) to update?
7. CONSTRAINT GAPS: New constraints or validation rules? How do they interact with existing constraints?

For each gap, identify specific files that need to change and describe the change at a
level of detail sufficient for a developer to implement it.
```

**Drill into sparse categories:**
```
The [CATEGORY] section seems sparse. Look more carefully at:
- [Specific area of concern]
- Indirect dependencies or downstream effects in this category
- Files that might not be obviously related but would need changes
```

**Identify cross-cutting concerns:**
```
Are there cross-cutting concerns that span multiple gap categories? For example:
- A data model change that cascades to UI, validation, and API layers
- A constraint that affects both business logic and rendering
- An integration change requiring coordinated updates across subsystems

List these and the full chain of files affected.
```

**Report:** Summarize gap counts per category, highlight any sparse categories investigated.

## Phase 3: Validation & Completeness

**Completeness check:**
```
Review this gap analysis for completeness:
- Are there any files or components I'm missing?
- Are there any downstream effects that aren't captured?
- Are there any existing patterns that the gap analysis contradicts?
- What is the recommended implementation order?
```

**Pattern conflict check:**
```
For each proposed change in the gap analysis, does it follow the existing
architectural patterns in the codebase? Flag any changes that would introduce
inconsistencies or require pattern exceptions.
```

**Scope summary:**
```
Based on the validated gap analysis, provide a scope summary:
- Total number of files to create vs. modify
- Highest-risk changes (most dependencies, most complex logic)
- Any gaps that could be deferred to a later iteration without blocking the core feature
```

## Phase 4: Implementation Planning

**Generate the plan:**
```
Produce a dependency-ordered implementation plan. Group changes:
1. Data Model changes (foundations everything else depends on)
2. Business Logic changes (rules and calculations)
3. UI changes (components and screens)
4. Rendering/Output changes (visual output and reports)
5. Integration changes (APIs, events, external systems)

For each group, list:
- Specific files to create or modify
- The change required
- Which existing patterns to follow
- What tests should validate the change
- Dependencies on other groups
```

**Label the conversation:**
```
Use CoreStory MCP: rename_conversation
Title: "Gap Analysis: [Feature Name] — Complete"
```

**Report:** Present the full gap analysis report using this structure:
```
# Feature Gap Analysis: [Feature Name]

## Executive Summary
[2-3 sentences: what the feature does, gap count, key risks]

## Gaps by Category
For each category, use gap IDs (DM-001, UI-001, BL-001, RO-001, IG-001, CG-001):
- Gap ID, description, files affected, priority
- Current state vs. required state
- Dependencies on other gaps

## Cross-Cutting Concerns
[Gaps spanning multiple categories with full dependency chains]

## Scope Summary
- Files to create: [count]
- Files to modify: [count]
- Highest-risk changes: [list]
- Deferrable items: [list]

## Implementation Plan
Ordered: Data Model → Business Logic → UI → Rendering → Integration
Per step: file, change, pattern to follow, tests, dependencies
```

## Error Handling

- **Project not found:** List available projects, ask user to specify
- **PRD/TechSpec too large:** Use `send_message` to query specific sections instead of loading full documents
- **Sparse category results:** Drill in with targeted follow-up; some categories legitimately have no gaps
- **CoreStory response is vague:** Provide more specific feature requirements — concrete fields, screens, rules
- **Conflicting recommendations:** Ask CoreStory to identify the dominant pattern and recommend which to follow
- **Too many gaps:** Break the feature into sub-features and run separate analyses

## When NOT to Use

- Entirely greenfield features with no existing codebase interaction
- Pure business rules extraction (use `business-rules-extraction` instead)
- User is past analysis and ready to implement (use `implement-feature` instead)
- No CoreStory project available
