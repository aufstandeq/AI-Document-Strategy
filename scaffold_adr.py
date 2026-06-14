#!/usr/bin/env python3
"""
scaffold_adr.py — Create the next sequential Architecture Decision Record.

Usage:
  python3 scaffold_adr.py <decision-title>

Examples:
  python3 scaffold_adr.py "use-postgresql-for-primary-storage"
  python3 scaffold_adr.py "api-versioning-strategy"

Creates:
  decisions/NNNN-<slugified-title>.md

The file is pre-filled with the standard ADR template and the next available
sequence number. Open the file and fill in Context, Decision, and Consequences.
"""

import re
import sys
import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()
DECISIONS_DIR = WORKSPACE_ROOT / "decisions"

ADR_TEMPLATE = """\
# ADR-{num:04d}: {title}

## Document Status
Draft

## Purpose
Record the architectural decision regarding {title_lower}.

## Owner
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Last Updated
{today}

---

See [Glossary](../glossary.md) for definitions of key terms.

---

## Status

Proposed

## Context

<!-- Describe the situation and forces that led to this decision.
     What problem is being solved? What constraints exist?
     What options were considered? -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Decision

<!-- State the decision clearly and directly.
     "We will..." -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## Consequences

### Positive
<!-- Benefits, improvements, simplifications this decision enables. -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

### Negative / Trade-offs
<!-- Costs, risks, or constraints this decision introduces. -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

### Neutral
<!-- Changes in process, tooling, or understanding — neither good nor bad. -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

---

## Related Decisions
<!-- Link to ADRs that this decision depends on or supersedes. -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD

## References
<!-- External references, RFCs, prior art, vendor docs. -->
<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->
TBD
"""


def slugify(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'[\s_]+', '-', title)
    title = re.sub(r'-+', '-', title)
    return title.strip('-')


def next_adr_number(decisions_dir: Path) -> int:
    if not decisions_dir.exists():
        return 1
    existing = sorted(
        int(m.group(1))
        for f in decisions_dir.iterdir()
        if f.is_file() and f.suffix == ".md"
        for m in [re.match(r'^(\d{4})-', f.name)]
        if m
    )
    return (existing[-1] + 1) if existing else 1


def title_from_slug(slug: str) -> str:
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scaffold_adr.py <decision-title>")
        print('Example: python3 scaffold_adr.py "use-postgresql-for-primary-storage"')
        sys.exit(1)

    raw_title = " ".join(sys.argv[1:])
    slug = slugify(raw_title)
    if not slug:
        print(f"Error: '{raw_title}' produces an empty slug after normalization.")
        sys.exit(1)

    num = next_adr_number(DECISIONS_DIR)
    filename = f"{num:04d}-{slug}.md"
    target = DECISIONS_DIR / filename

    if target.exists():
        print(f"Error: {target.relative_to(WORKSPACE_ROOT)} already exists.")
        sys.exit(1)

    DECISIONS_DIR.mkdir(exist_ok=True)

    human_title = title_from_slug(slug)
    today = datetime.date.today().isoformat()

    content = ADR_TEMPLATE.format(
        num=num,
        title=human_title,
        title_lower=human_title.lower(),
        today=today,
    )
    target.write_text(content, encoding="utf-8")

    print(f"✅ Created: decisions/{filename}")
    print(f"   ADR number: {num:04d}")
    print(f"   Next: fill in Context, Decision, and Consequences in the file.")


if __name__ == "__main__":
    main()
