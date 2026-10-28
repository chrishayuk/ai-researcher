# Verify a real Tuza result yourself

This folder holds the independent checker that a blind Sonnet agent wrote during TUZA-002 (B0 Round 2,
Stage 1). The checker re-enumerates the degree-7 case and validates every one of its certificates. Alongside it
are the certificates the research agent produced. Run it:

```bash
cd examples/tuza-case-study/verify
python3 -I ws/B2/s1/check/run.py
```

You need Python 3.10 or later and `networkx` (`pip install networkx`). It takes about 6 seconds.

**Expected output (abridged):**

```
my |L_7| = 10305
my orbits = 174  sizes by k: {4: 38, 5: 136}
missing 0 extra 0 dups 0
cert kinds Counter({'reducible': 153, 'excluded_disconnected_link': 21})
errors [] orbit sum 10305 formula |L| 10305
```

**What it shows.** The checker generates every configuration of the degree-7 case itself, 10,305 of them, from
the specification. It finds that they fall into 174 symmetry classes, and that the certificate file covers each
class exactly once. It then checks each certificate:
- 153 classes carry a reduction certificate, each validated against the stated conditions;
- 21 classes are excluded because their link is disconnected. That exclusion rests on a cited published result
  (Puleo's robustness, F8), not on a certificate.

**What it does not show.** This is the finite part of one case (degree 7). The whole argument also needs:
- the structure and locality lemmas;
- the degree-8 and degree-9 classifications;
- Lemma W, for degrees 10 and above.

These are in `../round2/`. The overall result is an internally reviewed proof candidate. It is not an
established theorem, and its novelty is unconfirmed.

**Provenance.** These files are byte-identical copies from the frozen TUZA-002 record. Their SHA-256 hashes
appear in that record's `round2-snapshot/ROUND2.sha256`:

| File | SHA-256 |
|---|---|
| `ws/B2/s1/check/chk.py` | `dd32e81f801a080b58ef8080f7020db43431d643e0d28c303c9c05d13352cb95` |
| `ws/B2/s1/check/run.py` | `73aaefa61b16e4a052d7adf9761ff424cfab40291ac1a3ff3d56865c8ad49046` |
| `ws/B2/s1/certs/phi7.json` | `63d5bd005a2527f95c04f59d86b0f9bcc5187a0fa694370cc36076a1148cd77d` |
| `ws/B2/s1/certs/SHA256SUMS` | `eaba6e04f8f9a7bbc816d5e871b41af99686effa3ae7d69f1d57ffb4655b1256` |

The specification it checks against is `../round2/SPEC.md`.
