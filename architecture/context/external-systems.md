# External Systems

## Document Status
Approved

## Purpose
This document details the external integrations and internal systems that interact with the Distributed Payment Reconciliation Subsystem, including their communication directions and ownership.

## Owner
Architecture Team

## Last Updated
2026-06-11

## Upstream Systems
- **Stripe API:** Provides transaction details, payout reports, dispute records, and webhooks for credit card and automated payments.
- **PayPal API:** Provides transaction searches, express checkout logs, refund records, and webhooks for PayPal transactions.

## Downstream Systems
- **Internal Billing Ledger:** The core system of record that receives matched transaction batches and discrepancy logs to record reconciled cash flows.

## Third-Party Services
- **Stripe SDK / REST endpoints:** Used for querying charge objects and capturing asynchronous webhook events.
- **PayPal SDK / REST endpoints:** Used for querying transaction history and capturing asynchronous webhook events.

## Integration Responsibilities
- **Data Fetching:** The Payment Extraction module pulls transaction records from Stripe and PayPal endpoints and queues them.
- **Webhook Processing:** The Payment Extraction module exposes public webhook endpoints to receive real-time transaction updates from Stripe and PayPal.
- **Ledger Ingestion:** The Reconciliation Ledger module exports verified match batches and exception reports to the Billing Ledger via its public API.

## Ownership
- **External Gateways (Stripe, PayPal):** Maintained externally by third-party vendor platforms. Integration configuration is owned by the Architecture Team.
- **Internal Billing Ledger:** Maintained and owned by the Billing & Core Finance Team.

| System | Type | Responsibility | Owner |
|---|---|---|---|
| Stripe API | Upstream Third-Party Service | Provides transaction logs, payout reports, and webhook events for credit card payments | External (Stripe) / Architecture Team |
| PayPal API | Upstream Third-Party Service | Provides transaction search, payout status, and webhook events for PayPal transactions | External (PayPal) / Architecture Team |
| Internal Billing Ledger | Downstream Internal System | Consumes reconciled payment reports and exceptions to update corporate ledger records | Internal (Billing & Core Finance Team) |

---

See [Glossary](../../glossary.md) for definitions of key terms used in this document.
