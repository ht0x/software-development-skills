---
name: generate-mermaid-diagram
description: >-
  PRIMARY PURPOSE: generate valid, renderable Mermaid diagrams from codebase
  analysis or a plain description. Supports 6 diagram types: flowchart,
  sequenceDiagram, classDiagram, erDiagram, graph, and stateDiagram-v2.
  Triggered only by the slash command /generate-mermaid-diagram. Asks whether
  to output inline in chat or save to a .md file. Works from attached code
  files or from a description — no domain restriction.
---

# /generate-mermaid-diagram

Generate a valid, renderable Mermaid diagram from codebase analysis or a plain description. Supports 6 diagram types and two input modes.

## Usage

```
/generate-mermaid-diagram [type] [source]
```

Slash command only — does not trigger conversationally.

- `[type]` (optional): `flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `graph`, or `stateDiagram-v2`. If omitted, infer from context.
- `[source]` (optional): a description, or attach code files for analysis.

Examples:
```
/generate-mermaid-diagram sequenceDiagram  ← attach code files
/generate-mermaid-diagram flowchart The user logs in, picks a plan, checks out
/generate-mermaid-diagram  ← describe what you need and Claude will infer the type
```

## Workflow at a Glance

```
1. Detect   →  identify diagram type from argument, trigger phrase, or context
2. Gather   →  read input: scan code files or parse the user's description
3. Ask      →  confirm output mode (inline in chat or save to .md file)
4. Generate →  build valid Mermaid syntax following all rules
5. Validate →  check syntax, node count, and offer to split if needed
```

---

## Phase 1 — Detect Diagram Type

Choose the diagram type using this priority order:

1. Explicit argument passed by the user (e.g., `/generate-mermaid-diagram erDiagram`)
2. Inferred from the description or code content

Use this mapping to infer type from context:

| Diagram type | Best for |
|---|---|
| `flowchart` | Process flows, request handling, business logic |
| `sequenceDiagram` | API call sequences, service interactions, message passing |
| `classDiagram` | Module structure, class relationships, interfaces |
| `erDiagram` | Database schema, entity relationships |
| `graph` | Dependency trees, module relationships, build graphs |
| `stateDiagram-v2` | State machines, workflow states, lifecycle transitions |

Default to `flowchart` if the type cannot be determined.

---

## Phase 2 — Gather Input

### If generating from code (attached files present):

- **Imports / exports** → map module dependencies (use for `graph` or `classDiagram`)
- **Route definitions** → extract request flow (use for `sequenceDiagram` or `flowchart`)
- **Database schemas** → parse tables and foreign keys (use for `erDiagram`)
- **Class / interface definitions** → extract hierarchy and relationships (use for `classDiagram`)
- **State transitions** → identify states and triggers (use for `stateDiagram-v2`)

Scan only the files needed for the chosen diagram type. Do not read unrelated files.

### If generating from description:

Parse the user's requirements directly. Ask one clarifying question if the description is genuinely ambiguous about structure — otherwise proceed.

---

## Phase 3 — Ask Output Mode

Before generating, ask:

> Should I output this inline in chat, or save it to a `.md` file?

- **Inline**: output the Mermaid block directly in the response, with a one-sentence description above it.
- **Save to file**: write to `/mnt/user-data/outputs/<diagram-name>.md` and call `present_files`.

---

## Phase 4 — Generate the Diagram

Build the Mermaid syntax and wrap it in the standard format:

````markdown
```mermaid
<diagram-type>
    <nodes and relationships>
```
````

Always include a brief plain-text description above the code block explaining what the diagram shows.

### Rules — enforce all of these:

- **Max 20 nodes** — if the content exceeds 20 nodes, split into multiple focused diagrams and note what each covers.
- **Descriptive labels** on all edges and nodes — avoid generic names like `A`, `B`, `node1`.
- **Consistent naming** — use naming conventions that match the codebase or description provided.
- **Subgraphs** for grouping related components (services, layers, domains).
- **Focused scope** — each diagram should show one aspect of the system clearly; do not try to show everything in one diagram.

---

## Phase 5 — Validate

Before presenting, verify:

- Mermaid syntax is correct and will render (check for unclosed brackets, invalid arrow types, missing quotes on labels with spaces).
- Node count is ≤ 20; if over, split and note the split.
- All edges have labels where the relationship is non-obvious.
- Subgraphs are used where there are 3+ nodes in the same logical group.
- The description above the block accurately describes what is shown.

If saving to file: confirm the file was written and present it with `present_files`.

---

## Quality Checklist

Before presenting the output, verify:
- [ ] Skill name is `generate-mermaid-diagram` and matches the frontmatter `name` field
- [ ] Description is under 1024 characters
- [ ] No conversational trigger phrases in description (slash-only skill)
- [ ] Output mode was asked before generating
- [ ] Diagram type was correctly detected or inferred
- [ ] Input mode (code scan vs description) was applied correctly
- [ ] All 6 rules from Phase 4 are satisfied
- [ ] Syntax validated — no unclosed brackets, invalid arrows, or unquoted labels with spaces
- [ ] Node count ≤ 20, or split with explanation if over
- [ ] Brief plain-text description appears above the Mermaid block
