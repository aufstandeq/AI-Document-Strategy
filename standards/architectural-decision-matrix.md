# Architectural Decision Matrix

## Document Status
Draft

## Purpose
This document provides a decision-support framework to help software architects and development teams select the correct deployment topology for new projects. 

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
2026-06-11

---

## 1. Decision Criteria

Before choosing a topology, evaluate the project's parameters using the following dimensions:

*   **Team Scale:** How many developers will actively commit to the codebase?
*   **Domain Complexity:** How many distinct business domains or bounded contexts exist?
*   **Deployment Frequency:** Do domains need to scale and deploy independently?
*   **Operational Budget/Capacity:** Does the team have the overhead to manage distributed systems, networks, and distinct pipelines?
*   **Data Coupling:** Do business transactions span multiple domains, or are they isolated?

---

## 2. Topology Comparison Matrix

| Evaluation Dimension | Monolith | Modular Monolith | Microservices | Serverless (FaaS) |
| :--- | :--- | :--- | :--- | :--- |
| **Ideal Team Size** | 1–8 developers | 5–25 developers | 20+ developers (split into pods) | 1–15 developers |
| **Domain Coupling** | High database coupling | High logical, zero db coupling | Completely decoupled | Fully decoupled / Event-driven |
| **Operational Overhead** | Low (Single process/db) | Medium (Single process/multi-schema)| High (Service discovery, networks) | Medium (Cold starts, vendor lock-in)|
| **Scale Characteristics** | All-or-nothing scaling | All-or-nothing scaling | Fine-grained independent scaling | Automatic scale-to-zero |
| **Best Used When...** | Rapid prototyping, simple domains | Complex domain with small-to-medium teams | Large, independent teams with high scale | Intermittent workloads, event pipelines |

---

## 3. Topology Profiles

### Profile A: Monolith
Select this if you are a small team proving product-market fit. The speed of feature iteration outweighs the need for strict domain boundaries.
*   *Downstream Standards Focus:* Internal code modularity (directory structure), single-database optimizations, unified testing.

### Profile B: Modular Monolith
Select this if your domain is complex, but your team lacks the operational capacity to manage complex networks, distributed tracing, and independent deployments.
*   *Downstream Standards Focus:* Database schema-per-module design, public interface/API enforcement between modules, in-process event patterns.

### Profile C: Microservices
Select this if you have multiple independent teams that are blocked by single release trains, and the domains require independent scaling or distinct database technologies.
*   *Downstream Standards Focus:* OpenTelemetry distributed tracing, network failure patterns (retry, circuit breakers), API-first specs, distributed data consistency (Outbox/Saga).

### Profile D: Serverless (FaaS)
Select this if the system is driven by intermittent workloads, event processing, or requires elastic scaling without managing persistent server runtimes.
*   *Downstream Standards Focus:* Cold-start mitigation, function payload sizing, serverless security permissions, state management.

---

## 4. AI Prompt Hooks (How to Populate Standards & Context)

Once a topology is chosen, copy the appropriate template block below and paste it into your AI assistant to bootstrap your architecture repository documents.

### 4.1 Solutions Architect Prompt: Initial Context Setup
Use this hook to populate the high-level context, actor roles, and external integrations based on your product requirements.

```text
SYSTEM INSTRUCTION: You are an Expert Solutions Architect.
We are initiating a new project with the following core characteristics:
- Business Goal: [INSERT BRIEF BUSINESS OBJECTIVE]
- Primary Users/Actors: [INSERT KEY ACTORS/ROLES, e.g., Customers, Admin]
- External Dependencies: [INSERT INTEGRATIONS, e.g., Stripe, SendGrid]

Based on these parameters, please generate:
1. The Business Context for architecture/context/business-context.md:
   - Specific Business Objectives, Success Metrics, and Constraints.
2. The Actors and Roles mapping for architecture/context/actors-and-roles.md:
   - A table listing Actor, Responsibility, Role, and Security Scope.
3. The External Systems mapping for architecture/context/external-systems.md:
   - A table mapping Upstream/Downstream systems, Integration Responsibilities, and Ownership.

Ensure all output strictly adheres to the repository's metadata header rules and relative pathing constraints.
```

### 4.2 Solutions Architect Prompt: Principles & Ways of Working
Use this hook to establish the architectural principles and integration governance in `technical-standards.md` based on your chosen topology.

```text
SYSTEM INSTRUCTION: You are an Expert Solutions Architect.
We have selected the [INSERT CHOSEN TOPOLOGY: Monolith/Modular Monolith/Microservices/Serverless] topology and are establishing the architectural principles and ways of working.

Please generate the high-level governance section for standards/technical-standards.md covering:
1. Architectural Principles:
   - 3-5 core invariants (e.g., Data Sovereignty, API-First, Security-by-Default) tailored for this topology.
2. Integration Standards:
   - High-level interface rules (e.g., REST vs gRPC, event contract registries, error propagation patterns).
3. Ways of Working (Governance):
   - The process for proposing, reviewing, and approving changes to these standards using ADRs.

Ensure output is written strictly in Markdown conforming to the repository metadata rules.
```

### 4.3 Software Architect Prompt: Technical Standards & Quality Attributes
Use this hook to generate concrete codebase standards and quality metrics.

```text
SYSTEM INSTRUCTION: You are an Expert Software Architect.
We have selected the [INSERT CHOSEN TOPOLOGY: Monolith/Modular Monolith/Microservices/Serverless] topology for our project.

Based on this topology, please generate:
1. The Core Technical Standards for standards/technical-standards.md covering:
   - Integration / Inter-service communication rules.
   - Database / Data separation rules.
   - Observability & Logging rules appropriate for this topology.
2. The Quality Attributes targets for standards/quality-attributes.md covering:
   - Availability, Latency, and Scalability objectives.
   - The measurement method for each metric.

Write this strictly in Markdown conforming to the repository's metadata header rules.
```

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.
