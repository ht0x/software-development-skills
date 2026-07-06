---
name: task-process-report-doc
description: >-
  PRIMARY PURPOSE: track how a task was implemented from planning through
  review — a living document covering starting context, scope, workflow
  checklist, implementation phases, testing, review findings, and lessons
  learned. Generates a filled-in task process report document. Works across
  domains (web, backend, game, mobile, desktop). Trigger with
  "/task-process-report-doc", "create a process report for X", "write a
  task trace for...", "I need a task process report", "start tracking my
  implementation of...", "document how this task was implemented", or
  whenever a medium or large task needs its implementation history captured.
  Not needed for small tasks unless explicitly requested.
disable-model-invocation: true
---

# /task-process-report-doc

Generate a filled-in task process report — a living document that tracks how a task was planned, implemented, tested, reviewed, and closed, capturing decisions, blockers, and lessons learned for future reference.

## Usage

```
/task-process-report-doc $ARGUMENTS
```

Example: `/task-process-report-doc PROJ-42 add rate limiting to the login endpoint`

This skill also activates conversationally — e.g. "write a task process report for the inventory refactor" or "create a task trace for PROJ-12" — without needing the slash form.

## Core Idea: Size Drives Which Sections Are Required

| Size | Definition |
| --- | --- |
| **Small** | Typo fix, narrow bug fix, small config/asset change, localized doc update. |
| **Medium** | Changes several files, affects runtime behavior, touches shared modules/schemas/assets, or needs testing/review coordination. |
| **Large** | New feature, cross-system change, architecture decision, data/schema/persistence impact, or phased work. |

| Label | Meaning |
| --- | --- |
| `Required for Medium/Large` | Fill for medium and large tasks. Optional for small tasks unless explicitly requested. |
| `Required When Applicable` | Fill when the task touches the described area. |
| `Optional` | Fill only when useful. Mark `Not Required` if it does not apply. |

For **small tasks**: this report is optional. If requested, fill only Report Information, Task Summary, Testing Report, and Final Outcome.
For **medium/large tasks**: create this document before implementation starts and update it continuously.

## Workflow at a Glance

```
1. Elicit   →  ask task size FIRST, then gather task ID/title/owner/domain/stack
2. Plan     →  propose which sections to fill vs skip, based on size; confirm with user
3. Confirm  →  wait for explicit approval before generating
4. Draft    →  fill the full report using gathered context; mark unknowns as TODO
5. Deliver  →  ask Markdown or DOCX, save to outputs, present file
```

**Rule**: Steps 2 and 3 are never skipped. The user must approve the section plan before the document is generated.

---

## Phase 1 — Elicit

### 1.1 Determine task size first

Task size gates which sections are required. Ask this as the very first question if not already clear from the user's message, using `ask_user_input_v0`:

- Question: "What is the task size?"
- Options: `Small (narrow fix/doc update)`, `Medium (multiple files, runtime behavior)`, `Large (new feature, cross-system, phased work)`

If size is already obvious from the user's message (e.g. "new authentication system" → Large), infer it and state the assumption.

### 1.2 Gather remaining context

After size is confirmed, ask only what is genuinely missing. Skip anything already stated or inferable.

**Always gather:**
- Task ID and title (e.g. `PROJ-42`, "Add rate limiting to login endpoint")
- Owner (who implements it) and reviewer (who reviews it)
- What kind of project: web, backend, game, mobile, desktop, library?
- What language/framework/engine is in use?

**For Medium/Large — also gather:**
- What is the task supposed to accomplish? Why is it needed?
- What is the current behavior before this task?
- Which files, modules, or systems are expected to be touched?
- Are there any blocking tasks or required decisions before work can start?
- Does this task touch approval-sensitive areas (new dependencies, architecture changes, data/schema changes, shared API contracts, file moves, broad refactors)?
- What test types are realistic: unit/integration/E2E, manual, review-only?
  - For Unity: EditMode / PlayMode tests, Unity Editor verification
  - For web: Jest / Cypress / Playwright / Postman
  - For mobile/desktop: device/emulator manual checks

Use `ask_user_input_v0` for multi-choice questions (domain, test types). Use plain text for task ID, title, and open-ended context.

---

## Phase 2 — Propose Section Plan

After eliciting, present a concise section plan before generating anything.

List each of the 19 sections with its fill status based on the task size:

