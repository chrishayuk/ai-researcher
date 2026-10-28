# TUZA-002 Round 1: every mathematical claim and its status

Each claim has exactly one status:
- **Verified result**: proved, and the proof reviewed.
- **Independently reproduced computation**: a finite computation that someone other than its author re-did from
  the statement.
- **Operator-checked observation**: checked only by the operator, outside the protocol.
- **Unverified conjecture**: anything else asserted, including author-only computations.
- **Refuted claim**: shown false.

Evidence notation is as in FAILURES.md. "Audit" means this audit's own scripts in `audit-r1/tools/`.

## Workstream A (claims.json, RESULT.md)

| Claim | Status | Evidence |
|---|---|---|
| **Set-up**: exactly four connected triangle-free 9-vertex graphs are not WKE (L1–L4). In a minimal K4-free 9-degenerate counterexample, δ = 9 and every degree-9 vertex has one of them as its link. | Independently reproduced computation | TUZA-001 census. A.review's generator-independent `review/links_census.py` gives 1380 connected graphs, exactly 4 non-WKE, isomorphic to L1–L4, with OEIS-matching counts (agent-4c51d2f0 L76). The deduction to the link structure was reviewed (REVIEW.md:15-25). |
| **A-R1**: no single-vertex local certificate (E0, S, X inside G[N[v]], valid in every host) exists for any Li; the minimum of \|X\| − 2\|S\| is exactly 1. | Verified result | Lemma 0 and Lemma R1 were reviewed (REVIEW.md:27-44). The finite part is the author's `src/check_r1.py`, which has no certificate and no Sonnet check (G12). It was re-derived independently twice: the review's CP-SAT model straight from Def. 4.2 on G⁺ (OPTIMAL 1 for L1–L4, agent-4c51d2f0 L84), and the audit's direct enumeration (min 1 for all four, `audit_math.out`). |
| **A-R2**: 6,346 of the 6,362 labelled adjacent degree-9 gluings carry a valid certificate. The 16 others are exactly the L2–L2 gluings at vertex 7 whose β does not map {2,3} onto a twin pair. | Independently reproduced computation | Blind Sonnet check: own builder and enumerator, 10 mutants plus 200 random deletions rejected, PASS (A/check/CHECK.md:5-11). Review: own networkx checker plus host-embedding test on 1270 gluings (REVIEW.md:46-58). Audit: 6,362 gluings, 16 = 24 − 8 exceptional bijections, \|Aut(L2)\| = 32 and every automorphism fixes 7, and the file's 16 nulls are exactly L2/L2/7/7. |
| **A-R2-COR**: in a minimal counterexample, adjacent degree-9 vertices both have link L2 and φ(w) = 7 for every φ. Degree-9 vertices induce a matching. Degree-9 vertices with link L1, L3 or L4 have every neighbour of degree ≥ 10. | Verified result | Reviewed (REVIEW.md:60-68). The proof uses A-R2, Lemma 0, Lemma 4.3 and closure under subgraphs. The step "for every φ" needs Aut(L2) to fix 7, which the audit confirmed. The 16 exceptions are accounted for (ANSWERS Q2). |
| **A-R2-NEG**: for the 16 exceptional gluings, CP-SAT finds optimum \|X\| − 2\|S\| = 1 within the R2 class. | Unverified conjecture | Author-only solver run with no infeasibility certificate (`certs/r2_log.txt`). It is labelled correctly as "NO REDUCTION FOUND … not a proof". |
| **A-PS-C5**: E0 = {va0, va1, va3} is reducible at a C5 link component (true), "in particular R1 strictly extends Puleo's Lemma 4.4, as C5 is not WKE" (false). | Refuted claim | C5 is WKE (REVIEW.md:70-80; audit `audit_math.out`: C5 WKE True). The reducibility computation itself is correct. |
| RESULT.md: "R1 is strictly larger than Lemma 4.4 (… a C5 component or a leaf)", and "this partial-star notion may shrink the 10-vertex obstruction lists". | Refuted claim | The same refutation. The review shows that every Li plus a pendant edge is WKE, so the leaf example has no witness either (REVIEW.md:77-80). |
| RESULT.md headline 4: "9-degeneracy does not force a degree-9 vertex to have a degree-9 neighbour". | Unverified conjecture | Asserted without proof (REVIEW.md:90-91). |
| RESULT.md: "Any proof of A1 must use information about vertices of degree ≥ 10 or a non-local argument". | Unverified conjecture | Informal. It holds only relative to the classes R1 and R2 (REVIEW.md:92-93). |
| RESULT.md next step 1: a degree-10 vertex of a minimal counterexample has a connected, non-WKE link. | Unverified conjecture | Short argument, not reviewed as a claim. The audit sees no gap: an isolated link vertex gives an edge in no triangle, which reduces. Still unreviewed. |
| Ledger 20 and RESULT.md: CP-SAT gives an R1 optimum of 1 for each Li, and 1144 of the 1160 R2 orbit-representative gluings are reducible. | Unverified conjecture | Author-only solver output. It is superseded by A-R1 and A-R2, which were checked. |

