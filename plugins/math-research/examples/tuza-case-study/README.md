# Case study: Tuza's conjecture (Erdős Problem #167)

**Tuza's conjecture (1981).** If a graph has at most k edge-disjoint triangles, then removing at most 2k edges
makes it triangle-free. Equivalently, τ(G) ≤ 2ν(G). It is open in general.

This folder holds the key evidence from two campaigns that applied this project's method to restricted
cases. The campaigns themselves are not included (several hundred files, with full transcripts). Paths inside
these files refer to the original campaign layout.

## The outcome

| | |
|---|---|
| Target (TUZA-002, workstream B0) | Every finite 5-degenerate graph satisfies τ ≤ 2ν |
| Result | An **internally reviewed proof candidate**. Novelty unconfirmed; not formally verified |
| Configurations | 6,302 symmetry classes (6,094,848 labelled): 6,054 reduced by checked certificates, 248 excluded by a cited theorem, **0 uncovered** |
| Degrees ≥ 10 | One general written argument (Lemma W, a Hall-type matching argument). No enumeration needed |
| Reported agent cost | $23.20 for the whole of TUZA-002 (two rounds) |

The result rests on:
- the correctness of Puleo's published lemmas (arXiv:1308.2211), which were cited and their hypotheses
  checked, but not re-proved;
- AI review. No expert has read the argument.

> The system produced an internally reviewed proof candidate for a substantial special case of a conjecture
> that's been open for over 40 years. We independently reproduced the computational evidence and challenged
> the mathematical argument. Whether the result is new remains unconfirmed.

## How the proof is put together (round2/)

The structure is the standard minimal-counterexample argument:
- Take a smallest counterexample.
- Pick a vertex u whose neighbourhood is mostly made up of low-degree vertices.
- Show u can't exist, case by case on its degree:

| Degree of u | How it is closed | Evidence |
|---|---|---|
| 7, 8, 9 | Finite classification of every possible neighbourhood. Each class either has a reduction certificate, or is excluded because its link is disconnected | `SPEC.md` (the frozen specification, including the completeness argument), `check1-CHECK.md`, `check3-CHECK.md` |
| ≥ 10 | Lemma W: the neighbourhood is always "WKE", so u is reducible | `R2-lemma-W.md` |
| Assembly | The cases are exhaustive, and each is closed | `final-REVIEW.md`, `RESULT.md` |

The round ran in three gated stages (`PROTOCOL-AMENDMENT-B0R2.md`). Stage 2 could not start until the Stage 1
check and review had passed.

## What went wrong, and what was learned (round1-audit/)

An independent audit of Round 1 found 27 failures (1 high, 12 medium, 14 low severity). The earlier campaign,
TUZA-001, had 33. Its earlier failures include a literature miss and a result accepted on a stale check. The
most instructive findings:
- **Receipts that didn't mean what they seemed to.** Every Round 1 receipt bound only the outputs, so "all
  receipts VALID" meant "files intact", not "verified". Round 2 binds every input a task consumed.
- **A false claim relayed too early.** A research agent claimed that a reduction strictly extended a
  published lemma. The operator relayed the claim to the user, and the review then refuted it.
- **A workstream with no checker.** Exploratory results were never independently checked, and a false value
  went uncaught.
- **The operator overstated.** The operator described results more broadly than the checked statements.

`FAILURES.md` gives the full list, `COMPARISON.md` the comparison with TUZA-001, and `CLAIMS.md` the status of
every claim.

## A second partial result (lemma-A/)

Workstream A, on K4-free 9-degenerate graphs, did not reach its target. It did produce a candidate structural
lemma about adjacent degree-9 vertices in a smallest counterexample, backed by 6,346 independently checked
certificates and 16 precisely identified exceptions.
