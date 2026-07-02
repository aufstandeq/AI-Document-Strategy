# Claude Skills Operating Plan

## Purpose

This plan defines the end state for the Claude skill system being added to the AI-Document-Strategy repository.

The goal is not to create a pile of prompts. The goal is to create a controlled documentation operating model where Claude can:

- Understand the repository rules.
- Prepare the deterministic documentation loop.
- Review failures before mutation.
- Apply bounded repairs.
- Use scaffold scripts instead of hand-created structures.
- Stop cleanly when human source facts are missing.
- Preserve the architecture repository as the source of truth.

This file is a planning and visibility artifact for the skill system. It is not active architecture documentation.

## Target End State

The end state is a self-contained Claude Code skill layer that sits on top of the existing repository controls.

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

The skill layer must never bypass the repository's deterministic controls. The success authority remains the verifier and harness layer.

## Non-Goals

The skill system must not:

- Replace `agent_harness.py`.
- Replace `verify_docs.py`, `verify_e2e.py`, or `verify_coverage.py`.
- Let Claude edit its own control plane without human review.
- Resolve architecture facts from model knowledge.
- Invent actors, integrations, boundaries, ownership, risks, decisions, or dependencies.
- Treat `.claude/skills/**` as active architecture documentation.
- Hide tracked skill files in `.gitignore`.

## Operating Principles

| Principle | Meaning |
|---|---|
| Observe before mutate | Always inspect harness state and policy before editing. |
| Policy before skill | `agent/SKILL.md` overrides any individual Claude skill. |
| Scaffold before hand-create | ADRs and systems must be created through repo scaffold scripts. |
| Source facts before content | No architecture content is populated without explicit source material. |
| Repair plan before repair | Checker produces the repair plan before mutation. |
| Escalate instead of invent | Missing facts become owned gaps, open questions, assumptions, or risks. |
| Deterministic verification wins | Success is valid only after the repo verifier/harness passes. |

## Current Skill Set

| Skill | Status | Mutation | Purpose |
|---|---|---:|---|
| `doc-loop-prepare` | Added | No | Prepare the documentation loop and classify the next safe action. |
| `run-doc-checker` | Added | No | Review verifier failures or proposed diffs and produce a repair plan. |
| `fix-doc-linter-failures` | Added | Yes, bounded | Execute safe verifier/linter repairs inside policy. |
| `create-adr` | Added | Yes, scaffold only | Create ADRs through `scaffold_adr.py`. |
| `create-system-scaffold` | Added | Yes, scaffold only | Create system folders through `scaffold_system.py`. |
| `create-system-context` | Added | Yes, bounded | Update C4 context documents from explicit source facts. |
| `escalate-doc-gap` | Added | Yes, bounded | Record missing human-owned facts instead of inventing content. |

## Core Workflow

### 1. Prepare

Skill:

```text
doc-loop-prepare
```

Purpose:

- Run `python3 agent_harness.py --prepare`.
- Read `agent/STATE.md`, `agent/SKILL.md`, and `agent/GOAL.md`.
- Classify whether the loop is successful, blocked, escalated, or ready for repair planning.

Output:

```text
Loop Status
Failing Files
Responsible Specialist
Recommended Next Action
Blockers or Human Input Needed
```

### 2. Check and Plan

Skill:

```text
run-doc-checker
```

Purpose:

- Review verifier failures or proposed Maker diffs.
- Produce a repair plan.
- Classify each item as safe, source-dependent, blocked, or human-review-required.

Output:

```text
Repair Plan
Blocked Items
Recommended Next Skill
```

### 3. Repair

Skill:

```text
fix-doc-linter-failures
```

Purpose:

- Apply only safe repairs identified by the checker.
- Stay inside the write allowlist.
- Avoid blocklisted files.
- Preserve unknowns as `PENDING_DISCOVERY` or `ARCH-GAP`.

Output:

```text
Repairs Applied
Verification Result
Remaining Failures
Escalations or Human Input Needed
```

### 4. Escalate When Needed

Skill:

```text
escalate-doc-gap
```

Purpose:

- Convert missing facts into owned open questions, assumptions, risks, or inline `ARCH-GAP` comments.
- Prevent hallucinated completion.

Output:

```text
Gap Escalated
Gap Type
Owner
Files Updated
Verification Result
Human Answer Needed
```

## Creation Workflows

### ADR Creation

Skill:

```text
create-adr
```

Command contract:

```bash
python3 scaffold_adr.py "decision-title"
```

Rules:

