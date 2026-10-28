# R2: for d(u) ≥ 10 the link of u is WKE, so {u} is reducible

B2.t2, amendment B0R2, Stage 2. Uses the setting and definitions of `ws/B2/s1/SPEC.md` (B2-SPEC-v1, accepted
at Gate 1). Page numbers refer to Puleo, arXiv:1308.2211v3.

## 0. Statement

**Setting.** G is the minimal counterexample of SPEC §1.2 (a counterexample to τ ≤ 2ν in the class D5 of
5-degenerate graphs, with |V(G)| + |E(G)| minimal). I = {v : d(v) ≤ 6}. u ∉ I is a vertex with
|N(u) ∖ I| ≤ 5 (SPEC §1.3; such u exists). B = N(u) ∖ I, A = N(u) ∩ I, and S_a = N(a) ∩ N(u) for a ∈ A.

**Theorem R2.** In this setting, d(u) ≤ 9. Equivalently: if d(u) ≥ 10, then G[N(u)] is WKE, hence {u} is
reducible (Puleo Lemma 4.4, p. 10), contradicting F0.

The proof has two parts:
- §1 derives three facts (H1)–(H3) about A, B and the S_a for d(u) ≥ 10, from SPEC and Puleo only;
- §2 proves a purely graph-theoretic lemma (Lemma W) that (H1)–(H3) imply WKE;
- §3 combines them.

No use is made of SPEC Lemma P1 (which is stated for d ∈ {7, 8, 9} only), of F3–F8, or of Puleo Lemma 7.3.
Only F0, F1, F2 and the definition of u are used.

## 1. The hypotheses and their derivation

Write H = G[N(u)], k = |B|, m = |A|, d = d(u) = k + m (A and B partition N(u) by definition).
Assume d ≥ 10.

- **(H1) |B| ≤ 5 and |A| ≥ max(|B|, 4).**
  - k = |N(u) ∖ I| ≤ 5 by the choice of u (SPEC §1.3).
  - m = d − k ≥ 10 − 5 = 5. So m ≥ 5 ≥ k and m ≥ 4.
- **(H2) A is an independent set of G, so A is independent in H, and N_H(a) = S_a ⊆ B for each a ∈ A.**
  - A ⊆ I, and I is independent by F2 (Puleo Lemma 2.7(b) / Prop. 5.2, p. 15; applicable by F0).
  - N_H(a) = N(a) ∩ N(u) = S_a by definition of H and S_a. S_a contains no vertex of A (independence), and
    S_a ⊆ N(u) = A ∪ B, so S_a ⊆ B. (This is the remark "By F2, S_a ⊆ B" of SPEC §1.3.)
- **(H3) |S_a| ≥ 3 for every a ∈ A.**
  - By F1 (Puleo Lemma 2.7(a) / Prop. 5.1, p. 14; applicable by F0), d(a) ∈ {5, 6} and the complement of
    G[N(a)] has maximum degree ≤ 1.
  - u ∈ N(a) since a ∈ N(u). So u has at most one non-neighbour in N(a) ∖ {u}, i.e.
    |N(a) ∩ N(u)| ≥ (d(a) − 1) − 1 = d(a) − 2 ≥ 3.
  - This is the argument of Puleo, proof of Lemma 7.3, p. 19 ("d_B(a) ≥ 3 for all a ∈ A"), which uses only
    Prop. 5.1 and Prop. 5.2, not the subsumption hypothesis of Lemma 7.3.

Nothing else about A, B, S_a is assumed. In particular the lemma below does not need the S_a to be of the
types K3, K4, C4 (although, by Puleo Lemma 7.3, p. 18, u subsumes no vertex of A when |A| ≥ d − 5, so those are
in fact the only types; this is not used).

## 2. Lemma W (graph theory)

**Definition** (Puleo Def. 4.1, p. 9; SPEC §1.1). A graph H is WKE if there are a matching M of H and a set
Q ⊆ V(H) with |Q| ≤ |M| such that every edge of H not in M has an endpoint in Q.

**Lemma W.** Let H be a graph whose vertex set is the disjoint union A ⊔ B, where
- (W1) |B| ≤ 5 and |A| ≥ max(|B|, 4);
- (W2) A is independent in H;
- (W3) every a ∈ A has d_B(a) := |N_H(a) ∩ B| ≥ 3.

Then H is WKE.

**Proof.** Put k = |B|. By (W2), every edge of H is either an A–B edge or a B–B edge, and N_H(a) ⊆ B for
a ∈ A. By (W3), each a ∈ A has at most k − 3 ≤ 2 non-neighbours in B. A is nonempty by (W1).

Let B* = {b ∈ B : b has a neighbour in A} and B° = B ∖ B*. For any a ∈ A, N_H(a) ⊆ B*, so by (W3) |B*| ≥ 3 and
|B°| ≤ k − 3 ≤ 2.

For T ⊆ B write N_A(T) = {a ∈ A : a has a neighbour in T}. Call a nonempty T ⊆ B* *deficient* if
|N_A(T)| < |T|.

