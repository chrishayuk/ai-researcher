# B2.review3: adversarial review of Stage 3 (B2-D8, B2-D9) and of the whole B0 argument (B2-ASSEMBLY)

Reviewer: B2.review3 (Opus), 2026-10-25.

## What I read, in this order

1. `../PROTOCOL-AMENDMENT-B0R2.md`.
2. `ws/B2/s1/SPEC.md`.
3. `s1/claims.json`, `s2/claims.json`, `s3/claims.json`, and the markers `s1/t1.complete`, `s2/t2.complete`, `s3/t3.complete`.
4. `s3/certs/` (phi8.json, phi9.json, SHA256SUMS), `s3/check/check.json` and `CHECK.md`.
5. The Stage 1 and Stage 2 reviews, `s2/R2.md`, and the gate files.
6. Background:
   - Puleo's TeX: Def. 2.1, Lemma 2.2, Lemmas 2.6/2.7 and the `\robG`/`\robrem` macros, Lemma 4.4, Cors. 4.9/4.10, Cor. 5.3, and the statements of Lemmas 7.4–7.7;
   - Round 1's `campaign/ws/B/claims.json` (C1–C4).

I formed my verdicts on B2-D8 and B2-D9 from these, and recorded them in `ws/B2/state.json`. Only after that did I read `s3/ASSEMBLY.md` and `s3/NOTES.md`. I did not read `ws/B2/archive/`.

My code is all in this directory. It imports no author code and no checker code, and I ran it with `python3 -I`:
- `rv3.py` is my own implementation of SPEC §§2, 3, 5, 6 and 7:
  - V1–V5;
  - H(φ), its triangles, and R0–R4;
  - disconnectedness of the link;
  - a complete orbit invariant: the minimum over Sym(k) of a form invariant under Sym(m);
  - stabilisers, brute-forced over all k!·m! elements of Γ and cross-checked against a product formula;
  - the closed-form |L_d|.
- `brute_L.py` counts |L_d| by direct enumeration of item sequences and RGS strings. It does not use the Bell-number formula.
- `loc3.py` is a stress test of L0 on random host graphs.
- `mut3.py` runs mutation tests on phi9.json.

Logs: `run_rv3_d7.log`, `run_rv3_d8.log`, `run_rv3_d9.log`, `run_bruteL.log`, `run_loc3.log`, `run_mut3.log`.

## Frozen SPEC: was it used as accepted?

- **SPEC hash.** `shasum -a 256 ws/B2/s1/SPEC.md` = `a979f4bb…0f205`. This is identical to the hash bound by `s1/t1.complete`, so SPEC.md is unchanged since Stage 1.
- **Certificate hashes.** phi8.json = `38773308…`, phi9.json = `3b7c4c1b…`. Both match `s3/certs/SHA256SUMS`.
- **Φ_8 and Φ_9 match the definitions in SPEC §§2–3.** I implemented T_8 = {5x, 6x, 6t, 6s, 6se}, T_9 = all seven types, V4 (sub ≤ 2 at d = 9), and the (k, m) pairs of V1 directly from SPEC. With these:
  - every file entry passes V1–V5;
  - the entries are in pairwise distinct orbits;
  - their orbit sizes sum to my own |L_d|, both overall and separately for k = 4 and k = 5.

  So the files cover exactly the SPEC-defined L_8 and L_9: nothing was removed, added or redefined.
- **Methods.** Every V0 has the form {u} ∪ A′. The certificate kinds are the frozen ones, and none is `uncovered`.

## Verdicts

### B2-D8: NO ERROR FOUND

| Check | Result |
|---|---|
| Format, n_configs | ok (738) |
| K1: V1–V5 | holds for all 738 entries |
| K2 | 738 pairwise distinct orbit invariants |
| K3 | Σ k!m!/\|Stab\| = 11100 + 148186 = 159286. This equals my closed form, my brute-force count (`brute_L.py`: 148186 for k = 5), and `labelled_total`. Every `stabiliser_order` matches a brute-force count over all of Γ. |
| Certificates | 689 reducible, all of them valid under R0–R4 on my own H(φ) and triangle set, and all with V0 = {u} ∪ A (572 with m = 3, 117 with m = 4). 49 exclusions, whose links are all disconnected. 0 uncovered, 0 errors. |
| Locality (`loc3.py`) | 5512 random hosts G ⊇ H(φ), each keeping the facts of P1(e). The hosts add up to 4 outside vertices and random x–x, x–(B ∖ S), B–outside, x–outside and outside–outside edges. In each host I checked Def. 2.1 for ι(V0) directly in G: **0 failures**. As a control, adding B–B edges (which violates P1(e)) gave 622 failures out of 1378, so the test discriminates. |

