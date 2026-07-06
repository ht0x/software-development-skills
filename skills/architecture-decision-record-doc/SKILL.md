---
name: architecture-decision-record-doc
description: >-
  PRIMARY PURPOSE: record a technical decision with long-term impact — a
  choice between technologies, patterns, or approaches worth preserving for
  future reference. Written primarily for Team Leads and Tech Leads.
  Generates a filled-in Architecture Decision Record (ADR) document. Works
  across domains (web, backend, game, mobile, desktop). Trigger with
  "/architecture-decision-record-doc", "create an ADR for X", "write a
  decision record for choosing Y", "document why we chose X over Y", or
  whenever a technical decision will have long-term consequences and needs
  its alternatives and trade-offs captured. Not needed for routine
  implementation choices that don't need long-term justification — propose
  a quick note instead.
disable-model-invocation: true
---

# /architecture-decision-record-doc

Generate a complete, filled-in Architecture Decision Record (ADR) — a short, durable document capturing a specific technical decision, the alternatives considered, and the consequences of choosing it.

## Usage

```
/architecture-decision-record-doc $ARGUMENTS
```

Example: `/architecture-decision-record-doc choosing a save data format for the farming game`

This skill also activates conversationally — e.g. "write an ADR for why we're using PostgreSQL over MongoDB" — without needing the slash form.

## What an ADR Is For

An ADR records one decision: what was chosen, what else was considered, and what the trade-offs are. It's meant to be short enough to read in a few minutes and durable enough that someone reading it a year later understands why the decision was made — not just what it was.

Use this for decisions worth justifying long-term: choosing between technologies, frameworks, architectural patterns, libraries, or significant structural approaches. Skip it for routine implementation choices that don't need this level of justification — offer a brief note instead and proceed only if the user confirms they want the full ADR.

## Workflow at a Glance

```
1. Elicit   →  ask about the decision, options considered, and consequences
2. Number   →  ask if sequential ADR numbering should be tracked, or leave as placeholder
3. Draft    →  fill the ADR using gathered context + reasonable inference
4. Flag     →  mark any field that's still genuinely unknown as a TODO, never invent specifics
5. Deliver  →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1 — Elicit the Decision

ADRs are usually short and the user often already knows the decision they want recorded — don't over-ask if they've already given the key details. Cover what's missing from these areas:

**The decision itself**
- What decision is being recorded? What problem or situation made this decision necessary?
- What was actually chosen?

**Alternatives considered**
- What other options were on the table? For each, what were the pros and cons that led to it being rejected (or chosen)?
- If the user says there was really only one viable option, that's fine — don't invent rejected alternatives just to fill the section out. Note that explicitly instead.

**Consequences**
- What good outcomes does this decision bring (positive consequences)?
- What does it cost, or what risk does it introduce (negative consequences)? Trade-offs being consciously accepted belong here too.

**Practical rules**
- Are there concrete rules developers (or AI agents working on this codebase) should follow as a result of this decision? E.g. "always use X for Y," "never introduce Z without revisiting this ADR."

Don't force every question if context already answers it. If the user pushes back on answering everything ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 2 — Determine Numbering

ADRs are conventionally numbered sequentially (e.g. `ADR-0001`, `ADR-0002`). Ask the user whether they want this tracked:

- If they want sequential numbering and can tell you the last number used (or the existing ADRs in their project), use the next number in sequence.
- If they want it tracked but don't know the last number, ask them to check their ADR log/folder, or proceed with a placeholder and a clear `TODO: confirm sequence number` note.
- If they don't want numbering tracked, leave the identifier as a placeholder (e.g. `ADR-XXXX`) for them to assign manually.

Don't guess a number — an incorrect ADR number that collides with an existing one is worse than an honest placeholder.

---

## Phase 3 — Draft the Document

Fill in every section using gathered context. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics — a fabricated alternative or consequence is worse than an honest gap, since ADRs exist specifically to be trusted later as the real record of why a decision was made.

### Document Template

```markdown
# ADR-[number or XXXX]: [Decision Title]

## Status
`Proposed / Accepted / Rejected / Superseded / Deprecated`

## Date
[YYYY-MM-DD]

## Context
[Describe the problem and situation that made this decision necessary. What constraints, requirements, or forces were at play.]

## Decision
[Describe the decision that was made, stated clearly and directly — what was chosen, not just the topic.]

## Alternatives Considered

### Option A: [Name]
Pros:
- `[pro]`

Cons:
- `[con]`

### Option B: [Name]
Pros:
- `[pro]`

Cons:
- `[con]`

*(Add or remove Option subsections to match what was actually considered. If only one viable option existed, state that directly instead of fabricating alternatives.)*

## Consequences

Positive:
- `[positive consequence]`

Negative:
- `[negative consequence or trade-off being accepted]`

## Rules
[Concrete, practical rules developers and AI agents should follow as a result of this decision. Keep these actionable — e.g. "Always use X for Y" rather than restating the decision.]
```

---

## Phase 4 — Flag Gaps Honestly

Before presenting the draft, scan it for any section filled with a guess rather than something the user actually stated. Convert genuine guesses into `TODO:` markers instead of presenting them as settled facts.

Pay particular attention to:
- Alternatives Considered — don't invent plausible-sounding rejected options if the user only described one approach; say so directly instead.
- Consequences — don't pad the Negative list with generic risk boilerplate; only include trade-offs the user actually discussed or that are direct, clear implications of the decision.
- Rules — don't generate vague filler rules; if no concrete rule was discussed, leave it as `TODO: confirm any practical rules to enforce this decision` rather than writing something hollow like "follow best practices."

---

## Phase 5 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Read `/mnt/skills/public/md` conventions if relevant, write the filled document directly as a `.md` file |
| **DOCX** | Read `/mnt/skills/public/docx/SKILL.md` before generating — follow its formatting and table guidance |

Save the file to `/mnt/user-data/outputs/`, then use `present_files` to share it. Use the decision title for the filename, e.g. `adr-0007-save-data-format.md`.

Keep the chat response brief: a short note on what was filled vs. what's flagged as TODO, then the file. Don't restate the whole document inline if it's already being delivered as a file.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Every section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Alternatives Considered reflects what was actually discussed, not fabricated options
- [ ] Decision is stated as an actual decision, not a restated problem statement
- [ ] Consequences include genuine trade-offs, not just upside
- [ ] Rules are concrete and actionable, not vague restatements of the decision
- [ ] ADR number is either a real confirmed sequence number or an honest placeholder, never guessed
