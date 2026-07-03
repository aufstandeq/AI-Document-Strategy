#!/usr/bin/env python3
"""Validate machine-readable source-fact citation fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
FIXTURE = ROOT / ".claude" / "skills" / "tests" / "source-fact-citation-pattern.json"

CLASSIFICATIONS = {"SOURCE_FACT", "INFERENCE", "GAP", "POLICY", "VERIFIER_OUTPUT"}
STATUSES = {"SAFE_TO_REPAIR", "REQUIRES_SOURCE_FACTS", "BLOCKED_POLICY", "HUMAN_REVIEW_REQUIRED", "NO_REPAIR_NEEDED"}
REQUIRED_TOP = {
    "schema_version",
    "purpose",
    "classifications",
    "required_sections",
    "optional_sections",
    "mutation_allowed_when",
    "prohibited_source_types",
    "cases",
}
REQUIRED_CASE = {
    "id",
    "description",
    "classification_set",
    "expected_status",
    "requires_source_fact_inventory",
    "requires_inference_table",
    "requires_gap_table",
    "mutation_allowed",
}


def error(message: str) -> str:
    return f"{FIXTURE.relative_to(ROOT)}: {message}"


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing_top = sorted(REQUIRED_TOP - set(data))
    if missing_top:
        return [error(f"missing top-level fields: {missing_top}")]

    if set(data["classifications"]) != CLASSIFICATIONS:
        errors.append(error("classifications do not match approved set"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(error("cases must be a non-empty list"))
        return errors

    seen: set[str] = set()
    observed_classifications: set[str] = set()

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

        classifications = case["classification_set"]
        if not isinstance(classifications, list) or not classifications:
            errors.append(error(f"{prefix}.classification_set must be a non-empty list"))
        else:
            for item in classifications:
                if item not in CLASSIFICATIONS:
                    errors.append(error(f"{prefix}.classification_set contains unknown value: {item}"))
                else:
                    observed_classifications.add(item)

        if case["expected_status"] not in STATUSES:
            errors.append(error(f"{prefix}.expected_status is not approved"))

        for field in [
            "requires_source_fact_inventory",
            "requires_inference_table",
            "requires_gap_table",
            "mutation_allowed",
        ]:
            if not isinstance(case[field], bool):
                errors.append(error(f"{prefix}.{field} must be boolean"))

        if "INFERENCE" in classifications and not case["requires_inference_table"]:
            errors.append(error(f"{prefix}: INFERENCE cases must require an inference table"))

        if "GAP" in classifications and not case["requires_gap_table"]:
            errors.append(error(f"{prefix}: GAP cases must require a gap table"))

        if case["expected_status"] in {"REQUIRES_SOURCE_FACTS", "HUMAN_REVIEW_REQUIRED", "BLOCKED_POLICY"} and case["mutation_allowed"]:
            errors.append(error(f"{prefix}: blocked/review statuses must not allow mutation"))

    missing_coverage = sorted(CLASSIFICATIONS - observed_classifications)
    if missing_coverage:
        errors.append(error(f"missing classification coverage: {missing_coverage}"))

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

    print("verify_source_fact_citation_fixtures.py")
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
