# math-research

A Claude Code plugin for running autonomous mathematical research campaigns. A campaign has three steps:
- a research agent works on your question;
- a blind checker rebuilds its computations from scratch;
- an adversarial reviewer tries to break its proofs.

Everything runs under a hard budget, can be paused and resumed, and ends with an audit of what the evidence
actually supports. This is the engine from *How to Build an Autonomous AI Math Researcher*, packaged as a plugin.

## What you need

- [Claude Code](https://claude.com/claude-code), installed and logged in. The runner drives `claude -p` in
  headless mode, so it can bill the API.
- Python 3.10 or later. `networkx` helps for graph problems; everything else uses the standard library.
- macOS or Linux.

## Install

```bash
claude plugin marketplace add chrishayuk/ai-researcher     # or a local path to this repository
claude plugin install math-research@ai-researcher
```

Inside Claude Code, the `math-research` command is already on the PATH. To use it in your own terminal too,
add this line to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export PATH="$PATH:$HOME/.claude/plugins/marketplaces/ai-researcher/plugins/math-research/bin"
```

If you added the marketplace from a local folder instead, use that folder's `plugins/math-research/bin`.

## Quick start: a small, known theorem (about 15 minutes, a few dollars)

Open Claude Code in any project directory and ask:

> Use the math-research campaign skill to run the ramsey-r33 example with a $5 budget, then audit it.

Or run `/math-research:campaign`. Or drive it yourself (`math-research` is on the PATH while the plugin is enabled):

```bash
math-research new --name r33 --question "$(math-research path)/examples/ramsey-r33/QUESTION.md" --budget 5 --hours 1
math-research start r33 --detach
math-research status r33          # repeat until every task is done
math-research audit r33
```

Campaigns are written to `campaigns/<name>/` in your project, never inside the plugin. Open it afterwards:
- `ws/main/research/`: the author's claims, certificates and code;
- `ws/main/check/`: the blind checker's own code and verdicts;
- `ws/main/review/`: the reviewer's attack on the proofs;
- `AUDIT.md`: what you may believe;
- `events.jsonl`, `receipts.jsonl` and `ledger.jsonl`: the record of what happened.

## Pause, resume, crash recovery

```bash
math-research pause <name> all     # e.g. before closing the laptop
math-research resume <name> all    # also after a crash or a reboot
```

The state lives in files, not in any conversation. A fresh terminal or a fresh agent can pick a campaign up.

## Each campaign carries its own engine

`math-research new` copies the tools into `campaigns/<name>/tools/` and freezes them by hash with the question
and prompts. Every later command runs that copy. A plugin update therefore never changes a campaign that is
already frozen or running, and a changed tool file blocks the campaign at its next start or resume.

## What is in the box

| Path | What it does |
|---|---|
| `skills/campaign/SKILL.md` | How your agent runs a campaign: scoping, literature, freezing, monitoring, honest reporting |
| `bin/math-research` | One command: `new`, `start`, `status`, `pause`, `resume`, `audit`, `ledger`, `list` |
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
  necessarily a new one. For more, formalise it (for example in Lean) or ask an expert.

## Known limits

- **No isolation.** Agents run with the access of the environment that launched them. A separate working
  directory and prompt rules do not stop an agent reading other files on the machine, so a run is not a clean
  held-out benchmark.
- **One time budget per workstream.** `--hours` caps the workstream's total active time across research,
  check and review. The per-role minutes are guidance in the prompts, not enforced limits.

## Licence

Apache License 2.0. See `LICENSE`.
