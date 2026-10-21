---
title: 'Wiki Ingest'
description: 'Ingest sources into a persistent, LLM-maintained wiki following the LLM Wiki pattern.'
weight: 30
---

Ingest sources into a persistent, LLM-maintained wiki following the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. Drop an article, paper, or note into `_inbox/` (or give a path or URL) and the agent moves inbox files into `raw/` without changing their contents, reads each source fully, discusses takeaways with you, writes a summary page, updates affected entity, concept, domain, and project pages, and appends to the wiki log. Knowledge compounds: cross-references accumulate and contradictions get flagged instead of silently overwritten. This skill also bootstraps the wiki layout on first run.

**Use when:**

- "Ingest this"
- "Add this source to the wiki"
- "File this article/paper/note"
- "Process this source"
- "Add this to the knowledge base"
- "Process the inbox"
- "I just added X to _inbox/"
- "I just added X to raw/"

**What it does:**

- Bootstrap: reads existing conventions, then creates only missing wiki files and directories. For a new wiki with no schema, it adds a CLAUDE.md schema skeleton; existing instruction files and wiki content are preserved
- Looks in `_inbox/` by default when no source is specified; moves selected files into `raw/` rather than copying them, preserving contents and avoiding overwrites
- One source at a time by default (takeaways discussed with you first); batch mode when you explicitly ask
- Writes `wiki/sources/<slug>.md` with key claims, dates, and reliability notes, citing the raw file
- Updates affected entity/concept pages, creating new pages for significant topics and flagging contradictions without silently overwriting claims
- Maintains broad domain syntheses in `wiki/domains/` and project indexes, architecture, workflow, and decision notes in `wiki/projects/<project>/`
- Keeps `wiki/index.md` (one line per page) and `wiki/log.md` current on every ingest
- Commits each completed source ingest locally when the wiki is in a Git working tree, including during batch ingestion; leaves unrelated edits and staged changes out of the commit

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Ingest the sources in _inbox/
```
```
I just added three papers to _inbox/ — batch-ingest them with less supervision
```
```
File this article into the wiki: https://example.com/sparse-attention
```

## Wiki layout

`_inbox/` and `raw/` remain siblings of `wiki/`. The compiled wiki uses this layout:

```text
wiki/
  index.md                 # catalog of all pages, by category
  overview.md              # evolving top-level synthesis
  log.md                   # append-only chronological record
  sources/                 # one summary per archived source
  entities/                # people, orgs, products, places...
  concepts/                # reusable topics, themes, methods...
  analyses/                # durable answers and comparisons
  domains/                 # broad areas of knowledge
    ai.md
    software-engineering.md
    self-hosting.md
    finances.md
  projects/                # project-specific context and decisions
    home-lab/
      index.md
      architecture.md
      decisions.md
    llm-wiki/
      index.md
      workflow.md
      decisions.md
```

Domain pages synthesize broad areas and connect related knowledge. Project folders hold local context, supporting notes, and recorded decisions. The named domain and project pages are examples, created when relevant content exists. Reusable concepts and entities stay in their shared directories and are linked from domain and project pages.

The global `wiki/index.md` catalogs every page, including project indexes and supporting pages; each project index also provides local navigation. Use qualified wikilinks such as `[[projects/home-lab/index]]` and `[[projects/llm-wiki/decisions]]` because filenames repeat across projects. Proposed decisions remain distinct from adopted decisions.

## How it works

1. Locates the wiki using your path and schema before default-path discovery, and records any existing Git changes before editing. With no explicit source, looks in `_inbox/`, including subdirectories. An empty inbox is reported rather than triggering automatic re-ingestion of `raw/`
2. Moves selected inbox files into `raw/` unchanged, choosing a distinct destination on collisions. Files already in `raw/` stay in place; other explicit paths or attachments are copied unless you request a move. URL sources become new snapshots in `raw/` with the URL and retrieval date recorded. Citations use the archived path; existing raw files are never overwritten
3. Reads it fully, viewing referenced images separately when they matter, then normalizes generic X titles/filenames and supported handle-only authors before writing wiki pages. May also update `tags` and `description` frontmatter and label clearly recognizable, unlabeled Mermaid fences as described below
4. Discusses key takeaways and planned page updates with you before writing
5. Writes the source summary page, updates affected entity/concept, domain, and project pages and, when the big picture changes, `wiki/overview.md`, refreshes `wiki/index.md`, and appends a `## [YYYY-MM-DD] ingest | <Title>` entry to `wiki/log.md`
6. Checks the final title, filename, author, source preservation, resolved raw/asset links, page updates, and log entry against the original source before committing. Reports unsupported identities or schema restrictions explicitly.
7. If the wiki is in a Git working tree (including a worktree or a wiki nested in a larger repo), commits only that completed source’s ingest changes with a message such as `wiki: ingest Attention Is All You Need`, then reports the commit hash. This includes archived sources/assets, tracked inbox removals, wiki updates, and any bootstrap files. Batch ingestion creates one commit per completed source.

