---
name: game-design-document
description: >-
  Triggered ONLY by the slash command /game-design-document. Do not invoke this
  skill from natural-language requests like "write the game design", "document
  these features" or "create a design doc" — wait for the explicit command.
  Builds a comprehensive, non-technical Game Design Document for a game project
  or a single milestone of one. Takes scope from any issue tracker (Trello,
  Jira, Nulab Backlog, Linear, GitHub Projects) or from pasted text, and
  optionally adapts an existing reference project's documentation. Produces a
  numbered multi-file Markdown set — one file per feature, every rule and
  acceptance criterion carrying a stable ID a ticket can cite — with Mermaid
  diagrams and a combined print-ready PDF. Researches before writing, and stops
  for explicit confirmation on design decisions, conflicts and gaps before
  generating anything. Written for project managers, stakeholders and game
  designers: game design only, no software or technical design.
---

# /game-design-document

Turn a tracker board, a reference project and a pile of assumptions into a Game Design Document that a team lead can use as the single source of truth when writing SDDs, ADRs, backlog issues and development tasks.

## Usage

```
/game-design-document
```

Optionally name the scope up front:

```
/game-design-document Milestone 2 - Alpha
```

**Slash command only.** This skill produces a multi-hour deliverable and must never start because someone described wanting one. If a user asks conversationally for a game design document, tell them the command exists and let them run it.

## Workflow at a Glance

```
1. Gather      →  ask where scope, reference material and output belong
2. Research    →  read every source completely; write nothing yet
3. Analyse     →  derive features, surface conflicts and gaps
4. Confirm     →  propose design decisions — HARD STOP until approved
5. Write       →  generate the document set
6. Verify      →  IDs, diagrams, technical leaks, counts
7. Deliver     →  save, build the PDF, report what is still open
```

**Rule:** Phase 4 is never skipped and never assumed. Nothing is written until the user approves the decisions.

---

## Phase 1 — Gather project information

Ask for what you do not already have. Do not ask about anything the user has already supplied or that is obvious from the conversation.

**Ask as multiple choice where the options are clean, plain text otherwise:**

1. **Where does the scope come from?**
   - A tracker board — ask for the URL or board name
     - Trello, Jira, Nulab Backlog, Linear, GitHub Projects, or any other
     - Check whether a connector for it is available before promising to read it
   - Existing documentation — ask for `[path or None]`
   - Pasted text in the conversation
   - More than one of the above
2. **Is there a reference project to adapt from?** `[path or None]`
   - Its product docs, architecture docs, feature lists or wiki
   - State explicitly that it is reference only, and that its decisions will be adopted or rejected case by case, never copied wholesale
3. **Is there an art or asset source?** `[path or None]`
   - A purchased pack, a style guide, a Figma file. Used to keep the art direction section honest and to catch content the design assumes but the assets do not provide
4. **Where should the document be written?** `[output path]`
   - Suggest `<docs path>/design/GDD` and let the user override
5. **Whole game, or one milestone?**
   - One milestone is the common case and produces a sharper document. If a milestone, ask which one
6. **Output language(s)?** Default English unless the user says otherwise

**Do not start reading until these are answered.** Guessing the output path or the scope source wastes an entire research pass.

---

## Phase 2 — Research first

Read everything, completely, before writing a single line of the document.

**Hard rules for this phase:**

- **Write nothing.** No outline, no draft, no file.
- **Open no output-format skill** (docx, pdf, pptx or similar) yet. Those describe how to build a deliverable, and reading one now anchors you on document mechanics before you have anything correct to put in the document.
- **Read the tracker completely** — every list, card, description, checklist and comment. Card *descriptions* usually carry the real scope; card *titles* carry only the label.
- **Read the reference project's documentation completely.** Note what it does, and start a list of what you will deliberately not reuse.
- **Read the project's own existing documentation** — a repo guide, prior design docs, decision records. Check whether a GDD already exists that this one supersedes.
- **Inspect the art or asset source** if one was given. Verify what it actually contains rather than trusting its store description.

**When a source cannot be read** — an image attachment, a diagram, a board you have no connector for — say so plainly and ask the user to describe or paste it. Never infer the contents of something you could not open, and never present an inference as a finding.

---

## Phase 3 — Analyse

Build the working material. Still no document.

**Derive the feature list.** Group the scope into player-facing features — things a player experiences, not systems an engineer builds. "Time and day cycle" is a feature; "event bus" is not. Aim for 5 to 15; more than 15 usually means the grouping is too fine.

**Find the conflicts.** The most common and most damaging:

- The tracker's scope statement contradicts its own stated goal — a card promising two stages of work whose goal describes one.
- The reference project solved something one way and the project being documented implies another.
- Two sources disagree on a platform, a target or a headline number.

**Find the gaps.** Anything undecided that would change the shape of the document — control scheme, target platforms, core pacing, whether a system is in scope at all.

**Separate blocking from non-blocking.** A blocking gap changes what gets written. A non-blocking one becomes an open question with a proposed answer.

---

## Phase 4 — Confirm before generating

Present the decisions and **stop**.

