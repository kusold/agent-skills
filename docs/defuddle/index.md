---
title: 'Defuddle'
description: 'Extract clean article content and metadata from web pages as Markdown with the defuddle CLI.'
weight: 85
---

Extract the readable content of a web page with [defuddle](https://github.com/kepano/defuddle), a CLI that parses HTML from a URL, file, or stdin and returns the main article content with its metadata — navigation, ads, and boilerplate stripped. Where `curl` gives you a raw HTML dump, defuddle gives you text worth reading: Markdown tables, preserved code fences, and structured metadata such as title, author, publish date, and word count.

**Use when:**

- "Extract this article"
- "Convert this page to markdown"
- "Get the main content of this URL"
- "Clean up this HTML"
- "Save a readable snapshot of this link"
- Any request for a page's readable text rather than its raw HTML

## What it does

- Parses a URL, a local HTML file, or stdin (`defuddle parse -`)
- Outputs Markdown (`--markdown`), full metadata JSON (`--json`), or a single field (`--property wordCount` — camelCase, matching the JSON keys)
- Prepends YAML frontmatter (`title`, `site`, `source`, `domain`, `language`, `word_count`) with `--frontmatter`; combined with `--markdown --output <file>` this writes a complete page snapshot in one step
- Retries blocked fetches with a custom user agent (`--user-agent`); accepts a language hint with `--lang`

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Extract the main content of https://example.com/article as markdown
```
```
Save a readable snapshot of this link with frontmatter
```
```
What's the publish date and author of this article?
```

The skill treats each extraction as a claim to verify: fetch errors print but exit 0, so the output is checked directly; empty bodies, login walls, and paywall stubs are reported as failed extractions instead of being summarized as the source. JavaScript-rendered pages that return little content are named as a limitation, with a fallback attempted before giving up.

Defuddle is an external dependency (npm package `defuddle`). Agents run it via `npx --yes defuddle@<version>` with a pinned version when reproducibility matters, and record the version used when an extraction is kept. When defuddle feeds a wiki-ingest URL snapshot, wiki-ingest remains in charge of provenance, retrieval date, and commit discipline.

## Full Skill Definition

See [skills/defuddle/SKILL.md](../../skills/defuddle/SKILL.md) for the complete agent instructions — output-format selection, the verified property list, extraction checks, and boundaries — that the agent loads when this skill is active.
