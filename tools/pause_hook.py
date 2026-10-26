#!/usr/bin/env python3
"""PreToolUse hook that enforces a pause in the harness instead of relying on the agent to comply.

The runner installs it in every agent session (claude --settings). While any file in $CAMPAIGN_PAUSE_FILES
exists, the only tool calls allowed are reading and writing the workstream's own checkpoint files
(ws/<W>/state.json, HANDOVER.md, steps.jsonl and their .tmp copies), plus simple single shell commands (ls, cat,
mv, test, echo, printf, head, tail, wc) that touch nothing else. Everything else is refused, and the refusal
tells the agent to save its state and reply PAUSED. Found necessary by G0 v4: an agent saw the pause file and
ran a step anyway.
"""
import json, os, re, shlex, sys

pause_files = [p for p in os.environ.get("CAMPAIGN_PAUSE_FILES", "").split(os.pathsep) if p]
if not any(os.path.exists(p) for p in pause_files):
    sys.exit(0)
root, ws = os.environ.get("CAMPAIGN_ROOT", ""), os.environ.get("CAMPAIGN_WS", "")
wsdir = os.path.realpath(os.path.join(root, "ws", ws))
CKPT = {"state.json", "HANDOVER.md", "steps.jsonl", "state.json.tmp", "HANDOVER.md.tmp", "steps.jsonl.tmp"}


def allowed_path(p):
    p = os.path.realpath(os.path.join(root, p))
    if p in map(os.path.realpath, pause_files):
        return True
    return os.path.dirname(p) == wsdir and os.path.basename(p) in CKPT


d = json.load(sys.stdin)
tool, inp = d.get("tool_name", ""), d.get("tool_input", {}) or {}
ok = False
if tool in ("Read", "Write", "Edit"):
    ok = allowed_path(inp.get("file_path", ""))
elif tool in ("Glob", "Grep", "LS"):
    ok = True
elif tool == "Bash":
    cmd = inp.get("command", "")
    if not re.search(r"[;&|`]|\$\(", cmd):
        try:
            words = shlex.split(cmd.replace(">>", " ").replace(">", " "))
        except ValueError:
            words = []
        if words and words[0] in ("ls", "cat", "mv", "test", "echo", "printf", "head", "tail", "wc"):
            paths = [w for w in words[1:] if "/" in w or "." in w]
            ok = words[0] in ("ls", "test") or all(allowed_path(w) for w in paths if not w.startswith("-")
                                                    and not w.startswith("{") and not w.startswith('"'))
if ok:
    sys.exit(0)
print("This campaign workstream is PAUSED. Only reading and updating ws/<W>/state.json, HANDOVER.md and "
      "steps.jsonl is allowed. Bring them up to date, then reply with the single word PAUSED and stop.", file=sys.stderr)
sys.exit(2)
