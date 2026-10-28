---
title: 'Architectural Decision Records'
description: 'Create and maintain evidence-based ADRs using MADR and project conventions.'
weight: 10
---

Record a consequential software design choice so future maintainers can understand the constraints, alternatives, and tradeoffs behind it. The skill creates and updates ADRs, reviews existing records, and connects superseded decisions to their replacements.

## Install and use

```bash
npx skills add kusold/agent-skills --skill architectural-decision-records
```

Example requests:

```text
Write an ADR for our decision to keep PostgreSQL instead of adding a search service.
Use the tradeoffs in this issue and the existing decision log.
```

```text
Document why this service uses asynchronous events. The implementation exists,
but we do not have the original discussion notes.
```

```text
Draft a proposal to replace ADR-0003. Keep the existing decision active until
the replacement is accepted.
```

```text
Review our ADR for missing information without editing it.
```

The skill follows the repository's existing log, template, and status conventions. For a new log, it starts with MADR under `docs/decisions/`, numbered filenames, and a small index. It writes a proposal when acceptance is unknown and labels reconstructed rationale when documenting an existing implementation.

## Templates and clarification

The bundled lightweight template is based on [MADR's minimal template](https://github.com/adr/madr/blob/develop/template/adr-template-minimal.md): context, considered options, decision outcome, and consequences. It supports multiple genuine alternatives. Use the full starter when detailed drivers, option comparisons, or confirmation criteria help explain the choice. Both templates share the same metadata and lifecycle rules.

Both templates contain only the body. The agent prepends the [shared front matter](../../../skills/software-development/architectural-decision-records/assets/adr-frontmatter.md), which is the single definition of field defaults and examples, then fills in the resulting record. Changing templates does not change its metadata.

The agent investigates repository facts before asking questions. It groups independent questions about intent or tradeoffs, recommends answers where useful, and preserves consequential clarifications in the record. Unresolved choices can remain explicit in a proposal; an exhaustive interview is not required.

Diagrams are encouraged when they clarify boundaries, interactions, data flow, or changes to the design. Either template can include a Mermaid diagram. A diagram generator is optional, and a record that is clearer in prose does not need a diagram.

## Relationship metadata

The default MADR convention supports three optional fields:

```yaml
supersedes: [ADR-0003]
extends: [ADR-0008]
related: [ADR-0010]
```

`supersedes` declares replacement, `extends` adds to a decision that remains active, and `related` identifies useful context. Include only applicable fields, always as lists. In the default log, `ADR-0003` identifies the record whose filename starts with `0003-`. References across logs use repository-relative paths when needed to avoid ambiguity. Existing project syntax takes precedence.

Targets must exist. Replacement and extension chains must not contain cycles or self-references. Body links explain the relationship and keep the history readable without tooling. Only forward metadata is authored; incoming relationships can be discovered with ordinary file search. Inverse metadata such as `superseded-by` is not required or introduced by this convention.

The skill works from local files and bundled resources using ordinary file search; no search engine or graph service is required.

## Research and format choice

The MADR sources were reviewed on 2026-10-28:

| Source | Finding | Application |
| --- | --- | --- |
| [MADR development template](https://github.com/adr/madr/blob/develop/template/adr-template.md) | Separates context, alternatives, and outcome, with optional detail. | Provides the basis for the bundled starter. |
| [MADR repository](https://github.com/adr/madr) | Hosts templates, examples, and version history. | Distinguish development material from published versions. |
| [MADR guide](https://adr.github.io/madr/) | Describes keeping decisions alongside documentation and permits project-specific organization. | Preserve local conventions; use its numbered decision-log layout as the fallback. |

The skill uses MADR's flexible structure while preserving existing repository conventions. Shared status and date defaults, relationship metadata, and lifecycle transitions are conventions chosen for this skill. The full starter includes MADR's optional Confirmation section for describing how implementation can be checked.

## History and evidence

The shared front matter defines the allowed statuses and their meanings once for both templates. Existing project lifecycle rules take precedence when they differ.

The workflow preserves the rationale of accepted records. A changed choice gets a successor with `supersedes` metadata and a body link to its predecessor. The predecessor stays active while the successor is proposed or rejected. Acceptance of the successor marks the predecessor superseded and adds a body link back to the successor. Extension and association do not change status. Deprecation without replacement does not require a successor. This is a workflow policy chosen for this skill.

An implementation can show what the code does without establishing historical consensus or rationale. The skill distinguishes these facts, leaves substantive unknowns visible, and never invents participants, approval, measurements, or completed audits. Writing an ADR does not implement the architecture it describes.

## Evaluation cases

Use these cases for future agent trials; they are acceptance criteria, not claims of measured performance:

| Case | Expected outcome |
| --- | --- |
| New project with an explicitly accepted decision | Numbered MADR record and index; supported rationale and tradeoffs; accepted status. |
| Existing unnumbered log with a local template | Existing paths and template retained; no parallel log or renumbering. |
| Concise choice with two genuine alternatives | Lightweight MADR can retain both options; no forced single-option format. |
| Complex comparison | Full starter retains the drivers and substantive comparison needed to understand the choice. |
| Unknown fact available in the repository | Agent investigates and cites it instead of asking the user. |
| Uncertain intent or tradeoff | Focused question with a recommendation; supported proposal can retain open questions. |
| Component interaction clarified by a diagram | Evidence-grounded diagram added to either template; otherwise omitted. |
| Relationship to an existing decision | Applicable list metadata, valid target, and explanatory body link. |
| Self-reference, missing target, or cyclic replacement/extension | Invalid relationship identified and corrected or left unresolved; no invented target. |
| Cross-log reference | Unambiguous path or existing repository convention used. |
| Retrospective record from code alone | Observed implementation separated from unknown history; no invented approval. |
| Unresolved architectural choice | Proposed record with open questions; no claimed acceptance. |
| Proposed replacement of an accepted ADR | Successor links to predecessor; predecessor remains active. |
| Accepted replacement | Old rationale retained; status and reciprocal links updated. |
| Extension or rejected replacement | Existing decision status remains unchanged. |
| Search/graph service unavailable | Ordinary file search remains sufficient; record creation can proceed. |
| Review-only request | Findings reported; files unchanged. |
| Ordinary release-note request | ADR workflow does not divert the task. |

## Full instructions

See the [skill definition](../../../skills/software-development/architectural-decision-records/SKILL.md), [full starter](../../../skills/software-development/architectural-decision-records/assets/adr-template.md), and [lightweight template](../../../skills/software-development/architectural-decision-records/assets/adr-template-minimal.md). Runtime guidance, shared front matter, and both body templates travel with the installed skill; this documentation page is not required at runtime.
