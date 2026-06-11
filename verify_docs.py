#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()

# Allowed values
ALLOWED_STATUSES = {"Draft", "In Review", "Approved", "Deprecated"}

def load_gitignore():
    """Load exclude patterns from .gitignore if it exists."""
    patterns = []
    gitignore_path = WORKSPACE_ROOT / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception:
            pass
    return patterns

def check_headers(file_path: Path, content: str) -> list:
    errors = []
    
    # 1. Clean code blocks, comments, and inline code (AST-aware line parsing)
    lines = []
    in_code_block = False
    in_comment = False
    for line in content.splitlines():
        stripped = line.strip()
        
        # Toggle code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
            
        # Toggle comments
        if stripped.startswith("<!--"):
            in_comment = True
        if "-->" in stripped:
            in_comment = False
            continue
            
        if in_code_block or in_comment:
            continue
            
        # Strip inline code blocks on this line (e.g. `[text](path)`)
        line_clean = re.sub(r'`[^`]*`', '', line)
        lines.append(line_clean)

    # Check H1 title exists
    has_title = any(line.strip().startswith("# ") for line in lines)
    if not has_title:
        errors.append("Missing H1 title ('# [Document Title]')")

    # Find headers and extract values
    headers = {
        "Document Status": None,
        "Purpose": None,
        "Owner": None,
        "Last Updated": None
    }
    
    for key in headers.keys():
        header_str = f"## {key}"
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(header_str):
                # Try inline match (e.g., "## Document Status: Approved" or "## Document Status - Approved")
                if ":" in stripped:
                    headers[key] = stripped.split(":", 1)[1].strip()
                elif " - " in stripped:
                    headers[key] = stripped.split(" - ", 1)[1].strip()
                elif i + 1 < len(lines):
                    # Check next line
                    next_val = lines[i+1].strip()
                    if next_val and not next_val.startswith("#"):
                        headers[key] = next_val
                break

    # Validate the extracted headers
    for key, val in headers.items():
        if val is None:
            errors.append(f"Missing or malformed header: '## {key}'")
        else:
            # Enforce Document Status values
            if key == "Document Status" and val not in ALLOWED_STATUSES:
                errors.append(f"Invalid Document Status value '{val}'. Allowed values are: {ALLOWED_STATUSES}")
                
    return errors

def check_links(file_path: Path, content: str) -> list:
    errors = []
    
    # Clean code blocks, comments, and inline code before matching links
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
            
        # Strip inline code blocks (e.g. `[text](path)`)
        line_clean = re.sub(r'`[^`]*`', '', line)
        lines.append(line_clean)
        
    clean_content = "\n".join(lines)
    paths_to_check = []
    
    # 1. Inline links: [text](path)
    inline_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', clean_content)
    for text, path in inline_links:
        paths_to_check.append(path.strip())
        
    # 2. Reference-style links: [ref]: path
    ref_links = re.findall(r'^\[[^\]]+\]:\s*([^\s]+)', clean_content, re.MULTILINE)
    for path in ref_links:
        paths_to_check.append(path.strip())
        
    # 3. Autolinks: <path/to/file.md> (ignore standard HTML tags)
    autolinks = re.findall(r'<([^>:\s]+)>', clean_content)
    for path in autolinks:
        if not path.startswith(("http", "https", "mailto", "a ", "/a", "p>", "h1", "h2", "h3", "h4", "div", "span", "img", "table", "tr", "td", "th", "tbody", "thead")):
            paths_to_check.append(path.strip())

    # 4. HTML anchors: <a href="path">
    html_anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', clean_content)
    for path in html_anchors:
        paths_to_check.append(path.strip())

    for path in paths_to_check:
        # Ignore external links or local page-only anchors
        if path.startswith(("http://", "https://", "mailto:", "#")):
            continue
            
        # Check absolute paths
        if path.startswith("/") or re.match(r'^[a-zA-Z]:\\', path):
            errors.append(f"Absolute path link detected: '{path}' (must be relative)")
            continue
            
        anchor = None
        clean_path = path
        if "#" in path:
            parts = path.split("#", 1)
            clean_path = parts[0]
            anchor = parts[1]
            
        if not clean_path:
            # Link is just an anchor to another section in the same file
            # Verify anchor in current file
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
            
        # Check if anchor exists in destination file
        if anchor and target_path.suffix.lower() in {".md", ".markdown", ".mdown"}:
            if not check_anchor_in_file(target_path, anchor):
                errors.append(f"Broken anchor link: '{path}' (anchor '#{anchor}' not found in '{clean_path}')")
                
    return errors

def check_anchor_in_file(file_path: Path, anchor: str) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return False
        
    def slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        return text

    target_slug = slugify(anchor)
    
    # Look for headings in target file
    for line in content.splitlines():
        line_strip = line.strip()
        if line_strip.startswith("#"):
            heading_text = line_strip.lstrip("#").strip()
            if slugify(heading_text) == target_slug:
                return True
    return False

def check_entity_alignment(file_path: Path, content: str) -> list:
    errors = []
    # If the file is a view file, verify that any system links cataloged actually exist
    if file_path.name in {"logical-view.md", "deployment-view.md", "data-view.md", "security-view.md", "integration-view.md"}:
        links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
        for text, path in links:
            if "systems/" in path and not path.startswith(("http://", "https://")):
                target_path = (file_path.parent / path).resolve()
                if not target_path.exists():
                    errors.append(f"System link defined in {file_path.name} does not exist on disk: '{path}'")
    return errors

def main():
    exclude_dirs = {".git", ".github", ".agents", "archive/legacy-artifacts", "architecture/systems/system-template/components"}
    gitignore_patterns = load_gitignore()
    markdown_files = []
    
    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        # Prevent traversal of excluded directories safely using segment checks
        rel_path = Path(root).relative_to(WORKSPACE_ROOT)
        rel_parts = rel_path.parts
        
        # Check explicit exclude_dirs segments
        if any(part in exclude_dirs for part in rel_parts):
            continue
            
        # Check gitignore patterns
        should_skip = False
        for pattern in gitignore_patterns:
            if any(re.match(pattern.replace("*", ".*"), part) for part in rel_parts):
                should_skip = True
                break
        if should_skip:
            continue
            
        for file in files:
            # Case-insensitive checks for MD extensions
            if file.lower().endswith((".md", ".markdown", ".mdown")):
                # Skip temporary files
                if file.startswith("~") or file.startswith(".") or file in {"ORIGINAL_REQUEST.md", "TEST_READY.md"}:
                    continue
                markdown_files.append(Path(root) / file)

    has_failures = False
    
    print(f"Scanning {len(markdown_files)} markdown files for structural rules...\n")
    
    for file_path in markdown_files:
        rel_path = file_path.relative_to(WORKSPACE_ROOT)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {rel_path}: {e}")
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
    else:
        print("\nAll structural validations passed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
