# Learning Backlog

## Document Status
Draft

## Purpose
Track reference materials, books, and specific architectural topics/lessons that need to be learned, documented, and integrated.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../glossary.md) for definitions of key terms.

---

## 1. Reference Library

The following books and materials are available under the project's reference folder:  
`Projects/StorGratis baop/temp-working-file/Reference/`

| Reference / Document | Focus Area | Status |
| :--- | :--- | :--- |
| *Fundamentals of Software Architecture (2nd Edition)* | Layered architectures, modular monoliths, component design | Active |
| *Software Architecture: The Hard Parts* | Distributed data, transaction patterns, service decomposition | Active |
| *The C4 Model* (System Context, Container, Component, Deployment) | Standardized diagrams and viewpoints for architecture docs | Active |
| *Software Architecture Fundamentals (Third Edition)* | Architectural styles, analysis, and diagramming techniques | Active |

---

## 2. Learning & Content Backlog

Use this backlog to record specific architectural topics, design patterns, or framework guides that the team needs to document and train the agents on.

| ID | Topic | Source Material | Target Document | Status |
| :--- | :--- | :--- | :--- | :--- |
| LRN-001 | C4 Component Diagram standards | *The C4 Model (5. Component Diagram)* | `standards/technical-standards.md` | Open |
| LRN-002 | Modular Monolith in-process event patterns | *Fundamentals of Software Architecture (Ch 11)* | `standards/technical-standards.md` | Open |
| LRN-003 | Database schema separation rules | *Software Architecture: The Hard Parts* | `standards/architecture-guidelines.md` | Open |
| LRN-004 | Distributed transactional consistency (Saga/Outbox) | *Software Architecture: The Hard Parts* | `standards/architecture-guidelines.md` | Open |
| LRN-005 | Temporal workflow-engine pattern guide | Local project code & workflow docs | `standards/technical-standards.md` | Open |

---

## 3. How to Add to this Backlog

When a new architectural pattern, technology choice, or documentation gap is identified:
1.  Add a new line item under **2. Learning & Content Backlog** with a unique `LRN-XXX` ID.
2.  Specify the **Source Material** (e.g., specific chapters from the Reference Library or codebase paths).
3.  Set the **Target Document** where these rules/standards will eventually be written.
4.  Once the content is written and verified, change the status to `Completed` and update the document's metadata header.
