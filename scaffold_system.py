#!/usr/bin/env python3
"""
scaffold_system.py — Create a new system / bounded-context folder from the template.

Usage:
  python3 scaffold_system.py <system-name>
  python3 scaffold_system.py <system-name> --title "Human-Readable Title"

Examples:
  python3 scaffold_system.py payments
  python3 scaffold_system.py order-management --title "Order Management"

Creates:
  architecture/systems/<system-name>/
  architecture/systems/<system-name>/index.md   (pre-filled from system-template)
  architecture/systems/<system-name>/components/ (empty, for future component docs)
"""

import re
import sys
import datetime
from pathlib import Path
from shutil import copytree

WORKSPACE_ROOT = Path(__file__).parent.resolve()
TEMPLATE_DIR = WORKSPACE_ROOT / "architecture" / "systems" / "system-template"
SYSTEMS_DIR = WORKSPACE_ROOT / "architecture" / "systems"


def slugify(name: str) -> str:
    """Normalize to lowercase-hyphenated slug."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')


def title_case(slug: str) -> str:
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print("Usage: python3 scaffold_system.py <system-name> [--title \"Human Title\"]")
        sys.exit(1)

    raw_name = args[0]
    slug = slugify(raw_name)
    if not slug:
        print(f"Error: '{raw_name}' produces an empty slug after normalization.")
        sys.exit(1)

    # Optional --title flag
    title = None
    if "--title" in args:
        idx = args.index("--title")
        if idx + 1 < len(args):
            title = args[idx + 1]
    if not title:
        title = title_case(slug)

    target_dir = SYSTEMS_DIR / slug
    if target_dir.exists():
        print(f"Error: architecture/systems/{slug}/ already exists.")
        sys.exit(1)

    if not TEMPLATE_DIR.exists():
        print(f"Error: system-template not found at {TEMPLATE_DIR}")
        sys.exit(1)

    # Copy template
    copytree(str(TEMPLATE_DIR), str(target_dir))

    # Patch index.md
    index_path = target_dir / "index.md"
    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
        today = datetime.date.today().isoformat()

        # Replace the generic H1 title
        content = re.sub(r'^# System Template', f'# {title}', content, count=1, flags=re.MULTILINE)

        # Set Last Updated to today
        content = re.sub(
            r'(## Last Updated\s*\n)\s*YYYY-MM-DD',
            f'\\g<1>{today}',
            content,
            count=1,
        )

        # Fix the glossary relative path depth:
        # system-template uses ../../../glossary.md (3 levels up)
        # architecture/systems/<slug>/ is also 3 levels from root — same depth, no change needed.

        index_path.write_text(content, encoding="utf-8")

    print(f"✅ Created: architecture/systems/{slug}/")
    print(f"   Title:   {title}")
    print(f"   Next: edit architecture/systems/{slug}/index.md to fill in purpose, scope, and dependencies.")
    print(f"   Then: link to it from architecture/views/logical-view.md and architecture/index.md.")


if __name__ == "__main__":
    main()
