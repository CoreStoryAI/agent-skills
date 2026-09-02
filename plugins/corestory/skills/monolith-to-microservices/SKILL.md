---
name: monolith-to-microservices
description: "Guide service extraction from a monolith using CoreStory and the Strangler Fig pattern. Use for service-boundary discovery, microservice extraction, database decomposition, coexistence, or cutover planning."
license: Proprietary
---

# CoreStory Monolith to Microservices

When this skill activates, guide the user through the six-step workflow to extract a service from a monolith.

## Activation Triggers

Activate when user requests:
- Service extraction from a monolith
- Service boundary identification or validation
- Database decomposition planning
- Strangler Fig implementation
- Any request containing "extract service", "microservice", "monolith", "service boundary", "decompose database"

## Prerequisites

- Completed Phases 1–4 of the modernization workflow
- CoreStory MCP server configured with completed ingestion
- Work package definition from Phase 4

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Context Loading
1. Identify target project (`list_projects`)
2. Locate prior conversations — decomposition, architecture, assessment
3. Retrieve work package details (`get_conversation`)
4. Create conversation: "[Extraction] SystemName - ServiceName (WP-XXX)"

## Step 2: Service Boundary Identification
- Map domain boundary: MOVE / SHARE / LEAVE classification
- Identify hidden coupling: direct calls, shared state, implicit deps
- Validate feasibility: can service and monolith function independently?

## Step 3: Database Decomposition Planning
- Map data dependencies: owned, read-only, shared writes
- Choose strategy: database-per-service, schema ownership, CDC, API-mediated
- Plan migration: sequence, sync during coexist, rollback

## Step 4: Façade & Communication Design
- Map all entry points into the component
- Design façade routing (API gateway / reverse proxy)
- Choose communication patterns (sync / async per interaction)
- Design anti-corruption layer

## Step 5: Service Extraction Execution
- Transform: build new service using Spec-Driven Development delta spec
- Coexist: configure façade, run both versions, monitor
- Eliminate: remove legacy code, update routing, clean up

## Step 6: Verification & Cutover
- Behavioral verification using Phase 2 inventory
- Post-elimination testing
- **HITL Gate: Engineering lead approves cutover**

## Error Handling
- **Circular dependencies:** Boundary needs adjustment, merge components or introduce event decoupling
- **Shared database can't be split:** Use schema ownership as intermediate step
- **Façade can't route cleanly:** Consider branch-by-abstraction at code level
- **Performance degradation after extraction:** Network calls replacing in-process calls — add caching, optimize APIs
