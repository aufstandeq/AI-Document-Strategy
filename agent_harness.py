#!/usr/bin/env python3
"""
agent_harness.py — Documentation loop state harness.

Pure Python. No LLM API calls. Claude Code (or a cowork agent reading CLAUDE.md)
acts as the Maker and Checker. This script manages state, runs verifiers,
enforces stop rules, and returns a structured brief for Claude to act on.

Usage:
  python3 agent_harness.py --prepare           Run verifiers, write STATE.md, print brief
  python3 agent_harness.py --reset             Clear STATE.md for a fresh run
  python3 agent_harness.py --status            Print current STATE.md summary

Exit codes for --prepare:
  0  Continue — verifier failures found, brief written, Claude should act
  1  Escalate — max iterations reached, no progress, or blocklist violation
  2  Success  — both verifiers passed (verify_e2e.py exited 0)
"""

import argparse
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(__file__).parent.resolve()
AGENT_DIR = WORKSPACE_ROOT / "agent"
STATE_FILE = AGENT_DIR / "STATE.md"
SKILL_FILE = AGENT_DIR / "SKILL.md"
GOAL_FILE = AGENT_DIR / "GOAL.md"
LOGS_DIR = AGENT_DIR / "logs"

MAX_ITERATIONS = 3

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

_FIELD_RE = re.compile(r'^## (.+)$')


def _read_field(lines: list[str], field: str) -> str:
    """Return the first non-blank, non-comment line after '## field'."""
    target = f"## {field}"
    capture = False
    for line in lines:
        if line.strip() == target:
            capture = True
            continue
        if capture:
            stripped = line.strip()
            if stripped.startswith("## "):
                break
            if stripped and not stripped.startswith("<!--"):
                return stripped
    return ""


def read_state() -> dict:
    if not STATE_FILE.exists():
        return {
            "run_id": None,
            "iteration": 0,
            "status": "ready",
            "failing_files_hash": "NONE",
            "previous_failing_files_hash": "NONE",
            "stop_reason": "UNSET",
        }
    lines = STATE_FILE.read_text(encoding="utf-8").splitlines()
    return {
        "run_id": _read_field(lines, "run_id") or None,
        "iteration": int(_read_field(lines, "iteration") or "0"),
        "status": _read_field(lines, "status") or "running",
        "failing_files_hash": _read_field(lines, "failing_files_hash") or "NONE",
        "previous_failing_files_hash": _read_field(lines, "previous_failing_files_hash") or "NONE",
        "stop_reason": _read_field(lines, "stop_reason") or "UNSET",
    }


def write_state(state: dict, brief: str = "") -> None:
    AGENT_DIR.mkdir(exist_ok=True)
    content = f"""# STATE.md — Loop Run State

<!-- Written by agent_harness.py. Gitignored — never commit this file. -->

## run_id
{state.get('run_id') or 'UNSET'}

## iteration
{state.get('iteration', 0)}

## max_iterations
{MAX_ITERATIONS}

## status
{state.get('status', 'running')}

## failing_files_hash
{state.get('failing_files_hash', 'NONE')}

## previous_failing_files_hash
{state.get('previous_failing_files_hash', 'NONE')}

## stop_reason
{state.get('stop_reason', 'UNSET')}

## brief
{brief}
"""
    STATE_FILE.write_text(content, encoding="utf-8")


def reset_state() -> None:
    run_id = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    write_state({
        "run_id": run_id,
        "iteration": 0,
        "status": "ready",
        "failing_files_hash": "NONE",
        "previous_failing_files_hash": "NONE",
        "stop_reason": "UNSET",
    }, brief="Fresh run — no verifier output yet.")
    print(f"✅ STATE.md reset. Run ID: {run_id}")


# ---------------------------------------------------------------------------
# Verifiers
# ---------------------------------------------------------------------------

def run_verifiers() -> tuple[int, int, str]:
    """Run both verifier scripts. Returns (docs_exit, e2e_exit, compressed_summary)."""
    def run(script: str) -> tuple[int, str]:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT,
        )
        # Keep only failure lines to minimise context sent to Claude
        failure_lines = [
            ln for ln in result.stdout.splitlines()
            if any(tok in ln for tok in ("❌", "BROKEN", "MISSING", "ORPHAN", "gap", "Error", "FAIL"))
        ]
        return result.returncode, "\n".join(failure_lines[:50])

    docs_exit, docs_out = run("verify_docs.py")
    e2e_exit, e2e_out = run("verify_e2e.py")

    parts = []
    if docs_out:
        parts.append(f"[verify_docs.py — exit {docs_exit}]\n{docs_out}")
    if e2e_out:
        parts.append(f"[verify_e2e.py — exit {e2e_exit}]\n{e2e_out}")
    summary = "\n\n".join(parts) if parts else "No failures detected."

    return docs_exit, e2e_exit, summary


