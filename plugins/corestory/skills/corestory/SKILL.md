---
name: corestory
description: "Use CoreStory MCP for project discovery, architecture and requirements context, or help choosing a CoreStory workflow. Prefer a specialized installed CoreStory skill for bug resolution, feature work, modernization, test generation, or diligence."
license: Proprietary
---

# CoreStory Skill Reference

## Product Summary

CoreStory is a code intelligence platform that creates a persistent, queryable model of your codebase. It ingests repositories (public, private, or uploaded files) and produces an intelligence model that AI agents can query via MCP (Model Context Protocol) to understand architecture, business rules, data structures, and integration points before writing code.

**Key files and commands:**
- MCP URL: `https://app.corestory.ai/mcp/{org-slug}-{org-id}` (from Settings → IDE Integrations)
- MCP server setup: `claude mcp add --transport http corestory {MCP_URL}`
- Configuration: `.claude/config.json` (Claude Code), `~/.cursor/mcp.json` (Cursor), `.cursor/mcp.json` (per-project Cursor)
- Skill files: `.claude/skills/{skill-name}/SKILL.md` (Claude Code), `.cursor/rules/{rule-name}/RULE.md` (Cursor)
- Custom instructions: `.github/copilot-instructions.md` (GitHub Copilot)

**Primary docs:** https://docs.corestory.ai

## When to Use

Activate CoreStory when:
- **Querying code intelligence** — asking questions about architecture, patterns, business rules, data structures, or integration points
- **Implementing features** — need to understand existing patterns, find extension points, or identify reusable components before coding
- **Resolving bugs** — need architectural context to understand how the system should work before investigating what's wrong
- **Writing specifications** — grounding specs in actual architecture to prevent conflicts, duplication, and bloat
- **Generating tests** — deriving test cases from specifications and business rules
- **Modernizing codebases** — mapping dependencies, identifying service boundaries, extracting components, or migrating systems
- **Onboarding** — helping new developers understand system behavior, architecture, and patterns
- **Due diligence** — analyzing acquisition targets or evaluating technical risk

Do NOT use CoreStory for:
- Trivial changes (typos, formatting, documentation-only)
- Tasks that don't require architectural understanding
- When no CoreStory project has been ingested yet (direct the user to create an account and upload their repo first)

## Quick Reference

### MCP Tools Available

| Tool | Purpose |
|------|---------|
| `list_projects` | List all projects in your org with ingestion status |
| `get_project_prd` | Retrieve a project's Product Requirements Document |
| `get_project_techspec` | Retrieve a project's Technical Specification |
| `create_conversation` | Create a persistent conversation thread for a task |
| `send_message` | Query CoreStory's code intelligence (streaming) |
| `get_conversation` | Retrieve conversation history |
| `rename_conversation` | Rename a conversation (use to mark as resolved) |
| `semantic_search` | Search project's code index by semantic meaning |
| `describe_index` | List file paths and filterable metadata in project |
| `filter_chunks` | Fetch code chunks by metadata filter |
| `generate_document` | Start generation of a custom document |
| `get_document_generation_result` | Poll for custom document generation results |
| `refine_document_definition` | Build and validate a custom document definition |

### MCP Connection Setup by Agent

| Agent | Config File | Command |
|-------|-------------|---------|
| **Claude Code** | `~/.claude/config.json` or `.claude/config.json` | `claude mcp add --transport http corestory {URL}` |
| **Claude Desktop** | UI-based | Settings → Connectors → Add custom connector |
| **Cursor** | `~/.cursor/mcp.json` or `.cursor/mcp.json` | Edit JSON, restart Cursor |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | Use `serverUrl` (not `url`) |
| **GitHub Copilot** | VS Code MCP settings | Add via UI or settings JSON |

**Critical:** Use OAuth browser sign-in (no Authorization header). If migrating from legacy tokens, delete the old `Authorization` header entirely — it suppresses the OAuth flow.

### Core Workflow Pattern

Every CoreStory workflow follows this pattern:

