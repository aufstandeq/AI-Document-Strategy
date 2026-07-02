# SKILL.md — Agent Policy Document

## Document Status
Approved

## Purpose
Define the governing rules for all agents operating within the agentic documentation loop. This file is read-only to agents and is loaded once at loop start. It replaces guesswork with explicit constraints.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## 1. Role Definitions

### Orchestrator
The Python process (`agent_harness.py`) that manages deterministic loop state. It reads and writes `agent/STATE.md`, invokes verifier scripts, compresses verifier output, enforces stop rules, and emits the Supervisor brief. It does not call LLM APIs and does not write documentation directly.

### Supervisor (Director Agent)
Coordinates the specialized Maker sub-agents. Analyzes verifier failures in STATE.md, delegates files and tasks to the appropriate specialized architects, checks that they stay within their write allowlists, and consolidates their proposals. System prompt: [supervisor_prompt.md](./prompts/supervisor_prompt.md).

### Specialized Makers (Implementer Sub-Agents)
- **Solutions Architect:** Focuses on business context, actors, integrations, and decisions. Write allowlist: `architecture/context/`, `decisions/`. System prompt: [solutions_architect_prompt.md](./prompts/solutions_architect_prompt.md).
- **Software Architect:** Focuses on system views, quality attributes, and codebase technical standards. Write allowlist: `architecture/views/`, `standards/`. System prompt: [software_architect_prompt.md](./prompts/software_architect_prompt.md).
- **Security Reviewer:** Focuses on risk modeling, assumptions, and security standards. Write allowlist: `governance/risks.md`, `governance/assumptions.md`. System prompt: [security_reviewer_prompt.md](./prompts/security_reviewer_prompt.md).

### Checker (Verifier Sub-Agent)
Reviews the Supervisor's final merged changes against this SKILL.md and the repository conventions. Does not modify files — outputs a structured review with PASS or FAIL and specific issues. Runs before the deterministic verifier scripts. System prompt: [checker_system_prompt.md](./prompts/checker_system_prompt.md).

---

## 2. Write Allowlist

Sub-agents may only write to the following paths. Any write attempt outside this list must be rejected by the orchestrator before execution.

```
architecture/context/
architecture/views/
architecture/systems/          (new systems via scaffold_system.py only)
decisions/                     (new ADRs via scaffold_adr.py only)
governance/risks.md
governance/assumptions.md
governance/open-questions.md
governance/migration_log.md
glossary.md
agent/STATE.md                 (orchestrator only)
agent/logs/                    (orchestrator only)
```

---

## 3. Write Blocklist

Writes to any of the following paths fail the loop immediately and trigger escalation. These files define the harness — an agent modifying them is reward-hacking.

```
agent_harness.py
verify_docs.py
verify_e2e.py
verify_coverage.py
scaffold_adr.py
scaffold_system.py
.github/
agent/SKILL.md
agent/GOAL.md
agent/prompts/
README.md
how-to-start.md
onboarding-dev.md
standards/
```

---

## 4. Documentation Rules

Every markdown file the agentic team creates or modifies must satisfy all of the following:

### 4.1 Required Header Block
Every file must open with this exact structure:

```markdown
# [Document Title]

## Document Status
Draft

## Purpose
[One sentence describing what this document covers]

## Owner
[Team or person name]

## Last Updated
YYYY-MM-DD
```

### 4.2 Document Status Values
`Document Status` must be exactly one of:
- `Draft`
- `In Review`
- `Approved`
- `Deprecated`

Any other value fails `verify_docs.py`.

### 4.3 Incomplete Sections
Never use bare `TBD`. All incomplete sections must use:

```markdown
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD
```

### 4.4 Architectural Gap Tags
When a section is known to be incomplete and the answer is not yet available:

```markdown
<!-- ARCH-GAP: [Short description of what is unknown]. [Owner: TeamName]. -->
```

The `Owner:` field is required. Gaps without an owner fail `verify_e2e.py`.

### 4.5 Link Rules
- All cross-document links must use relative paths (e.g., `../glossary.md`)
- Absolute paths (`/architecture/...`) fail the linter
- Every active document must contain at least one link to `glossary.md`

### 4.6 Scaffold Scripts
- New ADRs: call `python3 scaffold_adr.py "<title>"` — never create ADR files by hand
- New systems: call `python3 scaffold_system.py <name>` — never copy system-template manually

---

## 5. Mandatory Tool Sequence

The loop must execute steps in this exact order each iteration:

```
1. Run: python3 agent_harness.py --prepare
2. Read agent/STATE.md → load iteration context and compressed verifier failure summary
3. Invoke Supervisor agent with: SKILL.md + STATE.md + verifier failure summary
4. Supervisor delegates to specialized SA, SWA, and SR sub-agents and consolidates proposed changes
5. Invoke Checker sub-agent with: SKILL.md + Supervisor's consolidated diff only
6. If Checker returns FAIL → do not apply changes; run python3 agent_harness.py --prepare again only after revising the proposal
7. Apply Supervisor/Specialist changes to disk (within allowlist only)
8. Run: python3 agent_harness.py --prepare
9. If harness exits 2 → success; stop
10. If harness exits 1 → escalated; stop and read agent/logs/ESCALATION.md
11. If harness exits 0 → failures remain; continue only if stop rules allow another iteration
```

---

## 6. Context Hygiene

To control token costs (loops consume ~4x tokens vs. single-turn chat):

- Pass verifier output to agents as **compressed signal only**: failing file paths + specific error messages. Do not pass full file contents unless the agent explicitly needs to read a specific file.
- Load SKILL.md as a **stable prefix** — it never changes mid-run, enabling prompt caching.
- STATE.md contains the dynamic context; SKILL.md contains the static policy.
- Supervisor and specialists receive only their target file lists or failure context, not the entire repository.
- Checker receives only the Supervisor's consolidated diff, not the full file.

---

## 7. Stop Rules

The orchestrator enforces all three stop conditions. They are not optional.

| Condition | Threshold | Action |
|---|---|---|
| Success | `agent_harness.py --prepare` exits 2 | Write STATE.md status=success, stop |
| Max iterations | 3 iterations | Write ESCALATION.md, stop |
| No progress | Same `failing_files_hash` as prior iteration | Write ESCALATION.md, stop |
| Blocklist write attempt | Any | Write ESCALATION.md, stop immediately |

### Escalation Content (agent/logs/ESCALATION.md)
Must include:
- Timestamp
- Iteration count reached
- Failing files list
- Last verifier stderr output (compressed)
- Stop reason (max_iterations | no_progress | blocklist_violation)

---

## 8. The Stop Authority Rule

> **The agent is never allowed to declare success based on its own opinion.**

Success is defined exclusively by `agent_harness.py --prepare` exiting 2 after both deterministic verifier scripts pass. The Checker sub-agent's PASS output advances to the verifier step — it does not stop the loop. Only the deterministic Python harness holds stop authority.
