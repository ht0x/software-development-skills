---
name: build-to-learn-systems
description: >-
  Author rigorous, phase-by-phase engineering course documents that teach
  how to build a real, production-grade system by actually building it.
  Domain-general: backend, distributed systems, chat/realtime, game systems,
  compilers, ML pipelines, CLI tools, infrastructure. Each phase is one PDF:
  theory, architecture with ADRs, runnable code, tests/deploy steps, and a
  SPEC with an acceptance checklist. Use proactively whenever the user wants
  to learn something by building a real instance of it over multiple
  sessions — even without the words skill, course, curriculum, or phase.
  Trigger with "/build-to-learn-systems"; on course/curriculum/phase
  language ("write the next phase", "continue my course"); on learning-goal
  phrasing ("I want to learn X by building it", "build a toy version of Y
  to understand it", "project-based curriculum for..."); on requests for an
  ADR/SPEC for a learning project or a course-context/manifest file. Do not
  use for a single explanation with no intent to build over time.
---

# Build-to-Learn Systems Course Author

## What this skill produces

A multi-document course that teaches a developer to build a real, production-grade
system by building it step by step. The course is split into **phases** (Phase 0,
Phase 1, …). **Each phase is one self-contained document, delivered as a PDF.**

The guiding pedagogy is: **learn what → build it → run it → understand why.** The
learner should never copy code they don't understand; every phase ends with
something that actually runs and a checklist proving it.

This skill is domain-general (use it for any backend / realtime / distributed /
infrastructure system), but it carries a fully worked example: a chat + realtime
voice system for a game. See `references/example-evergreen-context.md`.

## Core operating rules (read before doing anything)

1. **One phase at a time.** Write phase N, deliver it, then STOP and wait for the
   user to confirm ("done with Phase N") before writing phase N+1. Never batch
   several phases. This keeps each document deep and the learner un-overwhelmed.

2. **Ground every phase in the real state, not memory.** Before writing phase N+1,
   read (a) the **course-context file** (the manifest — see below) and (b) the
   actual artifacts from the prior phase (the previous phase document and, when the
   learner has built code, the real repository files). Do not invent file names,
   ports, schemas, or code that contradicts what already exists. If you are unsure
   of an exact detail, ask the user to paste the file or read the repo — do not
   guess. Hallucinated continuity is the main failure mode of a long course.

3. **Maintain a course-context file (manifest).** This is a small, high-density
   Markdown file the user keeps and re-pastes at the start of each session. It is
   the externalized memory of the course. After finishing each phase, update it.
   See "The course-context file" below and the template in
   `assets/course-context-template.md`.

4. **Separate FACT from INFERENCE.** State plainly which claims are established
   technical facts and which are your recommendation/opinion/estimate. When you give
   a number, a default, or a "you should", label it as a recommendation so the
   learner can weigh it. This is a hard requirement, not a stylistic nicety.

5. **Choose the document language once, record it, reuse it.** Before writing the
   very first phase (or if the manifest does not already record a language), ask:

   > "What language should I write the course documents in?"
   > 1. English
   > 2. Tiếng Việt
   > 3. Other — please specify

   Record the answer in the manifest (canonical names book §F or a top-level note).
   All subsequent phases use that language automatically — never ask again unless the
   user explicitly requests a change. This SKILL.md is always in English regardless.

## Per-phase document structure

Every phase document follows the same rhythm. Use these sections in order:

1. **Cover** — course title, phase number/name, one-line subtitle, "Document N / total".
2. **Objectives** — what the learner will understand and be able to do by the end.
3. **Theory** — the concepts needed before writing a line of code, explained for a
   newcomer, with everyday analogies. Define vocabulary; forward-reference where a
   term is covered in depth later.
4. **Architecture & decisions** — system/data diagrams (Mermaid) plus **ADRs**
   (Architecture Decision Records) for each significant choice.
5. **Hands-on** — concrete, runnable code with per-part explanation. Prefer a fast
   dev loop (run locally) before the production-shaped packaging.
6. **Test & Deploy** — how to verify the feature actually works.
7. **SPEC & acceptance checklist** — functional + non-functional requirements and a
   tick-box checklist the learner uses to self-certify "this phase is done",
   including at least one deliberate "break it and watch it fail" test.
8. **Summary & next-phase preview** — what was achieved; what the next phase builds;
   the explicit "tell me 'done with Phase N'" handoff.

Target length: **~1000+ source lines per phase.** Depth over brevity. If a phase
would exceed that and cover several distinct features, propose splitting it into
two phases and ask the user before doing so.

## Authoring conventions

The detailed conventions (callout HTML, ADR template, SPEC template, diagram and
fact/inference guidance) live in `references/authoring-conventions.md`. **Read that
file before writing a phase.** The essentials:

- **Callout boxes** for emphasis: `key` (◆ core concept), `tip` (✔ best practice),
  `warn` (▲ pitfall), `note` (ℹ aside). Authored as
  `<div class="callout key" markdown="1"><span class="lbl">…</span>…</div>`.
- **Diagrams in Mermaid** (```mermaid fenced blocks); the pipeline renders them to
  crisp SVG.
- **ADR format:** Context → Decision → Alternatives & comparison → Consequences.
- **SPEC format:** Scope (in/out) → Functional (FR-x) → Non-functional (NFR-x) →
  Acceptance checklist.
- **Schema evolution via migrations:** introduce base tables early with room to
  grow; let each feature phase create its own tables/columns, teaching real
  migration discipline rather than designing everything up front.

## Output: rendering to PDF

The documents are written in Markdown (with Mermaid blocks and the callout divs)
and rendered to PDF by a bundled engine. **Read `references/pdf-pipeline.md` for the
full pipeline, environment setup, and troubleshooting** (it covers the two quirks
that will otherwise bite you: pointing the Mermaid CLI at a working Chromium, and a
heredoc byte-corruption trap with Vietnamese text — write Markdown via a file-create
tool, not shell heredocs).

Quick usage once the environment is set up:

```bash
python3 scripts/build_pdf.py <phase.md> <out.pdf> "Footer title text"
```

After building, render a few pages to images and visually inspect them (diagrams,
code highlighting, accented text, callouts) before delivering. Confirm every Mermaid
block rendered (no error placeholder in the generated HTML).

## The course-context file (manifest)

This single Markdown file is the course's externalized memory and the antidote to
context-window loss across many sessions. Keep it dense. It should contain:

- **Project context** — what is being built, constraints (scale, budget, timeline),
  the "build from scratch" allow/deny list, output language, the fact-vs-inference rule.
- **Target scale** — the numbers that constrain design.
- **Tech stack** — locked choices.
- **Roadmap** — the full phase list with status (done / pending).
- **Authoring conventions** — output format, callouts, ADR/SPEC, length, one-phase
  workflow.
- **Canonical names book** — repo name, service names, ports, project names,
  endpoints, connection conventions, data ownership, any cross-service contracts
  (e.g. a JWT contract). Later phases must not contradict this.
- **ADR ledger** — one line per ADR.
- **Per-phase summary & hooks** — for each finished phase, one paragraph of "what it
  established" + "what later phases depend on". For planned phases, note where
  cross-cutting features land.
- **Source of truth** — where the real artifacts live (the delivered PDFs + the repo).

Use `assets/course-context-template.md` as the blank skeleton, and
`references/example-evergreen-context.md` as a filled, real example. After each
phase, hand the user an updated version (bump v1 → v2 → …) and tell them to use the
newest one.

## Phase review & feedback loop (before writing Phase N+1)

Run this step every time the user says "done with Phase N" — before the pre-flight
for Phase N+1. Its purpose is to surface gaps between *what the document describes*
and *what the learner actually built*, so the learner can decide whether to fix
things before continuing.

**Claude's role:** read, compare, report, ask. Claude does NOT edit code, commit
files, or decide to skip discrepancies. All fixes are made by the learner.

### Step 1 — Gather the artifacts to review

Two modes depending on context:

**Claude Code (automated, has repo access)**
Read the following automatically:
- The phase N document (`docs/phases/phaseN.md`).
- The course-context file (manifest).
- All source files the phase touches (infer from the phase doc's hands-on section —
  e.g. `Program.cs`, `docker-compose.yml`, `Dockerfile`, migration files, etc.).
List the files read at the top of the feedback so the learner knows what was
checked.

**Chat (no repo access)**
Ask the learner to paste or attach the relevant files:

> "To review Phase N before moving on, please paste (or attach from your repo):
> 1. The key source files changed in this phase — e.g. `Program.cs`,
>    `docker-compose.yml`, any new migration files.
> 2. Any config files that were modified (env files, appsettings, etc.).
>
> You don't need to paste the phase document — I already have it."

Wait for the learner to provide the files, then proceed.

### Step 2 — Compare and produce structured feedback

Compare what the phase document specifies against what is actually in the provided
files. Produce feedback using exactly this structure:

```
## Phase N review

### ✅ Matches — looks good
- <item: what the doc said, what the code has — they match>
- …

### ⚠️ Discrepancies — doc says X, repo has Y
- <item: exact location in doc + exact location in code + what differs>
  Suggestion: [fix in code] or [update manifest if intentional deviation]
- …

### 💡 Gaps — in doc but not found in repo (or vice-versa)
- <item: what the doc describes that isn't visible in the provided files>
  Note: could be implemented elsewhere — ask the learner to verify.
- …

### 📋 Manifest drift
- <any canonical name, port, schema, or endpoint in the repo that differs
  from or is missing in the manifest — these must be synced before Phase N+1>
- …
```

Keep each item concrete: cite the specific file, line reference or section, and
the exact value that differs. Avoid vague statements like "code looks different".

### Step 3 — Ask the learner how to proceed

After the feedback, always ask:

> "Do you want to fix anything before we move on, or continue to Phase N+1?
>
> - **Fix first:** make your changes, then tell me 'review again' and I'll re-read
>   the updated files and run through the checklist again.
> - **Continue:** I'll carry any noted discrepancies forward as context when writing
>   Phase N+1 (and flag them in the manifest)."

Wait for the learner's response. Do not start the pre-flight until they reply.

### Step 4 — Repeat if the learner chooses to fix

If the learner says "review again":
- In Claude Code: re-read the updated files from the repo.
- In chat: ask them to re-paste the changed files.

Run the comparison again from Step 2. There is no limit on the number of cycles —
the learner decides when they are satisfied and ready to move on.

### Step 5 — When the learner says "continue"

Note any unresolved ⚠️ or 💡 items briefly in the manifest (§G per-phase summary,
under Phase N) so they are not lost. Then proceed to the **pre-flight review** for
Phase N+1.

---

## Pre-flight review (MANDATORY before writing any phase)

**Never start writing a phase document without running this check.** A 200-word
pre-flight that catches a scope problem costs almost nothing; rewriting a 1000-line
document costs everyone.

### When to run it

- Before writing Phase 0 (after the initial interview, before any document).
- Before writing Phase N+1 (after the user says "done with Phase N").
- Any time the user asks "write the next phase" without prior discussion.

### What to show the user

Present a compact pre-flight summary — not the full document, just a structured
preview. Always include all five items:

```
## Pre-flight: Phase N — <title>

**Scope (in):**
- <feature / concept 1>
- <feature / concept 2>
- …

**Scope (out — saved for later):**
- <item deferred and why>

**Key decisions / ADRs this phase records:**
- <ADR topic 1>
- <ADR topic 2>

**Dependencies on prior phases:**
- <what this phase builds directly on top of>

**Cross-phase features landing here:**
- <any item from the roadmap/manifest that the course-context flags as
  "should land in this phase">
```

### Proactive questions to always ask (pick the relevant ones)

After the summary, **always ask these proactively** — don't wait for the user to
raise them:

1. **Split check.** "This phase covers X, Y, Z. Combined, that's likely 1500+ lines.
   Should I split it into Phase N-a (X, Y) and Phase N-b (Z), or keep it together?"
   Propose a concrete split; let the user decide.

2. **Missing requirements.** "Based on the roadmap and what Phase N−1 established,
   I notice these related features haven't been scheduled yet: [list]. Should any
   of them land in this phase, or stay deferred?"

3. **Dependency check.** "Phase N+1 will need [X] to exist after this phase.
   Confirm this phase creates/establishes [X], or flag it now so I can add it."

4. **ADR questions.** "This phase will record ADR-XXXX about [topic]. Do you have
   a preference, or should I recommend an option?"

5. **Canonical name / schema confirmation.** If the phase introduces new service
   names, ports, table names, or endpoints: list the proposed canonical names and
   ask for confirmation before writing them into the document (they can't easily
   be changed later without inconsistency).

### Then wait

After presenting the pre-flight, **stop and wait for the user's response.** Do not
proceed to write the document until the user explicitly says "looks good" or provides
adjustments. This single rule eliminates most token-wasting rewrites.

### Exception: Claude Code automated loop

When running inside the Claude Code automated loop (the learner has pushed their
code and Claude Code is operating autonomously), skip the interactive pre-flight
wait and instead document the scope decisions as comments at the top of the
generated Markdown file, flagged for the learner to review in the PR.

---

## Starting a brand-new course (Phase 0)

When the user wants to start a new build-to-learn course from scratch:

1. Ask the document language (Core rule 5) — do this first, before anything else.
2. Interview for: the system to build, the learner's starting level, hard
   constraints (scale, budget, timeline, allowed/forbidden tech).
3. Propose a full phase roadmap as a table (phase number, name, one-line
   description). Ask: "Does this look right? Should any phase be split, merged, or
   reordered? Are there capabilities missing?" Wait for confirmation.
4. Run the **pre-flight review** for Phase 0 (see above). Wait for confirmation.
5. Write Phase 0: dev environment, foundational vocabulary, first ADRs, running
   health-check milestone.
6. Create the course-context file (v1) — include the chosen document language.
7. Deliver Phase 0 PDF + manifest v1, then wait.

## Continuing an existing course (Phase N+1)

1. Read the course-context file the user provides. Confirm the document language is
   recorded in the manifest; if not, ask now (see Core rule 5).
2. Run the **phase review & feedback loop** for Phase N (see above). Wait for the
   learner to say "continue" before proceeding.
3. Run the **pre-flight review** for Phase N+1 (see above). Wait for confirmation
   or adjustments before writing a single line of the document.
4. Write the phase, keeping every canonical name/port/schema consistent with the
   manifest. Reuse, don't reinvent.
5. Build the PDF, inspect it, deliver it, and deliver the updated manifest.
6. Stop and wait for "done with Phase N+1".

## Claude Code repo workflow (automated loop)

This is the recommended workflow when the learner uses **Claude Code on the web**
(claude.ai/code) with a GitHub repo. It minimises manual context-pasting and makes
each phase a proper version-controlled PR.

### One-time repo setup (learner does this once)

Commit these files into the repo so Claude Code can find and use them in any
session without re-uploading:

```
docs/
  tools/
    build_pdf.py          ← the PDF rendering engine (from this skill)
    BUILD.md              ← environment setup instructions (from this skill)
  phases/                 ← one .md + one .pdf per phase
  adr/                    ← ADR files (0001-…md, 0002-…md …)
Course-Context_<name>.md  ← the course-context/manifest file (kept at repo root)
```

`BUILD.md` describes the exact commands to install all dependencies (mermaid-cli,
Chromium via Playwright, Python libs, fonts) for both macOS and Ubuntu/Linux. The
Claude Code sandbox runs Ubuntu, so the Ubuntu section is what Claude Code executes
when it installs the pipeline before building a PDF.

### The repeating loop (one turn per phase)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. LEARNER builds phase X                                       │
│     • implements the feature described in the phase X document  │
│     • when it works: git commit + git push (to main or a branch)│
│     • if questions arise mid-phase → ask in claude.ai chat      │
└──────────────────────┬──────────────────────────────────────────┘
                       │  "done with Phase X" (or opens Claude Code)
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. CLAUDE CODE reads repo, writes Phase X+1                    │
│     Prompt to use:                                              │
│     "Read Course-Context_<name>.md and docs/phases/phaseX.md,  │
│      plus any src/ files that phase X+1 builds on.             │
│      Write docs/phases/phase(X+1).md following the authoring   │
│      conventions in the skill. Then:                            │
│        - run BUILD.md steps if pipeline not installed           │
│        - run: python3 docs/tools/build_pdf.py                   │
│            docs/phases/phase(X+1).md                           │
│            docs/phases/phase(X+1).pdf                          │
│            '<footer title>'                                      │
│        - update Course-Context_<name>.md (bump version,         │
│          mark phase X done, fill in §G summary & hooks)         │
│        - commit everything to a branch named phase-(X+1)-draft" │
└──────────────────────┬──────────────────────────────────────────┘
                       │  Claude Code opens a PR
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. LEARNER reviews PR                                           │
│     • open the PDF (GitHub renders it or download)              │
│     • check the updated manifest looks right                    │
│     • merge → go to step 1 for phase X+1                        │
└─────────────────────────────────────────────────────────────────┘
```

### Why the manifest update is non-negotiable (step 2)

The manifest is the only thing that keeps later sessions grounded. If Claude Code
skips updating it after a phase, the next session starts with stale context and will
hallucinate details (wrong ports, missing tables, skipped ADRs). Always include the
manifest update as part of the same commit as the new phase document.

### When to ask in chat (claude.ai) vs. run Claude Code

Use **claude.ai chat** for: design questions, deciding whether to split a phase,
understanding an error, clarifying requirements.

Use **Claude Code** for: writing the phase document, rendering the PDF, updating the
manifest, committing to the repo. This keeps long document generation out of the
chat context window.

## Quality bar before delivering any phase

- The hands-on code is internally consistent and would actually run.
- No name/port/schema/endpoint contradicts the manifest or earlier phases.
- Every significant decision has an ADR; the phase ends with a SPEC + checklist.
- Fact vs inference is visibly separated.
- All diagrams rendered; accented characters and code highlighting look correct in
  the PDF.
- The manifest has been updated to reflect the new phase.
