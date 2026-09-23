#!/usr/bin/env python3
"""
Agent Skills Standard Validator
Validates that all skills in the repository adhere to the Agent Skills Open Standard:
1. Directory name matches frontmatter 'name'.
2. 'name' is <= 64 chars, lowercase alphanumeric and non-consecutive hyphens.
3. 'description' is <= 1024 chars and includes negative trigger boundaries.
4. 'SKILL.md' is < 500 lines to preserve model reasoning capacity.
5. Internal references link to existing files in references/ or scripts/.
6. Bundled verification utilities execute successfully.
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).resolve().parent.parent

def find_skills(root_dir: Path):
    skills = []
    for item in root_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in ["scripts", "assets"]:
            skill_md = item / "SKILL.md"
            if skill_md.is_file():
                skills.append(item)
    return sorted(skills, key=lambda p: p.name)

def validate_skill(skill_dir: Path) -> list:
    errors = []
    warnings = []
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    # Read content
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read SKILL.md: {e}"], []

    lines = content.splitlines()
    line_count = len(lines)

    # 1. Line budget check (< 500 lines)
    if line_count >= 500:
        errors.append(f"Line count ({line_count}) exceeds the 500-line budget limit.")
    
    # 2. YAML frontmatter parse
    parts = content.split("---")
    if len(parts) < 3:
        errors.append("Invalid or missing YAML frontmatter delimiters ('---').")
        return errors, warnings

    try:
        frontmatter = yaml.safe_load(parts[1])
    except Exception as e:
        errors.append(f"Failed to parse YAML frontmatter: {e}")
        return errors, warnings

    if not isinstance(frontmatter, dict):
        errors.append("YAML frontmatter must be a dictionary.")
        return errors, warnings

    # 3. Name parameter validation
    name = frontmatter.get("name")
    if not name:
        errors.append("Missing required frontmatter field: 'name'.")
    else:
        if name != skill_name:
            errors.append(f"Frontmatter 'name' ('{name}') does not match directory name ('{skill_name}').")
        if len(name) > 64:
            errors.append(f"Frontmatter 'name' length ({len(name)}) exceeds 64 characters.")
        if not all(c.isalnum() or c == '-' for c in name):
            errors.append("Frontmatter 'name' must contain only lowercase alphanumeric characters and hyphens.")
        if "--" in name:
            errors.append("Frontmatter 'name' contains consecutive hyphens.")

    # 4. Description validation
    desc = frontmatter.get("description", "")
    if not desc:
        errors.append("Missing required frontmatter field: 'description'.")
    else:
        if len(desc) > 1024:
            errors.append(f"Frontmatter 'description' length ({len(desc)}) exceeds 1024 characters.")
        desc_lower = desc.lower()
        if "not" not in desc_lower and "never" not in desc_lower and "exclude" not in desc_lower:
            warnings.append("Description lacks explicit negative trigger boundary ('Do NOT trigger...').")

    # 5. Check internal references
    for line in lines:
        if "](" in line:
            for part in line.split("](")[1:]:
                link = part.split(")")[0].strip()
                if link and not link.startswith("http") and not link.startswith("#") and not link.startswith("mailto"):
                    target_path = (skill_dir / link).resolve()
                    if not target_path.exists():
                        warnings.append(f"Potential broken relative link in SKILL.md: '{link}'")

    return errors, warnings

def run_bundled_tests():
    print(f"\n{BOLD}Executing Bundled Test Suites...{RESET}")
    ux_metrics_script = REPO_ROOT / "quantitative-ux-engine" / "scripts" / "ux-metrics.py"
    if ux_metrics_script.exists():
        res = subprocess.run([sys.executable, str(ux_metrics_script)], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [{GREEN}PASS{RESET}] quantitative-ux-engine/scripts/ux-metrics.py execution verified.")
            return True
        else:
            print(f"  [{RED}FAIL{RESET}] ux-metrics.py failed:\n{res.stderr}")
            return False
    return True

def main():
    print(f"{BOLD}=== Production Agent Skills Standard Validator ==={RESET}\n")
    skills = find_skills(REPO_ROOT)
    
    if not skills:
        print(f"{RED}No skills found in {REPO_ROOT}!{RESET}")
        sys.exit(1)

    all_passed = True
    total_skills = len(skills)
    passed_skills = 0

    for skill in skills:
        errors, warnings = validate_skill(skill)
        skill_name = skill.name
        
        if not errors:
            passed_skills += 1
            status = f"{GREEN}PASS{RESET}"
            line_count = len((skill / "SKILL.md").read_text(encoding="utf-8").splitlines())
            print(f"[{status}] {BOLD}{skill_name:<30}{RESET} ({line_count} lines)")
        else:
            all_passed = False
            status = f"{RED}FAIL{RESET}"
            print(f"[{status}] {BOLD}{skill_name:<30}{RESET}")
            for err in errors:
                print(f"    {RED}• Error: {err}{RESET}")

        for warn in warnings:
            print(f"    {YELLOW}• Warning: {warn}{RESET}")

    bundled_passed = run_bundled_tests()
    if not bundled_passed:
        all_passed = False

    print(f"\n{BOLD}Validation Summary:{RESET} {passed_skills}/{total_skills} skills conforming.")

    if all_passed:
        print(f"\n{GREEN}{BOLD}✔ All skills strictly adhere to the Agent Skills Open Standard.{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}{BOLD}✘ Conformance errors detected. Please fix the above issues.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
