---
name: jujutsu
description: Use Jujutsu (jj) for any version-control operation when .jj exists in the current directory or an ancestor, including status, diff, log, commits, and history edits; in these workspaces use only jj, never Git, and follow a describe-first, atomic-commit workflow.
---

# Jujutsu

## Select the VCS before running commands

Before any VCS operation, inspect the current directory and its ancestors for `.jj` using filesystem tools. If present, use **only Jujutsu** for VCS operations, even if `.git` is also present. Do not run Git commands or tools that invoke Git on your behalf. `jj --no-pager diff --git` is allowed: `--git` selects a diff format. Jujutsu's own `jj git` subcommands are also allowed when needed for Git remotes.

If `.jj` is absent, this workflow does not apply; follow the repository's VCS conventions. If `.jj` is present but `jj` is unavailable, report the missing prerequisite instead of falling back to Git.

## Start on a blank revision; describe before coding

Before writing code or other task changes:

1. Run `jj st`. Inspect both the working-copy changes and the description of `@` (the working-copy revision). A blank revision has no changes relative to its parents and no description; an absence of uncommitted changes is not the relevant test because Jujutsu records working-copy changes automatically.
2. If `@` already contains changes or has a description, run `jj new` to preserve it and start a fresh revision. Run `jj st` again to verify the new revision is blank. Do not edit, discard, or absorb pre-existing work as part of starting a new task.
3. **Describe first, then code.** Set the intended commit message before editing files:

   ```bash
   jj describe -m "feat(parser): support quoted field names"
   ```

Use Conventional Commits: `type(optional-scope): imperative summary`, such as `fix(auth): reject expired tokens` or `docs: clarify setup`. Refine the description as the work evolves so it describes the final change.

Each commit must represent **one logical change**. Implementation, focused tests, and documentation for that change can belong together. Before starting another logical change, run `jj new`, verify with `jj st`, and describe the new commit before editing.

## Refine commits before finishing

Commits are mutable. Always review and refine them before considering the work done:

```bash
jj --no-pager show @
# Or inspect the patch alone:
jj --no-pager diff --git
```

Check:

- **Atomicity:** Does each commit contain one logical change?
- **Message:** Does the Conventional Commit description clearly explain the final change?
- **Scope:** Are unrelated changes mixed in? Split them into a separate commit:

  ```bash
  jj split -m "docs: clarify setup" <paths>
  ```

  Replace `<paths>` with the files to separate. The selected changes receive that message; review both resulting commits and fix the remaining description with `jj describe` as needed. For mixed changes within a file, use `jj split --interactive` to select hunks.

- **Placement:** Should a change be part of another commit? Use `jj squash --into <change-id>` for a chosen destination, optionally limiting it to paths. Use `jj absorb` for fixups whose destination can be inferred from mutable ancestors. Inspect the intended destinations first; do not fold unrelated or pre-existing work into them.

Use **change IDs** when targeting revisions: they stay stable across ordinary rewrites, unlike commit hashes. Use `jj --no-pager log` to find them. After splitting, squashing, or absorbing, inspect the log and review every affected commit with `jj --no-pager show <change-id>`; `@` may now refer to a different revision. Check for conflicts and run the relevant project checks on the final result.

## Work with commits directly

There is no staging area and no need to stash. Working-copy edits belong to `@` and are snapshotted automatically by Jujutsu commands. Use `jj new` to begin separate work and refine commits with split, squash, and absorb. Finish with `jj st` and report the relevant change IDs, descriptions, and validation results.
