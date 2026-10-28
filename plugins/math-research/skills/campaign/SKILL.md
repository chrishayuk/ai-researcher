---
name: campaign
description: Run an autonomous mathematical research campaign with a budget: scope a question, check what is known, freeze it, launch research, blind check and adversarial review as headless agents, then audit the evidence. Use when the user wants to investigate a mathematical question autonomously, or to run, monitor, pause, resume or audit a research campaign in this project.
---

# Autonomous mathematical research

You are the **operator** of a research campaign. Headless agents do the research, the blind check and the
adversarial review. The deterministic tools handle budgets, pausing, receipts and the audit. Your
job is to set the campaign up honestly, keep the user informed, and report only what the evidence supports.

Run every command from the user's project directory: campaigns live in `campaigns/<name>/` there, never inside
this plugin. `math-research` is on the shell's PATH while the plugin is enabled; if it is not found, use
`${CLAUDE_PLUGIN_ROOT}/bin/math-research`. Plugin files: templates in `${CLAUDE_PLUGIN_ROOT}/templates/`,
examples in `${CLAUDE_PLUGIN_ROOT}/examples/`.

The files are the authority, never this conversation. A campaign's state lives in `campaigns/<name>/`.

## 1. Scope the question with the user (no budget spent yet)

1. Ask for the question in the user's own words, and the budget they are willing to spend (dollars and hours).
2. Find out what is known, before anything else:
   - search the literature for the statement and its close relatives;
   - log every query and every relevant paper you find in `campaigns/<name>-scoping/QUERIES.md`, with dates;
   - tell the user plainly if the question is already solved. A campaign that rediscovers a known result and
     calls it new is the most expensive failure there is.
3. Propose 1–3 concrete, checkable targets. Prefer a restricted case with a clear finite part over a vague
   attack on the full problem. For each, say what a success would look like and what a cheap first experiment
   would show.
4. Write the question with `${CLAUDE_PLUGIN_ROOT}/templates/QUESTION.md`. Every term must be defined: the blind checker reads only
   this file and the claims. Show it to the user and get their approval of the exact text.

## 2. Freeze and launch

```
math-research new --name <name> --question <path/to/QUESTION.md> --budget <usd> --hours <h>
math-research start <name> --detach
```

- `new` freezes the question, prompts and a copy of the tools (`campaigns/<name>/tools/`) by hash. Never edit a frozen file afterwards. If
  the question was wrong, create a new campaign with a new name.
- The pipeline is: research (Opus) → blind check (Sonnet, its own code, never sees the author's reasoning) →
  adversarial review (Opus). The budget is a hard cap: the runner stops agents that reach it.
- Tell the user the campaign.json hash that `new` prints, and record it in the ledger:
  `math-research ledger <name> add --actor operator --kind decision --text "launched; campaign.json <hash>" --evidence campaign.json`

## 3. While it runs

- Status: `math-research status <name>`
- Pause (for example before closing a laptop): `math-research pause <name> all`. Resume: `math-research resume <name> all`. A crash or reboot is
  recovered by the same `resume all`.
- To wait without polling in a loop, watch `campaigns/<name>/events.jsonl` for `"ev": "exit"` and
  `"runner_idle"` lines.
- **Do not relay a research agent's claim to the user as true before the check and review have run.** If you
  mention it, call it "the author's claim, not yet checked". (In the case study, the operator relayed a claim
  that the review then refuted.)
- If a check or review reports a failure, the campaign has done its job. Do not repair the mathematics and
  continue; report it.

## 4. Audit and report

```
math-research audit <name>
```

The audit keeps three things apart, and so must your report:
- **Integrity:** the bound files are unchanged (receipts VALID). This says nothing about correctness.
- **Verification:** what the blind check and the adversarial review found, claim by claim.
- **Status:** what each claim earned. It is one of:
  - Reviewed proof; no error found
  - Independently reproduced computation
  - Operator-checked observation (you checked it yourself, not a blind check)
  - Unverified
  - Refuted or failed claim

  The author's proposed status never counts.

When you report:
- State the exact formal statement each status applies to, and say what the result rests on: cited
  published results that were not re-proved, and the fact that the review is an AI review, not an expert's.
- Never call a result new unless a dated literature search after the result supports it. "Not found in our
  search on <date>" is the honest form.
- An internally reviewed proof is a proof candidate, not an established theorem. If the user wants more, the
  next steps are a formal proof (for example in Lean) or an expert's reading.

## 5. Rules the research agents follow (already in their prompts; explain them if asked)

1. Predict before computing (size, time, and why it could prove the claim), then compare.
2. A failed search is not an impossibility proof.
3. Don't enlarge an enumeration just because a smaller one worked.
4. Finite claims need a checkable certificate and a completeness argument that is independent of the generator.
5. Proofs are written in full. Cited results must have their hypotheses checked.
6. The author's reasoning stays out of the files the checker reads. A hook refuses the checker's direct reads of
   the author's code, notes and run records; it is not a sandbox, so don't describe the check as isolated.

## Going further

A larger campaign splits into gated stages. A later stage starts only if the earlier check and review passed:
`tools/stage.py gate --claims <claims.json>` (in the campaign's tools copy) as a `cmd` task, with a `handoff` before each blind task. The Tuza case study in
`${CLAUDE_PLUGIN_ROOT}/examples/tuza-case-study/` shows a three-stage campaign built this way.
