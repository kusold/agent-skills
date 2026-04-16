# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### vja-vikunja

Manage Vikunja tasks from the command line using `vja`, the CLI client for [Vikunja](https://vikunja.io) (self-hosted task manager). Supports full task lifecycle: add, list, edit, delete, defer, and filter by project, label, priority, due date, or urgency.

**Use when:**
- "Add a task"
- "List my tasks"
- "Mark task 5 as done"
- "Show my urgent tasks"
- "What's due this week"
- "Edit task priority"
- "Create a project"

**Commands covered:**
- Task management: add, list, edit, delete, check, clone, defer
- Filtering: by project, label, priority, due date, urgency
- Projects, labels, and kanban buckets
- Opening tasks in the browser

## Installation

```bash
npx skills add kusold/agent-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Add a task "Fix the login bug" with priority 3 due tomorrow
```
```
List my urgent tasks
```
```
Mark task 42 as done
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
