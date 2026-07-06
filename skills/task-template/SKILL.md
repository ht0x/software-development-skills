---
name: task-template
description: >-
  PRIMARY PURPOSE: produce a clear, ready-to-start task definition for a
  team member, agent, or yourself — clear enough to start, review, test,
  and finish without guessing. Generates a filled-in task document. Works
  across domains (web, backend, game, mobile, desktop). Trigger with
  "/task-template", "create a task for X", "write a task spec for...",
  "I need a ticket for...", "break this into a task doc", or whenever work
  needs to be handed off (to a teammate, an AI agent, or your future self)
  with explicit scope, requirements, and a definition of done. Scales from
  a short checklist for small fixes to a full multi-section document for
  large or risky work.
disable-model-invocation: true
---

# /task-template

Generate a complete, filled-in task document for a specific piece of work — sized appropriately, ready to hand to a teammate, an agent, or yourself.

## Usage

```
/task-template $ARGUMENTS
```

Example: `/task-template fix null reference crash when closing the inventory panel with no items`

This skill also activates conversationally — e.g. "write a task spec for adding rate limiting to the login endpoint" — without needing the slash form.

## Core Idea: Size Drives Depth

Not every task needs every section. The whole point of this template is to scale: a typo fix should take thirty seconds to spec, a new cross-system feature should not skip risk analysis. Decide the task size early — it determines how much of the rest of this skill actually gets filled in.

| Size | Definition |
| --- | --- |
| **Small** | Typo fix, narrow bug fix, small asset/import/config change, localized documentation update. |
| **Medium** | Changes several files, affects runtime behavior, touches shared modules/schemas/scenes/prefabs/assets, or needs testing/review coordination. |
| **Large** | New feature, cross-system change, architecture decision, data/schema/save-data/networking impact, or work that should be split into phases. |

Each section below is labeled with how much it matters at each size:

| Label | Meaning |
| --- | --- |
| `Required for All` | Fill this for every task, including small fixes. |
| `Recommended for Medium/Large` | Fill this when the task changes multiple files/systems, or needs team coordination. |
| `Required for Medium/Large` | Fill this for medium and large tasks; optional for small tasks unless the task is risky. |
| `Optional` | Fill only when useful. Mark `Not Required` if it doesn't apply. |

If the user invokes this skill for something that's clearly small (a one-line typo fix, a trivial config tweak), don't generate the full 19-section document — fill only the `Required for All` sections plus a short checklist, and say so. Offer to expand to the full document if they want it.

## Workflow at a Glance

```
1. Size      →  determine Small / Medium / Large FIRST — this gates step 2
2. Elicit    →  ask only the question groups that size unlocks
3. Draft     →  fill every applicable section using gathered context + reasonable inference
4. Flag      →  mark any field that's still genuinely unknown as a TODO, never invent specifics
5. Deliver   →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1a — Determine Task Size First

Size must be settled before any other question is asked, because it decides which question groups in Phase 1b are even relevant — there's no point asking about risk mitigation for a typo fix.

Try to infer size from the request itself against the size table above (a one-line bug description usually reads as Small; "add a settings menu" usually reads as Medium; "design the save system" usually reads as Large). If the request is genuinely ambiguous, ask a single dedicated question before anything else, using `ask_user_input_v0`:

- Question: "How big is this task?"
- Options: `Small (typo/narrow fix)`, `Medium (multiple files, runtime behavior)`, `Large (new feature, cross-system, architecture)`

Don't bundle this with other questions — size gates everything downstream, so it needs its own answer before Phase 1b begins. If the user's request already states or strongly implies size (e.g. "quick fix" → Small, "new feature" → Large), skip the question and proceed with the inferred size, but mention the assumption when presenting the draft so they can correct it.

## Phase 1b — Elicit Context, Scoped to That Size

If the request is already detailed (clear description, known files/owner) beyond size, skip straight to drafting and only ask about genuine gaps. Otherwise, ask a focused round of clarifying questions before drafting. Use `ask_user_input_v0` where questions fit clean multiple-choice options; use plain text for open-ended items like file paths or task IDs.

The size from Phase 1a determines which groups below to ask. Skip anything already answered or inferable from the original request.

**Always ask, regardless of size:**
- What needs to be done, and why does it matter?
- What does "done" look like?
- Who is this for — a teammate, an AI coding agent, or yourself? Who owns it, who reviews it?
- What kind of project is this (web, backend, game, mobile, desktop, library, other), and what language/framework/engine?
- What test types are realistic here: unit/EditMode, integration/PlayMode/E2E, manual, review-only?

**Small — stop after the "always ask" group.** Don't ask about background, dependencies, approval-sensitive areas, or risks unless the user's own description already signals one of these is relevant (e.g. they mention touching a shared schema even in a "small" fix — in that case, ask the relevant follow-up from the Medium/Large group below before proceeding).

**Medium and Large — also ask:**
- Current behavior, and what's wrong/missing/unclear about it?
- Which existing files, modules, or systems does this touch?
- Anything explicitly out of scope that someone might accidentally touch?
- Any required documents, decisions, or blocking tasks before work can start?
- Does this touch a new dependency, architecture, save/data schema, shared API/contract, file move, or broad refactor? These typically need explicit approval before implementation.

**Large only — also ask:**
- Should this be split into implementation phases? If so, what's the natural breakpoint between phases?
- Any known risk that could change the approach mid-implementation (e.g. unproven third-party dependency, unclear ownership boundary, performance unknown)?

Don't force every question if context already answers it. If the user pushes back on answering everything ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 2 — Draft the Document

Fill in every applicable section using gathered context. Where a domain-hint sub-bullet doesn't apply to the user's stack (e.g. "scene/prefab" hints for a backend-only task), drop it rather than leaving it as dead placeholder text. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics.

For a **small** task, use only the sections marked `Required for All`, condensed, plus a short checklist in place of Implementation Plan / Review Plan. For **medium/large** tasks, fill the full document below.

### Document Template

```markdown
# Task: [Task Title]

