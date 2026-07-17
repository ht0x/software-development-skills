# Authoring conventions (read before writing a phase)

This file holds the exact formatting and structural conventions for course phase
documents. Keep them consistent across every phase — consistency is what makes a
long multi-document course feel like one coherent book.

For the **Roadmap** document specifically, see `references/roadmap-doc.md`. The
callout, diagram, and cover conventions below apply to it too.

## Depth levels (Standard vs Deep)

The learner picks a depth level when the course starts (Core rule 6); it's recorded
in the manifest §E and applies to every phase. Never mix levels mid-course.

| | **Standard** | **Deep** |
|---|---|---|
| Target length | ~1000+ lines (~20 pages) | ~2000–2500 lines (~40–55 pages) |
| Glossary section | — | **Required** |
| Problem→solutions→comparison | ADR tables only | **Required for every technical decision** |
| Jargon | Define the important ones | **Every term, on first use** |
| Code | Inline comments + per-part explanation | **+ line-by-line dissection below each block** |
| Hands-on steps | What to do | **+ why, for every step** |
| Common-mistakes section | — | **Required** |

Recommend **Deep** for learners new to the domain or complex systems; **Standard**
for experienced learners who want speed.

### What each Deep-only section must contain

**Terminology glossary** (top of the phase, before Theory). Every new term the phase
uses, in a table or definition list:

> English name → learner's-language name → literal meaning → everyday analogy →
> where it shows up in this project.

The rule it enforces: *the learner never meets an undefined term*. If a term appears
in the phase body and isn't in this glossary or an earlier one, that's a bug.

**Problem & solutions.** For every technical decision, in this order:

1. State the **problem** as a question the learner would ask.
2. List **every plausible solution** — including the naive one and the one you reject.
3. A **comparison table**: pros / cons / complexity / performance.
4. The **pick, and why** — with the fact/inference split visible.

This differs from an ADR: the ADR records the decision for the *project*; this section
teaches the learner *how to reason* about the choice. A phase can have several of
these feeding one ADR.

**Code dissection.** Each code block gets:

- (a) **Dense inline comments** in the code itself — what and why.
- (b) **A dissection below**: walk the block line-by-line or chunk-by-chunk. Cover
  syntax the learner may not know, the intent, the pitfalls, and — the important one
  — *why it's written this way rather than the obvious alternative*.

**Common mistakes.** The errors beginners actually make on this topic. Each entry:
the mistake → **the exact symptom** (the real error text or observed behaviour) → the
fix. Symptoms matter more than causes; the learner searches by symptom.

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

**Standard:** Cover → Objectives → Theory → Architecture & ADRs → Hands-on (runnable)
→ Test & Deploy → SPEC & checklist → Summary & next-phase preview.

**Deep:** Cover → Objectives → **Glossary** → Theory → **Problem & solutions** →
Architecture & ADRs → Hands-on (**+ dissection**) → **Common mistakes** →
Test & Deploy → SPEC & checklist → Summary & next-phase preview.

## Markdown gotcha — bold label followed by a list

python-markdown renders a list inline if there's no blank line before it:

```markdown
**New concepts.**
- Thing one          ← WRONG: renders as "New concepts. - Thing one"

**New concepts.**

- Thing one          ← RIGHT
```

This bites constantly in Roadmaps and glossaries. Check a rendered page before
delivering.

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
