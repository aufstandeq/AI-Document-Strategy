# Actors and Roles

## Document Status
Draft

## Purpose
This document defines the actors, their operational responsibilities, role mappings, and security scopes within the Distributed Payment Reconciliation Subsystem.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

## Example Content Notice

This document currently contains example architecture content for a Distributed Payment Reconciliation Subsystem. It is retained as a worked example and must not be treated as approved source-truth architecture for a real implementation until replaced with project-specific source facts and explicitly re-approved.

---

## Actors
- **Reconciliation Analyst (Finance):** Business users who monitor daily reconciliation outcomes, investigate exceptions, and resolve transaction mismatches.
- **Operations Admin (Ops):** Technical administrators responsible for managing integration settings, monitoring performance, and executing manual reconciliation runs.
- **Systems Developer (Engineering):** Engineers responsible for maintaining the system, writing matching rules, managing schemas, and configuring deployment profiles.

## Responsibilities
- **Reconciliation Analyst:** Resolves mismatched entries, marks exceptions, confirms accuracy of automated runs, and reports financial anomalies.
- **Operations Admin:** Manages gateway credentials, monitors system health, adjusts rate limiting settings, and triggers batch reconciliation replays.
- **Systems Developer:** Manages database schemas, updates module APIs, configures container environment variables, and tests mock APIs.

## Role Definitions
- **Reconciliation Analyst (`reconciliation_analyst`):** Grants permission to view transaction records, update mismatch resolution statuses, and export reconciliation reports.
- **Operations Admin (`operations_admin`):** Grants permission to execute system operations, trigger batch processing, and modify environment configurations.
- **Systems Developer (`systems_developer`):** Grants administrative access to codebase, configuration files, and schema migrations.

## Permissions
- `reconciliation:read`: Ability to view reconciliation records and exception logs.
- `reconciliation:resolve`: Ability to write to exception resolution logs and force-match records.
- `system:trigger`: Ability to trigger manual reconciliation runs and API fetches.
- `system:configure`: Ability to edit external API configurations and system keys.

## Security Scopes
- `read:reconciliation`: Covers read access to reconciliation outcomes.
- `write:reconciliation`: Covers write access to resolving mismatches and logging exceptions.
- `write:system`: Covers execution and configuration rights.

| Actor | Responsibility | Role | Scope |
|---|---|---|---|
| Reconciliation Analyst | Investigate mismatches, export reports, resolve exceptions | Reconciliation Analyst (`reconciliation_analyst`) | `read:reconciliation`, `write:reconciliation` |
| Operations Admin | Monitor runs, update API configs, trigger manual runs | Operations Admin (`operations_admin`) | `read:reconciliation`, `write:system` |
| Systems Developer | Modify code, configure schemas, update matching logic | Systems Developer (`systems_developer`) | `*` (All scopes / Full Admin) |

---

See [Glossary](../../glossary.md) for definitions of key terms used in this document.
