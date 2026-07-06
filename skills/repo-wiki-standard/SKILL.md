---
name: repo-wiki-standard
description: >-
  Triggered ONLY by the slash command /repo-wiki-standard. Generates and maintains a
  living, structured wiki for a code repository — architecture overviews,
  per-module pages, dependency and sequence diagrams, and technical insights
  derived directly from the source. Config-driven via a wiki_plan.yaml, supports
  Architecture / Product Requirement / Onboarding templates, Mermaid diagrams,
  any output language, and incremental updates that regenerate only pages whose
  source changed while protecting hand-edited content. Before creating anything,
  it asks the user for the output path (default docs/wiki) and the language(s).
---

# Repo Wiki

Turn a codebase into living, shared documentation. This skill analyzes a Git
repository and produces a structured wiki: an overview, per-module pages,
diagrams, and cross-references — every claim grounded in the actual source.
It is config-driven and incremental, so it can be regenerated as the code
evolves without discarding human edits.

## When to use

This skill is triggered **only** by the slash command `/repo-wiki-standard`. Do
not fire it from natural-language phrasing; if the user describes wanting repo
docs without the command, suggest they run `/repo-wiki-standard`.

`/repo-wiki-standard` supports these intents, optionally passed as arguments:

- generate a wiki for the first time
- update / sync an existing wiki after code changes
- (re)configure via `wiki_plan.yaml`

Arguments may include an output path and/or language(s). Any choice not supplied
is collected in Phase 0 before anything is created.

## Core concepts

- **Wiki pages** — human-readable Markdown docs (overview, module pages, flows).
- **wiki_plan.yaml** — a pre-generation config that steers scope, template,
  languages, guidance notes, and an optional strict page allowlist.
- **Manifest** (`.wiki_manifest.json`) — records which source files each page was
  built from (with content hashes), so a later run can regenerate only the pages
  whose sources changed. This is what makes the wiki "living."
- **Protected blocks** — regions a human edited by hand, wrapped in markers so
  automatic regeneration never overwrites them.

## Output layout

Everything lives under the user's chosen **output path** (`<WIKI>`) in the target
repository so it can be committed and shared over Git. `<WIKI>` defaults to
`docs/wiki/` when the user doesn't specify one (see Phase 0). One subfolder is
created per selected language, using its short code (e.g. `en/`, `ja/`, `fr/`):

```
<WIKI>/
  wiki_plan.yaml         # config (create from assets/wiki_plan.example.yaml if absent)
  .wiki_manifest.json    # page ↔ source-file map + hashes (machine-managed)
  <lang>/                # one tree per selected language, e.g. en/
    Home.md              # index / table of contents
    01-Architecture-Overview.md
    02-<Module>.md
    ...
```

Always write under `<WIKI>` — never scatter files elsewhere or hardcode a
different path once the user has chosen one.

---

## Workflow

Follow these phases in order. Prefer read-only analysis first; only write files
in the generation phase.

### Phase 0 — Gather the user's choices (before creating anything)

Do this **first**, before any analysis, directory creation, plan file, page, or
manifest is written. Nothing is created until both choices below are settled.

1. **Output path.** If the `/repo-wiki-standard` invocation included a path, use it.
   Otherwise ask the user where the wiki should be written and state the default:
   *"Where should the wiki be written? (default: `docs/wiki/`)"*. If they decline
   or give no answer, use `docs/wiki/`. Call the resolved path `<WIKI>`.
2. **Language(s).** If the invocation named a language, use it. Otherwise ask:
   *"Which language(s) should the wiki be written in? (default: English)"*. Accept
   one or more languages; if none is given, use English. Record the short code for
   each (e.g. `en`, `ja`, `fr`) — these become the per-language subfolders.

Only after both are resolved, continue. If an existing wiki is found at `<WIKI>`
with a `wiki_plan.yaml`, treat its stored `output`/`languages` as the current
choices and confirm rather than re-ask.

### Phase 1 — Preconditions

1. Confirm the target is a Git repo with at least one commit
   (`git rev-parse --is-inside-work-tree` and `git rev-parse HEAD`). If not, tell
   the user the wiki needs a committed Git repo and stop.
2. If the repo has more than ~10,000 tracked files, tell the user and recommend
   narrowing `scope.exclude` before proceeding (large trees are slow and noisy).

### Phase 2 — Load or create the plan

1. Look for `<WIKI>/wiki_plan.yaml`.
   - If present, parse it. It is the source of truth for template, languages,
     scope, notes, and any page allowlist. See `references/wiki_plan.md`.
   - If absent, copy `assets/wiki_plan.example.yaml` to `<WIKI>/wiki_plan.yaml`,
     writing in the `output` path and `languages` the user chose in Phase 0 plus
     sensible defaults inferred from the repo (`src/**` include if it exists), and
     briefly show the user the plan you'll use.
2. Resolve effective settings: `output` path, `template`, `languages` (from Phase
   0; default `["en"]`), `scope.include/exclude`, `notes`, and `documents`
   (allowlist, may be empty). Phase 0 choices win over stale file values.

