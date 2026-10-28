# TUZA-002 amendment B0R2: Round 2 result

The operator compiled this file on 2026-10-25, after the round ended (runner idle at 23:49:14Z). The amendment
(§8) requires that it be compiled from the accepted check and review verdicts only. The operator adds no
verdicts of their own.

**Status wording** (user, 2026-10-25): a proof accepted only by this campaign's internal adversarial review is
reported as "**Reviewed proof; no error found**". The frozen §7 label appears in brackets for traceability.

## Outcome

Every stage passed, and no stop rule fired. The round's target statement is

> **B0. Every finite 5-degenerate graph G satisfies τ(G) ≤ 2ν(G).**

It is now an **internally reviewed proof candidate**. It is not a formally verified theorem, and its novelty is
not confirmed. It rests on three things:
- the correctness of Puleo's published lemmas, which are cited, with their hypotheses checked, but not
  re-proved: Lemmas 2.2, 4.3, 4.4, Cor. 4.9, Props 5.1 and 5.2, Cor. 5.3, Lemmas 2.7 and 7.4–7.7;
- Round 1's C2 and C3, whose status is "Proof; review found no error";
- this campaign's internal reviews (Opus) and blind checks (Sonnet). Nobody outside the campaign has examined
  the argument.

## P1–P6

Final statuses are as assigned by review3 (`s3/review/REVIEW.md`).

| | Content | Final status | Established by |
|---|---|---|---|
| P1 | Structure lemma: every u has its neighbourhood structure in Φ_d, d ∈ {7, 8, 9} | Reviewed proof; no error found [Verified result] | review1 (Gate 1), re-checked by review3 |
| P2 | Locality lemma L0 and Cor. 5.4 | Reviewed proof; no error found [Verified result] | review1. Stress-tested on 6,120 + 47,208 random host graphs, 0 failures; the controls failed as they should. |
| P3 | Coverage (frozen SPEC §7 checks K1–K3) | Independently reproduced computation | check1 (d = 7) and check3 (d = 8, 9), each with its own enumeration. review3's own code and a brute-force count of \|L_d\| agree. |
| P4 | Certificates | Independently reproduced computation | check1 and check3 PASS, with mutation tests. review3 re-validated every certificate. |
| P5 | R2 (Lemma W): d(u) ≥ 10 is impossible | Reviewed proof; no error found [Verified result] | review2 (Gate 2). Sanity runs: 527,136 exhaustive instances, plus the proof's construction executed on 8.2 million instances. |
| P6 | Assembly: the cases d(u) = 7, 8, 9 and ≥ 10 are exhaustive and each is closed | Reviewed proof; no error found [Verified result] | review3 |

F8, "d(v) ≤ 9 implies G[N(v)] is connected", is used for every exclusion below:
- **its applicability** (robustness through C2) was reviewed;
- **the statement itself** is an operator-checked observation (the user): it follows from Puleo's Def. 2.3,
  since two link components of ≥ 5 vertices each would need ≥ 10 neighbours.

## The finite classification

Each symmetry class of configurations falls into exactly one of three kinds: reduced by a certificate,
excluded by a theorem (F8), or uncovered.

| d | Classes | Labelled configurations | Reduced, V0 = {u} ∪ A | Reduced, V0 = {u} ∪ A′, \|A′\| = \|A\| − 1 | Excluded by F8 (disconnected link) | Uncovered |
|---|---|---|---|---|---|---|
| 7 | 174 | 10,305 | 153 | 0 | 21 | 0 |
| 8 | 738 | 159,286 | 689 | 0 | 49 | 0 |
| 9 | 5,390 | 5,925,257 | 5,203 | 9 | 178 | 0 |
| **Total** | **6,302** | **6,094,848** | **6,045** | **9** | **248** | **0** |

- **Exclusions are not reductions.** The 248 exclusions carry F8 as an explicit dependency. They are not
  certificates of reducibility.
- **The 9 smaller-V0 cases.** For these, the solve with V0 = {u} ∪ A reached its 120-second limit. Certificates
  were then found with a smaller V0, which SPEC §5.1 allows. They are validated directly, like every other
  certificate.

## Deviations, gaps and overruns

- **D1, a reviewed specification deviation.** Amendment P1 asked Φ_d to record the adjacencies of the outside
  vertices. SPEC.md leaves them out, and L0 justifies the omission. review1 accepted it. It is recorded in the
  ledger.
- **The prediction missed, but no stop rule fired.** Before enumerating, the author predicted a certificate
  search of under 15 minutes. The search took 26.5 minutes of wall time (1,588 s), about 4.5 hours of CPU time
  on 10 processes. That is still under S3's 30-minute limit.
  - S3 does not say whether its limit means wall time or CPU time. The operator records that ambiguity here.
- **A killed first attempt.** The author's first degree-9 run used a brute-force canonicalisation that was far
  slower than predicted, and the author killed it. The rewritten enumeration uses the same method and SPEC,
  and reproduces phi8.json exactly.
  - It is disclosed in `s3/NOTES.md`.
  - It is not mentioned in ASSEMBLY.md's stop-rule summary.
- **A gap in the mutation evidence, closed by review3.**
  - check3 reported 14 of 14 mutants rejected at degree 9, but saved no output file for that run.
  - The author ran no degree-9 mutation tests.
  - review3 ran its own 10 mutants on phi9.json, all rejected, and saved the log (`s3/review/run_mut3.log`).
- **Authors' proposed statuses.** Each author task proposed "Verified result" for its own proofs before
  review. Under §7 such proposals carry no weight. Every final status above comes from a check or a review.
- **Per-task time limits** were set by prompt only. No research task exceeded its limit.

## Cost and time

Total cost: $11.57 of the $40 hard cap. Active time: 5,726 s of the 19,800 s hard cap.

| Task | Model | Cost | Wall time | Limit |
|---|---|---|---|---|
| B2.t1 (SPEC and degree 7) | Opus | $2.43 | 10.4 min | 45 |
| B2.check1 | Sonnet | $0.35 | 1.8 min | 40 |
| B2.review1 | Opus | $1.44 | 6.6 min | 40 |
| B2.t2 (R2) | Opus | $1.15 | 12.0 min | 30 |
| B2.review2 | Opus | $1.70 | 13.1 min | 40 |
| B2.t3 (degrees 8 and 9, assembly) | Opus | $2.08 | 34.9 min | 45 |
| B2.check3 | Sonnet | $0.48 | 8.8 min | 40 |
| B2.review3 | Opus | $1.95 | 8.3 min | 40 |

- Research took 57 minutes in total, against a 2-hour limit. Checks and reviews took 39 minutes.
- TUZA-002 as a whole: Round 1 cost $11.63 and Round 2 $11.57, so $23.20 of the $110 ceiling.
- These are reported agent costs only. They do not include development, operator or human effort.

## Integrity at close (operator, 2026-10-25)

- `campaign.json` matches the launch hash in the ledger (51fbcac8…).
- `frozen.sha256` verifies.
- All 18 receipts are VALID. Each one binds its task's upstream inputs.
- All three gates pass.
- The four integrity checks pass: frozen files, TUZA-001, Round 1, and the Round 1 ledger prefix.
- The evidence is snapshotted in `../../round2-snapshot/ROUND2.sha256`.

## Not done, and not authorised in this round

- **Novelty.** B0 was not found in the pre-freeze search. Planar graphs (Tuza 1990) are a known 5-degenerate
  special case. No dated repeat search (E2) has been run, so no novelty label is attached.
- **External or formal verification.** None has been done.
- **A, B1 and C.** No further work on them has been authorised.
