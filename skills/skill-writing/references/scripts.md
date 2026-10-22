# Executable helpers

Use an existing tool for a simple operation; bundle repeated or fragile logic. This checklist adapts the official [script guidance](https://agentskills.io/skill-creation/using-scripts), reviewed on 2026-10-22.

- Declare runtime and package requirements; constrain dependency versions for reproducibility.
- Resolve bundled script paths from the installed skill root, independently of the user's working directory.
- Accept flags, environment variables, or stdin; avoid blocking prompts.
- Provide concise `--help`, actionable errors, and documented exit codes.
- Separate machine-readable stdout from stderr diagnostics when downstream parsing matters.
- Define retry behavior; use idempotency or preview support where repeated or stateful operations need it.
- Exercise a representative input and a meaningful failure; verify artifacts and effects as well as exit status.

These checks complement the workflow's actual invariants. Add safeguards in proportion to the operation rather than imposing confirmation flags on every helper.
