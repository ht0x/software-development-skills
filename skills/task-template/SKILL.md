---
name: task-template
description: >-
  PRIMARY PURPOSE: produce a clear, ready-to-start task definition for a
  team member, agent, or yourself — clear enough to start, review, test,
  and finish without guessing, and readable by developers, QA and project
  managers alike. Generates a filled-in task document. Works across
  domains (web, backend, game, mobile, desktop). Trigger with
  "/task-template", "create a task for X", "write a task spec for...",
  "I need a ticket for...", "break this into a task doc", or whenever work
  needs to be handed off (to a teammate, an AI agent, or your future self)
  with explicit scope, requirements, and a definition of done. Scales from
  a short checklist for small fixes to a full multi-section document for
  large or risky work.
disable-model-invocation: true
---

# /task-template

Generate a complete, filled-in task document for a specific piece of work — sized appropriately, ready to hand to a teammate, an agent, or yourself, and understandable by everyone who touches the task: the developer who builds it, the QA engineer who checks it, and the project manager who tracks it.

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

## Core Idea: Write for Every Reader

A task document is read by more people than the one who builds it. Write it so each of them can do their job without opening the code.

| Reader | What they need from the task | Sections they read |
| --- | --- | --- |
| Project manager / lead | What changes for the user or player, why, how big, when | 1, 2, 4, 6 |
| QA engineer / tester | Exactly how to check that it works, in a running build | 2, 7, 13, 15 |
| Developer / AI agent | What to build, the limits, and where the technical plan lives | All, then the linked plan |

**The task says *what* and *why*. The technical plan says *how*.** Implementation detail — class, method, file, folder, module or assembly names, code snippets, commit hashes, call graphs, lists of code defects found while investigating — belongs in a separate technical plan document (an analysis plan, a spec, a design doc) that the task links to in §12 and §18. It does not belong in the task.

### Two zones

| Zone | Sections | Rule |
| --- | --- | --- |
| **Plain-language zone** | 1–8, 13, 15 | Someone who has never opened the code must understand every line. No code, no class/method/file/folder/module names, no commit hashes. Asset or content names a designer would use are fine. |
| **Implementer zone** | 9–12, 14, 16–19 | May name systems, features and modules, but stays at that level. Still no code and no file-by-file lists — link the technical plan instead. |

### Writing rules

1. **Describe what someone can observe, not how the code does it.**
   - ✗ "Exactly one type calls `OnUpdate` on the content manager."
   - ✓ "Pausing the game stops the character, the clock and every timer at the same moment."
2. **Acceptance criteria are checkable in a running build** by someone who hasn't read the code: an action and the result they should see. Use "Given / When / Then" or a short play step.
3. **Refactors and other no-visible-change work** say so in §2. Their main requirement is "behaves exactly as before", with a short regression list of what to check. State the structural goal in one plain sentence, not a list of types.
4. **Cite design rules instead of restating them.** If the project has a design document with rule or acceptance IDs, quote the IDs in §1 and in each §7 requirement.
5. **Use the project's own vocabulary** (its glossary or design terms) rather than code names.
6. **One plain sentence plus a link** for any technical fact others must know — a risk, a blast radius, a dependency. The detail lives in the linked document.
7. **Stay inside the length budget.** If a section grows past it, the detail belongs in the technical plan.

### Length budget

| Size | Whole task document (guideline) |
| --- | --- |
| Small | ≤ ~2,500 characters — about one screen |
| Medium | ≤ ~6,000 characters |
| Large | ≤ ~10,000 characters, with the rest in linked design or plan documents |

### Project rules come first

