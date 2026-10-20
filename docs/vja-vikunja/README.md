# vja-vikunja

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

## Usage

The skill activates automatically when the agent detects a relevant task request.

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

## Full Command Reference

See [skills/vja-vikunja/SKILL.md](../../skills/vja-vikunja/SKILL.md) for the complete `vja` command reference (adding, listing, filtering, editing, deferring, projects, labels, buckets, urgency, and common workflows) that the agent loads when this skill is active.
