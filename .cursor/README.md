# Cursor configuration

This directory holds everything Cursor loads for **OmniCursor**: AI behavior rules, lifecycle hooks, and agent routing configs.

| Subfolder | Purpose |
|-----------|---------|
| [`rules/`](./rules/) | `.mdc` rules — always-on guardrails + activatable methodology (buckets 1–3). |
| [`hooks/`](./hooks/) | Python **stdlib-only** scripts wired by [`hooks.json`](./hooks.json). |
| [`agents/`](./agents/) | JSON agent definitions merged with base categories in `src/omnicursor/agents.py`. |

**Also here:** [`hooks.json`](./hooks.json) — maps Cursor lifecycle events (`beforeSubmitPrompt`, `beforeShellExecution`, etc.) to hook scripts.

**Docs:** [Root README](../README.md), [Quickstart](../docs/QUICKSTART.md), [cursor.md](../cursor.md) (commands and constraints).
