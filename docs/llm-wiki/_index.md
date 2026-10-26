---
title: 'LLM Wiki'
description: 'Build, query, and maintain a persistent, LLM-maintained wiki: ingest sources with provenance, answer questions with citations, and health-check the knowledge base.'
weight: 30
bookCollapseSection: true
---

Skills for building and maintaining a persistent, LLM-maintained knowledge wiki (the LLM Wiki pattern), grouped under `skills/llm-wiki/` in the repository.

- [Wiki Ingest](wiki-ingest/) — read sources fully and compile them into wiki pages with provenance
- [Wiki Lint](wiki-lint/) — periodic health-check: contradictions, orphans, stale claims, index drift
- [Wiki Query](wiki-query/) — answer questions from wiki pages with citations

## The core idea

The LLM Wiki pattern comes from [a gist that Andrej Karpathy wrote in April 2026](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). It shows how to build a personal knowledge base with an LLM.

Most LLM knowledge tools use retrieval. You upload your sources, and the tool re-reads them each time you ask a question. The knowledge does not persist between questions.

The wiki pattern takes a different path. The LLM writes and maintains a set of linked markdown pages. These pages sit between you and the raw sources. When the LLM ingests a source, it writes a summary, adds cross-references, and flags contradictions. This work happens once, not at every question. Karpathy calls the result "a persistent, compounding artifact": the wiki grows with every source you add.

The roles are clear. You supply the sources and ask the questions. The LLM does the maintenance: summaries, entity and concept pages, index updates, and log entries. This bookkeeping is the work that kills human-maintained wikis. LLMs do not get bored, and one ingest pass can touch 10 to 15 pages.

The pattern has three layers:

1. **Raw sources** — files that do not change. They are the source of truth.
2. **The wiki** — markdown pages that the LLM owns and maintains.
3. **The schema** — a config file (`CLAUDE.md` or `AGENTS.md`) that sets the rules and workflows.

It has three operations: **ingest** a new source, **query** the wiki, and **lint** it for contradictions, orphans, and stale claims. Good query answers go back into the wiki. The three skills in this section implement these operations.

Karpathy pairs the agent with Obsidian: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase." The idea goes back to Vannevar Bush's 1945 Memex. Bush did not answer who maintains the collected memory. LLMs now fill that role.
