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
2026-06-11

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
* [how-to-start.md](./how-to-start.md): Onboarding guide and operational workflow (Read this next).
* [architecture/](./architecture/index.md): System contexts, views, and specific sub-system templates.
* [standards/](./standards/technical-standards.md): Engineering, coding, testing, and quality attribute standards.
* [decisions/](./decisions/0001-record-architecture-decisions.md): Architecture Decision Records (ADRs).
* [governance/](./governance/open-questions.md): Risk logs, assumption trackers, and open questions logs.
* [archive/](./archive/README.md): Retrospective, superseded, or legacy architectural artifacts.
* [glossary.md](./glossary.md): Authoritative domain vocabulary and technical terms.

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

