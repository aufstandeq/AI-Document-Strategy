# AI & Human Architectural Documentation Strategy

## Document Status
Draft

## Purpose
Define the operating strategy for creating and maintaining architectural documentation as a shared responsibility between humans, AI agents, and deterministic verification tooling.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](./glossary.md) for definitions of key terms used in this document.

---

## 1. The Problem This Strategy Solves

Architecture documentation fails in two directions:

- **For humans**, documentation drifts. Design decisions fade from memory, wiki pages go stale, and code gradually violates boundaries nobody remembers defining. The cost appears months later as rework, outages, and onboarding friction.
- **For AI**, documentation gaps become hallucinations. Coding assistants that must guess system boundaries, actors, or constraints will confidently invent them — and inventions written into documentation are worse than gaps, because they look authoritative.

This strategy addresses both failure modes with one operating model: **documentation as code, verified by deterministic tooling, created by humans and AI in bounded collaboration, and maintained by an agentic loop that is structurally prevented from inventing facts.**

This repository is both the definition of the strategy and its reference implementation.

---

## 2. Division of Labor

The strategy assigns each responsibility to the party that can be trusted with it:

| Responsibility | Owner |
|---|---|
| Business facts, topology choices, and architectural decisions | Humans |
| Drafting content from explicit, human-provided source facts | AI agents, with human review |
| Structure, metadata, link integrity, and glossary anchoring | AI agents (bounded by policy) |
| Flagging missing knowledge (`ARCH-GAP`, `PENDING_DISCOVERY`) | AI agents |
| Resolving flagged gaps with real answers | Humans |
| Declaring work complete | Deterministic verifiers only |

Two rules make this division enforceable rather than aspirational:

1. **No invention.** An AI agent that lacks a fact must record the gap with an owner, never fill it in. The `PENDING_DISCOVERY` and `ARCH-GAP` conventions in the [README Operational Guide](./README.md) give agents a machine-auditable way to say "I don't know."
2. **No self-declared success.** Only the verifier scripts exiting 0 constitutes success, as defined in [agent/GOAL.md](./agent/GOAL.md). Agent opinion, checker approval, and even human impressions are not stop authorities.

---

## 3. Maturity Ladder

The strategy progresses through capability levels. Each level is a prerequisite for the next.

| Level | Name | Capability | Status |
|---|---|---|---|
| 0 | Ad-hoc | Scattered wikis and design docs; no single source of truth | Superseded |
| 1 | Structured templates | Consistent document structure, metadata headers, and placeholder conventions | Complete |
| 2 | Documentation as code | Version control, PR review, relative-link discipline, archive-over-delete | Complete |
| 3 | Deterministic harness | Structural linting and cross-repository audit as hard CI gates (`verify_docs.py`, `verify_e2e.py`) | Complete |
| 4 | Loop engineering | Autonomous, bounded maintenance loop with allowlists, stop rules, and escalation ([agent/README.md](./agent/README.md)) | Current |
| 5 | Semantic drift detection | Verification that documentation matches implementation reality, not just structural rules | Planned |

The distinction between Level 3 and Level 4: at Level 3, tooling *detects* problems and humans fix them; at Level 4, a governed agent team fixes structural problems autonomously and escalates everything else. Level 5 is the open frontier — today every verifier checks *form* (headers, links, sequences), and no check confirms that documented architecture still matches deployed systems.

---

## 4. Creating Documentation (Human-Led Path)

Creation is human-led because it is fact-production. The workflow is defined in [How to Start](./how-to-start.md):

1. **Decide topology first** using the [Architectural Decision Matrix](./standards/architectural-decision-matrix.md), and record the outcome as an ADR.
2. **Scaffold, never hand-create.** New ADRs come from `scaffold_adr.py`; new system folders come from `scaffold_system.py`. Scaffolds guarantee structural compliance from the first commit.
3. **Populate context and views** from real source material, leaving unknowns explicitly marked rather than guessed.
4. **Use AI as a drafting partner, not a fact source.** AI generates standards and view content *from* the human-selected topology and source facts — for example, "Given the Modular Monolith topology selected in ADR-0002, draft the schema isolation guidelines."

