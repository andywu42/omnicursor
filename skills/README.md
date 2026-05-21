# Skills have moved

Skills are now at `.cursor/skills/<name>/SKILL.md` (Cursor-native format).
Canonical skill ids are **`onex-<name>`** (same as the directory name `<name>`).

Each skill is a directory containing a `SKILL.md` with YAML frontmatter
(`name:`, `description:`) followed by the skill instructions. Cursor
discovers them natively in its skill picker.

See `cursor-plugin.json` for the full plugin surface map.
