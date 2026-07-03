# Claude Skills Operating Plan

## Purpose

This plan defines the end state for the Claude skill system in the AI-Document-Strategy repository.

The goal is to create a controlled documentation operating model where Claude can:

- Understand repository rules.
- Prepare the documentation loop.
- Review failures before mutation.
- Apply bounded repairs.
- Use scaffold scripts instead of hand-created structures.
- Stop when human source facts are missing.
- Preserve the architecture repository as the source of truth.

This file is a planning and visibility artifact for the skill system. It is not active architecture documentation.

## Target End State

```text
Human request
  ↓
Claude skill trigger
  ↓
Repository policy load
  ↓
Harness / verifier state read
  ↓
Checker / repair planning
  ↓
Bounded mutation or escalation
  ↓
Deterministic verification
  ↓
Human-visible result
```

The success authority remains the repository verifier and harness layer.

## Operating Principles

| Principle | Meaning |
|---|---|
| Observe before mutate | Inspect harness state and policy before editing. |
| Policy before skill | `agent/SKILL.md` overrides individual Claude skills. |
| Scaffold before hand-create | ADRs and systems use repository scaffold scripts. |
| Source facts before content | Architecture content requires explicit source material. |
| Repair plan before repair | Checker produces the plan before mutation. |
| Escalate instead of invent | Missing facts become owned gaps, questions, assumptions, or risks. |
| Deterministic verification wins | Success is valid only after repository checks pass. |

## Current Skill Set

| Skill | Mutation | Purpose |
|---|---:|---|
| `doc-loop-prepare` | No | Prepare the documentation loop and classify the next safe action. |
| `run-doc-checker` | No | Review verifier failures or proposed diffs and produce a repair plan. |
| `fix-doc-linter-failures` | Yes, bounded | Execute safe verifier/linter repairs inside policy. |
| `create-adr` | Yes, scaffold only | Create ADRs through `scaffold_adr.py`. |
| `create-system-scaffold` | Yes, scaffold only | Create system folders through `scaffold_system.py`. |
| `create-system-context` | Yes, bounded | Update C4 context documents from explicit source facts. |
| `escalate-doc-gap` | Yes, bounded | Record missing human-owned facts instead of inventing content. |

## Current Validation Gates

| Gate | Command | Scope | Hard gate? |
|---|---|---|---:|
| Claude skills validation | `python3 verify_claude_skills.py` | `.claude/skills/**` structure, naming, and frontmatter | Yes |
| Skill trigger fixture validation | `python3 verify_skill_trigger_fixtures.py` | Machine-readable skill trigger expectations | Yes |
| Repair-plan fixture validation | `python3 verify_repair_plan_fixtures.py` | Machine-readable checker repair-plan expectations | Yes |
| Skill verifier fixture validation | `python3 verify_skill_verifier_fixtures.py` | Positive and negative cases for the skill validator | Yes |
| Executable skill verifier fixture validation | `python3 verify_skill_verifier_execution.py` | Temporary skill trees prove validator behavior against fixtures | Yes |
| Source-fact citation fixture validation | `python3 verify_source_fact_citation_fixtures.py` | Source-fact, inference, gap, policy, and verifier-output citation rules | Yes |
| Skill retirement fixture validation | `python3 verify_skill_retirement_fixtures.py` | Skill lifecycle and retirement behavior rules | Yes |
| Structural architecture validation | `python3 verify_docs.py` | Active architecture Markdown document structure and links | Yes |
| Cross-repository audit | `python3 verify_e2e.py` | Orphans, glossary links, ARCH-GAP owners, ADR sequence, system references | Yes |
| Coverage report | `python3 verify_coverage.py` | Gap inventory, status distribution, stale docs, system inventory | No |

The local validation runner loads `.validation-config.json` and runs the gates in the configured order. The intended CI target is the same command: `python3 run_validation.py`.

## Core Workflow

### 1. Prepare

Use `doc-loop-prepare` to run:

```bash
python3 agent_harness.py --prepare
```

Read:

```text
agent/STATE.md
agent/SKILL.md
agent/GOAL.md
```

### 2. Check and Plan

Use `run-doc-checker` to inspect failures or proposed diffs and produce a repair plan.

Statuses:

```text
SAFE_TO_REPAIR
REQUIRES_SOURCE_FACTS
BLOCKED_POLICY
HUMAN_REVIEW_REQUIRED
NO_REPAIR_NEEDED
```

### 3. Repair

Use `fix-doc-linter-failures` only for safe repairs identified by the checker.