### Phase 3 — Analyze the codebase

Build a mental model of the repo. Do this efficiently — sample, don't read
everything. Gather:

1. **Repo shape** — top-level dirs, build/config files (`package.json`, `go.mod`,
   `pyproject.toml`, `pom.xml`, `Cargo.toml`, `Makefile`, Dockerfiles, CI configs).
   Infer language(s), framework(s), and how the project is built and run.
2. **Entry points** — `main`, `index`, server bootstraps, CLI entry, app roots.
3. **Modules / components** — group source into logical units (by directory,
   package, or bounded context). This grouping drives the per-module pages.
4. **Dependencies** — internal (module → module) and notable external libraries.
   Note direction of dependencies for the dependency diagram.
5. **Key flows** — request lifecycle, data pipeline, auth, or the domain's core
   workflow. These become sequence diagrams.
6. **Cross-cutting concerns** — config, logging, error handling, persistence, tests.

Respect `scope.include/exclude` (`.gitignore` syntax) — never document excluded
paths. Record, for each finding, the source file(s) it came from; you will cite
them in the pages.

### Phase 4 — Plan the pages

- If `wiki_plan.yaml` has a non-empty `documents` allowlist, generate **exactly**
  those pages (honoring `parent`, `goal`, `hints`) — no more, no less.
- Otherwise derive the page set from the chosen template
  (see `references/templates.md`):
  - **architecture** — Overview, Architecture, one page per major module,
    Data & Persistence, Key Flows, Dependencies, Build & Deploy.
  - **product_requirement** — Product Overview, Features, User Workflows,
    Requirements, Domain Model.
  - **onboarding** — Getting Started, Project Layout, Core Concepts, Common Tasks,
    Glossary.
- Always include a `Home.md` index that links every page.
- Fold the user's `notes` into how each page is framed (audience, depth, focus).

Present the planned page list to the user before generating if the repo is large
or the plan was auto-created; otherwise proceed.

### Phase 5 — Generate pages

For each planned page, write a Markdown file under `<WIKI>/<lang>/`:

- Start with a one-paragraph summary, then structured sections.
- **Ground every substantive claim in source.** Cite files inline as
  `` `path/to/file.ext` `` (optionally with a symbol or line range). Do not assert
  behavior the code doesn't show.
- Include **Mermaid diagrams** where they clarify structure — see
  `references/mermaid.md`. At minimum:
  - a component/architecture graph on the Architecture page,
  - a module dependency graph,
  - a sequence diagram for at least one key flow.
- Cross-link related pages with relative Markdown links.
- Keep prose in the reader's register set by `notes` (e.g., new-engineer focus).
- Honor **protected blocks**: if a page already exists, preserve any content
  between `<!-- wiki:protected -->` and `<!-- /wiki:protected -->` verbatim.
  See `references/incremental-update.md`.

If multiple `languages` are configured, generate a parallel tree per language
(one subfolder per language code, e.g. `en/`, `ja/`). Translate content
faithfully; keep code identifiers, paths, and diagram node IDs unchanged across
languages.

### Phase 6 — Write the manifest

Update `<WIKI>/.wiki_manifest.json` recording, for each page: its path, the
template used, the language, and the list of source files it was built from with
their current content hashes (e.g. `git hash-object`). This enables Phase 7.
Schema and hashing details are in `references/incremental-update.md`.

### Phase 7 — Incremental update (on later runs)

When the user asks to update/sync an existing wiki:

1. Load `.wiki_manifest.json`.
2. Recompute hashes for each recorded source file. A page is **stale** if any of
   its sources changed, was added, or was removed.
3. Regenerate only stale pages (and `Home.md` if the page set changed).
   Leave fresh pages untouched.
4. Preserve every `<!-- wiki:protected -->` block during regeneration.
5. Report a short diff to the user: which pages were updated, added, or removed,
   and why (which source files changed).

If the user hand-edited a Markdown page outside a protected block and its sources
didn't change, do not overwrite it — surface the conflict and ask.

### Phase 8 — Wrap up

- Summarize what was generated/updated (page count, languages, diagrams).
- Remind the user they can commit `<WIKI>/` to share the wiki via Git, and can
  refine `wiki_plan.yaml` then re-run to steer future generations.

## Reference files

- `references/wiki_plan.md` — full `wiki_plan.yaml` schema, options, examples.
- `references/templates.md` — page blueprints for the three templates.
- `references/mermaid.md` — diagram types and conventions.
- `references/incremental-update.md` — manifest schema, hashing, protected blocks.
- `assets/wiki_plan.example.yaml` — starter config to copy into a repo.

## Guardrails

- Only document what the source supports; mark genuine unknowns as `TODO` rather
  than inventing behavior.
- Never delete or overwrite protected blocks or unrelated user files.
- Keep the wiki inside the chosen `<WIKI>` path; don't scatter files elsewhere.
- The manifest is machine-managed — don't ask the user to edit it by hand.
