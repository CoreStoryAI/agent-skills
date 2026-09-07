---
name: codebase-assessment
description: "Assess a legacy codebase's modernization readiness with CoreStory. Use for architecture inventory, dependency and coupling analysis, technical debt, risk, readiness, or modernization assessment requests."
license: Proprietary
---

# CoreStory Codebase Assessment

When this skill activates, guide the user through the six-step assessment workflow to produce a Modernization Readiness Report.

## Activation Triggers

Activate when user requests:
- Codebase assessment or modernization assessment
- Modernization readiness evaluation
- Architecture analysis for modernization planning
- Legacy system evaluation or analysis
- Any request containing "assess", "readiness", "evaluate architecture", "modernization planning"

## Prerequisites

- CoreStory MCP server configured
- At least one CoreStory project with completed ingestion (the legacy codebase)
- Read access to the repository for cross-referencing findings

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Setup & Orientation

1. **Identify the Target Project**
   ```
   Use CoreStory MCP: list_projects
   ```
   - Multiple projects → ask user which one to assess
   - Single project → confirm with user before proceeding
   - Verify ingestion is complete

2. **Retrieve Synthesized Specifications**
   ```
   Use CoreStory MCP: get_project_techspec
   Use CoreStory MCP: get_project_prd
   ```
   - Summarize: system architecture, technology stack, external integrations, data model, deployment model
   - This establishes the architectural vocabulary for all subsequent queries

3. **Create Assessment Conversation**
   ```
   Use CoreStory MCP: create_conversation
   Title: "[Assessment] SystemName - Modernization Readiness"
   ```
   Store conversation_id for all subsequent queries.

**Report:**
```
🔍 Starting codebase assessment for modernization readiness
Target: [project name]
Architecture: [high-level summary]
Tech Stack: [languages, frameworks, infrastructure]
CoreStory conversation: [conversation-id]
```

## Step 2: Architecture Mapping

Query CoreStory to map the system's structure:
- "Provide a complete inventory of components, services, and modules with purpose, technology, and size"
- "Map all inter-service communication patterns — sync, async, shared DB access"
- "What data stores are used? Which components share them?"
- "Identify all external entry points — APIs, batch triggers, event consumers, scheduled tasks"
- For mainframe/legacy: "Identify non-code artifacts encoding business logic — JCL, copybooks, CICS, VSAM, stored procedures, configuration"

## Step 3: Dependency Analysis

- "Map internal dependency chains. Identify highest fan-in, highest fan-out, circular dependencies, hub components"
- "Which components share database tables? List all readers and writers per shared resource"
- "List all external system dependencies with data exchanged, protocol, and fallback behavior"
- "Which external integrations are most fragile? Missing retries, hardcoded URLs, tight version coupling?"

## Step 4: Tech Debt & Risk Assessment

- "Identify god classes, circular dependencies, duplicated business logic, missing abstraction layers. Provide file paths."
- "Find dead code, unused dependencies, deprecated APIs still in use"
- "Assess security: auth patterns, hardcoded secrets, PII flows, input validation, dependency CVEs"
- "Identify compliance-relevant patterns: data residency, audit logging, access control, data retention"
- "Evaluate testability: coverage, test types, isolation capability, untested critical paths"
- "Describe operational complexity: deployment, config management, monitoring, known pain points"

## Step 5: Modernization Readiness Scoring

- "Score each component on readiness (1-5) with recommended 7 Rs strategy, key blockers, and effort estimate"
- "Recommend modernization sequence based on dependencies, coupling, risk, and business value"

## Step 6: Report Generation

1. **Synthesize Report**
   Compile findings into Modernization Readiness Report:
   - Executive Summary (overall readiness, top findings)
   - Architecture Map (components, data stores, integrations)
   - Dependency Graph (coupling, shared data, external deps)
   - Tech Debt Inventory (by severity and blast radius)
   - Risk Register (security, compliance, data, operational)
   - Component Readiness Scores (per-component 7 Rs recommendation)
   - Recommended Sequence (ordered migration plan)
   - Prerequisites & Blockers

2. **Mark Completed**
   ```
   Use CoreStory MCP: rename_conversation
   New title: "RESOLVED - [Assessment] SystemName - Modernization Readiness"
   ```

**HITL Gate: Technical leadership and product/business stakeholders review the Modernization Readiness Report and make an explicit go/no-go decision. Do not proceed to Business Rules Inventory (Phase 2) or Target Architecture (Phase 3) without that approval.**

Present four decisions for the reviewers to make: go/no-go on modernization at all, confirmation of the per-component 7 Rs strategies, priority alignment against business priorities, and any organizational prerequisites (staffing, governance, budget) that must be resolved first. Recommend a domain-expert review for mainframe or legacy systems where business logic lives in non-code artifacts, and a security/compliance review if the assessment flagged compliance constraints. The assessment informs every downstream decision, so an unapproved assessment creates compounding errors.

## Error Handling

- **Project not found:** List available projects, ask user to specify the target
- **CoreStory gives generic answers:** Narrow queries — use specific service names, module names from the Tech Spec
- **Response too long:** Break into smaller domain-specific queries
- **Legacy system uses non-code artifacts:** Explicitly ask about JCL, copybooks, CICS, VSAM — CoreStory surfaces these if prompted
- **Assessment reveals system isn't ready:** This is a valid finding — flag prerequisites that must be addressed first
