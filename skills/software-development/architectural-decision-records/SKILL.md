---
name: architectural-decision-records
description: Create, update, review, or supersede Architectural Decision Records (ADRs) grounded in project evidence using MADR and existing project conventions; use for "write an ADR", "record this architecture decision", "document why we chose this", or "supersede ADR-0003".
metadata:
  credits:
    skill: Markdown Architectural Decision Records (MADR)
    author: MADR contributors
    organisation: ADR GitHub organization
    url: "https://adr.github.io/madr/"
---

# Architectural Decision Records

Record one consequential design choice and the evidence behind it. Capture enough context for a future maintainer to understand why the choice made sense at the time.

## Discover the decision log

Read repository instructions, the local ADR template, the decision index, and relevant records before writing. Search filenames first, for example:

```bash
rg --files --hidden -g '!.git' -g '!node_modules' -g '!vendor' | rg '(^|/)(decisions?|adrs?)(/|[-_.])|[Aa][Dd][Rr]|[Aa][Gg][Ee][Nn][Tt][Ss]\.md$'
```

Follow the project's directory, numbering scope, filename, format, metadata, and lifecycle conventions. Check related records for duplicates and conflicts. Do not migrate an existing log as a side effect of recording a decision.

If no convention exists, use `docs/decisions/NNNN-short-title.md`, starting at `0001`. Choose the next unused number after the highest existing number in that log; do not renumber records or reuse gaps. Recheck the destination before writing to avoid overwriting concurrent work. Maintain an existing index; for a new log, add a small `README.md` linking its records.

Use the bundled [lightweight template](assets/adr-template-minimal.md) when context, options, outcome, and consequences explain the choice adequately. Use the [full starter](assets/adr-template.md) when competing options need detailed comparison or the decision needs explicit drivers or confirmation criteria. Honor an explicit request for either template, and expand a lightweight record when necessary. Neither template requires a fixed number of alternatives.

Both templates contain only the body and a removable assembly instruction. Read the [shared front matter](assets/adr-frontmatter.md) and prepend it to the selected body, separated by a blank line. Populate that single YAML block using the evidence and lifecycle rules below, and remove the template instruction from the finished ADR. Keep shared field defaults and examples in that file; do not duplicate them in the body templates.

## Establish what is known

Extract the problem, scope, constraints, options, chosen approach, rationale, and tradeoffs from the user's account and available code, issues, discussions, or design notes. Link evidence that actually supports the record.

- Distinguish a decision already made from a recommendation under discussion. Default new recommendations to `proposed`; record `accepted` when the user or project evidence establishes acceptance. A request to document an existing choice does not need another approval round.
- Code establishes implemented behavior, but does not establish who approved it or which alternatives were debated. Identify retrospective records and distinguish observed implementation from reconstructed rationale.
- Do not invent decision makers, consensus, dates, benchmarks, rejected alternatives, risk ratings, or audit results. Omit unknown optional metadata. Label unresolved substantive facts and ask focused questions if they would change the record.
- If the choice is unresolved, write a useful proposal from available evidence and identify the remaining decision. Do not fill in an accepted outcome to complete a template.

For new records, use today's date as the recording date. Preserve a known historical decision date separately when the project supports it; never backdate an unknown decision. In existing records, preserve creation dates and update modification dates according to local conventions.

## Resolve consequential uncertainty

Investigate repository facts before asking the user: read the relevant code, configuration, and prior decisions, and cite the evidence. Ask about intent, preferences, and tradeoff tolerance that the evidence cannot resolve. Do not ask the user to supply facts that are available locally.

Group independent questions into one concise round, with a recommended answer and its tradeoff where useful. Ask dependent questions after their prerequisites are answered. Focus on uncertainty that changes the choice, scope, acceptance, or relationship to an existing decision; do not require exhaustive questioning before writing. Reuse answers already provided.

