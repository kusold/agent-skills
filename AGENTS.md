# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

A collection of agent skills following the [Agent Skills](https://agentskills.io/) format. Installed via `npx skills add`.

## Creating a New Skill

### Directory Structure

```
skills/
  {skill-name}/           # kebab-case directory name
    SKILL.md              # Required: skill definition with YAML frontmatter
docs/
  {skill-name}/           # mirrors skills/ — one directory per skill
```

Every skill in `skills/{skill-name}/` has a corresponding `docs/{skill-name}/` directory for extended documentation (design notes, usage guides, etc.). When adding a new skill, create both directories; keep the names in sync.

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {One sentence describing when to use this skill. Include trigger phrases.}
---

# {Skill Title}

{Instructions for the agent to follow when this skill is activated.}
```

### Required Fields

- `name`: Unique identifier (lowercase, hyphens allowed)
- `description`: Brief explanation of what the skill does and when to use it

### Best Practices

- Keep SKILL.md concise — it loads into the agent's context when activated
- Include clear trigger phrases in the description so the agent knows when to use the skill
- Prefer concrete command examples over abstract descriptions
- Reference supporting docs only when needed (progressive disclosure)

### Installation

Users install skills from this repo with:

```bash
npx skills add kusold/agent-skills
```

Or install a specific skill:

```bash
npx skills add kusold/agent-skills --skill vja-vikunja
```
