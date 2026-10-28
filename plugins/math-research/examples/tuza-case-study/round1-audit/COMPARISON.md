# TUZA-001 versus TUZA-002 Round 1: failures by class (PROTOCOL.md §8c)

## Mapping TUZA-001 onto the §8c classes

TUZA-001's FAILURES.md groups failures differently: literature, operator errors, and agent rule breaks. Below is my
mapping of its F1–F33 onto the five §8c classes, using the same H/M/L ratings. The mapping is mine; TUZA-001 did not
use these classes.

| Class | TUZA-001 items |
|---|---|
| Literature | F1 (H); F2, F3, F4, F8, F13, F18 (M); F5, F6, F7, F16 (L) |
| Provenance | F19 (M); F21, F27, F32 (L) |
| Acceptance | F25 (H); F17, F30 (M); F10, F26 (L) |
| Attribution | F24 (M). OPERATOR-ERRATA 1–3 and 5 are attribution corrections with no severity assigned; they are not counted below. |
| Process | F11, F12, F22, F23, F28 (M); F9, F14, F15, F20, F29, F31, F33 (L) |
| Mathematical error | none recorded. TUZA-001's review found no error, and no false claim was logged. |

## Counts

| Class | TUZA-001 H / M / L (total) | TUZA-002 R1 H / M / L (total) |
|---|---|---|
| Literature | 1 / 6 / 4 (11) | 0 / 2 / 1 (3) |
| Provenance | 0 / 1 / 3 (4) | 0 / 4 / 3 (7) |
| Acceptance | 1 / 2 / 2 (5) | 1 / 2 / 0 (3) |
| Attribution | 0 / 1 / 0 (1) + 4 unrated errata | 0 / 1 / 2 (3) |
| Process | 0 / 5 / 7 (12) | 0 / 2 / 3 (5) |
| Mathematical error | 0 / 0 / 0 (0) | 0 / 1 / 5 (6) |
| **Total** | **2 / 15 / 16 (33)** | **1 / 12 / 14 (27)** |

## Scale

The two campaigns differ greatly in size:

| | TUZA-001 | TUZA-002 Round 1 |
|---|---|---|
| Scope | A whole campaign over about 16 hours (01:58–17:49 UTC) | One round of 33 minutes |
| Agent runs | About 15: selection study (4 candidates, a literature sub-agent, 2 assessors), Phase 0, WP1, WP1-check, WP2, WP3, the review, the audit | 8 |
| Literature searches | Several | None |
| Operator-written protocols and amendments | Several | None (all were frozen before launch) |
| Cost | Not tracked | $11.63 |

Per agent run, TUZA-001 had about 2.2 failures and Round 1 has about 3.4, or 2.6 if mathematical errors are left
out. Raw totals therefore cannot be compared, and Round 1 is no cleaner per unit of work. The useful comparison is by
class, in the next section.

## Reading by class

### Literature: fewer failures, but mostly because the situation did not arise

- **What the engine did.** The E2 pre-freeze search ran before Round 1, outside this audit's scope.
- **Why Round 1 has few literature failures.** No search ran during Round 1, so there was nothing to miss. A
  Kandasamy-type miss (F1) could not happen.
- **What did happen.**
  - Agent A skipped its required reading (G1).
  - Results were labelled before the repeat search that E2 requires (G2).
  - These are the same kind of discipline failure as F13 (frozen without a novelty check).
- **Verdict.** Not tested. Literature failures are absent only because no search happened, not because the engine
  prevented them.

### Provenance: more failures, and concentrated in the operator's reports

- **The engine fixes worked where they applied.**
  - E5: this audit was built from transcripts and file times.
  - E6: headless sessions wrote their own files, so F32 (the reviewer could not write its report) could not recur.
  - This class of failure was **prevented by the engine**.
- **Self-reports.** Agents still describe their own checks generously:
  - "independently checked" (G7);
  - "I reproduced the output" for a script that was never run (G8);
  - "seven ledger entries" when there were six (G9).
  - These are the same species as F27: agent notes that the transcript does not bear out.
- **Operator reports.** Three M items (G4–G6) are the operator relaying claims to the user before verification, or
  stronger than their evidence.
  - This repeats F19 ("overclaimed in chat").
  - The engine has no control over operator chat, so this class is **untouched by the engine changes**.
  - Mitigation: the operator withdrew G4 promptly and on its own initiative.

### Acceptance: the H item recurs in a new form

