---
name: fix-doc-linter-failures
description: Repairs architecture documentation verifier failures using the repository agent policy, state file, and deterministic harness. Use when the documentation loop reports failed verify_docs.py or verify_e2e.py checks, when asked to fix doc linter failures, resolve broken documentation links, repair metadata headers, add ARCH-GAP owners, or make the loop pass without inventing missing architecture facts.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: documentation-automation
---

# fix-doc-linter-failures

## Purpose

Repair documentation verifier failures while staying inside the repository's agent policy.

This skill is mutation-capable, but only for files allowed by `agent/SKILL.md`. It must never modify harness, verifier, prompt, policy, workflow, onboarding, or README files.

## Required Inputs

Before proposing or applying any repair, read:

```text
agent/STATE.md
agent/SKILL.md
agent/GOAL.md
```

If `agent/STATE.md` is missing or stale, run:

```bash
python3 agent_harness.py --prepare
```

Then reread `agent/STATE.md`.

## Critical Rules

- Follow `agent/SKILL.md` over this skill if there is any conflict.
- Edit only paths allowed by the current `agent/SKILL.md` write allowlist.
- Never edit paths in the current `agent/SKILL.md` write blocklist.
- Do not edit `agent/SKILL.md`, `agent/GOAL.md`, `agent/prompts/`, verifier scripts, scaffold scripts, workflow files, root README, onboarding files, or archive files.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- Do not invent missing business, system, security, integration, actor, topology, or technology facts.
- Use `ARCH-GAP` with an owner when required facts are missing.
- Use the `PENDING_DISCOVERY` block only where repository rules require it.
- New ADRs must be created through `python3 scaffold_adr.py "title"`.
- New systems must be created through `python3 scaffold_system.py name`.
- Success is valid only when `python3 agent_harness.py --prepare` exits 2.

## Repair Workflow

### Step 1: Prepare State

Run:

```bash
python3 agent_harness.py --prepare
```

Interpret the exit code:

| Exit code | Meaning | Action |
|---|---|---|
| 2 | Success | Stop and report success |
| 1 | Escalated | Stop, read `agent/logs/ESCALATION.md`, and report the escalation reason |
| 0 | Continue | Read `agent/STATE.md` and repair only the reported failures |

### Step 2: Classify Failures

Classify each failing file by policy ownership:

| Failing path | Responsible repair owner |
|---|---|
| `architecture/context/` | Solutions Architect |
| `decisions/` | Solutions Architect |
| `architecture/views/` | Software Architect |
| `architecture/systems/` | Software Architect |
| `standards/` | Software Architect |
| `governance/risks.md` | Security Reviewer |
| `governance/assumptions.md` | Security Reviewer |
| `governance/open-questions.md` | Supervisor |
| `governance/migration_log.md` | Supervisor |
| `glossary.md` | Supervisor |
| Anything outside the write allowlist | Blocked; human review required |

### Step 3: Build a Minimal Repair Plan

Before editing, create a short plan with:

```markdown
## Repair Plan

| File | Failure | Proposed repair | Policy basis |
|---|---|---|---|
```

The repair must be the smallest change that satisfies the verifier without changing architectural meaning.

### Step 4: Apply Only Safe Repairs

Safe repairs include:

- Adding missing required document headers.
- Correcting `Document Status` to one of the allowed values.
- Fixing broken relative links when the intended target is unambiguous.
- Replacing absolute repo links with relative markdown links.
- Adding a required relative link to `glossary.md`.
- Adding an owner to an existing `ARCH-GAP` tag when the owner can be inferred from the document domain.
- Adding an `ARCH-GAP` with an owner when missing information blocks completion.
- Removing naked `TBD` only by replacing it with the approved `PENDING_DISCOVERY` block.

Unsafe repairs include:

- Choosing architecture topology.
- Inventing actors, integrations, APIs, systems, domains, infrastructure, or security controls.
- Resolving an `ARCH-GAP` without a cited source of truth.
- Creating ADR content manually instead of using the scaffold.
- Creating system folders manually instead of using the scaffold.
- Editing policy, prompt, harness, workflow, README, onboarding, or verifier files.

### Step 5: Verify

After applying repairs, run:

```bash
python3 agent_harness.py --prepare
```

Then:

- If exit code is 2, report success.
- If exit code is 0, report remaining failures and whether another iteration is safe.
- If exit code is 1, report escalation and read `agent/logs/ESCALATION.md`.

## Common Repair Patterns

### Missing header

Add the required header block at the top of the file:

```markdown
# [Document Title]

## Document Status
Draft

## Purpose
[One sentence describing what this document covers]

## Owner
Architecture Team

## Last Updated
YYYY-MM-DD
```

Do not guess a business owner. Use `Architecture Team` only for structural architecture repository ownership.

### Naked TBD

Replace naked `TBD` with:

```markdown
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD
```

### Missing unknown source of truth

Add:

```markdown
<!-- ARCH-GAP: [Short description of what is unknown]. [Owner: Architecture Team]. -->
```

Use a more specific owner only when the document domain makes it obvious, such as `Security Team`, `Product Team`, or `Business Team`.

### Broken relative link

Only fix a broken link when the intended target is clear from the existing text and repository structure. Otherwise add an `ARCH-GAP` or report the ambiguity.

### Orphaned document

Add one inbound link from the most appropriate index or parent document. Do not create unrelated links just to satisfy the verifier.

## Output Format

When complete, return:

```markdown
## Repairs Applied

## Verification Result

## Remaining Failures

## Escalations or Human Input Needed
```
