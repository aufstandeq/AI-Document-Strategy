#!/usr/bin/env python3
"""
verify_e2e.py — Cross-repository architectural audit. CI gate.

Runs checks that span multiple files and cannot be done per-file in verify_docs.py:
  1. Orphan detection — markdown files with no inbound links from any other doc
  2. ARCH-GAP owner enforcement — gaps without an Owner: field fail the build
  3. Glossary reference enforcement — every active doc must link to glossary.md
  4. ADR sequence integrity — no numbering gaps in decisions/
  5. Cross-system reference validation — systems/ links referenced in view files exist on disk

Exit codes:
  0 — all checks passed (or only warnings)
  1 — one or more hard failures found

Usage:
  python3 verify_e2e.py
  python3 verify_e2e.py --warn-only   (report failures but exit 0; useful for initial adoption)
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

WORKSPACE_ROOT = Path(__file__).parent.resolve()

EXCLUDE_DIR_PARTS = {
    ".git", ".github", "__pycache__",
    "archive", "TEMP",
}

# Directories whose files are excluded from orphan checking
# (template stubs and components placeholders are intentionally unlinked)
ORPHAN_EXCLUDE_PARTS = EXCLUDE_DIR_PARTS | {"system-template"}

# Files that are allowed to be orphans (entry points / root docs)
ORPHAN_ALLOWLIST = {
    "README.md",
    "glossary.md",
    "how-to-start.md",
    "onboarding-dev.md",
}

VIEW_FILES = {
    "logical-view.md",
    "deployment-view.md",
    "data-view.md",
    "security-view.md",
    "integration-view.md",
}


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files(exclude_extra: set[str] | None = None) -> list[Path]:
    exclude = EXCLUDE_DIR_PARTS | (exclude_extra or set())
    files = []
    for path in sorted(WORKSPACE_ROOT.rglob("*.md")):
        rel_parts = path.relative_to(WORKSPACE_ROOT).parts
        if any(part in exclude for part in rel_parts):
            continue
        if path.name.startswith(("~", ".")):
            continue
        files.append(path)
    return files


# ---------------------------------------------------------------------------
# Link extraction (outbound)
# ---------------------------------------------------------------------------

def extract_outbound_links(file_path: Path) -> list[str]:
    """Return all relative link targets from a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Strip code blocks and HTML comments before link extraction
    clean_lines = []
    in_code = False
    in_comment = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if stripped.startswith("<!--"):
            in_comment = True
        if "-->" in stripped:
            in_comment = False
            continue
        if in_code or in_comment:
            continue
        clean_lines.append(re.sub(r'`[^`]*`', '', line))

    clean = "\n".join(clean_lines)
    links = []
    for _, path in re.findall(r'\[([^\]]*)\]\(([^)]*)\)', clean):
        path = path.strip().split("#")[0]  # drop anchors
        if path and not path.startswith(("http://", "https://", "mailto:")):
            links.append(path)
    return links


# ---------------------------------------------------------------------------
# Build inbound link index
# ---------------------------------------------------------------------------

def build_inbound_index(all_files: list[Path]) -> dict[Path, list[Path]]:
    """Map each file to the list of files that link to it."""
    inbound: dict[Path, list[Path]] = defaultdict(list)
    for source in all_files:
        for link in extract_outbound_links(source):
            resolved = (source.parent / link).resolve()
            inbound[resolved].append(source)
    return inbound


# ---------------------------------------------------------------------------
# Check 1: Orphan detection
# ---------------------------------------------------------------------------

def check_orphans(all_files: list[Path], inbound: dict[Path, list[Path]]) -> list[str]:
    errors = []
    for f in all_files:
        rel_parts = f.relative_to(WORKSPACE_ROOT).parts
        if any(part in ORPHAN_EXCLUDE_PARTS for part in rel_parts):
            continue
        if f.name in ORPHAN_ALLOWLIST:
            continue
        if not inbound.get(f):
            errors.append(f"ORPHAN (no inbound links): {f.relative_to(WORKSPACE_ROOT)}")
    return errors


# ---------------------------------------------------------------------------
# Check 2: ARCH-GAP owner enforcement
# ---------------------------------------------------------------------------

def strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks and inline code so examples don't trigger checks."""
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`\n]+`', '', content)
    return content


