# Claude Skills Index

This directory contains project-scoped Claude skills for the AI-Document-Strategy repository.

These files are tracked runtime skill configuration. They are intentionally excluded from architecture-document audits, but they are not ignored by Git.

## Directory Rules

- Each skill lives in `.claude/skills/<skill-name>/SKILL.md`.
- Skill folder names must use kebab-case.
- `SKILL.md` must be named exactly `SKILL.md`.
- Do not add a `README.md` inside an individual skill folder.
- Use this parent index for human navigation only.

## Operating Sequence

Use the skills in this order for the main documentation loop:

```text
doc-loop-prepare
run-doc-checker
fix-doc-linter-failures
escalate-doc-gap, if source facts are missing
```

Use the scaffold-specific skills when creating new documentation structures:

```text
create-adr
create-system-scaffold
create-system-context
```

## Skill Catalog

| Skill | Mutation | Primary use |
|---|---:|---|
| `doc-loop-prepare` | No | Run the deterministic harness and classify the next safe action. |
| `run-doc-checker` | No | Produce a bounded repair plan or review a proposed diff before mutation. |
| `fix-doc-linter-failures` | Yes, bounded | Repair verifier/linter failures inside the current policy allowlist. |
| `create-adr` | Yes, scaffold only | Create ADR files through `scaffold_adr.py`. |
| `create-system-scaffold` | Yes, scaffold only | Create system/bounded-context folders through `scaffold_system.py`. |
| `create-system-context` | Yes, bounded | Update C4/context files from explicit source facts only. |
| `escalate-doc-gap` | Yes, bounded | Record missing human-owned facts as open questions, assumptions, risks, or `ARCH-GAP` comments. |

## Boundary Notes

`.claude/skills/**` is not active architecture documentation.

Do not add architecture-document metadata headers to skill files just to satisfy repository audits. The verifier boundary should exclude `.claude/`, while Git should continue tracking these files.

Future improvement: replace direct verifier exclusions with a dedicated documentation-audit ignore file. See issue #2.
