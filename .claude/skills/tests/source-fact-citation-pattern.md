# Source Fact Citation Pattern

## Purpose

This file defines the required pattern for citing source facts when Claude skills propose or make architecture-document changes.

The goal is to make every meaningful architecture change traceable to explicit source material, while clearly separating direct facts, reasonable inferences, and unresolved gaps.

## Applies To

This pattern applies to these skills:

| Skill | Use of this pattern |
|---|---|
| `run-doc-checker` | Cite the source facts behind each repair recommendation. |
| `create-system-context` | Cite source facts before updating context documents. |
| `escalate-doc-gap` | Cite missing or ambiguous source material when recording a gap. |
| `fix-doc-linter-failures` | Cite the repair plan or verifier output when applying bounded repairs. |

## Source Classification

| Classification | Meaning | Allowed action |
|---|---|---|
| `SOURCE_FACT` | A directly observed statement from a source file, user-provided note, verifier output, or repository document. | May be used as document content when relevant. |
| `INFERENCE` | A conclusion derived from one or more source facts. | May be proposed, but must be labeled as inference. |
| `GAP` | A missing, contradictory, or ambiguous fact. | Must be escalated; do not invent. |
| `POLICY` | A repository rule from `agent/SKILL.md`, skill files, verifier behavior, or scaffold contract. | Must constrain the action. |
| `VERIFIER_OUTPUT` | A deterministic finding from a repository verifier. | May drive repair planning. |

## Required Evidence Block

Any checker plan or skill output that changes architecture meaning must include an evidence block:

```markdown
## Source Fact Inventory

| ID | Classification | Source | Fact / Finding | Used For |
|---|---|---|---|---|
| SF-001 | SOURCE_FACT | `path/to/source.md` | Short factual statement. | Target document section or repair. |
| SF-002 | VERIFIER_OUTPUT | `verify_docs.py` | Reported missing `## Owner`. | Metadata repair. |
| SF-003 | GAP | `path/to/source.md` | Owner not identified. | Escalate open question. |
```

## Source Reference Format

Use repository-relative paths wherever possible:

```text
architecture/context/system-context.md
architecture/views/logical-view.md
governance/open-questions.md
agent/SKILL.md
```

When the source is verifier output, use the verifier name plus the exact finding:

```text
verify_docs.py: architecture/context/system-context.md missing ## Last Updated
```

When the source is a user instruction in the current session, cite it as:

```text
USER_REQUEST: "exact short quoted instruction"
```

Do not cite general model knowledge as a source fact.

## Inference Rule

Inferences must be explicit:

```markdown
## Inferences

| ID | Based On | Inference | Confidence | Needs Review? |
|---|---|---|---|---|
| INF-001 | SF-001, SF-002 | Pricing appears to be part of Orders. | Medium | Yes |
```

If an inference changes ownership, boundaries, integrations, data flow, security posture, or business meaning, it requires human review or an ADR.

## Gap Rule

When the source fact is missing, contradictory, or ambiguous, use a gap instead of filling content.

```markdown
## Gaps / Escalations

| ID | Missing Fact | Source Context | Required Owner | Recommended Recording Location |
|---|---|---|---|---|
| GAP-001 | Payment Gateway owner | External system listed without owner. | Architecture Team | `governance/open-questions.md` |
```

Use `escalate-doc-gap` when the gap requires human input or additional source material.

## Repair Plan Output Requirement

`run-doc-checker` repair plans should use this structure:

```markdown
## Checker Mode

## Loop Status

## Source Fact Inventory

## Failure Classification

## Repair Plan

## Inferences

## Gaps / Escalations

## Blocked Items

## Recommended Next Skill

## Verification Needed
```

## Mutation Rule

A skill may mutate architecture documents only when one of these is true:

1. The change is directly supported by `SOURCE_FACT` or `VERIFIER_OUTPUT`.
2. The change is a safe structural repair and does not alter architecture meaning.
3. The user explicitly approved the inferred change.

Otherwise, the skill must escalate.

## Examples

### Safe Metadata Repair

```markdown
| ID | Classification | Source | Fact / Finding | Used For |
|---|---|---|---|---|
| SF-001 | VERIFIER_OUTPUT | `verify_docs.py` | `system-context.md` missing `## Last Updated`. | Add required metadata header. |
```

Classification:

```text
SAFE_TO_REPAIR
```

### Missing Ownership

```markdown
| ID | Classification | Source | Fact / Finding | Used For |
|---|---|---|---|---|
| SF-001 | SOURCE_FACT | `architecture/context/external-systems.md` | Payment Gateway is listed as an external system. | External system inventory. |
| SF-002 | GAP | `architecture/context/external-systems.md` | Payment Gateway owner is not identified. | Open question. |
```

Classification:

```text
REQUIRES_SOURCE_FACTS
```

### Boundary Change

```markdown
| ID | Classification | Source | Fact / Finding | Used For |
|---|---|---|---|---|
| SF-001 | SOURCE_FACT | `architecture/systems/orders/index.md` | Orders owns checkout flow. | Context analysis. |
| INF-001 | INFERENCE | SF-001 | Pricing may belong in Orders. | Proposed boundary change. |
```

Classification:

```text
HUMAN_REVIEW_REQUIRED
```

## Prohibited Patterns

Do not write:

```text
Based on best practices...
Generally, systems like this...
It is likely that...
```

unless the statement is explicitly labeled as an inference and does not become source-of-truth content without approval.
