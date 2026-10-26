#!/usr/bin/env python3
"""Create a frozen research campaign from a question file and a budget.

  new_campaign.py --name NAME --question QUESTION.md [--budget USD] [--hours H]
                  [--research-model opus] [--check-model sonnet] [--review-model opus]
                  [--research-minutes 45] [--check-minutes 30] [--review-minutes 30]

Writes campaigns/NAME/ (relative to the project root):
  QUESTION.md        a copy of the question; the campaign is bound to this exact text
  prompts/           research, check and review prompts rendered from templates/
  campaign.json      one workstream "main": research -> handoff -> blind check -> handoff -> adversarial review
  frozen.sha256      hashes of the question, prompts and tools; checked at every start and resume
  campaign.sha256    hash of campaign.json, including which files each receipt binds
  ledger.jsonl       the attribution ledger (empty)

Every task's receipt binds the upstream files it consumed, so a later change to the question, a claim or a
certificate makes the receipt INVALID and blocks the workstream. The budget is a hard cap enforced by the
runner (the dollar cap through claude's --max-budget-usd, the time cap by pausing). Nothing is launched:
read the files, then start with  python3 -I tools/runner.py --campaign campaigns/NAME start --detach
"""
import argparse, hashlib, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
TOOLS = ["runner.py", "verify.py", "manifest_check.py", "pause_hook.py", "mark_complete.py", "ledger.py",
         "stage.py"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--question", required=True)
    ap.add_argument("--budget", type=float, default=5.0, help="hard dollar cap for the whole campaign")
    ap.add_argument("--hours", type=float, default=2.0, help="hard cap on active time")
    for role, model, minutes in (("research", "opus", 45), ("check", "sonnet", 30), ("review", "opus", 30)):
        ap.add_argument(f"--{role}-model", default=model)
        ap.add_argument(f"--{role}-minutes", type=int, default=minutes)
    a = ap.parse_args()

    out = os.path.join(ROOT, "campaigns", a.name)
    if os.path.exists(out):
        sys.exit(f"{out} already exists; a frozen campaign is never overwritten. Choose another --name.")
    os.makedirs(os.path.join(out, "prompts"))
    shutil.copy(a.question, os.path.join(out, "QUESTION.md"))
    open(os.path.join(out, "ledger.jsonl"), "w").close()

    W = "main"
    roles = {"research": a.research_minutes, "check": a.check_minutes, "review": a.review_minutes}
    for role, minutes in roles.items():
        text = open(os.path.join(ROOT, "templates", role + ".txt")).read()
        for k, v in {"@@NAME@@": a.name, "@@WS@@": W, "@@TASK@@": role, "@@MINUTES@@": str(minutes)}.items():
            text = text.replace(k, v)
        open(os.path.join(out, "prompts", role + ".txt"), "w").write(text)

    man = os.path.join(ROOT, "tools", "manifest_check.py")
    r, c, v = f"ws/{W}/research/", f"ws/{W}/check/", f"ws/{W}/review/"

    def agent(tid, model, outputs, binds):
        return {"id": tid, "kind": "agent", "prompt": f"prompts/{tid}.txt", "model": model,
                "outputs": outputs, "inputs": binds,
                "accept": {"inputs": ["campaign.json"] + binds, "checker": [man],
                           "cmd": [PY, "-I", man, *outputs]}}

    def handoff(after):
        dest = f"ws/{W}/archive/{after}"
        return {"id": f"handoff.{after}", "kind": "cmd", "outputs": [dest + "/MOVED.json"],
                "cmd": [PY, "-I", os.path.join(ROOT, "tools", "stage.py"), "handoff", W, dest]}

    tasks = [
        agent("research", a.research_model,
              [r + "RESULT.md", r + "claims.json", r + "NOTES.md", r + "research.complete"],
              ["QUESTION.md", r + "certs"]),
        handoff("research"),
        agent("check", a.check_model, [c + "CHECK.md", c + "check.json", c + "check.complete"],
              ["QUESTION.md", r + "claims.json", r + "certs", r + "research.complete"]),
        handoff("check"),
        agent("review", a.review_model, [v + "REVIEW.md", v + "review.json", v + "review.complete"],
              ["QUESTION.md", r + "claims.json", r + "certs", r + "RESULT.md", r + "NOTES.md",
               c + "check.json", c + "check.complete"]),
    ]
    spec = {"name": a.name,
            "workstreams": {W: {"model": a.research_model, "budget_usd": a.budget, "wall_s": int(a.hours * 3600),
                                "resume_policy": "session", "max_failures": 2, "tasks": tasks}},
            "integrity_checks": [{"name": "frozen question, prompts and tools",
                                  "cmd": ["shasum", "-a", "256", "-c", "-q", "frozen.sha256"]}]}
    json.dump(spec, open(os.path.join(out, "campaign.json"), "w"), indent=1)

    frozen = ["QUESTION.md"] + [f"prompts/{x}.txt" for x in roles]
    lines = [f"{sha(os.path.join(out, p))}  {p}" for p in frozen]
    lines += [f"{sha(os.path.join(ROOT, 'tools', t))}  ../../tools/{t}" for t in TOOLS]
    open(os.path.join(out, "frozen.sha256"), "w").write("\n".join(lines) + "\n")
    open(os.path.join(out, "campaign.sha256"), "w").write(f"{sha(os.path.join(out, 'campaign.json'))}  campaign.json\n")

    print(f"created {os.path.relpath(out, ROOT)}: research ({a.research_model}, {a.research_minutes} min) -> "
          f"blind check ({a.check_model}) -> adversarial review ({a.review_model}); hard caps ${a.budget:g}, "
          f"{a.hours:g} h")
    print(f"campaign.json sha256 {sha(os.path.join(out, 'campaign.json'))}")
    print(f"start:  python3 -I tools/runner.py --campaign {os.path.relpath(out, ROOT)} start --detach")


if __name__ == "__main__":
    main()
