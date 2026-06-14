# Developer Onboarding Guide

## Document Status
Draft

## Purpose
Step-by-step onboarding for developers joining this project. Covers the architecture repository structure, core design principles, domain vocabulary, and how to verify documentation changes before submitting a pull request.

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
YYYY-MM-DD

---

## 1. Critical First-Reads

Before writing any code or proposing architectural changes, read and internalize these documents **in order**:

1. **[Glossary](./glossary.md) — Read First.** This repository enforces a ubiquitous language. Understand the authoritative terms for the system's domain before discussing or documenting anything.
2. **[How to Start](./how-to-start.md)** — Understand how this repository works, the chosen deployment topology, and the rules governing AI-assisted development.
3. **[Technical Standards](./standards/technical-standards.md)** — Coding, API, data, and event standards you must follow.
4. **[Architecture Overview](./architecture/index.md)** — The high-level system map.

---

## 2. Core Architectural Principles

<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD — Populate with the project's chosen deployment topology and its key rules (e.g., Modular Monolith schema-per-module isolation, microservice boundaries, event-driven constraints).

---

## 3. Documentation Rules for Developers

Every developer is responsible for keeping architecture documentation current:

1. **New documents must pass the linter.** Run `python3 verify_docs.py` before submitting a PR. The CI pipeline will reject docs that fail structural checks.
2. **Use `PENDING_DISCOVERY` for unknowns.** Never leave a bare `TBD`. Use the standard placeholder:
   ```markdown
   <!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
   TBD
   ```
3. **Tag unresolved design decisions** with an `ARCH-GAP` comment (see `README.md` §5 for format).
4. **Every new document must link to the glossary.** AI behavior rules require it; the linter enforces it.
5. **ADRs capture decisions, not options.** When a significant technical decision is made, record it in `decisions/`. Use `python3 scaffold_adr.py` to create a correctly numbered file.

---

## 4. Local Verification Commands

```bash
# Hard gate — same check the CI runs. Fix all errors before pushing.
python3 verify_docs.py

# Coverage report — informational, does not fail the build.
# Shows ARCH-GAP inventory, stale docs, document status distribution.
python3 verify_coverage.py

# Cross-repo audit — orphaned files, ADR sequencing, BC inventory.
# Also runs in CI. Resolve any errors before merging.
python3 verify_e2e.py
```

---

## 5. Creating New Architecture Artifacts

```bash
# Create a new bounded context / system folder from the template
python3 scaffold_system.py "my-system-name"

# Create the next sequential ADR
python3 scaffold_adr.py "short-decision-title"
```

---

## References

See [Glossary](./glossary.md) for definitions of all domain and technical terms used in this project.
