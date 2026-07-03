#!/usr/bin/env python3
"""
verify_coverage.py — Architectural coverage and gap inventory tool.

Informational management view — does NOT fail CI (exits 0 always).
"""

import datetime
import re
import sys
from pathlib import Path
from collections import defaultdict

from audit_ignore import is_audit_ignored, load_audit_ignore_patterns

WORKSPACE_ROOT = Path(__file__).parent.resolve()
STALE_THRESHOLD_DAYS = 30


def collect_markdown_files() -> list[Path]:
    patterns = load_audit_ignore_patterns(WORKSPACE_ROOT)
    files = []
    for path in sorted(WORKSPACE_ROOT.rglob("*.md")):
        if is_audit_ignored(path, WORKSPACE_ROOT, patterns):
            continue
        if path.name.startswith(("~", ".")):
            continue
        files.append(path)
    return files


def strip_code_blocks(content: str) -> str:
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`\n]+`', '', content)
    return content


def extract_arch_gaps(file_path: Path) -> list[dict]:
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    content = strip_code_blocks(raw)
    gaps = []
    pattern = re.compile(r'<!--\s*ARCH-GAP:\s*(.*?)-->', re.DOTALL)
    for match in pattern.finditer(content):
        raw = match.group(1).strip()
        owner_match = re.search(r'\[?Owner:\s*([^\].\n>]+)\]?', raw, re.IGNORECASE)
        owner = owner_match.group(1).strip() if owner_match else "UNSPECIFIED — required"
        desc = re.sub(r'\s*\[?Owner:\s*[^\].\n>]+\]?\.?', '', raw).strip().rstrip('.')
        desc = re.sub(r'\s+', ' ', desc)
        gaps.append({
            'file': str(file_path.relative_to(WORKSPACE_ROOT)),
            'description': desc[:140] if len(desc) > 140 else desc,
            'owner': owner,
        })
    return gaps


def extract_header_value(content: str, header: str) -> str | None:
    lines = content.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f"## {header}" or stripped.startswith(f"## {header}:"):
            if ":" in stripped:
                return stripped.split(":", 1)[1].strip()
            for j in range(i + 1, min(i + 4, len(lines))):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#") and not next_line.startswith("<!--"):
                    return next_line
    return None


def days_since(date_str: str) -> int | None:
    try:
        date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        return (datetime.date.today() - date).days
    except ValueError:
        return None


def check_system_inventory() -> tuple[list[str], list[str]]:
    issues = []
    ok_list = []
    systems_dir = WORKSPACE_ROOT / "architecture" / "systems"
    if not systems_dir.exists():
        return (["architecture/systems/ directory does not exist"], [])

    system_dirs = sorted(f for f in systems_dir.iterdir() if f.is_dir() and f.name != "system-template")
    if not system_dirs:
        return (["No system folders found under architecture/systems/ (only system-template exists)"], ok_list)

    for folder in system_dirs:
        index = folder / "index.md"
        if not index.exists():
            issues.append(f"MISSING index.md: architecture/systems/{folder.name}/")
            continue
        try:
            content = index.read_text(encoding="utf-8")
        except Exception:
            issues.append(f"UNREADABLE index.md: architecture/systems/{folder.name}/")
            continue

        non_placeholder_lines = [
            ln for ln in content.splitlines()
            if ln.strip()
            and not ln.strip().startswith("#")
            and ln.strip() not in {"TBD", "---"}
            and "PENDING_DISCOVERY" not in ln
            and "AI_HINT" not in ln
        ]
        if len(non_placeholder_lines) < 3:
            issues.append(f"STUB (unpopulated): architecture/systems/{folder.name}/index.md")
        else:
            ok_list.append(f"architecture/systems/{folder.name}/")

    return (issues, ok_list)


def check_adr_sequence() -> list[str]:
    issues = []
    decisions_dir = WORKSPACE_ROOT / "decisions"
    if not decisions_dir.exists():
        return ["decisions/ directory does not exist"]

    adr_files = sorted(
        f for f in decisions_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and re.match(r'^\d{4}-', f.name)
    )
    if not adr_files:
        return ["No ADR files found in decisions/"]

    expected = 1
    for f in adr_files:
        num_match = re.match(r'^(\d{4})-', f.name)
        if num_match:
            actual = int(num_match.group(1))
            if actual != expected:
                issues.append(f"ADR sequence gap: expected {expected:04d}, found {actual:04d} ({f.name})")
            expected = actual + 1

    return issues


