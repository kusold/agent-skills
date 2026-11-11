#!/usr/bin/env python3
"""Push one local _inbox/ file to Forgejo mike/llm-wiki main via the gitea MCP
gateway, then verify it landed. Single-file commit by design.

Usage:
  stage_inbox_file.py <path-under-wiki-_inbox>.md [custom commit message]
  stage_inbox_file.py --check        # MCP handshake + list _inbox, no writes
"""
import json, subprocess, os, sys

URL = "https://mcp.svc.rockymtn.org/gitea"
KEY_PATH = "/var/lib/hermes/.local/share/rockymtn-k8s/mcp-hermes.key"
LOCAL_WIKI = "/var/lib/hermes/workspace/llm-wiki"
OWNER, REPO, BRANCH = "mike", "llm-wiki", "main"

KEY = open(KEY_PATH).read().strip()
session = None
_id = [0]


def post(payload, capture_headers=False):
    global session
    cmd = ["curl", "-s", "--max-time", "300", "-X", "POST", URL,
           "-H", "Content-Type: application/json",
           "-H", "Accept: application/json, text/event-stream",
           "-H", "X-API-Key: " + KEY]
    if capture_headers:
        cmd.append("-i")
    if session:
        cmd += ["-H", "mcp-session-id: " + session]
    cmd += ["--data-binary", "@-"]
    p = subprocess.run(cmd, input=json.dumps(payload).encode(), capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    if capture_headers:
        for line in out.splitlines():
            if line.lower().startswith("mcp-session-id:"):
                session = line.split(":", 1)[1].strip()
        if "\r\n\r\n" in out:
            out = out.split("\r\n\r\n", 1)[1]
        elif "\n\n" in out:
            out = out.split("\n\n", 1)[1]
    for line in reversed([l[5:].strip() for l in out.splitlines() if l.startswith("data:")]):
        try:
            return json.loads(line)
        except Exception:
            continue
    if not out.strip():
        return {"ok": True, "empty": True}  # 202 Accepted, empty body (notifications)
    try:
        return json.loads(out)
    except Exception:
        raise RuntimeError("unparseable MCP response: " + out[:300])


def call_tool(name, args):
    _id[0] += 1
    r = post({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
              "params": {"name": name, "arguments": args}})
    if "error" in r:
        raise RuntimeError("jsonrpc error: " + json.dumps(r["error"])[:500])
    res = r.get("result", {})
    text = " ".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
    if res.get("isError"):
        raise RuntimeError("tool error: " + text[:500])
    return text


post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                 "clientInfo": {"name": "wiki-inbox-stage", "version": "1.0"}}},
     capture_headers=True)
post({"jsonrpc": "2.0", "method": "notifications/initialized"})

if "--check" in sys.argv:
    entries = json.loads(call_tool("get_dir_contents",
                                   {"owner": OWNER, "repo": REPO, "ref": BRANCH, "path": "_inbox"}))
    print(f"MCP OK; remote _inbox has {len([e for e in entries if e['type'] == 'file'])} files")
    sys.exit(0)

if len(sys.argv) < 2:
    sys.exit("usage: stage_inbox_file.py <wiki>/_inbox/<slug>.md [commit message] | --check")

local = os.path.abspath(sys.argv[1])
inbox = os.path.join(LOCAL_WIKI, "_inbox")
if not (local.startswith(inbox + os.sep) and local.endswith(".md") and os.path.isfile(local)):
    sys.exit(f"refusing: {local} is not a .md file inside {inbox}")
rel = "_inbox/" + os.path.basename(local)
slug = os.path.basename(local)[:-3]
message = sys.argv[2] if len(sys.argv) > 2 else f"wiki: stage {slug} in _inbox/ (defuddle extraction)"

# collision check: never overwrite an existing remote file
try:
    call_tool("get_file_contents", {"owner": OWNER, "repo": REPO, "path": rel})
    sys.exit(f"refusing: {rel} already exists on the remote (never overwrite; pick a distinct name)")
except RuntimeError:
    pass  # 404-ish tool error = path is free

content = open(local, encoding="utf-8").read()
print(f"pushing {rel} ({len(content)} chars) ...")
out = call_tool("create_or_update_file", {
    "owner": OWNER, "repo": REPO, "branch_name": BRANCH, "message": message,
    "files": [{"path": rel, "content": content}]})
print("server:", out[:200])

# verify: file present + new HEAD commit
entries = json.loads(call_tool("get_dir_contents",
                               {"owner": OWNER, "repo": REPO, "ref": BRANCH, "path": "_inbox"}))
remote_names = [e["name"] for e in entries if e["type"] == "file"]
head = json.loads(call_tool("list_commits", {"owner": OWNER, "repo": REPO, "sha": BRANCH, "per_page": 1}))[0]

ok = os.path.basename(local) in remote_names
print(f"verify: file on remote = {ok} | HEAD {head['sha'][:10]}: {head['message'].strip()[:80]}")
print(f"local : {local}")
print(f"remote: https://git.svc.rockymtn.org/{OWNER}/{REPO}/src/branch/{BRANCH}/{rel}")
sys.exit(0 if ok else 1)
