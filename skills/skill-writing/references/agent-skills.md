# Agent Skills format

Checked against the [official specification](https://agentskills.io/specification) on 2026-10-22. Recheck it when compatibility questions arise.

Use the bundled [specification snapshot](specification.md) for full rules and examples without network access. It includes attribution, its retrieval date, and extraction notes. This checklist is a summary; the snapshot preserves the source's detail, including its ambiguous wording about Unicode names. Use the live source to resolve changes or ambiguities when needed.

## Package checks

Require `SKILL.md` with YAML frontmatter followed by Markdown instructions.

| Field | Constraint |
| --- | --- |
| `name` | Required; 1–64 lowercase alphanumeric characters or hyphens; no leading, trailing, or consecutive hyphens; matches the directory |
| `description` | Required; 1–1024 characters describing capability and activation |
| `license` | Optional license identifier or bundled license reference |
| `compatibility` | Optional environment requirements; 1–500 characters when present |
| `metadata` | Optional mapping of string keys to string values |
| `allowed-tools` | Optional space-separated tool string; experimental and host-dependent |

Use ASCII names for portability. Do not treat tool metadata as overriding host permissions.

Keep references shallow and directly discoverable from `SKILL.md`. The specification recommends fewer than 500 lines and roughly 5,000 tokens for the entrypoint; these are ceilings, not targets.

When available, run:

```bash
skills-ref validate ./skills/example
```

If `skills-ref` is not installed and `uvx` is available, run the official reference package in an isolated environment:

```bash
uvx --from 'git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref' \
  skills-ref validate ./skills/example
```

This fallback requires Git and network access on the first run. Replace `./skills/example` with the skill directory being checked. If neither command is available, inspect the package checks above and report that automated validation was unavailable.

The [reference library](https://github.com/agentskills/agentskills/tree/main/skills-ref) is demonstrative, not a complete behavioral validator. If a host validator rejects a standard field, report the compatibility difference rather than silently stripping it.

## Official authoring guides

Consult the relevant guide when deeper guidance is needed:

- [Best practices](https://agentskills.io/skill-creation/best-practices)
- [Description optimization](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Output evaluation](https://agentskills.io/skill-creation/evaluating-skills)
- [Script design](https://agentskills.io/skill-creation/using-scripts)

## Refreshing the snapshot

Fetch a candidate with the recorded extractor version:

```bash
npx --yes defuddle@0.19.5 parse https://agentskills.io/specification \
  --markdown --output /tmp/agent-skills-specification-candidate.md
```

Compare the candidate with the live page or its native Markdown at `https://agentskills.io/specification.md`, checking tables and code examples for dropped content. Review the diff before replacing the bundled body. Preserve attribution and licensing, update the actual retrieval date and conversion notes, and reconcile this checklist when requirements change. Fetching alone does not verify an extraction.
