# Architecture Document Selection Guidance

## Document Status
Draft

## Purpose
Define how to decide which architecture documents are needed for a project based on architecture style, risk, complexity, and implementation needs.

## Owner
Architecture Team

## Last Updated
2026-07-03

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## 1. Core Rule

Do not create architecture documents merely because a framework offers a document type.

Create or expand architecture documents when they answer questions required for safe implementation, review, operation, or change.

## 2. Baseline Documents

Every project should normally start with these baseline documents:

| Document | Why It Exists |
|---|---|
| `architecture/context/business-context.md` | Defines the business reason for the system. |
| `architecture/context/system-context.md` | Defines system purpose, scope, and boundary. |
| `architecture/context/actors-and-roles.md` | Defines users, operators, system actors, roles, and permissions. |
| `architecture/context/external-systems.md` | Defines external dependencies and integration ownership. |
| `architecture/architecture-clarity-checklist.md` | Tests whether the architecture is clear enough for implementation. |
| `glossary.md` | Defines project vocabulary used in architecture, design, and code. |
| `decisions/` | Captures material architecture decisions. |
| `governance/risks.md` | Captures material architecture and delivery risks. |
| `governance/assumptions.md` | Captures assumptions until confirmed. |
| `governance/open-questions.md` | Captures unresolved questions and owners. |

## 3. View Selection Rules

| Trigger | Add or Expand | Reason |
|---|---|---|
| Multiple modules, services, bounded contexts, or deployable units exist. | `architecture/views/logical-view.md` | Clarifies responsibilities and dependencies. |
| Data ownership, classification, retention, or reporting matters. | `architecture/views/data-view.md` | Prevents data-boundary and lifecycle mistakes. |
| APIs, events, files, queues, webhooks, or third-party integrations exist. | `architecture/views/integration-view.md` | Clarifies contracts and message flow. |
| Runtime placement, environments, or infrastructure shape matters. | `architecture/views/deployment-view.md` | Clarifies where the system runs and environment assumptions. |
| Identity, authorization, privacy, compliance, or sensitive data matters. | `architecture/views/security-view.md` | Clarifies security boundaries and responsibilities. |
| Specific subsystem complexity exists. | `architecture/systems/<system-name>/` | Provides focused architecture for a subsystem or bounded context. |

## 4. Architecture Style Selection

Architecture style affects which documents need more depth.

| Architecture Style | Documents That Usually Need More Depth | Primary Reason |
|---|---|---|
| Layered Architecture | Logical View, Technical Standards, ADRs | Clarifies layer responsibilities and dependency direction. |
| Modular Monolith | Logical View, Data View, ADRs, System Folder Docs | Clarifies module boundaries and ownership. |
| Microservices | System Context, Logical View, Integration View, Deployment View, Data View, Security View, ADRs | Clarifies service boundaries, contracts, deployment, and ownership. |
| Event-Driven Architecture | Integration View, Data View, Security View, ADRs | Clarifies event ownership, schemas, ordering, and failure handling. |
| Serverless Architecture | Deployment View, Integration View, Security View, Operational Standards | Clarifies managed services, triggers, permissions, and runtime assumptions. |
| Data-Intensive System | Data View, Integration View, Quality Attributes, Security View | Clarifies data lifecycle, classification, and data movement. |
| AI-Enabled System | Data View, Integration View, Security View, Quality Attributes, ADRs | Clarifies data sources, model boundaries, evaluation, risk, and operational controls. |

## 5. Risk-Based Expansion

Expand documentation depth when any of the following are true:

- many teams must coordinate around the same system;
- the system crosses trust, data, or ownership boundaries;
- implementation errors could cause material business, security, compliance, financial, or operational impact;
- several architecture styles are plausible and trade-offs must be explained;
- the implementation is expected to evolve over time;
- AI-assisted development will rely on the architecture as source material;
- prior delivery work showed confusion, rework, or boundary drift.

## 6. Minimum Decision Questions

Before selecting documents, answer:

1. What decisions must developers make correctly?
2. What boundaries are most likely to be violated?
3. What parts of the system are hardest to change later?
4. What risks need explicit ownership?
5. What terminology must be consistent across architecture, design, and code?
6. What architecture style or styles are being considered?
7. What evidence is available, and what still requires discovery?

## 7. Output Rule

Each selected architecture document should have a clear reason to exist.

If the reason is unclear, do not create the document yet. Capture the need as an open question or assumption instead.
