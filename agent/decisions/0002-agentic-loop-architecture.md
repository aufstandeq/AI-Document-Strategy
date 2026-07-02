# ADR-0002: Agentic Loop Architecture

## Document Status
Approved

## Purpose
Record the architectural decision regarding agentic loop architecture.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../../glossary.md) for definitions of key terms.

---

## Status

Approved

## Context

The repository already operates as a Level 3 Harness: Python verification scripts (`verify_docs.py`, `verify_e2e.py`, `verify_coverage.py`) and scaffolding tools (`scaffold_adr.py`, `scaffold_system.py`) provide deterministic, external validation with CI enforcement. Documentation is currently maintained manually — a developer writes or updates files, the linter catches structural errors, and CI gates merges.

As projects scale, the gap between the current codebase state and the documentation state widens faster than humans can maintain it. The manual loop (human writes → linter checks → human fixes → CI passes) is the bottleneck. The harness is in place; the autonomous control cycle is not.

Loop Engineering (defined by Osmani and Steinberger, June 2026) addresses this by replacing the human prompter with a governed system that manages its own iteration, planning, and verification — while keeping deterministic Python scripts as the sole stop authority.

## Decision

We will add a Loop Engineering layer on top of the existing harness. Claude Code (or a cowork background agent) acts as the Orchestrator, Maker, and Checker — eliminating the need for external API calls or a separate API key. The layer introduces:

- **`CLAUDE.md`** — persistent meta-prompt at repo root; Claude Code reads this at session start to establish its role, loop sequence, and hard rules
- **`agent/SKILL.md`** — consolidated agent policy (write allowlist, blocklist, documentation rules, stop rules)
- **`agent/GOAL.md`** — machine-readable success criteria per run
- **`agent/STATE.md`** — ephemeral per-run state store (gitignored, written by harness)
- **`agent_harness.py`** — pure Python harness with no LLM API calls; runs verifiers, manages STATE.md, enforces stop rules, and returns a structured brief for Claude to act on
- **`agent/prompts/`** — versioned Maker and Checker system prompt references (used in cowork background mode)

The loop follows the Incident Response topology (Supervisor + Specialist). In **in-session mode**, Claude Code plays all three roles using its built-in file and shell tools. In **cowork/background mode**, a scheduled agent reads the same `CLAUDE.md` and runs the same loop autonomously.

The existing harness (`verify_*.py`, `scaffold_*.py`, `.github/`) is not modified.

## Consequences

### Positive
- Documentation gaps that currently require human triage can be identified and fixed autonomously within the constraints of the write allowlist
- The verifier scripts already in place serve as the natural stop authority — no new verification logic needed
- Sub-agent prompts are versioned Markdown files — reviewable, diffable, and improvable via normal PR workflow
- The `--dry-run` flag allows safe testing of loop behavior before any files are modified

### Negative / Trade-offs
- Loops consume approximately 4x more tokens than a single-turn interaction; multi-agent runs approach 15x — token costs must be monitored
- The Maker can only fix structural violations within the write allowlist; content requiring human domain knowledge is out of scope and must be escalated
- In-session mode requires an active Claude Code session; cowork background mode requires setup of the cowork agent schedule

### Neutral
- The `agent/` directory is a peer to `architecture/`, `decisions/`, and `governance/` — it is part of the repository but subject to its own gitignore rules for ephemeral state
- The AI Maturity Staircase position advances from Level 3 (Harness Engineering) to Level 4 (Loop Engineering)

---

## Related Decisions

- [ADR-0001: Record Architecture Decisions](../../decisions/0001-record-architecture-decisions.md) — establishes the ADR pattern this record follows

## References

- Osmani, A. and Steinberger, P. — Loop Engineering (June 2026)
- Hashimoto, M. — Harness Engineering (February 2026)
- ReAct pattern — Reasoning and Acting in language models
- [CLAUDE.md](../../CLAUDE.md) — in-session and cowork agent operating instructions
- [agent/SKILL.md](../SKILL.md) — governing policy for the loop
- [agent/GOAL.md](../GOAL.md) — success criteria definition
