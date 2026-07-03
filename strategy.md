# AI-Assisted Documentation Strategy

## Document Status
Draft

## Purpose
Define the reusable strategy behind this repository: a simple, self-testing documentation operating system for creating and maintaining architecture documentation with human and AI collaboration.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See the [Agent Tooling Glossary](./agent/glossary.md) for AI documentation-system terms and the [Project Glossary](./glossary.md) for target-system vocabulary.

---

## 1. Final Goal

The final goal of this repository is to create enough architectural clarity that a human or AI can safely design, build, modify, and maintain the target system without breaking architectural intent.

The validation harness, documentation structure, AI skills, glossary rules, scaffolds, and governance workflow are guardrails. They exist to reduce drift, prevent mistakes, and preserve the clarity needed for correct development.

The process is not the product. The product is useful architecture knowledge that improves development decisions.

## 2. Strategy Statement

This repository is both a working implementation and a reference strategy for AI-assisted architecture documentation.

The strategy is not to let AI freely generate architecture content. The strategy is to give AI a constrained operating environment where:

- humans own source facts, decisions, priorities, and approval;
- AI assists with structure, repair, synthesis, and gap surfacing;
- deterministic verifiers define success;
- missing information is recorded as an owned gap instead of invented;
- local validation and CI validation converge on the same repeatable checks;
- architecture documents remain useful enough to guide development.

The intended end state is a repository that makes the architecture understandable, durable, and actionable for both human and AI development work.

## 3. Core Separation Rule

This repository has two documentation planes. They must remain clearly separated.

| Plane | Purpose | Primary Audience | Examples |
|---|---|---|---|
| Documentation Operating System | Files needed to build, govern, validate, and maintain the architecture-as-code structure. | Repository maintainers, AI assistants, documentation tooling authors. | `strategy.md`, `agent/`, `.claude/skills/`, validation scripts, scaffold scripts, `.validation-config.json`, `.doc-audit-ignore`. |
| Client Architecture Workspace | Files, templates, standards, and guidance the client uses to document the actual system being designed and built. | Client architects, developers, product owners, security reviewers, operations teams, AI assistants working on the project. | `architecture/`, `decisions/`, `standards/`, `governance/`, root `glossary.md`, onboarding guidance, templates. |

The Documentation Operating System explains and enforces the process. The Client Architecture Workspace is the place where project-specific architecture knowledge is created and maintained.

AI must not mix these planes. Tooling vocabulary belongs in `agent/glossary.md`. Project vocabulary belongs in root `glossary.md`. Harness and policy changes should not be disguised as project architecture updates, and project architecture content should not be treated as agent/tooling configuration.

## 4. Core Problem

Architecture documentation usually fails in one of four ways:

1. **Creation failure** — documents are never created, or are created inconsistently.
2. **Clarity failure** — documents exist but do not help humans or AI make correct development decisions.
3. **Maintenance failure** — documents exist but fall out of date.
4. **Trust failure** — documents look polished but no longer reflect source truth.

AI can accelerate all four failure modes if it is allowed to invent, overwrite, or optimize for passing text checks without grounding changes in evidence.

This strategy uses repository rules and deterministic validation to make AI useful without making it authoritative.

## 5. Operating Principles

| Principle | Meaning |
|---|---|
| Architectural clarity first | Every artifact should improve the ability of a human or AI to understand the system and make correct development decisions. |
| Human source facts first | Business facts, system boundaries, decisions, ownership, and approvals come from humans or explicit source material. |
| AI may structure, not invent | AI can organize, repair, summarize, and propose, but it must not fabricate missing architecture facts. |
| Verifiers define success | A task is not complete because an agent says it is complete; it is complete when the relevant validation gates pass. |
| Gaps are first-class artifacts | Missing facts become `ARCH-GAP`, open questions, assumptions, or risks with an owner. |
| Guardrails serve architecture | Validation, skills, scaffolds, and policy exist to protect architecture clarity, not to become the main deliverable. |
| Control files are protected | Agents must not modify the harness, verifiers, scaffold scripts, CI, or policy without human approval. |
| Local equals CI | The same validation path should run locally and in GitHub Actions. |
| Plane separation | The documentation operating system and the client architecture workspace are related but distinct. |
| Documentation is active system infrastructure | Architecture documentation, standards, decisions, and governance files are maintained as part of delivery, not as a side artifact. |

## 6. Human and AI Division of Labor

| Responsibility | Human | AI |
|---|---:|---:|
| Define business goals and system intent | Owns | May summarize |
| Approve architecture decisions | Owns | May draft ADR shells and options |
| Provide source facts | Owns | May extract and organize |
| Create document structure | Reviews | May scaffold and repair |
| Maintain links, headers, status, and glossary references | Reviews | May repair when safe |
| Identify missing information | Reviews | May detect and escalate |
| Validate repository health | Reviews output | Runs deterministic gates |
| Decide whether content reflects reality | Owns | May flag likely drift |
| Decide whether documentation is useful for development | Owns | May identify clarity gaps |
| Distinguish tooling docs from client architecture docs | Owns | Must preserve separation |

## 7. Documentation Operating Loop

The working loop is:

```text
observe → plan → ask/escalate → repair → verify → clarify
```

The loop is intentionally conservative:

