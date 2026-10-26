# AI Math Researcher: a companion project

The companion project for *How to Build an Autonomous AI Math Researcher* (video 2; video 1 covered solving
maths problems with AI and Lean).

It gives your coding agent the skill and the tools to run a research campaign. The campaign has three steps:
- a research agent works on your question;
- a blind checker rebuilds its computations from scratch;
- an adversarial reviewer tries to break its proofs.

Everything runs under a hard budget, can be paused and resumed, and ends with an audit of what the evidence
actually supports.

> You don't need a research lab running thousands of AI agents. You can use the coding agents available today,
> combine them with mathematical tools, and build a research process you control yourself.

## What you need

- [Claude Code](https://claude.com/claude-code), installed and logged in. The runner drives `claude -p` in
  headless mode, so it can bill the API.
- Python 3.10 or later. `networkx` helps for graph problems (`pip install networkx`); everything else uses the
  standard library.
- macOS or Linux.

## Quick start: a small, known theorem (about 15 minutes, a few dollars)

Open Claude Code in this directory and ask:

> Use the math-research skill to run the example campaign in examples/ramsey-r33 with a $5 budget, then audit it.

Or run it yourself:

```bash
python3 -I tools/new_campaign.py --name r33 --question examples/ramsey-r33/QUESTION.md --budget 5 --hours 1
python3 -I tools/runner.py --campaign campaigns/r33 start --detach
python3 -I tools/runner.py --campaign campaigns/r33 status      # repeat until every task is done
python3 -I tools/audit.py campaigns/r33
```

Then open `campaigns/r33/`:
- `ws/main/research/`: the author's claims, certificates and code;
- `ws/main/check/`: the blind checker's own code and verdicts;
- `ws/main/review/`: the reviewer's attack on the proofs;
- `AUDIT.md`: what you may believe;
- `events.jsonl`, `receipts.jsonl` and `ledger.jsonl`: the record of what happened.

## Your own question

1. Copy `templates/QUESTION.md`, or ask the agent to help you write it with the skill. The skill searches the
   literature first and proposes checkable targets before any budget is spent.
2. `tools/new_campaign.py --name <name> --question <file> --budget <usd> --hours <h>` freezes it.
3. `tools/runner.py --campaign campaigns/<name> start --detach` runs it.
4. `tools/audit.py campaigns/<name>` tells you what to trust.

## Pause, resume, crash recovery

```bash
python3 -I tools/runner.py --campaign campaigns/<name> pause all    # e.g. before closing the laptop
python3 -I tools/runner.py --campaign campaigns/<name> resume all   # also after a crash or a reboot
```

The state lives in files, not in any conversation. A fresh terminal or a fresh agent can pick a campaign up.

## What is in the box

| Path | What it does |
|---|---|
| `.claude/skills/math-research/SKILL.md` | How your agent runs a campaign: scoping, literature, freezing, monitoring, honest reporting |
| `tools/new_campaign.py` | Question + budget → a frozen, hash-protected campaign |
| `tools/runner.py` | Launches the agents; enforces the budget; pause, resume and crash recovery |
| `tools/verify.py` | Acceptance receipts that bind the exact files a task consumed and produced |
| `tools/audit.py` | Integrity, verification and status, kept apart |
| `tools/stage.py` | Gates and handoffs for multi-stage campaigns |
| `tools/mark_complete.py`, `ledger.py`, `pause_hook.py`, `manifest_check.py` | Completion markers, the attribution ledger, pause enforcement, output checks |
| `templates/` | The question template and the research, check and review prompts |
| `examples/ramsey-r33/` | The small example |
| `examples/tuza-case-study/` | What happened when this method was applied to Tuza's conjecture (Erdős Problem #167) |
| `examples/tuza-case-study/verify/` | Re-run the real blind checker on the real degree-7 Tuza certificates (about 6 s) |

## Three distinctions to keep

- **A receipt is not a verification.** A receipt says the files are unchanged. Only the check and review
  verdicts say what was verified.
- **A passing computation is not a proof of coverage.** Coverage needs its own argument, checked independently.
- **An internally reviewed proof is a proof candidate.** It is not an established theorem, and not
  necessarily a new one. For more, formalise it (video 1: Lean) or ask an expert.

## Using Codex or another agent

The skill is plain Markdown, and `AGENTS.md` points to it, so any coding agent can follow the workflow. The
runner launches research agents with Claude Code's headless mode (`claude -p`). Driving a different agent CLI
means changing the agent launch in `tools/runner.py`.

## Licence

Apache License 2.0. See `LICENSE`.
