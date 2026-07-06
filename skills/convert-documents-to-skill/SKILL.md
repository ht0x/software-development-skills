---
name: convert-documents-to-skill
description: >-
  Triggered ONLY by the slash command /convert-documents-to-skill. Converts
  an existing document (template, workflow, process doc, or any structured
  reference) into a ready-to-install Claude skill. Works across all domains
  — web, backend, game, mobile, desktop. The skill asks for a skill name if
  not provided, reads the source document thoroughly, proposes a conversion
  plan with frontmatter, workflow phases, and quality checklist, asks for
  confirmation before generating, then produces the final SKILL.md. Never
  proceeds to generation without explicit user confirmation of the plan.
disable-model-invocation: true
---

# /convert-documents-to-skill

Convert an existing document — a template, workflow guide, process doc, checklist, or any structured reference — into a properly structured Claude skill (a `SKILL.md` file with YAML frontmatter, phased workflow, and quality checklist), ready to install or package into a plugin.

## Usage

```
/convert-documents-to-skill
```

The user must also provide the source document, either:
- Uploaded as a file attachment, or
- Pasted inline in the conversation.

The skill name is either passed explicitly or asked for during Phase 1.

## Workflow at a Glance

```
1. Read       →  parse the source document thoroughly before doing anything else
2. Elicit     →  ask for the skill name (if missing) + any conversion requirements
3. Plan       →  propose the full conversion plan for user confirmation
4. Confirm    →  WAIT for explicit approval — never proceed without it
5. Generate   →  write the SKILL.md following all skill writing conventions
6. Package    →  write to /mnt/user-data/outputs/ and present the file
```

**Rule**: Steps 3 and 4 are never skipped. The user must see and approve the plan before any SKILL.md is generated.

---

## Phase 1 — Read and Elicit

### 1.1 Read the source document first

Before asking anything, read the entire source document carefully. Identify:

- **Purpose**: What does this document help someone do?
- **Audience**: Who uses it — developer, PM, QA, designer, agent?
- **Structure**: Is it a template (fill-in-the-blank), a guide (step-by-step instructions), a reference (lookup tables/schemas), or a mixed format?
- **Domain signals**: Are there domain-specific terms (Unity, React, SQL, mobile, backend)? Are they fundamental to the document or incidental?
- **Trigger vocabulary**: What user phrases would naturally lead someone to want this skill? What slash command would feel natural?
- **Size/complexity**: How many workflow phases will the skill need? Is a `references/` subfolder warranted for heavy content?

### 1.2 Elicit missing information

After reading, check what's still needed. Ask only for what is genuinely unclear — don't ask about things already obvious from the document or the conversation.

**Always confirm (if not already stated):**
- **Skill name** — ask if not provided. Must be kebab-case, lowercase, descriptive. Suggest a name based on the document and let the user confirm or override it.
- **Trigger mode** — slash-command only, conversational auto-trigger, or both? Default: both (slash + auto), unless the user says otherwise.
- **Domain scope** — should the skill be general-purpose (web/backend/game/mobile/desktop) or locked to a specific domain? If the source document is domain-specific (e.g. Unity-only), ask whether to generalize it or keep it domain-specific.
- **Target audience** — who will use this skill? (developer, PM, QA, agent, any)
- **Output format** — should the generated skill produce Markdown files, DOCX files, or ask the user each time?
- **Confirmation requirement** — should the skill ask for user confirmation before generating its output? Default: yes, unless the user says otherwise.

Use `ask_user_input_v0` for questions that fit clean multiple-choice options (trigger mode, domain scope, output format). Use plain text for the skill name and any open-ended questions.

---

## Phase 2 — Propose the Conversion Plan

After eliciting, prepare a concise conversion plan and present it to the user **before writing any SKILL.md**. The plan must cover:

### Plan structure to present:

**1. Proposed skill name and trigger**
- `name: <kebab-case-name>`
- Trigger: slash command `/name`, conversational phrases (list 3–5 example trigger phrases), or slash-only

**2. Description summary**
- One sentence describing what the description will say and what trigger phrases it will include.
- Note the character limit: the description field must stay under 1024 characters.

**3. Workflow phases**
- A numbered list of phases the skill will use, each with a one-line summary of what happens in that phase.
- Explicitly note which phases will ask the user questions and which will produce output.

**4. Domain generalization decisions**
- If the source document has domain-specific content (e.g. Unity paths, React-specific fields), list what will be generalized (turned into domain-hint sub-bullets) and what will be kept as-is.

**5. Sections dropped or condensed**
- If any sections of the source document are being dropped, merged, or restructured, explain why briefly.

**6. References folder**
- Will a `references/` subfolder be created? If yes, what goes in it and why?

**7. Confirmation behavior**
- Will the generated skill ask the user to confirm a plan before generating its own output? (Default: yes)

Then end the plan with:

> **Ready to generate the SKILL.md with this plan?** Reply "yes" or "go ahead" to proceed, or tell me what to change.

Do not write any SKILL.md content yet. Wait for explicit confirmation.

---

## Phase 3 — Await Confirmation