## 1. Task Information — Required for All

| Field | Value |
| --- | --- |
| Task ID | `[task-id]` |
| Task Title | `[short action-focused title]` |
| Feature or Area | `[feature/module/system]` |
| Owner | `[name or agent]` |
| Reviewer | `[name or role]` |
| Created Date | `[YYYY-MM-DD]` |
| Target Date | `[YYYY-MM-DD or Not Set]` |
| Status | `Todo / In Progress / Blocked / In Review / Done / Cancelled` |
| Priority | `Must / Should / Could` |
| Task Size | `Small / Medium / Large` |

## 2. Summary — Required for All

Describe the task in one short paragraph: what needs to be done, why it matters, what result should exist when finished.

```text
[Task summary]
```

## 3. Background — Recommended for Medium/Large

- Current behavior or state: `[what happens today]`
- Problem or missing part: `[what is wrong, unclear, missing, or incomplete]`
- User, player, customer, developer, or system impact: `[who or what is affected]`

For small tasks, one sentence is enough.

## 4. Goals — Required for All

- `[Goal 1]`
- `[Goal 2]`
- `[Goal 3]`

## 5. Non-Goals — Recommended for Medium/Large

- `[Non-goal 1]`
- `[Non-goal 2]`

For small tasks, use this only when there's real risk of someone changing unrelated files or behavior.

## 6. Scope — Required for All

### 6.1 In Scope
- `[In-scope item]`
- `[In-scope item]`

### 6.2 Out of Scope
- `[Out-of-scope item]`
- `[Out-of-scope item]`

For small tasks, this can be a short bullet list. For medium/large, separate in-scope and out-of-scope clearly.

## 7. Requirements — Required for All

Use "Must" for required behavior, "Should" for expected behavior, "Could" for optional behavior.

| ID | Requirement | Priority | Acceptance Criteria |
| --- | --- | --- | --- |
| `REQ-001` | `[required behavior]` | `Must / Should / Could` | `[how to verify]` |
| `REQ-002` | `[required behavior]` | `Must / Should / Could` | `[how to verify]` |

For small tasks, 1-3 bullet requirements are enough if a table feels too heavy.

## 8. Expected Deliverables — Required for All

- Code changes: `[Yes / No, details]`
- Tests: `[Yes / No, details]`
- Documentation: `[Yes / No, details]`
- Asset, schema, config, or data changes: `[Yes / No, details]`
  - For web/backend: migration files, API schema, config files
  - For game: scenes, prefabs, ScriptableObjects, level data
  - For mobile/desktop: platform-specific resources, manifests
- Review report or task process report: `[Yes / No, path]`

## 9. Affected Areas — Required for Medium/Large

List files, folders, systems, or assets likely to be touched.

| Area | Path or Name | Expected Change |
| --- | --- | --- |
| `[system/module]` | `[path or name]` | `Add / Modify / Remove / Unknown` |
| `[system/module]` | `[path or name]` | `Add / Modify / Remove / Unknown` |

For small tasks, include this only if the task depends on a specific file, asset, config, or decision.

## 10. Dependencies and Inputs — Recommended for Medium/Large

- Required documents: `[paths or None]`
- Required assets or data: `[paths/names or None]`
- Required decisions: `[decision needed or None]`
- Blocking tasks: `[task IDs or None]`
- External tools, packages, or services: `[details or None]`

## 11. Approval-Sensitive Changes — Required for Medium/Large

| Area | Needed? | Notes |
| --- | --- | --- |
| New package, dependency, or plugin | `Yes / No` | `[notes]` |
| Architecture or ADR change | `Yes / No` | `[notes]` |
| Data schema, persistence, save data, or migration | `Yes / No` | `[notes]` |
| Shared contracts, networking, or public API | `Yes / No` | `[notes]` |
| File or folder move | `Yes / No` | `[notes]` |
| Large refactor outside local task scope | `Yes / No` | `[notes]` |

