# Codex packaging and authoring helpers

Read this reference when creating or updating a skill for Codex. These details reflect the bundled `skill-creator` inspected on 2026-10-22; consult the target installation's instructions and helper usage before relying on them if interfaces differ. This skill does not bundle those helpers or require them on other hosts.

## Location and naming

Honor explicit paths and repository conventions first. Otherwise use `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Create a user-owned skill rather than modifying bundled system skills unless that is explicitly requested.

Use lowercase letters, digits, and hyphens; avoid leading, trailing, or consecutive hyphens. Keep the name under 64 characters and match the directory name.

## UI metadata and invocation

`agents/openai.yaml` supplies optional Codex UI metadata, tool dependencies, and invocation policy. A skill does not need invented branding or dependencies. When those settings are needed, read the installed `skill-creator/references/openai_yaml.md` for the supported schema. If unavailable, consult the target host's official documentation rather than guessing fields.

For example, when UI metadata is appropriate:

```yaml
interface:
  display_name: "API Migration"
  short_description: "Write actionable API migration guides"
  default_prompt: "Use $api-migration to draft an API migration guide."
```

Quote string values. Keep the short description between 25 and 64 characters and mention `$skill-name` in a supplied default prompt.

Automatic selection is enabled by default. Set the following only when the user requests explicit-only invocation:

```yaml
policy:
  allow_implicit_invocation: false
```

Sensitive operations alone do not justify disabling discovery; handle authorization at the operation. Preserve existing invocation policy and unrelated `interface`, `policy`, and `dependencies` fields when editing.

## Optional bundled tools

Locate the installed `skill-creator` directory. A common location is:

```bash
skill_creator_dir="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator"
```

Verify that the files exist and inspect their `--help` or instructions before using them. The commands below assume that location and the documented interfaces are available; choose the output path from the task's conventions. They are authoring examples, not commands to execute merely because this reference was loaded.

For a new skill in a repository with a `skills/` directory:

```bash
python3 "$skill_creator_dir/scripts/init_skill.py" api-migration --path ./skills
```

Initialize only new skills. The initializer creates `SKILL.md` and `agents/openai.yaml`; request optional resources with `--resources references` only when needed. Replace scaffolding and remove unused generated files before finishing.

To generate UI metadata when needed:

```bash
python3 "$skill_creator_dir/scripts/generate_openai_yaml.py" ./skills/api-migration \
  --interface 'display_name=API Migration' \
  --interface 'short_description=Write actionable API migration guides'
```

The metadata generator replaces the entire YAML file. If an existing file has policy, dependencies, or unrelated settings to preserve, edit the intended fields in place instead.

Validate a completed package:

```bash
python3 "$skill_creator_dir/scripts/quick_validate.py" ./skills/api-migration
```

The inspected validator requires PyYAML. If the environment lacks it, use an available isolated dependency environment; for example, when `uv` is installed:

```bash
uv run --no-project --with pyyaml python \
  "$skill_creator_dir/scripts/quick_validate.py" ./skills/api-migration
```

The inspected Codex validator does not accept the standard `compatibility` field. Treat that as a validator compatibility limitation; do not remove valid environment requirements merely to obtain a pass. Check against the Agent Skills specification as well when the target package uses that field.

If the helpers are unavailable, create the minimal package directly and inspect naming, YAML, resource links, and unfinished scaffolding. Report the checks actually performed. Format validation does not establish activation quality or correct workflow behavior; select behavioral checks using [evaluation.md](evaluation.md).
