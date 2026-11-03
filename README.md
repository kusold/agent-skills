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

## Counting skill tokens

Run the token counter with [uv](https://docs.astral.sh/uv/), which installs its
pinned `tiktoken` dependency in an isolated environment:

```bash
uv run scripts/count_skill_tokens.py
uv run scripts/count_skill_tokens.py --include-supporting
uv run scripts/count_skill_tokens.py --encoding cl100k_base --json
uv run scripts/count_skill_tokens.py --include-supporting --markdown
```

By default, the tool recursively finds each `SKILL.md` beneath `skills/`, including
grouped skills such as `skills/languages/nix/nix-flake-parts/SKILL.md`, and counts its
complete text, including YAML frontmatter and whitespace, with the `o200k_base`
encoding. Use `--skills-dir PATH`
to scan another collection. The default path works from any working directory.

`--include-supporting` also counts UTF-8 text files recursively within each skill,
including reference documents and scripts. It excludes hidden files/directories
and `__pycache__`, reports skipped binary or non-UTF-8 files, and rejects symlinked
files. Totals sum the counts of individual files; docs outside `skills/` are excluded.
Reports identify skills by their path relative to `skills/`. Nested skill packages
are counted separately rather than included in a parent skill's supporting files.
JSON output includes a per-file breakdown.

The **Skill token counts** GitHub Actions workflow runs on relevant pull requests,
pushes to `main`, and manual dispatch. Its run summary contains a Markdown table
with each skill's `SKILL.md`, supporting-file, and total token counts, plus overall
totals. It uses `o200k_base` and includes supporting text files.

These are source-text counts for the selected tokenizer, not measured context
usage or API billing. Hosts may load only metadata during discovery and load
instructions or references later. Other model families can use different
tokenizers. Counting runs locally without an API key; the first run needs network
access to download dependencies and tokenizer data.

Run the counter's regression tests with:

```bash
uv run --with tiktoken==0.12.0 python -m unittest discover -s scripts
```

## License

MIT
