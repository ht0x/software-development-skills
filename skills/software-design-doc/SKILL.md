---
name: software-design-doc
description: >-
  PRIMARY PURPOSE: work through a large module or task and align dev, QA,
  DevOps, and PM before implementation. Written primarily for Team Leads
  and Tech Leads. Generates a filled-in software design document. Works
  across domains (web, backend, game, mobile, desktop). Trigger with
  "/software-design-doc", "create a design doc for X", "write a design
  document for this feature", "I need a SDD for...", or whenever a task is
  large enough to need cross-functional alignment before coding starts. Not
  needed for small tasks like a narrow bug fix, typo fix, or localized doc
  update — propose a lighter alternative for those instead.
---

# /software-design-doc

Generate a complete, filled-in Software Design Document (SDD) for a specific feature or task, ready to use for design review before implementation.

## Usage

```
/software-design-doc $ARGUMENTS
```

Example: `/software-design-doc water crop in 2D farming game`

This skill also activates conversationally — e.g. "write a design doc for the password reset flow" — without needing the slash form.

## When to Use This vs a Lighter Alternative

Use the full document when the task is medium to large: it touches multiple systems or layers, introduces a new feature, or the user explicitly asks for design review before implementation.

Skip it, or propose something shorter, when the task is a narrow bug fix, a typo fix, or a localized documentation update. If the user invokes this skill for something that small, say so and offer a 3-5 bullet summary instead — then proceed only if they confirm they still want the full document.

## Workflow at a Glance

```
1. Elicit   →  ask about domain/stack, scope, related docs, constraints, approval-sensitive areas
2. Draft    →  fill every section of the SDD using gathered context + reasonable inference
3. Flag     →  mark any field that's still genuinely unknown as a TODO, never invent specifics
4. Deliver  →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1 — Elicit Requirements

If the user's request is already detailed (clear problem statement, known files/modules, stated constraints), skip straight to drafting and only ask about genuine gaps.

If the request is short — a one-line feature name or task description, e.g. "water crop in 2D farming game" — ask a full round of clarifying questions before drafting. Use `ask_user_input_v0` where the questions fit clean multiple-choice options; use plain text questions for open-ended items like file paths.

Cover these areas:

**Document metadata**
- Do they have a Task ID and related task/requirements/ADR document links to include?

**Domain & stack**
- What kind of project is this? (web app, backend service, game, mobile app, desktop app, library, other)
- What language/framework/engine is in use?

**Scope**
- What is the problem or gap this task addresses, in the user's own words?
- What's explicitly out of scope (non-goals)?
- How will they know the design is acceptable (success criteria)?

**Current system**
- Which existing files, modules, or systems does this touch? (ask for paths if known)
- Any existing architecture pattern or convention to follow (e.g. layered architecture, MVC, MVP, feature-first, clean architecture)?

**Design approach**
- Did they already settle on one approach, or are there alternatives worth comparing (e.g. a simpler-but-slower option, a different library/pattern)? If they only have one approach in mind, it's fine to leave Alternatives Considered thin or skip it — don't invent rejected alternatives just to fill the table.
- Any known trade-off they're consciously accepting (e.g. simplicity over performance, speed of delivery over flexibility)?

**Constraints**
- Any approved constraints that must not change without sign-off (architecture, dependencies, data format, tech stack)?
- Any data, serialization, or persistence impact (save files, database schema, network contracts, config formats)?
- Does the design touch any approval-sensitive areas: new packages/plugins, architecture/ADR changes, save data or migration, shared contracts, file/asset moves, or large refactors outside the task scope?

**Integration**
- Does this interact with other features/systems/teams? Through what kind of interface (API, event, shared module, message queue)?

Don't force every question if context already answers it — only chase what's genuinely missing. If the user pushes back on answering everything ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 2 — Draft the Document

Fill in every section below using gathered context. Where a domain hint sub-bullet doesn't apply to the user's stack, drop it rather than leaving it as noise. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics — fabricated detail is worse than an honest gap.

### Document Template

The template to fill in follows. Output it as a `.md` file with all placeholders replaced.

```markdown
# Software Design Document: [Feature Name]

## 1. Document Information

| Field | Value |
| --- | --- |
| Task ID | `[task-id]` |
| Feature Name | `[feature-name]` |
| Document Name | `[task-id]-software-design-document.md` |
| Author | `[name or agent]` |
| Created Date | `[YYYY-MM-DD]` |
| Last Updated | `[YYYY-MM-DD]` |
| Status | `Draft / In Review / Approved / Superseded` |
| Related Task Document | `[path or link]` |
| Related Requirements Doc | `[path or link, if any]` |
| Related ADR or Architecture Doc | `[path or link, if any]` |

