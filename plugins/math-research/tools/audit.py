#!/usr/bin/env python3
"""Evidence audit: what may you believe about a finished campaign?

  audit.py campaigns/NAME            prints the report and writes campaigns/NAME/AUDIT.md

Deterministic, no AI. It keeps three questions apart:
  integrity     are the bound files unchanged?   (frozen hashes, campaign.json hash, every receipt re-verified)
  verification  what did the blind check and the adversarial review actually say about each claim?
  status        the status each claim earns from those verdicts, which may be lower than the author proposed

Status rules (the author's proposed status never counts):
  any check FAIL / INSUFFICIENT, or any review ERROR FOUND        -> Refuted or failed claim
  finite-certificate, check PASS, review absent or NO ERROR FOUND  -> Independently reproduced computation
  proof, review NO ERROR FOUND, every dependency earned its status -> Reviewed proof; no error found
  anything else (conjectures, negative searches, unchecked claims) -> Unverified
Evidence counts only if an ACCEPTED receipt binds the file's current bytes: verdicts from a task that failed,
or files changed since, are ignored and flagged. Refutations are read leniently ("ERROR FOUND: off by one",
"fail") and credit strictly (only the exact strings): an unrecognised verdict can lower a claim, never lift it.
A claim id used twice earns Unverified for every copy.
A receipt certifies integrity, never correctness: a review reporting ERROR FOUND is still an ACCEPTED task.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK_V = {"PASS", "FAIL", "INSUFFICIENT", "CANNOT CHECK", "NOT FINITE"}
REVIEW_V = {"ERROR FOUND", "NO ERROR FOUND", "CANNOT ASSESS"}
RANK = {"Unverified": 0, "Unverified conjecture": 0, "Refuted claim": 0, "Refuted or failed claim": 0,
        "Independently reproduced computation": 1, "Reviewed proof": 2, "Reviewed proof; no error found": 2}


def load(path, default):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return default


def refutes(name, v):
    """Lenient: anything that reads as a failure or an error found refutes the claim."""
    v = str(v).strip().upper()
    if name == "check":
        return v.startswith(("FAIL", "INSUFFICIENT"))
    return "ERROR FOUND" in v and "NO ERROR FOUND" not in v


def bound_files(camp):
    """{path: sha256} for every output an ACCEPTED receipt bound, kept only while the file still has those bytes."""
    out = {}
    try:
        lines = open(os.path.join(camp, "receipts.jsonl")).read().splitlines()
    except OSError:
        return out
    for line in lines:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("status") != "ACCEPTED":
            continue
        for path, h in (r.get("outputs") or {}).items():
            f = os.path.join(camp, path)
            if os.path.isfile(f) and hashlib.sha256(open(f, "rb").read()).hexdigest() == h:
                out[path] = h
    return out


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main(camp):
    spec = load(os.path.join(camp, "campaign.json"), None)
    if spec is None:
        sys.exit(f"no campaign.json in {camp}")
    out, flags = [f"# Audit of campaign {spec['name']}", ""], []

    # integrity
    out += ["## Integrity", ""]
    frozen = open(os.path.join(camp, "campaign.sha256")).read().split()[0]
    same =run(["shasum", "-a", "256", "campaign.json"], camp)[1].split()[0] == frozen
    out.append(f"- campaign.json matches its frozen hash: {'yes' if same else 'NO'}")
    for chk in spec.get("integrity_checks", []):
        code, txt = run(chk["cmd"], camp)
        out.append(f"- {chk['name']}: {'ok' if code == 0 else 'FAILED ' + txt[-200:]}")
        if code:
            flags.append(f"integrity check failed: {chk['name']}")
    code, txt = run([sys.executable, "-I", os.path.join(HERE, "verify.py"), "verify"], camp)
    lines = [l for l in txt.splitlines() if l.startswith(("VALID", "INVALID"))]
    bad = [l for l in lines if l.startswith("INVALID")]
    out.append(f"- receipts: {len(lines) - len(bad)} VALID, {len(bad)} INVALID")
    flags += ["receipt " + l for l in bad]
    if not same:
        flags.append("campaign.json changed after it was frozen")
    _, st = run([sys.executable, "-I", os.path.join(HERE, "runner.py"), "--campaign", ".", "status"], camp)
    out += ["", "```", st, "```", ""]

    # verification and status, per workstream
    bound = bound_files(camp)

    def evidence(rel, default):
        """A file's content, only if an accepted receipt binds its current bytes."""
        if not os.path.exists(os.path.join(camp, rel)):
            return default
        if rel not in bound:
            flags.append(f"{rel} is not bound by an ACCEPTED receipt (its task failed, or it changed since); ignored")
            return default
        return load(os.path.join(camp, rel), default)

    for w in spec["workstreams"]:
        base = f"ws/{w}"
        claims = evidence(f"{base}/research/claims.json", None)
        check = (evidence(f"{base}/check/check.json", {}) or {}).get("claims", {})
        review = (evidence(f"{base}/review/review.json", {}) or {}).get("claims", {})
        out += [f"## Claims of workstream {w}", ""]
        if claims is None:
            out += ["No accepted claims.json: the research task has not finished and been accepted.", ""]
            flags.append(f"{w}: research not finished")
            continue
        if not claims:
            out += ["No claims were made.", ""]
            continue
        claims = [c for c in claims if isinstance(c, dict) and "id" in c] or claims
        ids = [c.get("id") for c in claims]
        dup = sorted({str(i) for i in ids if ids.count(i) > 1})
        if dup:
            flags.append(f"{w}: claim ids used more than once {dup}; every copy earns Unverified")
        final = {}
        for c in claims:  # refutations and finite claims first, so proofs can see their dependencies' status
            cid, kind, ch, rv = c["id"], c.get("type"), check.get(c["id"], "-"), review.get(c["id"], "-")
            if str(cid) in dup:
                final[cid] = "Unverified"
            elif refutes("check", ch) or refutes("review", rv):
                final[cid] = "Refuted or failed claim"
            elif kind == "finite-certificate" and ch == "PASS" and rv in ("-", "NO ERROR FOUND"):
                final[cid] = "Independently reproduced computation"
        for c in claims:
            cid, kind = c["id"], c.get("type")
            if cid in final:
                continue
            deps = c.get("depends_on", [])
            deps_ok = all(final.get(d) in ("Independently reproduced computation",
                                           "Reviewed proof; no error found") for d in deps)
            if kind == "proof" and review.get(cid) == "NO ERROR FOUND" and check.get(cid, "-") in ("-", "NOT FINITE") \
                    and deps_ok:
                final[cid] = "Reviewed proof; no error found"
            else:
                final[cid] = "Unverified"
        out += ["| Claim | Type | Check | Review | Author proposed | Earned status |", "|---|---|---|---|---|---|"]
        for c in claims:
            cid, prop = c["id"], c.get("proposed_status") or c.get("status") or "-"
            out.append(f"| {cid} | {c.get('type')} | {check.get(cid, '-')} | {review.get(cid, '-')} | {prop} | "
                       f"**{final[cid]}** |")
            if RANK.get(prop, 0) > RANK.get(final[cid], 0):
                flags.append(f"{w}/{cid}: author proposed '{prop}' but earned only '{final[cid]}'")
            if any(os.path.basename(f) == "NOTES.md" for f in c.get("files", [])):
                flags.append(f"{w}/{cid}: lists NOTES.md as evidence (reviewers would read the reasoning first)")
        for name, verdicts, allowed in (("check", check, CHECK_V), ("review", review, REVIEW_V)):
            odd = {k: v for k, v in verdicts.items() if v not in allowed}
            if odd:
                flags.append(f"{w}: {name}.json has unrecognised verdicts {odd}; they never lift a claim, and any "
                             "that reads as a failure refutes it")
        missing = [c["id"] for c in claims if c["id"] not in review]
        if missing:
            flags.append(f"{w}: claims with no review verdict: {missing}")
        out.append("")
        for c in claims:
            out.append(f"- **{c['id']}**: {c.get('statement', '')[:400]}")
        out.append("")

    out += ["## Flags", ""] + ([f"- {f}" for f in flags] or ["- none"]) + [""]
    out += ["A receipt shows the files are intact. Only the check and review verdicts above show what was",
            "verified, and only for the formal statement as written. Read the statement before trusting the status."]
    report = "\n".join(out) + "\n"
    open(os.path.join(camp, "AUDIT.md"), "w").write(report)
    print(report)
    return 1 if any(f.startswith(("integrity", "receipt", "campaign.json")) for f in flags) else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
