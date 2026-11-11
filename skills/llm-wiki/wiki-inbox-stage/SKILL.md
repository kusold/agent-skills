---
name: wiki-inbox-stage
description: Use when staging a URL into the llm-wiki inbox via defuddle.
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Wiki Inbox Stage

Capture a web source into the wiki's `_inbox/` on both the local working
copy and the Forgejo remote, ready for a later `wiki-ingest` pass. One file
per commit; batching is not required. This skill never performs ingestion
(no moving to `raw/`, no wiki page writes).

Activate on requests like "add this URL/article/post to the wiki inbox",
"stage this for the wiki", or "file this into llm-wiki" when the inbox —
not full ingestion — is the target. Sibling skills: `wiki-ingest` (full
ingestion from inbox/raw), `wiki-query`, `wiki-lint`. Load `defuddle` for
extraction details beyond the recap below.

## Environment facts (verified 2026-10-27)

- `defuddle` v0.19.5 is a standalone binary in PATH
  (`/etc/profiles/per-user/hermes/bin/defuddle`). There is NO node/npx on
  this host — never use npx; call `defuddle` directly.
- Local wiki: `/var/lib/hermes/workspace/llm-wiki` — `_inbox/` (staging,
  this skill's target), `raw/` (immutable archive), `wiki/` (pages). Schema:
  `AGENTS.md` at the repo root. The local `.git` history is synthetic; the
  remote is authoritative.
- Remote: Forgejo `mike/llm-wiki` (private, `git.svc.rockymtn.org`, branch
  `main`). No git credentials exist for it — all remote writes go through
  the gitea MCP gateway. Do not attempt `git push`.
- MCP: `https://mcp.svc.rockymtn.org/gitea`, header `X-API-Key` = contents of
  `/var/lib/hermes/.local/share/rockymtn-k8s/mcp-hermes.key` (0600; never
  print it). Small read calls can use the deferred `mcp__gitea__*` tools
  directly; file payloads must go through the bundled script so content
  never transits chat context.

## Workflow

1. **Extract** the URL:
   ```bash
   defuddle parse "<url>" --frontmatter --markdown --output "<tmp>.md"
   ```
   Fetch failures print `Error:` but EXIT 0 — the exit code is not a success
   signal. Fallbacks, in order: 403 → retry once with `--user-agent` set to a
   browser string; empty/SPA output → `curl -sL "<url>" | defuddle parse -
   --markdown`; still failing → report the failure, never fabricate content.
   defuddle is HTML-only: for PDFs or arXiv links use `web_extract` instead
   and record that as the extraction method.
2. **Name the file.** Kebab-case slug of the post title (e.g.
   `lilian-weng-llm-powered-autonomous-agents.md`). GitHub repo-root URLs get
   `<owner> - <repo>.md` (matches existing `raw/` convention). On collision
   with an existing inbox file of different content, add a date suffix —
   never overwrite.
3. **Normalize frontmatter** in the final file. Required fields (merge with
   defuddle's own; these win):
   ```yaml
   ---
   title: <post title>
   author: <full name; keep "Name (@handle)" when only a handle is known — never guess identity>
   source: <original URL>
   site: <domain>
   retrieved: <YYYY-MM-DD from `date +%F`>
   extraction: defuddle 0.19.5 CLI
   ---
   ```
4. **Verify before pushing**: body is real content (>~400 words of body
   text, or an explicitly requested short post noted as such), starts with
   the expected topic, contains no login/paywall/cookie-consent text, and
   frontmatter is complete.
5. **Push** — save the file to `/var/lib/hermes/workspace/llm-wiki/_inbox/`
   first, then run the bundled script (it reads the file from disk, does the
   MCP handshake, commits it to `main`, and verifies):
   ```bash
   python3 "<skill_dir>/scripts/stage_inbox_file.py" \
     /var/lib/hermes/workspace/llm-wiki/_inbox/<slug>.md
   ```
   Commit message defaults to `wiki: stage <slug> in _inbox/ (defuddle
   extraction)` — keep the repo's `wiki: ...` prefix convention. Use
   `--check` to test MCP connectivity without writing anything.
6. **Verify and report**: the script prints the commit sha and confirms the
   file is present in the remote `_inbox/`. Report to the user: local path,
   remote path, commit sha, word count, author, and any extraction caveats.

Multiple URLs: repeat per file, one commit each. If one fails, continue with
the rest and report failures at the end.

## Boundaries

- Never touch `raw/` or `wiki/` on either side; never modify or delete
  existing inbox files on the remote.
- Never print the MCP key. Terminal output redacts `*_API_KEY`-looking
  tokens; verify key files by exact-match compare, not eyeballing.
- Full ingestion stays a separate, user-involved step (`wiki-ingest`, one
  source at a time by default per `AGENTS.md`).
