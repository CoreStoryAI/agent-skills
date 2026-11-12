---
name: using-corestory
license: MIT
description: "Use a local CoreStory knowledge graph to answer codebase questions with source-backed evidence. Use when CoreStory local tools are available and a task involves understanding, tracing, planning, or citing code."
---

# Using CoreStory locally

CoreStory exposes a read-only knowledge graph for the ingested codebase in the current workspace.
Use the tools and parameters advertised by this connection.
Available capabilities depend on the local build, configuration, and captured data.

Start with corpus metadata when needed.
Search for the behavior, concept, or symbol under investigation.
Follow returned entity IDs and relationships to refine the result.
Read enough surrounding source to verify a claim before relying on it or changing code.

Cite paths and locations that the tools returned or that source reading verified.
Treat derived findings as leads, not as proof.
The captured snapshot can differ from the current working tree.

Follow pagination when a result is incomplete.
An empty result or tool error does not prove that a rule or behavior does not exist.
Report the limit and use the tool's next-step guidance rather than inventing missing facts.
