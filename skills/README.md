# Markdown skills

Each file is human-readable skill content loaded by the MCP tool **`invoke_skill`** via `src/omnicursor/skills.py`. Names here match tool arguments (e.g. `brainstorming`, `plan-ticket`).

**Compliance:** `check_compliance` uses `src/omnicursor/compliance.py` — add registry entries when you add skills that need automated checks.

**Buckets:** Methodology skills are Bucket 1/2; `adapter-stub` documents Bucket 3 dry-run behavior. See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).

**Reference:** [OMNICLAUDE_SKILLS.md](../OMNICLAUDE_SKILLS.md) (read-only comparison to upstream omniclaude skills).
