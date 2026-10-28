# B2 SPEC: the configuration spaces Φ_7, Φ_8, Φ_9 for B0, the structure lemma P1, the locality lemma L0, the certificate format and the completeness checks

Version B2-SPEC-v1 (B2.t1, 2026-10-25). Frozen with Stage 1 of amendment B0R2. Stage 3 is bound to it.

Source for every citation: H. Puleo, *Tuza's Conjecture for graphs with maximum average degree less than 7*,
arXiv:1308.2211v3 (page numbers refer to that PDF). Statements that involve complements were checked against
the TeX source, because the PDF text drops overlines.

---

## 1. Setting and definitions

### 1.1 Basic notions

- **Graphs.** All graphs are finite and simple.
  - A *triangle* is a set of three pairwise adjacent vertices; its *edges* are its three pairs.
  - ν(G) is the largest number of pairwise edge-disjoint triangles of G.
  - τ(G) is the smallest size of an edge set X such that G − X has no triangle.
  - G is *Tuza* if τ(G) ≤ 2ν(G).
- **Neighbourhoods.** N(v) is the open neighbourhood of v and N[v] = N(v) ∪ {v}. d(v) = |N(v)|.
  - A *k-vertex* has degree k. A *k⁻-vertex* has degree ≤ k.
  - The *link* of v is G[N(v)].
  - H̄ is the complement of H.
  - K_n − e is K_n minus one edge. K_n − je is K_n minus a matching of j edges.
- **5-degenerate.** G is 5-degenerate if every subgraph of G (including G itself) has a vertex of degree ≤ 5.
  The class D5 of 5-degenerate graphs is closed under taking subgraphs.
- **WKE** (Puleo Def. 4.1, p. 9). A graph H is *weak König–Egerváry* if there are a matching M of H and a set
  Q ⊆ V(H) with |Q| ≤ |M| such that every edge of H not in M has an endpoint in Q.
- **Reducible vertex set** (Puleo Def. 2.1, p. 4). Let S be a set of triangles of G. An *S-edge* is an edge of
  some triangle in S. A nonempty set V0 ⊆ V(G) is *reducible* (in G) if there exist a set S of pairwise
  edge-disjoint triangles of G and a set X ⊆ E(G) such that:
  - (i) |X| ≤ 2|S|;
  - (ii) G − X has no triangle containing a vertex of V0;
  - (iii) X contains every S-edge whose two endpoints are both outside V0.
- **Reducible edge set** (Puleo Def. 4.2, p. 9). A nonempty E0 ⊆ E(G) is *reducible* if there exist a set S of
  pairwise edge-disjoint triangles and a set X ⊆ E(G) such that:
  - (i) |X| ≤ 2|S|;
  - (ii) G − X has no triangle containing an edge of E0;
  - (iii) X contains every S-edge not in E0.
- **Robust** (Puleo Def. 2.3, p. 5). G is robust if, for every vertex v, every component of G[N(v)] has at
  least 5 vertices.
- **Subsumes** (Puleo Def. 2.4, p. 5). u *subsumes* v if N[u] ⊇ N[v].
- **Thin** (Puleo Def. 2.5, p. 5; overline confirmed in the TeX). A 6-vertex v is *thin* if the complement of
  G[N(v)] contains a matching of size 3.

### 1.2 The minimal counterexample and its inherited properties

Let G be a counterexample to τ ≤ 2ν in D5 with |V(G)| + |E(G)| minimal among counterexamples in D5. Let
I = {v : d(v) ≤ 6}. The following facts are used. F0 and F8 are proved here. F1–F7 are Puleo's Lemma 2.7,
which applies to G because of F0.

