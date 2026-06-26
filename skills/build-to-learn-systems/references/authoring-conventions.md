# Authoring conventions (read before writing a phase)

This file holds the exact formatting and structural conventions for course phase
documents. Keep them consistent across every phase — consistency is what makes a
long multi-document course feel like one coherent book.

## Fact vs inference (hard requirement)

The learner explicitly wants to know what is an established technical fact versus
your recommendation. Apply this everywhere:

- State facts plainly.
- When you give an opinion, a default choice, an estimate, or a "you should",
  mark it. A short inline note works: *"(Fact: … . Recommendation: … — this is my
  opinion, not absolute.)"* Inside an ADR, the comparison table and the
  "Consequences" section carry most of the inference; keep the "Decision" line
  factual about what was chosen.

## Callout boxes

Author callouts as HTML blocks with `markdown="1"` so Markdown inside still renders:

```html
<div class="callout key" markdown="1">
<span class="lbl">◆ Core concept — Title</span>
Body text. Can contain **markdown**, `code`, lists.
</div>
```

Four classes, each with a conventional label prefix:

- `key` → ◆ core concept (something to remember long-term)
- `tip` → ✔ best practice (do-it-right-the-first-time advice)
- `warn` → ▲ caution (a common beginner pitfall)
- `note` → ℹ note (aside, or a pointer to another phase)

Use callouts to spotlight the few ideas that matter most per section — not on every
paragraph. A page wall-to-wall with callouts loses its emphasis.

## Diagrams (Mermaid)

Use fenced ```mermaid blocks. Keep each diagram focused on one idea. Useful types:

- `graph TB` / `graph LR` for architecture and data-flow.
- `sequenceDiagram` for protocol handshakes (TCP, WebSocket upgrade, auth flow).
- Put node text in quotes; use `<br/>` for line breaks inside a node.
- Cylinders `[("…")]` read as datastores; subgraphs group a tier.

The pipeline renders Mermaid to SVG; do not hand-write SVG.

## ADR template

Use this exact shape for every Architecture Decision Record:

```markdown
### ADR-XXXX — <short title>

**Context.** What problem/forces led to a decision point.

**Decision.** What was chosen (state it factually).

**Alternatives & comparison.**

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| **<chosen>** ✅ | … | … | — (this is the choice) |
| <alt> | … | … | … |

**Consequences.** What this buys, what it costs, what it commits future phases to.
```

Number ADRs globally and never delete an old one — supersede it with a new ADR and
note the supersession. Keep an ADR ledger line in the course-context file.

## SPEC template

End each phase with a specification the learner can self-check against:

```markdown
# SPEC Phase N — specification & acceptance

## Scope
| In scope | Out of scope (later phases) |
|----------|------------------------------|
| … | … |

## Functional requirements
- **FR-N.1** — …
- **FR-N.2** — …

## Non-functional requirements
- **NFR-N.1 (Reproducibility)** — …
- **NFR-N.2 (Durability / ordering / security / …)** — …

## Acceptance checklist
- [ ] …
- [ ] At least one deliberate failure test ("stop service X, confirm it reports unhealthy").
```

Distinguish functional ("what it does") from non-functional ("how good it is");
teaching this distinction is itself a goal.

## Per-phase section order (recap)

Cover → Objectives → Theory → Architecture & ADRs → Hands-on (runnable) →
Test & Deploy → SPEC & checklist → Summary & next-phase preview.

## Cover page

Author the cover as a `<div class="cover">` block:

```html
<div class="cover">
<div class="kicker">Course · <COURSE NAME></div>
<h1>Phase N<br/><Phase title></h1>
<div class="sub">One-line subtitle</div>
<div class="meta">
Audience / project / "Document N / total" / stack summary
</div>
</div>
```

## Tone

Explain *why* things matter rather than dictating. Use everyday analogies for hard
concepts (a post office for client/server, a registered letter vs a postcard for
TCP vs UDP). Assume an intelligent newcomer to the domain, not a child. Keep the
learner's stated career goal in mind (e.g. aiming for tech lead → emphasize the
judgment skills: ADRs, SPECs, trade-off analysis, knowing when NOT to use a
technique like sharding).