Before drafting, look for a project-level issue-writing guideline (for example a file linked from the repository's `CLAUDE.md` or `README`, such as `docs/tech/backlog-issue-guideline.md`). If one exists, read it and follow it: it decides project specifics such as title format, design-ID citation, glossary terms and extra Task Information fields. Where it is more specific than this skill, it wins.

## Workflow at a Glance

```
1. Size      →  determine Small / Medium / Large FIRST — this gates step 2
2. Elicit    →  ask only the question groups that size unlocks
3. Draft     →  fill every applicable section in the right zone, inside the length budget
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
- What does "done" look like — what will a user, player or tester see?
- Who is this for — a teammate, an AI coding agent, or yourself? Who owns it, who reviews it, who tests it?
- What kind of project is this (web, backend, game, mobile, desktop, library, other), and what language/framework/engine?
- Is there a design document with rule or acceptance IDs this task should cite?
- What test types are realistic here: unit/EditMode, integration/PlayMode/E2E, manual, review-only?

**Small — stop after the "always ask" group.** Don't ask about background, dependencies, approval-sensitive areas, or risks unless the user's own description already signals one of these is relevant (e.g. they mention touching a shared schema even in a "small" fix — in that case, ask the relevant follow-up from the Medium/Large group below before proceeding).

**Medium and Large — also ask:**
- Current behavior, and what's wrong/missing/unclear about it, as a user or player would notice it?
- Which existing systems or features does this touch?
- Anything explicitly out of scope that someone might accidentally touch?
- Any required documents, decisions, or blocking tasks before work can start?
- Does this touch a new dependency, architecture, save/data schema, shared API/contract, file move, or broad refactor? These typically need explicit approval before implementation.
- Is there (or will there be) a technical plan document the task should link to?

**Large only — also ask:**
- Should this be split into implementation phases? If so, what's the natural breakpoint between phases?
- Any known risk that could change the approach mid-implementation (e.g. unproven third-party dependency, unclear ownership boundary, performance unknown)?

Don't force every question if context already answers it. If the user pushes back on answering everything ("just draft something"), proceed and mark unanswered fields as TODO rather than guessing specifics.

---

## Phase 2 — Draft the Document

Fill in every applicable section using gathered context, following **Write for Every Reader**: plain language in sections 1–8, 13 and 15; system-level only in the rest; technical detail linked, not pasted. Where a domain-hint sub-bullet doesn't apply to the user's stack (e.g. "scene/prefab" hints for a backend-only task), drop it rather than leaving it as dead placeholder text. Where information is genuinely unknown and the user declined to clarify, write `TODO: [what's needed]` rather than inventing plausible-sounding specifics.

For a **small** task, use only the sections marked `Required for All`, condensed, plus a short checklist in place of Implementation Plan / Review Plan. For **medium/large** tasks, fill the full document below.

### Document Template

```markdown
# Task: [Task Title]

## 1. Task Information — Required for All

| Field | Value |
| --- | --- |
| Task ID | `[task-id]` |
| Task Title | `[short action-focused title, in user/player terms]` |
| Feature or Area | `[feature or system, by its product name]` |
| Design Reference | `[design rule / acceptance IDs this task delivers, or None]` |
| Platforms | `[platforms this must work on, or All]` |
| Owner | `[name or agent]` |
| Reviewer | `[name or role]` |
| Created Date | `[YYYY-MM-DD]` |
| Target Date | `[YYYY-MM-DD or Not Set]` |
| Status | `Todo / In Progress / Blocked / In Review / Done / Cancelled` |
| Priority | `Must / Should / Could` |
| Task Size | `Small / Medium / Large` |

## 2. Summary — Required for All

At most three sentences: what will be different when this is done, for whom, and why it matters. Write it so a project manager could repeat it in a meeting. For work with no visible change (refactor, tooling), say so plainly.

```text
[Task summary]
```

## 3. Background — Recommended for Medium/Large

- Current behavior or state: `[what a user, player or tester sees today]`
- Problem or missing part: `[what is wrong, unclear, missing, or incomplete — as it shows up, not where it is in the code]`
- User, player, customer, developer, or system impact: `[who or what is affected]`
- Technical root cause, if relevant: `[one plain sentence + link to the technical plan]`

For small tasks, one sentence is enough.

## 4. Goals — Required for All

Outcomes, not implementation steps.

- `[Goal 1]`
- `[Goal 2]`
- `[Goal 3]`

## 5. Non-Goals — Recommended for Medium/Large

- `[Non-goal 1]`
- `[Non-goal 2]`

For small tasks, use this only when there's real risk of someone changing unrelated behavior.

## 6. Scope — Required for All

Scope is described as features and behaviors, not files.

### 6.1 In Scope
- `[In-scope item]`
- `[In-scope item]`

### 6.2 Out of Scope
- `[Out-of-scope item]`
- `[Out-of-scope item]`

For small tasks, this can be a short bullet list. For medium/large, separate in-scope and out-of-scope clearly.

## 7. Requirements — Required for All

Use "Must" for required behavior, "Should" for expected behavior, "Could" for optional behavior. Each requirement describes observable behavior and cites its design rule ID when one exists. Each acceptance criterion is something a tester can do in a running build and the result they should see.

| ID | Requirement | Priority | Acceptance Criteria (how to verify in a build) |
| --- | --- | --- | --- |
| `REQ-001` | `[observable behavior] ([design ID])` | `Must / Should / Could` | `[action → expected result]` |
| `REQ-002` | `[observable behavior] ([design ID])` | `Must / Should / Could` | `[action → expected result]` |

For small tasks, 1-3 bullet requirements are enough if a table feels too heavy.

## 8. Expected Deliverables — Required for All

Name each deliverable by what it is, not by its file path.

- Code changes: `[Yes / No, what it delivers]`
- Tests: `[Yes / No, what they check]`
- Documentation: `[Yes / No, which documents]`
- Asset, schema, config, or data changes: `[Yes / No, details]`
  - For web/backend: migrations, API schema, configuration
  - For game: scenes, prefabs, game data, level data, art assets
  - For mobile/desktop: platform-specific resources, manifests
- Review report or task process report: `[Yes / No]`

## 9. Affected Areas — Required for Medium/Large

Systems, features or content areas — not individual files. File-level detail goes in the technical plan.

| Area | System / Feature / Asset | Expected Change |
| --- | --- | --- |
| `[area]` | `[system, feature or asset name]` | `Add / Modify / Remove / Unknown` |
| `[area]` | `[system, feature or asset name]` | `Add / Modify / Remove / Unknown` |

For small tasks, include this only if the task depends on a specific system, asset, config, or decision.

## 10. Dependencies and Inputs — Recommended for Medium/Large

- Required documents: `[document names or None]`
- Required assets or data: `[names or None]`
- Required decisions: `[open question or decision needed, or None]`
- Blocking tasks: `[task IDs or None]`
- External tools, packages, or services: `[details or None]`

## 11. Approval-Sensitive Changes — Required for Medium/Large

One plain line per "Yes"; link the decision record or technical plan for detail.

| Area | Needed? | Notes |
| --- | --- | --- |
| New package, dependency, or plugin | `Yes / No` | `[one line]` |
| Architecture or ADR change | `Yes / No` | `[one line + link]` |
| Data schema, persistence, save data, or migration | `Yes / No` | `[one line]` |
| Shared contracts, networking, or public API | `Yes / No` | `[one line]` |
| File or folder move | `Yes / No` | `[one line]` |
| Large refactor outside local task scope | `Yes / No` | `[one line]` |

For small tasks, use this section only if the task may touch dependencies, architecture, data/persistence, shared contracts, networking, file moves, or broad refactors.

## 12. Implementation Plan — Required for Medium/Large

At most six steps, each an outcome someone could check. The detailed technical plan lives in its own document — link it below the table.

| Step | Work | Owner | Done When | Status |
| --- | --- | --- | --- | --- |
| `1` | `[outcome]` | `[name]` | `[observable done condition / REQ IDs]` | `Todo / Doing / Done` |
| `2` | `[outcome]` | `[name]` | `[observable done condition / REQ IDs]` | `Todo / Doing / Done` |
| `3` | `[add or update tests]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |
| `4` | `[update docs or reports]` | `[name]` | `[done condition]` | `Todo / Doing / Done` |

Technical plan: `[link or path, or TODO]`

For small tasks, a short checklist is enough.

## 13. Testing Plan — Required for All

| Test ID | Test Type | Target | Steps | Expected Result | Status |
| --- | --- | --- | --- | --- | --- |
| `TEST-001` | `[Unit/EditMode, Integration/PlayMode, E2E, Manual, Review]` | `[behavior or REQ ID]` | `[what to do]` | `[what should happen]` | `Todo / Done / Not Required` |
| `TEST-002` | `[Unit/EditMode, Integration/PlayMode, E2E, Manual, Review]` | `[behavior or REQ ID]` | `[what to do]` | `[what should happen]` | `Todo / Done / Not Required` |

Manual tests are written so a tester can follow them without reading code. Automated tests name the behavior they check, not the test class.

Recommended checks (apply the ones relevant to the stack):
- Read any project-specific testing guideline doc, if one exists, before writing tests.
- Run relevant unit/EditMode tests when changing isolated logic.
- Run relevant integration/PlayMode/E2E tests when changing cross-component, gameplay, scene, prefab, UI, or runtime integration behavior.
- Run manual verification when the task affects runtime behavior, UI flow, scene/prefab loading, or startup/bootstrap behavior.

For small tasks, write only the manual check or test command needed to confirm the fix.

## 14. Review Plan — Required for Medium/Large

- Review type: `Code / Design / Documentation / Manual QA / Full task review`
- Review guideline: `[document name or None]`
- Reviewer focus:
  - `[focus area 1]`
  - `[focus area 2]`
  - `[focus area 3]`

For small tasks, this can be replaced by the Definition of Done checklist below.

## 15. Definition of Done — Required for All

- Requirements are implemented or explicitly deferred.
- The acceptance criteria in §7, and any design acceptance IDs cited in §1, pass in a running build.
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
| `[risk, in one plain sentence]` | `Low / Medium / High` | `[how to reduce or handle the risk]` |

For small tasks, use this only when there's uncertainty that could change the solution.

## 17. Open Questions — Optional

| Question | Owner | Answer or Decision | Status |
| --- | --- | --- | --- |
| `[question]` | `[name]` | `[answer]` | `Open / Answered` |

## 18. Related Documents — Recommended for Medium/Large

| Document | Path or Link | Status |
| --- | --- | --- |
| Design document (e.g. GDD, product spec) | `[path or Not Required]` | `Draft / Approved / Not Required` |
| System Requirements Specification | `[path or Not Required]` | `Draft / Approved / Not Required` |
| Software Design Document | `[path or Not Required]` | `Draft / Approved / Not Required` |
| Technical plan / Spec-Driven Development Plan | `[path or Not Required]` | `Draft / In Progress / Not Required` |
| Task Process Report | `[path or Not Required]` | `In Progress / Completed / Not Required` |

For small tasks, include only direct links to references if needed.

## 19. Progress Log — Optional

Plain language: what now works, what's next, what's blocked.

| Date | Update | Blockers or Decisions |
| --- | --- | --- |
| `[YYYY-MM-DD]` | `[progress update]` | `[blocker/decision or None]` |
```

---

## Phase 3 — Flag Gaps Honestly

Before presenting the draft, scan it for any field filled with a guess rather than something the user actually stated or that's clearly inferable from context (e.g. an assumed file path, an assumed test framework). Convert genuine guesses into `TODO:` markers instead of presenting them as settled facts. Light structural inference is fine (e.g. inferring "this needs an integration test" from "touches two systems") — the line is between reasonable inference and invented specifics like fake paths, fictional existing systems, or made-up reviewers.

Then read sections 1–8, 13 and 15 as if you were a tester who has never seen the code. Rewrite any line that only makes sense to the person who built it.

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
- [ ] Sections 1–8, 13 and 15 contain no code, no class/method/file/folder/module names and no commit hashes
- [ ] A tester who has never seen the code could follow every acceptance criterion and manual test step
- [ ] Every requirement cites its design rule ID when the project has a design document
- [ ] The document is inside the length budget for its size; technical detail is linked, not pasted
- [ ] Every applicable section has either real content or an explicit `TODO:` — nothing is silently invented
- [ ] Domain-hint sub-bullets that don't apply to this stack have been removed, not left as dead placeholders
- [ ] No external doc paths or process references are hardcoded from a different project than the user's
- [ ] Any project-level issue-writing guideline was read and followed
- [ ] Test plan matches what the user said is realistically testable for their stack
- [ ] Document is internally consistent (names and owners referenced in one section match elsewhere)
