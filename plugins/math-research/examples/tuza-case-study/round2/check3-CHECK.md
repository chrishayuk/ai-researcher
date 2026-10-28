# CHECK (B2.check3): blind check of the degree-8 and degree-9 certificates

Code written from scratch in this directory, from SPEC.md only (python stdlib + networkx):
- `chk.py`: V1-V5, literal Gamma action (SPEC 3.3), brute-force canonical form and stabiliser, own closed-form |L_d|, H(phi)/L(phi) construction, independent recomputation of the triangle set, R0-R4 check, disconnected-link check.
- `match.py`: independent enumeration of Phi_d and comparison with the certificate files (uses a second, structurally different canonical form).
- `mut.py`: mutation tests.
The author's source and lists were not read.

## B2-D8 (certs/phi8.json): PASS
1. Own enumeration of Phi_8 (one E_B per isomorphism class; multisets of subsumed items and partitions of x-bearing items into blocks; canonicalised under Aut(E_B)): 738 orbits.
2. Matching with phi8.json (738 entries): 0 missing, 0 extra, 0 duplicates, 0 uncovered.
3. All 738 entries pass V1-V5 and their certificates: 689 reducible (R0-R4 on my recomputed H(phi) and triangle set), 49 disconnected link. Zero errors.
4. Completeness (SPEC 7.1): K1 ok; K2 all literal-canonical forms distinct (brute force over k!m! group elements); K3 stabiliser_order matches for every entry; sum of k!m!/|Stab| = 159286 = my closed-form |L_8| = labelled_total.
5. Mutation tests (14 per degree), all rejected: dropped config with and without n_configs adjusted (orbit sum 159270 != 159286), dropped last config, X edge removed (R3), S triangle removed (R2), non-triangle in S, bogus reducible cert on a link entry, reducible entry marked excluded (link connected), reducible marked uncovered, duplicated orbit, stabiliser_order +1, labelled_total +1, V0 shrunk to {u} (R4), invalid x (V5).

## B2-D9 (certs/phi9.json): PASS
Same procedure. Own enumeration: 5390 orbits (with the sub <= 2 restriction). Matching with phi9.json (5390 entries): 0 missing, 0 extra, 0 duplicates, 0 uncovered. 5212 reducible + 178 excluded, all valid. K2 distinct, K3 stabilisers match, orbit sum = 5925257 = my |L_9| = labelled_total. All 14 mutations rejected (see above; output in this session's mut.py run).

## Sufficiency (does a valid certificate establish the statement?) -- no gap found
- Types and T_d: re-derived from P1(b) with F1. u covered or not by M_a gives exactly the seven types. T_8 excludes 5s, 5se (F5, 8^- vertex), allows 6t (F4 concerns 7-vertices only), 6s, 6se (F3 concerns 7-vertices only). T_9 with sub <= 2 follows from F6 (at most three subsumed; three would force no other 6^- neighbour, but |A| >= 4 by F7). I checked F1, F3-F7 against the statements in Puleo's TeX (Lemma redlem (a)-(h)); they match.
- Case split k in {4,5}, m = d - k: from m <= d - 4 (F7) and |B| <= 5 (choice of u). Complete for d = 8, 9.
- The certificate is only needed for V0 = {u} + A', a set of vertices whose full closed neighbourhoods are determined in H (N_H(u), N_H(a_i) map onto the true neighbourhoods and induced adjacencies on them, P1(e)); L0's proof (triangles through V0 vertices lie inside those neighbourhoods; R4 edges map injectively) is sound and uses no assumption about the rest of G. Unknown edges (x-x, x to B outside S, B-B nothing unknown since E_B is recorded) cannot create triangles through V0 vertices, so they cannot matter.
- Disconnected-link exclusions are valid because F8 (d <= 9, components >= 5 vertices) makes G[N(u)] connected; L(phi) is the true link.
- The conclusion is exactly the claim's statement (no u outside I with |N(u)\I| <= 5 and d(u) = 8 or 9), given F0 (minimal counterexample, robust, no reducible set) from SPEC section 1.2. I did not re-check F0-F8 beyond Puleo's statements (SPEC's proof of P1 is outside this task's blind scope).

## B2-ASSEMBLY: NOT FINITE (type proof; not a finite claim; not checked here)
