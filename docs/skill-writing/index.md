---
title: 'Skill Writing'
description: 'Create and improve agent skills with focused instructions, progressive context, and observable checks.'
weight: 90
---

Create a new agent skill, review an existing skill, or improve its clarity, context use, behavior, or fit to changed requirements. The workflow covers both discovery through the frontmatter description and execution through the instructions and supporting resources.

## Usage

Install this skill from the repository:

```bash
npx skills add kusold/agent-skills --skill skill-writing
```

Example requests:

```text
Write a skill for our release process using the examples in this repository.
```

```text
Improve this skill: it activates for ordinary documentation edits,
but it should apply only to API migration guides.
```

```text
Review skills/example/SKILL.md for unclear decisions and missing resources.
Report findings without changing files.
```

The agent reads local conventions and available evidence, identifies the intended outcome, and creates or revises the package. A review request produces findings; a request to improve the skill includes making the relevant edits. Existing working behavior and unrelated metadata are preserved.

## What makes a useful skill

The skill applies these design criteria:

- **Precise discovery:** the name and description identify the actual capability and distinguish nearby requests. Different names alone do not resolve overlap with installed skills.
- **Useful decisions:** instructions supply specialized guidance instead of repeating generic advice.
- **Progressive context:** essential decisions stay in `SKILL.md`; conditional detail is linked and loaded when needed.
- **Portable packaging:** executable guidance travels with the skill, with external dependencies stated explicitly.
- **Appropriate constraints:** fixed steps protect real invariants, while routine choices remain adaptable.
- **Observable outcomes:** checks examine selection, artifacts, and effects, with regression cases for changes.
- **Maintainability:** improvements address a stated objective, including demonstrated failures, clarity, brevity, or changed requirements.

These are design criteria, not a numerical quality rubric. A format validator can detect structural errors but cannot prove that an agent will select or execute a skill correctly. Validation reports distinguish inspection, walkthroughs, and actual agent trials.

## Packaging and Codex support

The entrypoint keeps shared authoring decisions independent of a particular host and routes format rules and package examples to the bundled specification. An optional [Codex reference](../../skills/skill-writing/references/codex.md) covers default installation paths, naming limits, `agents/openai.yaml`, invocation policy, and bundled initialization, metadata generation, and validation tools. It also explains how to proceed when those helpers are unavailable.

The reference is loaded only for Codex-specific work. Its commands use tools from the target installation; this package does not include copies of Codex's authoring scripts. Existing YAML settings are edited in place when regenerating the file would discard unrelated policy or dependencies.

## Agent Skills references

The [format reference](../../skills/skill-writing/references/agent-skills.md) records portable requirements and links to official authoring guides, reviewed on 2026-10-22. It distinguishes the standard from host-specific extensions and validator limitations. The [script checklist](../../skills/skill-writing/references/scripts.md) applies when adding executable helpers.

The full [specification snapshot](../../skills/skill-writing/references/specification.md) is bundled for offline checks of exact rules and examples. It was extracted with Defuddle 0.19.5 and checked against the site's native Markdown on 2026-10-22. The file records its source, CC BY 4.0 attribution, and conversion changes. It loads only when detailed format guidance is needed; the short checklist remains the normal entry point. Refresh instructions in the format reference require reviewing the conversion before replacing the snapshot.

The official documentation informed additional guidance on grounding skills in actual project knowledge, choosing useful defaults, separating discovery from outcome checks, reviewing execution traces, and evaluating against a baseline. Sources: [best practices](https://agentskills.io/skill-creation/best-practices), [descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), [evaluation](https://agentskills.io/skill-creation/evaluating-skills), and [scripts](https://agentskills.io/skill-creation/using-scripts).

The [specification](https://agentskills.io/specification) is the format authority; local helpers can lag behind it. For example, the inspected Codex validator rejects the standard `compatibility` field. Such disagreements should be reported rather than resolved by silently discarding valid metadata.

## Research basis and limits

This skill was informed by a wiki-query pass over the author's `llm-wiki` on 2026-10-22, beginning with `wiki/index.md` and following the relevant concepts to source summaries and archived raw text. The wiki had no dedicated skill-authoring source or behavioral evaluation evidence at that time.

The following evidence informed the design:

| Wiki evidence | Supported idea | Application to this skill |
| --- | --- | --- |
| `wiki/sources/openwiki.md`, verified against `raw/OpenWiki Open Source Repo Documentation for Coding Agents.md` | Short instruction files point agents to detailed context consulted when needed. The announcement also describes Git-diff-driven maintenance. | **Inference:** keep a small entrypoint, link conditional references, and review skills when their underlying context changes. |
| `wiki/concepts/simplified-technical-english.md` and `wiki/sources/karpathy-on-understanding-llm-outputs.md`, verified against `raw/karpathy-on-understanding-llm-outputs.md` | Karpathy reports that constrained prose helps him read LLM outputs; the wiki identifies this as personal experience, not measured compliance or effectiveness. | **Inference:** use direct, precise prose for instructions without requiring formal ASD-STE100 compliance. |

The archived originals are [OpenWiki's release announcement](https://www.langchain.com/blog/introducing-openwiki-an-open-source-agent-for-repo-documentation) and [Karpathy's post on understanding LLM outputs](https://x.com/karpathy/status/2105819303471976479?lang=en). This research used the local snapshots; it did not verify the live pages.

Discovery boundaries, portable packaging, scoped improvements, and behavioral checks also draw on the bundled `skill-creator` guidance consulted during authoring and this repository's packaging conventions. They are implementation choices here, not findings established by the wiki. The wiki remains unchanged, and using this skill does not require access to it or to another authoring skill.

## Full instructions

See [the skill definition](../../skills/skill-writing/SKILL.md) and its [evaluation reference](../../skills/skill-writing/references/evaluation.md). The evaluation reference provides representative cases and a result-recording template; it does not require a particular test framework or delegation tool.
