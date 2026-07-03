#!/usr/bin/env python3
"""Validate machine-readable skill retirement policy fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
FIXTURE = ROOT / ".claude" / "skills" / "tests" / "skill-retirement-policy.json"

RETIREMENT_STATES = {"ACTIVE", "DEPRECATED", "SUPERSEDED", "ARCHIVED", "REMOVED"}
REQUIRES_BLOCK = {"DEPRECATED", "SUPERSEDED", "ARCHIVED"}
REQUIRES_APPROVAL = {"REMOVED"}
REQUIRED_FIELDS = {"Status", "Effective Date", "Replaced By", "Reason", "Approved By"}
REQUIRED_TOP = {
    "schema_version",
    "purpose",
    "retirement_states",
    "states_requiring_retirement_block",
    "states_requiring_human_approval",
    "required_retirement_fields",
    "required_update_targets",
    "cases",
}
REQUIRED_CASE = {
    "id",
    "description",
    "state",
    "requires_retirement_block",
    "requires_replacement",
    "requires_human_approval",
    "may_be_selected_for_new_work",
}


def error(message: str) -> str:
    return f"{FIXTURE.relative_to(ROOT)}: {message}"


def validate_bool(case: dict[str, Any], field: str, prefix: str) -> list[str]:
    if not isinstance(case.get(field), bool):
        return [error(f"{prefix}.{field} must be boolean")]
    return []


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing_top = sorted(REQUIRED_TOP - set(data))
    if missing_top:
        return [error(f"missing top-level fields: {missing_top}")]

    if set(data["retirement_states"]) != RETIREMENT_STATES:
        errors.append(error("retirement_states does not match approved set"))
    if set(data["states_requiring_retirement_block"]) != REQUIRES_BLOCK:
        errors.append(error("states_requiring_retirement_block does not match approved set"))
    if set(data["states_requiring_human_approval"]) != REQUIRES_APPROVAL:
        errors.append(error("states_requiring_human_approval does not match approved set"))
    if set(data["required_retirement_fields"]) != REQUIRED_FIELDS:
        errors.append(error("required_retirement_fields does not match approved set"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(error("cases must be a non-empty list"))
        return errors

    seen: set[str] = set()
    observed_states: set[str] = set()

    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(error(f"{prefix} must be an object"))
            continue

        missing_case = sorted(REQUIRED_CASE - set(case))
        if missing_case:
            errors.append(error(f"{prefix} missing fields: {missing_case}"))
            continue

        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(error(f"{prefix}.id must be a non-empty string"))
        elif case_id in seen:
            errors.append(error(f"duplicate case id: {case_id}"))
        else:
            seen.add(case_id)

        state = case["state"]
        if state not in RETIREMENT_STATES:
            errors.append(error(f"{prefix}.state is not approved"))
        else:
            observed_states.add(state)

        for field in [
            "requires_retirement_block",
            "requires_replacement",
            "requires_human_approval",
            "may_be_selected_for_new_work",
        ]:
            errors.extend(validate_bool(case, field, prefix))

        if state in REQUIRES_BLOCK and not case["requires_retirement_block"]:
            errors.append(error(f"{prefix}: {state} must require a retirement block"))
        if state == "ACTIVE" and case["requires_retirement_block"]:
            errors.append(error(f"{prefix}: ACTIVE must not require a retirement block"))
        if state == "SUPERSEDED" and not case["requires_replacement"]:
            errors.append(error(f"{prefix}: SUPERSEDED must require a replacement"))
        if state in REQUIRES_APPROVAL and not case["requires_human_approval"]:
            errors.append(error(f"{prefix}: {state} must require human approval"))
        if state != "ACTIVE" and case["may_be_selected_for_new_work"]:
            errors.append(error(f"{prefix}: retired states must not be selected for new work"))

    missing_coverage = sorted(RETIREMENT_STATES - observed_states)
    if missing_coverage:
        errors.append(error(f"missing retirement state coverage: {missing_coverage}"))

    return errors


def main() -> int:
    errors: list[str] = []

    if not FIXTURE.exists():
        errors.append(error("fixture file does not exist"))
    else:
        try:
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            errors.extend(validate(data))
        except json.JSONDecodeError as exc:
            errors.append(error(f"invalid JSON: {exc}"))

    print("verify_skill_retirement_fixtures.py")
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