## Workstream B (claims.json, FEASIBILITY.md)

| Claim | Status | Evidence |
|---|---|---|
| **C1**: a connected graph on n ≤ 6 vertices is non-WKE iff n ∈ {5,6} and Δ(H̄) ≤ 1. These are K5, K5−e, K5−2e, K6, K6−e, K6−2e and K2,2,2. | Verified result | The hand proof was reviewed (REVIEW.md:38-43). The computation was independently reproduced: by the blind Sonnet check (agent-2491f666 L40-41, PASS, 6 mutants rejected) and by the review's generator-free labelled census (REVIEW.md:27-34). |
| **C2**: in a minimal counterexample within any subgraph-closed class, Puleo's Lemma 2.7, Prop. 5.1, Prop. 5.2 and Cor. 5.3 hold. Links at 6⁻-vertices are K5, K5−e, K6, K6−e or K2,2,2. | Verified result | Reviewed. Prop. 5.1 and its converse, Prop. 5.2, and Lemmas 7.5–7.7 were mechanically re-verified by the review (REVIEW.md:45-86). The unstated isolated-vertex case is harmless. |
| **C3**: the second-layer set-up. There is a vertex u with \|N(u) ∖ I\| ≤ dg, together with the stated \|A\| bounds and subsumption facts. | Verified result | Reviewed (REVIEW.md:88-109). Its text says "δ(G) = 5", which is wrong for dg = 6 and unused (G24). |
| **C4**: for dg = 5 and d(u) = 7, every connected non-WKE configuration has {u} ∪ A reducible. For dg = 6 there is one survivor, a K7 block. | Unverified conjecture | Exploratory MILP whose certificates were not saved. B labels it "(Exploratory, uncertified.)". Neither the check nor the review examined it. |
| FEASIBILITY §2: the five surviving links are irreducible singletons, with no condition on the rest of G. | Independently reproduced computation | B's own argument for this is a non-sequitur (G24). The fact was established by the reviewer's `t_singleton.py` (exact CP-SAT, all 21 + 112 connected links, REVIEW.md:70-72). That is a single computation, and it is not B's. |
| FEASIBILITY §4: R1 + R2 + the d = 7 rung would together give B0. | Verified result | The implication was reviewed (REVIEW.md:131-135). R1 and R2 themselves are unproved. |
| Proposed lemmas R1 (d(u) ∈ {7,8,9}), R2 (a Hall-type extension of Lemma 7.3) and R3 (the K7 block). | Unverified conjecture | Proposals only. |
| The B1 survivor (u ∪ B = K7) cannot be reduced with V0 = {u} ∪ A. | Unverified conjecture | Part of C4: an uncertified negative local search. |
| `src/fastwke.py`: there are 117 connected non-WKE graphs on 7 vertices. | Independently reproduced computation | It agrees with the operator's pre-freeze count. Both computations are uncertified and exploratory. |
| B0 GO-WITH-CONDITIONS, B1 NO-GO (verdicts). | (not a mathematical claim) | These rest partly on C4. See ANSWERS, extra check 2. |

## Workstream C (claims.json, MAP.md)

