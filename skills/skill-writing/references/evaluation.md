# Evaluating a skill

Use this reference when creating a workflow or changing behavior. For a narrow edit, select checks that exercise the affected decision; do not turn every revision into an evaluation project.

## Select representative cases

Use actual user requests, artifacts, and past failures when available. Include the cases that can distinguish a useful skill from a plausible instruction file:

| Case | What to observe |
| --- | --- |
| Ordinary in-scope request | Correct deliverable and relevant workflow |
| Natural paraphrase without the skill name | Description supports selection when the host offers automatic discovery |
| Nearby out-of-scope request | Skill does not divert unrelated work |
| Missing prerequisite or consequential ambiguity | Agent identifies the missing input and follows the skill's boundary |
| Improvement objective | Revised guidance meets the requested objective while a relevant working case still succeeds |
| Prior failure, when available | Correction fixes the observed failure |

Explicit invocation tests execution after selection; it cannot establish automatic activation quality. If the host cannot test discovery, inspect description boundaries and report that limitation.

For discovery tuning, label realistic prompts with expected selection. Include indirect paraphrases and near-misses sharing vocabulary. Confirm registration and observe entrypoint loading in host traces. Use fresh contexts, repeat ambiguous results, and reserve unseen prompts to check generalization. Tune activation separately from execution quality; broader triggering can increase false positives. See the official [description guide](https://agentskills.io/skill-creation/optimizing-descriptions).

Define expectations before running the case. Check the result, resource use, and side effects, rather than requiring exact phrases or headings. A useful case record is:

```text
Request:
Inputs and environment:
Expected selection or non-selection:
Observable success criteria:
Permitted side effects:
Observed result and artifact locations:
Check method (inspection, walkthrough, or agent run):
Limitations:
```

For example, "Review this SKILL.md without editing it" succeeds when the agent reports actionable findings and leaves files unchanged. "Improve the description; keep the workflow unchanged" succeeds when the selection boundary improves without unrelated workflow edits. Neither requires a particular response heading.

## Execute only what the environment supports

Use disposable copies or fixtures for generated artifacts and mutations. Avoid live services unless their use is authorized and needed for the case. When delegated evaluation is available and authorized, supply the evaluator with the request, skill, and necessary inputs, without coaching it toward the expected answer.

For an existing skill, compare the old and revised versions on the same relevant inputs where practical. For a new skill, a run without the skill can reveal whether its guidance adds value. Record tool and model differences that limit comparison. If execution is unavailable, walk through decisions and report the result as a walkthrough, not a successful agent trial.

Inspect the produced artifacts and effects. A convincing explanation of success is insufficient if the deliverable is wrong. Avoid turning a small sample into a success-rate claim.

Start with a small set of representative cases. Run comparisons in clean contexts with equivalent tools and inputs; snapshot the old skill before editing when needed for the baseline. Keep reusable cases separate from generated results. Use deterministic checks for objective properties and human review for subjective quality; preserve evidence for each judgment. Inspect traces for wasted steps, and record time or tokens when available. If the skill adds no benefit over the baseline, simplify it or reconsider whether it is needed. See the official [output evaluation guide](https://agentskills.io/skill-creation/evaluating-skills).

## Revise from evidence

Compare the result with the improvement objective. For a failure, locate its cause: selection, missing context, ambiguous decision, incorrect tool use, resource defect, or validation gap. For clarity, brevity, or changed requirements, check that the requested improvement preserves necessary decisions and constraints. Rerun the affected case when possible and check a relevant working case for regressions. Keep evidence-backed rules and remove instructions superseded by the correction.

Revisit the skill when its tools, schemas, conventions, or supported tasks change. A modification date or successful format check does not establish that guidance is still correct.
