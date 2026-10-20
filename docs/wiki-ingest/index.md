---
title: 'Wiki Ingest'
description: 'Ingest sources into a persistent, LLM-maintained wiki following the LLM Wiki pattern.'
weight: 30
---

Ingest sources into a persistent, LLM-maintained wiki following the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. Drop an article, paper, or note into `raw/` (or give a URL) and the agent reads it fully, discusses takeaways with you, writes a summary page, updates every entity and concept page it touches, and appends to the wiki log. Knowledge compounds: cross-references accumulate and contradictions get flagged instead of silently overwritten. This skill also bootstraps the wiki layout on first run.

**Use when:**

- "Ingest this"
- "Add this source to the wiki"
- "File this article/paper/note"
- "Process this source"
- "Add this to the knowledge base"
- "I just added X to raw/"

**What it does:**

- Bootstrap: reads existing conventions, then creates only missing wiki files and directories. For a new wiki with no schema, it adds a CLAUDE.md schema skeleton; existing instruction files and wiki content are preserved
- One source at a time by default (takeaways discussed with you first); batch mode when you explicitly ask
- Writes `wiki/sources/<slug>.md` with key claims, dates, and reliability notes, citing the raw file
- Updates affected entity/concept pages, creating new pages for significant topics and flagging contradictions without silently overwriting claims
- Keeps `wiki/index.md` (one line per page) and `wiki/log.md` current on every ingest

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Ingest raw/attention-is-all-you-need.md
```
```
I just added three papers to raw/ — batch-ingest them with less supervision
```
```
File this article into the wiki: https://example.com/sparse-attention
```

## How it works

1. Locates the wiki using your path and schema before default-path discovery. Saves URL sources as new snapshots in `raw/`, recording the URL and retrieval date; existing raw files are never overwritten
2. Reads it fully, viewing referenced images separately when they matter
3. Discusses key takeaways and planned page updates with you before writing
4. Writes the source summary page, updates entity/concept pages and, when the big picture changes, `wiki/overview.md`, refreshes `wiki/index.md`, and appends a `## [YYYY-MM-DD] ingest | <Title>` entry to `wiki/log.md`

Your wiki's own CLAUDE.md/AGENTS.md schema overrides the default layout and formats — the defaults apply only until you and the agent co-evolve something better.

## Sibling skills

This skill is one of three interoperating wiki skills in this collection:

- **wiki-query** — answers questions from the wiki with citations; files valuable answers back as `wiki/analyses/` pages
- **wiki-lint** — health-checks the wiki: contradictions, stale claims, orphan pages, missing concepts

## Full Skill Definition

See [skills/wiki-ingest/SKILL.md](../../skills/wiki-ingest/SKILL.md) for the complete agent instructions (default wiki layout, page and index/log formats, contradiction handling, and edge cases) that the agent loads when this skill is active.
