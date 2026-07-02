# Claude Skill Trigger Cases

## Purpose

This file defines expected Claude skill activation behavior for common documentation operating tasks.

These are human-readable trigger tests. They are not active architecture documentation and should not be interpreted as repository facts.

## Test Status Values

| Status | Meaning |
|---|---|
| `SHOULD_TRIGGER` | The named skill should be selected for this request. |
| `SHOULD_NOT_TRIGGER` | The named skill should not be selected for this request. |
| `AMBIGUOUS_ASK_CLARIFYING_QUESTION` | The request lacks enough intent to safely select one skill. |

## Core Loop Trigger Cases

| User request | Expected skill | Status | Rationale |
|---|---|---|---|
| Run the documentation loop and tell me what needs to happen next. | `doc-loop-prepare` | `SHOULD_TRIGGER` | The request asks for loop preparation and next-action classification. |
| Check the repo state before we make any documentation edits. | `doc-loop-prepare` | `SHOULD_TRIGGER` | The request is observe-before-mutate. |
| Fix whatever the architecture linter is complaining about. | `run-doc-checker` | `SHOULD_TRIGGER` | The safe first step is repair planning, not mutation. |
| Review these proposed doc changes before applying them. | `run-doc-checker` | `SHOULD_TRIGGER` | The request asks for diff review. |
| Apply the safe linter fixes from the repair plan. | `fix-doc-linter-failures` | `SHOULD_TRIGGER` | The request references an existing repair plan and asks for bounded mutation. |
| Repair missing headers and broken links only. | `fix-doc-linter-failures` | `SHOULD_TRIGGER` | The request asks for bounded verifier/linter repair. |
| Fill in all the unknown architecture details so the docs pass. | `escalate-doc-gap` | `SHOULD_TRIGGER` | Unknown facts must be escalated, not invented. |
| Add an open question for the missing integration owner. | `escalate-doc-gap` | `SHOULD_TRIGGER` | The request asks to record a missing human-owned fact. |

## Creation Trigger Cases

| User request | Expected skill | Status | Rationale |
|---|---|---|---|
| Create an ADR for choosing Postgres as the primary database. | `create-adr` | `SHOULD_TRIGGER` | ADR creation must use `scaffold_adr.py`. |
| Add a new decision record named API Gateway Boundary. | `create-adr` | `SHOULD_TRIGGER` | Decision record creation maps to ADR scaffolding. |
| Scaffold a Payments bounded context. | `create-system-scaffold` | `SHOULD_TRIGGER` | System/bounded-context folder creation must use `scaffold_system.py`. |
| Add a Customer Identity system folder but leave it as draft. | `create-system-scaffold` | `SHOULD_TRIGGER` | The request asks for scaffold-only system creation. |
| Rebuild the C4 system context from these notes. | `create-system-context` | `SHOULD_TRIGGER` | The request targets coordinated C4/context documents. |
| Update actors and external systems from the supplied source notes. | `create-system-context` | `SHOULD_TRIGGER` | The request targets the context quartet and source-fact extraction. |

## Negative Trigger Cases

| User request | Skill that should not trigger | Status | Rationale |
|---|---|---|---|
| What is C4 architecture? | `create-system-context` | `SHOULD_NOT_TRIGGER` | This is a learning question, not a repo mutation task. |
| Explain what an ADR is. | `create-adr` | `SHOULD_NOT_TRIGGER` | This is conceptual explanation, not ADR creation. |
| Rewrite this paragraph to be clearer. | `fix-doc-linter-failures` | `SHOULD_NOT_TRIGGER` | Generic writing is not a verifier/linter repair. |
| Show me the current skills in the repo. | `doc-loop-prepare` | `SHOULD_NOT_TRIGGER` | This is navigation/inspection, not loop preparation. |
| Create a production deployment architecture from best practices. | `create-system-context` | `SHOULD_NOT_TRIGGER` | This would require source facts; do not generate architecture from general knowledge. |
| Add a system using whatever name makes sense. | `create-system-scaffold` | `AMBIGUOUS_ASK_CLARIFYING_QUESTION` | The system boundary/name is missing. |

## Skill Selection Rule

When a request could trigger both a planning skill and a mutation skill, prefer the planning skill unless the user explicitly refers to an existing approved repair plan.

```text
observe → check/plan → repair/escalate → verify
```