def hash_failures(summary: str) -> str:
    lines = sorted(
        ln.strip() for ln in summary.splitlines()
        if ln.strip() and ("❌" in ln or ".md" in ln)
    )
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Escalation
# ---------------------------------------------------------------------------

def write_escalation(state: dict, reason: str, summary: str) -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now(datetime.UTC).isoformat() + "Z"
    path = LOGS_DIR / "ESCALATION.md"
    path.write_text(f"""# ESCALATION — Loop Failed

**Timestamp:** {ts}
**Run ID:** {state.get('run_id', 'unknown')}
**Iterations reached:** {state.get('iteration', 0)} / {MAX_ITERATIONS}
**Stop reason:** {reason}

## Last Verifier Output
{summary}

## Action Required
A human must resolve the issues above. Common causes:
- Sections requiring domain knowledge (use ARCH-GAP tags)
- Architectural decisions needing an ADR
- Files outside the write allowlist

After fixing, run: `python3 agent_harness.py --reset` then start a new loop.
""", encoding="utf-8")
    print(f"🚨 Escalation written → {path.relative_to(WORKSPACE_ROOT)}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_prepare() -> int:
    state = read_state()

    # Initialise run_id on first prepare if missing
    if not state.get("run_id"):
        state["run_id"] = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")

    iteration = state["iteration"] + 1
    state["iteration"] = iteration
    state["previous_failing_files_hash"] = state["failing_files_hash"]

    print(f"\n{'='*60}")
    print(f"agent_harness.py — prepare  (iteration {iteration}/{MAX_ITERATIONS})")
    print(f"Run ID: {state['run_id']}")
    print(f"{'='*60}\n")

    # Run verifiers
    print("Running verifiers...")
    docs_exit, e2e_exit, summary = run_verifiers()
    print(f"  verify_docs.py exit: {docs_exit}")
    print(f"  verify_e2e.py  exit: {e2e_exit}")

    # Success path
    if docs_exit == 0 and e2e_exit == 0:
        state["status"] = "success"
        state["stop_reason"] = "success"
        write_state(state, brief="All verifiers passed.")
        print("\n✅ SUCCESS — both verifiers passed. Loop complete.")
        return 2

    # Compute no-progress hash
    new_hash = hash_failures(summary)
    state["failing_files_hash"] = new_hash

    # No-progress check (only after first iteration)
    if iteration > 1 and new_hash == state["previous_failing_files_hash"]:
        state["status"] = "escalated"
        write_state(state, brief=summary)
        write_escalation(state, "no_progress", summary)
        return 1

    # Max iterations check
    if iteration > MAX_ITERATIONS:
        state["status"] = "escalated"
        write_state(state, brief=summary)
        write_escalation(state, "max_iterations", summary)
        return 1

    # Continue — write brief for Claude
    brief = (
        f"Iteration {iteration}/{MAX_ITERATIONS}. "
        f"Failures remain. Act as Supervisor: coordinate your team of specialized architects "
        f"(Solutions Architect, Software Architect, Security Reviewer) to resolve the issues below. "
        f"Consolidate their changes and present the final merged diff array. "
        f"Then run `python3 agent_harness.py --prepare` again.\n\n"
        f"{summary}"
    )
    state["status"] = "running"
    write_state(state, brief=brief)

    print(f"\n📋 Brief written to agent/STATE.md")
    print(f"\nVerifier failures to fix:\n{summary}\n")
    print("→ Claude: act as Supervisor, coordinate the team to fix the issues, then run --prepare again.")
    return 0


def cmd_reset() -> int:
    reset_state()
    return 0


def cmd_status() -> int:
    if not STATE_FILE.exists():
        print("No STATE.md found. Run: python3 agent_harness.py --reset")
        return 1
    print(STATE_FILE.read_text(encoding="utf-8"))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Documentation loop state harness")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", action="store_true",
                       help="Run verifiers, write STATE.md brief, return exit code")
    group.add_argument("--reset", action="store_true",
                       help="Reset STATE.md for a fresh run")
    group.add_argument("--status", action="store_true",
                       help="Print current STATE.md")
    args = parser.parse_args()

    if args.prepare:
        sys.exit(cmd_prepare())
    elif args.reset:
        sys.exit(cmd_reset())
    elif args.status:
        sys.exit(cmd_status())


if __name__ == "__main__":
    main()
