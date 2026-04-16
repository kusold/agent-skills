---
name: vja-vikunja
description: Manage Vikunja tasks using the vja CLI. Use when the user asks to "add a task", "list tasks", "show my tasks", "mark task done", "edit task", "create a project", "what's due", or any task management action with Vikunja.
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Vja - Vikunja CLI Task Manager

Manage tasks on a Vikunja server using the `vja` command-line interface. `vja` is a CLI client for [Vikunja](https://vikunja.io), the open-source self-hosted task manager.

## Prerequisites

Check if `vja` is installed and authenticated:

```bash
vja ls 2>/dev/null
```

If this fails, prompt the user to install and configure.

## Commands Reference

All task commands work as both `vja <command>` and `vja task <command>`.

### Adding Tasks

```bash
# Quick add to default project
vja add "Task title"

# Full options
vja add "Task title" \
  --note="Description text" \
  --priority=3 \
  --favorite \
  --due="tomorrow at 11:00" \
  --reminder \
  --label=@work \
  --project=1
```

Short flags: `-n` note, `-p` priority, `-f` favorite, `-d` due date, `-r` reminder, `-l` label, `-o` project

```bash
# Clone an existing task
vja clone 1 "Copy of task with this new title"
```

### Listing Tasks

```bash
# All active tasks
vja ls

# JSON output
vja ls --json

# Specific tasks by ID
vja ls 10 13 14
```

**Sorting:**

```bash
vja ls --sort=id
vja ls --sort=-id          # reverse
vja ls --sort='due_date, -priority'
```

Default sort: `'done, -urgency, due_date, -priority, project.title, title'`

**Filtering:**

```bash
vja ls --project=1                          # by project ID
vja ls -o=projec                            # project name (regex)
vja ls --base-project=myproject             # base project
vja ls --label=@work                        # exact label
vja ls -l=work                              # label (regex)
vja ls --due-date="before today"            # overdue
vja ls --due-date="ge in 0 days" --due-date="before 5 days"  # due within range
vja ls --favorite=True                      # favorites only
vja ls --priority="gt 3"                    # priority greater than 3
vja ls --title=ask                          # title matches regex
vja ls -u                                   # urgency >= 3
vja ls --urgency=8                          # urgency >= 8
```

**Advanced filters:**

```bash
vja ls --filter="created after 2 days ago"
vja ls --filter="due_date before today in 7 days"
vja ls --filter="labels contains @work"
vja ls --filter="labels ne @work"
vja ls --filter="priority gt 2"
vja ls --filter="title contains clean up"
```

Filters can be combined:

```bash
vja ls --filter="labels ne @work" --project=1 --urgent
```

### Showing a Task

```bash
vja show 1
vja show 1 --json
vja show 1 2 3
```

### Editing Tasks

```bash
# Update properties
vja edit 1 --title="new title" --due-date="friday" --priority=1 --star
vja edit 1 --no-star

# Set due date with reminder
vja edit 1 --due="in 4 days at 15:00" -r

# Toggle label (use --force to create new label)
vja edit 1 -l @work

# Mark as done
vja edit 1 --done="true"

# Shortcut to toggle done
vja check 1

# Batch edit
vja edit 1 5 8 --due="next monday 14:00"
```

### Deferring Tasks

```bash
# Defer by timedelta
vja defer 1 1d
vja defer 1 2w

# Batch defer
vja defer 1 2 3 1d
```

Moves due_date and first reminder forward by the given timedelta.

### Reminders

```bash
# Absolute time
vja edit 1 -r "next sunday at 11:00"

# Relative to due date
vja edit -r "1h before due_date"
vja edit -r "10m before due"

# Set reminder equal to due date
vja edit 1 -r

# Remove reminder
vja edit 1 -r ""
```

### Deleting Tasks

```bash
vja delete 1
vja delete 1 2 3
```

**Note:** No confirmation prompt — use carefully.

### Opening in Browser

```bash
# Open Vikunja starting page
vja open

# Open specific tasks in browser
vja open 42 43
```

### Managing Projects

```bash
# Add project
vja project add "New Project"

# Add subproject
vja project add "Subproject" -o 2
vja project add "Subproject" -o "parent-title"

# List projects
vja project ls

# Show project details
vja project show 1

# Open in browser
vja project open 1
```

### Managing Kanban Buckets

```bash
vja bucket add "Doing" --project=1
vja bucket ls --project-id=1
```

### Managing Labels

```bash
vja label add "Next action"
vja label ls
```

### Session

```bash
# Logout (removes local token)
vja logout
```

## Urgency

Tasks have an urgency score (displayed in the last column) calculated from:
- Due date proximity
- Priority
- Favorite status
- Keyword matches in project title
- Keyword matches in label titles

Weights and keywords are configurable in `~/.vjacli/vja.rc` under `[urgency_coefficients]` and `[urgency_keywords]`.

## Priority Values

| Value | Meaning |
|-------|---------|
| 1     | High    |
| 2     | Medium  |
| 3     | Low     |
| 4     | None    |
| 5     | -1 (urgent) |

## Common Workflows

### Quick task capture
```bash
vja add "Fix the login bug" -p 2 -d "tomorrow" -l @work -r
```

### Daily review
```bash
vja ls --sort='-urgency' -u
vja ls --due-date="before tomorrow"
```

### Get things done
```bash
vja check 1
vja check 2 3
```

### Reschedule
```bash
vja defer 5 2d
vja edit 8 9 --due="next monday"
```
