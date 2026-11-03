#!/usr/bin/env python3
"""
Technical Stack & Official Tooling (Skills & MCP) Auditor
- Detects package manager, framework, ORM, auth, styles, cloud services
- Recommends and verifies official tooling installation (MCP servers & Skills)
- Fully generic and configurable
"""

import sys
import json
from pathlib import Path

# UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

ECOSYSTEM_CATALOG = {
    "shadcn": {
        "deps": ["@radix-ui", "clsx", "tailwind-merge"],
        "files": ["components.json"],
        "skill": "shadcn",
        "mcp_server": None,
        "purpose": "Accessible and styled UI component primitives"
    },
    "prisma": {
        "deps": ["@prisma/client", "prisma"],
        "files": ["prisma/schema.prisma"],
        "skill": "prisma-management",
        "skill_keywords": ["prisma"],
        "mcp_server": None,
        "purpose": "Database schema management and validation"
    },
    "upstash": {
        "deps": ["@upstash/redis", "@upstash/qstash", "@upstash/ratelimit"],
        "files": [],
        "skill": "upstash",
        "mcp_server": "upstash",
        "purpose": "Asynchronous job queue, rate limiting, and distributed cache"
    },
    "tigris": {
        "deps": ["@aws-sdk/client-s3", "@aws-sdk/s3-request-presigner"],
        "env_keys": ["TIGRIS_", "AWS_ENDPOINT_URL_S3"],
        "files": [],
        "skill": "file-storage",
        "skill_keywords": ["tigris", "storage"],
        "mcp_server": None,
        "purpose": "Zero-egress S3-compatible high-performance object storage"
    },
    "playwright": {
        "deps": ["@playwright/test", "playwright"],
        "files": ["playwright.config.ts", "playwright.config.js"],
        "skill": "playwright-skill",
        "skill_keywords": ["playwright"],
        "mcp_server": None,
        "purpose": "Deterministic E2E testing and browser automation"
    }
}

def detect_stack() -> dict:
    dependencies = {}
    pkg_json = ROOT_DIR / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                dependencies.update(data.get("dependencies", {}))
                dependencies.update(data.get("devDependencies", {}))
        except Exception:
            pass

    env_content = ""
    for env_file in [".env", ".env.local", ".env.example"]:
        p = ROOT_DIR / env_file
        if p.exists():
            try:
                env_content += p.read_text(encoding="utf-8") + "\n"
            except Exception:
                pass

    installed_skills = set()
    skills_dir = ROOT_DIR / ".agents" / "skills"
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir():
                installed_skills.add(item.name.lower())

    configured_mcps = set()
    mcp_json = ROOT_DIR / ".mcp.json"
    if mcp_json.exists():
        try:
            with open(mcp_json, "r", encoding="utf-8") as f:
                mcp_data = json.load(f)
                servers = mcp_data.get("mcpServers", {})
                configured_mcps.update(k.lower() for k in servers.keys())
        except Exception:
            pass

    detected = {}
    for tech, meta in ECOSYSTEM_CATALOG.items():
        is_present = False
        for dep in meta.get("deps", []):
            if any(dep.lower() in d.lower() for d in dependencies.keys()):
                is_present = True
                break
        if not is_present:
            for f in meta.get("files", []):
                if (ROOT_DIR / f).exists():
                    is_present = True
                    break
        if not is_present:
            for env_key in meta.get("env_keys", []):
                if env_key in env_content:
                    is_present = True
                    break

        if is_present:
            skill_found = False
            target_skill = meta.get("skill")
            skill_keywords = meta.get("skill_keywords", [target_skill])
            for s in installed_skills:
                if any(kw and kw.lower() in s for kw in skill_keywords):
                    skill_found = True
                    break

            mcp_found = False
            target_mcp = meta.get("mcp_server")
            if target_mcp:
                for m in configured_mcps:
                    if target_mcp.lower() in m:
                        mcp_found = True
                        break
            else:
                mcp_found = True

            detected[tech] = {
                "purpose": meta["purpose"],
                "has_skill": skill_found,
                "recommended_skill": target_skill,
                "has_mcp": mcp_found,
                "recommended_mcp": target_mcp
            }

    return detected

def main():
    print("[RSI Stack Inspector] Analyzing project ecosystem...")
    stack = detect_stack()

    if not stack:
        print("[INFO] No standard ecosystem technologies detected yet.")
        return

    print(f"[INFO] {len(stack)} technical components identified in the project:\n")
    missing_tools = []

    for tech, info in stack.items():
        skill_status = "[OK] Installed" if info["has_skill"] else f"[WARN] MISSING ({info['recommended_skill']})"
        mcp_status = "[OK] Configured" if info["has_mcp"] else f"[WARN] MISSING ({info['recommended_mcp']})"
        
        print(f"* {tech.upper()}: {info['purpose']}")
        print(f"   |-- Skill : {skill_status}")
        if info["recommended_mcp"]:
            print(f"   \\-- MCP   : {mcp_status}")
        print()

        if not info["has_skill"] or not info["has_mcp"]:
            missing_tools.append((tech, info))

    if missing_tools:
        print("[INFO] [RSI Recommendations] To avoid unguided coding, install the missing official tools.")
    else:
        print("[OK] [RSI Stack Audit] Official tooling is complete and compliant!")

if __name__ == "__main__":
    main()
