# ADR-0003: Agentic Team Collaboration

## Document Status
Approved

## Purpose
Record the architectural decision regarding the multi-agent team collaboration structure for the architecture-as-code repository.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../../glossary.md) for definitions of key terms.

---

## Status

Approved (per implementation plan approval on 2026-07-02)

## Context

In [ADR-0002: Agentic Loop Architecture](./0002-agentic-loop-architecture.md), we established a Level 4 Loop Engineering architecture using a single-agent Maker-Checker topology. While this model is highly effective for basic structural fixes, it has several scaling limitations:
1. **Domain Overlap:** A single generic Maker must handle business context, technical software standards, and deep security threat modeling with equal efficacy. 
2. **Role Dilution:** It is difficult to keep a single system prompt calibrated for distinct, sometimes competing architectural goals (e.g., rapid feature mapping vs. strict security verification).
3. **Rigidity:** The harness cannot dynamically adjust its focus area or compose targeted task groups based on the nature of the validation failures.

To scale the design, creation, and documentation of architectures for complex enterprise systems, we need a multi-agent team structure where specialized agents collaborate under a supervisor.

## Decision

We will transition the loop implementation from a single-Maker model to a multi-agent team collaboration model. The loop will consist of the following roles:

### 1. The Supervisor Agent
Acts as the team director and router. 
- **Responsibility:** Receives the verifier failure log from the Orchestrator, determines which specialized roles are required to resolve the failures, dynamically delegates files/tasks to them, and coordinates their proposed changes into a single consolidated diff.
- **System Prompt:** `agent/prompts/supervisor_prompt.md`

### 2. Specialized Maker Agents (The Team)
- **Solutions Architect:**
  - *Focus:* Business objectives, actors & roles, external system context, and high-level system boundary mapping.
  - *Write Allowlist:* `architecture/context/`, `decisions/`
  - *System Prompt:* `agent/prompts/solutions_architect_prompt.md`
- **Software Architect:**
  - *Focus:* Logical/deployment views, codebase technical standards (API design, databases, logging), and quality attribute targets.
  - *Write Allowlist:* `architecture/views/`, `standards/`
  - *System Prompt:* `agent/prompts/software_architect_prompt.md`
- **Security Reviewer:**
  - *Focus:* Risk modeling, assumptions tracking, security attributes, and compliance checks.
  - *Write Allowlist:* `governance/risks.md`, `governance/assumptions.md`
  - *System Prompt:* `agent/prompts/security_reviewer_prompt.md`

### 3. The Checker Agent
Remains the deterministic/compliance reviewer that audits the Supervisor's final merged diff against `SKILL.md` rules before passing it to disk.

### 4. Harness Updates
`agent_harness.py` will be modified to invoke the Supervisor agent with the failure context. The Supervisor will manage the downstream execution of the specialized sub-agents.

## Consequences

### Positive
- **Specialization & Depth:** Each architect agent is trained specifically on its domain, yielding much higher-fidelity architectural documents.
- **Faceted Governance:** Scopes are isolated, minimizing the risk of an agent making changes to files they do not own.
- **Dynamic Assembly:** A Supervisor allows the system to spin up only the necessary specialists to solve a given set of linter/E2E failures.

### Negative / Trade-offs
- **Token Overhead:** Spawning a Supervisor and calling specialists in parallel or sequence increases the token cost per loop run. 
- **Latency:** The round-trips required for Supervisor delegation add latency.

### Neutral
- **Stable Checker:** The Checker agent's role does not change; it still verifies compliance against the core constraints.
- **Learning Backlog:** We will establish a learning backlog file (`standards/learning-backlog.md`) to index external reference books and track specific architecture lessons that need to be trained into the team.

---

## Related Decisions

- [ADR-0002: Agentic Loop Architecture](./0002-agentic-loop-architecture.md) — Establishes the core loop which this decision extends.

## References

- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani — *Software Architecture: The Hard Parts* (O'Reilly, 2021)
- Simon Brown — *The C4 Model* (C4Model.com)
