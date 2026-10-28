#!/usr/bin/env python3
"""Default acceptance check for a task that declares no checker of its own.
Usage: manifest_check.py <output>...   (run from the campaign directory)
Every declared output must exist and be non-empty, and every .json output must parse. Exit 0 iff all hold.
With this check, no task becomes done without a receipt binding its outputs."""
import json, os, sys

bad = []
for p in sys.argv[1:]:
    if not os.path.isfile(p) or os.path.getsize(p) == 0:
        bad.append(f"{p}: missing or empty")
    elif p.endswith(".json"):
        try:
            json.load(open(p))
        except ValueError as e:
            bad.append(f"{p}: invalid JSON ({e})")
print("\n".join(bad) if bad else f"manifest OK: {len(sys.argv) - 1} outputs")
sys.exit(1 if bad or len(sys.argv) < 2 else 0)