Allowed repairs include metadata fixes, obvious relative-link fixes, glossary links, owned ARCH-GAP comments, and approved `PENDING_DISCOVERY` blocks.

### 4. Escalate

Use `escalate-doc-gap` when a missing fact requires human input or source material.

## Creation Workflows

### ADR Creation

Use `create-adr` with:

```bash
python3 scaffold_adr.py "decision-title"
```

Do not hand-create ADR files or manually select ADR numbers.

### System / Bounded Context Creation

Use `create-system-scaffold` with:

```bash
python3 scaffold_system.py <system-name>
python3 scaffold_system.py <system-name> --title "Human-Readable Title"
```

Do not hand-create system folders.

### System Context Update

Use `create-system-context` for the linked context set:

```text
architecture/context/business-context.md
architecture/context/system-context.md
architecture/context/actors-and-roles.md
architecture/context/external-systems.md
```

Build a source-fact inventory before editing.

## Skill System Structure

```text
.claude/
  skills/
    README.md
    PLAN.md
    doc-loop-prepare/SKILL.md
    run-doc-checker/SKILL.md
    fix-doc-linter-failures/SKILL.md
    create-adr/SKILL.md
    create-system-scaffold/SKILL.md
    create-system-context/SKILL.md
    escalate-doc-gap/SKILL.md
    tests/
      trigger-cases.md
      example-transcripts.md
      trigger-cases.json
      repair-plan-fixture.md
      repair-plan-fixture.json
      skill-verifier-fixtures.json
      source-fact-citation-pattern.md
      source-fact-citation-pattern.json
      skill-retirement-policy.md
      skill-retirement-policy.json
```

Rules:

- Skill folder names use kebab-case.
- Each skill folder contains required `SKILL.md`.
- `SKILL.md` frontmatter includes `name` and `description`.
- Frontmatter `name` matches the folder name.
- Description includes trigger context using `Use when`.
- Parent-level `README.md`, `PLAN.md`, and `tests/` are allowed.
- Individual skill folders do not contain README files.

## Repository Control Files

These files define repository behavior and require human review when changed:

```text
agent/SKILL.md
agent/GOAL.md
agent_harness.py
run_validation.py
.validation-config.json
audit_ignore.py
.doc-audit-ignore
verify_docs.py
verify_e2e.py
verify_coverage.py
verify_claude_skills.py
verify_skill_trigger_fixtures.py
verify_repair_plan_fixtures.py
verify_skill_verifier_fixtures.py
verify_skill_verifier_execution.py
verify_source_fact_citation_fixtures.py
verify_skill_retirement_fixtures.py
scaffold_adr.py
scaffold_system.py
agent/prompts/
.github/
README.md
how-to-start.md
onboarding-dev.md
```

## Audit Boundary

`.claude/skills/**` is tracked runtime configuration, not active architecture documentation.

Current state:

- `.doc-audit-ignore` defines architecture-audit exclusions.
- `audit_ignore.py` provides shared ignore semantics.
- `verify_docs.py`, `verify_e2e.py`, and `verify_coverage.py` use `.doc-audit-ignore` for audit scope.
- `.claude/skills/**` is validated by `verify_claude_skills.py` and fixture validators.
- `.claude/` is not in `.gitignore`.

## Completed Backlog

| Item | Result |
|---|---|
| Skill trigger tests | Human-readable and machine-readable trigger cases added. |
| Example task transcripts | Behavioral transcripts added. |
| Repair-plan fixture | Human-readable and machine-readable repair-plan fixtures added. |
| Skill verifier fixtures | Positive and negative skill-validator fixtures added. |
| `.doc-audit-ignore` | Audit scope is now separated from Git tracking. |
| Source-fact citation pattern | Citation rules distinguish source facts, verifier output, policy, inference, and gaps. |
| Skill retirement policy | Skill lifecycle rules define active, deprecated, superseded, archived, and removed states. |
| Actual fixture execution harness | `verify_skill_verifier_execution.py` executes temporary skill trees against `verify_claude_skills.py`. |
| Local developer command wrapper | `run_validation.py` runs validation gates from `.validation-config.json`. |

## Future Backlog

| Item | Purpose |
|---|---|
| CI runner simplification | Replace expanded workflow verifier list with `python3 run_validation.py` once workflow editing is available. |
| Additional executable fixture harnesses | Expand execution harnesses beyond `verify_claude_skills.py` where useful. |

## Working Rule

```text
observe → plan → ask/escalate → repair → verify
```

Do not skip directly from request to mutation when repository policy, source facts, or verifier state are unknown.
