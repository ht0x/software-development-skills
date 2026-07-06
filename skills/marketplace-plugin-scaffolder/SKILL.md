---
name: marketplace-plugin-scaffolder
description: >
  Triggered only by the slash command /marketplace-plugin-scaffolder. Scaffolds
  a new Claude Code or Cowork marketplace plugin project from an existing set
  of skills. It builds the standard `.claude-plugin/` + `skills/` project
  layout and, once the files are ready, asks whether to also create and push a
  GitHub repository for it. Not for editing an already packaged `.plugin`
  file, and not for building a single SKILL.md from scratch with no
  plugin-level packaging involved.
metadata:
  version: "0.1.0"
  category: plugin-tooling
disable-model-invocation: true
---

# Marketplace Plugin Scaffolder

Build a standard marketplace-plugin project structure around a set of skills, then offer to publish it as a new GitHub repository. This mirrors the two-part workflow: scaffold first, confirm contents, then optionally create the repo — never push anything without explicit confirmation.

## Why this structure

Claude Code and Cowork discover plugins through a marketplace. A marketplace is just a git repo with a `.claude-plugin/marketplace.json` at its root, listing one or more plugins. Each plugin needs its own `.claude-plugin/plugin.json` plus a `skills/` directory. Keeping every plugin repo shaped the same way (as in `software-development-skills` and `code-quality-skills`) means `/plugin marketplace add <owner>/<repo>` works predictably and users can read any plugin repo the same way.

## Standard project structure

```
<plugin-repo-name>/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
├── README.md
└── LICENSE
```

