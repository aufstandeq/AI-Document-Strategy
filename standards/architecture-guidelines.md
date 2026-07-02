# Architecture Design Guidelines

## Document Status
Approved

## Purpose
Establish core software and solution architecture design guidelines to train agentic team members and govern system design.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../glossary.md) for definitions of key terms.

---

## 1. Domain-Driven Design (DDD) & Bounded Contexts

To maintain a clean, maintainable product structure, all systems must be designed around Domain-Driven Design principles:
*   **Ubiquitous Language:** All terms used in code, databases, and APIs must map directly to [glossary.md](../glossary.md).
*   **Bounded Contexts:** Each system folder under `architecture/systems/` represents a Bounded Context (BC). A Bounded Context must have:
    *   Explicit responsibilities (what it does).
    *   Clearly defined public interfaces (APIs, events).
    *   Zero direct logical or database coupling to other contexts.
*   **Context Mapping:** Any interaction between Bounded Contexts must be explicitly mapped in the Logical View (`architecture/views/logical-view.md`). Direct cross-context queries are forbidden.

---

## 2. Data Sovereignty & Separation

Data coupling is the most common cause of architectural drift. We enforce strict data isolation rules based on the chosen deployment topology:

### 2.1 Monolith & Modular Monolith
*   **Schema Isolation:** Each Bounded Context must own its tables.
*   **No Cross-Context Joins:** A query in Context A must never join tables owned by Context B. 
*   **Data Sharing:** If Context A needs data from Context B, it must retrieve it via Context B's public API or subscribe to an event published by Context B.

### 2.2 Microservices & Serverless
*   **Database Sovereignty:** Each service/context must have a physically separate database instance.
*   **Eventual Consistency:** Distributed transactions must use asynchronous message passing (e.g., Outbox pattern, Saga pattern) rather than synchronous distributed locks.

---

## 3. Interface & API Design

Integrations must be API-first and contract-governed:
*   **Contracts:** All inter-context communication must be documented using open standards (e.g., OpenAPI/Swagger for REST, Protobuf for gRPC, AsyncAPI for events).
*   **Compatability:** APIs must be backward-compatible. Breaking changes require major version increments and a migration log entry.
*   **Event Payloads:** Event schemas must be thin. Prefer publishing identifiers and status changes (e.g., `OrderCompleted` with `order_id`) rather than full entity representations, forcing consumers to fetch current state via API if needed.

---

## 4. Non-Functional Requirements (NFR) Governance

Architectural designs must explicitly align with the project's quality attributes:
*   **Availability:** Define failure recovery actions (retry budgets, circuit breakers, fallback static responses).
*   **Latency:** Establish performance budgets at the container/API gateway boundary.
*   **Scalability:** Design systems to be stateless to support horizontal autoscaling.
*   **Security:** Enforce Least Privilege. Every component boundary must validate incoming requests (authentication) and permissions (authorization).

---

## 5. Reference Material & Book Map

For advanced architectural patterns, the team references the canonical library located in the project's reference folder:
`Projects/StorGratis baop/temp-working-file/Reference/`

Key reference mappings:
*   **C4 Modeling:** See *The C4 Model* PDFs (System Context, Container, Component, and Deployment diagrams) to design views under `architecture/views/`.
*   **Component-Based & Modular Design:** See *Fundamentals of Software Architecture (2nd Edition)*, Chapter 8 (Component-Based Thinking) and Chapter 11 (The Modular Monolith Architecture Style).
*   **Distributed Systems Trade-offs:** See *Software Architecture: The Hard Parts* for analyzing data coupling, service decomposition, and transactional orchestration.

---

## 6. AI-Collaborative Architectural Workflows

When human developers and AI assistants (like Claude Code or Cursor) collaborate, the following rules apply:
1.  **Read Before Proposing:** The AI must read `how-to-start.md`, `standards/technical-standards.md`, and the relevant system `/index.md` before generating code.
2.  **Explicit Gaps:** If an architectural detail is missing, do not assume or invent. Mark it with a `<!-- ARCH-GAP: [description]. [Owner: Team]. -->` comment.
3.  **Strict Linting:** All architectural changes must pass `verify_docs.py` and `verify_e2e.py` locally before a PR is opened.