Unrelated working-tree edits and pre-existing staged changes are preserved and excluded from the ingest commit, including unrelated edits in the same file. If the changes cannot be separated, the agent reports the blocked commit. No empty commit is created when nothing changed. A commit failure leaves the files intact and is reported separately from successful ingestion; Git configuration and hooks are preserved. Outside Git, ingestion finishes without initializing a repository. Ingest commits stay local unless you separately request a push.

If ingestion fails after a move, the agent reports the archived path and unfinished work so it can resume from `raw/`.

For GitHub repository-root sources, use `<owner> - <repo>.md` as the archived Markdown filename: `https://github.com/tobi/qmd` becomes `raw/tobi - qmd.md`. This applies to inbox exports identified by their original source URL and to newly fetched repository-root snapshots, including URLs with a trailing slash. Issues, pull requests, files, and other repository subpages keep their own naming. Preserve the source title and provenance, handle collisions with a date or unique suffix, preserve asset links, and cite the final archived path.

The source file’s `tags` and `description` YAML frontmatter fields may be added or updated. When moving an X (Twitter) post from `_inbox/` into `raw/`, a generic frontmatter `title` such as `Post by @karpathy on X` must be replaced after reading the source with a concise title grounded in the post’s content. Give the archived file a matching kebab-case name, preserving its extension: for example, `Karpathy on maintaining an LLM wiki` becomes `raw/karpathy-on-maintaining-an-llm-wiki.md`. On collisions, retain that slug and add a date or unique suffix. Preserve accompanying asset links and cite the final path. Meaningful existing titles are preserved. When the source, established wiki context, or user confirmation supports a handle’s identity, expand a handle-only frontmatter `author` to a full name while preserving the handle (for example, `Andrej Karpathy (@karpathy)`). Keep ambiguous identities as handles and report the uncertainty. Post text, headings, URLs, dates, unrelated metadata, and other provenance stay unchanged. These normalization rules also cover resuming an unfinished ingest already archived in `raw/`. During ingestion, the agent may also label a clearly recognizable Mermaid diagram in an unlabeled fenced code block by adding `mermaid` to its opening fence (for example, a block beginning with `flowchart LR`). Apart from these permitted frontmatter edits, diagram contents, closing fences, surrounding text, other original fields, and provenance stay unchanged. Blocks that are ambiguous or already have a language identifier are left as they are.

For example, an unlabeled block containing `flowchart LR` can become:

````markdown
```mermaid
flowchart LR
  Q[User Query] --> X[Query Expansion]
```
````

The completion message links both the archived raw file and its source summary and includes the commit hash when applicable.

A blanket schema rule such as “raw: read, never modify” conflicts with the permitted normalization. The agent must identify this conflict before edits, apply existing explicit user authorization if it resolves the conflict, and otherwise report which required changes are blocked. It updates an existing wiki schema only when authorized; new schema skeletons explicitly describe the permitted exceptions.

Your wiki's own CLAUDE.md/AGENTS.md schema overrides the default layout and formats — the defaults apply only until you and the agent co-evolve something better.

## Sibling skills

This skill is one of three interoperating wiki skills in this collection:

- **wiki-query** — answers questions from the wiki with citations; files valuable answers back as `wiki/analyses/` pages
- **wiki-lint** — health-checks the wiki: contradictions, stale claims, orphan pages, missing concepts

## Full Skill Definition

See [skills/wiki-ingest/SKILL.md](../../skills/wiki-ingest/SKILL.md) for the complete agent instructions (default wiki layout, page and index/log formats, contradiction handling, and edge cases) that the agent loads when this skill is active.
