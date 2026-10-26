import json, sys, itertools, math
import networkx as nx
from itertools import combinations, permutations, product

# type -> (x-bearing, |S|, edges in G[B][S], degree-seq test)
TYPES = {
 '5x': (True, 3, 'K3'), '6x': (True, 4, 'K4'), '6t': (True, 4, 'C4'),
 '5s': (False, 4, 'K4'), '5se': (False, 4, 'K4-e'), '6s': (False, 5, 'K5'), '6se': (False, 5, 'K5-e')}
T7 = ['5x', '6x']

def induced_ok(kind, S, EB):
    sub = [e for e in EB if e[0] in S and e[1] in S]
    n = len(S); ne = len(sub)
    want = {'K3': (3, 3), 'K4': (4, 6), 'C4': (4, 4), 'K4-e': (4, 5), 'K5': (5, 10), 'K5-e': (5, 9)}[kind]
    if (n, ne) != want: return False
    if kind == 'C4':
        deg = {s: 0 for s in S}
        for p, q in sub: deg[p] += 1; deg[q] += 1
        return all(v == 2 for v in deg.values())
    return True

def rgs(parts):
    """normalise labels (None kept) to restricted growth string"""
    mp = {}; out = []
    for v in parts:
        if v is None: out.append(None); continue
        if v not in mp: mp[v] = len(mp)
        out.append(mp[v])
    return out

def valid_x(x, types):
    seen = -1
    for xi, t in zip(x, types):
        if TYPES[t][0]:
            if xi is None or not isinstance(xi, int) or xi < 0 or xi > seen + 1: return False
            seen = max(seen, xi)
        else:
            if xi is not None: return False
    return True

def check_V(cfg, d):
    k, m = cfg['k'], cfg['m']
    if k not in (4, 5) or m != d - k: return 'V1'
    EB = [tuple(e) for e in cfg['B_edges']]
    if len(set(EB)) != len(EB) or any(not (0 <= p < q < k) for p, q in EB): return 'V2'
    A = cfg['A']
    if len(A) != m or len(cfg['x']) != m: return 'len'
    allowed = {7: T7, 8: ['5x','6x','6t','6s','6se'], 9: list(TYPES)}[d]
    for a in A:
        if a['type'] not in allowed: return 'V3type'
        S = a['S']
        if any(S[i] >= S[i+1] for i in range(len(S)-1)) or any(not (0 <= s < k) for s in S): return 'V3S'
        if len(S) != TYPES[a['type']][1] or not induced_ok(TYPES[a['type']][2], S, EB): return 'V3graph'
    if d == 9 and sum(1 for a in A if not TYPES[a['type']][0]) > 2: return 'V4'
    if not valid_x(cfg['x'], [a['type'] for a in A]): return 'V5'
    return None

def encode(k, m, EB, tS, x):
    return (k, m, tuple(sorted(EB)), tuple(tS), tuple(x))

def act(cfg, sigma, rho):
    k, m = cfg['k'], cfg['m']
    EB = [tuple(sorted((sigma[p], sigma[q]))) for p, q in cfg['B_edges']]
    tS = [None]*m; xs = [None]*m
    for i, a in enumerate(cfg['A']):
        tS[rho[i]] = (a['type'], tuple(sorted(sigma[s] for s in a['S'])))
        xs[rho[i]] = cfg['x'][i]
    return encode(k, m, EB, tS, rgs(xs))

def group(k, m):
    return [(s, r) for s in permutations(range(k)) for r in permutations(range(m))]

def canon_and_stab(cfg):
    G = group(cfg['k'], cfg['m'])
    base = act(cfg, tuple(range(cfg['k'])), tuple(range(cfg['m'])))
    best = None; stab = 0
    for s, r in G:
        e = act(cfg, s, r)
        if best is None or e < best: best = e
        if e == base: stab += 1
    return best, stab, len(G)

# ---------- own enumeration of L_d (d=7) ----------
def all_graphs(k):
    pairs = list(combinations(range(k), 2))
    for mask in range(1 << len(pairs)):
        yield [pairs[i] for i in range(len(pairs)) if mask >> i & 1]

def set_partitions_rgs(j):
    def rec(pref, mx):
        if len(pref) == j: yield list(pref); return
        for v in range(mx + 2):
            yield from rec(pref + [v], max(mx, v))
    yield from rec([], -1)