For small tasks, use this section only if the task may touch dependencies, architecture, data/persistence, shared contracts, networking, file moves, or broad refactors.

## 12. Implementation Plan — Required for Medium/Large

| Step | Work | Owner | Done When | Status |
| --- | --- | --- | --- | --- |
| `1` | `[investigate current behavior]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |
| `2` | `[implement change]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |
| `3` | `[add or update tests]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |
| `4` | `[update docs or reports]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |
| `5` | `[review and fix findings]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |

For small tasks, a short checklist is enough.

## 13. Testing Plan — Required for All

| Test ID | Test Type | Target | Expected Result | Status |
| --- | --- | --- | --- | --- |
| `TEST-001` | `[Unit/EditMode, Integration/PlayMode, E2E, Manual, Review]` | `[target]` | `[expected result]` | `Todo / Done / Not Required` |
| `TEST-002` | `[Unit/EditMode, Integration/PlayMode, E2E, Manual, Review]` | `[target]` | `[expected result]` | `Todo / Done / Not Required` |

Recommended checks (apply the ones relevant to the stack):
- Read any project-specific testing guideline doc, if one exists, before writing tests.
- Run relevant unit/EditMode tests when changing isolated logic.
- Run relevant integration/PlayMode/E2E tests when changing cross-component, gameplay, scene, prefab, UI, or runtime integration behavior.
- Run manual verification when the task affects runtime behavior, UI flow, scene/prefab loading, or startup/bootstrap behavior.

For small tasks, write only the manual check or test command needed to confirm the fix.

## 14. Review Plan — Required for Medium/Large

- Review type: `Code / Design / Documentation / Manual QA / Full task review`
- Review guideline: `[path or None]`
- Reviewer focus:
  - `[focus area 1]`
  - `[focus area 2]`
  - `[focus area 3]`

For small tasks, this can be replaced by the Definition of Done checklist below.

## 15. Definition of Done — Required for All

- Requirements are implemented or explicitly deferred.
- In-scope deliverables are complete.
- Out-of-scope items were not added silently.
- Tests and manual checks are completed or documented as not required.
- Build/compile errors are resolved.
- Relevant documentation or task reports are updated.
- Review findings are resolved or tracked.
- The final result matches the acceptance criteria.

## 16. Risks and Mitigations — Recommended for Medium/Large

| Risk | Impact | Mitigation |
| --- | --- | --- |
| `[risk]` | `Low / Medium / High` | `[how to reduce or handle the risk]` |

For small tasks, use this only when there's uncertainty that could change the solution.

## 17. Open Questions — Optional

| Question | Owner | Answer or Decision | Status |
| --- | --- | --- | --- |
| `[question]` | `[name]` | `[answer]` | `Open / Answered` |

## 18. Related Documents — Recommended for Medium/Large

| Document | Path or Link | Status |
| --- | --- | --- |
| System Requirements Specification | `[path or Not Required]` | `Draft / Approved / Not Required` |
| Software Design Document | `[path or Not Required]` | `Draft / Approved / Not Required` |
| Spec-Driven Development Plan | `[path or Not Required]` | `Draft / In Progress / Not Required` |
| Task Process Report | `[path or Not Required]` | `In Progress / Completed / Not Required` |

For small tasks, include only direct links to references if needed.

## 19. Progress Log — Optional

| Date | Update | Blockers or Decisions |
| --- | --- | --- |
| `[YYYY-MM-DD]` | `[progress update]` | `[blocker/decision or None]` |
```

---

## Phase 3 — Flag Gaps Honestly

Before presenting the draft, scan it for any field filled with a guess rather than something the user actually stated or that's clearly inferable from context (e.g. an assumed file path, an assumed test framework). Convert genuine guesses into `TODO:` markers instead of presenting them as settled facts. Light structural inference is fine (e.g. inferring "this needs an integration test" from "touches two systems") — the line is between reasonable inference and invented specifics like fake paths, fictional existing systems, or made-up reviewers.

---

## Phase 4 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Read `/mnt/skills/public/md` conventions if relevant, write the filled document directly as a `.md` file |
| **DOCX** | Read `/mnt/skills/public/docx/SKILL.md` before generating — follow its formatting and table guidance |

Save the file to `/mnt/user-data/outputs/`, then use `present_files` to share it. Use the task title for the filename, e.g. `fix-inventory-panel-crash-task.md`.

Keep the chat response brief: a short note on the chosen size and what's flagged as TODO, then the file. Don't restate the whole document inline if it's already delivered as a file.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Task size was determined and the right amount of detail was filled in for that size
- [ ] Every applicable section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Domain-hint sub-bullets that don't apply to this stack have been removed, not left as dead placeholders
- [ ] No external doc paths or process references are hardcoded from a different project than the user's
- [ ] Test plan matches what the user said is realistically testable for their stack
- [ ] Document is internally consistent (paths/owners referenced in one section match elsewhere)
