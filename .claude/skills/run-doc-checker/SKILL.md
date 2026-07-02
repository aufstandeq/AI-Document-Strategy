---
name: run-doc-checker
description: Performs read-only documentation compliance review and produces a bounded repair plan before mutation. Use when the user asks to check proposed documentation changes, review a repair plan, validate a Maker diff, classify verifier failures, or prepare the next safe repair step before running fix-doc-linter-failures.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: documentation-review
---

# run-doc-checker

## Purpose

Review documentation failures or proposed changes without modifying files.

This skill is a read-only planning and compliance gate. It creates the repair plan that `fix-doc-linter-failures` may later execute, and it can also check a proposed Maker diff against `agent/SKILL.md` before any changes are applied.

## Operating Modes

Use one of two modes:

| Mode | Use when | Output |
|---|---|---|
| Failure planning mode | Verifier output or `agent/STATE.md` shows failures | A file-by-file repair plan |
| Diff review mode | A Maker/Supervisor diff already exists | PASS/FAIL compliance review plus repair-plan corrections |

Do not mix modes unless the user explicitly asks for both.

## Critical Rules

- Do not edit files.
- Do not create commits.
- Do not run scaffold scripts.
- Do not resolve missing facts.
- Do not invent actors, integrations, system boundaries, risks, assumptions, decisions, ownership, or technical facts.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- Enforce `agent/SKILL.md` as the governing policy.
- Treat `verify_docs.py`, `verify_e2e.py`, and `agent_harness.py --prepare` as deterministic validation authorities.
- Treat Checker PASS as permission to proceed to deterministic validation, not as final success.

## Required Inputs

Read:

```text
agent/SKILL.md
agent/GOAL.md
agent/STATE.md
agent/prompts/checker_system_prompt.md
```

If `agent/STATE.md` is missing or stale, run:

```bash
python3 agent_harness.py --prepare
```

Then reread `agent/STATE.md`.

Only read failing or proposed target files when needed to produce a specific repair plan.

## Failure Planning Mode

Use this mode when the task is to plan repairs from verifier failures.

### Step 1: Prepare state

Run:

```bash
python3 agent_harness.py --prepare
```

Interpret exit code:

| Exit code | Meaning | Action |
|---|---|---|
| 2 | Success | Stop and report no repair plan is needed |
| 1 | Escalated | Stop, read `agent/logs/ESCALATION.md`, and report the escalation reason |
| 0 | Continue | Read `agent/STATE.md` and produce a repair plan |

### Step 2: Classify each failure

Classify each failure by the target file and rule type:

| Failure type | Typical repair |
|---|---|
| Missing H1 | Add compliant H1 title |
| Missing metadata header | Add required `Document Status`, `Purpose`, `Owner`, or `Last Updated` section |
| Invalid status | Change to `Draft`, `In Review`, `Approved`, or `Deprecated` |
| Broken relative link | Correct the relative path if target is unambiguous |
| Absolute path link | Replace with a relative path |
| Missing glossary link | Add relative glossary link in a natural context |
| Orphan document | Add inbound link from appropriate parent/index only if semantically valid |
| ARCH-GAP missing owner | Add owner only if domain is defensible; otherwise use `Architecture Team` |
| ADR sequence gap | Use scaffold rules or escalate; do not manually renumber unless explicitly instructed |
| Broken system reference | Link to existing system or scaffold only when boundary is confirmed |
| Missing fact | Add `ARCH-GAP`, open question, assumption, or risk instead of inventing content |
| Blocklisted file | Human review required |

### Step 3: Assign repair owner

| Target path | Responsible specialist |
|---|---|
| `architecture/context/` | Solutions Architect |
| `decisions/` | Solutions Architect |
| `architecture/views/` | Software Architect |
| `architecture/systems/` | Software Architect |
| `standards/` | Software Architect, unless blocked by current policy |
| `governance/risks.md` | Security Reviewer |
| `governance/assumptions.md` | Security Reviewer |
| `governance/open-questions.md` | Supervisor |
| `governance/migration_log.md` | Supervisor |
| `glossary.md` | Supervisor |
| Anything outside allowlist | Human review required |

If `agent/SKILL.md` allowlist and blocklist conflict, classify the target as blocked and require human review. Do not resolve policy conflict implicitly.

### Step 4: Produce repair plan

Return a minimal repair plan. Each planned repair must be:

- Specific enough for `fix-doc-linter-failures` to execute.
- Bound to one target file.
- Mapped to a policy basis.
- Explicit about whether source facts are required.
- Explicit about whether the repair is safe, unsafe, or blocked.

## Diff Review Mode

Use this mode when a proposed Maker/Supervisor diff already exists.

Review each proposed change against `agent/SKILL.md` and the Checker prompt.

Checks:

1. Target file is inside the write allowlist.
2. Target file is not in the write blocklist.
3. Change addresses the stated failure.
4. Change does not create a new verifier failure.
5. Change does not invent missing `PENDING_DISCOVERY` content.
6. Scaffold-required actions use scaffold scripts rather than manual file creation.
7. Proposed links are relative and likely to resolve.
8. Proposed `ARCH-GAP` comments include an owner.

Return `PASS` only if every proposed change is compliant.

## Safe Repair Categories

Safe to recommend:

- Add missing required metadata headers.
- Normalize `Document Status` to an allowed value.
- Correct obvious relative links.
- Replace absolute links with relative links.
- Add glossary link to active architecture docs.
- Add missing owner to `ARCH-GAP` when domain ownership is defensible.
- Replace naked `TBD` with approved `PENDING_DISCOVERY` block.
- Add open question when source facts are missing.

Not safe to recommend as direct repair:

- Define a system boundary without source evidence.
- Add an actor not documented by source material.
- Add an external system not documented by source material.
- Resolve an ADR decision without a real decision.
- Invent risks, assumptions, controls, APIs, owners, or dependencies.
- Edit verifier, harness, prompt, policy, workflow, README, onboarding, or archive files.

## Output Format: Failure Planning Mode

Return:

```markdown
## Checker Mode
Failure planning

## Loop Status

## Repair Plan

| File | Failure | Responsible specialist | Proposed repair | Policy basis | Source facts required | Status |
|---|---|---|---|---|---|---|

## Blocked Items

## Recommended Next Skill
```

For `Status`, use exactly one of:

```text
SAFE_TO_REPAIR
REQUIRES_SOURCE_FACTS
BLOCKED_POLICY
HUMAN_REVIEW_REQUIRED
NO_REPAIR_NEEDED
```

## Output Format: Diff Review Mode

Return a JSON object:

```json
{
  "result": "PASS",
  "issues": [],
  "repair_plan_adjustments": []
}
```

Or:

```json
{
  "result": "FAIL",
  "issues": [
    {
      "file": "relative/path/to/file.md",
      "change_index": 0,
      "issue": "Specific problem",
      "rule": "agent/SKILL.md section or checker rule"
    }
  ],
  "repair_plan_adjustments": [
    {
      "file": "relative/path/to/file.md",
      "recommended_action": "Specific correction before mutation"
    }
  ]
}
```

## Recommended Next Skill Rules

- If all planned repairs are `SAFE_TO_REPAIR`, recommend `fix-doc-linter-failures`.
- If any item is `REQUIRES_SOURCE_FACTS`, recommend `escalate-doc-gap` or ask the user for source material.
- If any item is `BLOCKED_POLICY`, recommend human review before mutation.
- If no failures remain, recommend no further repair skill.