## 2. Design Context

### 2.1 Problem Statement

Describe the design problem in plain language.

Write:
- What currently does not exist, does not work, or needs to change.
- Who or what is affected.
- Why a design decision is needed before implementation.

[Problem statement]

### 2.2 Design Goals

List what the design must achieve.

- `[Design goal 1]`
- `[Design goal 2]`
- `[Design goal 3]`

### 2.3 Design Non-Goals

List related problems this design intentionally does not solve.

- `[Non-goal 1]`
- `[Non-goal 2]`

### 2.4 Design Success Criteria

Define how reviewers will know the design is acceptable.

- `[Observable design quality, constraint, or review outcome]`
- `[Observable design quality, constraint, or review outcome]`

## 3. Requirement Context

Summarize only the requirements that affect the design. Keep the full requirement list in the requirements or task document.

| Requirement ID | Design-Relevant Summary | Priority | Design Impact |
| --- | --- | --- | --- |
| `REQ-001` | `[summary]` | `Must / Should / Could` | `[why this affects the design]` |
| `REQ-002` | `[summary]` | `Must / Should / Could` | `[why this affects the design]` |

## 4. Current System Analysis

### 4.1 Relevant Files and Systems

List the existing files, modules, classes, scenes, prefabs, assets, or systems that shape the design.

| Area | Path or Name | Current Responsibility | Design Relevance |
| --- | --- | --- | --- |
| `[Module/System]` | `[path or name]` | `[what it does today]` | `[why it matters]` |

### 4.2 Current Behavior

Describe the current behavior that the proposed design must preserve, replace, or extend.

- `[Current behavior 1]`
- `[Current behavior 2]`

### 4.3 Constraints

List constraints from existing architecture, conventions, tooling, data formats, scenes, assets, or runtime requirements.

- Follow the project's existing architecture pattern: `[pattern or path]`.
- Follow established coding conventions: `[path or Not Documented]`.
- Follow existing data, serialization, or storage conventions: `[path or Not Applicable]`.
- Follow existing testing conventions: `[path or Not Documented]`.
- Do not change approved architecture, dependencies, storage strategy, networking contracts, or technology stack without explicit approval.
- `[Additional constraint]`

### 4.4 Assumptions

List assumptions the design depends on.

- `[Assumption 1]`
- `[Assumption 2]`

## 5. Proposed Design

### 5.1 Design Overview

Explain the proposed solution in a short narrative.

Write:
- Which module, component, scene, prefab, asset, or layer owns the new behavior.
- Which layer handles which responsibility.
- How the change fits into the existing system.
- What behavior or structure changes from the current system.

[Design overview]

### 5.2 Component Ownership

| Responsibility | Owning Module, Layer, or Asset | Reason |
| --- | --- | --- |
| `[responsibility]` | `[owner]` | `[why this owner is correct]` |

### 5.3 Architecture Fit

Describe how the design follows the project's expected architecture flow. Adapt the generic flow below to the actual architecture.

[Input/Event]
  -> [Coordinating Layer]
  -> [Domain/Business Logic]
  -> [Data/Persistence/Infrastructure if needed]
  -> [Presentation/UI/Scene result]

Architecture notes:
- `[How this follows existing architecture]`
- `[Any approved exception or deviation]`

### 5.4 Components to Add or Modify

| Component | Path or Name | Add/Modify | Design Responsibility |
| --- | --- | --- | --- |
| `[Class/File/Scene/Prefab/Asset]` | `[path or name]` | `Add / Modify` | `[responsibility]` |

### 5.5 Data Design

Use this section if the task touches runtime state, persisted data, configuration, network payloads, ScriptableObjects, save data, or any serialized format.

| Data Object | Type | Owner | Serialized? | Notes |
| --- | --- | --- | --- | --- |
| `[name]` | `Runtime / Persisted / Config / Network / Asset` | `[module]` | `Yes / No` | `[notes]` |

Serialization/storage impact:

- Does this change persisted data structures? `Yes / No`
- Does this require migration? `Yes / No`
- Does this affect external contracts such as APIs, file formats, or network protocols? `Yes / No`
- Required approval or documentation: `[details]`

### 5.6 API, Events, and Integration Points

