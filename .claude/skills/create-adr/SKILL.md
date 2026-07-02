---
name: create-adr
description: Creates Architecture Decision Records using the repository scaffold script and decision-readiness checks. Use when the user asks to create an ADR, record an architecture decision, document a topology choice, capture an accepted technical decision, or add a decision record without manually creating the ADR file.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: architecture-decision-records
---

# create-adr

## Purpose

Create Architecture Decision Records through the repository scaffold only.

This skill prevents manually created ADR files, numbering gaps, malformed headers, and invented decision content.

## Critical Rules

- Follow `agent/SKILL.md` over this skill if there is any conflict.
- Never create ADR markdown files by hand.
- Always use `python3 scaffold_adr.py "decision-title"` to create a new ADR.
- Do not edit `scaffold_adr.py`.
- Do not choose a decision for the user.
- Do not invent context, alternatives, consequences, technology choices, owners, or status.
- Do not resolve `PENDING_DISCOVERY` placeholders unless the user provides explicit source material in the current task.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- After scaffolding or editing an ADR, run `python3 agent_harness.py --prepare` and report the result.

## Required Inputs

Before creating an ADR, read:

```text
agent/SKILL.md
agent/GOAL.md
scaffold_adr.py
```

If the user expects the ADR to be filled beyond the scaffold template, also read any cited source documents that justify the decision.

## Decision Readiness Check

Before running the scaffold command, verify that the user has provided at least:

| Required item | Acceptable input |
|---|---|
| Decision title | A short architecture decision name |
| Decision intent | What decision is being recorded |
| Evidence source | User-provided notes, existing repo document, or explicit instruction to scaffold only |

If the user only asks to create an empty ADR shell, the evidence source can be `scaffold only`.

If the user asks for a populated ADR but does not provide sufficient decision content, stop and ask for the missing source material. Do not fill the ADR from general knowledge.

## Title Normalization

Convert the decision title into a concise command argument:

- Use lower-case words separated by hyphens when practical.
- Remove filler words.
- Keep the title focused on the decision, not the implementation task.

Examples:

| User phrase | Command argument |
|---|---|
| Create an ADR for using PostgreSQL as primary storage | `use-postgresql-for-primary-storage` |
| Record the decision to use a modular monolith | `use-modular-monolith` |
| Add an ADR for API versioning strategy | `api-versioning-strategy` |

## Creation Workflow

### Step 1: Run the scaffold

```bash
python3 scaffold_adr.py "decision-title"
```

The script will create:

```text
decisions/NNNN-decision-title.md
```

### Step 2: Read the created ADR

Open the new ADR file and confirm:

- Sequential ADR number is present.
- Required metadata header is present.
- `Document Status` is `Draft`.
- Glossary link is present.
- Context, Decision, Consequences, Related Decisions, and References remain explicitly marked as pending discovery unless provided source content exists.

### Step 3: Optional population

Populate ADR content only when the user provides explicit decision content or points to an existing active repository source.

Allowed source examples:

- Current user-provided notes in the task.
- Active files under `architecture/`, `standards/`, `decisions/`, `governance/`, or `glossary.md`.
- External source material pasted or explicitly provided by the user.

Not allowed:

- General model knowledge.
- Assumptions about the system.
- Deprecated content from `archive/` unless explicitly requested.

### Step 4: Verify

Run:

```bash
python3 agent_harness.py --prepare
```

Interpret the result:

| Exit code | Meaning | Action |
|---|---|---|
| 2 | Success | Report success |
| 1 | Escalated | Read `agent/logs/ESCALATION.md` and report the escalation reason |
| 0 | Continue | Report remaining verifier failures without inventing content |

## ADR Quality Checklist

When ADR content is being populated, ensure the ADR answers these questions:

| Section | Required answer |
|---|---|
| Context | What problem, constraint, or force makes a decision necessary? |
| Decision | What is the chosen direction, stated clearly? |
| Positive consequences | What improves because of this decision? |
| Negative consequences | What trade-offs or risks are introduced? |
| Neutral consequences | What changes operationally without being clearly good or bad? |
| Related decisions | Which ADRs does this depend on, supersede, or constrain? |
| References | What active repo docs or external sources support the decision? |

If any answer is unknown, leave the existing `PENDING_DISCOVERY` block in place or add an `ARCH-GAP` with an owner if the verifier requires a trackable gap.

## Output Format

Return:

```markdown
## ADR Created

## Command Used

## Content Populated

## Verification Result

## Remaining Gaps or Human Input Needed
```
