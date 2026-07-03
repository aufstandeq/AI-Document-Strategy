#!/usr/bin/env python3
"""Validate machine-readable repair-plan fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
FIXTURE = ROOT / ".claude" / "skills" / "tests" / "repair-plan-fixture.json"

STATUSES = {
    "SAFE_TO_REPAIR",
    "REQUIRES_SOURCE_FACTS",
    "BLOCKED_POLICY",
    "HUMAN_REVIEW_REQUIRED",
    "NO_REPAIR_NEEDED",
}

NEXT_SKILLS = {
    "fix-doc-linter-failures",
    "escalate-doc-gap",
    "none",
}

REQUIRED_TOP = {
    "schema_version",
    "purpose",
    "approved_statuses",
    "approved_next_skills",
    "required_output_sections",
    "cases",
}

REQUIRED_CASE = {
    "id",
    "input_failure",
    "expected_status",
    "expected_next_skill",
    "requires_source_facts",
    "requires_human_review",
    "must_not_invent",
    "expected_actions",
}


def err(message: str) -> str:
    return f"{FIXTURE.relative_to(ROOT)}: {message}"


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing_top = sorted(REQUIRED_TOP - set(data))
    if missing_top:
        errors.append(err(f"missing top-level fields: {missing_top}"))
        return errors

    if set(data["approved_statuses"]) != STATUSES:
        errors.append(err("approved_statuses does not match verifier status set"))

    if set(data["approved_next_skills"]) != NEXT_SKILLS:
        errors.append(err("approved_next_skills does not match verifier next-skill set"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(err("cases must be a non-empty list"))
        return errors

    seen: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(err(f"{prefix} must be an object"))
            continue

        missing_case = sorted(REQUIRED_CASE - set(case))
        if missing_case:
            errors.append(err(f"{prefix} missing fields: {missing_case}"))
            continue

        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(err(f"{prefix}.id must be a non-empty string"))
        elif case_id in seen:
            errors.append(err(f"duplicate case id: {case_id}"))
        else:
            seen.add(case_id)

        if case["expected_status"] not in STATUSES:
            errors.append(err(f"{prefix}.expected_status is not approved"))

        if case["expected_next_skill"] not in NEXT_SKILLS:
            errors.append(err(f"{prefix}.expected_next_skill is not approved"))

        if not isinstance(case["requires_source_facts"], bool):
            errors.append(err(f"{prefix}.requires_source_facts must be boolean"))

        if not isinstance(case["requires_human_review"], bool):
            errors.append(err(f"{prefix}.requires_human_review must be boolean"))

        if not isinstance(case["must_not_invent"], list):
            errors.append(err(f"{prefix}.must_not_invent must be a list"))

        actions = case["expected_actions"]
        if not isinstance(actions, list) or not actions:
            errors.append(err(f"{prefix}.expected_actions must be a non-empty list"))

        if case["expected_status"] == "SAFE_TO_REPAIR" and case["requires_source_facts"]:
            errors.append(err(f"{prefix}: SAFE_TO_REPAIR cannot require source facts"))

        if case["expected_status"] == "REQUIRES_SOURCE_FACTS" and not case["requires_source_facts"]:
            errors.append(err(f"{prefix}: REQUIRES_SOURCE_FACTS must require source facts"))

        if case["expected_status"] in {"BLOCKED_POLICY", "NO_REPAIR_NEEDED"} and case["expected_next_skill"] != "none":
            errors.append(err(f"{prefix}: terminal statuses must use next skill 'none'"))

    return errors


def main() -> int:
    errors: list[str] = []

    if not FIXTURE.exists():
        errors.append(err("fixture file does not exist"))
    else:
        try:
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            errors.extend(validate(data))
        except json.JSONDecodeError as exc:
            errors.append(err(f"invalid JSON: {exc}"))

    print("verify_repair_plan_fixtures.py")
    print(f"Fixture: {FIXTURE.relative_to(ROOT)}")

    if errors:
        print("\nFAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