**Step 1: the only possible deficient sets.** Let T ⊆ B* be nonempty.
- If |T| = 1, T = {b} with b ∈ B*, so |N_A(T)| ≥ 1 = |T|. Not deficient.
- If |T| ≥ k − 2, then T is larger than the set of non-neighbours in B of any a ∈ A (which has size ≤ k − 3),
  so every a ∈ A has a neighbour in T: N_A(T) = A and |N_A(T)| = |A| ≥ k ≥ |T| by (W1). Not deficient.
- Otherwise 2 ≤ |T| ≤ k − 3 ≤ 2. So a deficient T has k = 5, |T| = 2 and |N_A(T)| ≤ 1; as T ⊆ B* is nonempty,
  |N_A(T)| = 1.

**Step 2: no deficient set.** By Hall's theorem applied to the bipartite graph of A–B* edges of H, there is
a matching M1 of H consisting of A–B* edges that covers every vertex of B*; |M1| = |B*|.
- If |B°| = 2, say B° = {c, c′}, and cc′ ∈ E(H), put M2 = {cc′}. Otherwise M2 = ∅.
- M = M1 ∪ M2 is a matching: the vertices of M2 lie in B°, and those of M1 in A ∪ B*.
- Q = B*. Then |Q| = |B*| = |M1| ≤ |M|.
- Cover check. Let e be an edge of H.
  - e = ab with a ∈ A, b ∈ B: then b ∈ B* = Q by definition of B*.
  - e = bb′ ⊆ B with an endpoint in B*: covered by Q.
  - e = bb′ ⊆ B°: then |B°| = 2, e = cc′, and e ∈ M2 ⊆ M.

  So every edge not in M has an endpoint in Q, and H is WKE.

**Step 3: a deficient set exists.** By Step 1, k = 5 and there is T = {t1, t2} ⊆ B* with N_A(T) = {a0}.
- t1, t2 ∈ B* each have a neighbour in A, which must lie in N_A(T) = {a0}. So a0t1, a0t2 ∈ E(H).
- Let R = B ∖ T, |R| = 3. For a ∈ A ∖ {a0}, N_H(a) ∩ T = ∅, so N_H(a) ⊆ R; by (W3) N_H(a) = R.
- |A ∖ {a0}| ≥ 3 by (W1) (|A| ≥ 4). Choose distinct a1, a2, a3 ∈ A ∖ {a0} and write R = {r1, r2, r3}. Then
  a_i r_i ∈ E(H) for i = 1, 2, 3.
- Let e* = t1t2 if t1t2 ∈ E(H), and e* = a0t1 otherwise. Put M = {a1r1, a2r2, a3r3, e*}. Its 8 endpoints are
  distinct (a0, a1, a2, a3 distinct; r1, r2, r3, t1, t2 are the five distinct vertices of B), so M is a
  matching, |M| = 4.
- Q = R ∪ {a0}, |Q| = 4 = |M|.
- Cover check. Let e be an edge of H.
  - e has endpoint a0: covered by Q.
  - e = ab with a ∈ A ∖ {a0}, b ∈ B: b ∈ N_H(a) = R ⊆ Q.
  - e = bb′ ⊆ B with an endpoint in R: covered.
  - e = bb′ ⊆ B with no endpoint in R: {b, b′} = T, so e = t1t2 ∈ E(H), hence e* = t1t2 and e ∈ M.

  So H is WKE.

Steps 2 and 3 are exhaustive. ∎

## 3. Proof of Theorem R2

Suppose d(u) ≥ 10. Let H = G[N(u)], with the partition N(u) = A ⊔ B. By §1, (H1) gives (W1), (H2) gives (W2),
and (H2)+(H3) give (W3) (d_B(a) = |S_a| ≥ 3). By Lemma W, G[N(u)] is WKE. By Puleo Lemma 4.4 (p. 10; its proof
takes M and Q from the WKE witness, S = {u y z : yz ∈ M}, X = M ∪ {u q : q ∈ Q}), {u} is reducible in G. This
contradicts F0 (SPEC §1.2: G has no reducible vertex set). Hence every u as in SPEC §1.3 has d(u) ≤ 9; since
u ∉ I, d(u) ∈ {7, 8, 9}. ∎

## 4. Remarks on the hypotheses

- (W1) cannot simply be dropped: for (|B|, |A|) ∈ {(4, 3), (5, 3), (5, 4)} there are non-WKE graphs satisfying
  (W2) and (W3) (sanity runs, `src/run_small.log`, `src/run_k5.log`; not part of the proof). These do
  not arise for d(u) ≥ 10, where |A| ≥ 5 ≥ |B|.
- Lemma W is the non-subsuming extension of Puleo's proof of Lemma 7.3 (pp. 18–19). Puleo uses the subsumed
  vertex w (with d_B(w) ≥ 4) to rule out the deficient pair; here the deficient pair is handled directly by
  Step 3, which needs |A| ≥ 4 instead.
