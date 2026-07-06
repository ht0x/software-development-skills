---
name: spec-driven-development-doc
description: >-
  PRIMARY PURPOSE: write implementation specs clearly enough — behavior,
  constraints, testable outcomes — before code starts, which is especially
  valuable when working with AI agents, junior developers, or a large team.
  Generates a filled-in Spec-Driven Development document. May be called by
  other names: feature spec, implementation plan, dev note, ticket
  breakdown. Works across domains (web, backend, game, mobile, desktop).
  Trigger with "/spec-driven-development-doc", "break this into
  implementation specs", "write a feature spec for X", "create a dev note
  / ticket breakdown for Y", "I need an implementation tracking doc for...",
  or whenever requirements/design need to become trackable, testable
  implementation work. Not needed for small tasks like a narrow bug fix or
  documentation-only update — propose a shorter checklist instead.
disable-model-invocation: true
---

# /spec-driven-development-doc

Generate a complete, filled-in Spec-Driven Development document — the bridge between approved requirements/design and actual implementation, broken into small, testable, trackable specs.

## Usage

```
/spec-driven-development-doc $ARGUMENTS
```

Example: `/spec-driven-development-doc water crop in 2D farming game`

This skill also activates conversationally — e.g. "break the password reset feature into implementation specs" — without needing the slash form.

## What This Document Is For (and Isn't)

This document answers a different question than the other two design documents in this family:

- A System Requirements Specification (`system-requirements-specification-doc`) defines **what** the system must do.
- A Software Design Document (`software-design-doc`) defines **how** the system should be designed.
- This Spec-Driven Development document defines **how the work will be implemented, verified, tracked, and reviewed**, in small steps.

It is a planning and execution document, not a replacement for either of the other two. If requirements or design aren't settled yet, point the user to those skills first — this document works best once there's something concrete to break down.

## When to Use This vs a Lighter Alternative

Use the full document when there's a real body of approved (or at least drafted) requirements/design to translate into implementation work — typically medium-to-large tasks spanning multiple specs or phases.

Skip it, or propose something shorter, for a narrow bug fix or documentation-only update. If the user invokes this skill for something that small, say so and offer a short checklist instead — then proceed only if they confirm they still want the full document.

## Workflow at a Glance

```
1. Source check  →  confirm whether SRS/SDD already exist; pull from them or proceed with verbal scope
2. Elicit        →  ask mainly about spec breakdown, scope, approval-sensitive areas, test boundaries
3. Draft         →  fill every section, creating one SPEC-XXX subsection per implementation unit
4. Flag          →  mark any field that's still genuinely unknown as a TODO, never invent specifics
5. Deliver       →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1 — Check for Source Documents

Before asking implementation questions, find out what this is building on:

- Ask whether a System Requirements Specification and/or Software Design Document already exist for this feature.
- If yes: ask the user to paste the relevant content, upload the file, or summarize the key requirements/design decisions. Use that as the actual source for section 3 (Source Documents) and section 5 (Requirement-to-Spec Breakdown) — don't re-derive requirements from scratch if they're already stated elsewhere.
- If no: proceed using whatever scope the user describes verbally. Mark the relevant rows in section 3 as `Not Required` rather than inventing a path to a document that doesn't exist, and note in section 2 (Purpose) that this plan is based on verbally-described scope rather than a formal requirements/design doc.

Don't block on this — if the user doesn't have formal docs and just wants to move forward, proceed with what they give you.

---

## Phase 2 — Elicit Implementation Details

This skill assumes requirements and design intent are largely already known (from Phase 1, or from earlier in the same conversation). The elicitation here is lighter than the SRS/SDD skills — focus mainly on how the work should be broken down and tracked, not on re-establishing what the feature is.

If the user's request is already detailed (clear requirement list, known components, stated approval-sensitive areas), skip straight to drafting and only ask about genuine gaps.

Cover these areas:

**Spec breakdown**
- How many distinct implementation specs make sense for this work? If the user doesn't know, infer a reasonable breakdown from the requirements/scope discussed (e.g. one spec per major behavior or component) and confirm it with them before drafting all of section 6.
- Are there natural phase boundaries (e.g. data layer first, then logic, then UI)?

**Scope**
- What implementation work is explicitly in scope vs. out of scope for this task?

**Approval-sensitive areas**
- Does this touch dependencies, architecture, persisted/save data, network protocols or external contracts, file/folder moves, or large refactors? Any of these should be flagged as requiring explicit approval before implementation.

**Testing**
- What test types are realistically in scope per spec: unit, integration/E2E, manual?

Don't force every question if context already answers it. If the user pushes back on answering everything ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 3 — Draft the Document

Fill in every section using gathered context. Create one `SPEC-XXX` subsection in section 6 per implementation unit agreed on in Phase 2 — don't pad with filler specs to look thorough, and don't collapse multiple distinct behaviors into one oversized spec. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics.

### Document Template

```markdown
# Spec-Driven Development: [Feature Name]

