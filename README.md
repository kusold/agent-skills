# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

- **[vja-vikunja](docs/vja-vikunja/)** — Manage Vikunja tasks from the command line using `vja`, the CLI client for the self-hosted task manager [Vikunja](https://vikunja.io).

## Installation

```bash
npx skills add kusold/agent-skills
```

Or install a specific skill:

```bash
npx skills add kusold/agent-skills --skill vja-vikunja
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

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
