---
name: wiki-lint
description: Periodic health-check for an LLM Wiki markdown knowledge base. Use when the user says "lint the wiki", "health check the wiki/knowledge base", "clean up the wiki", "check the wiki for contradictions/orphans", "what's stale in my wiki", "wiki maintenance", or similar.
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Wiki Lint

Check a persistent Markdown knowledge wiki for correctness, drift, and missing connections. Read and report by default. When the user has already requested fixes, apply the authorized changes without asking again; a request to review or report alone authorizes no wiki writes, including log entries. Never modify files under the raw-source directory.

Sibling skills: `wiki-ingest` adds sources and bootstraps new wikis; `wiki-query` answers from wiki pages. They are optional companions, not runtime dependencies.

## Locate the wiki and read its schema

Honor a user-specified root and paths first. Read applicable `AGENTS.md`/`CLAUDE.md` instructions and any wiki schema they reference **before** assuming a layout. Schema-defined directories, index paths, hubs, categories, and citation conventions override the defaults below.

If no root is specified or configured, inspect the current project for `wiki/index.md`. Search within the project only as needed; exclude raw-source directories. If several wikis fit, ask which one. A missing default index does not mean a custom-layout wiki is absent. If the configured wiki does not exist, report that and suggest creating it with `wiki-ingest` or the user's chosen workflow; do not bootstrap during lint.

If wiki pages exist but the configured index, log, or raw directory is missing, report the missing component rather than declaring the wiki absent. The checker requires an existing index and raw directory; run applicable checks manually when those prerequisites are missing. A missing log does not block the checker. Create missing components only within an authorized repair request.

Default layout:

```text
<wiki-root>/
  CLAUDE.md           # or AGENTS.md — conventions (optional)
  raw/                # immutable source snapshots
  wiki/
    index.md          # catalog of pages, grouped by category
    log.md            # append-only activity history
    overview.md       # evolving synthesis
    sources/          # source summaries
    entities/ concepts/ analyses/
```

Read recent log entries and prior lint results if available. Skip dismissed findings unless new evidence changes them, or label them with the earlier decision and date.

## Mechanical checks

Run the bundled, read-only checker using Python 3.10 or newer. Resolve `<skill-dir>` to the directory containing this `SKILL.md`, not the wiki directory:

```bash
python3 -B <skill-dir>/scripts/check_wiki.py /path/to/wiki-root
```

For schema-defined layouts, pass paths relative to the wiki root (absolute paths also work):

```bash
python3 -B <skill-dir>/scripts/check_wiki.py /path/to/wiki-root \
  --wiki-dir knowledge --raw-dir material --index knowledge/catalog.md \
  --hub knowledge/activity.md --hub knowledge/synthesis.md
```

`--hub` is repeatable. The configured index and default `log.md`/`overview.md` at the top of the wiki directory are excluded from orphan, index-coverage, and stub candidates. Add any other schema-defined hubs explicitly.

The checker prints JSON candidates with a kind, file, line, and message. Exit 0 means the scan completed, even with findings; exit 2 indicates a missing layout, unreadable file, or invalid configuration. It does not create files, fetch URLs, edit the wiki, or update the log.

Checks:

- **Broken or ambiguous wikilinks.** Handles aliases, heading suffixes, optional `.md`, and relative links. Qualified targets keep their directory identity; unqualified names matching several pages are reported for review. Heading-only links stay on the current page. It checks destination pages, not whether individual headings exist.
- **Broken raw references and unreferenced raw files.** Markdown links resolve relative to their page, with URL decoding and support for spaces/Unicode. Root-relative raw paths in `source:` fields, quoted strings, inline code, and simple bare paths are also recognized.
- **Index drift.** Reports missing catalog entries and broken/ambiguous links in the index without conflating pages sharing a basename.
- **Orphans.** Reports pages without inbound wikilinks from another page; index links and self-links do not count.
- **Possible stubs.** Pages under 10 lines are candidates, not automatically incomplete.

Verify candidates before reporting. This is a small heuristic checker, not a complete Markdown, YAML, or Obsidian parser. It skips fenced code and HTML comments, and ignores wikilinks in inline code. Reference-style Markdown links, complex nested link syntax, attachment wikilinks, heading validation, custom link resolution rules, and unusual frontmatter need manual inspection. Wikilinks provide the page graph; ordinary Markdown links between wiki pages are not counted as graph edges. Bare paths ending in sentence punctuation are heuristic; prefer Markdown links, quoted paths, or the `source:` field for filenames containing spaces or punctuation. Do not conclude a source was never ingested solely because the checker found no recognized reference. Adapt checks manually when the schema uses unsupported conventions.

## Judgment checks

Read related pages together; mechanical checks cannot establish truth or completeness.

- **Contradictions.** Cite both claims and their evidence. A newer publication date alone does not establish supersession. Compare scope, source quality, editions, and any explicit corrections. Propose replacing an old claim only when the evidence supports it, preserving its history and citations; otherwise keep the conflict visible and unresolved.
- **Stale claims.** Check source publication/revision dates and evidence of actual change. A page's `updated` date records editing activity, not the age or reliability of its claims.
- **Missing concepts and cross-references.** Look for important recurring terms without pages and clearly related pages without links. Repetition alone is not a reason to create a page.
- **Data gaps and growth.** Suggest specific facts to verify, useful questions to investigate, and sources that would strengthen weak areas. Search externally when already requested or otherwise authorized by the user; proposing a search does not require performing it.

## Report and apply changes within the request

Order findings by impact:

1. **Correctness:** contradictions, stale claims, broken links/references.
2. **Drift:** index inconsistencies.
3. **Hygiene:** orphans, stubs, unreferenced raw files, missing cross-references.
4. **Growth:** missing concepts, data gaps, new questions, and sources to seek.

Give each finding a specific file and line or claim, its consequence, and a concrete proposed fix. Distinguish demonstrated errors from candidates requiring judgment.

For report-only requests, return the findings without editing any wiki file or appending a log entry. If the user requested repairs, apply the fixes within that existing authorization; ask only about changes outside it or unresolved choices that materially affect the content. Preserve unresolved contradictions and raw sources.

After authorized changes, update the index for added, removed, renamed, or materially changed pages. Append a concise entry to the configured log using the actual current ISO date and the wiki's format, for example:

```markdown
## [2026-10-20] lint | 9 findings, 5 fixes applied

Fixed broken links and synchronized the index. Preserved two unresolved conflicts.
```

Log a report-only pass only if the user explicitly requested logging or an established user-approved workflow permits it. Never edit existing log entries. Change the schema only when that change is within the user's request.