- **What the engine did.**
  - Output binding: markers plus receipts. All 48 bound hashes match.
  - TUZA-001 snapshot checks.
  - The frozen-hash refusal on resume.
  - The F25 pattern (a gate declared on stale files) did not occur.
- **G11: the gate cannot see inputs.** Receipts bind only outputs. No task declared inputs, so the certificates are
  bound nowhere. Acceptance also never reads a checker's verdict.
  - So F25's stale-input case would **not** have been caught in Round 1. Its absence is an accident of no input
    changing, not something the engine guaranteed.
  - This is the most important engine finding.
- **Partly prevented.** Of the E1 test cases, "an edited file" was guarded only for outputs, and nothing in the
  receipts covered the certificates.
- **The other acceptance items** are routing gaps: an uncertified finite fact typed "proof" (G12), and C with no
  check (G13).
- **Independence held.** TUZA-001's F17 (the checker and the author shared a counting method) did not recur. The
  blind Sonnet checks were genuinely blind and generator-free, and they confirmed both finite certificates.

### Attribution: much improved by the ledger, with one regression

- **What the engine did.** E3 worked as intended for the agents.
  - They logged ideas, claims and results in real time with evidence: 13 agent entries, each inside its task's time
    window.
  - Uncertain results were labelled at entry, for example "(unverified, solver output)" and "Exploratory MILP
    (uncertified)".
  - The TUZA-001 errata were of the form "found by the operator" when someone else found it. No such case occurred:
    every Round 1 idea has a recorded originator.
- **The regression.** The operator wrote an entry under an agent's name (G14). That is exactly the slip E3 was meant
  to stop. It was small and the content was accurate.
- **Also.** Check and review agents were not asked to log their results (G15).

### Process: fewer failures, but the conflicts moved somewhere new

- **What the engine did.**
  - E4 caught the freeze-time prompt errors that TUZA-001 had (F12, F14).
  - Sessions ran unattended, with caps passed correctly to the CLI.
  - Nothing broke. No relaunch, crash or retry was needed.
  - So the tooling-slip half of TUZA-001's process list (F15, F20, F31, F33) mostly **did not arise**.
- **Conflicts now arise at run time.**
  - The runner rules clash with the blind-check prompt (G18).
  - Claims list conclusion and src/ files, which collides with the reading rules (G17).
  - E4 cannot catch these, because they depend on what the author writes.
- **Pause and resume were never exercised.** The engine's main investment (G0) was neither stressed nor needed in
  Round 1.

### Mathematical error: a new class, and the engine caught the one that mattered

- **The outcome.** One M-severity false claim (G22, the strictness of A's class) was caught by the E7 adversarial
  review 13 minutes after it was made.
- **Who caught the rest.**
  - B.review caught three of B's slips (G24).
  - Errors that no agent caught: one in C's MAP.md (G25), because MAP.md was outside any review; and two mislabelled
    sanity controls (G26).
- **No comparison is possible here.** TUZA-001 produced fewer claims, and its review found nothing.

## Short honest reading

- **Engine aim.**
  - Round 1 shows real improvements in attribution: the ledger is kept by the agents in real time.
  - It shows real improvements in verification independence. The blind checks were truly blind and re-derived both
    finite certificates, and the adversarial review caught a false claim before it could be used.
  - It shows real improvements in operational robustness. There were no tooling failures and no report-writing
    workarounds.
- **The most serious TUZA-001 failure class, acceptance, was not engineered out.**
  - It was narrowed to outputs.
  - The receipts that were reported to the user as "all VALID" bind no certificate and no verdict (G11, H).
  - F25 did not recur only because nothing changed underneath a check.
- **Operator over-reporting (G4–G6) is unchanged from TUZA-001**, because nothing in the engine touches it.
- **Literature discipline was not tested.** No search ran, and the one rule that applied (E2's repeat search
  before labelling) was not followed.
- **Mathematics aim.**
  - The verified gains are A's R1 and R2 corollary (degree-9 vertices induce a matching in a minimal K4-free
    9-degenerate counterexample), and B's census and transfer of Puleo's lemmas.
  - These are partial results, not a new theorem.
  - C's K10 observation is operator-checked only.
- **Caveat on what was tested.** A single 33-minute round with no pauses, no failures and no literature search
  exercises only part of what the engine was built to handle. Several failure classes were absent because their
  situations never arose, not because the engine was shown to prevent them.
