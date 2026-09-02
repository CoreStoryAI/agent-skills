# Security

## What installs

This repository contains declarative Agent Skills and plugin manifests. The CoreStory plugin has no hooks and runs no local executable code. Its only declared remote service is the HTTPS MCP endpoint in `plugins/corestory/.mcp.json`.

## Authentication and data access

CoreStory MCP authentication uses OAuth. Never add access tokens, API keys, organization secrets, or customer source code to this repository. Access through the MCP server is limited by the permissions of the signed-in CoreStory user.

Agent skills are instructions, not a security boundary. Review a skill before installation, keep normal repository protections enabled, and require human review for consequential code or external-system changes.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through the security-reporting option on the relevant repository in the [CoreStory GitHub organization](https://github.com/corestoryai). Do not open a public issue containing exploit details, credentials, or customer data.