def check_arch_gap_owners(all_files: list[Path]) -> list[str]:
    errors = []
    pattern = re.compile(r'<!--\s*ARCH-GAP:\s*(.*?)-->', re.DOTALL)
    owner_re = re.compile(r'\[?Owner:\s*([^\].\n>]+)\]?', re.IGNORECASE)
    for f in all_files:
        try:
            raw = f.read_text(encoding="utf-8")
        except Exception:
            continue
        content = strip_code_blocks(raw)
        for match in pattern.finditer(content):
            raw = match.group(1).strip()
            if not owner_re.search(raw):
                desc = re.sub(r'\s+', ' ', raw)[:80]
                errors.append(
                    f"ARCH-GAP missing Owner: [{f.relative_to(WORKSPACE_ROOT)}] "
                    f"— \"{desc}...\""
                )
    return errors


# ---------------------------------------------------------------------------
# Check 3: Glossary reference enforcement
# ---------------------------------------------------------------------------

def check_glossary_links(all_files: list[Path]) -> list[str]:
    """Every active document (outside system-template) must link to glossary.md."""
    errors = []
    # Root-level glossary files are themselves exempt
    exempt_names = {"glossary.md", "README.md"}
    for f in all_files:
        rel_parts = f.relative_to(WORKSPACE_ROOT).parts
        if "system-template" in rel_parts:
            continue
        if f.name in exempt_names:
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
        # Check for any link whose path ends in 'glossary.md'
        links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
        has_glossary = any("glossary.md" in lpath for _, lpath in links)
        if not has_glossary:
            errors.append(
                f"MISSING GLOSSARY LINK: {f.relative_to(WORKSPACE_ROOT)}"
            )
    return errors


# ---------------------------------------------------------------------------
# Check 4: ADR sequence integrity
# ---------------------------------------------------------------------------

def check_adr_sequence() -> list[str]:
    errors = []
    decisions_dir = WORKSPACE_ROOT / "decisions"
    if not decisions_dir.exists():
        return ["decisions/ directory missing"]
    adr_files = sorted(
        f for f in decisions_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and re.match(r'^\d{4}-', f.name)
    )
    if not adr_files:
        return []  # No ADRs yet — not an error for a fresh repo
    expected = 1
    for f in adr_files:
        m = re.match(r'^(\d{4})-', f.name)
        if m:
            actual = int(m.group(1))
            if actual != expected:
                errors.append(
                    f"ADR sequence gap: expected {expected:04d}, got {actual:04d} ({f.name})"
                )
            expected = actual + 1
    return errors


# ---------------------------------------------------------------------------
# Check 5: Cross-system reference validation
# ---------------------------------------------------------------------------

def check_cross_system_refs(all_files: list[Path]) -> list[str]:
    """Links in view files that point to systems/ paths must resolve on disk."""
    errors = []
    view_files = [f for f in all_files if f.name in VIEW_FILES]
    for f in view_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for _, path in re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content):
            if "systems/" in path and not path.startswith(("http://", "https://")):
                resolved = (f.parent / path.split("#")[0]).resolve()
                if not resolved.exists():
                    errors.append(
                        f"BROKEN SYSTEM LINK in {f.relative_to(WORKSPACE_ROOT)}: "
                        f"'{path}' does not exist"
                    )
    return errors


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_audit(warn_only: bool = False) -> bool:
    """Run all cross-repo checks. Returns True if all passed."""
    all_files = collect_files()
    audit_files = collect_files(exclude_extra=ORPHAN_EXCLUDE_PARTS - EXCLUDE_DIR_PARTS)
    inbound = build_inbound_index(all_files)

    results: list[tuple[str, list[str]]] = [
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
            for e in errors:
                print(f"   {e}")
            total_failures += len(errors)
        else:
            print(f"\n✅ {check_name} — passed")

    print("\n" + "=" * 70)
    if total_failures == 0:
        print("All cross-repository checks passed.")
        return True
    else:
        mode = "WARNINGS" if warn_only else "FAILURES"
        print(f"{total_failures} {mode} found.")
        if not warn_only:
            print("Fix the issues above before merging.")
        return warn_only  # True (pass) in warn-only mode, False (fail) otherwise


if __name__ == "__main__":
    warn_only = "--warn-only" in sys.argv
    passed = run_audit(warn_only=warn_only)
    sys.exit(0 if passed else 1)
