# wiki_plan.yaml — configuration reference

`wiki_plan.yaml` lets the user steer wiki generation *before* it runs. It lives
at `<output>/wiki_plan.yaml` (the user-chosen output path, default `docs/wiki/`)
and is committed to Git so the whole team shares the same generation intent.
After editing it, the wiki must be (re)generated for changes to take effect.

The output path and languages are chosen by the user up front (Phase 0) and are
recorded here so future runs reuse them.

## Full schema

```yaml
version: 1

wiki:
  output: "docs/wiki"          # output directory (user's choice; default docs/wiki)
  template: "architecture"     # architecture | product_requirement | onboarding
  languages: ["en"]            # any languages, by short code; one output tree each. default ["en"]
  notes:                        # free-form guidance injected during planning
    - text: "Focus on business workflows over code minutiae; audience is new engineers."
      author: "tri"
  documents:                    # OPTIONAL strict page allowlist. If non-empty,
    - title: "System Architecture Overview"   # ONLY these pages are generated.
      goal: "Describe overall architecture, core modules, and their interactions."
      parent: ""               # optional: parent page title (for nesting in Home)
      hints: "Include a component diagram and a module dependency graph."
    - title: "Order System"
      goal: "Explain the full order lifecycle from creation to fulfillment."
      parent: "System Architecture Overview"
      hints: ""

scope:
  include:                      # .gitignore syntax; empty = whole repo
    - "src/**"
  exclude:
    - "**/test/**"
    - "**/*.min.js"
    - "vendor/**"
    - "node_modules/**"
```

## Field reference

| Key | Meaning |
| --- | --- |
| `version` | Schema version. Always `1` for now. |
| `wiki.output` | Output directory for the wiki. Set from the user's Phase 0 choice; defaults to `docs/wiki`. |
| `wiki.template` | Page blueprint to use when `documents` is empty. See `templates.md`. |
| `wiki.languages` | Which language trees to emit (any language, by short code). Each produces `<output>/<lang>/`. Defaults to `["en"]`. |
| `wiki.notes` | Guidance prompts that shape audience, depth, and focus of every page. |
| `wiki.documents` | Explicit page allowlist. **When non-empty, exactly these pages are generated** — the template's default page set is ignored. Each entry has `title`, `goal`, optional `parent`, optional `hints`. |
| `scope.include` | Files visible to generation (`.gitignore` syntax). Empty means all tracked files. |
| `scope.exclude` | Files hidden from generation. Applied after `include`. |

## Behavior rules

- If `documents` is provided and non-empty, honor it strictly: generate those
  page titles, nest them per `parent`, and use `goal`/`hints` to drive content.
- If `documents` is empty, derive pages from `template`.
- `scope` filters what the analyzer may read and cite. Never document an excluded
  path even if it's referenced by an included one — reference it by name only.
- `notes` are advisory but strong: they set tone (e.g., onboarding vs. deep-dive)
  and highlight subsystems to emphasize.
- Missing file → create it from `assets/wiki_plan.example.yaml` with inferred
  defaults, then show the user before generating.

## Minimal example

```yaml
version: 1
wiki:
  output: "docs/wiki"
  template: "onboarding"
  languages: ["en"]
scope:
  include: []
  exclude: ["node_modules/**", "dist/**"]
```

## Custom-path, allowlisted example

```yaml
version: 1
wiki:
  output: "wiki"                # write to ./wiki instead of docs/wiki
  template: "architecture"
  languages: ["en"]
  notes:
    - text: "Emphasize the payment and order subsystems."
  documents:
    - title: "Architecture Overview"
      goal: "System-wide structure and module interactions."
    - title: "Payment Subsystem"
      goal: "Payment flow, providers, retries, and idempotency."
      parent: "Architecture Overview"
scope:
  include: ["src/**"]
  exclude: ["**/__tests__/**"]
```

## Multi-language example

```yaml
version: 1
wiki:
  output: "docs/wiki"
  template: "architecture"
  languages: ["en", "ja"]        # any languages you choose, by short code
scope:
  include: ["src/**"]
```