The worked example in this repository (the fictional Distributed Payment Reconciliation Subsystem in `architecture/context/`, `architecture/views/`, and `standards/`) demonstrates what completed output of this path looks like. Every file containing it carries a `WORKED_EXAMPLE` banner; it is illustrative content, never a source fact.

---

## 5. Maintaining Documentation (AI-Led Path)

Maintenance is AI-led because it is rule-application. The agentic loop, defined in [agent/README.md](./agent/README.md) and governed by [agent/SKILL.md](./agent/SKILL.md), runs:

```text
observe → plan → repair or escalate → verify
```

1. **Observe:** the harness (`agent_harness.py --prepare`) runs both verifiers and emits a bounded brief of failures.
2. **Plan:** a checker pass classifies each failure — safe to repair, requires source facts, blocked by policy, or needs human review.
3. **Repair or escalate:** safe structural repairs (metadata, links, glossary anchors, owned gap tags) are applied within the write allowlist; anything requiring facts becomes an owned gap or an escalation.
4. **Verify:** the verifiers re-run. Only their exit codes end the loop.

Guardrails that keep the loop trustworthy:

- **Write allowlist and blocklist** ([agent/SKILL.md](./agent/SKILL.md)): agents cannot touch the verifiers, scaffolds, CI, or their own policy — modifying the referee is treated as reward-hacking and fails the run.
- **Iteration cap and escalation:** the loop stops after bounded attempts and writes an escalation log for humans rather than thrashing.
- **The tooling is held to the same standard as the docs:** the Claude skill layer that operates the loop is itself fixture-tested (see the validation gates in [.claude/skills/PLAN.md](./.claude/skills/PLAN.md)).

---

## 6. Trust Boundaries

| Boundary | Rule |
|---|---|
| Source of truth | Active directories only (`architecture/`, `standards/`, `decisions/`, `governance/`, `glossary.md`); `archive/` is never read into agent context |
| Worked example content | Files carrying the `WORKED_EXAMPLE` AI hint are illustrative; agents must not cite them as source facts |
| Control files | Verifiers, scaffolds, CI workflows, agent policy, and onboarding docs change only through human-reviewed PRs |
| Unknown facts | Recorded as `PENDING_DISCOVERY` or owner-tagged `ARCH-GAP`, never auto-filled |
| Vocabulary | Terms are defined in [the glossary](./glossary.md) before broad use; every active document anchors to it |

---

## 7. Adopting This Strategy in a New Repository

1. Copy the repository structure, verifier scripts, scaffold scripts, and CI workflow.
2. Run the [Architectural Decision Matrix](./standards/architectural-decision-matrix.md) for the new system and record the topology ADR.
3. Replace all `WORKED_EXAMPLE` content with real system facts, following the [How to Start](./how-to-start.md) workflow.
4. Assign real owners to every document header and open gap.
5. Enable the CI gate so structural verification blocks merges from day one.
6. Once content stabilizes, enable the maintenance loop on a recurring cadence.

---

## 8. Roadmap

| Item | Level served | Description |
|---|---|---|
| Semantic drift detection | 5 | Verify documented views and standards against a target codebase or deployed environment; surface mismatches as owned gaps |
| Scheduled loop runs | 4 | Cron- or CI-triggered maintenance runs so upkeep does not depend on manual invocation (trigger modes are defined in [agent/GOAL.md](./agent/GOAL.md)) |
| Scoped runs | 4 | Harness support for verifying a subdirectory, enabling PR-scoped verification |
| Glossary depth | 2 | Grow the glossary into a genuine vocabulary authority to match the "Glossary First" principle |