List public methods, interfaces, events, messages, asset references, scene links, or cross-module calls introduced or affected.

| Integration Point | Direction | Purpose | Notes |
| --- | --- | --- | --- |
| `[method/event/interface/reference]` | `[caller -> callee]` | `[purpose]` | `[notes]` |

### 5.7 UI, Scene, Prefab, and Asset Impact

Use this section if user-facing or editor-facing elements are affected.

- Screens/views/scenes affected: `[paths or None]`
- Prefabs affected: `[paths or None]`
- ScriptableObjects or assets affected: `[paths or None]`
- Reusable UI components or controls affected: `[paths or None]`
- Tooling or editor support needed: `[Yes / No, details]`

### 5.8 Error Handling and Edge Cases

List important edge cases and how the design handles them.

| Case | Expected Handling | Owner |
| --- | --- | --- |
| `[edge case]` | `[handling]` | `[component/module]` |

### 5.9 Performance Considerations

Describe expected performance risks and mitigations.

- Runtime frequency: `[per frame / per action / on load / rare]`
- Expected data size: `[small / medium / large / unknown]`
- Main risk: `[risk]`
- Mitigation: `[mitigation]`
- Verification approach: `[what should be checked during implementation/testing]`

## 6. Alternatives Considered

Describe other approaches that were evaluated and why they were not chosen. This section shows the reasoning behind the chosen design, not just the conclusion.

| Alternative | Description | Why Not Chosen |
| --- | --- | --- |
| `[Alternative 1]` | `[brief description]` | `[reason rejected]` |
| `[Alternative 2]` | `[brief description]` | `[reason rejected]` |

## 7. Trade-offs and Risks

State what is being sacrificed by this design, in addition to what could go wrong.

Trade-offs:

- `[Trade-off 1]`
- `[Trade-off 2]`

| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| `[risk]` | `Low / Medium / High` | `Low / Medium / High` | `[mitigation]` |

## 8. Approval-Sensitive Design Changes

Mark whether the proposed design touches areas that require explicit approval before implementation.

| Area | Needed? | Notes |
| --- | --- | --- |
| New package, dependency, or plugin | `Yes / No` | `[notes]` |
| Architecture or ADR change | `Yes / No` | `[notes]` |
| Save data, serialization, or migration | `Yes / No` | `[notes]` |
| SharedContracts, networking, or API contract | `Yes / No` | `[notes]` |
| File, folder, scene, prefab, or asset move | `Yes / No` | `[notes]` |
| Large refactor outside local task scope | `Yes / No` | `[notes]` |

## 9. Open Design Questions

List unresolved design questions that need input before implementation can proceed safely.

| Question | Owner | Needed By | Status |
| --- | --- | --- | --- |
| `[question]` | `[name/role]` | `[date or milestone]` | `Open / Answered` |

## 10. Design Approval

| Reviewer | Decision | Date | Notes |
| --- | --- | --- | --- |
| `[name]` | `Approved / Changes Requested / Rejected` | `[YYYY-MM-DD]` | `[notes]` |
```

---

## Phase 3 — Flag Gaps Honestly

Before presenting the draft, scan it for any section that was filled with a guess rather than something the user actually stated or that's clearly inferable from context. Convert genuine guesses into `TODO:` markers instead of presenting them as settled facts. It's fine to make light structural inferences — the line is between reasonable inference and invented specifics like fake file paths, fictional existing systems, or made-up rejected alternatives in section 6. If no real alternatives were discussed, leave that table as `TODO: confirm if other approaches were considered` rather than fabricating plausible-sounding ones.

---

## Phase 4 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Write the filled document directly as a `.md` file |
| **DOCX** | Read the docx SKILL.md before generating — follow its formatting and table guidance |

Save the file to the outputs folder, then use `present_files` to share it. Use the task/feature name for the filename, e.g. `water-crop-design-doc.md`.

Keep the chat response brief: a short note on what was filled vs. what's flagged as TODO, then the file. Don't restate the whole document inline if it's already being delivered as a file.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Every section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Domain hint sub-bullets that don't apply to this stack have been removed, not left as dead placeholders
- [ ] No external doc paths or process references are hardcoded from a different project than the user's
- [ ] Approval-Sensitive Design Changes (section 8) is filled in, not left as all placeholder values
- [ ] Document is internally consistent (component names in section 5.4 match references elsewhere)
- [ ] Related document links in section 1 are filled in or marked `TODO` — not silently omitted
