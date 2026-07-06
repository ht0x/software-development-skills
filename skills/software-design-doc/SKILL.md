---
name: software-design-doc
description: >-
  PRIMARY PURPOSE: work through a large module or task and align dev, QA,
  DevOps, and PM before implementation. Not for small bug fixes, typo fixes,
  or doc-only changes. Written primarily for Team Leads and Tech Leads. 
  Generates a filled-in Software Design Document (SDD) covering all 14 standard 
  sections — from Overview and Goals to Design Approval and Appendix. 
  Triggered only by the slash command /software-design-doc. 
  Asks for output format (Markdown or Word) before generating. Works across domains: 
  web, backend, game, mobile, desktop. Fills each section from context and marks 
  genuinely unknown fields with TODO rather than inventing placeholder facts.
disable-model-invocation: true
---

# /software-design-doc

Generate a complete, filled-in Software Design Document (SDD) from a feature description or brief, covering all 14 standard sections and aligned for cross-functional review.

## Usage

```
/software-design-doc
```

Slash command only — does not trigger conversationally. Provide the feature name, a brief description, and any known constraints inline or as an attachment. The skill will ask for output format, then generate immediately.

## Workflow at a Glance

```
1. Read     →  extract feature context from the conversation and any attachments
2. Elicit   →  collect missing metadata and ask for output format (Markdown or Word)
3. Generate →  write the full 14-section SDD with domain-aware hints
4. Deliver  →  save to /mnt/user-data/outputs/ and present the file
```

---

## Phase 1 — Read Context

Before asking anything, extract from the conversation and any attached files:

- **Feature / project name**
- **Author and reviewers** (infer from conversation if possible)
- **Problem being solved** — what's broken, missing, or needed
- **Tech stack or domain** — web, backend, game, mobile, desktop (or mixed)
- **Known requirements, constraints, or related docs** (PRDs, RFCs, tickets)
- **Scope signals** — small fix, medium feature, or large system change

---

## Phase 2 — Elicit Missing Information

Ask only for what you could not determine from context. Always ask for output format.

**Collect if missing:**
- Feature / project name
- Author name(s)
- Reviewer name(s)
- Document status: Draft / In Review / Approved / Superseded

**Always ask:**
- Output format: Markdown (.md) or Word (.docx)?

Keep the form short — one question per genuinely unknown field. Do not ask for things already inferable from context.

---

## Phase 3 — Generate the SDD

Generate the full document immediately after elicitation. Fill each section with real content from context; use `TODO: [description]` for genuinely unknown fields — never invent placeholder facts.

### Document header

```markdown
# Software Design Document (SDD)

| Field | Value |
|---|---|
| **Project / Feature** | [name] |
| **Author(s)** | [name] |
| **Reviewers** | [names] |
| **Status** | Draft / In Review / Approved / Superseded |
| **Version** | 0.1 |
| **Last Updated** | [YYYY-MM-DD] |
| **Related Docs** | [links: PRD, RFC, tickets] |
```

---

### Section 1 — Overview

2–4 sentences. Someone unfamiliar with the feature should grasp the gist from this section alone.

---

### Section 2 — Background & Context

- **Problem statement** — what's broken, missing, or needed
- **Current state** — how things work today (if applicable)
- **Why now** — the trigger or motivation

---

### Section 3 — Goals & Non-Goals

**Goals** — measurable, specific outcomes.

**Non-Goals** — explicitly out of scope, to prevent scope creep.

---

### Section 4 — Requirements

**Functional** — what the system must do.

**Non-Functional** — cover: performance, scalability, availability, security, accessibility, observability, cost. Use `N/A` for irrelevant dimensions, not silence.

**Constraints & Assumptions** — tech stack, deadlines, team size, dependencies, things assumed true.

---

### Section 5 — Proposed Design

The core of the document. Fill all sub-sections; mark unknowns with `TODO`.

#### 5.1 High-Level Architecture

Diagram (ASCII, Mermaid, or description) + narrative of major components and how they interact.

