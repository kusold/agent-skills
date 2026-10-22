---
title: 'Wiki Query'
description: 'Answer questions from wiki evidence with citations, and file durable analyses back into the wiki.'
weight: 50
---

Answer questions against an [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Andrej Karpathy's pattern for a persistent, LLM-maintained knowledge base of interlinked markdown pages — instead of re-reading raw sources. The skill reads `wiki/index.md` to find relevant pages, follows wikilinks, and synthesizes an answer where every claim cites the wiki page behind it (and through that page, the source summary and raw file). With your authorization or an established workflow, durable answers — comparisons, analyses, timelines, discovered connections — can be filed back into `wiki/analyses/` so explorations compound instead of disappearing into chat history.

**Use when:**

- "What does the wiki say about X?"
- "Search the wiki for X"
- "According to my notes / wiki / knowledge base, ..."
- "Compare X and Y using my wiki" (generic comparisons need an established wiki context)
- "What have I read about X?"
- "Summarize what I know about X"
- Any question about a topic you've been ingesting sources on

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
What does the wiki say about transformer attention variants?
```
```
Compare Postgres and SQLite for edge deployments using my wiki
```
```
Summarize what I know about sleep and exercise
```

## How it works

1. Reads your explicit path and existing schema before default-path discovery, then uses the configured catalog to select pages. If pages exist without a catalog, it searches them and reports the gap. If no wiki exists, it suggests **wiki-ingest** rather than bootstrapping one.
2. Resolves wikilinks to existing files, including aliases and headings, and reports unresolved ambiguity or broken links. Reads the pages, starting with domain syntheses for broad questions or project indexes and architecture/workflow/decision notes for project questions, then follows wikilinks to evidence. Uses qualified project links to distinguish repeated filenames and distinguishes proposed from adopted decisions. If the index is stale, it falls back to searching the wiki directory and suggests **wiki-lint** to fix the drift.
3. Checks the content of cited pages and traces source evidence when available. Reads raw sources for exact quotes, quantitative details, or disputed claims, and reports missing evidence without implying verification. Uses navigable chat citations when the host cannot resolve wikilinks. Synthesizes an answer with citations, clearly separating sourced claims, inferences it is constructing, and coverage gaps ("the wiki doesn't cover X yet — want to ingest a source on it?"). Conflicts between pages are surfaced, not averaged away.
4. Matches the output form to the ask: plain markdown (default), comparison table, Marp slide deck, or matplotlib chart.
5. Queries are read-only by default. With a save request or an established workflow, files durable syntheses as `wiki/analyses/<slug>.md`, updates `wiki/index.md`, and appends a `query` entry to `wiki/log.md`. Checks for an existing analysis before writing and chooses an unused descriptive slug unless revising that page is authorized. Uses actual dates and only verified source references. Relevant domain pages and project indexes link to saved analyses when useful. Casual Q&A stays in chat — the log stays signal-rich.

The shared [wiki layout](../wiki-ingest/) includes `domains/` and nested `projects/` alongside sources, entities, concepts, and analyses. The global index catalogs every page; project indexes provide additional local navigation.

## Full Workflow Reference

See [skills/wiki-query/SKILL.md](../../skills/wiki-query/SKILL.md) for the complete workflow, default wiki layout, analysis-page and log-entry formats, and edge cases that the agent loads when this skill is active.

## Sibling skills

One of three interoperating skills based on the LLM Wiki pattern:

- **wiki-ingest** — add sources and build/maintain wiki pages, index, and log
- **wiki-query** — this skill: answer from the wiki, file valuable answers back
- **wiki-lint** — health-check the wiki: contradictions, orphans, stale claims, index drift
