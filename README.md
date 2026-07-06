# Software Development Skills

A curated plugin bundling skills for software development teams — from technical documentation and design docs to task specs, algorithmic art, and learning systems.

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `algorithmic-visual-art` | "create generative art", "algorithmic art" | Generate p5.js algorithmic art with seeded randomness |
| `architecture-decision-record-doc` | `/architecture-decision-record-doc`, "create an ADR for X" | Document long-term technical decisions and trade-offs |
| `build-to-learn-systems` | `/build-to-learn-systems`, "I want to learn X by building it" | Author phase-by-phase engineering course documents |
| `convert-documents-to-skill` | `/convert-documents-to-skill` | Convert any document into a ready-to-install Claude skill |
| `convert-skills-into-plugin` | `/convert-skills-into-plugin` | Convert existing SKILL.md file(s) into an installable Claude Code / Cowork plugin |
| `generate-mermaid-diagram` | `/generate-mermaid-diagram` | Generate valid Mermaid diagrams (flowchart, sequence, class, ER, graph, state) from code or a description |
| `learn-new-skill` | "teach me X", "explain X", "ELI5", "walk me through" | Structured learning sessions for concepts and techniques |
| `marketplace-plugin-scaffolder` | `/marketplace-plugin-scaffolder` | Scaffold a new Claude Code / Cowork marketplace plugin project from a set of skills |
| `mini-spec` | `/mini-spec` | Guided module work plan — goal, scope, constraints, agent tasks, done criteria; outputs as Markdown or Word in English or Vietnamese |
| `repo-wiki-light` | `/repo-wiki-light` | Generate a lightweight architecture wiki (README, architecture, data-flow, decisions, module pages) for any repo |
| `repo-wiki-standard` | `/repo-wiki-standard` | Generate a full config-driven repo wiki (wiki_plan.yaml, templates, Mermaid diagrams) with incremental updates |
| `request-for-comments-doc` | `/request-for-comments-doc`, "write an RFC for X" | Propose significant changes and gather team feedback |
| `software-design-doc` | `/software-design-doc`, "create a design doc for X" | Design documents for cross-functional alignment before coding |
| `software-requirement-specification-doc` | `/software-requirement-specification-doc`, "create an SRS for X" | Nail down requirements before design or implementation |
| `spec-driven-development-doc` | `/spec-driven-development-doc`, "write a feature spec for X" | Bridge approved requirements into trackable implementation specs |
| `system-architecture-doc` | `/system-architecture-doc` | Document system structure — components, data models, interfaces, risks — with Mermaid context diagrams |
| `task-process-report-doc` | `/task-process-report-doc`, "create a process report for X" | Track implementation history from planning through review |
| `task-template` | `/task-template`, "create a task for X" | Produce clear, ready-to-start task definitions |
| `unity-software-design-doc` | `/unity-software-design-doc` | Unity-specific SDD covering scene structure, MonoBehaviour/DOTS design, save/load, and asset pipeline |

## Usage

Each skill can be triggered by its slash command (e.g., `/software-design-doc`) or by natural language phrases listed in the table above. Skills scale their output to the complexity of your task.

## Installation

### As a Claude Code plugin (recommended)

```bash
/plugin marketplace add ht0x/software-development-skills
/plugin install software-development-team-90@software-development-team-90
```

Skills are then available under the plugin namespace, e.g.:

```bash
/software-development-team-90:task-template
/software-development-team-90:software-design-doc
```

### Standalone (any Agent Skills tool)

Copy individual skill folders into your `.claude/skills/` directory:

```bash
cp -r skills/task-template ~/.claude/skills/
```

Each folder is self-contained and works in any agent that follows the Agent Skills spec.

## Requirements

No environment variables or external services required. All skills work out of the box.