```
Section 1  — Report Information          → Fill (Required for Medium/Large)
Section 2  — Task Summary                → Fill (Required for Medium/Large)
Section 3  — Workflow Checklist          → Fill (Required for Medium/Large)
Section 4  — Starting Context            → Fill (Required for Medium/Large)
Section 5  — Scope Confirmation          → Fill (Required for Medium/Large)
Section 6  — Approval-Sensitive Areas    → Fill (Required for Medium/Large)
Section 7  — Implementation Phases       → Fill (Required for Medium/Large)
Section 8  — Progress Log                → Fill (Required for Medium/Large) [update continuously]
Section 9  — Files Changed               → Fill (Required for Medium/Large)
Section 10 — Design and Implementation Decisions → Fill (Required for Medium/Large)
Section 11 — Issues, Blockers, Resolutions → Fill if any issues arise (Required When Applicable)
Section 12 — Testing Report              → Fill (Required for Medium/Large)
Section 13 — Runtime Verification        → Fill if runtime behavior changes (Required When Applicable)
Section 14 — Review Report               → Fill (Required for Medium/Large)
Section 15 — Documentation Updates       → Fill (Required for Medium/Large)
Section 16 — Final Outcome               → Fill (Required for Medium/Large)
Section 17 — Lessons Learned             → Fill (Required for Medium/Large)
Section 18 — Feedback Memory             → Fill if a project constraint was almost violated (Required When Applicable)
Section 19 — Approval and Sign-off       → Fill (Required for Medium/Large)
```

For **small tasks**, show a condensed plan covering only sections 1, 2, 12, and 16.

Note any domain-specific rows that will be adapted (e.g. "Section 13 will use web-specific checks since you're on a Next.js project").

End with:
> **Ready to generate the report with this plan?** Reply "yes" or "go ahead" to proceed, or tell me what to change.

Do not generate any document content yet.

---

## Phase 3 — Await Confirmation

Wait for explicit confirmation before proceeding: "yes", "go ahead", "looks good", "do it", or similar.

If the user requests changes, update the plan and re-present it. Repeat until confirmed.

---

## Phase 4 — Draft the Document

Generate the full report using the approved plan. Fill every applicable section with gathered context. For fields that are genuinely unknown, write `TODO: [what's needed]` — never invent specifics like fake file paths, commit hashes, or reviewer names.

### Document Template

````markdown
# Task Process Report: [Task Title]

> This document tracks how the task was implemented from planning through review.
> Update it continuously during implementation — do not fill it in retrospectively all at once.
> Related workflow doc: `[path to your project's workflow/agent doc, or None]`

## Section Requirement Guide

| Label | Meaning |
| --- | --- |
| `Required for Medium/Large` | Fill for medium and large tasks. Optional for small tasks unless requested. |
| `Required When Applicable` | Fill when the task touches the described area. |
| `Optional` | Fill only when useful. Mark `Not Required` if it does not apply. |

---

## 1. Report Information — Required for Medium/Large

| Field | Value |
| --- | --- |
| Task ID | `[task-id]` |
| Task Title | `[task-title]` |
| Feature or Area | `[feature/module/system]` |
| Report Name | `[task-id]-task-process-report.md` |
| Owner | `[name or agent]` |
| Reviewer | `[name or role]` |
| Created Date | `[YYYY-MM-DD]` |
| Last Updated | `[YYYY-MM-DD]` |
| Status | `Draft / In Progress / Blocked / In Review / Completed / Superseded` |
| Task Size | `Small / Medium / Large` |
| Related Task Document | `[path or link]` |
| Related Requirements Doc | `[path or Not Required]` |
| Related Design Document | `[path or Not Required]` |
| Related Spec-Driven Development Doc | `[path or Not Required]` |

## 2. Task Summary — Required for Medium/Large

Summarize the task: what it was supposed to accomplish, why it was needed, and what the final implementation changed.

```text
[Task summary]
```

## 3. Workflow Checklist — Required for Medium/Large

Track the key workflow steps from project start to completion. Adapt paths and steps to your project's actual conventions.

| Step | Required Action | Status | Evidence or Notes |
| --- | --- | --- | --- |
| `1` | Read project git/branching workflow doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `2` | Read project serialization or data guideline: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `3` | Read project coding convention doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `4` | Read project development cycle doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `5` | Read project testing guideline doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `6` | Analyze task size and required documentation | `Todo / Done` | `[Small / Medium / Large, reason]` |
| `7` | Create or update SRS, SDD, spec, or approved alternative | `Todo / Done / Not Required` | `[paths or notes]` |
| `8` | Implement subtasks or phases | `Todo / In Progress / Done` | `[notes]` |
| `9` | Write or update tests | `Todo / Done / Not Required` | `[notes]` |
| `10` | Run automated tests | `Todo / Passed / Failed / Not Required` | `[command/result]` |
| `11` | Run integration or E2E tests | `Todo / Passed / Failed / Not Required` | `[command/result]` |
| `12` | Verify runtime behavior manually | `Todo / Passed / Failed / Not Required` | `[what was checked]` |
| `13` | Read project review guideline doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `14` | Complete review and fixes | `Todo / In Progress / Done` | `[findings/fixes]` |
| `15` | Update architecture or feature map doc: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |
| `16` | Update project phase or progress report: `[path or None]` | `Todo / Done / Not Required` | `[notes]` |

