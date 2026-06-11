# How to Start

## Document Status
Draft

## Purpose
This document provides the foundational onboarding process for humans and AI agents utilizing this architecture repository. It outlines the repository's value proposition, operational workflows, and the onboarding path for new software projects.

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
2026-06-11

---

## 1. What is this Repository?
This repository is the single, version-controlled **authoritative source of truth** for all product, software, and systems architecture. Unlike transient design documents or scattered wiki pages, this repo treats architecture as versioned code—subject to pull request reviews, automated linting, and systematic revision history.

---

## 2. Why Use this Structure?
A structured, markdown-centric architecture repository solves two primary problems in software development:

### For Humans: Preventing Architecture Drift
As software scales, original design decisions fade from memory. Code changes begin to violate boundary isolation, security constraints, or performance requirements. By documenting architecture here, developers have immediate access to context, rules, and historical decisions (ADRs) directly alongside the codebase.

### For AI: Reducing Hallucinations & Maximizing Context
AI coding assistants perform poorly when they must guess system boundaries or code rules. This repository is structured specifically to serve as high-signal context for AI agents. By pointing an AI to these documents, the agent can understand constraints (such as security scopes, component boundaries, and technical standards) before proposing code modifications, minimizing structural errors and hallucinations.

---

## 3. Operational Workflow (How to Start a New Project)

To initialize or audit a project using this architecture framework, follow this step-by-step path:

### Step 1: Execute the Architectural Decision Matrix
Every project begins with a fundamental decision regarding deployment topology. Do not guess or pre-populate standard rules. 
1. Open the [Architectural Decision Matrix](./standards/architectural-decision-matrix.md).
2. Evaluate your project requirements against the key metrics (Team size, Latency, Data coupling).
3. Record the selected topology in a new ADR under `./decisions/`.

### Step 2: Generate Context & Views
Once the topology is chosen, populate the template files:
1. Complete [business-context.md](./architecture/context/business-context.md) and [system-context.md](./architecture/context/system-context.md).
2. Complete [logical-view.md](./architecture/views/logical-view.md) and [deployment-view.md](./architecture/views/deployment-view.md) using the topology selection to determine complexity.
3. Keep missing information marked explicitly with the `PENDING_DISCOVERY` block.

### Step 3: Populate Standards via AI-Partner Prompting
Use the chosen topology profile from the matrix to prompt an AI partner to generate the specific technical standards and quality attributes.
* **Example:** *"Given the Modular Monolith topology selected in ADR-0002, draft the database schema isolation guidelines for standards/technical-standards.md."*

### Step 4: Write and Audit Code
Once standards are populated:
1. Point your development tools/AI to the standards files as constraints.
2. Ensure all changes are validated locally via the linter script (`python3 verify_docs.py`) to verify structural integrity before merging.