- Do not manually create ADR files.
- Do not manually select ADR numbers.
- Do not invent context, alternatives, consequences, or decision rationale.
- Populate content only from explicit source facts.

### System / Bounded Context Creation

Skill:

```text
create-system-scaffold
```

Command contract:

```bash
python3 scaffold_system.py <system-name>
python3 scaffold_system.py <system-name> --title "Human-Readable Title"
```

Rules:

- Do not manually create `architecture/systems/<name>/` folders.
- Do not link the new system into indexes or views unless the boundary is confirmed.
- Do not invent scope, dependencies, data ownership, or interfaces.

### System Context Update

Skill:

```text
create-system-context
```

Controlled document set:

```text
architecture/context/business-context.md
architecture/context/system-context.md
architecture/context/actors-and-roles.md
architecture/context/external-systems.md
```

Rules:

- Treat these files as a linked context set.
- Build a source-fact inventory before editing.
- Keep C4 Level 1 context separate from implementation/deployment detail.
- Do not invent actors, integrations, or system responsibilities.

## Skill System Structure

```text
.claude/
  skills/
    README.md
    PLAN.md
    doc-loop-prepare/
      SKILL.md
    run-doc-checker/
      SKILL.md
    fix-doc-linter-failures/
      SKILL.md
    create-adr/
      SKILL.md
    create-system-scaffold/
      SKILL.md
    create-system-context/
      SKILL.md
    escalate-doc-gap/
      SKILL.md
```

Rules:

- Each skill folder contains exactly one required `SKILL.md` entrypoint.
- Parent-level `README.md` is allowed for human navigation.
- Parent-level `PLAN.md` is allowed for roadmap and end-state visibility.
- Individual skill folders should not contain README files.

## Repository Control Plane

The skill layer depends on, but must not casually modify, the following control-plane files:

```text
agent/SKILL.md
agent/GOAL.md
agent_harness.py
verify_docs.py
verify_e2e.py
verify_coverage.py
scaffold_adr.py
scaffold_system.py
agent/prompts/
.github/
README.md
how-to-start.md
onboarding-dev.md
```

Edits to these files require human review because they change the operating rules, not just documentation content.

## Audit Boundary

`.claude/skills/**` is tracked runtime configuration.

It is excluded from architecture-document validation because skill files do not use the architecture-document metadata contract.

Current state:

- `.claude/` is excluded directly in `verify_docs.py`.
- `.claude/` is excluded directly in `verify_e2e.py`.
- `.claude/` is not in `.gitignore`.

Future state:

- Add a dedicated `.doc-audit-ignore` or equivalent file.
- Move non-architecture Markdown exclusions into that file.
- Keep Git tracking and architecture-audit scope as separate concerns.

Tracked as issue #2.

## Completion Criteria for This PR

The current PR is complete when:

- The seven core skills are present.
- The parent skills index exists.
- This operating plan exists.
- `.claude/` remains tracked by Git.
- Architecture audits ignore `.claude/` as non-architecture Markdown.
- GitHub Actions passes.
- PR body explains the operating model clearly.

## Future Backlog

### Near-term

| Item | Purpose |
|---|---|
| Skill frontmatter validator | Check required frontmatter, kebab-case folders, and `SKILL.md` naming. |
| Skill trigger tests | Verify each skill's description triggers for intended requests and does not over-trigger. |
| Example task transcripts | Add concise examples showing the intended skill sequence. |
| Repair-plan fixture | Provide sample verifier failures and expected `run-doc-checker` repair plan output. |

### Later

| Item | Purpose |
|---|---|
| `.doc-audit-ignore` | Decouple audit scope from Git tracking and hardcoded verifier exclusions. |
| Skill smoke test in CI | Validate skill folder structure on pull requests. |
| Source-fact citation pattern | Standardize how source facts are cited in generated repair plans. |
| Skill retirement policy | Define how outdated skills are deprecated without deleting history. |

## Open Questions

| Question | Owner | Status |
|---|---|---|
| Should skill validation become part of the existing Architecture Repo Audit workflow? | Architecture Team | Open |
| Should `.claude/skills/PLAN.md` remain long-term, or move into `agent/docs/` after the skill system stabilizes? | Architecture Team | Open |
| Should future skills be grouped by lifecycle stage, such as prepare/check/repair/create/escalate? | Architecture Team | Open |

## Working Rule

When unsure, prefer the safer path:

```text
observe → plan → ask/escalate → repair → verify
```

Do not skip directly from request to mutation when repository policy, source facts, or verifier state are unknown.
