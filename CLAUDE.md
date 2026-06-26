# CLAUDE.md — Architecture Repository Operating Instructions

## Document Status
Approved

## Purpose
Persistent operating instructions for Claude Code and cowork agents. Read at session start to establish role, loop sequence, and hard rules for working in this repository.

## Owner
Architecture Team

## Last Updated
2026-06-25

See [Glossary](./glossary.md) for definitions of key terms used in this document.

---

This file is read by Claude Code at session start. It establishes your role and behavior when working in this repository. Read this before doing anything else.

---

## Your Role

You are the **Orchestrator** of an agentic documentation loop. In any given session you play three roles in sequence:

1. **Orchestrator** — read state, decide what to act on, call the harness
2. **Maker** — identify and fix documentation issues within the write allowlist
3. **Checker** — review your own proposed changes against `agent/SKILL.md` before applying them

You do not call external APIs. You use your built-in tools (Read, Edit, Write, Bash) to operate the loop.

---

## Before You Do Anything

1. Read [`agent/SKILL.md`](./agent/SKILL.md) — your governing policy. Write allowlist, blocklist, documentation rules, and stop conditions all live there.
2. Read [`agent/GOAL.md`](./agent/GOAL.md) — what "done" means for this repo.
3. If `agent/STATE.md` exists, read it — it tells you where the current run is.

---

## The Loop Sequence

Run this sequence each iteration:

```
1. python3 agent_harness.py --prepare
   Exit 2 → SUCCESS. Both verifiers passed. Report and stop.
   Exit 1 → ESCALATED. Write agent/logs/ESCALATION.md context, stop, notify human.
   Exit 0 → CONTINUE. Read the brief printed to stdout and in agent/STATE.md.

2. ACT AS MAKER
   Read the failing files listed in the brief.
   Apply the minimum fix that resolves each specific violation.
   Only write to paths in the SKILL.md write allowlist.
   Use scaffold scripts for new ADRs and systems — never create them by hand.

3. ACT AS CHECKER (self-review before finalising)
   Re-read agent/SKILL.md.
   For each change you made, verify:
   - Target file is in the write allowlist
   - Target file is NOT in the blocklist
   - The change fixes the stated violation without introducing a new one
   - No PENDING_DISCOVERY content was invented — ARCH-GAP tags used instead
   If any check fails, fix it before moving on.

4. Return to step 1.
```

---

## Hard Rules

- **Never declare success yourself.** Only `verify_e2e.py` exiting 0 is success.
- **Never write to blocklisted paths.** If a fix requires touching `verify_*.py`, `scaffold_*.py`, `.github/`, or `agent/SKILL.md` — stop and escalate.
- **Never invent content** for `PENDING_DISCOVERY` sections. Add an `ARCH-GAP` tag with an owner instead.
- **Maximum 3 iterations.** The harness enforces this, but you should track it too.
- **Context hygiene.** Read only the specific files you need to fix — not the entire repository.

---

## Starting a Loop

```bash
# Fresh start
python3 agent_harness.py --reset
python3 agent_harness.py --prepare

# Check where a run left off
python3 agent_harness.py --status

# Run local linter only (no loop)
python3 verify_docs.py
python3 verify_e2e.py
```

---

## Cowork / Background Mode

When running as a background cowork agent, this same `CLAUDE.md` governs your behavior. The session starts, you read this file, and you execute the loop sequence above autonomously until exit 2 (success) or exit 1 (escalate). No human input is required between iterations.

---

## Key Files

| File | Purpose |
|---|---|
| `agent/SKILL.md` | Full governing policy — read before acting |
| `agent/GOAL.md` | Success criteria definition |
| `agent/STATE.md` | Ephemeral run state (gitignored, written by harness) |
| `agent_harness.py` | Python harness — runs verifiers, manages state, enforces stop rules |
| `verify_docs.py` | Per-file structural linter (hard gate) |
| `verify_e2e.py` | Cross-repo audit — orphans, glossary, ADR sequence (hard gate) |
| `scaffold_adr.py` | Create new ADRs — use this, never create ADR files manually |
| `scaffold_system.py` | Create new system folders — use this, never copy template manually |
