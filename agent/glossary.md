# Agent Tooling Glossary

## Document Status
Draft

## Purpose
Define the vocabulary used to describe the AI-assisted documentation tooling, validation harness, skills, and operating model.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

This glossary is for the documentation operating system itself. Project, product, domain, architecture, design, and code vocabulary belongs in the root [Project Glossary](../glossary.md).

---

## Usage Rule

Use this glossary when documenting how AI, validators, skills, fixtures, and control policies operate. Do not place project-domain vocabulary here.

## Terms

| Term | Definition | Notes |
|---|---|---|
| Active Documentation | Documentation inside the active audit boundary that is treated as current repository knowledge. | Excludes archived, ignored, generated, or explicitly reference-only material. |
| Agentic Documentation Loop | The controlled process in which AI assistance observes repository state, plans bounded changes, escalates missing facts, repairs safe issues, and verifies results. | Current implementation uses Claude skills plus deterministic validators. |
| ARCH-GAP | A machine-auditable inline marker for a known unresolved architecture gap. | Must include an owner using `Owner:` so the gap can be assigned. |
| Audit Boundary | The set of files included in repository validation and cross-document checks. | Controlled by active paths and `.doc-audit-ignore`. |
| Bounded Repair | A safe, limited change that fixes structural or explicitly supported issues without inventing missing facts. | Examples: fixing links, headers, status values, glossary references, or scaffold shape. |
| Checker | A review role that evaluates proposed changes against policy and validation expectations without modifying files. | In the current repo, deterministic verifier scripts provide the strongest checker authority. |
| CI Validation | Validation performed by GitHub Actions after push or pull request events. | Strategic target is to use `python3 run_validation.py`. |
| Control File | A file that defines policy, validation behavior, scaffolding, CI, or agent operation. | Control files are protected from normal agent mutation. |
| Deterministic Verifier | A script that produces repeatable pass/fail results from repository contents. | Examples include `verify_docs.py`, `verify_e2e.py`, and fixture validators. |
| Drift Detection | A future capability that compares documentation claims against source-of-truth systems such as code, infrastructure, APIs, or runtime state. | Current validation mostly verifies structure, not semantic truth. |
| Example Content | Worked sample content retained to demonstrate documentation shape or patterns. | Must not be treated as approved source-truth architecture until replaced and re-approved. |
| Fixture | A controlled test case used to verify expected behavior of skills, validators, or repair plans. | May be human-readable, machine-readable, or executable. |
| Hard Gate | A validation gate that must pass for the repository to be considered valid. | Failure returns a non-zero result through `run_validation.py`. |
| Informational Gate | A validation gate that reports findings but does not fail the overall validation run. | `coverage-report` is currently informational. |
| Local Validation | Validation run by a developer or agent in a local workspace. | Current preferred command is `python3 run_validation.py`. |
| No-Invention Discipline | The rule that AI must not fabricate actors, requirements, integrations, decisions, or source facts. | Missing information must become an owned gap, question, assumption, or escalation. |
| Operating Model | The defined division of labor, workflow, policy, and verification process used to create and maintain documentation. | Captured in `strategy.md` and agent documentation. |
| Orphan | A Markdown file inside the audit boundary with no inbound relative link from another active Markdown file. | Detected by `verify_e2e.py`. |
| PENDING_DISCOVERY | A standard placeholder marker for information that is intentionally unknown and must not be autofilled by AI. | Used with `<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->`. |
| Reference Design | Documentation retained to describe a possible or future implementation approach, not necessarily the current runtime. | `agent/prompts/` is currently reference/future design unless explicitly wired. |
| Reward-Hacking | A failure mode where an agent modifies validators, policies, or success definitions to make itself appear successful. | Prevented by protecting control files. |
| Scaffold | A script or template-generated structure that creates documents in a repeatable approved shape. | Examples include ADR and system scaffolds. |
| Semantic Drift | The condition where documentation remains structurally valid but no longer reflects the implemented or deployed system. | Not fully solved by current validators. |
| Source Fact | A fact grounded in human input, source documents, code, infrastructure, runtime data, or other authoritative evidence. | AI may organize source facts but must not invent them. |
| Source Truth | The authoritative body of facts a document is allowed to reflect. | Active architecture docs should distinguish source truth from example content. |
| Strategy-as-Deliverable | The reusable documentation strategy captured separately from the working repo instance. | Captured in `strategy.md`. |
| Validation Gate | A configured check executed by the shared validation runner. | Defined in `.validation-config.json`. |
| Validation Runner | The script that loads validation configuration and executes gates in order. | Current runner is `run_validation.py`. |
| Write Allowlist | The set of paths a role or agent may modify. | Defined in `agent/SKILL.md`. |
| Write Blocklist | The protected set of paths that normal agents must not modify. | Includes harness, policy, CI, verifier, and scaffold files. |