## 1. Document Information

| Field | Value |
| --- | --- |
| Task ID | `[task-id]` |
| Feature Name | `[feature-name]` |
| Author | `[name or agent]` |
| Created Date | `[YYYY-MM-DD]` |
| Last Updated | `[YYYY-MM-DD]` |
| Status | `Draft / In Progress / In Review / Completed / Superseded` |
| Related Requirements Doc | `[path or link, if any]` |
| Related Design Document | `[path or link, if any]` |

## 2. Purpose

What approved (or verbally-described) requirements or design this document turns into implementation work. What level of tracking is needed for this task. Which parts of the work must be reviewed before continuing.

## 3. Source Documents

| Source | Path or Link | Status | Notes |
| --- | --- | --- | --- |
| Requirements | `[path, or "Not Required" if verbal-only]` | `Draft / Approved / Not Required` | `[notes]` |
| Software Design | `[path, or "Not Required" if verbal-only]` | `Draft / Approved / Not Required` | `[notes]` |
| Task Description | `[path or summary]` | `Draft / Approved / Not Required` | `[notes]` |

## 4. Development Scope

### 4.1 In Scope
- `[Implementation scope item]`
- `[Implementation scope item]`

### 4.2 Out of Scope
- `[Out-of-scope item]`
- `[Out-of-scope item]`

### 4.3 Approval-Sensitive Areas

| Area | Requires Approval? | Reason |
| --- | --- | --- |
| Dependencies | `Yes / No` | `[reason]` |
| Architecture changes | `Yes / No` | `[reason]` |
| Persisted/save data | `Yes / No` | `[reason]` |
| Network protocols or external contracts | `Yes / No` | `[reason]` |
| File or folder moves | `Yes / No` | `[reason]` |
| Large refactors | `Yes / No` | `[reason]` |

## 5. Requirement-to-Spec Breakdown

Map requirements to concrete implementation specs. Each spec should be small enough to implement, test, and review independently.

| Requirement ID | Requirement Summary | Spec ID | Implementation Spec | Priority |
| --- | --- | --- | --- | --- |
| `REQ-001` | `[requirement summary]` | `SPEC-001` | `[implementation-level spec]` | `Must / Should / Could` |

Guidance: a requirement describes what must be true; a spec describes what implementation work will make it true. Split work when a spec touches multiple systems, layers, or test types.

## 6. Implementation Specs

One subsection per spec agreed on during elicitation.

### SPEC-001: `[Spec Name]`

| Field | Value |
| --- | --- |
| Requirement IDs | `[REQ-001]` |
| Owner Area | `[feature/module/layer]` |
| Status | `Not Started / In Progress / Blocked / Done` |
| Risk Level | `Low / Medium / High` |

#### Objective
`[The implementation result this spec must produce]`

#### Planned Changes

| Component | Path | Add/Modify | Planned Change |
| --- | --- | --- | --- |
| `[component]` | `[path]` | `Add / Modify` | `[change]` |

#### Behavior Rules
- `[Rule 1]`
- `[Rule 2]`

#### Acceptance Checks
- `[Check 1]`
- `[Check 2]`

#### Tests

| Test Type | Test Target | Expected Coverage |
| --- | --- | --- |
| Unit | `[target]` | `[coverage]` |
| Integration/E2E | `[target]` | `[coverage]` |
| Manual | `[workflow]` | `[coverage]` |

#### Notes
- `[Implementation note, constraint, or reviewer comment]`

*(Repeat this SPEC-XXX subsection for each spec identified in section 5.)*

## 7. Implementation Phases

| Phase | Specs Covered | Scope | Done When | Review Required? |
| --- | --- | --- | --- | --- |
| `Phase 1` | `[SPEC-001]` | `[scope]` | `[completion condition]` | `Yes / No` |

Recommended phase pattern:
1. Verify current behavior and relevant files.
2. Implement domain or business rules.
3. Implement coordinating/orchestration logic.
4. Implement presentation, UI, assets, or tooling changes.
5. Add or update tests.
6. Update related documentation.
7. Review, fix findings, and finalize.

