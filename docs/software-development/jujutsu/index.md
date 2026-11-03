---
title: 'Jujutsu'
description: 'Use Jujutsu exclusively in .jj workspaces with a describe-first, atomic-commit workflow.'
weight: 20
---

Use Jujutsu (`jj`) whenever a VCS operation targets a workspace with `.jj` in the current directory or an ancestor. This includes workspaces that also contain `.git`. The skill requires Jujutsu for status, diffs, history, and commit operations, and prevents a fallback to Git if `jj` is missing.

## Install and use

```bash
npx skills add kusold/agent-skills --skill jujutsu
```

Example requests in a Jujutsu workspace:

```text
Fix the parser bug and keep the change in a focused commit.
```

```text
Review the current diff and separate unrelated documentation changes.
```

```text
Fold this fixup into the earlier change that introduced the affected lines.
```

The description supports automatic selection for VCS operations in `.jj` workspaces. Actual discovery depends on the host agent and its configuration. The skill requires the `jj` CLI; it does not initialize or migrate repositories.

## Describe first, then code

Start with `jj st`. Reuse `@` only when it is empty and undescribed; otherwise run `jj new` and check again. Describe the intended change with a Conventional Commit message before editing:

```bash
jj describe -m "fix(parser): handle empty quoted fields"
```

Keep one logical change per commit. Related implementation, tests, and docs can stay together. Start and describe another revision before beginning a separate change.

## Refine before finishing

Review with `jj --no-pager show @` or `jj --no-pager diff --git`. Check atomicity, message clarity, unrelated changes, and whether fixups belong in another commit.

- Use `jj split -m "docs: clarify setup" <paths>` to separate selected files, or interactive splitting for hunks within a file.
- Use `jj squash --into <change-id>` to move changes to a chosen commit.
- Use `jj absorb` to distribute eligible fixups among mutable ancestors, then inspect the result.

Use change IDs to target revisions across rewrites. Review all affected commits after restructuring and run the relevant project checks. Jujutsu snapshots working-copy changes automatically, so this workflow uses commits directly without staging or stashing.

The `--git` diff format and Jujutsu's `jj git` remote subcommands are Jujutsu operations and are allowed. Running the Git executable or a tool that invokes it is prohibited in these workspaces.

## Review scenarios

These cases define the intended behavior for future agent trials; they do not claim measured automatic activation:

| Situation | Expected behavior |
| --- | --- |
| VCS request from a nested directory with `.jj` at the workspace root | Detect ancestor marker and use only `jj`. |
| Both `.jj` and `.git` exist | Use only `jj`, including for read-only operations. |
| Empty, undescribed revision | Run `jj st`, describe the change, then edit. |
| Existing changes or an existing description | Run `jj new`, verify blank status, then describe before editing. |
| Unrelated file changes mixed into the task commit | Split selected paths and review both descriptions and patches. |
| Fixups belong to an earlier change | Inspect destination, squash or absorb, and review affected change IDs. |
| `.jj` exists but `jj` is missing | Report the missing CLI; do not fall back to Git. |
| Git-only repository without `.jj` | Leave VCS selection to the repository's conventions. |

## Full instructions

See the [skill definition](../../../skills/software-development/jujutsu/SKILL.md) for the complete workflow and the [official Jujutsu CLI reference](https://www.jj-vcs.dev/latest/cli-reference/) for command details. The installed skill is self-contained and does not require this documentation page.