**Format:** 3 to 5 questions, multiple choice, each option carrying its consequence — not just its label. Put the recommended option first and mark it. Then list the non-blocking gaps separately so the user can see them without having to answer them.

For each decision, state:

- What the conflict or gap is, and which sources disagree.
- What each option costs and what it buys.
- Which one you recommend and why.

End with:

> **Ready for me to write the GDD with these answers?** Reply yes, or tell me what to change.

**Do not generate any document content until the user explicitly approves.** If the user answers some questions and ignores others, use the stated proposed answer for the rest and say which ones you defaulted.

---

## Phase 5 — Write the document

Read `references/document-structure.md` now — it carries the full file map, the per-feature template and the ID conventions. The essentials:

**File set.** A README index, three orientation files (overview, scope, core loop), one file per feature, and three reference files (data tables, acceptance and playtest plan, glossary and open questions). Number the files so they sort.

**Every feature file follows the same eight sections:**

1. Purpose and role in the game
2. The player's experience — prose, what it feels like
3. Rules — a numbered table
4. A flow diagram, where one clarifies something prose cannot
5. Edge cases — a table of situation and behaviour
6. Acceptance criteria — a numbered table
7. Content or tuning tables, where the feature has content
8. Open questions

**Identifiers.** Features `F-01`…`F-nn`. Rules `F-05.R9`. Criteria `F-05.AC2`. These are the skill's main output for the team lead — every backlog issue and every SDD cites one, and that is what makes the document a source of truth rather than a description.

**Priority.** Must / Should / Stretch on every feature and, where it matters, on individual rules.

**Numbers.** Mark every value the team expects to change as *(tunable)* and collect all of them in one data-tables file, so balance changes never require touching a feature file.

**Traceability.** A table mapping each tracker item to its feature — **including features with no tracker item yet**. That column is usually the most valuable thing in the document, because it exposes the work nobody has ticketed.

**Adapting the reference project.** Reuse what fits; reject what does not, in writing. Every divergence gets a short callout naming what the reference does and why this project does otherwise. A silent divergence looks like an oversight six weeks later.

**Glossary.** Include a *words we do not use* section mapping the reference project's vocabulary to this project's, with the reason. Importing a word imports the design behind it — this section is the guard against that.

**Diagrams.** Mermaid, inside fenced blocks. One per idea that prose cannot carry: the core loop, a state machine, a screen flow, a dependency map. Keep them top-down rather than left-to-right — wide diagrams shrink to illegibility on a page.

**What must never appear:** class or type names, file paths, library or framework names, data schemas, field names, API shapes, architecture. If a technical detail is genuinely needed to explain a player-facing rule, state the rule and leave the mechanism out.

---

## Phase 6 — Verify

Read `references/quality-and-build.md` and run the checks it describes.

- **Cross-reference every ID.** Every `F-xx.Rn` and `F-xx.ACn` referenced anywhere must be defined somewhere, and must mean what the citing text claims.
- **Render every diagram.** A diagram that fails to parse is invisible in most viewers; one that renders illegibly is worse than none.
- **Scan for technical leaks.** Grep for engine, language and library names, and for file paths. Each hit is either a mistake or a deliberate reference to a tracker item — decide which.
- **Check the counts.** If the document states "82 criteria" or "10 features", verify the number.

---

## Phase 7 — Deliver

1. Write the Markdown set to the `[output path]` agreed in Phase 1.
2. Build the combined PDF using the recipe in `references/quality-and-build.md` — cover, contents, every section, diagrams rendered as images, IDs preserved as selectable text.
3. Report, in a few sentences: what was produced, the decisions that were applied, the open questions that remain and which of them block work, and any place where a source could not be read.

If the project keeps documentation in a shared workspace as well as a repository, offer to sync it there. Do not sync without asking.

---

## Size guide

| Size | Scope | Features | Rough output |
| --- | --- | --- | --- |
| **Small** | One milestone, a vertical slice or a prototype | 4–6 | 8–10 files, ~10k words |
| **Medium** | One substantial milestone | 8–12 | 15–18 files, ~25k words |
| **Large** | A whole game, or a feature-complete milestone | 15–25+ | 25+ files, 40k+ words |

Scale the per-feature depth, not the section list. Even a Small document keeps all eight sections per feature — a feature with two rules still needs its edge cases and its acceptance criteria.

---

## Quality Checklist

Before presenting the document, verify:

- [ ] Phase 4 happened and the user explicitly approved before anything was written
- [ ] Every feature file has all eight sections
- [ ] Every rule and criterion has a unique ID, and every cited ID resolves
- [ ] Every Mermaid diagram renders, and is legible at page width
- [ ] No class names, file paths, library names, schemas or architecture anywhere
- [ ] Every divergence from the reference project is called out with its reason
- [ ] The glossary includes the *words we do not use* mapping
- [ ] The traceability table shows features that have no tracker item yet
- [ ] Every tunable number appears in the data-tables file
- [ ] Stated counts match reality
- [ ] Open questions each carry a proposed answer and a blocking flag
- [ ] Anything a source could not supply is named as unknown, not guessed
