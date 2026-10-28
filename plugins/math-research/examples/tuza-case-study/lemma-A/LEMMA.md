# Candidate structural lemma: degree-9 vertices in a smallest K4-free 9-degenerate counterexample

TUZA-002 Round 1, workstream A. This file packages a result for preservation. It adds no new mathematics.
The wording follows the user's correction of 2026-10-25: the lemma states the exceptional L2–L2 structure
explicitly, rather than only "the degree-9 vertices form a matching". The source files are unchanged.
`EVIDENCE.sha256` binds the versions this package describes.

## Setting

𝒞 is the class of K4-free 9-degenerate graphs. It is closed under taking subgraphs.

Let G be a counterexample to Tuza's conjecture (τ ≤ 2ν) with |V(G)| + |E(G)| minimal in 𝒞. TUZA-001 gives
δ(G) = 9, using Fact F and Puleo's Lemma 4.4. Every degree-9 vertex v has a connected link G[N(v)] isomorphic
to one of the four connected triangle-free non-WKE graphs on 9 vertices:

    L1 = H?r@f_{   L2 = H?rF`zo   L3 = H?opvbE   L4 = H?opuJo   (graph6)

In L2 the neighbourhood N(7) is {2, 3, 4, 5}. Here 2 and 3 are false twins, with N(2) = N(3) = {6, 7, 8}, and
so are 4 and 5, with N(4) = N(5) = {0, 1, 7}. Vertex 7 is fixed by every automorphism of L2.

## Statement

Let v and w be adjacent degree-9 vertices of G. Then:
1. both links are isomorphic to L2;
2. w plays the role of vertex 7 in v's link, and v plays the role of vertex 7 in w's link, under every
   isomorphism to L2;
3. the gluing of the two links along the edge vw is one of the 16 exceptional configurations. These are the
   bijections β : N_{L2}(7) → N_{L2}(7) that send the twin pair {2, 3} to a mixed pair, meaning one vertex of
   {2, 3} and one of {4, 5}.

Consequences:
- every degree-9 vertex has at most one degree-9 neighbour, so the degree-9 vertices induce a matching;
- a degree-9 vertex whose link is L1, L3 or L4 has all of its neighbours of degree ≥ 10.

## What supports each part, and its status

The status labels follow PROTOCOL-AMENDMENT-B0R2.md §7, as the Round 1 audit assigned them (audit-r1/CLAIMS.md).

| Part | Source claim | Status | Basis |
|---|---|---|---|
| Finite classification: 6,346 of the 6,362 labelled adjacent degree-9 gluings carry a reduction certificate (A, S, X); the other 16 are exactly the configurations in point 3 | A-R2 | **Independently reproduced computation** | Blind Sonnet check with its own enumerator: PASS, with 10 mutants and 200 random deletions rejected. Adversarial review, with its own checker: no error found. The audit confirmed the 16 = 24 − 8 accounting. |
| Points 1–3 and the consequences (a certified gluing gives a reducible edge set, which contradicts minimality) | A-R2-COR | **Verified result**, in the sense of §7: a reviewed proof whose one finite dependency (A-R2) is independently reproduced | The adversarial review found no error. The inference itself (Lemma 0, Lemma 4.3, closure of 𝒞 under subgraphs, and Aut(L2) fixing vertex 7) was **reviewed, not machine-checked**. The blind check verdict on it was NOT FINITE. |
| The 16 exceptional configurations admit no certificate of the A-R2 type | A-R2-NEG | **Unverified conjecture** (a negative local search) | The author's CP-SAT run only (optimum \|X\| − 2\|S\| = 1), with no infeasibility certificate. **Not** a claim that the configurations are irreducible. |

Related claims:
- A-R1, no single-vertex local certificate for any Li: Verified result.
- A-PS-C5's "strictly extends Puleo's Lemma 4.4": Refuted claim, since C5 is WKE. It plays no part in this lemma.

## What it does and does not give

It narrows A1 (every K4-free 9-degenerate graph is Tuza) to two cases:
- a degree-9 vertex all of whose neighbours have degree ≥ 10;
- an adjacent L2–L2 pair glued in one of the 16 exceptional ways.

It does not prove A1. Novelty is unconfirmed: no repeat literature search was run for this statement (audit
item on E2). Extending A is not authorised in the current round.

## Files (paths relative to experiments/tuza-002/campaign/)

- `ws/A/RESULT.md`: the proofs (Lemma 0, R1, R2, the corollary).
- `ws/A/claims.json`.
- `ws/A/certs/r2_certs.json` and `r2_mutation.txt`.
- `ws/A/check/CHECK.md`, `check.json`.
- `ws/A/review/REVIEW.md`, `review.json`.
- `../audit-r1/CLAIMS.md`.
