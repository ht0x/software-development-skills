# Mermaid diagram conventions

Diagrams make structure legible. Embed them in pages as fenced ```mermaid blocks.
Keep them small and truthful — a diagram must reflect what the code actually does.
Prefer several focused diagrams over one sprawling one.

## Rules

- Use stable, code-derived node IDs (module or file names). Keep IDs identical
  across language trees so diagrams stay comparable between languages.
- Label edges with the nature of the relationship where it isn't obvious
  (`calls`, `depends on`, `publishes`, `reads`).
- Don't diagram trivial or speculative relationships. If unsure, omit.
- Validate syntax mentally; a broken diagram is worse than none.

## Architecture / component graph

Use on the Architecture Overview page.

```mermaid
graph TD
  Client[Client / UI]
  API[API Layer]
  Svc[Service Layer]
  Repo[Repository / Data Access]
  DB[(Database)]
  Client --> API --> Svc --> Repo --> DB
```

## Module dependency graph

Use on the Dependencies page. Direction = "depends on".

```mermaid
graph LR
  auth --> users
  orders --> users
  orders --> payments
  payments --> external_gateway[External Gateway]
```

## Sequence diagram (key flow)

Use for request lifecycles, auth, or the core domain workflow.

```mermaid
sequenceDiagram
  participant U as User
  participant API
  participant Svc as OrderService
  participant DB
  U->>API: POST /orders
  API->>Svc: createOrder(payload)
  Svc->>DB: insert order
  DB-->>Svc: order id
  Svc-->>API: 201 Created
  API-->>U: order confirmation
```

## Entity-relationship diagram (data model)

Use on Data & Persistence / Domain Model pages when a schema exists.

```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "referenced by"
```

## Directory structure (onboarding)

A flowchart works for a project-layout tour:

```mermaid
graph TD
  root[repo/] --> src[src/]
  root --> tests[tests/]
  src --> api[api/]
  src --> core[core/]
  src --> db[db/]
```

Choose the diagram type that matches the relationship: `graph` for structure and
dependencies, `sequenceDiagram` for flows over time, `erDiagram` for data models.
