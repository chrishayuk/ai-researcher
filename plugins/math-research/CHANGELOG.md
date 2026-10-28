# Changelog

## 0.2.0 (2026-10-28)

Fixes from a review of the whole engine. Each is covered by `tests/test_safety.py`.

- **Budget:** an agent that crashes or is killed without reporting its cost is charged its whole grant, so the
  dollar cap holds across crashes and retries. Each launch records its grant.
- **Audit:** verdict and claims files count only while an ACCEPTED receipt binds their current bytes; a failed
  review's verdicts are ignored and flagged. Refutations are read leniently ("ERROR FOUND: off by one",
  "fail") and credit strictly (exact strings only). A claim id used twice earns Unverified for every copy.
- **Receipts:** an empty input directory (such as a proof-only `certs/`) is bound, not treated as missing.
- **Pause hook:** newlines, substitutions and redirections to anything but checkpoint files are refused while
  paused, and `mv` arguments are checked.
- **Blind check:** the hook refuses the checker's direct reads of the author's `src/`, `NOTES.md`, `RESULT.md`,
  the archive, run records, ledgers and session transcripts, and searches that would reach them. Auto memory is
  off for every agent.
- **Gate:** `stage.py gate` takes `--claims` and fails when any claim has no verdict.
- **Runner:** `.DS_Store` and `__pycache__` no longer count as input changes; the runner lock is atomic; time
  that passes while agents run without a runner is charged when it comes back, and `status` warns meanwhile.

## 0.1.0 (2026-10-28)

The Video 2 companion project packaged as a Claude Code plugin.