Optional additions, only if the plugin actually needs them (don't add speculatively):
- `.mcp.json` at the repo root — declares MCP servers the plugin wires up (see `references/mcp-servers.md` if this skill has it bundled, otherwise ask the user for exact server URLs rather than guessing).
- `commands/` — legacy single-file command format; prefer `skills/*/SKILL.md` for anything new.
- `agents/`, `hooks/hooks.json` — only when the user explicitly wants subagents or lifecycle hooks bundled with the plugin.

## Workflow

### Step 1 — Ask where the source skills folder is located

Always ask the user directly where the skills live, via AskUserQuestion — don't guess a path or silently search the filesystem for candidates first. Something like: "Where is the skills folder for this plugin located?" with options covering the common cases:
- A specific existing folder the user names or has already referenced in the conversation (e.g., `team90/<something>/skills/`).
- Skills that were just discussed/drafted earlier in this conversation, not yet saved anywhere.
- No existing skills yet — scaffold an empty placeholder skill folder to fill in later.

Once you have the path, read each source `SKILL.md` fully before copying it. Don't paraphrase or "clean up" the skill content unless the user asks — copy it verbatim into the new structure so behavior doesn't silently change.

### Step 2 — Ask what connectors to add

Ask the user directly, via AskUserQuestion, whether this plugin should wire up any MCP connectors (e.g., GitHub, Notion, Context7, Slack, or anything else) — leave it open-ended rather than presenting a fixed menu, since needs vary per plugin. Don't assume "no connectors" by default and don't infer connectors from the skill content; always ask.

- If the user names one or more connectors, look up (or ask the user for) each connector's exact MCP endpoint — type (`http`/`sse`/`stdio`) and URL, or command for local/stdio servers. Don't invent a URL if you're not sure of it; check existing `.mcp.json` files in sibling/reference repos first (e.g., other plugins the user owns), and ask the user to confirm or supply the exact endpoint if it's not already known.
- Declare them in a `.mcp.json` file at the plugin root only — see the schema in Step 3. Do not modify any skill's `allowed-tools` frontmatter for this; connectors are made available at the plugin level, not wired into individual skills' tool lists.
- If the user says no connectors, skip `.mcp.json` entirely — don't create an empty or placeholder one.

### Step 3 — Collect plugin identity via AskUserQuestion

Never invent these silently — always confirm with the user, the same way this skill's own creation was confirmed. Ask (batched into one AskUserQuestion call where reasonable):

1. **Plugin/repo name** — used as both the marketplace name and the plugin entry name (e.g., `code-quality-skills`). Recommend matching the GitHub repo name exactly, since mismatches make `/plugin install` confusing.
2. **Description** — one or two sentences. Offer to draft one from the skill set and let the user approve or edit it, rather than asking them to write it from a blank prompt.
3. **Author/owner info** — name, and GitHub URL if publishing. Check whether the user already has a pattern in another plugin repo they own (look for `.claude-plugin/plugin.json` in any sibling/reference repos) and offer that as the recommended default.
4. **Version and license** — default to `0.1.0` for a first release. For license, ask whether to match whatever convention their existing skills already declare (check each `SKILL.md` frontmatter for a `license:` field) — don't default to MIT if the skills already say CC0-1.0 or similar, since a mismatched top-level LICENSE vs. per-skill license is confusing.

Draft the exact JSON for `marketplace.json` and `plugin.json` and show it to the user before writing any files. This is a cheap, fast confirmation step — do it even if the user seems in a hurry, because plugin metadata is annoying to fix after a repo is public.

### Step 4 — Scaffold the files locally

Build the full structure in a scratch/output directory first (never write directly into a location that can't be iterated on). Use this exact shape for the two JSON files:

**`.claude-plugin/marketplace.json`**
```json
{
  "name": "<plugin-name>",
  "owner": { "name": "<owner>", "url": "<owner-url>" },
  "description": "<description>",
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./",
      "description": "<description>",
      "author": { "name": "<owner>" },
      "category": "<category>",
      "keywords": ["<kw1>", "<kw2>"]
    }
  ]
}
```

**`.claude-plugin/plugin.json`**
```json
{
  "name": "<plugin-name>",
  "version": "<version>",
  "description": "<description>",
  "author": { "name": "<owner>", "url": "<owner-url>" },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "https://github.com/<owner>/<repo>",
  "license": "<license>",
  "keywords": ["<kw1>", "<kw2>"]
}
```

If connectors were requested in Step 2, also write `.mcp.json` at the plugin root:

```json
{
  "mcpServers": {
    "<connector-name>": {
      "type": "http",
      "url": "<connector-mcp-endpoint>"
    }
  }
}
```

Use `"type": "sse"` or a `command`/`args`/`env` stdio block instead of `http`/`url` if that's what the connector requires — confirm the right shape with the user rather than guessing.

Then:
- Copy each skill folder into `skills/<skill-name>/SKILL.md` unchanged.
- Write a `README.md` with: a one-paragraph description, a table of skills (name, trigger/command, purpose — pull this straight from each `SKILL.md` frontmatter `description`), a usage section, and an installation section showing both `/plugin marketplace add <owner>/<repo>` and standalone `cp -r skills/<name> ~/.claude/skills/` paths (see `references/readme-template.md` for the full template if bundled; otherwise follow the shape used in `software-development-skills`' and `code-quality-skills`' READMEs). If `.mcp.json` was created, mention the connectors it wires up in a short "Connectors" section.
- Write a `LICENSE` file matching the chosen license (MIT or CC0-1.0 are the two seen in practice so far; ask if the user wants a different one).

Show the user the final file tree, the two JSON files, and (if present) `.mcp.json` one more time before touching GitHub. Treat this as a hard gate, not a formality — do not proceed to Step 5 without an explicit yes.

### Step 5 — Ask about creating a GitHub repo

Once the local structure is confirmed, ask directly: does the user want to create a new GitHub repository for this plugin project, following the same process as any other "set up a new github repo" request (repo name, visibility, then push)? Use AskUserQuestion with clear options (e.g., "Yes, create public repo" / "Yes, create private repo" / "Not now, just leave the files locally").

If yes:
1. Check the repo name isn't already taken (search for `repo:<owner>/<name>` — a 404/validation-failed search result means it's available).
2. Create the repo (confirm public vs. private explicitly — don't default silently to one or the other).
3. If the repo creation tool supports `autoInit`, be aware that `autoInit: true` creates an empty placeholder file (e.g., `README.md` with 0 bytes) that a subsequent bulk-file push may collide with. Prefer `autoInit: false` and push all files as the very first commit — but if the bulk-push tool fails with "repository is empty," fall back to creating one file first via a single-file write, then bulk-push the rest.
4. Push every scaffolded file in as few commits as practical (ideally one).
5. Verify by listing the repo's root and `skills/` contents back and confirming the tree matches what was scaffolded locally.

If no: tell the user where the local files live and stop — don't create a repo "just in case."

## Things that have gone wrong before — watch for these

- **Always ask about connectors explicitly (Step 2) — never assume none, never infer some.** Don't skip the question just because the source skills don't obviously need external tools, and don't add a connector because it seems plausible. If the user changes their mind after `.mcp.json` is already scaffolded, cleanly drop it rather than leaving half-applied files — a `.mcp.json` in a write-protected scratch location may not be deletable via shell; in that case just exclude it from the GitHub push rather than fighting the filesystem.
- **Connectors go in `.mcp.json` only, not into individual skills' `allowed-tools`.** Keep the two concerns separate unless the user explicitly asks to scope a connector to specific skills.
- **Match the plugin's own license, not a generic default.** If every `SKILL.md` in the source folder declares `license: CC0-1.0` in its frontmatter, the top-level `LICENSE` file and `plugin.json`'s `license` field should match — don't default to MIT out of habit.
- **plugin.json name vs. repo name.** Keep them identical unless the user explicitly wants them to differ; mismatches make the install command (`/plugin install <plugin-name>@<marketplace-name>`) confusing to write correctly.
- **Empty-repo push order.** Some GitHub push tools fail with "repository is empty" on the very first bulk push. Push one small file first (or accept an `autoInit` placeholder), then bulk-push the rest.

## Output

By the end of this workflow, the user should have either:
- A confirmed local plugin project folder (structure + content approved), or
- The same folder plus a live GitHub repo with the full structure pushed and verified.

State clearly which of the two happened, and give the repo URL if one was created.