This agrees with check3. check3 also ran an independent orbit enumeration (738 orbits, with exactly 0 missing and 0 extra) and 14 mutants. The claim's counts (689 / 0 / 49) are exact.

### B2-D9: NO ERROR FOUND

| Check | Result |
|---|---|
| K1: V1–V5 (including V4) | holds for all 5390 entries |
| K2 | 5390 pairwise distinct invariants |
| K3 | Σ = 236197 + 5689060 = 5925257. This equals my closed form, the brute-force counts of `brute_L.py` for both k, and `labelled_total`. Stabilisers were brute-forced over all of Γ (up to 2880 elements) and all match. |
| Certificates | 5212 reducible, all valid: 469 with (m = 5, \|A′\| = 5), 4734 with (m = 4, \|A′\| = 4), and 9 with (m = 4, \|A′\| = 3). This is exactly the claimed 5203 + 9. 178 valid exclusions. 0 uncovered. |
| The 9 entries with smaller V0 | My R4 check covers the S-edges incident to the a-vertex left outside V0 (a–b, a–x, b–b). L0 is stated for arbitrary A′, so a smaller V0 is allowed by SPEC §5.1. |
| Locality | 41696 random hosts, **0 failures**. |
| Mutations (`mut3.py`) | The author ran none on phi9, so I ran them. Every one of 10 mutants was rejected: dropping an X-edge, dropping an entry (with n_configs adjusted), duplicating an entry, stabiliser + 1, an exclusion placed on a connected link, `uncovered`, a b-vertex in V0, a smaller V0 on one of the 9 entries, a type change, and labelled_total − 1. An unmutated control was accepted. |

### B2-ASSEMBLY: NO ERROR FOUND

I tried to break each step.

**1. A minimal counterexample exists, and F0 holds for it.**
- A minimal counterexample exists by well-ordering.
- F0 (C2): for a reducible V0, G′ = (G − X) − V0 is a subgraph of G, so it is in D5 and smaller than G. The same holds for a reducible edge set.
- I checked, in the TeX, that every Puleo result used from §5 to §7 has only the hypothesis `\robG` or `\robrem`:
  - Lemma 2.7(a)–(f) and (h);
  - Prop. 5.1 and Prop. 5.2;
  - Cor. 5.3;
  - Lemmas 7.4–7.7.

  None of them uses mad, minimality or any class hypothesis. A grep for "minimal", "mad", "average" and "counterexample" after §5 finds only §6 (the mad < 25/4 theorem, not used) and the closing remarks.
- Robustness uses Cor. 4.9 (`cor:deg4`, "connected with ≤ 4 vertices ⇒ WKE") together with the first part of Lemma 4.4, which gives a reducible edge set. The citation is the right one. The adjacent Cor. 4.10 (`cor:small`) would not suffice, because it needs |V| > 5 when α′ = 2. SPEC cites the correct one.

**2. Existence of u (C3).**
- G has a triangle, hence an edge. I is independent (F2), so G − I ≠ ∅.
- G − I is a subgraph of G, so it is 5-degenerate and has a vertex u with |N(u) ∖ I| ≤ 5.
- No other property of u is used.

**3. The cases are exhaustive.**
- u ∉ I gives d(u) ≥ 7.
- {7}, {8}, {9} and {≥ 10} partition the integers ≥ 7.
- d(u) ≤ 6 is impossible, by the definition of I. No degree is missed or counted twice.

**4. The case d(u) ≥ 10.**
- R2 uses only F0–F2 and |N(u) ∖ I| ≤ 5. I re-checked Lemma W:
  - Step 1's case split for k ∈ {3, 4, 5};
  - Step 3's 8 distinct endpoints, and |Q| = 4 = |M|;
  - that Hall's theorem is applied to the B* side.
- R2 does not use F7 or F8, which are false or unproved for d ≥ 10. It is unbounded in m.
- Its status is a Verified result (review2, Gate 2).

**5. The cases d(u) = 7, 8, 9.**
- Cor. 5.4 is uniform in d. I re-verified:
  - P1(e) at u and at each a_i, pair class by pair class;
  - L0 step (3);
  - the corollary's relabelling argument.
