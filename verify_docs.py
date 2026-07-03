#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

from audit_ignore import is_audit_ignored, load_audit_ignore_patterns

WORKSPACE_ROOT = Path(__file__).parent.resolve()
ALLOWED_STATUSES = {"Draft", "In Review", "Approved", "Deprecated"}


def check_headers(file_path: Path, content: str) -> list:
    errors = []
    lines = []
    in_code_block = False
    in_comment = False

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if stripped.startswith("<!--"):
            in_comment = True
        if "-->" in stripped:
            in_comment = False
            continue
        if in_code_block or in_comment:
            continue
        lines.append(re.sub(r'`[^`]*`', '', line))

    if not any(line.strip().startswith("# ") for line in lines):
        errors.append("Missing H1 title ('# [Document Title]')")

    headers = {
        "Document Status": None,
        "Purpose": None,
        "Owner": None,
        "Last Updated": None,
    }

    for key in headers:
        header_str = f"## {key}"
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(header_str):
                if ":" in stripped:
                    headers[key] = stripped.split(":", 1)[1].strip()
                elif " - " in stripped:
                    headers[key] = stripped.split(" - ", 1)[1].strip()
                elif i + 1 < len(lines):
                    next_val = lines[i + 1].strip()
                    if next_val and not next_val.startswith("#"):
                        headers[key] = next_val
                break

    for key, val in headers.items():
        if val is None:
            errors.append(f"Missing or malformed header: '## {key}'")
        elif key == "Document Status" and val not in ALLOWED_STATUSES:
            errors.append(f"Invalid Document Status value '{val}'. Allowed values are: {ALLOWED_STATUSES}")

    return errors


def check_anchor_in_file(file_path: Path, anchor: str) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return False

    def slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        return re.sub(r'[\s_]+', '-', text)

    target_slug = slugify(anchor)
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            if slugify(stripped.lstrip("#").strip()) == target_slug:
                return True
    return False


def check_links(file_path: Path, content: str) -> list:
    errors = []
    lines = []
    in_code_block = False
    in_comment = False

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if stripped.startswith("<!--"):
            in_comment = True
        if "-->" in stripped:
            in_comment = False
            continue
        if in_code_block or in_comment:
            continue
        lines.append(re.sub(r'`[^`]*`', '', line))

    clean_content = "\n".join(lines)
    paths_to_check = []

    for _, path in re.findall(r'\[([^\]]*)\]\(([^)]*)\)', clean_content):
        paths_to_check.append(path.strip())
    for path in re.findall(r'^\[[^\]]+\]:\s*([^\s]+)', clean_content, re.MULTILINE):
        paths_to_check.append(path.strip())
    for path in re.findall(r'<([^>:\s]+)>', clean_content):
        if not path.startswith(("http", "https", "mailto", "a ", "/a", "p>", "h1", "h2", "h3", "h4", "div", "span", "img", "table", "tr", "td", "th", "tbody", "thead")):
            paths_to_check.append(path.strip())
    for path in re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', clean_content):
        paths_to_check.append(path.strip())

    for path in paths_to_check:
        if path.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if path.startswith("/") or re.match(r'^[a-zA-Z]:\\', path):
            errors.append(f"Absolute path link detected: '{path}' (must be relative)")
            continue

        anchor = None
        clean_path = path
        if "#" in path:
            clean_path, anchor = path.split("#", 1)

        if not clean_path:
            if anchor and not check_anchor_in_file(file_path, anchor):
                errors.append(f"Broken internal anchor link: '{path}' (anchor '#{anchor}' not found)")
            continue

        target_path = (file_path.parent / clean_path).resolve()
        if not target_path.exists():
            try:
                rel_target = target_path.relative_to(WORKSPACE_ROOT)
            except ValueError:
                rel_target = target_path
            errors.append(f"Broken relative link: '{path}' (resolved to non-existent '{rel_target}')")
            continue

        if anchor and target_path.suffix.lower() in {".md", ".markdown", ".mdown"}:
            if not check_anchor_in_file(target_path, anchor):
                errors.append(f"Broken anchor link: '{path}' (anchor '#{anchor}' not found in '{clean_path}')")

    return errors


def check_entity_alignment(file_path: Path, content: str) -> list:
    errors = []
    if file_path.name in {"logical-view.md", "deployment-view.md", "data-view.md", "security-view.md", "integration-view.md"}:
        for _, path in re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content):
            if "systems/" in path and not path.startswith(("http://", "https://")):
                target_path = (file_path.parent / path).resolve()
                if not target_path.exists():
                    errors.append(f"System link defined in {file_path.name} does not exist on disk: '{path}'")
    return errors


def collect_markdown_files() -> list[Path]:
    ignore_patterns = load_audit_ignore_patterns(WORKSPACE_ROOT)
    markdown_files = []

    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not is_audit_ignored(root_path / d, WORKSPACE_ROOT, ignore_patterns)]

        if is_audit_ignored(root_path, WORKSPACE_ROOT, ignore_patterns):
            continue

        for file in files:
            path = root_path / file
            if is_audit_ignored(path, WORKSPACE_ROOT, ignore_patterns):
                continue
            if file.startswith("~") or file.startswith("."):
                continue
            if file.lower().endswith((".md", ".markdown", ".mdown")):
                markdown_files.append(path)

    return markdown_files


def main():
    global WORKSPACE_ROOT
    if "--workspace" in sys.argv:
        idx = sys.argv.index("--workspace")
        if idx + 1 < len(sys.argv):
            WORKSPACE_ROOT = Path(sys.argv[idx + 1]).resolve()

    markdown_files = collect_markdown_files()
    has_failures = False

    print(f"Scanning {len(markdown_files)} markdown files for structural rules...\n")

    for file_path in markdown_files:
        rel_path = file_path.relative_to(WORKSPACE_ROOT)
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"❌ Error reading {rel_path}: {exc}")
            has_failures = True
            continue

        file_errors = []
        file_errors.extend(check_headers(file_path, content))
        file_errors.extend(check_links(file_path, content))
        file_errors.extend(check_entity_alignment(file_path, content))

        if file_errors:
            print(f"❌ {rel_path}:")
            for error in file_errors:
                print(f"   - {error}")
            has_failures = True
        else:
            print(f"✅ {rel_path}")

    if has_failures:
        print("\nValidation failed with errors.")
        sys.exit(1)

    print("\nAll structural validations passed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
