---
name: create-system-context
description: Creates or updates C4-style system context documentation from explicit source material in the architecture repository. Use when the user asks to recreate system context, define system boundaries, document actors and roles, identify external systems, create in-scope and out-of-scope capabilities, or update architecture context files without inventing undocumented facts.
compatibility: Claude Code project skill for the AI-Document-Strategy repository. Requires local shell access and Python 3.
metadata:
  author: Architecture Team
  version: 0.1.0
  category: architecture-context
---

# create-system-context

## Purpose

Create or update the coordinated system context documentation set using only explicit source material.

This skill handles the C4 Level 1 context layer and adjacent scope documents. It must preserve the repository's source-of-truth discipline and must not infer system facts from general knowledge.

## Context Document Set

Treat these files as a linked update set:

```text
architecture/context/business-context.md
architecture/context/system-context.md
architecture/context/actors-and-roles.md
architecture/context/external-systems.md
```

When updating one file, check whether the same fact must be reflected in the others.

## Critical Rules

- Follow `agent/SKILL.md` over this skill if there is any conflict.
- Edit only files allowed by the current `agent/SKILL.md` write allowlist.
- Do not edit verifier scripts, scaffold scripts, workflow files, prompts, policy files, README files, onboarding files, or archive files.
- Do not read `archive/` unless the user explicitly asks for deprecated or legacy material.
- Do not invent actors, integrations, system responsibilities, technologies, topology, security scopes, or business objectives.
- Every new or updated active document must link to `glossary.md` using a relative link.
- Use `PENDING_DISCOVERY` blocks and `ARCH-GAP` tags when facts are missing.
- If a missing fact affects system boundary, actor authority, integration ownership, or in-scope capability, stop and ask for source material or record an `ARCH-GAP`.
- After edits, run `python3 agent_harness.py --prepare` and report the result.

## Required Inputs

Before updating context files, read:

```text
agent/SKILL.md
agent/GOAL.md
glossary.md
architecture/index.md
architecture/context/business-context.md
architecture/context/system-context.md
architecture/context/actors-and-roles.md
architecture/context/external-systems.md
```

Also read any user-specified active source documents, such as:

```text
architecture/views/logical-view.md
architecture/views/deployment-view.md
standards/architectural-decision-matrix.md
standards/architecture-guidelines.md
decisions/*.md
governance/assumptions.md
governance/open-questions.md
governance/risks.md
```

## Source Eligibility

Allowed sources:

- User-provided notes in the current task.
- Active repository files under `architecture/`, `standards/`, `decisions/`, `governance/`, and `glossary.md`.
- Explicit external source material provided by the user.

Disallowed sources:

- General model knowledge.
- Guesses based on common application patterns.
- Deprecated or archived documents unless explicitly requested.
- Existing code assumptions unless the user explicitly asks to use implementation discovery.

## Extraction Model

Extract only facts that can be traced to source material.

| Context element | Required source evidence |
|---|---|
| System purpose | Business objective, user statement, or existing context doc |
| System boundary | Explicit scope, view, ADR, or user-provided boundary statement |
| In-scope capability | Stated requirement, context doc, view, or ADR |
| Out-of-scope capability | Explicit exclusion, constraint, or negative scope statement |
| Actor | Existing actor doc, user-provided role, auth model, or workflow note |
| Permission or security scope | Existing actor doc, security standard, or explicit user-provided rule |
| External system | Existing integration doc, view, ADR, or user-provided integration note |
| Integration direction | Explicit upstream, downstream, inbound, outbound, webhook, batch, or API statement |
| Ownership | Existing ownership statement or explicit user-provided owner |

If evidence is weak, do not write it as fact. Use an `ARCH-GAP` or ask for clarification.

## Update Workflow

### Step 1: Build a source fact inventory

Create a working table before editing:

```markdown
## Source Fact Inventory

| Fact | Source file or user note | Target document |
|---|---|---|
```

Do not proceed if the main system boundary or system purpose is missing.

### Step 2: Update Business Context

Use `business-context.md` for:

- Business objectives.
- Success metrics.
- Stakeholders.
- Constraints.
- Assumptions.
- Risks.
- Out-of-scope business capabilities.

Do not duplicate technical implementation details here unless they are business constraints.

### Step 3: Update System Context

Use `system-context.md` for:

- System purpose.
- System responsibilities.
- In-scope technical capabilities.
- Explicit non-responsibilities.
- External dependencies.
- High-level C4-style context diagram.

The context diagram may use Mermaid when the existing file uses Mermaid.

### Step 4: Update Actors and Roles

Use `actors-and-roles.md` for:

- Human actors.
- System actors only if they act against the system boundary.
- Responsibilities.
- Role definitions.
- Permissions.
- Security scopes.

Do not create permissions unless the source material defines them.

### Step 5: Update External Systems

Use `external-systems.md` for:

- Upstream systems.
- Downstream systems.
- Third-party services.
- Integration responsibilities.
- Ownership.
- System integration summary table.

Do not list internal modules as external systems.

### Step 6: Cross-check consistency

Before finalizing, check:

- Every actor in `system-context.md` exists in `actors-and-roles.md` or is explicitly external.
- Every external dependency in `system-context.md` exists in `external-systems.md`.
- In-scope and out-of-scope statements do not contradict business context.
- External systems are not confused with internal modules.
- Diagram labels match document terminology and glossary terms.
- Any unresolved fact is marked with `PENDING_DISCOVERY` or `ARCH-GAP`.

### Step 7: Verify

Run:

```bash
python3 agent_harness.py --prepare
```

Interpret the result:

| Exit code | Meaning | Action |
|---|---|---|
| 2 | Success | Report success |
| 1 | Escalated | Read `agent/logs/ESCALATION.md` and report the escalation reason |
| 0 | Continue | Report remaining verifier failures and whether another safe iteration exists |

## Diagram Rules

When creating or updating a Mermaid context diagram:

- Keep it high-level.
- Show the system boundary explicitly.
- Show external actors and external systems.
- Show directional relationships.
- Do not introduce internal implementation modules unless they are already documented as part of the context boundary.
- Do not show deployment details in the system context diagram.
- Do not show database schemas unless the current context document already treats them as boundary-relevant.

## Output Format

Return:

```markdown
## Source Facts Used

## Context Files Updated

## Boundary Decisions Preserved

## Verification Result

## Remaining Gaps or Human Input Needed
```