- Nothing outside N[u] ∪ ⋃_a N[a] enters R3. S and X lie inside H, and every H-edge is a G-edge.
- The restrictions of Φ_d:
  - d = 8: only 5s and 5se are excluded, by F5 ("8⁻-vertex").
  - d = 9: V4 holds by F6 together with |A| ≥ 4 (F7, k ≤ 5).
  - (k, m) is forced by F7 together with k ≤ 5.
- Each restriction is cited, and its hypotheses hold by F0. I found no restriction that has no justification.

**6. The status of each dependency.**

| Dependency | Status | Source |
|---|---|---|
| P1, P2 | Verified result | review1, Gate 1 |
| D7 | Independently reproduced computation | check1 PASS, Gate 1 |
| D8, D9 | Independently reproduced computation | check3 PASS with its own enumeration and mutation tests; reproduced again here |
| R2 | Verified result | review2, Gate 2 |
| C2, C3 | "Proof; review found no error" | Round 1 |

**7. Unstated assumptions I looked for.**
- None found in the following:
  - the degrees of B- and x-vertices (never used);
  - whether x_a ∈ A ∪ B (excluded, since x_a ∉ N[u]);
  - A ≠ ∅ (not needed: m ≥ 2 by V1, and R2 has m ≥ 5);
  - whether the u of R2 and the u of Cor. 5.4 are the same object (they are: both are SPEC §1.3's u);
  - whether a certificate found in H(φ) might need edges absent from G (no: every H-edge is a G-edge).
- **The one standing assumption** is that Puleo's published proofs are correct: Lemmas 2.2, 4.3, 4.4, Cor. 4.9, Props 5.1 and 5.2, Cor. 5.3, and Lemmas 7.4–7.7. This round did not re-prove them, and neither did Round 1. ASSEMBLY.md §0/§3 states this explicitly, so it is not hidden.

**Procedural remarks (not mathematical errors).**
- **S3 time limit.** The d = 9 certificate search took 26.8 min of wall time on 10 processes, which is about 4.5 h of CPU time. The first d = 9 attempt was killed when its brute-force canonicalisation proved far slower than predicted.
  - The method used for Φ_9 did not change: only the enumeration code was rewritten. The run that produced the certificates stayed under 30 min of wall time.
  - Whether S3's "30 minutes" means wall time or CPU time is for the operator to note. It has no bearing on the validity of the certificates, which are checked independently.
- **The 9 smaller-V0 entries.** For these, the solve with V0 = {u} ∪ A hit its time limit. This is irrelevant to validity, since each saved certificate is checked directly.

## P1–P6: final statuses (amendment §7)

| | Final status | Basis |
|---|---|---|
| P1 Structure lemma (d = 7, 8, 9) | **Verified result** | review1 NO ERROR FOUND. Re-checked here for its use at d = 8 and 9 (T_8, V4). |
| P2 Locality lemma L0 and Cor. 5.4 | **Verified result** | review1. Re-checked here, plus 47,208 random-host tests at d = 8 and 9 with 0 failures. |
| P3 Coverage | **Independently reproduced computation** for d = 7, 8 and 9 | The frozen SPEC §7 argument was accepted by review1. K1–K3 were passed under check1 (d = 7), under check3 (d = 8, 9, with an independent enumeration), and under my own code. \|L_d\| was confirmed by a brute-force count. |
| P4 Certificates | **Independently reproduced computation** for d = 7, 8 and 9 | check1 and check3 PASS with mutation tests. Every certificate was re-validated here. |
| P5 R2 (d ≥ 10) | **Verified result** | review2. The proof was re-read here. |
| P6 Assembly | **Verified result** | Written proof. This review found no error, and its finite dependencies (D7, D8, D9) are independently reproduced. |

## Overall conclusion

I tried to find a gap in the assembled argument and did not find one:
- the cases d(u) = 7, 8, 9 and d(u) ≥ 10 are exhaustive;
- each case is closed by a result with the status §7 requires;
- the configuration spaces are correct over-approximations, with every restriction cited;
- Φ_8 and Φ_9 were used exactly as the frozen SPEC (hash a979f4bb…) defines them.

**The B0 theorem, "every 5-degenerate graph satisfies τ ≤ 2ν", is supported as a Verified result in the sense of §7.** This holds subject to two things, which ASSEMBLY.md states openly:
- the standing assumption that Puleo's cited published lemmas are correct;
- the Round 1 status of C2 and C3.

No stop rule fired on the mathematical side. The S3 wall-time versus CPU-time point above is noted for the operator.
