---
name: request-for-comments-doc
description: >-
  PRIMARY PURPOSE: start team discussion, gather feedback, and work through
  cross-team or high-risk changes before implementation begins. Written
  primarily for Team Leads and Tech Leads. Generates a filled-in Request
  for Comments (RFC) document. Works across domains (web, backend, game,
  mobile, desktop). Trigger with "/request-for-comments-doc", "write an RFC
  for X", "draft a proposal for changing Y", "I want to propose a
  significant change to...", or whenever a change is cross-team, high-risk,
  or contentious enough to need discussion before a decision is locked in.
  Not needed for decisions that are already settled (use
  architecture-decision-record-doc instead) or for small, uncontroversial
  changes.
disable-model-invocation: true
---

# /request-for-comments-doc

Generate a complete, filled-in Request for Comments (RFC) — a proposal document meant to invite discussion and feedback on a significant technical change *before* a decision is locked in.

## Usage

```
/request-for-comments-doc $ARGUMENTS
```

Example: `/request-for-comments-doc switching the save system to a cloud-backed format`

This skill also activates conversationally — e.g. "draft an RFC for moving our backend to event-driven architecture" — without needing the slash form.

## What an RFC Is For (and How It Differs from an ADR)

An RFC and an ADR (`architecture-decision-record-doc`) both discuss alternatives and consequences, but they serve different moments in a decision's life:

- An **RFC** proposes and opens a change for discussion **before** anything is decided. It's meant to be read, debated, and revised by reviewers — genuinely open questions are a feature, not a gap to fill in.
- An **ADR** records a decision **after** it's been made, as a durable reference for why that choice was final.

If the user already knows what they've decided and just wants it documented, point them to `architecture-decision-record-doc` instead — that's the better fit. Use this skill when the point is to propose something and invite pushback, not to record a settled outcome.

## When to Use This vs Something Else

Use the full RFC when a change is significant enough, or contentious enough, that it benefits from being written down and reviewed by others before implementation starts — a major architecture shift, a cross-cutting technical change, or anything where getting buy-in matters.

Skip it for changes that are small, uncontroversial, or already decided. If the user invokes this skill for something that doesn't need discussion, say so and ask whether they actually want an ADR (decision already made) or a lighter note instead.

## Workflow at a Glance

```
1. Elicit   →  ask about context/problem, goals, proposed solution, alternatives, risks, rollout
2. Draft    →  fill the RFC, using genuine open questions where discussion is the point
3. Flag     →  separate "open for debate" (author's deliberate choice) from "TODO" (a real info gap)
4. Deliver  →  ask output format (Markdown or DOCX), then generate and present the file
```

---

## Phase 1 — Elicit the Proposal

RFCs need enough substance to be a real discussion-starter, not just a list of questions for the reader to answer. Ask a full round, similar in depth to the ADR skill, but oriented toward proposing rather than recording:

**Context & problem**
- What's the situation today? What problem, limitation, or opportunity motivates this proposal?

**Goals & non-goals**
- What should this change achieve? What's explicitly out of scope, even if related?

**Proposed solution**
- What is the author actually proposing? This should be a real, concrete proposal — not just "we should do something about X."

**Alternatives considered**
- What other approaches could address the same problem? What are the trade-offs of each, including the one being proposed? If there's genuinely only one viable approach, say so rather than inventing alternatives.

**Risks**
- What could go wrong with the proposed approach? What's uncertain or debatable about it?

**Rollout**
- How would this change be introduced — all at once, phased, behind a flag, gradually migrated? Any rollback consideration?

Don't force every question if context already answers it. If the user pushes back on answering everything ("just draft something so I can iterate"), proceed with what's given and use open questions (see Phase 3) for the genuinely undecided parts — that's appropriate for this document type, unlike the other skills in this family.

---

## Phase 2 — Draft the Document

Fill in every section using gathered context.

### Document Template

