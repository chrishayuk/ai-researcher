#!/usr/bin/env python3
"""Write a completion marker that binds the exact bytes of a task's final outputs.
Usage (run from the campaign directory, as an agent's very last action):
  python3 -I ../tools/mark_complete.py <marker path> <output>...
The marker is JSON: {"outputs": {"<path>": "<sha256>", ...}, "t": "<UTC time>"}. The runner accepts a task only if
the marker lists every declared output and every listed hash still matches the file. The acceptance receipt
then binds the same hashes. A stale marker (any output changed after it was written) means the task is not done.
"""
import datetime, hashlib, json, os, sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
marker, outs = sys.argv[1], sys.argv[2:]
missing = [p for p in outs if not os.path.isfile(p)]
if missing:
    sys.exit(f"not writing marker: missing outputs {missing}")
h = {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in outs}
tmp = marker + ".tmp"
with open(tmp, "w") as f:
    json.dump({"outputs": h, "t": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}, f, indent=1)
os.replace(tmp, marker)
print(f"marker {marker}: {len(h)} outputs bound")
