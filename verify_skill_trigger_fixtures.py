#!/usr/bin/env python3
"""
verify_skill_trigger_fixtures.py — Validate machine-readable Claude skill trigger fixtures.

This verifier checks `.claude/skills/tests/trigger-cases.json` so trigger expectations
remain structured, reviewable, and ready for future automated skill-selection tests.

Checks:
  1. Fixture file exists and is valid JSON.
  2. Required top-level fields exist.
  3. Case IDs are unique.
  4. Each case has required fields.
  5. Expected skills refer to known skill names.
  6. Status values are from the approved set.
  7. Triggering cases do not use `none` as the expected skill.
  8. Ambiguous cases include a rationale.

Exit codes:
  0 — all checks passed
  1 — one or more hard failures found

Usage:
  python3 verify_skill_trigger_fixtures.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).parent.resolve()
FIXTURE_PATH = WORKSPACE_ROOT / ".claude" / "skills" / "tests" / "trigger-cases.json"

KNOWN_SKILLS = {
    "doc-loop-prepare",
    "run-doc-checker",
    "fix-doc-linter-failures",
    "create-adr",
    "create-system-scaffold",
    "create-system-context",
    "escalate-doc-gap",
    "none",
}

APPROVED_STATUSES = {
    "SHOULD_TRIGGER",
    "SHOULD_NOT_TRIGGER",
    "AMBIGUOUS_ASK_CLARIFYING_QUESTION",
}

TOP_LEVEL_REQUIRED_FIELDS = {
    "schema_version",
    "purpose",
    "status_values",
    "selection_rule",
    "cases",
}

CASE_REQUIRED_FIELDS = {
    "id",
    "user_request",
    "expected_skill",
    "status",
    "rationale",
}


def load_fixture() -> tuple[dict[str, Any] | None, list[str]]:
    if not FIXTURE_PATH.exists():
        return None, [f"Missing fixture file: {FIXTURE_PATH.relative_to(WORKSPACE_ROOT)}"]

    try:
        return json.loads(FIXTURE_PATH.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"Invalid JSON in {FIXTURE_PATH.relative_to(WORKSPACE_ROOT)}: {exc}"]


def validate_fixture(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in sorted(TOP_LEVEL_REQUIRED_FIELDS):
        if field not in data:
            errors.append(f"Missing top-level field: {field}")

    if errors:
        return errors

    if set(data.get("status_values", [])) != APPROVED_STATUSES:
        errors.append(
            "status_values must exactly match approved statuses: "
            f"{sorted(APPROVED_STATUSES)}"
        )

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        return errors

    seen_ids: set[str] = set()

    for idx, case in enumerate(cases):
        prefix = f"cases[{idx}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: case must be an object")
            continue

        for field in sorted(CASE_REQUIRED_FIELDS):
            if not case.get(field):
                errors.append(f"{prefix}: missing required field '{field}'")

        case_id = case.get("id")
        if case_id:
            if case_id in seen_ids:
                errors.append(f"{prefix}: duplicate id '{case_id}'")
            seen_ids.add(case_id)

        expected_skill = case.get("expected_skill")
        if expected_skill and expected_skill not in KNOWN_SKILLS:
            errors.append(
                f"{prefix}: unknown expected_skill '{expected_skill}'. "
                f"Known values: {sorted(KNOWN_SKILLS)}"
            )

        status = case.get("status")
        if status and status not in APPROVED_STATUSES:
            errors.append(
                f"{prefix}: invalid status '{status}'. "
                f"Approved values: {sorted(APPROVED_STATUSES)}"
            )

        if status == "SHOULD_TRIGGER" and expected_skill == "none":
            errors.append(f"{prefix}: SHOULD_TRIGGER cases must name a concrete skill")

        rationale = case.get("rationale", "")
        if status == "AMBIGUOUS_ASK_CLARIFYING_QUESTION" and len(rationale.strip()) < 20:
            errors.append(f"{prefix}: ambiguous cases require a specific rationale")

    return errors


def main() -> int:
    data, errors = load_fixture()
    if data is not None:
        errors.extend(validate_fixture(data))

    print("verify_skill_trigger_fixtures.py — Claude Skill Trigger Fixture Validation")
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Fixture: {FIXTURE_PATH.relative_to(WORKSPACE_ROOT)}")
    print("=" * 80)

    if errors:
        print("\n❌ Trigger fixture validation failures:")
        for err in errors:
            print(f"   {err}")
        print("\nFix the trigger fixture issues above before merging.")
        return 1

    assert data is not None
    print(f"\n✅ Trigger fixture validations passed. Cases: {len(data['cases'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