- **F0. G is robust and has no reducible vertex set and no reducible edge set.**
  - *Proof.* Suppose V0 is reducible using S and X. Let G′ = (G − X) − V0. Then G′ is a subgraph of G, so
    G′ ∈ D5. It is smaller than G, because V0 ≠ ∅. By minimality G′ is Tuza. So G is Tuza by Puleo Lemma 2.2
    (p. 4), a contradiction.
  - The same argument works for a reducible edge set E0, with G′ = (G − X) − E0 and Puleo Lemma 4.3 (p. 10).
  - Robustness: suppose some component of some link G[N(v)] has order ≤ 4. Let G0 be that component. G0 is
    connected with ≤ 4 vertices, so G0 ∈ WKE (Puleo Cor. 4.9, p. 12). Then G has a reducible edge set (Puleo
    Lemma 4.4, p. 10), a contradiction. (This is Puleo's proof of Lemma 2.6, p. 13.)
  - G has no isolated vertex v, since otherwise {v} is reducible with S = X = ∅. So every vertex has degree ≥ 5.
  - (Round 1 claim C2: status "Proof; review found no error".)
- **F1** (Lemma 2.7(a), pp. 5–6; Prop. 5.1, p. 14). If d(v) ≤ 6, then:
  - d(v) ∈ {5, 6}, by F0;
  - the complement of G[N(v)] has maximum degree ≤ 1, and it does not have exactly 2 edges.

  Hence G[N(v)] is K_{d(v)} minus a matching M_v, where:
  - |M_v| ∈ {0, 1} if d(v) = 5;
  - |M_v| ∈ {0, 1, 3} if d(v) = 6.

  (A matching on 5 vertices has ≤ 2 edges, and one on 6 vertices has ≤ 3.)
- **F2** (Lemma 2.7(b); Prop. 5.2, p. 15). I is an independent set.
- **F3** (Lemma 2.7(c); Lemma 7.6, p. 23). No 7-vertex subsumes a 6-vertex.
- **F4** (Lemma 2.7(d); Lemma 7.7, p. 24). No 7-vertex is adjacent to a thin 6-vertex.
- **F5** (Lemma 2.7(e); Lemma 7.5, p. 21, with Prop. 5.2). No 8⁻-vertex subsumes a 5-vertex.
- **F6** (Lemma 2.7(f); Lemma 7.4, p. 19). A 9-vertex subsumes at most three 6⁻-vertices. If it subsumes three,
  it is adjacent to no other 6⁻-vertex.
- **F7** (Lemma 2.7(h); Cor. 5.3, p. 17). A vertex v with d(v) ∈ {7, 8, 9} has at most d(v) − 4 neighbours in I.
- **F8** (Puleo, remark after Def. 2.3, p. 5). If d(v) ≤ 9, then G[N(v)] is connected.
  - *Proof.* Each component of G[N(v)] has ≥ 5 vertices (F0). Two components would need ≥ 10 vertices.

Puleo's Lemma 2.7 has the hypothesis "G is robust and has no reducible set" (p. 5), which F0 supplies. None of
the cited results uses an average-degree bound or a class hypothesis. (Round 1 review of C2, "NO ERROR FOUND".)

### 1.3 The vertex u, and the sets A, B, S_a, x_a

- **The vertex u.** Let u ∉ I be a vertex with |N(u) ∖ I| ≤ 5.
  - Such a u exists: G − I is a nonempty subgraph of G, hence 5-degenerate (Round 1 claim C3).
  - This SPEC concerns u with d(u) = d ∈ {7, 8, 9}.
- **The sets A and B.** Put B = N(u) ∖ I and A = N(u) ∩ I.
- **The set S_a.** For a ∈ A put S_a = N(a) ∩ N(u). By F2, S_a ⊆ B.
- **The vertex x_a.** If u does not subsume a, let x_a be the unique vertex of N(a) ∖ N[u]. Lemma P1(b) shows
  that it exists and is unique.

---

## 2. Types of A-vertices

Each a ∈ A has exactly one of the following seven *types* (Lemma P1(b)). The column "G[B][S]" gives the
isomorphism type of the subgraph of G[B] induced by S_a.

| type | d(a) | link of a | u subsumes a? | has x_a? | \|S_a\| | G[B][S_a] |
|---|---|---|---|---|---|---|
| `5x`  | 5 | K5 − e (the missing edge is u x_a) | no  | yes | 3 | K3 |
| `6x`  | 6 | K6 − e (the missing edge is u x_a) | no  | yes | 4 | K4 |
| `6t`  | 6 | K2,2,2 (thin; u x_a is one of the 3 missing edges) | no | yes | 4 | C4 |
| `5s`  | 5 | K5 | yes | no | 4 | K4 |
| `5se` | 5 | K5 − e (the missing edge avoids u) | yes | no | 4 | K4 − e |
| `6s`  | 6 | K6 | yes | no | 5 | K5 |
| `6se` | 6 | K6 − e (the missing edge avoids u) | yes | no | 5 | K5 − e |

- **Recognising the type from G[B][S].** "G[B][S] ≅ K3, K4, C4, K4 − e, K5, K5 − e" is equivalent to "|S| = 3, 4,
  4, 4, 5, 5 and the number of edges of G[B][S] is 3, 6, 4, 5, 10, 9 respectively". For C4 one also needs every
  vertex of S to have degree 2 in G[B][S]. (On 4 vertices with 4 edges, the only other graph is a triangle
  with a pendant edge, which fails the degree test.)
- **x-bearing and subsumed types.** Types `5x`, `6x`, `6t` are *x-bearing*. The other four are *subsumed*.
- **Allowed types T_d.** Here sub(φ) is the number of A-vertices of subsumed type.

| d | allowed types T_d | extra restriction | justification |
|---|---|---|---|
| 7 | `5x`, `6x` | none | F3 excludes `6s`, `6se`. F4 excludes `6t`. F5 excludes `5s`, `5se`. |
| 8 | `5x`, `6x`, `6t`, `6s`, `6se` | none | F5 excludes `5s`, `5se`. |
| 9 | all seven | sub(φ) ≤ 2 | F6 together with \|A\| ≥ 4 (see P1(a)). |

---

## 3. The configuration space Φ_d (d ∈ {7, 8, 9})

### 3.1 Labelled configurations

A **labelled configuration of degree d** is a tuple φ = (k, m, E_B, (τ_i, S_i)_{i<m}, x) such that:

- **(V1)** k ∈ {4, 5} and m = d − k. Hence:
  - d = 7: (k, m) ∈ {(4, 3), (5, 2)};
  - d = 8: (k, m) ∈ {(4, 4), (5, 3)};
  - d = 9: (k, m) ∈ {(4, 5), (5, 4)}.
- **(V2)** E_B is a set of pairs {p, q} with 0 ≤ p < q < k. It is the edge set of G[B] on B = {0, …, k−1}.
- **(V3)** For each i < m, τ_i ∈ T_d, and S_i ⊆ {0, …, k−1} has the size and induced graph that §2 requires
  for τ_i. The induced graph is the graph ({0, …, k−1}, E_B)[S_i].
- **(V4)** For d = 9: at most 2 indices i have τ_i of subsumed type.
- **(V5)** x = (x_0, …, x_{m−1}) has these properties:
  - x_i = null exactly when τ_i is a subsumed type;
  - otherwise x_i is a non-negative integer;
  - the integers form a *restricted growth string* in index order: the first non-null value is 0, and each
    non-null value is at most 1 + the largest non-null value before it.

  x encodes a set partition π(φ) of the x-bearing indices: i and j are in the same block iff x_i = x_j.

The set of all labelled configurations of degree d is called **L_d**. It is finite.

Nothing is recorded about the adjacencies between distinct outside vertices, or between an outside vertex
and B ∖ S_i, or about anything else in G. L0 (§4) shows that no certificate condition depends on them, so
they need not be enumerated.

### 3.2 The local graph H(φ) and the link L(φ)

- **The local graph H(φ).**
  - Vertices:
    - `u`;
    - `b0` … `b{k−1}`;
    - `a0` … `a{m−1}`;
    - `x0` … `x{r−1}`, where r = number of blocks of π(φ), and `xp` is the block with value p.
  - Edges, and nothing else:
    - u–b_j for all j;
    - b_p–b_q for {p, q} ∈ E_B;
    - u–a_i for all i;
    - a_i–b_s for s ∈ S_i;
    - for x-bearing i with x_i = p: a_i–x_p, and x_p–b_s for s ∈ S_i.
- **The link L(φ)** is the graph on {0, …, k+m−1} with:
  - the edges E_B;
  - an edge {s, k+i} for each i and each s ∈ S_i.

  (It is H(φ)[{b_j} ∪ {a_i}], relabelled.)

### 3.3 Isomorphism and Φ_d

The group Γ_{k,m} = Sym(k) × Sym(m), of order k!·m!, acts on the labelled configurations with given (k, m).
A pair (σ, ρ) sends φ to φ′, where:
- E′_B = {{σ(p), σ(q)} : {p, q} ∈ E_B};
- τ′_{ρ(i)} = τ_i;
- S′_{ρ(i)} = σ(S_i);
- x′ is the restricted growth string of the partition {ρ(P) : P ∈ π(φ)}, i.e. x′_{ρ(i)} and x′_{ρ(j)} are
  equal iff x_i = x_j.

Conditions V1–V5 are invariant under this action.

**Φ_d is the set of Γ-orbits of L_d.** A configuration "in Φ_d" means any labelled representative of an orbit.
Two representatives of one orbit give isomorphic local graphs, by an isomorphism that maps u to u, A to A,
B to B and the x's to the x's.

**Exact sizes, computed by the author** (Burnside's lemma, for cross-checking only; §6 says how a checker
confirms them independently):

| d | \|L_d\| (k = 4, k = 5) | \|L_d\| | \|Φ_d\| (k = 4 + k = 5) | \|Φ_d\| |
|---|---|---|---|---|
| 7 | 945 + 9360 | 10305 | 38 + 136 | 174 |
| 8 | 11100 + 148186 | 159286 | 122 + 616 | 738 |
| 9 | 236197 + 5689060 | 5925257 | 476 + 4914 | 5390 |

---

## 4. P1: the structure lemma

**Lemma P1.** Let G, I and u be as in §1, with d = d(u) ∈ {7, 8, 9}. Let A, B, S_a be as in §1.3. Then:

- **(a)** |A| = m with m ≤ d − 4, and |B| = k ∈ {4, 5}, where k = d − m.
- **(b)** Each a ∈ A has exactly one type of §2. If the type is x-bearing, x_a exists and is unique, and:
  - x_a ∉ N[u];
  - x_a ∉ I;
  - x_a is adjacent to a and to every vertex of S_a;
  - N(a) = {u} ∪ S_a ∪ {x_a}.

  If the type is subsumed, N(a) = {u} ∪ S_a. In every case G[S_a] has the isomorphism type given in §2.
- **(c)** The type of each a lies in T_d. If d = 9, at most 2 vertices of A have subsumed type.
- **(d)** Choose bijections β: B → {0, …, k−1} and α: A → {0, …, m−1}. Define:
  - E_B = {{β(b), β(b′)} : bb′ ∈ E(G[B])};
  - τ_{α(a)} = type of a;
  - S_{α(a)} = β(S_a);
  - x = the restricted growth string of the partition of the x-bearing indices in which α(a) ~ α(a′) iff
    x_a = x_{a′}.

  Then φ = (k, m, E_B, (τ_i, S_i), x) ∈ L_d.
- **(e)** There is an injective map ι: V(H(φ)) → V(G) with:
  - u ↦ u, b_j ↦ β⁻¹(j), a_i ↦ α⁻¹(i);
  - x_p ↦ the common vertex x_a of the A-vertices a with x_{α(a)} = p.

  It maps every edge of H(φ) to an edge of G. For every v ∈ {u} ∪ {a_i}:
  - N_G(ι(v)) = ι(N_H(v));
  - for all y, z ∈ N_H(v): yz ∈ E(H(φ)) iff ι(y)ι(z) ∈ E(G).
- **(f)** L(φ) is isomorphic to G[N(u)] and is connected.

**Proof.**

(a)
- m = |A| ≤ d − 4 by F7.
- k = |B| ≤ 5 by the choice of u. So m = d − k ≥ d − 5 ≥ 2, and k = d − m ≥ 4.

(b) Let a ∈ A. By F1, d(a) ∈ {5, 6} and G[N(a)] = K_{d(a)} − M_a, with M_a a matching of the sizes listed in
F1. Since a ∈ N(u), we have u ∈ N(a), and S_a = N(a) ∩ N(u) = N_{G[N(a)]}(u). Because M_a is a matching, u
has at most one non-neighbour in N(a): its M_a-partner, if u is covered by M_a.

- **Case 1: u is not covered by M_a.**
  - Then S_a = N(a) ∖ {u}, so N[a] = {a, u} ∪ S_a ⊆ N[u]: u subsumes a.
  - G[S_a] = G[N(a)] − u = K_{d(a)−1} − M_a.
  - d(a) = 5: |M_a| = 0 gives K4 (type `5s`), and |M_a| = 1 gives K4 − e (type `5se`).
  - d(a) = 6: |M_a| = 0 gives K5 (`6s`), and |M_a| = 1 gives K5 − e (`6se`). |M_a| = 3 is impossible: a
    3-edge matching on 6 vertices covers u.
- **Case 2: u is covered by M_a, with partner x.** Put x_a = x.
  - Then N(a) = {u} ∪ S_a ∪ {x_a} and x_a ∉ N(u). Also x_a ≠ u, so x_a ∉ N[u].
  - u does not subsume a, because x_a ∈ N[a] ∖ N[u]. x_a is the only vertex of N(a) ∖ N[u], hence unique.
  - In G[N(a)] the only non-neighbour of x_a is u, so x_a is adjacent to every vertex of S_a.
  - x_a ∉ I by F2, since x_a is adjacent to a ∈ I.
  - G[S_a] = G[N(a)] − {u, x_a} = K_{d(a)−2} − (M_a ∖ {u x_a}):
    - d(a) = 5, |M_a| = 1: K3 (`5x`);
    - d(a) = 6, |M_a| = 1: K4 (`6x`);
    - d(a) = 6, |M_a| = 3: K4 minus a perfect matching = C4 (`6t`). Here a is thin.

  The cases are exhaustive and the types are distinct, so each a has exactly one type. S_a ⊆ B by F2.

(c)
- d = 7: F3 excludes `6s` and `6se` (u is a 7-vertex subsuming a 6-vertex). F4 excludes `6t`. F5 excludes
  `5s` and `5se`.
- d = 8: F5 excludes `5s` and `5se`.
- d = 9: by (a), |A| ≥ 4. If u subsumed three vertices of A, then by F6 u would be adjacent to no other
  6⁻-vertex, contradicting |A| ≥ 4. If u subsumed four or more, it would subsume more than three, contradicting
  F6. Subsumed type means subsumed by u (Case 1), so at most 2 vertices of A have subsumed type.

(d) Check the conditions one by one.
- V1 holds by (a).
- V2 holds by construction.
- V3 holds by (b), (c) and the fact that β is an isomorphism G[B] → ({0, …, k−1}, E_B).
- V4 holds by (c).
- V5 holds because x is defined to be a restricted growth string, with null exactly at the subsumed indices.

(e) ι is well defined: within a block p all x_a are equal, by the definition of π.

*Injectivity.*
- u, B and A are disjoint (u ∉ N(u); A ⊆ I, B ∩ I = ∅).
- The x-images lie outside N[u] by (b).
- Distinct blocks have distinct x-vertices, by the definition of π.

*Edges.* Every edge of H(φ) maps to an edge of G:
- u–b_j and u–a_i: B, A ⊆ N(u);
- b_p–b_q: E_B is G[B] transported;
- a_i–b_s: S_a ⊆ N(a);
- a_i–x_p and x_p–b_s: by (b).

*The closed neighbourhood of u.*
- N_H(u) = {b_j} ∪ {a_i}, and ι of this set is B ∪ A = N_G(u).
- For y, z ∈ N_H(u):
  - two b's are adjacent in H iff adjacent in G (E_B);
  - two a's are adjacent in neither (H has no a–a edge; A ⊆ I is independent by F2);
  - a_i, b_s are adjacent in H iff s ∈ S_i, iff β⁻¹(s) ∈ S_a = N(a) ∩ N(u), iff they are adjacent in G.

*The closed neighbourhood of a_i (with a = α⁻¹(i)).*
- N_H(a_i) = {u} ∪ {b_s : s ∈ S_i}, together with x_{x_i} if i is x-bearing (no other H-edge meets a_i).
- ι maps this set onto N_G(a), by (b).
- For y, z ∈ N_H(a_i):
  - u–b_s is an edge in both;
  - b_s–b_t is an edge in H iff in G (E_B);
  - u–x is an edge in neither (H has no u–x edge; x_a ∉ N(u));
  - x–b_s with s ∈ S_i is an edge in both, by (b).

(f)
- The map j ↦ β⁻¹(j), k + i ↦ α⁻¹(i) is an isomorphism from L(φ) onto G[N(u)]: G[N(u)] has the edges of
  G[B], the edges a–s for s ∈ S_a, and no A–A edges (F2).
- G[N(u)] is connected by F8, since d(u) ≤ 9. ∎

**Consequence.** Every u as in §1.3 with d(u) = d determines a configuration of L_d, and so an element of
Φ_d, whose link L(φ) is connected.

---

## 5. P2: the locality lemma L0, and certificates

### 5.1 Allowed vertex sets

For a configuration φ, the **allowed sets** are V0 = {u} ∪ {a_i : i ∈ A′} for any A′ ⊆ {0, …, m−1}
(A′ = ∅ allowed). No other V0 is allowed. In particular V0 never contains a b_j or an x_p.

### 5.2 Certificates

A **reducibility certificate** for φ is a triple (V0, S, X) such that:

- **(R0)** V0 is an allowed set.
- **(R1)** S is a set of triangles of H(φ), pairwise edge-disjoint, and X ⊆ E(H(φ)).
- **(R2)** |X| ≤ 2|S|.
- **(R3)** Every triangle of H(φ) that contains a vertex of V0 contains an edge of X.
- **(R4)** Every edge of a triangle of S whose two endpoints are both outside V0 is in X.

In other words, V0 is reducible in the graph H(φ) using S and X, in the sense of Def. 2.1.

An **exclusion certificate** for φ is the assertion that L(φ) is disconnected. It is checked directly on L(φ).

### 5.3 The locality lemma

**Lemma L0.** Let G, u and φ be as in Lemma P1, with ι as in P1(e). Let (V0, S, X) be a reducibility
certificate for φ. Then ι(V0) is reducible in G using ι(S) = {ι(T) : T ∈ S} and ι(X) = {ι(e) : e ∈ X}.

The conclusion does not depend on any part of G outside the facts listed in P1(e). In particular it does not
depend on:
- the edges among the x-vertices;
- the edges from x-vertices to B ∖ S_a;
- the degrees or neighbourhoods of the B-vertices and x-vertices outside H.

**Proof.**

(1) *ι(S) is a set of pairwise edge-disjoint triangles of G, and ι(X) ⊆ E(G).* ι maps edges of H to edges of
G (P1(e)), so ι(T) is a triangle of G for every T ∈ S, and ι(X) ⊆ E(G). ι is injective, so it is injective on
edges; edge-disjoint triangles of H therefore map to edge-disjoint triangles of G, and |ι(S)| = |S|.

(2) *Def. 2.1(i).* |ι(X)| = |X| ≤ 2|S| = 2|ι(S)|, using R2 and injectivity.

(3) *Def. 2.1(ii).*
- Let T be a triangle of G containing some w ∈ ι(V0), say w = ι(v) with v ∈ V0 ⊆ {u} ∪ {a_i}.
- Write T = {w, y′, z′}. Then y′, z′ ∈ N_G(w) = ι(N_H(v)) by P1(e). So y′ = ι(y) and z′ = ι(z) with
  y, z ∈ N_H(v).
- y′z′ ∈ E(G), so yz ∈ E(H) by P1(e). Hence {v, y, z} is a triangle of H containing v ∈ V0.
- By R3 it contains an edge e ∈ X. Then ι(e) ∈ ι(X) is an edge of T.
- So G − ι(X) has no triangle containing a vertex of ι(V0).

(4) *Def. 2.1(iii).*
- Let e′ be an edge of a triangle ι(T), T ∈ S, with both endpoints outside ι(V0).
- Then e′ = ι(e) for an edge e of T. Since ι is injective, both endpoints of e lie outside V0.
- By R4, e ∈ X, so e′ ∈ ι(X).

(5) ι(V0) ∋ u is nonempty. So ι(V0) is reducible in G. ∎

### 5.4 The theorem a complete certificate file gives

**Corollary (degree-d closure).** Suppose every orbit of Φ_d has a representative φ that carries a valid
reducibility certificate or a valid exclusion certificate. Then no vertex u as in §1.3 has d(u) = d.

**Proof.**
- Suppose such a u exists. By P1 it gives φ_G ∈ L_d. Some listed representative φ is Γ-equivalent to φ_G.
- Γ-equivalence corresponds to relabelling B and A (choosing other β, α), and P1(d) holds for every choice of
  bijections. So φ itself arises from G by P1, with suitable β and α.
- φ cannot carry an exclusion certificate, because L(φ) ≅ G[N(u)] is connected (P1(f)).
- So φ carries a reducibility certificate. By L0, G has a reducible vertex set, contradicting F0. ∎

**Status of a failure.** If some orbit has no valid certificate, the corollary fails for d. That configuration
is reported as "no reduction found by the methods of SPEC.md". It is not reported as irreducible.

---

## 6. Certificate file format (JSON)

The file for degree d is a single JSON object:

```
{
  "format": "B2-SPEC-v1",
  "d": 7 | 8 | 9,
  "n_configs": <int, number of entries>,
  "labelled_total": <int, the author's value of |L_d|>,
  "configs": [ <entry>, ... ]
}
```

Each **entry** has this form:

```
{
  "config": {
    "k": <int>, "m": <int>,
    "B_edges": [[p, q], ...],        // 0 <= p < q < k, no repeats
    "A": [{"type": "<5x|6x|6t|5s|5se|6s|6se>", "S": [s0, s1, ...]}, ...],   // length m; S strictly increasing
    "x": [<int or null>, ...]        // length m; condition V5
  },
  "stabiliser_order": <int, the author's |Stab_Gamma(phi)|>,
  "certificate": <certificate>
}
```

A **certificate** is one of:

- `{"kind": "reducible", "V0": [<names>], "S": [[n1, n2, n3], ...], "X": [[n1, n2], ...]}`
  - Names are the vertex names of H(φ) from §3.2: `"u"`, `"b<j>"`, `"a<i>"`, `"x<p>"`.
  - V0 must contain `"u"`. Order within a triangle or edge is irrelevant.
  - It must satisfy R0–R4. A checker must recompute the triangle set of H(φ) itself.
- `{"kind": "excluded_disconnected_link"}`: valid iff L(φ) is disconnected.
- `{"kind": "uncovered"}`: no certificate found. The entry counts as **not covered**.

**Extra fields.** A file may contain extra fields; checkers ignore them. `stabiliser_order` and
`labelled_total` are the author's claims. A checker recomputes them and must reject the file if they differ.

**Checks a checker must make on each entry:**
- V1–V5 for the stated d;
- validity of the certificate as above.

The file **certifies degree d** iff every entry is valid, every certificate is `reducible` or a valid
`excluded_disconnected_link`, and the completeness checks of §7 pass.

---

## 7. Completeness

This section is frozen with SPEC.md. Stage 3 is judged by it and may not replace or extend it.

**Requirement.** Let F be a certificate file for degree d ∈ {7, 8, 9}. F is **complete** when every orbit of
Φ_d (§3.3) is represented by at least one entry of F.

The checker uses only §§2–3 of this SPEC and its own code. It does not use any author code or any author list.

### 7.1 Checks (identical for d = 7, 8 and 9)

- **K1 (membership).** Every entry of F satisfies V1–V5 for d.
- **K2 (distinct orbits).** No two entries of F lie in the same Γ-orbit.
  - The checker computes, for each entry, its own Γ-invariant canonical form. Example: the lexicographic
    minimum of an encoding of (E_B, (τ_i, S_i)_i, x) over all |Γ_{k,m}| = k!·m! group elements, applying the
    action of §3.3 exactly, including renormalising x to a restricted growth string.
  - It checks that all canonical forms are pairwise distinct.
- **K3 (orbit sum).**
  - The checker computes |Stab(φ)| for each entry by brute force over Γ_{k,m}: the number of group elements
    that map the entry to itself.
  - It then checks that Σ_{entries} k!·m!/|Stab(φ)| equals |L_d|, the total below, computed by the checker
    itself.
  - It also checks each entry's `stabiliser_order`, and `labelled_total` against its own values.
- **Independent total |L_d|.**
  - For k ∈ {4, 5} with m = d − k, iterate over all 2^{C(k,2)} labelled graphs E_B on {0, …, k−1}.
  - For each one, let:
    - X(E_B) = the number of pairs (τ, S) with τ an x-bearing type in T_d and S satisfying V3 for τ;
    - Y(E_B) = the same count for the subsumed types in T_d.
  - Then |L_d| = Σ_{k} Σ_{E_B} Σ_{j} C(m, j) · X(E_B)^j · Y(E_B)^{m−j} · Bell(j). The inner sum runs over
    j = 0..m, with the restriction m − j ≤ 2 when d = 9 and no restriction when d = 7 or 8.
  - Bell(j) is the number of set partitions of a j-set: Bell(0..5) = 1, 1, 2, 5, 15, 52.
  - *Justification:*
    - choose which j of the m indices are x-bearing (C(m, j));
    - choose their (type, S) (X^j) and the others' (Y^{m−j});
    - choose the partition of the x-bearing indices (Bell(j)), which V5 encodes uniquely as a restricted growth
      string.
  - For d = 7, T_7 has no subsumed type, so Y = 0 and only the j = m term contributes: Y^0 = 1, and
    Y^{m−j} = 0 for j < m.
- **K4 (cross-check, optional).** The number of entries equals the number of Γ-orbits of L_d. The checker
  computes that number independently, for example by Burnside's lemma, or (for d = 7, where |L_7| = 10305) by
  enumerating all of L_7 and mapping each labelled configuration to its canonical form. The author's values
  are 174, 738 and 5390.

### 7.2 Why K1–K3 prove completeness

- By K1 each entry's orbit is a subset of L_d.
- By K2 these orbits are pairwise disjoint.
- By orbit–stabiliser each orbit has size k!·m!/|Stab|.
- By K3 their total size is |L_d|.
- So the orbits of the entries are disjoint subsets of the finite set L_d whose sizes sum to |L_d|. Their union
  is therefore L_d, and every orbit of Φ_d is represented.

This argument uses only the definition of L_d and Γ, and quantities the checker computes. It applies verbatim
to d = 7, 8 and 9.

### 7.3 Feasibility for each d

- The largest group is |Γ| = 4!·5! = 5!·4! = 2880 (d = 9). For d = 8 it is 576 or 720, and for d = 7 it is 144
  or 240.
- K2 and K3 cost at most |F| · |Γ| encodings: at most 5390 · 2880 ≈ 1.6 × 10⁷ for d = 9.
- The total |L_d| needs 2^{10} + 2^6 graphs per d.
- Both are feasible in minutes in Python. No step depends on the author's generator.

### 7.4 Coverage in the certificate sense

Degree d is **closed** iff the following all hold:
- F passes K1–K3;
- every entry carries a valid `reducible` or valid `excluded_disconnected_link` certificate;
- no entry is `uncovered`.

Then the corollary of §5.4 applies. An `uncovered` entry, or an entry whose certificate fails, leaves degree d
open, with that configuration reported as "no reduction found by the methods of SPEC.md".

---

## 8. Scope statement

- This SPEC defines Φ_7, Φ_8 and Φ_9 and the methods (allowed V0, certificate kinds) for all three degrees.
- Stage 3 uses them unchanged.
- The author knows of no reason why Φ_8 or Φ_9 would be wrong. Their exact sizes (738 and 5390 orbits) are far
  below the limit of stop rule S3.
- Whether every configuration of Φ_8 and Φ_9 has a certificate is unknown. That is the content of Stage 3.
