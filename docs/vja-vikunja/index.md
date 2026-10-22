---
title: 'Vja — Vikunja CLI Task Manager'
description: 'Manage Vikunja tasks from the command line using `vja`: add, list, edit, delete, defer, and filter tasks.'
weight: 20
---

Manage Vikunja tasks from the command line using `vja`, the CLI client for [Vikunja](https://vikunja.io) (self-hosted task manager). Supports full task lifecycle: add, list, edit, delete, defer, and filter by project, label, priority, due date, or urgency.

**Use when:** Vikunja or `vja` is named or already established as the task system.

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

## Compatibility and configuration

Examples were checked against `vja 6.0.3`, which requires Vikunja >= 2.5.0 and `/api/v2`. Check `vja --version` and command help for other versions. The normal configuration path is `~/.config/vja/config.rc`; `$VJA_CONFIGDIR` and `$XDG_CONFIG_HOME` can override it. `~/.vjacli/vja.rc` is a legacy fallback. See the [upstream project](https://github.com/cernst72/vja) for installation and version-specific guidance.

Priorities run from 0 (unset) through 1 (low), 2 (medium), 3 (high), 4 (urgent), and 5 (do now). Completion requests use `--done=true`; `--done=false` reopens a task. `check` toggles one task and can reopen it.

## Resolving tasks and checking changes

For title-based changes, the agent searches and checks task IDs, titles, and projects before editing. List filters for titles, projects, and labels use regular expressions. If multiple tasks fit the request, the agent asks which one.

`vja ls` excludes completed tasks by default; `--include-completed` includes them when finding a completed task or reopening it. Label edits toggle membership, so the agent checks current labels before applying an add/remove request.

After a change, the agent checks the result and reports the task ID. If a write times out or a batch partly fails, it checks the affected state before retrying to avoid duplicate tasks, repeated deferrals, or reversed label changes.

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

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
