#!/usr/bin/env python3
"""
initialize_project.py — Bootstrap and initialize a new project architecture repository.

Usage:
  python3 initialize_project.py --name "Project Name" --topology <monolith|modular-monolith|microservices|serverless> --owner "Team Name"

This script automates the first onboarding step for a client:
1. Updates README.md and how-to-start.md with the client project name and owner.
2. Seeds glossary.md.
3. Dynamically generates and records the initial topology selection ADR.
4. Scaffolds initial Bounded Contexts (systems).
5. Runs verify_docs.py to ensure the fresh repository is linter-clean.
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()

def print_step(msg: str):
    print(f"\n★ {msg}")

def update_file_content(path: Path, find_pattern: str, replace_val: str):
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    new_content = re.sub(find_pattern, replace_val, content)
    path.write_text(new_content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Initialize a new project architecture repository")
    parser.add_argument("--name", required=True, help="Name of the client project (e.g., 'StorGratis BAOP')")
    parser.add_argument("--topology", required=True, 
                        choices=["monolith", "modular-monolith", "microservices", "serverless"],
                        help="Chosen deployment topology")
    parser.add_argument("--owner", required=True, help="Owner team name (e.g., 'Engineering Team')")
    parser.add_argument("--systems", nargs="*", default=[], help="Optional list of initial bounded contexts/systems to scaffold")
    args = parser.parse_args()

    project_name = args.name.strip()
    topology = args.topology.strip()
    owner = args.owner.strip()
    today = datetime.date.today().isoformat()

    print(f"\n==================================================")
    print(f"Initializing Architecture Repository for: {project_name}")
    print(f"Topology: {topology} | Owner: {owner}")
    print(f"==================================================\n")

    # 1. Update root README.md
    print_step("Updating root README.md...")
    readme_path = WORKSPACE_ROOT / "README.md"
    update_file_content(
        readme_path,
        r"^# Architecture Repository",
        f"# {project_name} Architecture Repository"
    )
    update_file_content(
        readme_path,
        r"## Owner\n(<!-- .* -->\n)?TBD",
        f"## Owner\n{owner}"
    )
    update_file_content(
        readme_path,
        r"## Last Updated\n\d{4}-\d{2}-\d{2}",
        f"## Last Updated\n{today}"
    )

    # 2. Update how-to-start.md
    print_step("Updating how-to-start.md onboarding guide...")
    how_start_path = WORKSPACE_ROOT / "how-to-start.md"
    update_file_content(
        how_start_path,
        r"## Owner\n(<!-- .* -->\n)?TBD",
        f"## Owner\n{owner}"
    )
    update_file_content(
        how_start_path,
        r"## Last Updated\n\d{4}-\d{2}-\d{2}",
        f"## Last Updated\n{today}"
    )

    # 3. Update onboarding-dev.md
    print_step("Updating onboarding-dev.md developer onboarding...")
    dev_path = WORKSPACE_ROOT / "onboarding-dev.md"
    update_file_content(
        dev_path,
        r"## Owner\n(<!-- .* -->\n)?TBD",
        f"## Owner\n{owner}"
    )
    update_file_content(
        dev_path,
        r"## Last Updated\n\d{4}-\d{2}-\d{2}",
        f"## Last Updated\n{today}"
    )

    # 4. Bootstrap glossary.md
    print_step("Seeding glossary.md...")
    glossary_path = WORKSPACE_ROOT / "glossary.md"
    glossary_content = f"""# Glossary

## Document Status
Approved

## Purpose
Ubiquitous domain vocabulary and authoritative technical terms for the {project_name} project.

## Owner
{owner}

## Last Updated
{today}

---

## 1. Domain Vocabulary

| Term | Definition | Context |
| :--- | :--- | :--- |
| Customer | An entity that interacts with {project_name} products or services. | Domain |
| System | The overall {project_name} software platform. | Technical |

