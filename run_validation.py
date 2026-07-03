#!/usr/bin/env python3
"""Run repository validation gates from .validation-config.json."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
CONFIG_PATH = ROOT / ".validation-config.json"


@dataclass(frozen=True)
class Gate:
    gate_id: str
    name: str
    command: list[str]
    hard_gate: bool


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing validation config: {CONFIG_PATH.relative_to(ROOT)}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def parse_gates(config: dict[str, Any]) -> list[Gate]:
    gates = config.get("validation_gates")
    if not isinstance(gates, list) or not gates:
        raise ValueError("validation_gates must be a non-empty list")

    parsed: list[Gate] = []
    seen: set[str] = set()

    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            raise ValueError(f"validation_gates[{index}] must be an object")

        for field in ["id", "name", "command", "hard_gate"]:
            if field not in gate:
                raise ValueError(f"validation_gates[{index}] missing field: {field}")

        gate_id = gate["id"]
        name = gate["name"]
        command = gate["command"]
        hard_gate = gate["hard_gate"]

        if not isinstance(gate_id, str) or not gate_id.strip():
            raise ValueError(f"validation_gates[{index}].id must be a non-empty string")
        if gate_id in seen:
            raise ValueError(f"duplicate validation gate id: {gate_id}")
        seen.add(gate_id)

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"validation_gates[{index}].name must be a non-empty string")
        if not isinstance(command, list) or not command or not all(isinstance(item, str) and item for item in command):
            raise ValueError(f"validation_gates[{index}].command must be a non-empty string list")
        if not isinstance(hard_gate, bool):
            raise ValueError(f"validation_gates[{index}].hard_gate must be boolean")

        parsed.append(Gate(gate_id=gate_id, name=name, command=command, hard_gate=hard_gate))

    return parsed


def run_gate(gate: Gate) -> bool:
    print("\n" + "=" * 88)
    print(f"{gate.name}")
    print(f"Gate:    {gate.gate_id}")
    print(f"Command: {' '.join(gate.command)}")
    print(f"Mode:    {'hard gate' if gate.hard_gate else 'informational'}")
    print("-" * 88)

    result = subprocess.run(gate.command, cwd=ROOT, text=True)

    if result.returncode == 0:
        print(f"\nPASS: {gate.name}")
        return True

    if gate.hard_gate:
        print(f"\nFAIL: {gate.name} exited with {result.returncode}")
        return False

    print(f"\nWARN: {gate.name} exited with {result.returncode}, but is informational")
    return True


def main() -> int:
    print("run_validation.py — Repository Validation")
    print(f"Workspace: {ROOT}")
    print(f"Config:    {CONFIG_PATH.relative_to(ROOT)}")

    try:
        config = load_config()
        gates = parse_gates(config)
    except Exception as exc:
        print(f"\nFAIL: could not load validation configuration: {exc}")
        return 1

    failures: list[str] = []

    for gate in gates:
        if not run_gate(gate):
            failures.append(gate.gate_id)

    print("\n" + "=" * 88)
    if failures:
        print(f"Validation failed. Failing gates: {', '.join(failures)}")
        return 1

    print("Validation passed. All hard gates succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
