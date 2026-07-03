#!/usr/bin/env python3
"""Shared documentation-audit ignore helpers."""

from __future__ import annotations

from pathlib import Path

DEFAULT_IGNORE_FILE = ".doc-audit-ignore"


def load_audit_ignore_patterns(workspace_root: Path, ignore_file: str = DEFAULT_IGNORE_FILE) -> list[str]:
    """Load repository-relative audit-ignore patterns."""
    path = workspace_root / ignore_file
    if not path.exists():
        return []

    patterns: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        patterns.append(item)
    return patterns


def normalize_pattern(pattern: str) -> str:
    """Normalize only repository-relative syntax without stripping dot-prefixed names."""
    normalized = pattern.strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_audit_ignored(path: Path, workspace_root: Path, patterns: list[str]) -> bool:
    """Return True when a path should be excluded from architecture-document audits."""
    try:
        rel_path = path.relative_to(workspace_root)
    except ValueError:
        return False

    rel_posix = rel_path.as_posix()
    rel_parts = rel_path.parts

    for pattern in patterns:
        normalized = normalize_pattern(pattern)
        if not normalized:
            continue

        is_dir_pattern = normalized.endswith("/")
        normalized = normalized.rstrip("/")

        if "/" in normalized:
            if rel_posix == normalized or rel_posix.startswith(normalized + "/"):
                return True
            if is_dir_pattern and rel_posix.startswith(normalized):
                return True
            continue

        if normalized in rel_parts or path.name == normalized:
            return True

    return False