1. **Observe** repository state, verifier failures, governing policy, and the relevant documentation plane.
2. **Plan** repairs before mutation.
3. **Ask or escalate** when source facts are missing.
4. **Repair** only bounded structural or explicitly supported content issues.
5. **Verify** through deterministic checks.
6. **Clarify** whether the resulting documentation actually helps humans or AI make better development decisions.

The loop should never jump directly from user request to mutation when policy, source facts, verifier state, or documentation-plane ownership is unknown.

## 8. Current Execution Model

The current operating model is Claude Code skills plus repository verifiers.

Primary current mechanisms:

- `.claude/skills/` — human-readable Claude skill instructions and trigger rules.
- `.claude/skills/tests/` — human-readable and machine-readable skill fixtures.
- `.validation-config.json` — shared validation gate configuration.
- `run_validation.py` — local validation runner.
- `verify_*.py` — deterministic validation scripts.
- `agent/SKILL.md` — governing policy for write boundaries and documentation rules.

The intended CI target is the same validation command used locally:

```bash
python3 run_validation.py
```

## 9. Reference / Future Execution Model

The `agent/prompts/` directory describes a Supervisor and specialist-agent architecture. Treat this as a reference or future harness design unless a runtime explicitly wires those prompts into execution.

The currently reliable execution model is the skills-and-verifiers model described in this strategy and in `.claude/skills/PLAN.md`.

## 10. Maturity Ladder

| Level | Name | Description | Primary Risk Controlled |
|---:|---|---|---|
| 1 | Document Template | Basic folders and document templates exist. | Inconsistent starting structure. |
| 2 | Structural Linter | Required headers, links, statuses, and placeholders are checked. | Broken or malformed documentation. |
| 3 | Harness | Verifiers, scaffolds, audit boundaries, and control files define a repeatable operating environment. | Manual inconsistency and accidental drift. |
| 4 | Loop Engineering | AI skills operate inside the harness using observe-plan-repair-verify discipline. | AI invention and reward-hacking. |
| 5 | Architecture Clarity Coverage | The workspace shows whether core architecture questions are answered well enough to guide development. | Valid documents that still do not help implementation. |
| 6 | Semantic Drift Detection | Documentation is checked against code, deployment, runtime, or other source-of-truth systems. | Perfectly linted but incorrect documentation. |
| 7 | Scheduled Maintenance | The documentation loop runs on a cadence and escalates changes or gaps. | Documentation decay between human touchpoints. |

This repository is currently strongest at Levels 2-4. Levels 5-7 are planned maturity extensions.

## 11. What the Current System Verifies

The current system verifies:

- required document structure;
- approved document status values;
- relative links and anchors;
- ADR sequence;
- orphaned active documents;
- glossary link coverage;
- owned `ARCH-GAP` comments;
- skill structure and trigger fixtures;
- repair-plan fixture shape;
- source-fact citation fixture shape;
- skill retirement fixture shape;
- selected executable fixture behavior.

## 12. What the Current System Does Not Yet Verify

The current system does not fully verify semantic truth or architecture usefulness.

It does not yet prove that:

- architecture views answer the questions developers need before implementation;
- system context and scope are complete enough for safe development;
- standards are actionable enough to guide code, test, security, and operations decisions;
- architecture views match a codebase;
- deployment diagrams match deployed infrastructure;
- integration claims match actual APIs or event contracts;
- ownership tables match current team responsibility;
- example content has been separated from active source-truth content;
- stale documents are wrong, only that they may need review.

These are intentionally called out as future maturity targets rather than hidden limitations.

## 13. Instantiating This Strategy in a New Repository

To apply this strategy elsewhere:

1. Establish the two-plane separation rule before adding content.
2. Identify which files belong to the Documentation Operating System and which belong to the Client Architecture Workspace.
3. Establish active client documentation boundaries: `architecture/`, `decisions/`, `standards/`, `governance/`, and `glossary.md` or project equivalents.
4. Define the architecture clarity questions that the workspace must answer for humans and AI before development.
5. Add deterministic structural validation before adding AI automation.
6. Define source-fact and gap-handling rules before allowing AI to update content.
7. Add scaffold scripts for repeatable artifacts such as ADRs and system folders.
8. Add AI skills only after repository policy and validation exist.
9. Protect control files from agent mutation.
10. Use a single local validation runner and wire CI to the same command.
11. Add semantic drift detection only after structural maintenance is stable.

## 14. Strategy Backlog

| Item | Purpose |
|---|---|
| Architecture clarity checklist | Define the core questions the client architecture workspace must answer before safe development. |
| Example-content isolation | Ensure demonstration content cannot be mistaken for active architecture truth. |
| Plane-aware validation | Add checks that prevent agent/tooling vocabulary or files from bleeding into project architecture vocabulary. |
| Semantic drift detection | Compare documentation claims against implementation, deployment, or runtime sources. |
| Scheduled maintenance cadence | Run the loop periodically and file escalations for stale or incomplete documents. |
| Project glossary expansion | Make the root `glossary.md` a true project vocabulary authority for the target system. |

## 15. Success Definition

The strategy succeeds when a repository can:

- create architecture artifacts consistently;
- explain the architecture clearly enough for humans and AI to make correct development decisions;
- maintain documentation structure through deterministic checks;
- let AI repair safe issues without inventing facts;
- surface missing information as owned gaps;
- separate active source truth from examples and archived material;
- separate the documentation operating system from the client architecture workspace;
- run the same validation path locally and in CI;
- reduce architectural drift, mistakes, and breakage during development;
- provide humans with clear decisions, risks, assumptions, and open questions.