<!-- AI_HINT: Add domain-specific nouns here to train AI assistants on ubiquitous vocabulary -->
"""
    glossary_path.write_text(glossary_content, encoding="utf-8")

    # 5. Scaffold Topology ADR
    print_step(f"Recording architecture decision for chosen topology: {topology}...")
    adr_title = f"select-{topology}-deployment-topology"
    
    # Run the existing scaffold_adr.py script via subprocess
    res = subprocess.run(
        [sys.executable, "scaffold_adr.py", adr_title],
        capture_output=True,
        text=True,
        cwd=WORKSPACE_ROOT
    )
    if res.returncode != 0:
        print(f"❌ Failed to scaffold topology ADR: {res.stderr}")
    else:
        # Find the newly created ADR file path
        match = re.search(r"Created: decisions/(.+)", res.stdout)
        if match:
            adr_filename = match.group(1)
            adr_path = WORKSPACE_ROOT / "decisions" / adr_filename
            print(f"✅ Created: decisions/{adr_filename}")
            
            # Update the status and write the topology decision
            adr_text = adr_path.read_text(encoding="utf-8")
            
            # Customize the ADR content
            adr_text = adr_text.replace("## Status\n\nProposed", "## Status\n\nApproved")
            adr_text = adr_text.replace("## Owner\n<!-- AI_HINT: PENDING_DISCOVERY - DO NOT AUTOFILL -->\nTBD", f"## Owner\n{owner}")
            
            context_desc = f"To align the technical architecture of the {project_name} platform with organizational constraints, we analyzed the required team scale, latency attributes, database coupling patterns, and deployment frequency requirements using the Architectural Decision Matrix."
            decision_desc = f"We select the **{topology.replace('-', ' ').title()}** deployment topology for {project_name}. All sub-systems, logical views, and coding standards must conform to the constraints defined in this topology profile."
            
            adr_text = re.sub(r"## Context\n\n.*?TBD", f"## Context\n\n{context_desc}", adr_text, flags=re.DOTALL)
            adr_text = re.sub(r"## Decision\n\n.*?TBD", f"## Decision\n\n{decision_desc}", adr_text, flags=re.DOTALL)
            
            adr_path.write_text(adr_text, encoding="utf-8")
            print(f"✅ Customized topology ADR details.")

    # 6. Scaffold Initial Bounded Contexts / Systems
    if args.systems:
        print_step("Scaffolding initial bounded context systems...")
        for system_name in args.systems:
            system_slug = system_name.lower().strip().replace(" ", "-")
            system_res = subprocess.run(
                [sys.executable, "scaffold_system.py", system_slug],
                capture_output=True,
                text=True,
                cwd=WORKSPACE_ROOT
            )
            if system_res.returncode != 0:
                print(f"❌ Failed to scaffold system '{system_slug}': {system_res.stderr}")
            else:
                print(f"✅ Scaffolding complete for bounded context: {system_slug}")
                # Set owner in the system index file
                sys_index = WORKSPACE_ROOT / "architecture" / "systems" / system_slug / "index.md"
                if sys_index.exists():
                    update_file_content(sys_index, r"## Owner\n(<!-- .* -->\n)?TBD", f"## Owner\n{owner}")
                    update_file_content(sys_index, r"## Last Updated\n\d{4}-\d{2}-\d{2}", f"## Last Updated\n{today}")

    # 7. Run verification check
    print_step("Running verify_docs.py check on initialized repository...")
    verify_res = subprocess.run(
        [sys.executable, "verify_docs.py"],
        capture_output=True,
        text=True,
        cwd=WORKSPACE_ROOT
    )
    if verify_res.returncode == 0:
        print("✅ verify_docs.py passed successfully!")
    else:
        print("⚠️ Warning: verify_docs.py detected structural issues:")
        print(verify_res.stdout)

    print("\n🎉 Project Architecture Repository initialization complete!")
    print(f"Next Steps: Let your AI coding assistant know about your new setup to start generating domain diagrams!")

if __name__ == "__main__":
    main()
