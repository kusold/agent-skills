---
title: 'Wiki Inbox Stage'
description: 'Stage a web source into the llm-wiki inbox: defuddle extraction, provenance frontmatter, and a single-file commit to the Forgejo remote.'
weight: 20
---

Stage a web source into the LLM wiki's `_inbox/` on both the local working copy and the Forgejo remote, ready for a later [wiki-ingest](../wiki-ingest/) pass. Given a URL, the skill extracts the article with the `defuddle` CLI, verifies the extraction is real content, writes it with provenance frontmatter (title, author, source URL, site, retrieval date, extraction method), and pushes it to the `mike/llm-wiki` repo on `git.svc.rockymtn.org` as a single-file commit through the gitea MCP gateway — no git credentials needed. One file per commit by design; batching is not required.

**Use when:**

- "Add this URL/article/post to the wiki inbox"
- "Stage this for the wiki"
- "File this into llm-wiki" (meaning the inbox, not full ingestion)

**What it does:**

- Extracts clean markdown with `defuddle parse <url> --frontmatter --markdown`, with fallbacks: browser user-agent retry on 403, `curl | defuddle parse -` for JS-heavy pages, and honest failure reporting (fetch failures exit 0, so output is always verified — never trust the exit code)
- Names files as kebab-case slugs; GitHub repo-root URLs follow the `<owner> - <repo>.md` convention
- Normalizes frontmatter to the required fields, never guessing author identity (handles stay as `Name (@handle)`)
- Pushes via the bundled `stage_inbox_file.py`: MCP handshake against the gitea gateway, single-file `create_or_update_file` commit to `main` with the repo's `wiki: ...` message convention, then verifies the file landed and reports the commit sha
- Refuses to overwrite existing remote files and refuses files outside `_inbox/`
- Never touches `raw/` or `wiki/` — full ingestion stays a separate, user-involved step
