---
title: 'Wiki Lint'
description: 'Check a markdown wiki for contradictions, stale claims, broken links, index drift, orphan pages, and incomplete pages.'
weight: 40
---

Check an existing Markdown knowledge wiki for contradictions, stale claims, broken links, index drift, orphan pages, and incomplete pages. The agent verifies candidates and proposes concrete fixes in a prioritized report. It also suggests useful questions and sources to investigate.

**Use when:**

- "Lint the wiki"
- "Health check my wiki / knowledge base"
- "Review the wiki for contradictions and orphan pages"
- "What's stale in my wiki?"
- "Clean up the wiki and fix the broken links"

The skill can be selected by an agent that supports installed skills, or invoked explicitly using the host agent's skill mechanism. It requires an existing wiki; `wiki-ingest` is an optional way to create one.

## Usage

```text
Health check the wiki and report what's stale. Do not change files.
```

```text
Lint the wiki and fix broken links and index drift.
```

A review or report request leaves wiki files untouched, including the log. A request to fix issues authorizes those fixes; the agent does not ask for the same permission again. Questions remain appropriate for unresolved content choices or changes outside the request. Raw source content and provenance stay unchanged; authorized repairs may add or update only the source file’s `tags` and `description` YAML frontmatter fields.

The agent reads your applicable `AGENTS.md`/`CLAUDE.md` instructions and wiki schema before assuming a directory layout. Explicit paths and schema conventions take precedence over defaults, including custom index and log locations.

If existing wiki pages lack a configured index, log, or raw directory, the agent reports that missing component and continues applicable checks manually. It does not treat the wiki as nonexistent or bootstrap a replacement. The bundled checker requires an existing index and raw directory; a missing log does not prevent its scan.

The shared [wiki layout](../wiki-ingest/) includes domain syntheses and project folders with local indexes and supporting notes. Lint checks domain consistency, project navigation, and agreement between project notes and recorded decisions. Example domain/project pages are not required when there is no content for them.

## Checks and limitations

The bundled Python 3.10+ checker is read-only and uses only the standard library. It checks wikilink destinations and ambiguity, raw references, index coverage, orphan pages, and short-page candidates. It preserves directory-qualified link targets, so `entities/acme.md` and `sources/acme.md` remain distinct. Raw Markdown links resolve relative to the page and support spaces, Unicode, and URL encoding. Link labels, titles, and remote destinations do not count as local raw references: `[paper](https://example.org/raw/paper.pdf)` does not reference a local `raw/paper.pdf`.

From a repository checkout, run:

```bash
python3 -B skills/wiki-lint/scripts/check_wiki.py /path/to/wiki-root
```

For a custom layout:

```bash
python3 -B skills/wiki-lint/scripts/check_wiki.py /path/to/wiki-root \
  --wiki-dir knowledge --raw-dir material --index knowledge/catalog.md \
  --hub knowledge/activity.md --hub knowledge/synthesis.md
```

Paths are relative to the wiki root unless absolute. `--hub` is repeatable and excludes additional schema-defined hub pages from orphan, index-coverage, and stub candidates. The index and default top-level `log.md`/`overview.md` are already hubs. Project indexes remain ordinary content pages: do not mark them as hubs just because they are named `index.md`. They and their supporting pages belong in the global catalog. Qualified links such as `[[projects/home-lab/decisions]]` avoid ambiguity between repeated filenames; short but complete navigation pages need not be reported as stubs. The checker prints JSON with file/line references. Exit 0 means the scan completed, even when findings exist; exit 2 indicates a configuration or read error. It never writes a report or changes wiki files itself.

Results require review: the checker is not a full Markdown/YAML/Obsidian parser. It does not validate heading anchors, reference-style Markdown links, attachment wikilinks, complex nested links, or custom link-resolution conventions. Its page graph uses wikilinks; ordinary Markdown links between wiki pages need manual checks. Bare raw paths with punctuation are heuristic; use Markdown links, quoted paths, or a `source:` field for unusual filenames. An unrecognized reference can make an ingested source look unreferenced.

The agent separately reads related pages for contradictions, stale claims, missing concepts, and missing cross-references. A newer source does not automatically supersede an older one; replacement requires evidence of a correction or relevant change. Otherwise both claims and their citations remain visible. Page modification dates do not establish claim freshness.

Findings are prioritized as correctness, drift, hygiene, then growth opportunities. Authorized repairs also update affected catalog entries and append a dated lint entry to the configured log. Report-only passes are logged only when explicitly requested or already covered by a user-approved workflow.

## Skill and regression tests

See [the full skill definition](../../skills/wiki-lint/SKILL.md) for the workflow and authorization boundaries, and [the checker](../../skills/wiki-lint/scripts/check_wiki.py) for the mechanical implementation.

Run the isolated fixture tests from a checkout:

```bash
python3 -B -m unittest discover -s skills/wiki-lint/scripts -p 'test_*.py' -v
```

Sibling skills: **wiki-ingest** adds sources and maintains wiki pages; **wiki-query** answers questions with citations and can save durable analyses.
