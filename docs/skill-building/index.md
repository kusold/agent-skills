---
title: 'Skill Building'
description: 'Build and improve portable Agent Skills from concrete workflows, then validate their structure and behavior.'
weight: 90
---

Turn a repeatable workflow into an installable Agent Skill, or improve an existing skill after a failure. The agent inspects your repository, identifies the decisions worth preserving, writes the skill and useful supporting files, and reports what it validated.

## Installation

```bash
npx skills add kusold/agent-skills --skill skill-building
```

Invoke it by name or describe a skill-authoring task. Automatic selection depends on the host agent and configuration.

## Example requests

```text
Create a skill for reconciling invoice and payment CSVs. Match on invoice ID,
report duplicate IDs and unmatched payments, and never overwrite the inputs.
Put it in skills/csv-reconciliation/.
```

```text
Turn the release-note workflow from this conversation into a skill. Preserve
our changelog conventions and draft the notes locally.
```

```text
Improve skills/incident-review/SKILL.md. It activates for ordinary code reviews
and assumes our monitoring connector is always connected.
```

Include known inputs, output examples, tools, and failure cases when available. The skill uses repository context to fill routine gaps.

## What it produces

A skill folder with `SKILL.md` and any resources justified by the workflow. Detailed instructions can live in bundled references; repeatable operations can use scripts; deliverable templates can live in assets. It also follows the destination repository's documentation conventions. Here, that means a matching docs page and README catalog entry.

The runtime skill stays inside its own folder so installation does not depend on this documentation site. Host-specific metadata is optional, and integration prerequisites must be explicit.

## Validation

Structural validation checks the package format and links. Behavioral validation checks selection and execution against realistic requests. A clean format check alone does not establish that a skill activates correctly or produces useful results.

For example, a CSV reconciliation skill should handle an ordinary invoice request and a paraphrase, avoid activation for an unrelated CSV chart, and produce the expected unmatched records from a small fixture. A missing invoice-ID column should produce a useful diagnostic. Those are proposed acceptance cases; run them against the resulting skill before recording them as passed.

The authoring agent reports completed checks separately from trials that require an unavailable host, model, or service. Installation, publishing, and external writes follow the user's requested scope.

## Workflow reference

See [the complete skill instructions](../../skills/skill-building/SKILL.md).

## Sources and design

The portable package follows the [Agent Skills overview](https://agentskills.io/home) and [format specification](https://agentskills.io/specification). The entrypoint carries the shared workflow, with resources loaded only when needed.

Repository discovery and installation examples follow [Vercel's creating-skills guide](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md). This repository uses `skills/<name>/SKILL.md`; a separate plugin manifest is unnecessary for that layout.

Concise instructions, selective references, and task-appropriate specificity draw on [Anthropic's authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). Claude-specific requirements should be checked for a Claude target rather than imposed on every host.

Concrete use cases and the distinction between trigger, functional, and baseline tests draw on [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en), especially its planning and testing chapters. Its example metrics are starting points for evaluation, not universal release thresholds.
