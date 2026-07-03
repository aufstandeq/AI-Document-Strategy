# Technical Standards

## Document Status
Draft

## Purpose
Define the technical standards, guidance, and reference structure used to support architecture clarity and implementation consistency for the target project.

## Owner
Architecture Team

## Last Updated
2026-07-03

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## Standards Structure

Technical standards should convert research and architectural judgment into reusable guidance without copying generic source material into project-specific architecture documents.

| Area | Document | Purpose |
|---|---|---|
| Knowledge Model | [Architecture Knowledge Model](./architecture-knowledge-model.md) | Explains how research becomes principles, practices, how-to guidance, frameworks, selection rules, or project facts. |
| Document Selection | [Architecture Document Selection Guidance](./architecture-document-selection.md) | Explains how architecture style, risk, and complexity determine which architecture documents are needed. |
| Quality Attributes | [Quality Attributes](./quality-attributes.md) | Defines quality characteristics that influence architecture and implementation. |
| Architecture Decision Matrix | [Architecture Decision Matrix](./architectural-decision-matrix.md) | Provides a decision lens for selecting architectural topology or style. |
| Architecture Guidelines | [Architecture Guidelines](./architecture-guidelines.md) | Captures solution and software design principles. |
| Learning Backlog | [Learning Backlog](./learning-backlog.md) | Tracks reference books, papers, and research themes. |

## Technical Standard Categories

Project-specific standards should be defined only when they are needed to guide implementation.

| Category | When to Define | Expected Output |
|---|---|---|
| Coding Standards | When language, framework, module, or repository conventions affect consistency. | Naming, layering, packaging, dependency, and code-organization rules. |
| API Standards | When the system exposes or consumes APIs. | API style, versioning, schema, compatibility, and error-response rules. |
| Data Standards | When the system owns, stores, moves, or transforms data. | Ownership, classification, lifecycle, migration, and retention rules. |
| Integration Standards | When the system exchanges data or events with other systems. | Contract, message, event, retry, idempotency, and ownership rules. |
| Security Standards | When identity, access, sensitive data, compliance, or trust boundaries matter. | Authentication, authorization, data protection, audit, and secrets rules. |
| Testing Standards | When architecture boundaries or quality attributes must be verified. | Unit, integration, contract, architecture, performance, and regression test expectations. |
| Observability Standards | When operations, support, or reliability matter. | Logging, metrics, tracing, alerting, dashboard, and incident evidence expectations. |
| Delivery Standards | When deployment, release, rollback, or environment management matters. | Build, release, deployment, rollback, migration, and environment rules. |

## Project-Specific Standards Rule

Do not define a standard simply because it is a best practice in general.

Define a project-specific standard when it:

- prevents likely implementation mistakes;
- preserves an architecture boundary;
- supports a required quality attribute;
- clarifies team ownership;
- protects security, reliability, data, or operational expectations;
- makes human or AI-assisted development more consistent.

## Research Use Rule

Research sources should inform standards through distilled principles, practices, how-to guidance, frameworks, and selection rules.

Do not copy research sections into this document. Link to or cite research sources from a research index or learning backlog, then record the actionable standard separately.

## Open Project Standards

<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
Add project-specific standards here only after source facts, architecture decisions, or delivery needs justify them.
