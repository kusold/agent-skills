# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

Browse the full documentation at **[skills.mikekusold.com](https://skills.mikekusold.com/)** — built from this repo with [Hugo](https://gohugo.io/) (hugo-book theme) and deployed to [Cloudflare Pages](https://pages.cloudflare.com/) on every push to `main`.

## Available Skills

- **[skill-writing](docs/skill-writing/index.md)** — Create, review, and improve agent skills with focused instructions and observable checks.
- **[vja-vikunja](docs/vja-vikunja/index.md)** — Manage Vikunja tasks from the command line using `vja`, the CLI client for the self-hosted task manager [Vikunja](https://vikunja.io).
- **[simplified-technical](docs/simplified-technical/index.md)** — Write or rewrite text in Simplified Technical English (ASD-STE100) at roughly 80% strictness: short sentences, clear verbs, active voice, and precise terminology.
- **[defuddle](docs/defuddle/index.md)** — Extract clean article content and metadata from web pages as Markdown with the defuddle CLI, checking extractions for blocked, empty, or partial results.
- **LLM Wiki** — persistent, LLM-maintained knowledge base (`skills/llm-wiki/`):
  - **[wiki-inbox-stage](docs/llm-wiki/wiki-inbox-stage/index.md)** — Stage a web source into the wiki inbox: defuddle extraction, provenance frontmatter, single-file push to the Forgejo remote via the gitea MCP.
  - **[wiki-ingest](docs/llm-wiki/wiki-ingest/index.md)** — Add sources to an LLM-maintained wiki, preserving provenance and flagging conflicting claims.
  - **[wiki-query](docs/llm-wiki/wiki-query/index.md)** — Answer questions from wiki evidence and optionally save durable analyses.
  - **[wiki-lint](docs/llm-wiki/wiki-lint/index.md)** — Check wiki links, coverage, and consistency, then apply authorized fixes.
- **Software Development** — software design and maintenance (`skills/software-development/`):
  - **[architectural-decision-records](docs/software-development/architectural-decision-records/index.md)** — Record architectural choices, evidence, and tradeoffs using MADR and project conventions.
- **Nix** — flake authoring and maintenance (`skills/languages/nix/`):
  - **[nix-flake-parts](docs/languages/nix/nix-flake-parts/index.md)** — Expert guidance for the flake-parts framework: `mkFlake`, `perSystem`, overlays, and reusable flakeModules.
  - **[nix-dendritic-flake](docs/languages/nix/nix-dendritic-flake/index.md)** — Convert flakes to the dendritic pattern where every file is a top-level module.
  - **[nix-module-options](docs/languages/nix/nix-module-options/index.md)** — Query upstream NixOS and Home Manager module options with `nix eval`.

## Installation

```bash
npx skills add kusold/agent-skills
```

Or install a specific skill:

```bash
npx skills add kusold/agent-skills --skill vja-vikunja
```

## Usage

After installation, invoke a skill by name or let your agent select it for a relevant request. Automatic discovery and activation depend on the host agent and its configuration.

## Skill Structure

```
skills/
  {skill-name}/           # the skill itself (flat, or grouped: {group}/{skill-name}/)
    SKILL.md              # Instructions for the agent
    scripts/              # Helper scripts for automation (optional)
    references/           # Supporting documentation (optional)
docs/
  {skill-name}/           # mirrors skills/ one-to-one
  {group}/_index.md       # group index (collapsible section on the docs site)
  {group}/{skill-name}/
    index.md              # extended documentation for the skill (rendered on the docs site)
```

## License

MIT
