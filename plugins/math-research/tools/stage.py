#!/usr/bin/env python3
"""Stage controls for a sequential workstream, run as "cmd" tasks by the runner (cwd = the campaign directory).

  stage.py handoff <ws> <archive dir>
      Move ws/<ws>/state.json, HANDOVER.md and steps.jsonl into <archive dir>, so the next task (a blind check or
      review) starts with no author state. The runner's agent rules tell every task to read those files; this
      removes them instead of relying on the prompt. Idempotent: rerunning after an interruption is safe.
      Writes <archive dir>/MOVED.json.

  stage.py gate <out.json> --claims <claims.json> --allow V[,V...] [--require-any V] <verdict.json>...
      Each verdict file is {"claims": {id: verdict}} and must have a matching completion marker (<dir>/*.complete
      written by mark_complete.py, binding its hash). The gate passes only if every file is non-empty, bound,
      gives a verdict for every claim in --claims, and every verdict is in --allow (and, with --require-any, at
      least one verdict equals it). Exit 1 otherwise,
      which fails the task. The gate is deterministic, so once its retries reach max_failures the runner blocks
      the workstream. Writes <out.json>.
"""
import argparse, datetime, glob, hashlib, json, os, shutil, sys


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def write(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path + ".tmp", "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(path + ".tmp", path)


def handoff(ws, archive):
    os.makedirs(archive, exist_ok=True)
    moved = []
    for name in ("state.json", "HANDOVER.md", "steps.jsonl"):
        src = os.path.join("ws", ws, name)
        if os.path.exists(src):
            shutil.move(src, os.path.join(archive, name))
            moved.append(name)
    record = os.path.join(archive, "MOVED.json")
    if os.path.exists(record):  # a rerun after an interruption keeps what the first run moved
        moved = json.load(open(record))["moved"] + moved
    write(record, {"ws": ws, "moved": moved, "t": now()})
    print(f"handoff {ws}: moved {moved or 'nothing (already moved)'} to {archive}")


def gate(out, claims_path, allow, require_any, files):
    problems, verdicts = [], {}
    try:
        ids = [c["id"] for c in json.load(open(claims_path))]
    except (OSError, ValueError, KeyError, TypeError) as e:
        ids = []
        problems.append(f"{claims_path}: unreadable ({e})")
    for p in files:
        try:
            claims = json.load(open(p))["claims"]
        except (OSError, ValueError, KeyError) as e:
            problems.append(f"{p}: unreadable ({e})")
            continue
        sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
        markers = glob.glob(os.path.join(os.path.dirname(p), "*.complete"))
        if not any(json.load(open(m)).get("outputs", {}).get(p) == sha for m in markers):
            problems.append(f"{p}: no completion marker binds its current hash")
        if not claims:
            problems.append(f"{p}: no verdicts")
        unjudged = [i for i in ids if i not in claims]
        if unjudged:
            problems.append(f"{p}: no verdict for claims {unjudged}")
        for cid, v in claims.items():
            verdicts[f"{p}:{cid}"] = v
            if v not in allow:
                problems.append(f"{p}: {cid} = {v}")
    if require_any and require_any not in verdicts.values():
        problems.append(f"no verdict equals {require_any}")
    write(out, {"pass": not problems, "problems": problems, "verdicts": verdicts, "t": now()})
    print("GATE PASS" if not problems else "GATE FAIL: " + "; ".join(problems))
    return 0 if not problems else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("handoff")
    h.add_argument("ws")
    h.add_argument("archive")
    g = sub.add_parser("gate")
    g.add_argument("out")
    g.add_argument("--claims", required=True)
    g.add_argument("--allow", required=True)
    g.add_argument("--require-any")
    g.add_argument("files", nargs="+")
    a = ap.parse_args()
    if a.cmd == "handoff":
        handoff(a.ws, a.archive)
    else:
        sys.exit(gate(a.out, a.claims, a.allow.split(","), a.require_any, a.files))