## 4. Starting Context — Required for Medium/Large

| Area | Details |
| --- | --- |
| Initial problem | `[what is missing, broken, or needed]` |
| Existing behavior | `[how the system behaves before this task]` |
| Relevant files or folders | `[paths]` |
| Relevant assets or data | `[paths or names]` — for game: scenes/prefabs/ScriptableObjects; for web/backend: schemas/migrations/configs; for mobile/desktop: manifests/resources |
| Dependencies or blockers | `[dependencies/blockers or None]` |
| Assumptions | `[assumptions made before starting]` |

## 5. Scope Confirmation — Required for Medium/Large

### 5.1 In Scope

- `[In-scope item]`

### 5.2 Out of Scope

- `[Out-of-scope item]`

### 5.3 Scope Changes During Implementation

| Date | Change | Reason | Approved By |
| --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[scope change]` | `[reason]` | `[name or Not Required]` |

## 6. Approval-Sensitive Areas — Required for Medium/Large

| Area | Touched? | Approval Required? | Approval Status | Notes |
| --- | --- | --- | --- | --- |
| New package, library, or dependency | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[package manager file: e.g. package.json, Packages/manifest.json, requirements.txt]` |
| Approved technology stack | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[list approved tools for this project]` |
| Architecture or ADR change | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[ADR reference or None]` |
| File or folder moves | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[notes]` |
| Data schema, serialization, or migration | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[notes]` |
| Shared API contract or network protocol | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[notes]` |
| Coding conventions, workflows, or testing standards | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[notes]` |
| Large refactor outside task scope | `Yes / No` | `Yes / No` | `Pending / Approved / Not Required` | `[notes]` |

## 7. Implementation Phases — Required for Medium/Large

| Phase | Planned Work | Owner | Status | Started | Completed | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `Phase 1` | `[planned work]` | `[name]` | `Todo / In Progress / Blocked / Done` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[commit/path/test/manual evidence]` |
| `Phase 2` | `[planned work]` | `[name]` | `Todo / In Progress / Blocked / Done` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[commit/path/test/manual evidence]` |

## 8. Progress Log — Required for Medium/Large

Update this section continuously during implementation. Keep entries short and factual.

| Date | Phase or Area | Progress | Blockers, Decisions, or Notes |
| --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[phase/area]` | `[what changed]` | `[blocker/decision/note or None]` |

## 9. Files Changed — Required for Medium/Large

| Path | Change Type | Reason |
| --- | --- | --- |
| `[path]` | `Add / Modify / Delete / Move` | `[why this file changed]` |

## 10. Design and Implementation Decisions — Required for Medium/Large

| Decision ID | Date | Decision | Reason | Impact |
| --- | --- | --- | --- | --- |
| `DEC-001` | `[YYYY-MM-DD]` | `[decision]` | `[reason]` | `[impact]` |

## 11. Issues, Blockers, and Resolutions — Required When Applicable

| Issue ID | Date Found | Issue or Blocker | Impact | Resolution | Status |
| --- | --- | --- | --- | --- | --- |
| `ISS-001` | `[YYYY-MM-DD]` | `[issue]` | `Low / Medium / High` | `[resolution]` | `Open / Resolved / Deferred` |

## 12. Testing Report — Required for Medium/Large

| Test ID | Test Type | Target | Command or Method | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| `TEST-001` | `Unit / Integration / E2E / Manual / Review` | `[target]` | `[command or manual check]` | `Passed / Failed / Not Run / Not Required` | `[notes]` |

Test type hints by domain:
- For Unity: `EditMode` (isolated logic) / `PlayMode` (runtime/scene integration)
- For web: `Unit` (Jest/Vitest) / `Integration` (Supertest) / `E2E` (Cypress/Playwright)
- For mobile/desktop: `Unit` / `Manual on device or emulator`

### 12.1 Test Failure Log — Required When Applicable

| Date | Test | Failure | Fix | Final Result |
| --- | --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[test]` | `[failure]` | `[fix]` | `Passed / Failed / Deferred` |

### 12.2 Skipped or Not Required Tests — Required When Applicable

| Test or Check | Reason | Risk | Follow-up |
| --- | --- | --- | --- |
| `[test/check]` | `[why not run]` | `Low / Medium / High` | `[follow-up or None]` |

## 13. Runtime Verification — Required When Applicable

Use this section when the task affects runtime behavior, UI flows, scene/prefab loading, startup/bootstrap behavior, or platform-specific integration. Fill the checks relevant to your stack.

