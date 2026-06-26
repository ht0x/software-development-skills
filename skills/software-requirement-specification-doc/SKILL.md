---
name: software-requirement-specification-doc
description: >-
  PRIMARY PURPOSE: surface ambiguous requirements, missing non-functional
  requirements, missing edge cases, and missing acceptance criteria before
  design or implementation begins — scoped to a module, system, or service
  (not a small task or bug fix). Written primarily for BAs, POs, System
  Analysts, and BrSEs. Generates a filled-in Software Requirement
  Specification (SRS) document. Works across domains (web, backend, game,
  mobile, desktop). Trigger with "/software-requirement-specification-doc",
  "create an SRS for X", "write requirements for this system", "I need a
  requirements spec for...", or whenever requirements for a module, service,
  or system need to be nailed down before design work starts.
---

# /software-requirement-specification-doc

Generate a complete, filled-in Software Requirement Specification (SRS) for a specific module, system, or service — describing what it must do, before any design or implementation work begins.

## Usage

```
/software-requirement-specification-doc $ARGUMENTS
```

Example: `/software-requirement-specification-doc authentication service`

This skill also activates conversationally — e.g. "write the requirements spec for the notification service" or "create an SRS for the inventory system" — without needing the slash form.

## What an SRS Is For (and Isn't)

An SRS is scoped to a **module, system, or service** — not an individual feature or bug fix. It captures what the system must do, how reviewers will know it's done correctly, and what constraints and quality expectations apply. It deliberately avoids implementation details (specific classes, file paths, internal architecture) unless those are hard constraints from existing project documentation.

Implementation belongs in a design document, not here. If the user also wants a design document, point them to the `software-design-doc` skill — or generate the SRS first and offer to follow up with a design doc once requirements are settled.

## When to Use This

Use the full SRS when:
- A new module, system, or service is being specified from scratch
- An existing system is being significantly extended or redesigned
- Requirements are unclear, contested, or missing before design starts
- Stakeholders (BA, PO, QA, dev) need a shared agreement on what's being built

Skip it (or propose a shorter requirement note) when the work is a narrow bug fix, a small isolated feature, or a documentation-only update.

## Workflow at a Glance

```
1. Elicit   →  ask about domain/stack, system scope, stakeholders, constraints, test boundaries
2. Draft    →  fill every section of the SRS using gathered context + reasonable inference
3. Flag     →  mark any field genuinely unknown as TODO, never invent specifics
4. Deliver  →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1 — Elicit Requirements

If the user's request is already detailed (clear scope, known stakeholders, stated constraints), skip straight to drafting and only ask about genuine gaps.

If the request is short — a one-line system or module name — ask a focused round of clarifying questions before drafting. Use `ask_user_input_v0` where questions fit clean multiple-choice options; use plain text for open-ended items like document paths or specific terminology.

Cover these areas:

**Domain & stack**
- What kind of project is this? (web app, backend service, game, mobile app, desktop app, library, other)
- What language/framework/engine is in use?

**System scope**
- What module, system, or service does this document cover, in the user's own words?
- What are the boundaries — what's inside this system vs. handled by a neighboring system?
- What's explicitly out of scope for this SRS?

**Stakeholders**
- Who cares about these requirements: end users, designers, developers, QA, other roles? What does each need from this system?

**Requirement framing**
- Is this system primarily user/player-facing (favors User Stories) or system/workflow-facing (favors Use Cases)? Use the answer to decide which framing to lead with in section 7 — drop the one that doesn't fit.

**Functional behavior**
- What are the must-have behaviors (functional requirements)? What's a nice-to-have vs. a hard requirement?
- Any quality expectations that matter — performance, reliability, usability, accessibility, security, maintainability?

**Data & integration**
- Does this system touch persisted data, configuration, or network/shared contracts?
- Does this system touch external interfaces — input handling, networking, file I/O, platform APIs, backend APIs, editor tooling?

**Constraints**
- Any approved constraints that must not change without sign-off (architecture, dependencies, tech stack, banned/required libraries)?

**Testing**
- What test types are realistically in scope: unit, integration/E2E, manual/exploratory?

Don't force every question if context already answers it. If the user pushes back ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 2 — Draft the Document

Fill in every section using gathered context. Where a domain hint sub-bullet doesn't apply to the user's stack, drop it. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics.

Keep functional and non-functional requirements implementation-free: describe behavior and observable outcomes, not classes, files, or internal structure. If a requirement can't be tested or observed as written, rewrite it until it can.

### Document Template

```markdown
# Software Requirement Specification: [System or Module Name]

