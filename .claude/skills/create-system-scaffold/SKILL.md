---
name: create-system-scaffold
description: Creates a new system or bounded-context folder using the repository scaffold script. Use when the user asks to add a system, create a bounded context, scaffold a system folder, document a new architecture system area, or prepare system documentation without manually copying templates.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: architecture-systems
---

# create-system-scaffold

## Purpose

Create a new system or bounded-context documentation folder through the repository scaffold only.

This skill prevents hand-created system folders, malformed system index files, missing component directories, and template-copy drift.

## Critical Rules

- Follow `agent/SKILL.md` over this skill if there is any conflict.
- Never create folders under `architecture/systems/` by hand.
- Always use `python3 scaffold_system.py <system-name>` to create a new system folder.
- Use `--title "Human-Readable Title"` when the user provides a display title.
- Do not edit `scaffold_system.py`.
- Do not choose a system boundary for the user.
- Do not invent purpose, scope, dependencies, components, ownership, integrations, technologies, or quality attributes.
- Do not resolve `PENDING_DISCOVERY` placeholders unless the user provides explicit source material in the current task.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- After scaffolding or editing a system document, run `python3 agent_harness.py --prepare` and report the result.

## Required Inputs

Before creating a system scaffold, read:

```text
agent/SKILL.md
agent/GOAL.md
scaffold_system.py
architecture/systems/system-template/index.md
architecture/index.md
architecture/views/logical-view.md
```

If the user expects the system index to be populated beyond the scaffold template, also read any cited active source documents that justify the system boundary.

## System Readiness Check

Before running the scaffold command, verify that the user has provided at least:

| Required item | Acceptable input |
|---|---|
| System name | A short slug or natural-language system / bounded-context name |
| System intent | What system or bounded context is being documented |
| Evidence source | User-provided notes, existing repo document, or explicit instruction to scaffold only |

If the user asks only to create an empty system shell, the evidence source can be `scaffold only`.

If the user asks for a populated system document but does not provide sufficient source material, stop and ask for the missing source. Do not fill the system document from general knowledge.

## Name Normalization

The scaffold script normalizes the system name into a lowercase hyphenated slug.

Examples:

| User phrase | Command |
|---|---|
| Add Payments system | `python3 scaffold_system.py payments --title "Payments"` |
| Create Order Management bounded context | `python3 scaffold_system.py order-management --title "Order Management"` |
| Scaffold customer identity | `python3 scaffold_system.py customer-identity --title "Customer Identity"` |

Use a concise slug. Do not include words like `system`, `service`, or `bounded-context` unless they are part of the actual domain name.

## Creation Workflow

### Step 1: Confirm the target does not already exist

Check:

```text
architecture/systems/<system-name>/
```

If it exists, do not run the scaffold. Read the existing `index.md` and report that the system already exists.

### Step 2: Run the scaffold

For a slug only:

```bash
python3 scaffold_system.py <system-name>
```

For a display title:

```bash
python3 scaffold_system.py <system-name> --title "Human-Readable Title"
```

The script creates:

```text
architecture/systems/<system-name>/
architecture/systems/<system-name>/index.md
architecture/systems/<system-name>/components/
```

### Step 3: Read the created index

Confirm:

- H1 title matches the intended display title.
- `Document Status` is present.
- `Purpose`, `Owner`, and `Last Updated` are present.
- The `Last Updated` date was set by the scaffold.
- The glossary link resolves through `../../../glossary.md`.
- Placeholder sections remain explicitly marked as pending discovery unless source content exists.

### Step 4: Optional population

Populate system content only when the user provides explicit source material or points to an active repository source.

Allowed source examples:

- Current user-provided notes in the task.
- Active files under `architecture/`, `standards/`, `decisions/`, `governance/`, or `glossary.md`.
- Explicit external source material provided by the user.

Not allowed:

- General model knowledge.
- Assumptions about a common software architecture.
- Deprecated content from `archive/` unless explicitly requested.
- Existing code assumptions unless the user explicitly asks to use implementation discovery.

### Step 5: Link the new system

The scaffold script prints a reminder to link the new system from:

```text
architecture/views/logical-view.md
architecture/index.md
```

Only add these links when the system boundary is confirmed by source material or the user explicitly instructs that the system is in scope.

If the boundary is not confirmed, leave the scaffolded system document as draft and add an `ARCH-GAP` or open question rather than creating misleading index/view links.

### Step 6: Verify

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

## System Document Quality Checklist

When system content is being populated, ensure the document answers these questions:

| Section | Required answer |
|---|---|
| Purpose | Why does this system or bounded context exist? |
| Scope | What responsibilities are inside the boundary? |
| Non-responsibilities | What is explicitly outside the boundary? |
| Interfaces | What systems, actors, or external services interact with it? |
| Data ownership | What data does this system own, if any? |
| Dependencies | What does it rely on? |
| Quality attributes | What reliability, security, performance, or operability expectations apply? |
| Open questions | What must humans confirm before the document can move beyond Draft? |

If any answer is unknown, leave the existing `PENDING_DISCOVERY` block in place or add an `ARCH-GAP` with an owner if the verifier requires a trackable gap.

## Output Format

Return:

```markdown
## System Scaffold Created

## Command Used

## Content Populated

## Links Added

## Verification Result

## Remaining Gaps or Human Input Needed
```