| Check | Result | Evidence or Notes |
| --- | --- | --- |
| Build or compile clean | `Passed / Failed / Not Run / Not Required` | `[notes]` |
| Automated test suite green | `Passed / Failed / Not Run / Not Required` | `[notes]` |
| Manual boot/startup check | `Passed / Failed / Not Run / Not Required` | `[what was tested: entry point, startup scene, app launch, etc.]` |
| Manual feature or workflow check | `Passed / Failed / Not Run / Not Required` | `[what was checked]` |
| Console/log errors reviewed | `Passed / Failed / Not Run / Not Required` | `[errors/warnings or None]` |

Domain hints for the boot/startup check row:
- For Unity: Press Play from Bootstrap scene; check Unity Test Runner and console
- For web: `npm run dev` / `npm run build` + open in browser; check console errors
- For mobile: install on device/emulator; check startup and key user flows
- For backend: start server; hit health endpoint; check logs

## 14. Review Report — Required for Medium/Large

Read your project's review guideline doc (if one exists) before filling this section.

| Review Item | Result | Notes |
| --- | --- | --- |
| Requirements satisfied | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Scope respected | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Architecture respected | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Coding convention followed | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Tests are sufficient | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Runtime verification completed | `Passed / Needs Work / Not Reviewed` | `[notes]` |
| Documentation updated | `Passed / Needs Work / Not Reviewed` | `[notes]` |

### 14.1 Review Findings

| Finding ID | Severity | Finding | File or Area | Resolution | Status |
| --- | --- | --- | --- | --- | --- |
| `REV-001` | `Low / Medium / High` | `[finding]` | `[path/area]` | `[fix or decision]` | `Open / Resolved / Deferred` |

## 15. Documentation Updates — Required for Medium/Large

| Document | Update Needed? | Status | Notes |
| --- | --- | --- | --- |
| Task document | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| SRS | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| Software Design Document | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| Spec-Driven Development document | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| Task Process Report | `Yes` | `Todo / Done` | `[this document]` |
| Architecture or feature map doc | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| Project phase or progress report | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |
| Other documentation | `Yes / No` | `Todo / Done / Not Required` | `[path/notes]` |

## 16. Final Outcome — Required for Medium/Large

| Field | Value |
| --- | --- |
| Final Status | `Completed / Partially Completed / Deferred / Cancelled` |
| Completed Scope | `[what was completed]` |
| Deferred Scope | `[what was not completed and why]` |
| Known Issues | `[known issues or None]` |
| Follow-up Tasks | `[task IDs or None]` |
| Final Verification | `[tests/checks/review result summary]` |

## 17. Lessons Learned — Required for Medium/Large

| Lesson | Applies To | Follow-up Needed? |
| --- | --- | --- |
| `[lesson]` | `[feature/process/tooling]` | `Yes / No, details` |

## 18. Feedback Memory — Required When Applicable

Use this section if a project constraint, convention, or workflow rule was almost missed or forgotten during this task. Capturing it here helps prevent the same mistake in future tasks.

| Date | Constraint or Feedback | Correction Made | Future Reminder |
| --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[constraint/feedback — reference your project's workflow or convention doc if applicable]` | `[correction]` | `[reminder]` |

## 19. Approval and Sign-off — Required for Medium/Large

| Role | Name | Decision | Date | Notes |
| --- | --- | --- | --- | --- |
| Owner | `[name]` | `Ready for Review / Completed / Blocked` | `[YYYY-MM-DD]` | `[notes]` |
| Reviewer | `[name]` | `Approved / Changes Requested / Deferred` | `[YYYY-MM-DD]` | `[notes]` |
````

---

## Phase 5 — Deliver

Ask the user which output format they want: **Markdown (.md)** or **DOCX**. For DOCX, read `/mnt/skills/public/docx/SKILL.md` before generating.

Save to `/mnt/user-data/outputs/` using the task ID in the filename (e.g. `PROJ-42-task-process-report.md`), then use `present_files` to share it.

Keep the response brief: note the task size assumed, any sections pre-marked as Not Required, and any fields left as TODO.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Task size was determined first and section labels match accordingly
- [ ] All `GameClient/` or other project-specific hardcoded paths replaced with `[path or None]` placeholders
- [ ] Unity-specific rows (EditMode/PlayMode, Bootstrap scene, Unity Test Runner) appear only as domain hints, not as the default
- [ ] Section 13 is titled "Runtime Verification" (not "Unity Editor Verification")
- [ ] Section 6 Approval-Sensitive Areas uses generic package manager and architecture references, not Unity-specific ones
- [ ] No field is silently invented — unknowns are marked `TODO: [what's needed]`
- [ ] Output filename includes the task ID
- [ ] File saved to `/mnt/user-data/outputs/` and presented via `present_files`
