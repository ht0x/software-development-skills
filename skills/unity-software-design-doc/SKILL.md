---
name: unity-software-design-doc
description: >-
  PRIMARY PURPOSE: work through a large module or task and align dev, QA,
  DevOps, and PM before implementation. Not for small bug fixes, typo fixes,
  or doc-only changes. Written for Unity developers and team leads.
  Triggered exclusively by /unity-software-design-doc. Generates a
  filled-in Software Design Document scoped to Unity projects. Covers
  architecture and scene structure, MonoBehaviour/ScriptableObject/DOTS
  system design, data model and save/load, Unity interfaces and C# events,
  approval-gating checklist, asset pipeline, build and platform targets,
  Unity Test Framework strategy, and design sign-off. Collects project
  context (feature name, Unity version, render pipeline, target platforms,
  audience), asks for output format (Markdown or Word .docx), then
  generates immediately. 
disable-model-invocation: true
---

# /unity-software-design-doc

Generate a filled-in Unity-specific Software Design Document from collected project context — generates immediately after elicitation, no confirmation step.

## Usage

```
/unity-software-design-doc
```

Invoke with the slash command. The skill collects project context, asks for output format, then writes the complete 17-section Unity SDD.

## Workflow at a glance

```
1. Elicit   →  collect project name, Unity version, render pipeline, platforms, audience, §5 sub-sections
2. Format   →  ask whether to output Markdown (.md) or Word (.docx)
3. Generate →  write the complete 17-section Unity SDD immediately
4. Deliver  →  save to outputs and present the file
```

---

## Phase 1 — Elicit

Ask the user for the following. Only ask for what is not already clear from the conversation.

- **Project / feature name** — what is being built?
- **Purpose and problem** — one or two sentences: what gameplay or technical need this addresses.
- **Unity version** — e.g. 2022.3 LTS, 6000.x, etc.
- **Render pipeline** — Built-in, URP, or HDRP?
- **Target platforms** — PC, iOS, Android, console, WebGL, or mixed?
- **Primary audience for this doc** — dev only, cross-functional (dev + QA + producer), or all stakeholders?
- **§5 Proposed Design sub-sections to include** — all five, or a subset?
  - 5.1 Architecture & Scene Structure
  - 5.2 Systems / Modules
  - 5.3 Data Model
  - 5.4 Interfaces & Contracts
  - 5.5 Key Flows
- **Known constraints or related docs** (optional) — third-party packages, deadlines, links to GDD, RFC, or tickets.

Use `AskUserQuestion` for multiple-choice options (render pipeline, platforms, §5 sub-sections). Use plain text for project name, purpose, and constraints.

Infer whatever is already stated — do not re-ask for information already in the conversation.

---

## Phase 2 — Ask output format

After elicitation, ask:

> "Should I produce this as **Markdown (.md)** or a **Word document (.docx)**?"

- If **Markdown**: generate the SDD as a `.md` file saved to `/mnt/user-data/outputs/`.
- If **DOCX**: read the `docx` skill at the path shown in your available skills list and follow its conventions to produce a `.docx` file.

---

## Phase 3 — Generate

Write the complete Unity SDD immediately using the corrected section numbering below (the source template had a duplicate §8 — this is fixed here). Substitute all collected values; use `_<placeholder>_` for anything not provided.

### Header table