def enum_L(d):
    assert d == 7
    out = []
    for k in (4, 5):
        m = d - k
        for EB in all_graphs(k):
            opts = []
            for t in T7:
                for S in combinations(range(k), TYPES[t][1]):
                    if induced_ok(TYPES[t][2], S, EB): opts.append((t, S))
            for combo in product(opts, repeat=m):
                for x in set_partitions_rgs(m):
                    cfg = {'k': k, 'm': m, 'B_edges': [list(e) for e in EB],
                           'A': [{'type': t, 'S': list(S)} for t, S in combo], 'x': x}
                    out.append(cfg)
    return out

# ---------- H(phi), triangles, certificate check ----------
def build_H(cfg):
    k, m = cfg['k'], cfg['m']
    E = set()
    def add(a, b): E.add(frozenset((a, b)))
    for j in range(k): add('u', f'b{j}')
    for p, q in cfg['B_edges']: add(f'b{p}', f'b{q}')
    for i, a in enumerate(cfg['A']):
        add('u', f'a{i}')
        for s in a['S']: add(f'a{i}', f'b{s}')
        if cfg['x'][i] is not None:
            p = cfg['x'][i]
            add(f'a{i}', f'x{p}')
            for s in a['S']: add(f'x{p}', f'b{s}')
    return E

def triangles(E):
    V = set().union(*E)
    adj = {v: set() for v in V}
    for e in E:
        a, b = tuple(e); adj[a].add(b); adj[b].add(a)
    return {frozenset(t) for t in combinations(sorted(V), 3)
            if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]}

def link_connected(cfg):
    k, m = cfg['k'], cfg['m']
    g = nx.Graph(); g.add_nodes_from(range(k + m))
    g.add_edges_from(map(tuple, cfg['B_edges']))
    for i, a in enumerate(cfg['A']):
        for s in a['S']: g.add_edge(s, k + i)
    return nx.is_connected(g)

def check_cert(cfg, cert):
    kind = cert.get('kind')
    if kind == 'excluded_disconnected_link':
        return None if not link_connected(cfg) else 'link connected'
    if kind != 'reducible': return f'kind {kind}'
    E = build_H(cfg); V = set().union(*E)
    V0 = set(cert['V0'])
    if 'u' not in V0: return 'R0 no u'
    allowed = {'u'} | {f'a{i}' for i in range(cfg['m'])}
    if not V0 <= allowed: return 'R0'
    Sx = [frozenset(t) for t in cert['S']]
    X = [frozenset(e) for e in cert['X']]
    if len(set(X)) != len(X): return 'X repeats'
    T = triangles(E)
    if any(t not in T for t in Sx): return 'R1 S not triangle'
    if len(set(Sx)) != len(Sx): return 'R1 S repeats'
    used = set()
    for t in Sx:
        for e in map(frozenset, combinations(t, 2)):
            if e in used: return 'R1 not edge-disjoint'
            used.add(e)
    if any(e not in E for e in X): return 'R1 X not edges'
    Xs = set(X)
    if len(Xs) > 2 * len(Sx): return 'R2'
    for t in T:
        if t & V0 and not any(frozenset(e) in Xs for e in combinations(t, 2)): return 'R3'
    for e in used:
        if not (e & V0) and e not in Xs: return 'R4'
    return None

def check_file(F, d=7, verbose=False):
    errs = []
    if F.get('d') != d or F.get('format') != 'B2-SPEC-v1': errs.append('header')
    seen = {}; tot = 0
    for idx, ent in enumerate(F['configs']):
        cfg = ent['config']
        r = check_V(cfg, d)
        if r: errs.append((idx, 'K1', r)); continue
        c, st, gs = canon_and_stab(cfg)
        if c in seen: errs.append((idx, 'K2 dup', seen[c]))
        seen[c] = idx
        if st != ent['stabiliser_order']: errs.append((idx, 'stab', st, ent['stabiliser_order']))
        tot += gs // st
        cert = ent['certificate']
        r = check_cert(cfg, cert)
        if r: errs.append((idx, 'cert', r))
    Ltot = 0
    # independent total by formula
    from math import comb
    bell = [1,1,2,5,15,52]
    for k in (4,5):
        m = d-k
        for EB in all_graphs(k):
            X = sum(1 for t in T7 for S in combinations(range(k), TYPES[t][1]) if induced_ok(TYPES[t][2], S, EB))
            Ltot += X**m * bell[m]
    if tot != Ltot: errs.append(('K3 orbit sum', tot, Ltot))
    if F.get('labelled_total') != Ltot: errs.append(('labelled_total', F.get('labelled_total'), Ltot))
    if F.get('n_configs') != len(F['configs']): errs.append('n_configs')
    return errs, tot, Ltot