1. **Select project** — `list_projects` → verify ingestion is "completed"
2. **Create conversation** — `create_conversation` with descriptive title (persists as institutional knowledge)
3. **Query Expert** — `send_message` to understand intended behavior, invariants, architecture
4. **Query Navigator** — `send_message` to find specific files, methods, extension points
5. **Act on knowledge** — implement, test, or document based on CoreStory's guidance
6. **Close loop** — `rename_conversation` to mark as resolved; commit only when the user requested a commit

### Standard Playbooks

| Playbook | When to Use | Key Phases |
|----------|-------------|-----------|
| **Bug Resolution** | Diagnose and fix bugs with architectural context | Intake → Expert → Navigator → TDD → Completion |
| **Feature Implementation** | Build new features following existing patterns | Intake → Expert → Navigator → TDD → Completion |
| **Spec-Driven Development** | Write grounded specs before implementation | Ground → Specify → Validate → Plan → Implement → Verify |
| **Test Generation** | Derive tests from specifications and business rules | Extract rules → Generate tests → Verify coverage |
| **Code Modernization** | Modernize legacy systems systematically | Assess → Inventory → Target → Decompose → Execute → Verify |
| **M&A Due Diligence** | Evaluate acquisition targets for risk and debt | Architecture → Risks → Debt → Integration complexity |

## Decision Guidance

### When to Use Expert vs Navigator Queries

| Situation | Use Expert | Use Navigator |
|-----------|-----------|---------------|
| "How should this work?" | ✓ | |
| "What invariants must hold?" | ✓ | |
| "What patterns does the system follow?" | ✓ | |
| "Where is this implemented?" | | ✓ |
| "What files do I need to modify?" | | ✓ |
| "What base class should I extend?" | | ✓ |
| "What's the design history?" | ✓ | |
| "What could go wrong?" | ✓ | |

**Rule:** Always query Expert before Navigator. Understand the system before planning implementation.

### When to Use Semantic Search vs Filter Chunks

| Scenario | Use Semantic Search | Use Filter Chunks |
|----------|-------------------|-------------------|
| "Find code related to payment processing" | ✓ | |
| "Find all files in the /api/v2 directory" | | ✓ |
| "What handles user authentication?" | ✓ | |
| "List all test files for the auth module" | | ✓ |
| "Find similar patterns to this code" | ✓ | |
| "Get all files with tag 'deprecated'" | | ✓ |

**Rule:** Semantic search is slower but finds conceptual matches. Filter chunks is fast for structural queries.

### When to Request Sections vs Full Documents

| Document | Approach |
|----------|----------|
| **PRD/TechSpec < 50KB** | Request full document with `get_project_prd` or `get_project_techspec` |
| **PRD/TechSpec > 50KB** | Call `describe_index` first to list sections, then request only needed sections |
| **Custom documents** | Use `refine_document_definition` to validate, then `generate_document` to create |
| **Large generation** | Submit `generate_document`, then poll `get_document_generation_result` |

## Workflow

### Typical Task Execution

1. **Verify CoreStory connection**
   - Ask agent: "List my CoreStory projects"
   - Confirm at least one project shows status "completed"
   - If no projects or connection fails, check MCP configuration and restart agent

2. **Create a persistent conversation**
   - Call `create_conversation` with descriptive title (e.g., "Bug Investigation: #1234 — Payment retry failing")
   - Store the `conversation_id` for all subsequent queries
   - This conversation becomes searchable institutional knowledge

3. **Query for understanding (Expert phase)**
   - Ask CoreStory about architecture, patterns, invariants, business rules
   - Example: "What files handle payment processing? What invariants must hold for retry logic?"
   - Wait for complete response before proceeding

4. **Query for location (Navigator phase)**
   - Ask CoreStory where to implement, what to reuse, what extension points exist
   - Example: "Where should I add retry logic? What base class should I extend?"
   - Get specific file paths and method names

5. **Implement or investigate**
   - Write tests first (for bugs and features)
   - Follow patterns CoreStory identified
   - Validate implementation against CoreStory's architectural guidance

6. **Mark conversation as resolved**
   - Call `rename_conversation` with prefix like "✅ RESOLVED:" or "COMPLETED —"
   - This signals the conversation is complete and available for future reference

### Example: Bug Investigation Workflow

