# Architecture Repository

## Document Status
Approved

## Purpose
This repository is the authoritative architecture source of truth for the system.

> [!IMPORTANT]
> **Getting Started:** If you are new to this repository (human or AI), please read the [How to Start](./how-to-start.md) onboarding guide first to understand the workspace setup, decision-making framework, and operational rules.

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
2026-07-02

## Audience
* Product
* Architecture
* Engineering
* Security
* Operations
* AI-assisted development tools

## Guiding Principles
* **Documentation as Code**: Architecture is versioned, reviewed, and maintained alongside code.
* **Architecture Before Implementation**: Design decisions and models are defined before construction.
* **Decisions Over Opinions**: Architectural choices are documented through formal Architecture Decision Records (ADRs).
* **Explicit Boundaries**: Clear boundaries are established between systems, domains, and responsibilities.
* **Single Authoritative Source**: Every concept has one primary source of truth, referencing rather than duplicating.
* **Glossary First Vocabulary**: Domain and technical terms must be defined in the glossary before broad usage.
* **Archive Rather Than Delete**: Superseded documents are moved to the archive directory rather than deleted to retain history.

## Repository Navigation
* [strategy.md](./strategy.md): The AI & human documentation strategy — operating model, maturity ladder, and trust boundaries.
* [how-to-start.md](./how-to-start.md): Onboarding guide and operational workflow (Read this next).
* [onboarding-dev.md](./onboarding-dev.md): Developer-specific onboarding with local verification commands.
* [glossary.md](./glossary.md): Authoritative domain vocabulary and technical terms.
* [architecture/](./architecture/index.md): System contexts, views, and specific sub-system templates.
* [decisions/](./decisions/0001-record-architecture-decisions.md): Architecture Decision Records (ADRs).
* [standards/](./standards/technical-standards.md): Engineering, coding, testing, and quality attribute standards.
  * [quality-attributes.md](./standards/quality-attributes.md): Non-functional requirement targets.
  * [architectural-decision-matrix.md](./standards/architectural-decision-matrix.md): Topology selection framework.
  * [architecture-guidelines.md](./standards/architecture-guidelines.md): Solution and software design principles.
  * [learning-backlog.md](./standards/learning-backlog.md): Architecture reference books and learning backlog.
* [governance/](./governance/open-questions.md): Risk logs, assumption trackers, and open questions.
  * [risks.md](./governance/risks.md): Risk register.
  * [assumptions.md](./governance/assumptions.md): Documented assumptions.
  * [migration_log.md](./governance/migration_log.md): Change and migration history.
  * [red-team-audit-report.md](./governance/red-team-audit-report.md): Documentation linter audit findings.
* [agent/](./agent/README.md): Agentic loop documentation, prompts, and policy files (for autonomous documentation maintenance).
* [archive/](./archive/README.md): Retrospective, superseded, or legacy architectural artifacts.

## Operational Guide

### 1. File Metadata Header Rule
Every new markdown file created in this repository must begin with the following metadata header block:

```markdown
# [Document Title]

## Document Status
Draft

## Purpose
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
YYYY-MM-DD
```

### 2. Incomplete Sections
Do not use naked `TBD` or custom placeholders. Every incomplete section must use:

```markdown
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD
```

### 3. Structural Link Rules
All cross-document references must use relative paths (e.g. `[Standards](./standards/technical-standards.md)`), never root-absolute paths or Windows backslash paths.

### 4. Running the Local Linter
To verify structural rules locally before pushing changes to GitHub:

```bash
python3 verify_docs.py
```

<!-- Note: Instructions for running the autonomous agentic loop have been isolated to agent/README.md -->

### 5. Marking Architectural Gaps

When a section or decision is known to be incomplete but the answer is not yet available, use an `ARCH-GAP` inline comment tag rather than leaving a bare `TBD`. This allows the audit scripts to inventory all open gaps across the repo.

```markdown
<!-- ARCH-GAP: [Short description of what is unknown or unresolved]. [Owner: Team/Person]. -->
```

- `Owner:` is required — the audit script will flag gaps without an owner.
- `ARCH-GAP` tags appear in the `verify_coverage.py` gap inventory report.
- Once resolved, remove the comment and document the decision in an ADR if appropriate.

### 7. AI System Instructions (Behavioral Rules)
If you are an AI assistant or agent reading this repository:
*   **Ignore the `/archive` Directory:** Do not read, search, or index documents under `archive/` unless the user explicitly instructs you to reference deprecated or legacy documents.
*   **Source of Truth:** Treat only the active directories (`architecture/`, `standards/`, `decisions/`, `governance/`, and `glossary.md`) as the current authoritative state.
*   **No Invention:** Do not extrapolate or invent system actors, requirements, integration systems, or technologies that are not explicitly documented.
*   **Worked Example Content:** Files containing a `WORKED_EXAMPLE` AI hint describe a fictional reference system (the Distributed Payment Reconciliation Subsystem) used to demonstrate completed templates. Treat that content as illustrative only — never cite it as a source fact or propagate it into other documents.


