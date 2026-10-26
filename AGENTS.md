# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

A collection of agent skills following the [Agent Skills](https://agentskills.io/) format. Installed via `npx skills add`.

## Creating a New Skill

### Directory Structure

```
skills/
  {skill-name}/           # kebab-case directory name (flat skills)
  {group}/{skill-name}/   # or grouped by category (e.g. languages/nix/)
    SKILL.md              # Required: skill definition with YAML frontmatter
docs/
  {skill-name}/
  {group}/{skill-name}/   # docs/ mirrors skills/ one-to-one
  {group}/_index.md       # group index page (collapsible section on the site)
```

Every skill in `skills/{skill-name}/` has a corresponding `docs/{skill-name}/` directory for extended documentation (design notes, usage guides, etc.). When adding a new skill, create both directories; keep the names in sync.

Skills may be grouped into category directories (e.g. `skills/languages/nix/`); the `docs/` tree mirrors the nesting exactly. Each `docs/` group directory gets an `_index.md` branch bundle (not `index.md` — it is a section, not a leaf bundle) with front matter:

```markdown
---
title: {Group Title}
description: {One-line summary}
weight: {order relative to sibling entries}
bookCollapseSection: true
---
```

`bookCollapseSection: true` renders the group as a collapsible section in the docs site sidebar (hugo-book). Docs pages and skill files link to each other with editor-style relative paths, so count one `../` per directory level below the repo root (from `docs/languages/nix/{skill}/index.md`, four levels deep, the skill definition is `../../../../skills/languages/nix/{skill}/SKILL.md`).

Docs pages are `index.md` (not `README.md`) because they are mounted into the Hugo site as leaf bundles (see [Documentation site](#documentation-site)). Give each one front matter for the site:

```markdown
---
title: {Skill Title}
description: {One-line summary}
weight: {10, 20, 30, ... sidebar order}
---
```

The page body has no `# H1` — the site renders the frontmatter title as the page heading. Relative links from docs pages to skill definitions (`../../skills/{skill-name}/SKILL.md`) work on both GitHub and the site.

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

## Documentation site

The Hugo site (hugo-book theme) lives in `site/` and is published to Cloudflare Pages at <https://skills.mikekusold.com/>. Skill guides and `SKILL.md` references render from the repo as-is — a new skill appears on the site automatically once its `docs/{skill-name}/index.md` exists with the front matter described above.

Site-specific guidance — local preview, theming, shadow partials, deploy — lives in [`site/AGENTS.md`](site/AGENTS.md).
