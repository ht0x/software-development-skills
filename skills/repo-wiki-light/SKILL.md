---
name: repo-wiki-light
description: Triggered ONLY by the slash command /repo-wiki-light. Do not invoke this skill based on natural-language requests to "document this codebase," "write onboarding docs," or similar phrasing — wait for the explicit /repo-wiki-light command. Once triggered, generates or incrementally updates an architecture wiki for any code repository — a README, architecture.md, data-flow.md, decisions.md, and one page per top-level module/feature. Works on any language or framework, tracking the last-generated commit in .wiki-state.json so re-runs only touch what changed.
---

# Repo Wiki Light

Triggered only by the explicit `/repo-wiki-light` command — not by general requests to document or explain a codebase. If the user asks something like "can you document this repo" or "write onboarding docs" without using the slash command, answer normally or suggest they run `/repo-wiki-light` rather than invoking this workflow.

Generate and maintain a living architecture wiki for a code repository: a short set of Markdown pages that explain how the codebase is organized, how data flows through it, why key decisions were made, and what each module does. The wiki tracks the commit it was last generated against, so later runs only touch what actually changed instead of rewriting everything.

This skill is deliberately general — it works on a Rails app, a Unity game, a Python data pipeline, a monorepo with 30 packages, or a five-file script collection. It infers structure from what's actually in the repo rather than assuming any particular stack.

## Why the confirmation step matters

Two decisions in this workflow are expensive to get wrong after the fact: where the wiki lives, and which modules get their own page. Writing 30 files in the wrong place, or splitting a repo's modules in a way the user disagrees with, wastes their time reviewing and fixing it. Both of these are cheap to check up front and expensive to redo, so always confirm them before writing anything.

## Step 1: Determine scope

Ask (or infer from context) where the wiki should live if this is a first run — a reasonable default is `docs/wiki/` at the repo root, but let the user override it. Look for a `.wiki-state.json` file at that location (or wherever the user points you).

- **State file exists:** read `last_generated_commit`. Run `git diff --name-only <last-hash> HEAD` to see what changed since the last generation. This is an incremental update — only the modules touched by that diff (plus anything that imports/depends on them) need re-analysis.
- **No state file:** this is a full first-time generation. Read the whole repo.

## Step 2: Discover modules — then confirm before writing anything

Read the repo structure, entry points, package/module boundaries, and key dependencies (package.json workspaces, a `src/` tree, a monorepo's `packages/*`, Unity's `Assets/` folders, whatever the actual project uses).

Map wiki pages to the repo's real top-level modules or features, one page per module, with **no fixed cap**. A small repo might warrant 5 pages; a large one with 30 distinct features warrants roughly 30. Forcing a large repo into an arbitrary "5-10 pages" box means either cramming unrelated features onto one page (hard to navigate) or leaving major features undocumented — neither serves the user. Let the actual module count in the codebase drive the page count.

Before writing any files, present the proposed module list (and the output path from Step 1) to the user and get their sign-off. They may want to merge two closely related modules onto one page, split a module you grouped too coarsely, exclude something (e.g. vendored/generated code, a deprecated module), or rename pages to match team vocabulary. This is the point where their domain knowledge is cheapest to incorporate — after 30 files are written, the same fix means re-reading and re-editing all of them.

For an incremental update, you don't need to re-confirm the whole module list — just note which pages will be touched (updated, added, or removed) based on the diff, and confirm that briefly if the change set looks larger than expected.

## Step 3: Write

Once the module list and location are confirmed:

- Write/update `README.md`, `architecture.md`, `data-flow.md`, `decisions.md`, and `modules/*.md` (one file per confirmed module) at the confirmed path.
- Use Mermaid diagrams (` ```mermaid ` blocks) in `architecture.md` and `data-flow.md` — GitHub and most modern doc viewers render these natively, and a diagram communicates component relationships faster than prose.
- In `decisions.md`, mark any inferred rationale as `Inferred:` — never assert a design reason as settled fact unless it's stated in code comments, commit messages, or existing docs. Guessing at intent is useful, but only if the reader can tell it's a guess.
- Keep each module page under ~150 lines: purpose, public interface, key dependencies, gotchas. Link out to related pages rather than duplicating detail — the wiki should stay skimmable even as it grows to dozens of pages.
- `README.md` should list all generated pages with one-line descriptions, plus a note that `Inferred:` content should be verified and that the state file exists so re-runs are incremental.

## Step 4: Update state

Write (or overwrite) `.wiki-state.json` at the wiki root with the current HEAD commit hash, the generation date, and the full list of generated file paths:

```json
{
  "last_generated_commit": "<git rev-parse HEAD>",
  "generated_at": "<ISO date>",
  "generated_files": ["docs/wiki/README.md", "docs/wiki/architecture.md", "..."]
}
```

This is what makes the next run incremental instead of a full rewrite.

## Step 5: Report

Summarize what happened: new pages, updated pages, removed pages (if a module was deleted), and anything marked `Inferred:` or otherwise uncertain that the user should double-check. If this was an incremental update, briefly note what triggered the changes (which files/modules were in the diff).