#### 5.2 Components / Modules

For each component: responsibility, inputs/outputs, key logic, ownership.

Domain hints:
- For web/backend: services, controllers, workers, queues, caches
- For game: scenes, managers, systems, prefabs, ScriptableObjects
- For mobile/desktop: screens, view models, platform-specific modules

#### 5.3 Data Model

Entities, schemas, relationships, storage choices, migration notes.

Domain hints:
- For web/backend: SQL/NoSQL schemas, migration files, API contracts
- For game: save data structures, ScriptableObject schemas, level data formats
- For mobile/desktop: local DB schema, sync strategy, offline handling

#### 5.4 APIs / Interfaces

Endpoints or contracts: method, request/response shape, error cases, versioning.

#### 5.5 Key Flows

Walk through 1–3 important sequences (e.g., request lifecycle, error path, happy path) step by step.

---

### Section 6 — Alternatives Considered

| Option | Pros | Cons | Why not chosen |
|---|---|---|---|
| [A] | | | |
| [B] | | | |

Include at least two alternatives. If none were seriously considered, say so explicitly.

---

### Section 7 — Cross-Cutting Concerns

- **Security & privacy** — auth, data handling, threat surface
- **Error handling & resilience** — failure modes, retries, fallbacks
- **Observability** — logging, metrics, tracing, alerting
- **Performance & scale** — expected load, bottlenecks, limits

---

### Section 8 — Testing Strategy

What "done and verified" means. Cover relevant test types; use `N/A` for irrelevant ones.

Domain hints:
- General: unit, integration, e2e, load, manual, review
- For Unity: EditMode tests, PlayMode tests
- For web: Jest (unit), Cypress / Playwright (e2e), k6 / Locust (load)
- For mobile: XCTest / Espresso (unit), Detox / Appium (e2e)

---

### Section 9 — Rollout & Migration

Phasing, feature flags, backfill/migration steps, rollback plan. If greenfield with no migration, state that explicitly.

---

### Section 10 — Risks & Open Questions

| Risk / Question | Impact | Mitigation / Owner |
|---|---|---|
| | | |

---

### Section 11 — Open Design Questions

Unresolved questions that need input before implementation can proceed safely.

| Question | Owner | Needed By | Status |
|---|---|---|---|
| `[question]` | `[name/role]` | `[date or milestone]` | Open / Answered |

---

### Section 12 — Timeline & Milestones

Rough phases or dates, with dependencies called out.

---

### Section 13 — Design Approval

| Reviewer | Decision | Date | Notes |
|---|---|---|---|
| `[name]` | Approved / Changes Requested / Rejected | `[YYYY-MM-DD]` | `[notes]` |

---

### Section 14 — Appendix

Glossary, references, supporting diagrams, raw data. Omit if empty.

---

## Phase 4 — Deliver

1. For Markdown: save to `/mnt/user-data/outputs/<feature-name>-sdd.md`
2. For Word: use the `docx` skill to produce `/mnt/user-data/outputs/<feature-name>-sdd.docx`
3. Call `present_files` with the output path.
4. Add a 1–2 sentence note listing any remaining `TODO` fields the user should fill in manually.

---

## Quality Checklist

Before presenting the output, verify:
- [ ] Skill name is `software-design-doc` and matches the frontmatter `name` field
- [ ] Description is under 1024 characters
- [ ] No conversational trigger phrases in description (slash-only skill)
- [ ] Output format was asked and matches what was generated
- [ ] No confirmation step present (skill generates immediately after elicitation)
- [ ] All 14 sections are present — none silently dropped
- [ ] Domain-hint sub-bullets appear in sections 5.2, 5.3, and 8
- [ ] Unknown fields use `TODO: [description]`, not invented placeholder facts
- [ ] Non-functional requirements and cross-cutting concerns use `N/A` for irrelevant dimensions
- [ ] Sections 10 and 11 are kept separate (risks vs. open design questions)
- [ ] Output file saved to `/mnt/user-data/outputs/` and presented with `present_files`
