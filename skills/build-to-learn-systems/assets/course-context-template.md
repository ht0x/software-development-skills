# COURSE_NAME — Course Context File (vN)

> HOW TO USE: Paste this entire file at the start of each new session before asking
> for the next phase. It gives just enough context to continue consistently while
> spending very few tokens. It is updated after every phase — always use the newest
> version.

## A. Project context
- What is being built (system, target platform, integration).
- Nature: learning-first / real product / both. Team size, timeline, budget.
- "Build from scratch" allow-list and deny-list (what libraries/components are
  allowed; which managed products are forbidden and why).
- Output language. Fact-vs-inference rule.

## B. Target scale (design constraints)
| Metric | MVP | Production |
|--------|-----|------------|
| … | … | … |

> One or two sentences on the single insight that makes the hardest number feasible,
> and any explicit "we will NOT do X (over-engineering at this scale)" notes.

## C. Tech stack (locked)
- Core service(s): language/runtime + why.
- Any separate services (and their language) — note if the system is polyglot.
- Datastores, media storage, broker, load balancer, infra/hosting.

## D. Roadmap (full phase list)
| # | Name | Status |
|---|------|--------|
| 0 | Foundations & environment | ✅ DONE / ⏳ |
| 1 | … | ⏳ |

## E. Authoring conventions (unchanged across phases)
- Output format (PDF), pipeline summary.
- Diagrams (Mermaid). Per-phase structure. Target length.
- Callout types. ADR template. SPEC template.
- Schema evolution via migrations.
- Workflow: one phase at a time; wait for "done with Phase N".

## F. Canonical names book (later phases MUST NOT contradict)
- Repo name and directory layout.
- Service names, ports, project names.
- Connection conventions (host = service name inside containers, etc.).
- Data ownership (which service owns which tables).
- Any cross-service contracts (e.g. a token/JWT contract).
- Existing endpoints.

## F-bis. ADR ledger
- ADR-0001 — …
- ADR-0002 — …

## G. Per-phase summary & hooks
- **Phase 0 (DONE):** what it established + what later phases build directly on top of.
- Where cross-cutting features land (note them so they aren't forgotten).
- Hooks for upcoming phases (what each will create/modify).
- *(Fill "what it did" + "what later phases depend on" after each phase.)*

## H. Source of truth
- The delivered PDFs + the project repository (code, ADRs, phase docs).
- When exact detail is needed, paste the relevant file (or let a coding agent read
  the repo) instead of relying on the model's memory.
