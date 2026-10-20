# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

- **[vja-vikunja](docs/vja-vikunja/)** — Manage Vikunja tasks from the command line using `vja`, the CLI client for the self-hosted task manager [Vikunja](https://vikunja.io).
- **[simplified-technical](docs/simplified-technical/)** — Write or rewrite text in Simplified Technical English (ASD-STE100) at roughly 80% strictness: short sentences, clear verbs, active voice, and precise terminology.
- **[wiki-ingest](docs/wiki-ingest/)** — Add sources to an LLM-maintained wiki, preserving provenance and flagging conflicting claims.
- **[wiki-query](docs/wiki-query/)** — Answer questions from wiki evidence and optionally save durable analyses.
- **[wiki-lint](docs/wiki-lint/)** — Check wiki links, coverage, and consistency, then apply authorized fixes.

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
  {skill-name}/           # the skill itself
    SKILL.md              # Instructions for the agent
    scripts/              # Helper scripts for automation (optional)
    references/           # Supporting documentation (optional)
docs/
  {skill-name}/           # extended documentation for the skill
```

## License

MIT
