---
name: wiki-ingest
description: Ingest sources into a persistent, LLM-maintained wiki (the LLM Wiki pattern) by writing a summary page and updating entity, concept, index, overview, and log pages. Use when the user says "ingest this", "add this source to the wiki", "file this article/paper/note", "process this source", "add this to the knowledge base", or "I just added X to raw/".
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Wiki Ingest

Build a persistent knowledge wiki that sits between the user and immutable raw sources: read each source fully, discuss takeaways with the user, then write its summary page and update every entity/concept page it touches, plus the index and log, and the overview when the big picture changes. Knowledge is compiled once and kept current — not re-derived per query. This skill also bootstraps the wiki on first run. Sibling skills in this collection: `wiki-query` (answer questions from the wiki) and `wiki-lint` (health-check it).

## Layers and default layout

- `raw/` — the user's curated sources. Immutable: read them, never modify them.
- `wiki/` — your pages. You create and maintain all of it.
- `<wiki-root>/CLAUDE.md` (or `AGENTS.md`) — the schema: conventions for this wiki, co-evolved by user and LLM.

Default layout (wiki root = current project directory unless the user points elsewhere):

```
<wiki-root>/
  CLAUDE.md                  # the schema — conventions for THIS wiki
  raw/                       # immutable sources (articles, papers, notes, assets)
  wiki/
    index.md                 # catalog of all pages, by category
    log.md                   # append-only chronological record
    overview.md              # evolving top-level synthesis
    sources/                 # one summary page per ingested raw source
    entities/                # people, orgs, products, places, projects...
    concepts/                # topics, themes, methods...
    analyses/                # answers filed back by wiki-query
```

**Schema overrides defaults.** If a CLAUDE.md/AGENTS.md exists at the wiki root, or `wiki/index.md`/`wiki/log.md` already follow a different structure, follow the wiki's own conventions instead of everything below.

## Workflow

### 0. Locate the wiki and bootstrap missing files

Start with the user's explicit path and available project instructions. Read existing `CLAUDE.md`/`AGENTS.md` conventions before looking for the default `wiki/index.md`; a schema may specify a different wiki directory or catalog name. If multiple candidate wikis remain, ask which one to use.

For a new wiki, create the default layout above. For an existing or partial wiki, create only missing directories and files, following its schema. A missing default index does not authorize replacing existing pages, logs, or instruction files. If no schema file exists, create a `CLAUDE.md` skeleton describing the layout, page types, and log format. If an instruction file already exists, preserve it; add wiki conventions only when requested. Tell the user where the conventions live and that they can evolve them.

### 1. Locate the source

The user gives a path under `raw/`, drops a file, or gives a URL. For a URL, fetch and save a new snapshot into `raw/` first (e.g. `raw/<slug>.md`), recording the URL and retrieval date, then ingest the saved file. Creating a new snapshot is allowed; never overwrite, edit, or delete an existing raw file. If the destination exists, reuse it only when it is the intended identical source; otherwise choose a distinct filename, such as a dated snapshot with a unique suffix. Apply the same collision check to dropped files copied into `raw/`.

### 2. Read it fully

Read the entire source — papers, articles, chapters — not excerpts. You cannot read markdown with inline images in one pass: read the text first, then view the referenced images separately if they matter. Note publication date, authorship, and quality signals as you go.

### 3. Discuss before writing

Default mode is one source at a time with the user involved: present key takeaways, the entity/concept pages you expect to create or update, and any contradictions with existing pages; let the user guide what to emphasize. Batch-ingest (skip the per-source discussion) only when the user explicitly asks for less-supervised bulk ingest — still surface all contradictions at the end.

### 4. Write the source page `wiki/sources/<slug>.md`

Key claims, dates, and quality/reliability notes. Cite the raw file.

```markdown
---
type: source
created: 2026-10-20
updated: 2026-10-20
source: raw/attention-is-all-you-need.md
---

# Attention Is All You Need

Raw: [raw/attention-is-all-you-need.md](../../raw/attention-is-all-you-need.md) — Vaswani et al., 2017.

**Reliability:** peer-reviewed, heavily cited; claims well-supported.

## Key claims
- Transformers replace recurrence with self-attention alone. (§3, raw/attention-is-all-you-need.md)
- ...
```

Use real current dates (ISO `YYYY-MM-DD`). Frontmatter is optional but recommended (enables Obsidian Dataview) unless the schema says otherwise.

### 5. Update entity and concept pages

For each significant entity or concept the source touches, create or update `wiki/entities/<slug>.md` or `wiki/concepts/<slug>.md`. Slugs are filenames; cite claims with `[[sources/<slug>]]`. Update every affected page, but create new pages only for significant entities or concepts; there is no target page count.

```markdown
---
type: entity
created: 2026-10-10
updated: 2026-10-20
sources:
  - "[[sources/attention-is-all-you-need]]"
---

# Google Brain

Google's AI research org; introduced the Transformer. ([[sources/attention-is-all-you-need]])
```

**Contradictions: never silently overwrite.** When new information conflicts with what a page says, add a `## Conflicts` section (or an inline note) citing both sources, and mention it to the user:

```markdown
## Conflicts
- [[sources/attention-is-all-you-need]] says X; [[sources/rnn-notes-2024]] says Y. Unresolved as of 2026-10-20.
```

### 6. Update `wiki/overview.md`

Only if the source changes the big picture — keep the synthesis short and evolving.

### 7. Update `wiki/index.md`

Add or update one line per page in the right category: wikilink + one-line summary. The index is a catalog, not content — keep every entry to one line.

```markdown
# Index

## Entities
- [[entities/google-brain]] — Google's AI research org; introduced the Transformer

## Concepts
- [[concepts/self-attention]] — attention within one sequence; core of Transformers (1 source)

## Sources
- [[sources/attention-is-all-you-need]] — Vaswani et al. 2017; introduced the Transformer

## Analyses
- (filed by wiki-query)
```

### 8. Append to `wiki/log.md`

Append-only, newest last:

```markdown
## [2026-10-20] ingest | Attention Is All You Need
- Wrote [[sources/attention-is-all-you-need]] from raw/attention-is-all-you-need.md
- Created [[entities/google-brain]], [[concepts/self-attention]]; updated [[concepts/seq2seq]]
- Conflict flagged on [[concepts/seq2seq]] (vs [[sources/rnn-notes-2024]]) — awaiting user resolution
```

The `## [YYYY-MM-DD] ingest | <Title>` prefix keeps the log parseable: `grep "^## \[" wiki/log.md | tail -5`.

## Edge cases

- **Schema overrides defaults**: if CLAUDE.md/AGENTS.md at the wiki root (or the existing index.md/log.md structure) defines different conventions, page types, or formats, follow those instead of this skill's defaults.
- **Duplicate or updated edition**: check the index and log before writing. If the new file is a new edition of an already-ingested work, update the existing source page (bump `updated`, note the edition, refresh claims) instead of creating a near-duplicate. Create a separate page only for a genuinely distinct document, and cross-link the two.
- **Low-quality or wiki-contradicting sources**: do not reject them — record reliability notes on the source page, flag contradictions on the affected pages, and let the user weigh the evidence.
- **Non-text sources** (images, data files): reference them from the source page and related pages; view images for context when useful; describe data files from inspection.
- **The wiki is just a git repo of markdown** — don't overengineer. Version history is free.