| Field | Value |
|---|---|
| **Project / Feature** | _[name]_ |
| **Author(s)** | _\<name\>_ |
| **Reviewers** | _\<names\>_ |
| **Status** | Draft |
| **Version** | 0.1 |
| **Unity Version** | _[Unity version]_ |
| **Render Pipeline** | _[Built-in / URP / HDRP]_ |
| **Target Platforms** | _[platforms]_ |
| **Last Updated** | _[today's date]_ |
| **Related Docs** | _[links if provided, else \<links: GDD, RFC, tickets\>]_ |

---

### Section writing guidance

**§1 Overview**
2–4 sentences. Someone unfamiliar should grasp what is being built and why from this section alone.

**§2 Background & Context**
- **Problem statement** — what gameplay or technical need this addresses.
- **Current state** — how it works today (if applicable).
- **Why now** — the trigger or motivation.

**§3 Goals & Non-Goals**
Goals: measurable, specific outcomes. Non-goals: explicitly out of scope to prevent scope creep. Use `_<placeholder>_` if not provided.

**§4 Requirements**
- **Functional** — what the system must do in-game.
- **Non-Functional** — frame budget, memory footprint, load times, platform constraints, accessibility, input support.
- **Constraints & Assumptions** — Unity version, render pipeline, third-party packages/assets, deadlines, team size, platform limits.

Fill from elicited constraints; use `_<placeholder>_` for anything unknown.

**§5 Proposed Design**
Include only the sub-sections confirmed in Phase 1.

- **5.1 Architecture & Scene Structure**
  - Overall pattern: pure MonoBehaviour, ECS/DOTS, or hybrid (engine glue vs. plain-C# logic layer).
  - Scene/prefab hierarchy and how scenes are loaded (single, additive, async).
  - Where logic lives vs. where it's just glue to the engine.
  - Diagram + narrative of major components and how they interact.

- **5.2 Systems / Modules**
  > "Module" here = a logical system, not a Unity `Component`. Unity components (MonoBehaviour/ScriptableObject) are described within each module.

  For each system: responsibility, key MonoBehaviours/ScriptableObjects, managers/singletons, and communication method (direct refs, UnityEvents, C# events, message bus, SO-based events).

- **5.3 Data Model**
  - **ScriptableObjects** — config/static data, designer-authored content.
  - **Runtime state** — what lives in memory, ownership.
  - **Save/load** — serialization format (JSON, binary), versioning/migration, Unity serialization quirks (`[SerializeField]`, `ISerializationCallbackReceiver`, no polymorphism by default).

- **5.4 Interfaces & Contracts**
  - Internal C# interfaces between systems.
  - Event signatures (who raises, who listens).
  - External APIs if any — backend, multiplayer/netcode, analytics, platform SDKs.

- **5.5 Key Flows**
  Walk through 1–3 important sequences step by step (e.g., spawn lifecycle, input → action → state update, save/load path), noting Update/FixedUpdate/coroutine/async boundaries.

**§6 Alternatives Considered**

| Option | Pros | Cons | Why not chosen |
|---|---|---|---|
| _\<A\>_ | | | |
| _\<B\>_ | | | |

Fill in from user-provided context if available; otherwise leave the placeholder rows.

**§7 Cross-Cutting Concerns**
- **Performance & frame budget** — target frame rate, draw calls, GC allocations, object pooling, profiler hotspots, main-thread vs. jobs.
- **Memory & assets** — texture/mesh budgets, Addressables loading/unloading, streaming.
- **Security / anti-cheat / save integrity** — where relevant (multiplayer, IAP, leaderboards).
- **Error handling & resilience** — failure modes, null-ref guards, missing-asset handling.
- **Observability** — debug logging, in-editor tooling/gizmos, telemetry.

**§8 Approval-Sensitive Design Changes**
Mark whether the proposed design touches areas that require explicit approval before implementation.

| Area | Needed? | Notes |
|---|---|---|
| New package, dependency, or plugin | `Yes / No` | _\<notes\>_ |
| Architecture or ADR change | `Yes / No` | _\<notes\>_ |
| Save data, serialization, or migration | `Yes / No` | _\<notes\>_ |
| SharedContracts, networking, or API contract | `Yes / No` | _\<notes\>_ |
| File, folder, scene, prefab, or asset move | `Yes / No` | _\<notes\>_ |
| Large refactor outside local task scope | `Yes / No` | _\<notes\>_ |

**§9 Asset Pipeline & Project Structure**
- Folder conventions and naming.
- Addressables / AssetBundles setup, import settings, presets.
- Prefab variants and nesting strategy.
- Source control considerations (meta files, `.gitignore`, LFS, scene/prefab merge conflicts).

**§10 Build & Platform Targets**
- Platforms and their build settings.
- Platform-specific code paths (`#if UNITY_ANDROID`, etc.) and input differences.
- Quality settings, define symbols, CI/build automation.

**§11 Testing Strategy**
- Unity Test Framework: EditMode (logic) vs. PlayMode (in-scene) tests.
- What's automated vs. manual playtesting.
- Designing logic to be testable (separating plain C# from MonoBehaviour).
- What "done and verified" means per platform.

**§12 Rollout & Migration**
Phasing, feature flags, data/save migration steps, rollback plan.

**§13 Risks & Open Questions**

| Risk / Question | Impact | Mitigation / Owner |
|---|---|---|
| _\<placeholder\>_ | | |

**§14 Open Design Questions**
Unresolved design questions that need input before implementation can proceed safely.

| Question | Owner | Needed By | Status |
|---|---|---|---|
| _\<question\>_ | _\<name/role\>_ | _\<date or milestone\>_ | Open |

**§15 Timeline & Milestones**
Rough phases or dates, with dependencies called out.

**§16 Design Approval**

| Reviewer | Decision | Date | Notes |
|---|---|---|---|
| _\<name\>_ | Approved / Changes Requested / Rejected | _\<YYYY-MM-DD\>_ | _\<notes\>_ |

**§17 Appendix**
Glossary, references, supporting diagrams, profiler captures, raw data.

---

## Phase 4 — Deliver

1. Save the generated file to `/mnt/user-data/outputs/<project-name>-unity-sdd.md` (or `.docx`).
2. Call `present_files` with the output path.
3. If any `_<placeholder>_` markers remain in critical sections (§1, §4, §5), add a one-sentence note listing which sections still need the user's input.

---

## Quality checklist

Before presenting the output, verify:
- [ ] Skill name is `unity-software-design-doc` and matches the frontmatter `name` field
- [ ] Description is under 1024 characters
- [ ] Slash-only trigger — no conversational auto-trigger phrases in the description
- [ ] All 17 sections present with corrected numbering (no duplicate §8)
- [ ] Only confirmed §5 sub-sections are included
- [ ] Unity-specific terminology preserved throughout (MonoBehaviour, ScriptableObject, DOTS, Addressables, URP/HDRP, EditMode/PlayMode, etc.)
- [ ] Header table includes Unity Version, Render Pipeline, and Target Platforms fields
- [ ] §8 Approval-Sensitive Design Changes table is present with `Yes / No` format
- [ ] No confirmation phase — skill generates immediately after Phase 1 and Phase 2
- [ ] `_<placeholder>_` used for unknowns, not invented content
- [ ] Output format (Markdown or DOCX) matches what the user chose in Phase 2
- [ ] File saved to `/mnt/user-data/outputs/` and presented via `present_files`
