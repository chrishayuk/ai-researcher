# B2.check1: blind check of the B2 claims (d = 7)

Checker code: `chk.py` (own enumeration, canonical forms, H(φ), R0–R4, K1–K3), `run.py`, `mut.py`; outputs in `run_output.txt`, `mutation_output.txt`. Certificate file hash matched `certs/SHA256SUMS` (63d5bd00…).
I read only SPEC.md, claims.json, certs/, and the Puleo text (Def. 2.1, Lemma 2.7 statements).

## B2-D7 (finite certificate): PASS
1. **Enumeration.** From SPEC §§2–3 only, I generated all of L_7 (k∈{4,5}, every graph E_B, every (type,S) for 5x/6x with the required induced graph, every restricted-growth x). |L_7| = 10305, which equals the independent formula count of §7.1. I took Γ-orbits via a brute-force canonical form: 174 orbits (38 for k=4, 136 for k=5), matching the author's figures.
2. **Matching.** Missing 0, extra 0, duplicates 0, uncovered 0. All 174 entries are covered: 153 `reducible` and 21 `excluded_disconnected_link`.
3. **Certificates.** My checker rebuilt H(φ) and its triangle set, and checked R0–R4 for each of the 153 reducible entries (V0 ∋ u, V0 ⊆ {u,a_i}; S triangles of H, edge-disjoint; X ⊆ E(H); |X| ≤ 2|S|; every triangle through V0 meets X; every S-edge outside V0 is in X). All valid. For the 21 excluded entries, L(φ) is disconnected. K1 (V1–V5) holds for all entries. Recomputed `stabiliser_order` agrees everywhere, the orbit sum is 10305, and `labelled_total` is correct.
4. **Mutation tests.** 13 corruptions were rejected, including: a dropped configuration, a duplicated configuration, a dropped X edge, a dropped S triangle, V0 shrunk to {u}, a non-triangle in S, an excluded entry marked `uncovered`, a reducible entry flipped to `excluded` (its link is connected), an excluded entry flipped to an empty reducible certificate, a changed x, a wrong stabiliser, a wrong labelled_total, and b0 added to V0. Also, deleting any single X edge from any reducible certificate was rejected in 1823 of 1830 cases (the other 7 are redundant edges, not a checker fault).
5. **Coverage argument (§7.2).** Sound: entries are distinct orbits within L_d, and their sizes (k!m!/|Stab|) sum to |L_d|, so they exhaust it. My direct enumeration agrees (K4).
6. **Does a valid file establish the statement?** Yes, given P1 and L0. I checked these as follows:
   - **Definitions.** Def. 2.1 and Lemma 2.7(a)–(h) in SPEC match Puleo's text.
   - **T_7.** Only `5x`/`6x` remain. F3 excludes the subsumed 6-types, F4 excludes thin `6t`, and F5 excludes `5s`/`5se`.
   - **Size of B.** m ≤ 3 by (h), and k ≤ 5 by the choice of u, so (k,m) ∈ {(4,3),(5,2)}.
   - **Locality.** L0 only uses N(ι(v)) for v in {u}∪A, which P1(e) pins down, so assuming nothing about the rest of G is legitimate.
   - **Closure.** The configuration space is a superset of what can occur (arbitrary G[B]), so extra cases only strengthen the result. The connected-link exclusion is justified by F8.
   - **Scope.** The statement is only "no such u of degree 7 in a minimal D5 counterexample". That is exactly what the claim says, and it is not a proof of Tuza on D5.
   - **Not re-verified.** Puleo's own lemmas (F1–F7) and the F0 transfer to D5 are taken from the cited text; I did not re-prove them.

## B2-P1, B2-L0 (proofs): NOT FINITE
Not a finite claim; not checked here. (I read the arguments in SPEC §§4–5 for the D7 sufficiency judgement above and found no gap.)
