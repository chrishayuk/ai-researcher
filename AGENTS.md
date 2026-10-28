# Instructions for coding agents

This repository is a Claude Code plugin marketplace. Its `math-research` plugin runs autonomous mathematical
research campaigns. When the user asks you to investigate a mathematical question, or to run, monitor, pause,
resume or audit a campaign, follow `plugins/math-research/skills/campaign/SKILL.md`, and run its commands as
`plugins/math-research/bin/math-research` if `math-research` is not on your PATH.

Never edit files inside an existing `campaigns/<name>/` directory by hand: they are frozen by hash.
