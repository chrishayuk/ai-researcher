# TUZA-002 amendment B0R2: workstream B0, Round 2

Version 1, drafted 2026-10-25. Authorised by the user on 2026-10-25 ("B0 Round 2: approved with the conditions
above"). This amendment adds one bounded round. It changes nothing in PROTOCOL.md or in Round 1:
- Round 1 (`campaign/`) is frozen by `round1-snapshot/ROUND1.sha256`.
- Round 2 runs in its own campaign directory, `campaign-b0r2/`.
- Every start and resume checks that Round 1, TUZA-001 and this amendment are unchanged.

All rules of PROTOCOL.md still apply unless this document says otherwise: §4, the receipts and the binding of
completion markers in §8a–8b, pause/resume, and the E8 stop rule.

## 1. Target and authorisation

**B0:** every 5-degenerate graph satisfies τ ≤ 2ν.

**Authorised:**
- one bounded round of three stages, run strictly in order;
- independent verification and adversarial review after each stage.

**Not authorised:**
- any further work on A, B1 or C;
- a second B0 round. That needs a new user decision.

## 2. What Round 1 established (the starting point)

Statuses use the five labels in §7:

| Claim | Status after Round 1 |
|---|---|
| C1: the census of connected non-WKE graphs on ≤ 6 vertices | Independently reproduced computation, plus a hand proof that the review accepted |
| C2: Puleo's reductions transfer to a minimal counterexample in a subgraph-closed class | Proof; review found no error |
| C3: the second-layer set-up (u ∉ I, \|B\| ≤ 5, A ≠ ∅, S_a ⊆ B, \|S_a\| ≥ 3) | Proof; review found no error |
| C4: at d(u) = 7, every B0 configuration has {u} ∪ A reducible | **Unverified conjecture.** The MILP was exploratory and its certificates were not saved. |
| R2: a Hall-type lemma for d(u) ≥ 10 | Unverified conjecture (not yet written as a proof) |
| d(u) = 8, 9 | Not attempted |

## 3. What a complete B0 proof would need

Let G be a minimal counterexample in the class of 5-degenerate graphs. Let I be its set of 6⁻-vertices, and
choose u as in C3, so that B = N(u) ∖ I has |B| ≤ 5 and A = N(u) ∩ I. B0 follows only if all of these hold:

- **(P1) Structure lemma.** Every possible neighbourhood structure of u in G lies in an explicitly defined
  configuration space Φ_d, for each d = d(u) ∈ {7, 8, 9}.
  - Φ_d records G[B], the type and attachment of each a ∈ A, the outside vertices x_a, all possible
    identifications among them, and their possible adjacencies.
  - Every restriction used to make Φ_d smaller must be a cited Puleo result whose hypotheses hold by C2, or a
    proved lemma.
- **(P2) Locality lemma (L0).** A certificate that is valid on the local structure of a configuration
  establishes that the stated set V0 is reducible in G, whatever G looks like outside that structure.
- **(P3) Coverage.** The enumeration of Φ_d is complete. Completeness is shown by an argument that does not
  depend on the author's generator: for example, an independent enumeration by the checker, or an orbit count
  matched against an independently computed total.
- **(P4) Certificates.** Every configuration in Φ_d carries a certificate, of a format that has been stated and
  frozen, which the independent checker accepts.
- **(P5) R2.** For d(u) ≥ 10 there is a written proof that G[N(u)] is WKE, so {u} is reducible by Lemma 4.4.
- **(P6) Assembly.** The cases d(u) = 7, 8, 9 and d(u) ≥ 10 exhaust all cases, and each case is closed by
  P1–P5.

**What a finite enumeration establishes, and what it doesn't.** A run in which every enumerated configuration
passes establishes only P4, for the configurations that were enumerated. It is not evidence for P1, P2 or P3.
The B0 theorem may be claimed only if P1–P6 are each established with the status required in §7. Otherwise
the result is reported as exactly the parts that were established.

## 4. Stages (strictly sequential; workstream B2 in `campaign-b0r2/`)

### Stage 1: verify the degree-7 computation

No new enumeration is allowed until Stage 1 passes.
- **B2.t1** (Opus, research, ≤ 45 min):
  - Write `SPEC.md`. It contains:
    - the formal definition of Φ_d for d = 7, 8 **and** 9;
    - P1 and L0 (P2) for all three, with proofs;
    - the certificate format;
    - the coverage argument.
  - Regenerate the d = 7 computation with saved certificates and check that it matches C4. Do not enumerate
    d = 8 or 9.
- **B2.check1** (Sonnet, blind but informed, ≤ 40 min):
  - Read only SPEC.md, the claims and the certificates.
  - Enumerate Φ_7 independently from SPEC.md.
  - Check every certificate.
  - Confirm that every configuration in its own enumeration is covered.
  - Run mutation tests.
- **B2.review1** (Opus, adversarial, ≤ 40 min): review P1 and L0, Φ_7's definition, and the d = 7 conclusion.
- **Gate 1:** every check verdict is PASS (NOT FINITE is allowed only for proof claims, and at least one PASS is
  required), and every review verdict is NO ERROR FOUND. Otherwise B2 is blocked and the round stops.
- **Freezing the specification:** Stage 3 must use the SPEC.md that Stage 1 accepted. That covers:
  - the definitions of Φ_8 and Φ_9;
  - the allowed sets V0;
  - the certificate format;
  - the "Completeness" section, which gives the completeness argument for each of Φ_7, Φ_8 and Φ_9.

  Stage 1's receipt binds SPEC.md's hash. The runner re-verifies receipts every 30 seconds, so any later edit
  invalidates the receipt and blocks B2. Every later task also declares SPEC.md as an input, so its receipt
  records which SPEC it used. Changing any of these after Stage 1 counts as an uncontrolled expansion (stop
  rule S3). Stage 3 may not add a completeness argument of its own: a Stage 3 run in which every configuration
  passes, but which a frozen completeness check doesn't confirm, does not establish P3.
  review1 reviews the completeness argument for degrees 8 and 9 as well, before Stage 2 begins.

### Stage 2: the Hall-type lemma, before anything relies on it

- **B2.t2** (Opus, research, ≤ 30 min):
  - Write R2 as a complete proof, with every use of Puleo cited.
  - Small sanity computations are allowed: links on ≤ 12 vertices, ≤ 10 min each. A sanity computation is
    not part of the proof.
- **B2.review2** (Opus, adversarial, ≤ 40 min).
- **Gate 2:** every review verdict is NO ERROR FOUND. Otherwise B2 stops before Stage 3.

### Stage 3: structured enumeration for d(u) = 8, 9

- **B2.t3** (Opus, research, ≤ 45 min):
  - Before enumerating anything, record in state.json the predicted size of Φ_8 and Φ_9, with its derivation.
  - Then enumerate, exactly as SPEC.md defines, with saved certificates.
  - Finally, write the assembly argument (P6) as a claim. It states which of P1–P6 hold and which do not.
- **B2.check3** (Sonnet, blind but informed, ≤ 40 min): as check1, for Φ_8 and Φ_9.
- **B2.review3** (Opus, adversarial, ≤ 40 min):
  - review the Stage 3 claims;
  - review the assembly: whether the cases are exhaustive, and whether every case is closed by an
    established result;
  - review the final conclusion.

Gates and handoffs are `cmd` tasks that run `tools/stage.py`. A gate fails deterministically, so after
max_failures = 2 attempts the runner blocks B2 (dry run: `campaign-b0r2/predryrun/`).

**What a receipt means (from the Round 1 audit, item G11).** In Round 1 every receipt bound only campaign.json
and the task's outputs, so "VALID" meant the outputs were intact, not that anything was verified. In Round 2:
- every receipt binds the exact upstream files its task consumed: the amendment, SPEC.md, claims, certificate
  directories, and verdict files with their markers;
- an author's receipt binds the certificate directory as it stood when the task finished.

The runner re-verifies every receipt every 30 seconds, so a change to any bound file after acceptance blocks
B2. That is the F25 case (dry run: `campaign-b0r2/predryrun/bind-*`). Author code is not bound, because a
reviewer running it would write bytecode files and invalidate the receipt falsely.

A receipt still certifies integrity, not correctness. A review that reports ERROR FOUND is "ACCEPTED" as a
completed task. Verification status comes only from the check and review verdicts, which the gates enforce
after Stages 1 and 2. Stage 3's verdicts have no later gate; they are reported as they stand.

Before every agent task after the first, a handoff task moves the previous task's state.json, HANDOVER.md and
steps.jsonl into `ws/B2/archive/<task>/`. Blind tasks are forbidden to read that directory. This removes the
Round 1 rule conflict, where the runner told blind checkers to read the author's state.

## 5. Stop rules

The round stops, and reports exactly what was established, when any of these happens:
- **S1.** Gate 1 fails: the degree-7 check fails, or the review finds an error.
- **S2.** Gate 2 fails: R2 has an error, or it can't be written as a proof.
- **S3. Uncontrolled expansion.** Any of:
  - Φ_8 or Φ_9 must be enlarged or redefined after Stage 1;
  - V0 must include B-vertices or other vertices of unbounded degree;
  - the predicted size of Φ_8 ∪ Φ_9 exceeds 2 × 10⁶ configurations (after symmetry reduction);
  - a single computation is expected to exceed 30 minutes.
- **S4. No checkable certificate.** A configuration whose reduction can't be exported in the frozen certificate
  format counts as uncovered.
- **S5. Obstruction outside the frozen methods.** A configuration of Φ_8 or Φ_9 has no certificate for any V0
  that SPEC.md allows. It is reported as "no reduction found by the methods of SPEC.md", never as
  irreducible. No new method may be introduced in this round.

## 6. Caps

The caps are upper limits, not targets.

| | Cap | Enforcement |
|---|---|---|
| Research (B2.t1 + B2.t2 + B2.t3) | 2 h in total (45 + 30 + 45 min) | Stated in each task's prompt |
| Verification and review (5 tasks) | ≤ 40 min each, 3 h 20 min in total | Stated in each task's prompt |
| Workstream B2, all tasks | $40 and 5 h 30 min of active time | **Hard.** Enforced by the runner: the budget is checked per task through `--max-budget-usd`, and the wall-clock cap by pausing |

- $40 is within the $98.37 that remains of the TUZA-002 ceiling, and is not a spending target.
- Per-task time limits are set in the prompts. The runner has no per-task cap, and adding one would mean
  changing frozen infrastructure. Overruns per task are reported.

## 7. Verification status of claims (applies to Round 2 and to all reporting)

Every mathematical claim used to justify a decision or a report carries exactly one of these statuses:

1. **Verified result:** a written proof that an adversarial review accepted (NO ERROR FOUND), whose finite
   dependencies are independently reproduced.
2. **Independently reproduced computation:** a finite certificate that a blind checker accepted, with
   mutation tests.
3. **Operator-checked observation:** checked by the operator only, not by a blind protocol check.
4. **Unverified conjecture:** includes exploratory computations and negative local searches.
5. **Refuted claim:** with the refutation.

claims.json in Round 2 carries a "status" field holding the author's proposed status. The final status is set
by the check and the review, never by the author. An exploratory workstream is not exempt: a claim that is used
in a decision, a map or a report needs a status.

## 8. Reporting

When the round ends, whether it completes or a stop rule fires, the operator compiles `ws/B2/RESULT.md` from the
accepted check and review verdicts. The operator does not add verdicts of their own. RESULT.md states:
- P1–P6, each with its status;
- the configurations that survived, if any;
- which stop rule fired, if any;
- cost and time per task, including any overruns.

The operator then reports to the user and does not launch anything further.
