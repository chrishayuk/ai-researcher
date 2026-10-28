#!/usr/bin/env python3
"""Acceptance receipts. Every acceptance is a receipt that binds the exact bytes involved: inputs, checker, outputs.

A receipt records: the SHA-256 of every input file, the SHA-256 of every checker file (the checker version),
the command, its exit status, and the SHA-256 of every output file after the run. A result is ACCEPTED only
while all of those hashes still match. Any later change makes the receipt INVALID: this is a failure, not a
warning, and `verify` exits 1.

Usage (paths relative to the current directory):
  verify.py run <name> --inputs P... --checker P... [--outputs P...] -- <check command...>
      Rejected if the check exits non-zero, or if any input or checker file changed while it ran.
      If a VALID receipt for <name> already exists, nothing is re-run and no second receipt is written.
  verify.py verify [<name>]     exit 0 iff every ACCEPTED receipt (or <name>'s) is still VALID
  verify.py status <name>       prints ACCEPTED | INVALID | NONE; exit 0 only for ACCEPTED
Receipts: receipts.jsonl (append-only).
"""
import datetime, hashlib, json, os, subprocess, sys

LOG = "receipts.jsonl"


def files_of(path):
    if os.path.isdir(path):
        out = []
        for d, dirs, fs in os.walk(path):
            dirs[:] = sorted(x for x in dirs if x != "__pycache__")
            out += [os.path.join(d, f) for f in sorted(fs) if f != ".DS_Store"]
        return out
    return [path] if os.path.exists(path) else []


def digest(paths):
    h = {}
    for p in paths:
        fs = files_of(p)
        if not fs:
            # an empty directory is a real, bound input (a proof-only result has an empty certs/); only a path
            # that does not exist is missing
            h[p] = "EMPTY DIRECTORY" if os.path.isdir(p) else "MISSING"
        for f in fs:
            with open(f, "rb") as fh:
                h[f] = hashlib.sha256(fh.read()).hexdigest()
    return h


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def receipts(name=None):
    if not os.path.exists(LOG):
        return []
    out = []
    for line in open(LOG):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:  # torn final line after a crash
            continue
        if r.get("status") == "ACCEPTED" and (name is None or r["name"] == name):
            out.append(r)
    return out


def check_receipt(r):
    """Return the list of paths whose current hash differs from the receipt."""
    diff = []
    for key in ("inputs", "checker", "outputs"):
        roots = r["roots"][key]
        cur = digest(roots)
        diff += sorted(p for p in set(cur) | set(r[key]) if cur.get(p) != r[key].get(p))
    return diff


def append(rec):
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
        f.flush()
        os.fsync(f.fileno())


def run(argv):
    name = argv[0]
    j = argv.index("--")
    opts, cmd = argv[1:j], argv[j + 1:]
    groups, key = {"--inputs": [], "--checker": [], "--outputs": []}, None
    for a in opts:
        if a in groups:
            key = a
        elif key:
            groups[key].append(a)
        else:
            sys.exit("unexpected argument " + a)
    if not groups["--inputs"] or not groups["--checker"] or not cmd:
        sys.exit("need --inputs, --checker and -- <command>")
    valid = [r for r in receipts(name) if not check_receipt(r)]
    if valid:
        print(f"ALREADY_ACCEPTED: {name} (receipt {valid[-1]['receipt_id']}); not re-run")
        return 0
    ins, chk = digest(groups["--inputs"]), digest(groups["--checker"])
    t0 = now()
    r = subprocess.run(cmd, capture_output=True, text=True)
    ins2, chk2 = digest(groups["--inputs"]), digest(groups["--checker"])
    outs = digest(groups["--outputs"])
    out = r.stdout + r.stderr
    changed = ins != ins2 or chk != chk2
    missing = [p for p, h in {**ins, **chk}.items() if h == "MISSING"]
    ok = r.returncode == 0 and not changed and not missing
    rec = {"receipt_id": hashlib.sha256((name + t0 + json.dumps(ins, sort_keys=True)).encode()).hexdigest()[:16],
           "name": name, "status": "ACCEPTED" if ok else "REJECTED", "started": t0, "finished": now(),
           "cmd": cmd, "exit": r.returncode, "changed_during_check": changed, "missing": missing,
           "roots": {"inputs": groups["--inputs"], "checker": groups["--checker"], "outputs": groups["--outputs"]},
           "inputs": ins, "checker": chk, "outputs": outs,
           "check_output_sha256": hashlib.sha256(out.encode()).hexdigest(), "check_output_tail": out[-1500:]}
    append(rec)
    print(f"{rec['status']}: {name} receipt {rec['receipt_id']} ({len(ins)} inputs, {len(chk)} checker files, "
          f"{len(outs)} outputs, exit {r.returncode})")
    return 0 if ok else 1


def verify(argv):
    rs = receipts(argv[0] if argv else None)
    if not rs:
        print("NONE")
        return 1
    bad = 0
    for r in rs:
        diff = check_receipt(r)
        bad += bool(diff)
        print(("VALID" if not diff else "INVALID") + f": {r['name']} receipt {r['receipt_id']} ({r['finished']})"
              + (f" changed: {diff[:6]}" if diff else ""))
    return 1 if bad else 0


def status(argv):
    rs = receipts(argv[0])
    if not rs:
        print("NONE")
        return 1
    if any(not check_receipt(r) for r in rs):
        print("ACCEPTED")
        return 0
    print("INVALID")
    return 1


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"run": run, "verify": verify, "status": status}
    if not a or a[0] not in cmds:
        sys.exit(__doc__)
    sys.exit(cmds[a[0]](a[1:]))
