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
  {skill-name}/
    index.md              # mirrors skills/ — one directory per skill
```

Every skill in `skills/{skill-name}/` has a corresponding `docs/{skill-name}/` directory for extended documentation (design notes, usage guides, etc.). When adding a new skill, create both directories; keep the names in sync.

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

The Hugo site (hugo-book theme) lives in `site/` and is published to Cloudflare Pages at <https://kusold-agent-skills.pages.dev/>. `site/hugo.toml` mounts `../docs` and `../skills` as site content, so skill guides and `SKILL.md` references render from the repo as-is — nothing is copied into `site/` except the landing page (`site/content/_index.md`) and the theme submodule. The landing page's "Available Skills" list and the site sidebar are both generated from the docs pages' front matter, so a new skill appears on the site automatically once `docs/{skill-name}/index.md` exists.

- Local preview: run `hugo server` from the `site/` directory (requires Hugo extended ≥ 0.158; on NixOS: `cd site && nix-shell -p hugo --run 'hugo server'`). Build from inside `site/` — invoking `hugo -s site` from the repo root writes some outputs to a stray root-level `public/`. Clone with `--recursive` to get the theme submodule (`site/themes/hugo-book`).
- Theming: colors are the Rosé Pine palette (auto light/dark), set in `site/assets/styles/custom.css` — hugo-book's supported override hook, which shadows the theme's stub. It depends on the explicit `assets` mount in `site/hugo.toml` (declaring mounts discards Hugo's default mounts). `site/layouts/_partials/docs/html-head.html` shadows the theme partial solely to set the `theme-color` metas; re-sync it from the theme if the submodule is updated.
- Skill links: `site/layouts/_partials/docs/links/portable-link.html` shadows the theme partial so relative links to `skills/{name}/SKILL.md` from docs pages render as the GitHub blob view (`BookRepo` + `/blob/main/`) instead of the mounted content page; on GitHub the relative links work as-is. Re-sync from the theme on submodule updates.
- Deploy: pushing to `main` (or opening a PR) runs `.github/workflows/deploy-docs.yml`, which builds with Hugo and deploys to Cloudflare Pages via `wrangler-action` (project `kusold-agent-skills`; PRs get `<branch>.kusold-agent-skills.pages.dev` previews). The workflow needs the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repo secrets.
- Known-benign build warnings: the portable-link warning for `docs/wiki-lint/index.md`'s link to `check_wiki.py` (a static file, not a content page — the link works) and the theme's own `.Page.IsNode` deprecation notice.
