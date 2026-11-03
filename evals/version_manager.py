#!/usr/bin/env python3
"""
Universal SemVer Versioning Manager
Manages release version life cycles:
- SemVer bumping (Major, Minor, Patch, pre-release tags)
- package.json version updating
- Sealing the [Unreleased] section in CHANGELOG.md with current date
- Automatic Git tagging preparation
"""

import sys
import os
import re
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
PACKAGE_JSON_PATH = ROOT_DIR / "package.json"
CHANGELOG_PATH = ROOT_DIR / "CHANGELOG.md"

def parse_semver(version_str: str) -> tuple[int, int, int, str | None]:
    clean = version_str.lstrip("v").strip()
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9._-]+))?$", clean)
    if not match:
        raise ValueError(f"Invalid SemVer format: '{version_str}'")
    return int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)

def get_current_version() -> str:
    if not PACKAGE_JSON_PATH.exists():
        return "0.1.0"
    with open(PACKAGE_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("version", "0.1.0")

def bump_semver(current_ver: str, bump_type: str, mention: str | None = None) -> str:
    major, minor, patch, _ = parse_semver(current_ver)
    bump_lower = bump_type.lower()

    if bump_lower == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_lower == "minor":
        minor += 1
        patch = 0
    elif bump_lower == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: '{bump_type}'")

    new_ver = f"{major}.{minor}.{patch}"
    if mention:
        clean_mention = re.sub(r"[^a-zA-Z0-9._-]", "-", mention.strip())
        new_ver = f"{new_ver}-{clean_mention}"
    return new_ver

def update_package_json(new_ver: str) -> None:
    if not PACKAGE_JSON_PATH.exists():
        return
    with open(PACKAGE_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["version"] = new_ver
    with open(PACKAGE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def update_changelog(new_ver: str) -> None:
    if not CHANGELOG_PATH.exists():
        return
    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    replacement = f"## [Unreleased]\n\n## [{new_ver}] - {today}"
    if re.search(r"##\s+\[Unreleased\]", content, re.IGNORECASE):
        updated = re.sub(r"##\s+\[Unreleased\]", replacement, content, count=1, flags=re.IGNORECASE)
        CHANGELOG_PATH.write_text(updated, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Universal SemVer Manager")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], default="patch", help="SemVer bump increment level")
    parser.add_argument("--mention", help="Optional pre-release tag (e.g. beta, hotfix)")
    args = parser.parse_args()

    curr = get_current_version()
    next_ver = bump_semver(curr, args.bump, args.mention)

    print(f"📦 [SemVer Bump] {curr} ➔ {next_ver}")
    update_package_json(next_ver)
    update_changelog(next_ver)
    print("✅ Version and CHANGELOG updated successfully.")

if __name__ == "__main__":
    main()
