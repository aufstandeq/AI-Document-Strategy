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
audit_ignore.py
.doc-audit-ignore
verify_docs.py
verify_e2e.py
verify_coverage.py
verify_claude_skills.py
verify_skill_trigger_fixtures.py
verify_repair_plan_fixtures.py
verify_skill_verifier_fixtures.py
verify_source_fact_citation_fixtures.py
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
