---
name: mini-spec
description: >-
  Triggered by /mini-spec. Guides you through writing a structured module work
  plan — collecting module name, goal, scope (included/excluded), constraints
  (tech stack, scale, client, security), design questions, need-to-learn topics,
  and done criteria. Asks for output language (English, Vietnamese, or other) and
  format (Markdown or Word file) before generating. Optional sections: agent task
  assignments and final decisions. General-purpose — works for any tech domain.
disable-model-invocation: true
---

# /mini-spec

Guide the user through filling a structured module work plan (mini spec), then generate it as a Markdown or Word file in their chosen language.

## Usage

```
/mini-spec
```

No arguments needed. The skill walks through each section interactively.

## Workflow at a Glance

```
1. Language & format  →  Ask output language and file format
2. Core info          →  Module name and goal
3. Scope              →  What's included and excluded
4. Constraints        →  Tech stack, scale, client context, security assumptions
5. Required sections  →  Design questions, need-to-learn, done criteria
6. Optional sections  →  Offer agent tasks and final decisions
7. Confirm            →  Show summary, wait for approval
8. Generate           →  Produce the output file and present it
```

---

## Phase 1 — Language & Format

Ask the user two questions before collecting any content:

**Output language** — present three options:
- English
- Vietnamese (Tiếng Việt)
- Other — ask them to specify

**Output format** — present two options:
- Markdown file (`.md`)
- Word document (`.docx`)

Remember both choices. All generated content (section headings, placeholder text, labels) must be written in the chosen language. If the user chose a language other than English or Vietnamese, confirm the language name before proceeding.

---

## Phase 2 — Module Name & Goal

Ask for:

1. **Module name** — a short, descriptive name for the module or feature (e.g., "Text Chat Delivery", "User Authentication", "Payment Checkout").

2. **Goal** — what this module must achieve. Prompt the user to describe it as a short bullet list of outcomes, for example:
   - User A sends a text message to User B.
   - If User B is online, deliver immediately.
   - If User B is offline, store and deliver after reconnect.

If the user gives a paragraph instead of bullets, reformat it into bullets silently.

---

## Phase 3 — Scope

Ask the user to define the boundary of the module:

**Included** — what is explicitly part of this module's responsibility.

**Excluded** — what is out of scope (even if related). Prompt with an example: "What are you deliberately NOT building in this slice?"

Both fields accept bullet lists. If the user leaves one blank, note it as `(not specified)` in the output — do not invent content.

---

## Phase 4 — Constraints

Ask for the following constraint categories one at a time, or all together if the user prefers:

| Category | Prompt |
|---|---|
| Tech stack | Backend language/framework, transport layer, database, cache/pubsub — list what's decided. |
| Scale | How many concurrent users at launch? What's the target after growth? |
| Client | What clients consume this module? (web, mobile, desktop, internal service) |
| Security assumptions | What security boundaries are assumed? (e.g., authenticated users only, TLS required, no client-side trust) |

Any category the user leaves blank is rendered as `(not specified)` in the output.

---

## Phase 5 — Required Sections

Collect content for the three sections that are always included:

### Design questions

Ask: "What questions need to be resolved before or during implementation?"

Accept a bullet list. If the user has none yet, write `(none yet)` — do not fabricate questions.

### Need to learn

Ask: "What topics do you need to research or understand better before you can implement this?"

Examples to suggest if the user is stuck: message persistence strategy, WebSocket lifecycle, retry/ack patterns, duplicate prevention, ordering guarantees.

### Done criteria

Ask: "How will you know this module is complete?"

Default checklist to offer (user can edit):
- Code compiles with no errors
- Tests pass (unit + integration)
- I can explain the data flow end-to-end
- I can explain failure behavior
- I can run it locally

Let the user add, remove, or replace items.

---

## Phase 6 — Optional Sections

Offer two optional sections. Ask: "Do you want to include either of these?"

### Agent tasks (optional)

If yes, ask which agents are involved. Default set:

| Agent | Default responsibility |
|---|---|
| Architect Agent | Design the module. No code. |
| Reliability Agent | Review failure cases and edge cases. |
| Security Agent | Review hostile client scenarios. |
| Implementation Agent | Implement only the approved first slice. |
| Test Agent | Write tests for expected behavior and failure cases. |

The user can add, remove, or rename agents and their responsibilities.

### My final decisions (optional)

If yes, leave a blank bullet list for the user to fill in after reviewing design questions and agent output. Render as empty bullets in the output, not `(not specified)`.

---

## Phase 7 — Confirm Before Generating

Present a compact summary of everything collected:

```
Module:      [name]
Goal:        [N bullets]
Language:    [English / Vietnamese / other]
Format:      [Markdown / Word]
Sections:    Core + Design questions + Need to learn + Done criteria
             [+ Agent tasks] [+ Final decisions]
```

Then ask: **"Ready to generate? Reply yes to proceed or tell me what to change."**

Do not generate any output until the user explicitly confirms.

---

## Phase 8 — Generate Output

After confirmation, assemble the complete mini spec using the structure below. Write all content in the chosen language.

### Output structure

```
# [Module name]

## 1. Module name
[name]

## 2. Goal
- [bullet 1]
- [bullet 2]
...

## 3. Scope

Included:
- ...

Excluded:
- ...

## 4. Constraints
- Tech stack: [value or "(not specified)"]
- Scale: [value or "(not specified)"]
- Client: [value or "(not specified)"]
- Security assumptions: [value or "(not specified)"]

## 5. Design questions
- ...

## 6. Need to learn
- ...

## 7. Agent tasks          ← omit if user skipped
### [Agent name]
[responsibility]
...

## 8. My final decisions   ← omit if user skipped
- 

## 9. Done criteria
- [ ] ...
```

### File output

**If Markdown:**
Save to `/mnt/user-data/outputs/mini-spec/[module-name-kebab-case].md`

**If Word:**
Read the docx SKILL.md at the skills path and follow its instructions to produce a `.docx` file.
Save to `/mnt/user-data/outputs/mini-spec/[module-name-kebab-case].docx`

Call `present_files` with the output path.

---

## Quality Checklist

Before presenting output, verify:
- [ ] All content is written in the language the user chose in Phase 1
- [ ] Module name and goal match what the user provided exactly — no paraphrasing
- [ ] Blank fields render as `(not specified)`, not invented content
- [ ] Omitted optional sections are completely absent from the output (no empty headings)
- [ ] Done criteria uses `- [ ]` checkbox format
- [ ] Output file is saved to `/mnt/user-data/outputs/mini-spec/` and presented via `present_files`
- [ ] If Word format: docx skill was invoked, not a raw markdown file renamed to .docx
