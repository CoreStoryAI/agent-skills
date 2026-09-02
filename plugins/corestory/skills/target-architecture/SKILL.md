---
name: target-architecture
description: "Define and compare modernization strategies, target architecture, risk, and effort with CoreStory. Use for 7-R strategy selection, target-state design, migration-pattern decisions, or architecture decision records."
license: Proprietary
---

# CoreStory Target Architecture & Strategy

When this skill activates, guide the user through the five-step workflow to produce an Architectural Decision Record (ADR).

## Activation Triggers

Activate when user requests:
- Modernization strategy selection or architecture decision
- Target architecture definition for modernization
- Migration pattern evaluation or comparison
- Any request containing "target architecture", "migration strategy", "modernization pattern", "7 Rs", "architecture decision"

## Prerequisites

- Completed Codebase Assessment (Phase 1) with Modernization Readiness Report
- CoreStory MCP server configured with completed ingestion
- The human decision-maker should be driving this phase

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Input Review
1. Identify target project (`list_projects`)
2. Locate assessment conversation (`list_conversations`)
3. Retrieve assessment findings (`get_conversation`)
4. Summarize: readiness scores, coupling hotspots, shared data deps, blockers
5. Create conversation: "[Architecture] SystemName - Strategy & Target Architecture"

## Step 2: Strategy Exploration
Query CoreStory to explore the option space:
- "Which components are natural candidates for service extraction?"
- "Which components have lowest coupling and could be modernized independently?"
- "Which components are so tightly coupled they must be modernized together?"
- "For each component, evaluate feasibility of all seven strategies: Retire, Retain, Rehost, Relocate, Replatform, Refactor/Re-architect, Repurchase"
- "What deployment model changes would [target pattern] require?"

**Present options with trade-offs. Do NOT converge on a single recommendation.**

## Step 3: Target Architecture Definition
- "If we extract [component], what integration points and shared data must be decoupled?"
- "What existing patterns should carry forward to the target architecture?"
- "Where does the current architecture align with [target] and where are the biggest gaps?"
- Address data architecture: shared DBs to split, FK relationships crossing boundaries, data sync
- Address cross-cutting concerns: auth, logging, config, error handling

## Step 4: Risk & Effort Estimation
- Per-component effort estimate (current → target, effort, risks, dependencies)
- Top migration risks with mitigations (data, integration, performance, org, compliance, rollback)
- Alternative architectures with trade-offs

**HITL Gate: Present analysis to architect/tech lead for the architectural decision.**

## Step 5: Decision Documentation
- Generate Architectural Decision Record (ADR):
  Current State | Selected Strategy | Target Architecture | Migration Scope |
  Constraints | Risks & Mitigations | Alternatives Considered | Approval
- Rename conversation: "RESOLVED - [Architecture] SystemName - Strategy & Target Architecture"

## Error Handling
- **Assessment not found:** Direct user to complete Codebase Assessment first
- **Too many options, no clarity:** Focus on the highest-value, lowest-coupling component first
- **Stakeholders disagree:** Document competing alternatives with trade-offs for each
- **Data decomposition unclear:** Ask targeted questions about shared table access patterns