def run_report(gaps_only: bool = False, stale_only: bool = False, systems_only: bool = False):
    files = collect_markdown_files()
    print("verify_coverage.py — Architectural Coverage Report")
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Date:      {datetime.date.today()}")
    print(f"Files:     {len(files)} active markdown files scanned")
    print("=" * 70)

    if not stale_only and not systems_only:
        all_gaps: list[dict] = []
        for f in files:
            all_gaps.extend(extract_arch_gaps(f))

        by_owner: dict[str, list[dict]] = defaultdict(list)
        for gap in all_gaps:
            by_owner[gap['owner']].append(gap)

        unowned = by_owner.pop("UNSPECIFIED — required", [])
        print(f"\n### ARCH-GAP Inventory ({len(all_gaps)} open gaps)\n")
        if unowned:
            print(f"  ⚠  GAPS WITHOUT OWNER ({len(unowned)}) — owner field is required:")
            for gap in unowned:
                print(f"    [{gap['file']}]  {gap['description']}")
            print()
        if not all_gaps:
            print("  No ARCH-GAP tags found.")
        else:
            for owner in sorted(by_owner.keys()):
                owner_gaps = by_owner[owner]
                print(f"  Owner: {owner} ({len(owner_gaps)} gap{'s' if len(owner_gaps) != 1 else ''})")
                for gap in owner_gaps:
                    print(f"    [{gap['file']}]")
                    print(f"      {gap['description']}")
                print()

    if not gaps_only and not stale_only and not systems_only:
        status_counts: dict[str, int] = defaultdict(int)
        status_unknown = []
        for f in files:
            try:
                content = f.read_text(encoding="utf-8")
            except Exception:
                continue
            val = extract_header_value(content, "Document Status")
            if val:
                status_counts[val] += 1
            else:
                status_unknown.append(str(f.relative_to(WORKSPACE_ROOT)))

        print("=" * 70)
        print("\n### Document Status Distribution\n")
        total = sum(status_counts.values())
        for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
            bar = "█" * count
            pct = f"{count/total*100:.0f}%" if total else "0%"
            print(f"  {status:<12} {count:>3}  {pct:>4}  {bar}")
        if status_unknown:
            print(f"\n  ⚠  Missing status header ({len(status_unknown)} files):")
            for path in status_unknown:
                print(f"    {path}")

    if not gaps_only and not systems_only:
        stale: list[tuple[int, str, str]] = []
        for f in files:
            try:
                content = f.read_text(encoding="utf-8")
            except Exception:
                continue
            date_val = extract_header_value(content, "Last Updated")
            if not date_val:
                continue
            age = days_since(date_val)
            if age is not None and age > STALE_THRESHOLD_DAYS:
                status = extract_header_value(content, "Document Status") or "Unknown"
                stale.append((age, str(f.relative_to(WORKSPACE_ROOT)), status))

        stale.sort(reverse=True)
        print("=" * 70)
        print(f"\n### Stale Documents (Last Updated > {STALE_THRESHOLD_DAYS} days ago)\n")
        if not stale:
            print(f"  All documents updated within the last {STALE_THRESHOLD_DAYS} days.")
        else:
            for age, path, status in stale:
                print(f"  {age:>4}d  [{status:<10}]  {path}")

    if not gaps_only and not stale_only:
        issues, ok_list = check_system_inventory()
        print("=" * 70)
        print("\n### System Folder Inventory\n")
        for item in ok_list:
            print(f"  ✅  {item}")
        for issue in issues:
            print(f"  ⚠   {issue}")
        if not issues and not ok_list:
            print("  No system folders found.")

    if not gaps_only and not stale_only and not systems_only:
        adr_issues = check_adr_sequence()
        print("=" * 70)
        print("\n### ADR Sequence Check\n")
        if not adr_issues:
            print("  ADR numbering is sequential with no gaps.")
        else:
            for issue in adr_issues:
                print(f"  ⚠  {issue}")

    print("\n" + "=" * 70)
    print("Informational report only — exits 0. Run verify_docs.py for hard CI validation.")
    print("Run verify_e2e.py for cross-repo link and orphan audit.")


if __name__ == "__main__":
    args = set(sys.argv[1:])
    run_report(
        gaps_only="--gaps-only" in args,
        stale_only="--stale-only" in args,
        systems_only="--systems-only" in args,
    )