```markdown
# [Proposal Title]

## Context
[The situation today. What exists, what constraints apply, why this is coming up now.]

## Problem
[The specific problem, limitation, or gap this proposal addresses. Should be concrete enough that a reader unfamiliar with the backstory understands why this matters.]

## Goals
- `[Goal 1]`
- `[Goal 2]`

## Non-Goals
- `[Explicitly out of scope, even if related]`

## Proposed Solution
[The actual proposal — what would change, at a level of detail sufficient for reviewers to evaluate it. Concrete enough to critique, not just a direction.]

## Alternatives Considered

### Option A: [Name]
[Description, and why it's a real alternative — not a strawman.]

Trade-offs:
- `[trade-off]`

### Option B: [Name]
[Description.]

Trade-offs:
- `[trade-off]`

*(Add or remove options to match what was genuinely considered. If only one viable approach exists, state that directly rather than inventing alternatives to fill space.)*

## Risks
- `[Risk 1, including how serious/likely it is if known]`
- `[Risk 2]`

## Rollout Plan
[How this would be introduced — phased, flagged, big-bang, gradual migration — and what rollback looks like if something goes wrong.]

## Open Questions
[Genuine points the author wants reviewers to weigh in on — not a substitute for things the author should have figured out before writing this. Phrase these as real questions inviting a position, e.g. "Should this also cover Y, or is that a separate follow-up RFC?"]

- `[Open question 1]`
- `[Open question 2]`
```

---

## Phase 3 — Separate Open Questions from Genuine Gaps

This is the key distinction for this document type, and it cuts the other way from the other skills in this family:

- **Open Questions** section: use this for things the author is deliberately leaving for reviewer input — a real fork in the design space, a values trade-off the team should weigh in on, or something genuinely debatable. This is a feature of a good RFC, not a sign of an incomplete one.
- **Everywhere else in the document**: if a section would otherwise be filled with a guess rather than something the user actually stated, don't dress it up as an "open question" to avoid an honest gap. Either ask the user directly, or mark it `TODO: [what's needed]` the same way the other skills do. An RFC with a vague Proposed Solution because the author hasn't actually decided what they're proposing yet isn't a good RFC — it's an unfinished one.

In short: genuine debate goes in Open Questions; missing information the user didn't provide gets a `TODO:`, not a rephrased question.

Also watch for:
- Alternatives Considered — don't invent a second option as a strawman just to make the proposed solution look better by comparison.
- Risks — don't pad this with generic boilerplate ("there could be unforeseen issues"); only include risks that are real, specific implications of this particular proposal.

---

## Phase 4 — Deliver

Ask the user which output format they want:

| Format | Action |
| --- | --- |
| **Markdown (.md)** | Read `/mnt/skills/public/md` conventions if relevant, write the filled document directly as a `.md` file |
| **DOCX** | Read `/mnt/skills/public/docx/SKILL.md` before generating — follow its formatting and table guidance |

Save the file to `/mnt/user-data/outputs/`, then use `present_files` to share it. Use the proposal title for the filename, e.g. `rfc-cloud-save-migration.md`.

Keep the chat response brief: a short note on what was filled vs. what's left as a genuine open question or TODO, then the file. Don't restate the whole document inline if it's already being delivered as a file.

If the proposal sounds like it's actually already decided rather than open for discussion, mention that `architecture-decision-record-doc` might be the better fit going forward — but don't switch documents unprompted.

---

## Quality Checklist

Before presenting the document, verify:
- [ ] Proposed Solution is a real, concrete proposal — not a restated problem statement
- [ ] Alternatives Considered reflects genuinely evaluated options, not strawmen
- [ ] Risks are specific to this proposal, not generic boilerplate
- [ ] Open Questions contains genuine discussion points the author chose to raise, not disguised information gaps
- [ ] Anything that's a real information gap (not a deliberate open question) is marked `TODO:`, not folded into Open Questions
- [ ] Rollout Plan is concrete enough to act on, not just "roll it out carefully"