When a decision remains open, draft the supported proposal and identify the unresolved question rather than inventing an answer. Preserve consequential clarifications in the rationale or a short clarification note; omit routine interview transcripts.

## Declare relationships

For the default MADR convention, use optional YAML lists of existing ADR identifiers:

| Field | Meaning |
| --- | --- |
| `supersedes` | Replaces the referenced decision on acceptance. |
| `extends` | Builds on the referenced decision while keeping it in force. |
| `related` | Provides relevant context without claiming replacement or dependency. |

For example, `supersedes: [ADR-0003]`. Treat the numeric filename prefix as `ADR-NNNN` in the default log even when the heading omits that identifier. Resolve each identifier within its log, and use a repository-relative file path when a reference crosses logs or would otherwise be ambiguous. Follow an existing project's reference syntax instead when it differs.

Omit unused fields. Verify targets exist, reject self-references and cycles in replacement or extension chains, and explain meaningful relationships with relative Markdown links in the body. Semantic similarity alone does not establish supersession; investigate conflicts and ask about consequential ambiguity.

Author only forward relationship metadata. Do not add inverse fields such as `superseded-by`; derive incoming relationships by searching the records. Keep human-readable links to successors in predecessors so the history is navigable without graph tooling. A proposal's `supersedes` field declares intended replacement; it does not change the target's status.

## Write the record

Use a title that identifies the concrete choice. Keep the scope to one decision; split independent choices into linked records. Ordinary implementation explanations and release notes do not require ADRs unless requested.

Explain the conditions that forced a choice and the criteria that matter. Compare genuine alternatives against those criteria, including retaining the current approach when relevant. Clearly distinguish alternatives proposed now from those considered historically; do not manufacture options to reach a fixed count.

State the chosen option or proposed recommendation and connect it to the decisive constraints. Include meaningful drawbacks, operational costs, and follow-up obligations, with mitigations where known. Keep implementation detail only when it defines the decision's boundaries.

When useful, describe a concrete way to check implementation against the decision, such as a dependency rule, integration check, or design review. Describe planned verification as planned. Do not claim checks ran while merely writing the record.

Encourage a small Mermaid diagram when it clarifies component boundaries, interactions, data flow, or a change from the current design. Add an Architecture Diagram section to either template when helpful; omit it when prose is clearer. Label proposed designs and observed implementations distinctly. Prefer a hand-authored diagram grounded in evidence; do not require a generator, service, or separate confirmation just to include one.

Replace instructional placeholders with supported content. Remove unused optional sections; retain required sections and explicitly state unknowns or non-applicability when the chosen format requires them.

## Preserve decision history

Use the allowed statuses defined in the shared front matter unless the project specifies its own lifecycle. Keep the status value separate from replacement links.

Revise proposals as the discussion evolves. Correct wording or factual errors in accepted records without changing their historical meaning.

When an accepted choice changes, create a successor describing the new circumstances and rationale. Declare `supersedes` and link it to the old record. Once the successor is accepted, mark the predecessor superseded and add a body link to the successor using the project's status syntax; a proposed or rejected successor does not retire an active decision. `extends` and `related` do not change target status. Preserve the predecessor's original argument and identifier. Deprecation without a replacement is a separate lifecycle change; do not fabricate a successor. Never infer acceptance merely from a relationship field.

## Check and report

Check identifier uniqueness, destination, local links, metadata/body agreement, relationship lists and targets, dates, unresolved placeholders, and consistency with related records. Review whether the template fits, alternatives are genuine, rationale explains the tradeoff, and diagrams match their stated scope. Update indexes and reciprocal body links as applicable. Run existing relevant Markdown or ADR validation when available; do not install CI or an ADR toolchain just to record a decision. Use ordinary file search for discovery and relationship checks; no search engine or graph service is required.

For review-only requests, report findings without edits. For writing requests, create the files and report their paths, status, unresolved questions, and checks actually performed. Recording a decision does not authorize implementing it.