## 1. Document Information

| Field | Value |
| --- | --- |
| System or Module | `[system/module/service name]` |
| Author | `[name or agent]` |
| Created Date | `[YYYY-MM-DD]` |
| Last Updated | `[YYYY-MM-DD]` |
| Status | `Draft / In Review / Approved / Superseded` |
| Related Design Document | `[path or link, if any]` |
| Related Task Trace | `[path or link, if any]` |

## 2. Purpose

What module, system, or service this document covers. What decisions this document should help reviewers make. What's out of scope for this requirements document specifically.

## 3. Scope

### 3.1 In Scope
- `[In-scope behavior or requirement]`

### 3.2 Out of Scope
- `[Out-of-scope item]`

## 4. Background and Context

What the system does today (or what gap it fills if new). What is missing, incorrect, confusing, risky, or incomplete. Any known project documents that affect these requirements (list only documents the user actually confirmed exist — do not invent paths).

Relevant documents:
- `[path or link, if the user provided one]`

## 5. Stakeholders and Users

| Stakeholder or User | Need |
| --- | --- |
| `[role, e.g. End User / Player]` | `[what they need]` |
| `[role, e.g. Developer]` | `[what they need]` |
| `[role, e.g. QA/Tester]` | `[what they need to verify]` |

## 6. Definitions and Glossary

| Term | Definition |
| --- | --- |
| `[term]` | `[definition]` |

## 7. User Stories or Use Cases

Use whichever framing fits the system — drop the section that doesn't apply.

### 7.1 User Stories

Use when the system is user/player-facing.

- As a `[type of user]`, I want `[goal]` so that `[benefit]`.

### 7.2 Use Cases

Use when the system is system-facing, workflow-facing, or tool/editor-facing.

| Use Case ID | Actor | Trigger | Expected Result |
| --- | --- | --- | --- |
| `UC-001` | `[actor]` | `[what starts the use case]` | `[expected result]` |

## 8. Functional Requirements

Use clear, testable language: "The system shall..." or "The module shall...".

| Requirement ID | Requirement | Priority | Source | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| `FR-001` | The system shall `[required behavior]`. | `Must / Should / Could` | `[stakeholder/source]` | `[how to verify]` |

## 9. Non-Functional Requirements

| Requirement ID | Category | Requirement | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| `NFR-001` | Performance | `[performance expectation]` | `Must / Should / Could` | `[how to verify]` |
| `NFR-002` | Reliability | `[reliability expectation]` | `Must / Should / Could` | `[how to verify]` |
| `NFR-003` | Usability | `[usability expectation]` | `Must / Should / Could` | `[how to verify]` |

Common categories: Performance, Reliability, Usability, Accessibility, Maintainability, Testability, Security, Compatibility. Only include categories that genuinely matter for this system.

## 10. Data Requirements

Use this section if the system touches runtime state, persisted data, configuration, or network/shared contracts.

| Data Requirement ID | Data | Requirement | Persistence or Serialization Impact |
| --- | --- | --- | --- |
| `DR-001` | `[data name]` | `[what must be stored, read, shown, or transmitted]` | `None / Runtime only / Persisted / Network / Config` |

Data impact checklist:
- Does this system introduce new persisted data? `Yes / No`
- Does this system modify existing persisted data? `Yes / No`
- Does this system require migration? `Yes / No`
- Does this system affect network protocols or shared contracts? `Yes / No`
- Does this system require approval before implementation? `Yes / No`

## 11. UI, UX, and Asset Requirements

Use this section if the system changes user-facing UI, visual feedback, or static assets.
- For web: pages/routes, components, layout
- For backend: API responses/schemas surfaced to consumers, admin UI if any
- For game: scenes/levels, prefabs, animations, audio, HUD
- For mobile/desktop: screens, platform-specific UI conventions

| Requirement ID | Area | Requirement | Acceptance Criteria |
| --- | --- | --- | --- |
| `UX-001` | `[UI/Visual/Audio/Animation]` | `[requirement]` | `[how to verify]` |

Additional notes:
- Required views/screens/scenes: `[names or None]`
- Required components/prefabs/widgets: `[names or None]`
- Required assets: `[names or None]`
- Required text or localization: `[details or None]`

