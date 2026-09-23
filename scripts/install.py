#!/usr/bin/env python3
"""
Production Agent Skills Cross-Platform Python Installer
Compatible with Windows, macOS, and Linux.
Installs skills into Antigravity, Claude Code, Cursor, or local workspaces.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILLS = [
    "ai-website-polish",
    "frontend-math-precision",
    "quantitative-ux-engine",
    "ux-laws-for-ai-design",
    "website-data-protection",
]

def resolve_target(target_name: str) -> Path:
    home = Path.home()
    if target_name == "antigravity":
        return home / ".gemini" / "config" / "skills"
    elif target_name == "claude":
        return home / ".claude" / "skills"
    elif target_name == "cursor":
        return home / ".cursor" / "skills"
    elif target_name == "local":
        return Path.cwd() / ".agents" / "skills"
    else:
        raise ValueError(f"Unknown target: {target_name}")

def main():
    parser = argparse.ArgumentParser(description="Install Production Agent Skills across environments.")
    parser.add_argument(
        "-t", "--target",
        choices=["antigravity", "claude", "cursor", "local"],
        default="antigravity",
        help="Target agent environment (default: antigravity)"
    )
    parser.add_argument(
        "-s", "--skill",
        choices=SKILLS,
        help="Install only a specific skill"
    )
    parser.add_argument(
        "--all", action="store_true", default=True,
        help="Install all skills in the repository (default)"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true",
        help="Preview changes without copying files"
    )

    args = parser.parse_args()
    dest_dir = resolve_target(args.target)

    skills_to_install = [args.skill] if args.skill else SKILLS

    print(f"=== Installing Production Agent Skills ===")
    print(f"Target Environment : {args.target}")
    print(f"Destination Path   : {dest_dir}")
    if args.dry_run:
        print("Execution Mode     : DRY RUN (no files modified)\n")
    else:
        print()
        dest_dir.mkdir(parents=True, exist_ok=True)

    for skill in skills_to_install:
        src = REPO_ROOT / skill
        dst = dest_dir / skill
        if not src.exists():
            print(f"  [SKIP] Missing source directory: {skill}")
            continue

        if args.dry_run:
            print(f"  [PLAN] Would install: {skill} -> {dst}")
        else:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  [INSTALLED] {skill}")

    print("\n✔ Done!")

if __name__ == "__main__":
    main()
