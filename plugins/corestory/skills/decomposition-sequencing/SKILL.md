---
name: decomposition-sequencing
description: "Decompose an approved modernization plan into dependency-aware work packages with CoreStory. Use for migration sequencing, waves, work packages, sprint planning, or executable modernization backlogs."
license: Proprietary
---

# CoreStory Decomposition & Sequencing

When this skill activates, guide the user through the six-step workflow to produce sequenced work packages for modernization execution.

## Activation Triggers

Activate when user requests:
- Migration decomposition or work package creation
- Migration sequencing or ordering
- Sprint planning for modernization
- Pushing modernization work to Jira or Linear
- Any request containing "decompose", "sequence", "work packages", "migration plan", "migration order"

## Prerequisites

- Completed Target Architecture decision (Phase 3) with ADR
- CoreStory MCP server configured with completed ingestion
- (Optional) Jira or Linear MCP for ticketing integration

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Input Loading
1. Identify target project (`list_projects`)
2. Locate prior conversations (`list_conversations`) — assessment + architecture
3. Retrieve ADR and dependency analysis (`get_conversation`)
4. Create conversation: "[Decomposition] SystemName - Migration Planning"

## Step 2: Component Decomposition
- Identify migration units (smallest independently-deployable sets)
- Map shared data stores that force components to migrate together
- Define work package boundaries (included, excluded, temporary integration)
- Validate each can be deployed independently

## Step 3: Dependency Mapping
- Map hard dependencies (must complete before), soft dependencies (easier if done first)
- Map shared data dependencies and ownership
- Identify infrastructure prerequisites (API gateway, event bus, CI/CD)
- Identify the critical path

## Step 4: Sequencing
- Order by dependency chain, risk, business value, team capacity
- Identify quick wins for the first sprint
- Identify parallel execution opportunities
- Analyze risk concentration per sequence position

## Step 5: Work Package Definition
For each work package, define:
- Transform: delta spec scope, target patterns, files, test strategy
- Coexist: façade approach, data sync, rollback plan, verification criteria
- Eliminate: legacy decommission, façade removal, final verification
- Acceptance criteria: functional, behavioral, performance, integration, operational

## Step 6: Ticketing System Integration
After the engineering lead approves the sequence, use Jira or Linear only if the user explicitly requests the external write:
- Create the migration epic
- Create stories per work package with Transform/Coexist/Eliminate sub-tasks
- Link dependencies between work packages
Otherwise, output the same structure for review or manual import.

**HITL Gate: Engineering lead approves the sequence. Approval of the sequence is not authorization to push it to a ticketing system; require an explicit request for that external write.**

## Error Handling
- **ADR not found:** Direct user to complete Target Architecture first
- **Components can't be separated:** Define as a cluster migration unit
- **Too many dependencies:** Look for infrastructure prerequisites that unblock multiple packages
- **Jira/Linear MCP not available:** Output structured work package definitions for manual import
