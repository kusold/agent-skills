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
2. Reads the pages, following wikilinks for multi-hop questions. If the index is stale, it falls back to searching the wiki directory and suggests **wiki-lint** to fix the drift.
3. Synthesizes an answer with citations, clearly separating sourced claims, inferences it is constructing, and coverage gaps ("the wiki doesn't cover X yet — want to ingest a source on it?"). Conflicts between pages are surfaced, not averaged away.
4. Matches the output form to the ask: plain markdown (default), comparison table, Marp slide deck, or matplotlib chart.
5. For durable syntheses, offers to file the answer as `wiki/analyses/<slug>.md`, update `wiki/index.md`, and append a `query` entry to `wiki/log.md`. Casual Q&A stays in chat — the log stays signal-rich.

## Full Workflow Reference

See [skills/wiki-query/SKILL.md](../../skills/wiki-query/SKILL.md) for the complete workflow, default wiki layout, analysis-page and log-entry formats, and edge cases that the agent loads when this skill is active.

## Sibling skills

One of three interoperating skills based on the LLM Wiki pattern:

- **wiki-ingest** — add sources and build/maintain wiki pages, index, and log
- **wiki-query** — this skill: answer from the wiki, file valuable answers back
- **wiki-lint** — health-check the wiki: contradictions, orphans, stale claims, index drift
