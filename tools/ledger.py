#!/usr/bin/env python3
"""Attribution ledger: claims and ideas are recorded when they first appear, not reconstructed later.

Usage (run from the campaign directory; the ledger is <campaign>/ledger.jsonl):
  python3 -I ../../tools/ledger.py add --actor <user|operator|agent:NAME> --kind <idea|claim|result|failure|decision>
                                 --text "<one sentence>" --evidence "<transcript line / file>"
  python3 -I ../../tools/ledger.py show
Entries are append-only. A correction is a new entry with --kind correction that names the entry number it corrects.
"""
import argparse, datetime, json, os, sys

LOG = "ledger.jsonl"
KINDS = {"idea", "claim", "result", "failure", "decision", "correction"}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--actor", required=True)
    a.add_argument("--kind", required=True, choices=sorted(KINDS))
    a.add_argument("--text", required=True)
    a.add_argument("--evidence", required=True)
    sub.add_parser("show")
    args = ap.parse_args()
    if args.cmd == "show":
        if os.path.exists(LOG):
            for i, line in enumerate(open(LOG), 1):
                r = json.loads(line)
                print(f"{i:3} {r['t']} {r['actor']:<28} {r['kind']:<10} {r['text']}")
        return 0
    if not (args.actor in ("user", "operator") or args.actor.startswith("agent:")):
        sys.exit("actor must be user, operator or agent:NAME")
    rec = {"t": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "actor": args.actor, "kind": args.kind, "text": args.text, "evidence": args.evidence}
    with open(LOG, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
