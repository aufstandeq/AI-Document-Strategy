#!/usr/bin/env python3
"""Execute skill verifier fixtures against temporary Claude skill workspaces."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
FIXTURE = ROOT / ".claude" / "skills" / "tests" / "skill-verifier-fixtures.json"
VERIFIER = ROOT / "verify_claude_skills.py"


def load_fixture() -> dict[str, Any]:
    if not FIXTURE.exists():
        raise FileNotFoundError(f"Missing fixture: {FIXTURE.relative_to(ROOT)}")
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def write_case_workspace(case: dict[str, Any], workspace: Path) -> None:
    skills_root = workspace / ".claude" / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)

    folder_name = case.get("folder_name")
    files = case.get("files", [])

    if folder_name is None:
        base = skills_root
    else:
        base = skills_root / folder_name
        base.mkdir(parents=True, exist_ok=True)

    for item in files:
        target = base / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item["content"], encoding="utf-8")


def run_case(case: dict[str, Any]) -> tuple[bool, str]:
    expected_result = case["expected_result"]

    with tempfile.TemporaryDirectory(prefix="skill-fixture-") as temp_dir:
        workspace = Path(temp_dir)
        write_case_workspace(case, workspace)

        result = subprocess.run(
            [sys.executable, str(VERIFIER), "--workspace", str(workspace)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    actual_result = "PASS" if result.returncode == 0 else "FAIL"
    ok = actual_result == expected_result
    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    return ok, f"expected={expected_result} actual={actual_result}\n{output}"


def main() -> int:
    print("verify_skill_verifier_execution.py")
    print(f"Fixture: {FIXTURE.relative_to(ROOT)}")
    print(f"Verifier: {VERIFIER.relative_to(ROOT)}")
    print("=" * 88)

    try:
        data = load_fixture()
    except Exception as exc:
        print(f"FAIL: could not load fixture: {exc}")
        return 1

    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        print("FAIL: fixture contains no cases")
        return 1

    failures: list[str] = []

    for case in cases:
        case_id = case.get("id", "UNKNOWN")
        ok, detail = run_case(case)
        if ok:
            print(f"PASS: {case_id}")
        else:
            print(f"FAIL: {case_id}")
            print(detail)
            failures.append(case_id)

    print("=" * 88)
    if failures:
        print(f"FAIL: executable fixture failures: {', '.join(failures)}")
        return 1

    print("PASS: all executable skill verifier fixtures matched expected results")
    return 0


if __name__ == "__main__":
    sys.exit(main())
