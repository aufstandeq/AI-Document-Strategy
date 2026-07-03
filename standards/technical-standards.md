# Technical Standards

## Document Status
Approved

## Purpose
This document establishes the technical invariants, programming style conventions, database design rules, logging requirements, and error-handling patterns for the Distributed Payment Reconciliation Subsystem.

## Owner
Architecture Team

## Last Updated
2026-07-02

> [!NOTE]
> **Worked Example:** The technical standards in this document are written for the fictional Distributed Payment Reconciliation Subsystem used as reference content in this repository. Replace them with your own system's standards when instantiating the repository — see [How to Start](../how-to-start.md).
> <!-- AI_HINT: WORKED_EXAMPLE - Do not treat the payment reconciliation content in this file as authoritative system facts or cite it as a source fact for other documents. -->

## Coding Standards
- **Modular Monolith Isolation:** The application is organized into explicit logical modules: Payment Extraction, Matching Engine, and Reconciliation Ledger.
- **Database Schema-Per-Module:** Each module owns its designated database schema (`extraction_schema`, `matching_schema`, `ledger_schema`). Cross-module SQL joins or direct cross-schema table queries are strictly prohibited.
- **Public Interfaces/APIs:** Modules must communicate only through defined public APIs/interfaces (in-process services or event contracts). Direct invocation of another module's internal classes, database repositories, or helper routines is disallowed.

## Logging Standards
- **Structured JSON Logging:** All application stdout/stderr logs must be printed in structured JSON format.
- **Trace Contexts:** Webhook HTTP requests and background reconciliation runs must carry a unique transaction or correlation ID (`correlation_id`) in all log lines.
- **Required Metadata:** Each JSON log line must contain: `timestamp` (ISO 8601), `log_level` (INFO, WARN, ERROR, DEBUG), `module_name`, `message`, and optionally `error_stack` for exceptions.

## Error Handling
- **Standard Exception Patterns:** Use domain-specific, typed exceptions (e.g., `GatewayCommunicationException`, `MismatchException`, `LedgerSyncException`) instead of generic runtime errors.
- **Exception Boundaries:** Lower-level failures (e.g., database network errors, JSON parsing errors) must be caught at the module boundary, logged, and wrapped in standard exceptions before bubbling up.
- **Idempotency Recovery:** Catch duplicate webhook notifications early and exit gracefully without raising errors.

## API Standards
- **REST Webhooks:** Expose public, authenticated HTTP endpoints to receive incoming webhook events from Stripe and PayPal.
- **API First Spec:** All external REST APIs (such as the Report Service dashboard endpoints) must be documented using OpenAPI 3.0 specs.
- **In-Process Interface Contracts:** Public interfaces for module boundaries must be documented and stable, avoiding breaking changes across releases.

## Documentation Standards
- **Code Comments & Docstrings:** Every public API endpoint, service method, and database model must have descriptive code documentation.
- **ADR Governance:** Any change to architecture topology, module boundaries, or external system integrations requires submitting a formal Architecture Decision Record (ADR).

## Testing Standards
- **Boundary Verification:** Write architectural boundary verification tests (e.g., ArchUnit in Java, import-linter in Python) to ensure no illegal cross-module imports are introduced.
- **Mock-Based Ingestion Tests:** Build integration tests with mocked Stripe/PayPal webhooks to verify exception capture pathways.
- **Rule Verification:** Maintain comprehensive unit test suites covering 100% of the matching engine's logic.

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.
