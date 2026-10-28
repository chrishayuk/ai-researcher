import json, sys, copy, random
sys.path.insert(0, 'ws/B2/s1/check')
from chk import *
F = json.load(open('ws/B2/s1/certs/phi7.json'))
L = enum_L(7)
print('my |L_7| =', len(L))
mine = {}
for c in L:
    cn, st, gs = canon_and_stab(c)
    mine.setdefault(cn, []).append(c)
print('my orbits =', len(mine), ' sizes by k:', {k: sum(1 for cn in mine if cn[0]==k) for k in (4,5)})
fcan = {}
for i, e in enumerate(F['configs']):
    cn, st, gs = canon_and_stab(e['config'])
    fcan.setdefault(cn, []).append(i)
missing = set(mine) - set(fcan); extra = set(fcan) - set(mine)
dups = {k: v for k, v in fcan.items() if len(v) > 1}
print('missing', len(missing), 'extra', len(extra), 'dups', len(dups))
from collections import Counter
print('cert kinds', Counter(e['certificate']['kind'] for e in F['configs']))
print('V0 sizes', Counter(len(e['certificate'].get('V0', [])) for e in F['configs']))
errs, tot, Lt = check_file(F)
print('errors', errs[:10], 'orbit sum', tot, 'formula |L|', Lt)
# burnside check of orbit count
