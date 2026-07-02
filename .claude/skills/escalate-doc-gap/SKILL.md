---
name: escalate-doc-gap
description: Records and escalates documentation gaps when required architecture, business, security, integration, or ownership facts are missing. Use when the documentation loop cannot proceed safely, when PENDING_DISCOVERY cannot be resolved, when an ARCH-GAP needs an owner, when open questions must be logged, or when human input is required to avoid invented documentation.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: documentation-governance
---

# escalate-doc-gap

## Purpose

Escalate missing information instead of inventing documentation.

This skill creates a clean stop path when a documentation task requires human knowledge, authoritative source material, or a decision that the agent is not allowed to make.

## Critical Rules

- Follow `agent/SKILL.md` over this skill if there is any conflict.
- Do not resolve a gap from general model knowledge.
- Do not choose architecture topology, system scope, actor permissions, external integrations, security controls, or ownership for the user.
- Do not edit policy, prompts, verifier scripts, scaffold scripts, workflows, root README, onboarding files, or archive files.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- Every `ARCH-GAP` must include an owner.
- Prefer logging a clear open question over adding vague placeholder text.
- After adding or updating gap records, run `python3 agent_harness.py --prepare` and report the result.

## When to Use

Use this skill when any of these are true:

- A required section is marked `PENDING_DISCOVERY` and no source material is available.
- A verifier failure cannot be fixed without deciding a missing fact.
- A proposed repair would require inventing actors, integrations, ownership, scope, or architecture decisions.
- An `ARCH-GAP` exists without sufficient owner or impacted-document context.
- The same verifier failures repeat and the loop risks no-progress escalation.
- Human review is required before the documentation can safely advance.

## Required Inputs

Read:

```text
agent/SKILL.md
agent/GOAL.md
agent/STATE.md
governance/open-questions.md
governance/assumptions.md
governance/risks.md
```

Also read the specific document containing the unresolved gap.

If `agent/STATE.md` is missing or stale, run:

```bash
python3 agent_harness.py --prepare
```

Then reread `agent/STATE.md`.

## Gap Classification

Classify the gap before writing anything:

| Gap type | Use | Primary record |
|---|---|---|
| Open question | Required fact is unknown and must be answered | `governance/open-questions.md` |
| Assumption | Temporary working belief is needed and must be validated | `governance/assumptions.md` |
| Risk | Unknown or unresolved issue creates delivery, security, compliance, or architecture exposure | `governance/risks.md` |
| Inline architecture gap | A specific section cannot be completed | `ARCH-GAP` comment in the impacted document |
| Harness escalation | Loop cannot safely continue | `agent/logs/ESCALATION.md` through the harness |

Do not use an assumption when the system cannot safely proceed without an answer. Use an open question instead.

## Owner Selection

Use the most specific defensible owner:

| Gap domain | Owner |
|---|---|
| Business objective, stakeholder, KPI, scope | Business Team |
| Product behavior, workflow, user-facing capability | Product Team |
| Architecture boundary, topology, module ownership | Architecture Team |
| Engineering implementation detail | Engineering Team |
| Security, permission, identity, threat model | Security Team |
| Operations, deployment, monitoring, runbook | Operations Team |
| Finance, ledger, reconciliation, payment control | Finance Team |
| Unknown owner | Architecture Team |

Do not invent a named individual.

## Inline ARCH-GAP Format

Use this exact format:

```markdown
<!-- ARCH-GAP: [Short description of what is unknown]. [Owner: Architecture Team]. -->
```

The description must state what is unknown, not what the answer might be.

Good:

```markdown
<!-- ARCH-GAP: External identity provider ownership and supported authentication flows are not documented. [Owner: Security Team]. -->
```

Bad:

```markdown
<!-- ARCH-GAP: Use Okta for identity. [Owner: Security Team]. -->
```

## Open Question Format

When adding to `governance/open-questions.md`, append a row to the table:

```markdown
| OQ-001 | What identity provider owns analyst authentication? | Security Team | architecture/context/actors-and-roles.md, architecture/context/system-context.md | OPEN | TBD |
```

Rules:

- Use the next sequential `OQ-NNN` ID if existing IDs are present.
- If existing rows use placeholders only, start at `OQ-001`.
- Status must be `OPEN`, `RESEARCHING`, or `RESOLVED`.
- Resolution remains `TBD` until answered by a source.

## Assumption Format

When adding to `governance/assumptions.md`, append a row:

```markdown
| AS-001 | The Billing Ledger API remains the system of record for reconciled payment outcomes. | Confirm with Finance Team and architecture owner. | OPEN |
```

Use assumptions only when temporary progress is safe.

## Risk Format

When adding to `governance/risks.md`, append a row:

```markdown
| R-001 | External gateway API limits may delay reconciliation windows. | Daily reconciliation SLA could be missed. | Validate rate limits and define backoff strategy. | OPEN |
```

Use risks when the unresolved gap creates delivery, reliability, security, compliance, or operational exposure.

## Escalation Workflow

### Step 1: Identify blocked fact

Write the blocked fact as a question:

```markdown
What fact is missing?
Which document needs it?
Who can answer it?
What happens if it remains unknown?
```

### Step 2: Choose record type

- Use inline `ARCH-GAP` when a specific document section is incomplete.
- Use `open-questions.md` when the team must answer a fact.
- Use `assumptions.md` only when a temporary belief is safe and explicitly labeled.
- Use `risks.md` when unresolved ambiguity creates exposure.

### Step 3: Apply minimal update

Make the smallest change needed to make the gap visible and owned.

### Step 4: Verify

Run:

```bash
python3 agent_harness.py --prepare
```

Report the exit code and remaining failures.

## Output Format

Return:

```markdown
## Gap Escalated

## Gap Type

## Owner

## Files Updated

## Verification Result

## Human Answer Needed
```
