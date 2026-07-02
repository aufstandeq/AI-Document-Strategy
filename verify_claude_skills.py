#!/usr/bin/env python3
"""
verify_claude_skills.py — Validate project-scoped Claude skill structure.

This verifier checks `.claude/skills/**` as runtime skill configuration.
It is intentionally separate from architecture-document validation because skill files
are tracked repository assets, but they are not active architecture documentation.

Checks:
  1. Skill folders use kebab-case names.
  2. Each skill folder contains required `SKILL.md`.
  3. `SKILL.md` contains YAML-style frontmatter bounded by `---`.
  4. Frontmatter includes required `name` and `description` fields.
  5. Frontmatter `name` matches the folder name.
  6. `description` includes trigger context by using `Use when`.
  7. Individual skill folders do not contain `README.md`.
  8. Parent-level README.md and PLAN.md are allowed.
  9. Parent-level support directories such as tests/ are allowed but are not treated as skills.

Exit codes:
  0 — all checks passed
  1 — one or more hard failures found

Usage:
  python3 verify_claude_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()
SKILLS_DIR = WORKSPACE_ROOT / ".claude" / "skills"
PARENT_ALLOWED_FILES = {"README.md", "PLAN.md"}
PARENT_ALLOWED_DIRS = {"tests"}
REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(content: str) -> tuple[dict[str, str], list[str]]:
    """Parse the simple top-level key/value frontmatter fields used by skills."""
    errors: list[str] = []
    if not content.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter delimiter '---'"]

    lines = content.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return {}, ["SKILL.md frontmatter is missing closing '---' delimiter"]

    fields: dict[str, str] = {}
    for line in lines[1:end_idx]:
        if not line.strip() or line.startswith("  ") or line.startswith("-"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    return fields, errors


def validate_skill_folder(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    rel_dir = skill_dir.relative_to(WORKSPACE_ROOT)
    folder_name = skill_dir.name

    if not KEBAB_CASE_RE.match(folder_name):
        errors.append(f"{rel_dir}: skill folder name must be kebab-case")

    readme_path = skill_dir / "README.md"
    if readme_path.exists():
        errors.append(f"{readme_path.relative_to(WORKSPACE_ROOT)}: README.md is not allowed inside an individual skill folder")

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        errors.append(f"{rel_dir}: missing required SKILL.md")
        return errors

    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"{skill_path.relative_to(WORKSPACE_ROOT)}: unreadable file: {exc}")
        return errors

    frontmatter, fm_errors = parse_frontmatter(content)
    for err in fm_errors:
        errors.append(f"{skill_path.relative_to(WORKSPACE_ROOT)}: {err}")

    for field in sorted(REQUIRED_FRONTMATTER_FIELDS):
        if not frontmatter.get(field):
            errors.append(f"{skill_path.relative_to(WORKSPACE_ROOT)}: missing required frontmatter field '{field}'")

    skill_name = frontmatter.get("name")
    if skill_name and skill_name != folder_name:
        errors.append(
            f"{skill_path.relative_to(WORKSPACE_ROOT)}: frontmatter name '{skill_name}' must match folder name '{folder_name}'"
        )

    description = frontmatter.get("description", "")
    if description and "Use when" not in description:
        errors.append(
            f"{skill_path.relative_to(WORKSPACE_ROOT)}: description must include trigger context using 'Use when'"
        )

    if "# " not in content:
        errors.append(f"{skill_path.relative_to(WORKSPACE_ROOT)}: missing H1 body heading")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"❌ Missing skills directory: {SKILLS_DIR.relative_to(WORKSPACE_ROOT)}")
        return 1

    errors: list[str] = []
    skill_dirs: list[Path] = []
    support_dirs: list[Path] = []

    for path in sorted(SKILLS_DIR.iterdir()):
        if path.is_dir() and path.name in PARENT_ALLOWED_DIRS:
            support_dirs.append(path)
        elif path.is_dir():
            skill_dirs.append(path)
        elif path.is_file() and path.name not in PARENT_ALLOWED_FILES:
            errors.append(
                f"{path.relative_to(WORKSPACE_ROOT)}: unexpected parent-level file; allowed files are {sorted(PARENT_ALLOWED_FILES)}"
            )

    if not skill_dirs:
        errors.append("No skill folders found under .claude/skills/")

    for skill_dir in skill_dirs:
        errors.extend(validate_skill_folder(skill_dir))

    print("verify_claude_skills.py — Claude Skills Validation")
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Skills scanned: {len(skill_dirs)}")
    print(f"Support dirs scanned: {len(support_dirs)}")
    print("=" * 70)

    if errors:
        print("\n❌ Skill validation failures:")
        for err in errors:
            print(f"   {err}")
        print("\nFix the skill issues above before merging.")
        return 1

    print("\n✅ All Claude skill validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
