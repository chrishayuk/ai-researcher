# ai-researcher

A Claude Code plugin marketplace for autonomous AI research.

```bash
claude plugin marketplace add chrishayuk/ai-researcher     # or: claude plugin marketplace add ./ai-researcher
claude plugin install math-research@ai-researcher
```

| Plugin | What it does |
|---|---|
| [`math-research`](plugins/math-research/) | Autonomous mathematical research campaigns: scope and freeze a question, run research, blind check and adversarial review as budgeted headless agents, then audit the evidence |

## Developing

Load a plugin straight from its folder, without installing it:

```bash
claude --plugin-dir ./plugins/math-research
```

Run `claude plugin validate .` after every change to a manifest. A new plugin goes in `plugins/<name>/` with
its own `.claude-plugin/plugin.json`, plus an entry in `.claude-plugin/marketplace.json` whose `name` matches it.

## Licence

Apache License 2.0. See `LICENSE`.