| Claim | Status | Evidence |
|---|---|---|
| **C1**: ρ_ν(K10) ≥ 5, that is, no X with 1 ≤ \|X\| ≤ 4 has ν(K10 − X) ≤ 13 − \|X\|/2. So H4 is false. | Operator-checked observation | C's own certificate and checker (no protocol check, no review: G13). The operator's separate CP-SAT check over all 19 edge-set shapes gives a maximum drop of 1 (`operator-check/c1_k10.out`). |
| ν(K10) = 13; a maximum packing's leave is K1,3 + 3K2; τ(K10) = 20 (MAP §4). | Operator-checked observation | The operator check confirms ν(K10) = 13. The leave structure and τ are unreviewed, though the audit's arithmetic agrees (45 − 39 = 6 leave edges, all degrees odd; τ = 45 − 25). |
| **C2** (conjecture): every K5-free graph with a triangle has ρ_ν ≤ 2. | Unverified conjecture | Correctly typed as a conjecture. Its falsifier K5,5,5,5 was not run. |
| E1: τ₂ ≤ 2ν₂ for all 2^20 families of triples on 6 points. No violation in a seeded 7-point search. | Unverified conjecture | Author-only exhaustive computation, labelled "Exploratory, no E7 certificate" (ledger 25). |
| E2: on ≤ 6 vertices, ρ_ν ∈ {1,2,4}, with 4 only for K5 and K5 plus a pendant edge; ρ_ex ≤ 3; ρ_star = ∞ for 10 classes. | Unverified conjecture | Author-only computation. |
| E2b: sample histogram; ρ_ν(K8) = 2; every K5-free sample graph has ρ_ν = 1. | Unverified conjecture | Author-only computation. The W5 row was mis-specified, which C itself noted (G27). |
| MAP §1: in a minimal counterexample ρ_ex = ∞, and the listed consequences follow. | Unverified conjecture | Unreviewed derivation, since C.review did not read MAP.md. The audit hand-checked the first two consequences and found no error. |
| MAP §0.4(a) and A4: all 9 graphs on ≤ 6 vertices with τ = 2ν have ρ_ν = τ. | Unverified conjecture | Author-only computation. |
| MAP §0.4(b): ρ_ν is probably unbounded. | Unverified conjecture | Labelled "idea, not proved". |
| MAP A3: τ(K8) = 12, τ(K7) = 9, ν(K8) = 8, ν(K7) = 7, so vertex deletion fails at K8. | Unverified conjecture | Hand check. The audit's arithmetic agrees: τ(K_n) = C(n,2) − ⌊n²/4⌋; STS(7); ⌊8/3·3⌋ = 8. |
| MAP A6: "K4 has ν\*/ν = 4/3". | Refuted claim | ν\*(K4) = 2, so ν\*/ν = 2 (`audit-r1/tools/nustar_k4.out`; G25). |
| MAP A7: K4 cover pairs {12,13} and {12,23} each miss a triangle. | Unverified conjecture | Hand check. The audit agrees. |

## Operator statements to the user (main L2805–L3076)

| Statement | Status | Evidence |
|---|---|---|
| "This class of reductions is strictly larger than Puleo's Lemma 4.4" (main L2860). | Refuted claim | The same claim as A-PS-C5. Withdrawn at main L3010. |
| "None of the four links can be eliminated by any reduction confined to the vertex's own neighbourhood" (main L2860, L3010, L3076). | Verified result | Equals A-R1. |
| "In a smallest counterexample, the degree-9 vertices form a matching" (main L2860, L3010, L3076). | Verified result | Equals A-R2-COR. |
| R2: 6,346 of 6,362 gluings certified, with 16 L2–L2 exceptions (main L2860, L2958, L3076). | Independently reproduced computation | Equals A-R2. |
| B's census: seven graphs (main L2911, L3076). | Verified result | Equals B's C1. |
| "Puleo's lemmas … eliminate K5−2e and K6−2e without assuming anything about neighbour degrees" (main L2911). | Verified result | Equals B's C2, reviewed later. |
| "In B's exploratory test, the first case (u of degree 7) closes in every configuration" (main L2911). | Unverified conjecture | Equals C4. The operator labelled it uncertified. |
| "B1 … one configuration (a K6 block) that no local reduction handles. It's structural, not a matter of search effort" (main L2911); "a K6 block, survives every local reduction tried" (main L3076). | Unverified conjecture | Overstated (G6). The block is K7, and the evidence is an uncertified negative search. |
| "K10 defeats any reduction that removes at most 4 edges at a time" (main L3010). | Unverified conjecture | The checked statement is narrower: ν-reducible sets only (G5). The audit's arithmetic suggests that exactly-reducible sets of size ≤ 4 also fail, since τ(K10 − X) = 20 − \|X\|, but no one checked that. |
| "K10 refutes H4 … ν(K10) = 13, and the best drop over all 19 edge-set shapes is 1" (main L3076). | Operator-checked observation | `operator-check/c1_k10.out`. |
| Conjecture C2 "would be a big result on thin evidence" (main L3010, L3076). | Unverified conjecture | A correct characterisation. |
| Pre-freeze operator census: non-WKE connected graphs number 0, 3, 4 and 117 for n ≤ 4, 5, 6 and 7 (PROTOCOL.md:52-56; ledger 9). | Independently reproduced computation | n ≤ 6 by B's C1, including its blind check and its review. n = 7 by B's `fastwke.py`, uncertified. |