## 12. External Interface Requirements

Use this section if the system touches input handling, networking, file I/O, platform APIs, backend APIs, or editor/tooling interfaces.

| Interface ID | Interface | Requirement | Notes |
| --- | --- | --- | --- |
| `IF-001` | `[input/network/file/editor/platform]` | `[requirement]` | `[notes]` |

## 13. Rules, Constraints, and Standards

List only constraints the user actually confirmed — do not invent project policy.

- `[architecture pattern or convention, if confirmed]`
- `[approved tech stack / required or banned dependencies, if confirmed]`
- Do not change approved architecture, dependencies, or technology stack without explicit approval.

System-specific constraints:
- `[constraint]`

## 14. Assumptions

| Assumption ID | Assumption | Risk if Wrong |
| --- | --- | --- |
| `ASM-001` | `[assumption]` | `[risk]` |

## 15. Dependencies

| Dependency ID | Dependency | Type | Status |
| --- | --- | --- | --- |
| `DEP-001` | `[dependency]` | `System / Service / Asset / Decision / Document` | `Available / Missing / Pending` |

## 16. Acceptance Criteria

- `[Acceptance criterion 1]`
- `[Acceptance criterion 2]`

Example phrasing:
```text
- Given [precondition], when [action], then [expected result].
```

## 17. Requirement Traceability

| Requirement ID | Design Section | Implementation Reference | Test Reference | Status |
| --- | --- | --- | --- | --- |
| `FR-001` | `[design doc section, once it exists]` | `[file/class, later]` | `[test, later]` | `Not Started / In Progress / Done` |

## 18. Testing Expectations

The detailed test plan belongs in the design document; this section states what verification is expected for the system.

| Test Type | Required? | Purpose |
| --- | --- | --- |
| Unit | `Yes / No` | `[what should be verified]` |
| Integration/E2E | `Yes / No` | `[what should be verified]` |
| Manual | `Yes / No` | `[what should be verified]` |

## 19. Open Questions

| Question ID | Question | Owner | Status |
| --- | --- | --- | --- |
| `Q-001` | `[question]` | `[user/agent/reviewer]` | `Open / Answered` |

## 20. Approval

| Reviewer | Decision | Date | Notes |
| --- | --- | --- | --- |
| `[name]` | `Approved / Changes Requested / Rejected` | `[YYYY-MM-DD]` | `[notes]` |
```

---

## Phase 3 — Flag Gaps Honestly

Before presenting the draft, scan for any section filled with a guess rather than something the user stated or that's clearly inferable. Convert genuine guesses into `TODO:` markers. Light structural inferences are fine (e.g. inferring an NFR-Performance row from "this runs on every request") — the line is between reasonable inference and invented specifics like fake stakeholder needs, fictional existing documents, or constraints the user never confirmed.

Pay particular attention to:
- Section 4 (Background and Context) — don't invent "relevant documents" that weren't mentioned.
- Section 13 (Rules, Constraints, and Standards) — don't assume a specific architecture pattern or banned library unless the user confirmed it.
- Section 7 — use only the framing (User Stories or Use Cases) that matches what the user confirmed about this system; don't fill both just to seem thorough.

---

## Phase 4 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Write the filled document directly as a `.md` file |
| **DOCX** | Read `/mnt/skills/public/docx/SKILL.md` before generating — follow its formatting and table guidance |

Save the file to `/mnt/user-data/outputs/`, then use `present_files` to share it. Use the system/module name for the filename, e.g. `authentication-service-srs.md`.

Keep the chat response brief: a short note on what was filled vs. flagged as TODO, then the file.

If the user seems likely to want a design document next, mention that the `software-design-doc` skill can pick up from this SRS once requirements are settled — but don't generate one unprompted.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Every section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Document title and section 1 say "module/system/service", not "feature" or "task"
- [ ] Requirements are testable/observable, not implementation descriptions (no class names, file paths, or internal structure in sections 8–9)
- [ ] Domain hint sub-bullets that don't apply to this stack have been removed
- [ ] Section 7 uses only the framing (User Stories or Use Cases) that fits this system, not both by default
- [ ] No external doc paths, architecture patterns, or process references are hardcoded from a different project
- [ ] Document is internally consistent (requirement IDs in section 17 match those defined in sections 8–9)
