#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()

# Allowed values
ALLOWED_STATUSES = {"Draft", "In Review", "Approved", "Deprecated"}

def check_headers(file_path: Path, content: str) -> list:
    errors = []
    
    # Check if standard markdown file
    if file_path.name == "README.md" and file_path.parent == WORKSPACE_ROOT:
        # Root README is special but should still have Document Status, Purpose, Owner, Last Updated
        pass

    # Normalize newlines
    lines = [line.strip() for line in content.splitlines()]
    
    # Helper to check if header exists in the file
    has_title = any(line.startswith("# ") for line in lines)
    has_status = "## Document Status" in lines
    has_purpose = "## Purpose" in lines
    has_owner = "## Owner" in lines
    has_updated = "## Last Updated" in lines

    if not has_title:
        errors.append("Missing H1 title ('# [Document Title]')")
    if not has_status:
        errors.append("Missing '## Document Status' header")
    if not has_purpose:
        errors.append("Missing '## Purpose' header")
    if not has_owner:
        errors.append("Missing '## Owner' header")
    if not has_updated:
        errors.append("Missing '## Last Updated' header")
        
    return errors

def check_links(file_path: Path, content: str) -> list:
    errors = []
    # Markdown links: [text](path)
    # Exclude external links starting with http://, https://, mailto:, etc.
    # Exclude anchor links starting with #
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    
    for text, path in md_links:
        path = path.strip()
        # Ignore external links or anchor-only links
        if path.startswith(("http://", "https://", "mailto:", "#")):
            continue
            
        # Check absolute paths
        if path.startswith("/") or re.match(r'^[a-zA-Z]:\\', path):
            errors.append(f"Absolute path link detected: '{path}' (must be relative)")
            continue
            
        # Check target file existence
        # Paths are relative to the directory of the file containing the link
        target_path = (file_path.parent / path).resolve()
        
        # If the target path contains an anchor (e.g., file.md#anchor), strip it
        if "#" in path:
            clean_path = path.split("#")[0]
            if clean_path: # Could be just anchor if it was not caught by startswith
                target_path = (file_path.parent / clean_path).resolve()
            else:
                continue
                
        if not target_path.exists():
            try:
                rel_target = target_path.relative_to(WORKSPACE_ROOT)
            except ValueError:
                rel_target = target_path # Fallback to absolute if not in subpath
            errors.append(f"Broken relative link: '{path}' (resolved to non-existent '{rel_target}')")
            
    return errors

def check_entity_alignment(file_path: Path, content: str) -> list:
    errors = []
    # Only validate logical-view.md alignment if it contains systems that are not TBD
    if file_path.name == "logical-view.md":
        # Look for markdown links pointing to systems directory
        # e.g., systems/my-system/index.md or similar
        links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
        for text, path in links:
            if "systems/" in path and not path.startswith(("http://", "https://")):
                target_path = (file_path.parent / path).resolve()
                if not target_path.exists():
                    errors.append(f"System link defined in logical-view.md does not exist on disk: '{path}'")
    return errors

def main():
    exclude_dirs = {".git", ".github", "archive/legacy-artifacts", "architecture/systems/system-template/components"}
    markdown_files = []
    
    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        # Exclude directories on the fly
        relative_path = Path(root).relative_to(WORKSPACE_ROOT)
        if any(str(relative_path).startswith(exclude) for exclude in exclude_dirs if exclude):
            continue
        if relative_path.name in exclude_dirs:
            continue
            
        for file in files:
            if file.endswith(".md"):
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
