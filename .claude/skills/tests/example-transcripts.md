# Claude Skill Example Transcripts

## Purpose

This file provides concise example task transcripts showing how the Claude skill layer should behave.

These examples are not architecture facts. They are behavioral fixtures for the skill operating model.

## Transcript 1: Prepare Before Repair

### User

```text
Run the documentation loop and tell me what needs to happen next.
```

### Expected Skill

```text
doc-loop-prepare
```

### Expected Behavior

1. Read `agent/SKILL.md`.
2. Read `agent/GOAL.md`.
3. Run `python3 agent_harness.py --prepare`.
4. Read `agent/STATE.md`.
5. Report loop status, failing files, responsible specialist, next safe action, and blockers.
6. Do not edit files.

### Expected Output Shape

```markdown
## Loop Status

## Failing Files

## Responsible Specialist

## Recommended Next Action

## Blockers or Human Input Needed
```

## Transcript 2: Plan Repairs Before Mutation

### User

```text
Fix whatever the architecture linter is complaining about.
```

### Expected Skill

```text
run-doc-checker
```

### Expected Behavior

1. Treat the request as repair planning first, not mutation.
2. Run or read the current harness/verifier state.
3. Classify failures by file, failure type, owner, policy basis, and source-fact requirement.
4. Recommend `fix-doc-linter-failures` only for safe repairs.
5. Escalate missing facts rather than inventing content.

### Expected Output Shape

```markdown
## Checker Mode
Failure planning

## Loop Status

## Repair Plan

## Blocked Items

## Recommended Next Skill
```

## Transcript 3: Execute Approved Safe Repairs

### User

```text
Apply the safe linter fixes from the repair plan.
```

### Expected Skill

```text
fix-doc-linter-failures
```

### Preconditions

- A repair plan already exists.
- Planned repairs are classified as `SAFE_TO_REPAIR`.
- Target files are inside the write allowlist and outside the blocklist.

### Expected Behavior

1. Read `agent/SKILL.md`, `agent/GOAL.md`, and current state.
2. Apply only safe repairs from the repair plan.
3. Do not invent missing facts.
4. Run `python3 agent_harness.py --prepare` after repair.
5. Report repairs applied and verification result.

### Expected Output Shape

```markdown
## Repairs Applied

## Verification Result

## Remaining Failures

## Escalations or Human Input Needed
```

## Transcript 4: Missing Facts Become Gaps

### User

```text
Fill in all the unknown architecture details so the docs pass.
```

### Expected Skill

```text
escalate-doc-gap
```

### Expected Behavior

1. Refuse to invent architecture facts.
2. Identify the missing fact category.
3. Record the missing item as an open question, assumption, risk, or inline `ARCH-GAP`.
4. Assign a defensible owner.
5. Run verification if files were updated.

### Expected Output Shape

```markdown
## Gap Escalated

## Gap Type

## Owner

## Files Updated

## Verification Result

## Human Answer Needed
```

## Transcript 5: ADR Creation

### User

```text
Create an ADR for choosing Postgres as the primary database.
```

### Expected Skill

```text
create-adr
```

### Expected Behavior

1. Read `scaffold_adr.py` and policy.
2. Run `python3 scaffold_adr.py "choosing-postgres-as-the-primary-database"` or an equivalent title consistent with the scaffold contract.
3. Do not manually create the ADR file.
4. Populate only source-backed fields.
5. Leave unknowns as `PENDING_DISCOVERY` or escalate if source facts are missing.

### Expected Output Shape

```markdown
## ADR Created

## Command Used

## Content Populated

## Verification Result

## Remaining Gaps or Human Input Needed
```

## Transcript 6: System Scaffold Creation

### User

```text
Scaffold a Payments bounded context.
```

### Expected Skill

```text
create-system-scaffold
```

### Expected Behavior

1. Read `scaffold_system.py` and policy.
2. Confirm `architecture/systems/payments/` does not already exist.
3. Run `python3 scaffold_system.py payments --title "Payments"`.
4. Do not manually create system folders.
5. Do not link or populate the system unless the boundary is source-confirmed or explicitly requested.
6. Run verification.

### Expected Output Shape

```markdown
## System Scaffold Created

## Command Used

## Content Populated

## Links Added

## Verification Result

## Remaining Gaps or Human Input Needed
```

## Transcript 7: Conceptual Question Should Not Trigger Mutation

### User

```text
What is C4 architecture?
```

### Expected Skill

```text
none
```

### Expected Behavior

Answer conceptually. Do not read or mutate repository files unless the user asks to apply the concept to the repository.

## Transcript 8: Ambiguous System Request

### User

```text
Add a system using whatever name makes sense.
```

### Expected Skill

```text
none yet
```

### Expected Behavior

Ask for the system name or boundary. Do not scaffold using an inferred domain name.

### Expected Response

```text
I need the system or bounded-context name before scaffolding. Provide the intended name and whether this is scaffold-only or should be populated from source notes.
```
