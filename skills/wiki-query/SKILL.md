---
name: wiki-query
description: Answer questions from an LLM-maintained wiki with citations and optionally save durable analyses; use for "what does the wiki say", "search my wiki", "what have I read about", or comparisons grounded in an explicitly requested or established wiki workflow.
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Wiki Query

Answer questions from the LLM Wiki — a persistent, interlinked knowledge base that the LLM builds and maintains from raw sources whose content is immutable (`tags` and `description` frontmatter fields may change; ingestion may also replace generic X post frontmatter titles when archiving and label unlabeled Mermaid fences) (Karpathy's "LLM Wiki" pattern). Start with the wiki rather than re-reading raw sources. Use its cross-references and summaries, but verify citations and surface gaps or contradictions you discover; maintenance may be incomplete. File valuable answers back into the wiki so explorations compound instead of disappearing into chat history.

## Default wiki layout

```
<wiki-root>/
  CLAUDE.md                  # or AGENTS.md — the schema: conventions for THIS wiki
  _inbox/                    # incoming sources; wiki-ingest moves them to raw/
  raw/                       # immutable source content; editable tags and description frontmatter
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

**The wiki's schema overrides these defaults.** If a CLAUDE.md/AGENTS.md schema exists at the wiki root (or index.md/log.md already follow a different structure), use the wiki's own conventions — categories, page formats, citation style — over everything below.

Start with the user's explicit path and available project instructions. Read existing `CLAUDE.md`/`AGENTS.md` conventions before looking for `wiki/index.md`; the schema may specify a different wiki directory or catalog name. Project indexes under `wiki/projects/` belong to the same wiki; they are not separate wiki roots. If multiple candidate wikis remain, ask which one to use. Paths below describe the default layout; substitute the schema's configured paths.

## Workflow

### 1. Read `wiki/index.md` first

The index is the catalog: every page with a wikilink and one-line summary, organized by category. Select relevant pages from it, including domain syntheses and project indexes. The global catalog includes project supporting pages as well as their indexes.

If no wiki exists after checking the user's path and schema, suggest **wiki-ingest** to bootstrap it. Do not create a wiki or index as part of answering a query. If wiki pages exist but their configured catalog is missing, search the pages directly and report the missing catalog; do not treat the wiki as nonexistent. Saving an analysis in an existing wiki is handled in step 5.

### 2. Read the relevant pages

Open the selected pages and follow `[[wikilinks]]` (page name = filename) as needed — domain → concept → source and project index → architecture/workflow/decisions → source chains are normal for multi-hop questions. For project questions, read its index and relevant supporting pages; for broad topic questions, consult the domain page and verify its supporting evidence. Distinguish proposed and adopted project decisions. Use qualified links such as `[[projects/home-lab/decisions]]` and `[[projects/llm-wiki/index]]` to avoid ambiguous shared filenames.

If the index looks stale or incomplete, fall back to searching the wiki directly:

```bash
rg -ni --fixed-strings -- "<term>" wiki/
```

Use any pages the search finds that the index missed, and report the catalog drift. Suggest **wiki-lint** for repair if available.

### 3. Synthesize an answer with citations

Every substantive claim links to the wiki page that backs it — and through that page to its source summary (`[[sources/some-article]]`) and raw file (`raw/some-article.md`).

Label what each part of the answer is. Never present a gap as knowledge:

- **Sourced** — the wiki backs it. Cite the page: `[[entities/postgresql]]`.
- **Inference** — you are constructing it from wiki content. Say so: "Synthesizing from [[concepts/cap-theorem]] and [[sources/brewer-keynote]], it follows that..."
- **Coverage gap** — the wiki doesn't cover it. Say so plainly: "The wiki doesn't cover X yet — want to ingest a source on it?"

### 4. Match the output form to the ask

Default to a plain markdown answer. Offer alternatives when they fit; don't force a format:

- **Comparison table** — "compare X and Y" across dimensions.
- **Marp slide deck** — the user wants to present or share (markdown with Marp frontmatter).
- **matplotlib chart** — quantitative answers where a figure communicates better.

These formats are query-time outputs, not stored wiki structure — unless the result is durable (next step).

### 5. File durable answers back into the wiki

When the answer is a durable artifact — a comparison, analysis, timeline, discovered connection — offer to save it (or save it directly if the user's workflow clearly wants that; ask when unsure):

1. Write `wiki/analyses/<slug>.md` (kebab-case slug) with frontmatter and wikilinks to everything it draws on:

   ```markdown
   ---
   type: analysis
   created: 2026-10-20
   updated: 2026-10-20
   sources:
     - "[[sources/postgres-vs-sqlite-benchmarks]]"
     - "[[sources/sqlite-docs]]"
   ---

   # Postgres vs SQLite for edge deployments

   Drawn from [[entities/postgresql]], [[entities/sqlite]], and [[concepts/embedded-databases]].

   ...the synthesis, each claim linked to its evidence...
   ```

2. Update `wiki/index.md`: add a line under the Analyses category:
   `- [[analyses/postgres-vs-sqlite-for-edge-deployments]] — one-line summary`

   Link the analysis from relevant domain pages and project indexes when it adds useful context. Update project supporting pages only when the requested save includes those changes; do not turn an analysis into an adopted project decision.

3. Append to `wiki/log.md` (ISO date from the actual current date):

   ```
   ## [2026-10-20] query | Postgres vs SQLite for edge deployments
   ```

Only file genuine syntheses. Casual Q&A stays in chat — no page, no log entry — so the log stays signal-rich (`grep "^## \[" wiki/log.md | tail -5` should show real work, not chatter).

## Edge cases

- **Wiki can't answer at all** — say so plainly, then suggest specific sources to ingest. Gap discovery is a feature of querying, not a failure. Hand off to wiki-ingest.
- **Conflicting information between pages** — surface the conflict: quote each claim with its citation and note which source is newer or more reliable. Do not average away contradictions.
- **Question about a specific source** — go straight to its `wiki/sources/` page; the raw file under `raw/` is there for deeper verification.
- **Multi-hop questions** — expected. Chain pages via wikilinks until the hops connect; the index is the entry point, not the whole map.

## Sibling skills

- **wiki-ingest** — processes new sources into wiki pages; also bootstraps the wiki. Run it first if no wiki exists.
- **wiki-lint** — periodic health-check (contradictions, orphans, stale claims); it fixes the index drift that queries discover.
