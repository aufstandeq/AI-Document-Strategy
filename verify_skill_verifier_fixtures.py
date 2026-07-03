#!/usr/bin/env python3
"""Validate machine-readable fixtures for verify_claude_skills.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
FIXTURE = ROOT / ".claude" / "skills" / "tests" / "skill-verifier-fixtures.json"

EXPECTED_RESULTS = {"PASS", "FAIL"}
FAILURE_CATEGORIES = {
    "folder-name",
    "missing-skill-md",
    "frontmatter",
    "name-mismatch",
    "description-trigger",
    "nested-readme",
    "parent-level-file",
}
REQUIRED_TOP = {
    "schema_version",
    "purpose",
    "approved_expected_results",
    "required_failure_categories",
    "cases",
}
REQUIRED_CASE = {
    "id",
    "description",
    "folder_name",
    "files",
    "expected_result",
    "expected_failures",
}
REQUIRED_FILE = {"path", "content"}


def error(message: str) -> str:
    return f"{FIXTURE.relative_to(ROOT)}: {message}"


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing_top = sorted(REQUIRED_TOP - set(data))
    if missing_top:
        return [error(f"missing top-level fields: {missing_top}")]

    if set(data["approved_expected_results"]) != EXPECTED_RESULTS:
        errors.append(error("approved_expected_results does not match verifier expected-result set"))

    if set(data["required_failure_categories"]) != FAILURE_CATEGORIES:
        errors.append(error("required_failure_categories does not match verifier failure-category set"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(error("cases must be a non-empty list"))
        return errors

    seen: set[str] = set()
    observed_failures: set[str] = set()
    pass_count = 0
    fail_count = 0

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

        description = case["description"]
        if not isinstance(description, str) or not description.strip():
            errors.append(error(f"{prefix}.description must be a non-empty string"))

        folder_name = case["folder_name"]
        if folder_name is not None and (not isinstance(folder_name, str) or not folder_name.strip()):
            errors.append(error(f"{prefix}.folder_name must be null or a non-empty string"))

        files = case["files"]
        if not isinstance(files, list):
            errors.append(error(f"{prefix}.files must be a list"))
        else:
            for file_index, file_item in enumerate(files):
                file_prefix = f"{prefix}.files[{file_index}]"
                if not isinstance(file_item, dict):
                    errors.append(error(f"{file_prefix} must be an object"))
                    continue
                missing_file = sorted(REQUIRED_FILE - set(file_item))
                if missing_file:
                    errors.append(error(f"{file_prefix} missing fields: {missing_file}"))
                    continue
                if not isinstance(file_item["path"], str) or not file_item["path"].strip():
                    errors.append(error(f"{file_prefix}.path must be a non-empty string"))
                if not isinstance(file_item["content"], str):
                    errors.append(error(f"{file_prefix}.content must be a string"))

        result = case["expected_result"]
        if result not in EXPECTED_RESULTS:
            errors.append(error(f"{prefix}.expected_result is not approved"))
        elif result == "PASS":
            pass_count += 1
        else:
            fail_count += 1

        failures = case["expected_failures"]
        if not isinstance(failures, list):
            errors.append(error(f"{prefix}.expected_failures must be a list"))
        else:
            for failure in failures:
                if failure not in FAILURE_CATEGORIES:
                    errors.append(error(f"{prefix}.expected_failures contains unknown category: {failure}"))
                else:
                    observed_failures.add(failure)

        if result == "PASS" and failures:
            errors.append(error(f"{prefix}: PASS cases must not declare expected failures"))
        if result == "FAIL" and not failures:
            errors.append(error(f"{prefix}: FAIL cases must declare at least one expected failure"))

    if pass_count < 1:
        errors.append(error("at least one PASS case is required"))
    if fail_count < 1:
        errors.append(error("at least one FAIL case is required"))

    missing_failure_coverage = sorted(FAILURE_CATEGORIES - observed_failures)
    if missing_failure_coverage:
        errors.append(error(f"missing failure category coverage: {missing_failure_coverage}"))

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

    print("verify_skill_verifier_fixtures.py")
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
