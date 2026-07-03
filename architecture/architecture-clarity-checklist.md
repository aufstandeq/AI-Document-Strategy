# Architecture Clarity Checklist

## Document Status
Draft

## Purpose
Define the minimum architecture questions that must be answered before significant implementation work begins.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## 1. Goal

The client architecture workspace must create enough clarity for correct development decisions.

A structurally valid repository is not enough. The documentation must make the system understandable, actionable, and resistant to drift.

## 2. Readiness Levels

| Level | Meaning | Guidance |
|---|---|---|
| Missing | The question is unanswered or only marked as pending discovery. | Escalate the gap before relying on this area. |
| Partial | Some information exists, but important boundaries, responsibilities, risks, or decisions remain unclear. | Proceed only with explicit assumptions. |
| Sufficient | The question is answered clearly enough to guide implementation. | Safe to use as implementation guidance. |
| Verified | The documentation has been checked against source truth such as stakeholder confirmation, code, infrastructure, APIs, or tests. | Preferred state for active systems. |

## 3. Core Architecture Questions

| Area | Question | Primary Document Location |
|---|---|---|
| Business Goal | What business outcome does this system support? | `architecture/context/business-context.md` |
| System Purpose | What is the system responsible for? | `architecture/context/system-context.md` |
| Scope Boundary | What is explicitly in scope and out of scope? | `architecture/context/system-context.md` |
| Actors and Roles | Who uses or operates the system, and what can each role do? | `architecture/context/actors-and-roles.md` |
| External Systems | What systems does this system depend on or integrate with? | `architecture/context/external-systems.md` |
| Domain Boundaries | What are the major bounded contexts, modules, or subsystems? | `architecture/index.md`, `architecture/systems/` |
| Responsibility Boundaries | What does each subsystem own, and what must it not own? | `architecture/systems/`, `architecture/views/logical-view.md` |
| Data Ownership | What data does each module or bounded context own? | `architecture/views/data-view.md` |
| Integration Contracts | What APIs, events, messages, or files cross system boundaries? | `architecture/views/integration-view.md` |
| Deployment Shape | Where does the system run, and what infrastructure assumptions matter? | `architecture/views/deployment-view.md` |
| Security Model | What are the authentication, authorization, data protection, and threat boundaries? | `architecture/views/security-view.md` |
| Quality Attributes | What reliability, scalability, performance, maintainability, and observability qualities must be preserved? | `standards/quality-attributes.md` |
| Technical Standards | What coding, testing, integration, and operational standards guide implementation? | `standards/technical-standards.md` |
| Architecture Decisions | What material architecture choices have been decided and why? | `decisions/` |
| Risks | What known risks could affect implementation or operations? | `governance/risks.md` |
| Assumptions | What assumptions are being made until source truth is confirmed? | `governance/assumptions.md` |
| Open Questions | What is unresolved and who owns resolution? | `governance/open-questions.md` |
| Project Vocabulary | Are key project, domain, architecture, design, and code terms defined consistently? | `glossary.md` |

## 4. Minimum Before Development

Before material development starts, the following should be at least **Sufficient**:

- Business Goal
- System Purpose
- Scope Boundary
- Actors and Roles
- External Systems
- Domain Boundaries
- Responsibility Boundaries
- Data Ownership
- Integration Contracts
- Security Model
- Quality Attributes
- Technical Standards
- Architecture Decisions for known material choices
- Project Vocabulary for terms used in code and documentation

If any of these are **Missing**, create or update an owned `ARCH-GAP`, open question, assumption, or risk before proceeding.

## 5. Drift Signals

Review the architecture when any of the following occur:

- implementation introduces a new module, service, API, event, database table, queue, or third-party dependency not reflected in architecture documents;
- implementation bypasses documented module or system boundaries;
- a new quality attribute requirement appears in delivery work but not in standards;
- a security or data handling decision changes without a matching ADR;
- teams use inconsistent vocabulary for the same concept;
- a document is structurally valid but no longer helps someone make an implementation decision.

## 6. Clarifying Questions for Reviewers

1. Could a new developer understand what to build and what not to build?
2. Are the most important boundaries explicit?
3. Are data ownership and integration responsibilities explicit?
4. Are the quality attributes concrete enough to influence implementation?
5. Are risks, assumptions, and unresolved questions visible?
6. Are project terms defined in the project glossary before being used broadly?
7. Is any example content still being mistaken for active architecture truth?

## 7. Completion Rule

A section is not complete because it is filled in. It is complete when it improves the ability to make correct development decisions and does not hide missing source facts.
