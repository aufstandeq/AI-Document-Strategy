---
name: doc-loop-prepare
description: Prepares the architecture documentation loop by running the deterministic verifier harness, reading agent state and policy files, and producing a bounded next-action brief. Use when starting, resuming, checking, or troubleshooting the documentation maintenance loop, especially after requests like prepare the doc loop, run the documentation harness, check agent state, or tell me what the loop should do next.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: documentation-automation
---

# doc-loop-prepare

## Purpose

Prepare the repository documentation loop without modifying files.

This skill is a read-only entrypoint. It runs the deterministic harness, reads the generated state, and translates verifier output into a concise action brief for the next safe step.

## Critical Rules

- Do not edit files.
- Do not create commits.
- Do not resolve missing business, architecture, security, or integration facts by invention.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- Treat `agent/SKILL.md` as policy.
- Treat `agent/GOAL.md` as the success contract.
- Treat `verify_docs.py` and `verify_e2e.py` as the only success authorities.
- If the harness reports success, stop and report success.
- If the harness reports escalation, stop and report the escalation reason.

## Required Sequence

Run from the repository root:

```bash
python3 agent_harness.py --prepare
```

Then read these files:

```text
agent/STATE.md
agent/SKILL.md
agent/GOAL.md
```

Optional read-only context, only if needed to classify the failure:

```text
agent/README.md
agent/prompts/supervisor_prompt.md
agent/prompts/solutions_architect_prompt.md
agent/prompts/software_architect_prompt.md
agent/prompts/security_reviewer_prompt.md
agent/prompts/checker_system_prompt.md
```

## Classification Rules

Classify the next action by failing path:

| Failing path | Responsible role |
|---|---|
| `architecture/context/` | Solutions Architect |
| `decisions/` | Solutions Architect |
| `architecture/views/` | Software Architect |
| `architecture/systems/` | Software Architect |
| `standards/` | Software Architect |
| `governance/risks.md` | Security Reviewer |
| `governance/assumptions.md` | Security Reviewer |
| `governance/open-questions.md` | Supervisor |
| `glossary.md` | Supervisor |
| `agent/STATE.md` | Orchestrator |
| Any verifier, scaffold, workflow, prompt, README, or policy file | Blocked or human review required |

If the failing path is outside the write allowlist in `agent/SKILL.md`, classify it as blocked.

## Output Format

Return exactly these sections:

```markdown
## Loop Status

## Failing Files

## Responsible Specialist

## Recommended Next Action

## Blockers or Human Input Needed
```

## Recommended Next Action Rules

- If the next action is safe, name the responsible specialist and the specific file scope.
- If a missing fact is required, recommend adding an `ARCH-GAP` with an owner rather than inventing content.
- If the issue requires editing harness, policy, prompt, workflow, README, or verifier files, classify as human review required.
- If no failures remain, report that the loop is complete only when the harness reports both verifiers passed.

## Common Failure Handling

### Harness command fails

Report the command failure and stop. Do not approximate verifier output.

### `agent/STATE.md` is missing

Run:

```bash
python3 agent_harness.py --reset
python3 agent_harness.py --prepare
```

Then read `agent/STATE.md`.

### Same failures repeat

If the state indicates no progress or escalation, stop and surface the escalation reason instead of proposing another edit loop.

### Unknown business or system context

Do not infer. Recommend an `ARCH-GAP` with an owner or ask the user for the missing source of truth.
