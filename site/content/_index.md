---
title: 'Home'
description: 'A collection of skills for AI coding agents, following the Agent Skills format.'
---

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities, following the [Agent Skills](https://agentskills.io/) format.

## Available Skills

<!-- Generated from docs/{skill}/index.md front matter by the skill-list shortcode. -->
{{< skill-list >}}

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
