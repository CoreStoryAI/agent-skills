---
name: ma-technical-due-diligence
description: "Perform technical due diligence on an acquisition target using CoreStory code intelligence. Use for M&A diligence, acquisition review, architecture and code quality assessment, risk, scalability, security, or integration analysis."
license: Proprietary
---

# CoreStory M&A Due Diligence

When this skill activates, execute the four-phase due diligence workflow.

## Activation Triggers

Activate when user requests:
- Due diligence or diligence audit
- Technical assessment
- M&A review or acquisition review
- Any request containing "due diligence", "diligence audit", "technical assessment", "M&A review", "acquisition review"

## Prerequisites

- CoreStory MCP server configured
- At least one CoreStory project with completed ingestion (the target codebase)
- Read access to the target's repository for cross-referencing findings

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Phase 1: Project Setup & Orientation

1. **Identify the Target Project**
   ```
   Use CoreStory MCP: list_projects
   ```
   - Multiple projects → ask user which one is the acquisition target
   - Single project → confirm with user before proceeding
   - Verify ingestion is complete

2. **Retrieve Synthesized Specifications**
   ```
   Use CoreStory MCP: get_project_techspec
   Use CoreStory MCP: get_project_prd
   ```
   - Summarize: system architecture, technology stack, external integrations, data model overview
   - This establishes the architectural vocabulary for all subsequent queries

3. **Create Diligence Conversation**
   ```
   Use CoreStory MCP: create_conversation
   Title: "[Diligence] TargetName - Technical Risk Audit"
   ```
   Store conversation_id for all subsequent queries.

**Report:**
```
🔍 Starting M&A technical due diligence
Target: [project name]
Architecture: [high-level summary]
Tech Stack: [languages, frameworks, infrastructure]
CoreStory conversation: [conversation-id]
```

## Phase 2: Risk Interrogation

Use `send_message` to interrogate the codebase across risk domains. Ask specific, evidence-oriented questions — always request file paths.

**Technical Debt & Obsolescence:**
- "List all services, modules, and frameworks running on end-of-life or unsupported versions. For each, provide current version, latest stable version, and upgrade complexity."
- "Identify high-complexity modules with poor separation of concerns — god classes, circular dependencies, excessive coupling. Provide file paths."

**Security & Secrets:**
- "Identify all code locations that hardcode API keys, passwords, tokens, or other secrets. For each, provide the file path and line context."
- "Map the authentication flow from login through session management. Identify whether it follows standard patterns or uses custom logic."
- "List all known CVEs from third-party libraries, sorted by severity."

**Licensing & Open Source Risk:**
- "Provide a complete bill of materials for all third-party dependencies. Flag any with GPL, AGPL, SSPL, or other copyleft licenses."
- "Are there any dependencies that are abandoned, archived, or have known unpatched vulnerabilities?"

**PII & Data Handling:**
- "Map data flows where PII is collected, transmitted, and stored. For each stage, state whether encryption is applied at rest and in transit."
- "Identify all database models containing PII fields. For each, list fields, encryption status, and access controls."
- "How is data deletion handled? Is there a right-to-be-forgotten implementation? Identify where PII might persist after deletion."

**Architecture & Integration Complexity:**
- "Map all external integrations, showing third-party dependencies, API touchpoints, and data flows."
- "What message queues, event buses, or async patterns are used? Identify single points of failure."
- "Describe the deployment architecture, CI/CD pipeline, and any cloud vendor lock-in."

## Phase 3: Cross-Reference & Validation

For critical findings — security issues, licensing risks, PII exposure:
1. Open each file path CoreStory identified and confirm the finding against source code
2. Check if findings reflect current state (CoreStory's analysis is based on ingestion snapshot)
3. Assess severity: production secrets vs. test placeholders, actual GPL usage vs. dev-only dependencies
4. Note any discrepancies between CoreStory findings and source code

## Phase 4: Synthesis & Reporting

1. **Compile Structured Report**
   Review conversation history and synthesize into:
   - Executive Summary — top 3-5 findings affecting deal risk or valuation
   - Critical Risks — security vulnerabilities, licensing exposure, PII compliance gaps (with file-level evidence and severity)
   - Technical Debt — end-of-life dependencies, architectural issues, maintainability concerns
   - Architecture Overview — component map, technology stack, external dependencies
   - Integration Assessment — complexity of merging with acquirer's platform
   - Recommendations — remediation priorities and estimated effort

2. **Mark Completed**
   ```
   Use CoreStory MCP: rename_conversation
   New title: "RESOLVED - [Diligence] TargetName - Technical Risk Audit"
   ```

## Error Handling

- **Project not found:** List available projects, ask user to specify the target
- **CoreStory gives generic answers:** Narrow queries — use specific service names, module names, and technology names from the Tech Spec
- **Response too long:** Break into smaller risk-domain queries
- **Findings don't match source:** Note ingestion date, request re-ingestion if target codebase has changed significantly
