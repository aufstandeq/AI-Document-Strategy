# Skill Retirement Policy

## Purpose

This file defines how Claude skills are deprecated, superseded, archived, or removed without losing traceability.

A skill is part of the repository control surface. It must not disappear silently, because downstream behavior, trigger expectations, fixtures, transcripts, and prior repair plans may depend on its existence.

## Retirement States

| State | Meaning | Allowed? |
|---|---|---:|
| `ACTIVE` | Skill is current and may be triggered. | Yes |
| `DEPRECATED` | Skill remains present but should not be selected for new work. | Yes |
| `SUPERSEDED` | Skill has been replaced by another named skill. | Yes |
| `ARCHIVED` | Skill content is preserved for history but excluded from active selection. | Yes |
| `REMOVED` | Skill folder is deleted. | Only with explicit human approval |

## Required Deprecation Metadata

A deprecated, superseded, or archived skill must include a retirement block in `SKILL.md`:

```markdown
## Retirement Status

| Field | Value |
|---|---|
| Status | DEPRECATED |
| Effective Date | YYYY-MM-DD |
| Replaced By | `new-skill-name` or `none` |
| Reason | Short reason. |
| Approved By | Human owner or approval source. |
```

## Active Skill Rule

A skill is considered active when:

1. Its folder exists under `.claude/skills/<skill-name>/`.
2. It contains `SKILL.md`.
3. Its frontmatter `name` matches the folder name.
4. Its frontmatter `description` contains `Use when`.
5. It does not contain a `## Retirement Status` block with `DEPRECATED`, `SUPERSEDED`, or `ARCHIVED`.

## Deprecation Rule

When a skill is deprecated:

1. Keep the skill folder and `SKILL.md` in place.
2. Add `## Retirement Status` to the skill body.
3. Update `.claude/skills/README.md` to show the skill state.
4. Update trigger fixtures so the deprecated skill no longer appears as the expected skill for new work.
5. Add or update replacement skill trigger cases when applicable.
6. Run all skill and fixture verifiers.

## Supersession Rule

When a skill is replaced by another skill:

1. Mark old skill as `SUPERSEDED`.
2. Name the replacement in `Replaced By`.
3. Preserve the old skill instructions for history.
4. Move active trigger cases to the replacement skill.
5. Add one negative or redirect fixture showing the old trigger should route to the replacement.

## Archive Rule

Use `ARCHIVED` when the skill is retained only for historical reference.

Archived skills may remain under `.claude/skills/<skill-name>/` only if the skill verifier explicitly allows archived status. Otherwise, move archived content to a clearly named historical reference location approved by the repository owner.

## Removal Rule

Deleting a skill folder is allowed only when all conditions are true:

1. The user explicitly approves deletion.
2. No trigger fixture expects the skill.
3. No repair-plan fixture depends on the skill.
4. `.claude/skills/README.md` and `.claude/skills/PLAN.md` are updated.
5. Git history preserves the removed content.
6. CI passes.

## Prohibited Patterns

Do not:

```text
Delete a skill because it appears unused.
Rename a skill folder without updating frontmatter and fixtures.
Leave trigger fixtures pointing at a retired skill.
Mark a skill deprecated without a replacement or reason.
Use retired skills for new mutation tasks.
```

## Required Retirement Checklist

```markdown
## Skill Retirement Checklist

- [ ] Retirement state chosen: ACTIVE / DEPRECATED / SUPERSEDED / ARCHIVED / REMOVED.
- [ ] `SKILL.md` retirement block added or updated.
- [ ] Replacement skill identified, or `none` documented.
- [ ] Trigger fixtures updated.
- [ ] Example transcripts updated if affected.
- [ ] README / PLAN updated.
- [ ] Verifiers updated if rules changed.
- [ ] CI passed.
- [ ] Human approval recorded for removal or behavior-breaking change.
```

## Default Decision

When uncertain, prefer:

```text
SUPERSEDED over REMOVED
DEPRECATED over DELETED
human review over silent behavior change
```
