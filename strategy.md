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

See [Glossary](./glossary.md) for definitions of key terms used in this document.

---

## 1. Strategy Statement

This repository is both a working implementation and a reference strategy for AI-assisted architecture documentation.

The strategy is not to let AI freely generate architecture content. The strategy is to give AI a constrained operating environment where:

- humans own source facts, decisions, priorities, and approval;
- AI assists with structure, repair, synthesis, and gap surfacing;
- deterministic verifiers define success;
- missing information is recorded as an owned gap instead of invented;
- local validation and CI validation converge on the same repeatable checks.

The intended end state is a documentation system that is easy to operate, hard to drift, and safe for both human developers and AI assistants to use.

## 2. Core Problem

Architecture documentation usually fails in one of three ways:

1. **Creation failure** — documents are never created, or are created inconsistently.
2. **Maintenance failure** — documents exist but fall out of date.
3. **Trust failure** — documents look polished but no longer reflect source truth.

AI can accelerate all three failure modes if it is allowed to invent, overwrite, or optimize for passing text checks without grounding changes in evidence.

This strategy uses repository rules and deterministic validation to make the AI useful without making it authoritative.

## 3. Operating Principles

| Principle | Meaning |
|---|---|
| Human source facts first | Business facts, system boundaries, decisions, ownership, and approvals come from humans or explicit source material. |
| AI may structure, not invent | AI can organize, repair, summarize, and propose, but it must not fabricate missing architecture facts. |
| Verifiers define success | A task is not complete because an agent says it is complete; it is complete when the relevant validation gates pass. |
| Gaps are first-class artifacts | Missing facts become `ARCH-GAP`, open questions, assumptions, or risks with an owner. |
| Control files are protected | Agents must not modify the harness, verifiers, scaffold scripts, CI, or policy without human approval. |
| Local equals CI | The same validation path should run locally and in GitHub Actions. |
| Documentation is active system infrastructure | Architecture documentation, standards, decisions, and governance files are maintained as part of delivery, not as a side artifact. |

## 4. Human and AI Division of Labor

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

## 5. Documentation Operating Loop

The working loop is:

```text
observe → plan → ask/escalate → repair → verify
```

The loop is intentionally conservative:

1. **Observe** repository state, verifier failures, and governing policy.
2. **Plan** repairs before mutation.
3. **Ask or escalate** when source facts are missing.
4. **Repair** only bounded structural or explicitly supported content issues.
5. **Verify** through deterministic checks.

The loop should never jump directly from user request to mutation when policy, source facts, or verifier state are unknown.

## 6. Current Execution Model

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

## 7. Reference / Future Execution Model

The `agent/prompts/` directory describes a Supervisor and specialist-agent architecture. Treat this as a reference or future harness design unless a runtime explicitly wires those prompts into execution.

The currently reliable execution model is the skills-and-verifiers model described in this strategy and in `.claude/skills/PLAN.md`.

## 8. Maturity Ladder

| Level | Name | Description | Primary Risk Controlled |
|---:|---|---|---|
| 1 | Document Template | Basic folders and document templates exist. | Inconsistent starting structure. |
| 2 | Structural Linter | Required headers, links, statuses, and placeholders are checked. | Broken or malformed documentation. |
| 3 | Harness | Verifiers, scaffolds, audit boundaries, and control files define a repeatable operating environment. | Manual inconsistency and accidental drift. |
| 4 | Loop Engineering | AI skills operate inside the harness using observe-plan-repair-verify discipline. | AI invention and reward-hacking. |
| 5 | Semantic Drift Detection | Documentation is checked against code, deployment, runtime, or other source-of-truth systems. | Perfectly linted but incorrect documentation. |
| 6 | Scheduled Maintenance | The documentation loop runs on a cadence and escalates changes or gaps. | Documentation decay between human touchpoints. |

This repository is currently strongest at Levels 2-4. Levels 5 and 6 are planned maturity extensions.

## 9. What the Current System Verifies

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

## 10. What the Current System Does Not Yet Verify

The current system does not fully verify semantic truth.

It does not yet prove that:

- architecture views match a codebase;
- deployment diagrams match deployed infrastructure;
- integration claims match actual APIs or event contracts;
- ownership tables match current team responsibility;
- example content has been separated from active source-truth content;
- stale documents are wrong, only that they may need review.

These are intentionally called out as future maturity targets rather than hidden limitations.

## 11. Instantiating This Strategy in a New Repository

To apply this strategy elsewhere:

1. Establish active documentation boundaries: `architecture/`, `decisions/`, `standards/`, `governance/`, and `glossary.md` or project equivalents.
2. Add deterministic structural validation before adding AI automation.
3. Define source-fact and gap-handling rules before allowing AI to update content.
4. Add scaffold scripts for repeatable artifacts such as ADRs and system folders.
5. Add AI skills only after repository policy and validation exist.
6. Protect control files from agent mutation.
7. Use a single local validation runner and wire CI to the same command.
8. Add semantic drift detection only after structural maintenance is stable.

## 12. Strategy Backlog

| Item | Purpose |
|---|---|
| CI runner simplification | Make GitHub Actions call `python3 run_validation.py` instead of manually listing gates. |
| Example-content isolation | Ensure demonstration content cannot be mistaken for active architecture truth. |
| Agent execution model reconciliation | Clearly label current skills-based operation versus future prompt-agent design. |
| Semantic drift detection | Compare documentation claims against implementation, deployment, or runtime sources. |
| Scheduled maintenance cadence | Run the loop periodically and file escalations for stale or incomplete documents. |
| Glossary expansion | Make `glossary.md` a true vocabulary authority rather than only a required link target. |

## 13. Success Definition

The strategy succeeds when a repository can:

- create architecture artifacts consistently;
- maintain documentation structure through deterministic checks;
- let AI repair safe issues without inventing facts;
- surface missing information as owned gaps;
- separate active source truth from examples and archived material;
- run the same validation path locally and in CI;
- provide humans with clear decisions, risks, assumptions, and open questions.