Wait for the user's response. Accept any of the following as confirmation: "yes", "go ahead", "looks good", "do it", "proceed", or similar unambiguous approval.

If the user requests changes, update the plan and present the revised plan again. Repeat until confirmed.

If the user says "skip confirmation" or "just generate it", treat that as immediate confirmation and proceed.

---

## Phase 4 — Generate the SKILL.md

Only after confirmation, generate the full `SKILL.md` using the approved plan. Follow all conventions below.

### SKILL.md writing conventions

**Frontmatter**

```yaml
---
name: kebab-case-name
description: >-
  [One paragraph. Start with what triggers this skill. List slash command
  and/or conversational trigger phrases. State what the skill does and what
  it produces. Mention domain scope (general or specific). Stay under 1024
  characters — check with len() before writing.]
---
```

**Body structure** — use this ordering:

```
# /skill-name

[One-sentence purpose statement]

## Usage
[Slash command syntax + example + note on conversational trigger if applicable]

## Workflow at a Glance
[Numbered list of phases, one line each, using → format]

---

## Phase 1 — [Name]
[...]

## Phase N — [Name]
[...]

## Quality Checklist
[Bullet list of things to verify before presenting output]
```

**Generalization rules**

When the source document has domain-specific content, apply these rules:
- Replace hardcoded tool paths (e.g. `GameClient/dev/docs/`) with `[path or None]` placeholders.
- Replace domain-only field names (e.g. "Unity scene, prefab, ScriptableObject") with domain-hint sub-bullets:
  ```
  - Asset/config/data changes: [Yes / No, details]
    - For web/backend: migration files, API schema, config files
    - For game: scenes, prefabs, ScriptableObjects, level data
    - For mobile/desktop: platform-specific resources, manifests
  ```
- Replace test type names that are engine-specific (e.g. "EditMode / PlayMode") with general equivalents first, then list engine-specific variants in a hint:
  ```
  - Test type: Unit / Integration / E2E / Manual / Review
    - For Unity: EditMode / PlayMode
    - For web: Jest / Cypress / Playwright
  ```
- Keep terms that are domain-specific but universally understood (e.g. "API contract", "migration", "schema") without modification.

**Size-scaling rules** (for skills that generate documents)

If the source document has sections labeled as optional, recommended, or required, preserve that scaling logic in the skill. Add a size guide table if the source document implies different effort levels:

| Size | Definition |
| --- | --- |
| Small | ... |
| Medium | ... |
| Large | ... |

**Confirmation phase** (if the skill itself should confirm before generating output)

If the approved plan includes a confirmation step, add a phase like this:

```markdown
## Phase N — Confirm Before Generating

Present a summary plan to the user before writing any output:
- [what the plan covers]
- End with: "Ready to generate? Reply yes to proceed or tell me what to change."

Do not generate any output until the user explicitly confirms.
```

**Quality checklist** — always include at the end of the skill body:

```markdown
## Quality Checklist

Before presenting the output, verify:
- [ ] Skill name is kebab-case and matches the frontmatter `name` field
- [ ] Description is under 1024 characters
- [ ] Trigger phrases in the description match how the skill actually behaves
- [ ] No domain-specific content left as hardcoded paths or engine-only field names
- [ ] No section is silently dropped — dropped sections are mentioned in the plan
- [ ] TODO markers used for genuinely unknown fields, not invented placeholders
- [ ] Output file saved to /mnt/user-data/outputs/ and presented with present_files
```

---

## Phase 5 — Package and Deliver

After generating the SKILL.md:

1. Check the description character count:
```python
# Run this check before saving
desc = "..."  # the description field value
assert len(desc) <= 1024, f"Description is {len(desc)} chars — trim it"
```

2. Save to a working directory first:
```
/home/claude/<skill-name>/SKILL.md
```

3. Package using the skill-creator packager if available:
```bash
cd /mnt/skills/examples/skill-creator && python3 -m scripts.package_skill /home/claude/<skill-name> /mnt/user-data/outputs
```

4. If the packager is unavailable, copy the file directly:
```bash
mkdir -p /mnt/user-data/outputs/<skill-name>
cp /home/claude/<skill-name>/SKILL.md /mnt/user-data/outputs/<skill-name>/SKILL.md
```

5. Call `present_files` with the output path. Then add a brief note (2–3 sentences) stating:
   - What the skill does
   - Where to install it: drop the folder into `/mnt/skills/user/<skill-name>/` or use it as a plugin skill under `skills/<skill-name>/`
   - Any TODOs the user should manually review before installing

---

## Quality Checklist

Before presenting the SKILL.md, verify:
- [ ] Description is under 1024 characters (checked with `len()`)
- [ ] Trigger phrases in description match the skill's actual trigger behavior
- [ ] Slash-only vs auto-trigger matches what the user specified
- [ ] No domain-specific hardcoded paths or engine-only field names remain (unless domain-specific was explicitly requested)
- [ ] Confirmation phase is present if the user requested it (or if the source document implies a confirm-before-generate pattern)
- [ ] No source document section is silently dropped — all drops/merges are noted in the plan
- [ ] Output file is saved and presented via `present_files`
