---
title: 'Home'
description: 'A collection of skills for AI coding agents, following the Agent Skills format.'
---

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities, following the [Agent Skills](https://agentskills.io/) format.

## Available Skills

- [Simplified Technical English](/docs/simplified-technical/) — write or rewrite text in Simplified Technical English (ASD-STE100) at roughly 80% strictness
- [Vja — Vikunja CLI Task Manager](/docs/vja-vikunja/) — manage Vikunja tasks from the command line
- [Wiki Ingest](/docs/wiki-ingest/) — add sources to an LLM-maintained wiki, preserving provenance and flagging conflicts
- [Wiki Query](/docs/wiki-query/) — answer questions from wiki evidence and optionally save durable analyses
- [Wiki Lint](/docs/wiki-lint/) — check wiki links, coverage, and consistency, then apply authorized fixes

## Installation

```bash
npx skills add kusold/agent-skills
```

Or install a specific skill:

```bash
npx skills add kusold/agent-skills --skill vja-vikunja
```

After installation, invoke a skill by name or let your agent select it for a relevant request. Automatic discovery and activation depend on the host agent and its configuration.

Each guide links to its skill's full agent instructions (`SKILL.md`), which are also rendered on this site.
