#!/usr/bin/env python3
"""Cross-repository architecture documentation audit."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()

EXCLUDE_DIR_PARTS = {
    ".git",
    ".github",
    ".agents",
    ".claude",
    "__pycache__",
    "archive",
    "TEMP",
    "Reference",
}

ORPHAN_EXCLUDE_PARTS = EXCLUDE_DIR_PARTS | {"system-template"}
ORPHAN_ALLOWLIST = {
    "README.md",
    "glossary.md",
    "how-to-start.md",
    "onboarding-dev.md",
    "STATE.md",
    "CLAUDE.md",
}
VIEW_FILES = {
    "logical-view.md",
    "deployment-view.md",
    "data-view.md",
    "security-view.md",
    "integration-view.md",
}


def collect_files(exclude_extra: set[str] | None = None) -> list[Path]:
    exclude = EXCLUDE_DIR_PARTS | (exclude_extra or set())
    files: list[Path] = []
    for path in sorted(WORKSPACE_ROOT.rglob("*.md")):
        rel_parts = path.relative_to(WORKSPACE_ROOT).parts
        if any(part in exclude for part in rel_parts):
            continue
        if path.name.startswith(("~", ".")):
            continue
        files.append(path)
    return files


def strip_ignored_text(content: str) -> str:
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    content = re.sub(r"`[^`\n]+`", "", content)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    return content


def extract_outbound_links(file_path: Path) -> list[str]:
    try:
        content = strip_ignored_text(file_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    links: list[str] = []
    for _, target in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", content):
        target = target.strip().split("#", 1)[0]
        if target and not target.startswith(("http://", "https://", "mailto:")):
            links.append(target)
    return links


def build_inbound_index(all_files: list[Path]) -> dict[Path, list[Path]]:
    inbound: dict[Path, list[Path]] = defaultdict(list)
    for source in all_files:
        for link in extract_outbound_links(source):
            inbound[(source.parent / link).resolve()].append(source)
    return inbound


def check_orphans(all_files: list[Path], inbound: dict[Path, list[Path]]) -> list[str]:
    errors: list[str] = []
    for file_path in all_files:
        rel_parts = file_path.relative_to(WORKSPACE_ROOT).parts
        if any(part in ORPHAN_EXCLUDE_PARTS for part in rel_parts):
            continue
        if file_path.name in ORPHAN_ALLOWLIST:
            continue
        if not inbound.get(file_path.resolve()):
            errors.append(f"ORPHAN (no inbound links): {file_path.relative_to(WORKSPACE_ROOT)}")
    return errors


def check_arch_gap_owners(all_files: list[Path]) -> list[str]:
    errors: list[str] = []
    gap_re = re.compile(r"<!--\s*ARCH-GAP:\s*(.*?)-->", re.DOTALL)
    owner_re = re.compile(r"\[?Owner:\s*([^\].\n>]+)\]?", re.IGNORECASE)
    for file_path in all_files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        content = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)
        content = re.sub(r"`[^`\n]+`", "", content)
        for match in gap_re.finditer(content):
            body = match.group(1).strip()
            if not owner_re.search(body):
                desc = re.sub(r"\s+", " ", body)[:80]
                errors.append(
                    f"ARCH-GAP missing Owner: [{file_path.relative_to(WORKSPACE_ROOT)}] — \"{desc}...\""
                )
    return errors


def check_glossary_links(all_files: list[Path]) -> list[str]:
    errors: list[str] = []
    exempt_names = {"glossary.md", "README.md", "STATE.md", "CLAUDE.md"}
    for file_path in all_files:
        rel_parts = file_path.relative_to(WORKSPACE_ROOT).parts
        if "system-template" in rel_parts or file_path.name in exempt_names:
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        links = re.findall(r"\[([^\]]*)\]\(([^)]*)\)", content)
        if not any("glossary.md" in target for _, target in links):
            errors.append(f"MISSING GLOSSARY LINK: {file_path.relative_to(WORKSPACE_ROOT)}")
    return errors


def check_adr_sequence() -> list[str]:
    decisions_dir = WORKSPACE_ROOT / "decisions"
    if not decisions_dir.exists():
        return ["decisions/ directory missing"]
    adr_files = sorted(
        file_path
        for file_path in decisions_dir.iterdir()
        if file_path.is_file() and file_path.suffix == ".md" and re.match(r"^\d{4}-", file_path.name)
    )
    errors: list[str] = []
    expected = 1
    for file_path in adr_files:
        match = re.match(r"^(\d{4})-", file_path.name)
        if not match:
            continue
        actual = int(match.group(1))
        if actual != expected:
            errors.append(f"ADR sequence gap: expected {expected:04d}, got {actual:04d} ({file_path.name})")
        expected = actual + 1
    return errors


def check_cross_system_refs(all_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for file_path in [f for f in all_files if f.name in VIEW_FILES]:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        for _, target in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", content):
            if "systems/" not in target or target.startswith(("http://", "https://")):
                continue
            resolved = (file_path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                errors.append(
                    f"BROKEN SYSTEM LINK in {file_path.relative_to(WORKSPACE_ROOT)}: '{target}' does not exist"
                )
    return errors


def run_audit(warn_only: bool = False) -> bool:
    all_files = collect_files()
    inbound = build_inbound_index(all_files)
    results = [
        ("Orphan Detection", check_orphans(all_files, inbound)),
        ("ARCH-GAP Owner Enforcement", check_arch_gap_owners(all_files)),
        ("Glossary Link Enforcement", check_glossary_links(all_files)),
        ("ADR Sequence Integrity", check_adr_sequence()),
        ("Cross-System Reference Validation", check_cross_system_refs(all_files)),
    ]

    print("verify_e2e.py — Cross-Repository Audit")
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Files scanned: {len(all_files)}")
    print("=" * 70)

    total_failures = 0
    for check_name, errors in results:
        if errors:
            print(f"\n❌ {check_name} ({len(errors)} issue{'s' if len(errors) != 1 else ''}):")
            for error in errors:
                print(f"   {error}")
            total_failures += len(errors)
        else:
            print(f"\n✅ {check_name} — passed")

    print("\n" + "=" * 70)
    if total_failures == 0:
        print("All cross-repository checks passed.")
        return True

    mode = "WARNINGS" if warn_only else "FAILURES"
    print(f"{total_failures} {mode} found.")
    if not warn_only:
        print("Fix the issues above before merging.")
    return warn_only


if __name__ == "__main__":
    if "--workspace" in sys.argv:
        idx = sys.argv.index("--workspace")
        if idx + 1 < len(sys.argv):
            WORKSPACE_ROOT = Path(sys.argv[idx + 1]).resolve()
    passed = run_audit(warn_only="--warn-only" in sys.argv)
    sys.exit(0 if passed else 1)
