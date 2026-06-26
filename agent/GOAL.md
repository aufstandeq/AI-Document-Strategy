# GOAL.md — Loop Success Criteria

## Document Status
Approved

## Purpose
Define the unambiguous, machine-readable objective for each agent loop run. The orchestrator reads this file at startup to determine what "done" means for the current run scope.

## Owner
Architecture Team

## Last Updated
2026-06-25

---

See [Glossary](../glossary.md) for definitions of key terms used in this document.

---

## 1. Primary Success Condition

A loop run is successful if and only if **both** of the following exit with code 0:

```
python3 verify_docs.py
python3 verify_e2e.py
```

No other signal — agent opinion, Checker PASS, or human review — constitutes success. The exit codes are the sole stop authority.

---

## 2. Default Run Scope

When triggered without an explicit scope argument, the loop targets all active documentation directories:

```
architecture/
decisions/
governance/
glossary.md
standards/
```

The `agent/`, `archive/`, and `.github/` directories are excluded from agent writes. The verifier scripts determine which active files have issues.

---

## 3. Scoped Run (Optional)

The orchestrator accepts a `--scope <path>` argument to target a subset of the repository. Examples:

```bash
python3 run_agent_loop.py --trigger manual --scope architecture/context/
python3 run_agent_loop.py --trigger manual --scope decisions/
```

A scoped run is still considered successful only when the global verifier scripts pass — fixing one directory must not break another.

---

## 4. Specific Measurable Outcomes

A fully passing run means all of the following are true across all active documents:

| Check | Verifier | Required Outcome |
|---|---|---|
| H1 title present | verify_docs.py | Every active `.md` file has an H1 |
| Required headers present | verify_docs.py | `Document Status`, `Purpose`, `Owner`, `Last Updated` in every file |
| Valid Document Status value | verify_docs.py | One of: Draft, In Review, Approved, Deprecated |
| No broken relative links | verify_docs.py | All `[text](path)` links resolve on disk |
| No absolute path links | verify_docs.py | No `/path/to/file` links |
| No orphaned documents | verify_e2e.py | Every active file has at least one inbound link |
| Glossary link present | verify_e2e.py | Every active document links to `glossary.md` |
| ARCH-GAP tags have owners | verify_e2e.py | No `ARCH-GAP` without `[Owner: ...]` |
| ADR sequence intact | verify_e2e.py | No numbering gaps in `decisions/` |
| System links resolve | verify_e2e.py | All `systems/` paths in view files exist on disk |

---

## 5. What the Loop Does NOT Own

The following are out of scope for the agent loop. The loop must not attempt to resolve these:

- Filling in `PENDING_DISCOVERY` sections (requires human knowledge — flag via ARCH-GAP, not invented content)
- Modifying Python scripts or CI configuration
- Creating ADR content beyond the scaffold template
- Making decisions about system topology or technology choices
- Resolving ARCH-GAP tags (the loop may *add* them where gaps exist, but not *resolve* them)

---

## 6. Trigger Modes

| Trigger | When Used | Scope Default |
|---|---|---|
| `cron` | Nightly scheduled run | Full repository |
| `pr` | Pull request opened against main | Files changed in the PR |
| `manual` | Human-initiated run | Specified via `--scope` or full repo |
