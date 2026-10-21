---
name: skill-building
description: Creates and improves Agent Skills with scoped workflows, discoverable descriptions, supporting resources, and validation; use for "create a skill", "build a skill", "turn this workflow into a skill", or "improve this SKILL.md".
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Skill Building

Build a reusable skill from a demonstrated workflow or a concrete task. Deliver working files in the user's repository or requested skill directory. For an existing skill, inspect its resources and callers before changing its structure.

## Define the job

Read the project's agent instructions and nearby skills. Infer the destination and conventions from that context; ask only for missing information that changes the result.

Identify representative requests, required inputs, expected artifacts, dependencies, and observable success criteria. Include a nearby request that should not activate the skill. Start with one coherent capability; split unrelated workflows when they need different triggers or context.

Use the user's examples and supplied sources to capture decisions the agent would otherwise miss. Verify version-sensitive commands against authoritative documentation. Preserve the user's chosen tools and scope; a skill does not grant permission to publish, send messages, or change external systems.

## Write the entrypoint

Create `<skill-name>/SKILL.md` with YAML frontmatter and Markdown instructions. Follow the [Agent Skills specification](https://agentskills.io/specification):

- `name`: 1–64 lowercase ASCII letters, digits, and hyphens; match the directory name; no leading, trailing, or consecutive hyphens.
- `description`: a nonempty string of at most 1,024 characters describing the capability and when it applies. Include natural request phrases; add exclusions only to prevent likely misrouting.
- Add optional fields only when useful. Keep `metadata` values as strings. Record actual environment requirements in `compatibility`; host-specific tool permissions are not portable guarantees.

For example, adapt this frontmatter to the actual capability:

```yaml
---
name: csv-reconciliation
description: Reconciles invoice and payment CSV files and reports unmatched records; use for "reconcile these invoices" or "find missing payments".
---
```

Write direct instructions covering inputs, consequential decisions, actions, expected outputs, and verification. Use concrete commands or input/output examples where they resolve ambiguity. Explain recovery for known failures; identify when a missing prerequisite prevents completion.

Assume the agent knows general programming and writing. Spend context on domain rules, local conventions, and non-obvious failure modes. Use flexible guidance for judgment calls and exact sequences for fragile operations. Keep the entrypoint comfortably below 500 lines; this is a ceiling, not a target.

## Package only useful resources

The installed skill must carry what its workflow needs:

- `references/`: conditional details such as schemas or provider procedures. Link directly from `SKILL.md` and state when each file should be read.
- `scripts/`: repeated or fragile deterministic operations. Document dependencies, invocation, inputs, and outputs; run each added or changed script with representative data.
- `assets/`: templates or files copied into the deliverable.

Resolve bundled paths from the skill directory, independently of the user's working directory. Do not require sibling repository docs at runtime: installers may copy only the skill folder. Avoid empty resource directories and unfinished scaffolding.

Keep host-specific settings separate from the portable core. Confirm tools exist before prescribing their names or argument shapes; document prerequisites or a useful fallback for unavailable integrations.

Follow repository packaging requirements. In this repository, also create `docs/<skill-name>/index.md` with `title`, `description`, and `weight` frontmatter, no body H1, and a relative link to the skill. Add the skill to the root README catalog.

## Validate and improve

Check frontmatter, matching folder/name, bundled links, and required documentation. If available, run the specification's reference validator:

```bash
skills-ref validate ./skills/<skill-name>
```

Substitute the actual destination. If the validator is unavailable, report the structural checks performed rather than claiming it passed.

Try representative requests in the intended host when available: an obvious trigger, a paraphrase, a nearby non-trigger, and a functional task with inspectable output. Exercise a relevant failure path, such as a missing input. Keep trials in temporary fixtures and within existing authorization.

Distinguish a description review from observed automatic activation. Explicit invocation can check execution but cannot prove discovery. For substantial workflows, compare the same task with and without the skill and judge artifact correctness, user corrections, and tool failures. Test across intended hosts or models when practical; report untested environments.

Fix the demonstrated cause: adjust discovery wording for routing failures and workflow instructions or helpers for execution failures. Deliver file paths, checks run, and remaining limitations. Never present a planned evaluation as a completed one.
