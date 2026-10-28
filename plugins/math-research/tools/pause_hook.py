#!/usr/bin/env python3
"""PreToolUse hook that enforces a pause, and a blind task's hidden paths, in the harness instead of relying on
the agent to comply.

The runner installs it in every agent session (claude --settings).

Pause. While any file in $CAMPAIGN_PAUSE_FILES exists, the only tool calls allowed are reading and writing the
workstream's own checkpoint files (ws/<W>/state.json, HANDOVER.md, steps.jsonl and their .tmp copies), plus a
single simple shell command (ls, cat, test, echo, printf, head, tail, wc, mv) with no separators, newlines or
substitutions, whose redirection targets and mv arguments are all checkpoint files. Everything else is refused,
and the refusal tells the agent to save its state and reply PAUSED. Found necessary by G0 v4: an agent saw the
pause file and ran a step anyway.

Hidden paths. $CAMPAIGN_HIDDEN lists paths, relative to the campaign, that a blind task must not read (the
author's src/, NOTES.md, RESULT.md, the run records and the ledgers). Read calls on or under them are refused,
so are Glob and Grep searches that would reach them, and so is any shell command that names one or names
Claude Code's session transcripts. This stops direct reads. It is not a sandbox: an agent determined to get
round it (a wildcard, a script that builds the path) still could.
"""
import json, os, re, shlex, sys

pause_files = [p for p in os.environ.get("CAMPAIGN_PAUSE_FILES", "").split(os.pathsep) if p]
hidden = [p for p in os.environ.get("CAMPAIGN_HIDDEN", "").split(os.pathsep) if p]
root, ws = os.environ.get("CAMPAIGN_ROOT", ""), os.environ.get("CAMPAIGN_WS", "")
wsdir = os.path.realpath(os.path.join(root, "ws", ws))
CKPT = {"state.json", "HANDOVER.md", "steps.jsonl", "state.json.tmp", "HANDOVER.md.tmp", "steps.jsonl.tmp"}
READ_ONLY = ("ls", "cat", "test", "echo", "printf", "head", "tail", "wc")


def refuse(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def real(p):
    return os.path.realpath(os.path.join(root, os.path.expanduser(p)))


def inside(p, top):
    return p == top or p.startswith(top + os.sep)


def allowed_path(p):
    p = real(p)
    if p in map(os.path.realpath, pause_files):
        return True
    return os.path.dirname(p) == wsdir and os.path.basename(p) in CKPT


def names(h):
    """The ways a shell command could name hidden path h: the path itself, its last two parts, and a file's name."""
    parts = os.path.normpath(h).split(os.sep)
    out = {os.path.normpath(h), os.sep.join(parts[-2:])}
    if "." in parts[-1]:
        out.add(parts[-1])
    return out


d = json.load(sys.stdin)
tool, inp = d.get("tool_name", ""), d.get("tool_input", {}) or {}
cmd = inp.get("command", "") if tool == "Bash" else ""

if hidden:
    tops = [real(h) for h in hidden]
    path = inp.get("file_path") or inp.get("notebook_path") or inp.get("path")
    blocked = False
    if tool in ("Read", "NotebookRead") and path:
        blocked = any(inside(real(path), t) for t in tops)
    elif tool in ("Glob", "Grep"):
        base = real(path or ".")
        blocked = any(inside(base, t) or inside(t, base) for t in tops)  # the search would reach a hidden path
    elif cmd:
        # the body of a `cat > file <<EOF` heredoc is text being written, not a path being read (a checker's
        # CHECK.md saying "I did not read NOTES.md"); heredocs fed to any other command are still scanned
        text = re.sub(r"(cat\s*(?:>>?\s*\S+\s*)?<<-?\s*['\"]?(\w+)['\"]?(?:\s*>>?\s*\S+)?[^\n]*\n).*?\n\2(?=\n|$)",
                      r"\1", cmd, flags=re.S).replace("\\", "")
        blocked = ".claude/projects" in text or any(
            re.search(r"(?<![\w.-])" + re.escape(n) + r"(?![\w-])", text) for h in hidden for n in names(h))
    if blocked:
        refuse("This is a blind task. The author's working files are hidden from it: " + ", ".join(hidden) +
               ". Read only what your prompt lists, and give Glob and Grep a path inside the files you may read. A shell "
               "command that names a hidden file is refused even in text it writes: write files with the Write tool.")

if not any(os.path.exists(p) for p in pause_files):
    sys.exit(0)

ok = False
if tool in ("Read", "Write", "Edit"):
    ok = allowed_path(inp.get("file_path", ""))
elif tool in ("Glob", "Grep", "LS"):
    ok = True
elif tool == "Bash" and not re.search(r"[;&|`\n\r]|\$\(|<\(", cmd):
    targets = re.findall(r">>?\s*([^\s>]+)", cmd)
    try:
        words = shlex.split(re.sub(r">>?\s*[^\s>]+", " ", cmd))
    except ValueError:
        words = []
    args = [w for w in words[1:] if not w.startswith("-")]
    if words and all(allowed_path(t) for t in targets):
        if words[0] in READ_ONLY:
            ok = True
        elif words[0] == "mv":
            ok = bool(args) and all(allowed_path(a) for a in args)
if ok:
    sys.exit(0)
refuse("This campaign workstream is PAUSED. Only reading and updating ws/<W>/state.json, HANDOVER.md and "
       "steps.jsonl is allowed. Bring them up to date, then reply with the single word PAUSED and stop.")