```
1. Fetch bug ticket (via ticketing MCP or user description)
2. list_projects → select project, verify ingestion complete
3. create_conversation "Bug Investigation: #6992 — reset_index coord_names issue"
4. send_message "What files implement reset_index? What invariants must hold?"
5. send_message "If _coord_names retains stale entries after drop=True, what code paths should I investigate?"
6. Write failing test that reproduces the bug
7. send_message "Does this test correctly validate expected behavior?"
8. Read implementation code, identify root cause
9. send_message "I found [code snippet]. Does this violate the invariant?"
10. Implement minimal fix, verify test passes
11. send_message "Does this fix align with architecture? Side effects?"
12. Add edge case tests, run full suite
13. If the user requested a commit, commit with a detailed message explaining root cause; otherwise leave the verified change uncommitted
14. rename_conversation "✅ RESOLVED: Bug Investigation: #6992 — reset_index coord_names cleanup"
```

## Common Gotchas

- **Skipping Expert phase.** Jumping straight to Navigator (finding files) without understanding how the system should work leads to architectural misalignment. Always query for understanding first.

- **Requesting full large documents.** PRDs and TechSpecs over 50KB will timeout. Use `describe_index` to list sections, then request only what you need.

- **Stale Authorization headers.** If migrating from legacy tokens, leaving the old `Authorization` header in config suppresses the OAuth browser sign-in. Delete it entirely.

- **Windsurf uses `serverUrl`, not `url`.** This is a common typo that silently fails to connect.

- **Assuming project is ready without checking status.** Always verify ingestion is "completed" before querying. Incomplete ingestion returns stale or partial data.

- **Creating new conversations for every query.** Reuse conversations for related queries. The conversation accumulates context that improves subsequent responses and reduces token usage.

- **Not validating tests with CoreStory.** Writing tests without checking them against CoreStory's understanding of expected behavior often produces tests that pass but don't validate the right thing.

- **Implementing without test-first.** The playbooks require failing tests before implementation code. Skipping this step increases regressions and architectural misalignment.

- **Ignoring invariants.** Invariants are non-negotiable constraints. Violating them causes subtle bugs that surface under production load. Always extract and test invariants explicitly.

- **Forgetting to rename conversations.** Leaving conversations unnamed makes them hard to find later. Rename with a status prefix ("✅ RESOLVED:", "COMPLETED —") so future engineers can find institutional knowledge.

- **Querying without specificity.** Vague queries like "Tell me about the order system" produce vague answers. Be specific: "What is the validation logic for order placement? What fields are required? What are the business rules for minimum amounts?"

- **Not checking for existing functionality.** Before designing new features, ask CoreStory what already exists. Teams often discover 40% of a feature's spec describes functionality that's already implemented.

## Verification Checklist

Before submitting work that used CoreStory:

- [ ] MCP connection verified (agent can list projects)
- [ ] CoreStory conversation created with descriptive title
- [ ] Expert phase completed (understand intended behavior, invariants, architecture)
- [ ] Navigator phase completed (specific files, methods, extension points identified)
- [ ] Tests written BEFORE implementation code
- [ ] Tests validated with CoreStory (correct coverage, follows patterns)
- [ ] Implementation follows patterns CoreStory identified
- [ ] Implementation validated with CoreStory (architectural alignment, side effects)
- [ ] Full test suite passes (no regressions)
- [ ] If committed, the commit message includes the CoreStory conversation ID
- [ ] CoreStory conversation renamed to mark as resolved
- [ ] Invariants from Phase 1 are explicitly tested and passing

## Resources

**Comprehensive navigation:** https://docs.corestory.ai/llms.txt

**Critical documentation pages:**
- [MCP Server Setup](https://docs.corestory.ai/getting-started/mcp-server-setup) — connection configuration for all agents
- [Supercharging AI Agents](https://docs.corestory.ai/getting-started/supercharging-ai-agents) — how to use CoreStory with agents, troubleshooting
- [Playbooks Index](https://docs.corestory.ai/playbooks/index) — all available workflows (bug resolution, feature implementation, spec-driven development, modernization, testing)

---

> For additional documentation and navigation, see: https://docs.corestory.ai/llms.txt