## 8. Test Mapping

| Spec ID | Test ID | Test Type | Test Name or Manual Check | Status |
| --- | --- | --- | --- | --- |
| `SPEC-001` | `TEST-001` | `Unit / Integration-E2E / Manual` | `[test name or check]` | `Not Started / In Progress / Done` |

## 9. Traceability Checklist

| Item | Status | Notes |
| --- | --- | --- |
| Requirements reviewed | `Not Started / Done` | `[notes]` |
| Software design reviewed | `Not Started / Done / Not Required` | `[notes]` |
| Specs created for all must-have requirements | `Not Started / Done` | `[notes]` |
| Specs split into reviewable phases | `Not Started / Done` | `[notes]` |
| Tests mapped to specs | `Not Started / Done` | `[notes]` |
| Documentation updated after implementation | `Not Started / Done` | `[notes]` |

## 10. Review Gates

| Gate | When It Happens | Required Evidence | Reviewer |
| --- | --- | --- | --- |
| Design readiness | Before implementation | Requirements and design are clear | `[name/role]` |
| Phase review | After each major phase | Phase output and tests/checks | `[name/role]` |
| Approval-sensitive change | Before modifying restricted areas | User approval | `User` |
| Completion review | Before marking done | Tests, docs, review notes | `[name/role]` |

Approval-sensitive changes include: modifying dependencies, changing approved architecture, changing persisted/save data or migration strategy, changing network protocols or external contracts, moving files/folders without clear approved reason, introducing third-party libraries, large refactors outside task scope.

## 11. Progress Log

| Date | Phase or Spec | Progress | Issues or Decisions |
| --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[phase/spec]` | `[progress]` | `[issue/decision]` |

## 12. Completion Criteria

The task can be considered complete when:
- All must-have specs are implemented.
- Acceptance checks for each spec are complete.
- Required tests or manual checks are complete.
- Approval-sensitive changes were either avoided or explicitly approved.
- Related documentation is updated if system behavior changed.
- Review findings are resolved or documented.

Task-specific completion criteria:
- `[criterion]`

## 13. Lessons Learned

| Lesson | Applies To | Follow-up Needed? |
| --- | --- | --- |
| `[lesson learned]` | `[feature/system/process]` | `Yes / No, details` |

## 14. Open Questions

| Question | Owner | Status |
| --- | --- | --- |
| `[question]` | `[name/role]` | `Open / Answered` |

## 15. Approval

| Reviewer | Decision | Date | Notes |
| --- | --- | --- | --- |
| `[name]` | `Approved / Changes Requested / Rejected` | `[YYYY-MM-DD]` | `[notes]` |
```

---

## Phase 4 — Flag Gaps Honestly

Before presenting the draft, scan it for any section filled with a guess rather than something the user actually stated or that's clearly inferable from context. Convert genuine guesses into `TODO:` markers instead of presenting them as settled facts.

Pay particular attention to:
- Section 3 (Source Documents) — don't invent a path to an SRS/SDD that wasn't confirmed to exist; use `Not Required` honestly when the user said there isn't one.
- Section 4.3 (Approval-Sensitive Areas) — don't mark something `No` just to move faster; if genuinely unsure whether an area is touched, mark it `TODO: confirm` rather than guessing.
- Section 6 — don't fabricate file paths in Planned Changes; if the user didn't give a path, write `TODO: confirm path` instead.

---

## Phase 5 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Read `/mnt/skills/public/md` conventions if relevant, write the filled document directly as a `.md` file |
| **DOCX** | Read `/mnt/skills/public/docx/SKILL.md` before generating — follow its formatting and table guidance |

Save the file to `/mnt/user-data/outputs/`, then use `present_files` to share it. Use the task/feature name for the filename, e.g. `water-crop-spec-driven-dev.md`.

Keep the chat response brief: a short note on what was filled vs. what's flagged as TODO, then the file. Don't restate the whole document inline if it's already being delivered as a file.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Every section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Number of SPEC-XXX subsections matches what was actually agreed on, not padded or collapsed
- [ ] Source Documents table reflects reality — no invented paths for SRS/SDD that don't exist
- [ ] Test types use the generic Unit / Integration-E2E / Manual framing, with irrelevant ones dropped rather than left blank
- [ ] Approval-sensitive areas are genuinely assessed, not defaulted to "No" for speed
- [ ] Document is internally consistent (Spec IDs in section 5 match subsections in section 6, and appear again in section 8)
