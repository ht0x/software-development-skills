# Page templates

When `wiki_plan.yaml` has no explicit `documents` allowlist, derive the page set
from the selected `template`. Each page is a Markdown file under
`<output>/<lang>/` (the user-chosen output path, default `docs/wiki/`), prefixed
with a two-digit order (`01-`, `02-`, …). Always also emit `Home.md` linking
every page.

Every page follows the same skeleton:

```
# <Page Title>

> One-paragraph summary of what this page covers.

## <Sections...>

...prose grounded in cited source files...

## Sources
- `path/to/file.ext` — what was drawn from it
```

Cite sources inline as `` `path/to/file` `` wherever a claim is made, and list
the main ones under a `## Sources` footer.

---

## Template: `architecture`

Comprehensive technical analysis. Default page set:

1. **Architecture Overview** — what the system does, high-level structure, the
   major components and how they interact. Include a component/architecture
   Mermaid graph.
2. **`<Module>` pages** (one per major module/package) — responsibility, public
   surface (key classes/functions/endpoints), collaborators, notable internals.
3. **Data & Persistence** — data models, storage, schemas/migrations, caching.
   Include an ER diagram if a schema exists.
4. **Key Flows** — the most important runtime paths (request lifecycle, job
   pipeline, auth). One sequence diagram per flow.
5. **Dependencies** — internal module dependency graph + notable external libs
   and why they're used.
6. **Build, Run & Deploy** — how to build, run, test, and ship; env/config;
   CI/CD if present.

## Template: `product_requirement`

Product-oriented framing derived from the code. Default page set:

1. **Product Overview** — what the product does and for whom, inferred from
   entry points, routes, UI, and domain names.
2. **Features** — enumerated capabilities, each mapped to the code that
   implements it.
3. **User Workflows** — end-to-end user journeys; sequence or flowchart diagrams.
4. **Requirements** — functional and non-functional requirements evidenced by the
   code (validation, limits, permissions, SLAs in config).
5. **Domain Model** — core entities and relationships; ER/class diagram.

Mark inferred product intent clearly as inference, not fact, when the code is
ambiguous.

## Template: `onboarding`

New-engineer focus, minimal jargon. Default page set:

1. **Getting Started** — clone, install, configure, run, and test the project,
   step by step, from the actual build/config files.
2. **Project Layout** — a tour of the directory tree: what lives where and why.
   Include a simple structure diagram.
3. **Core Concepts** — the handful of ideas you must understand to be productive
   (domain terms, key abstractions), each pointing to where they live in code.
4. **Common Tasks** — "how do I add X / change Y / debug Z", as concrete recipes.
5. **Glossary** — project-specific terms and acronyms.

---

## Choosing modules for per-module pages

Group source into logical units, preferring (in order): declared packages/modules,
top-level `src` subdirectories, then bounded contexts by naming. Create a page
only for modules with real surface area; fold trivial helpers into a parent page.
Cap per-module pages at a reasonable number (~12) for large repos and summarize
the long tail in the Architecture Overview.
