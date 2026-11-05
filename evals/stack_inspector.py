#!/usr/bin/env python3
"""
Technical Stack, Topological Map & Blast Radius Auditor
- Detects package manager, framework, ORM, auth, styles, cloud services
- Generates a compact Topological Repo Map (--map) of canonical singletons and hub files
- Predicts change Blast Radius (--impact <file>) via reverse dependency analysis
- Recommends and verifies official tooling installation (MCP servers & Skills)
"""

import sys
import re
import json
import argparse
from pathlib import Path

# UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.next', 'backups', 'logs'}
CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py'}

SINGLETON_SIGNATURES = [
    (re.compile(r'new\s+PrismaClient|PrismaClient'), "Database ORM Singleton"),
    (re.compile(r'createClient\s*\(|supabase', re.IGNORECASE), "Supabase / Cloud Client"),
    (re.compile(r'betterAuth\s*\(|NextAuth|authOptions'), "Authentication Core"),
    (re.compile(r'new\s+Redis\s*\(|Redis\.fromEnv|QStash', re.IGNORECASE), "Cache / Queue Client"),
    (re.compile(r'S3Client|Tigris', re.IGNORECASE), "Object Storage Client"),
    (re.compile(r'createEnv\s*\(|z\.object\s*\(.*process\.env', re.DOTALL), "Environment Schema Validator")
]

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

def iter_source_files() -> list[Path]:
    files = []
    for path in ROOT_DIR.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix in CODE_EXTENSIONS:
            files.append(path)
    return sorted(files)

def build_dependency_graph(files: list[Path]) -> dict[str, set[str]]:
    """Maps each relative file path to the set of relative file paths that import/reference it."""
    rel_files = [str(f.relative_to(ROOT_DIR)).replace("\\", "/") for f in files]
    reverse_deps: dict[str, set[str]] = {rf: set() for rf in rel_files}

    # Precompute stem and basename lookup keys for fast matching
    lookup_tokens: dict[str, list[str]] = {}
    for rf in rel_files:
        p = Path(rf)
        stem = p.stem
        no_ext = str(p.with_suffix("")).replace("\\", "/")
        tokens = [rf, no_ext]
        if stem not in {"index", "__init__", "main", "route", "page", "layout"}:
            tokens.append(stem)
        lookup_tokens[rf] = tokens

    for f in files:
        caller_rel = str(f.relative_to(ROOT_DIR)).replace("\\", "/")
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for target_rel, tokens in lookup_tokens.items():
            if target_rel == caller_rel:
                continue
            for tok in tokens:
                if re.search(rf'(?:from|import|require|\/|\"|\')\s*[\w\.\/\@\-]*\b{re.escape(tok)}\b', content):
                    reverse_deps[target_rel].add(caller_rel)
                    break

    return reverse_deps

def generate_topological_map() -> None:
    """Outputs a compact O(1) Topological Map of singletons, core hubs, and governance entrypoints."""
    files = iter_source_files()
    reverse_deps = build_dependency_graph(files)

    print("[RSI Topological Map] Scanning canonical singletons and hub modules...")
    singletons = []
    core_dirs = {"lib", "server", "core", "utils", "services", "evals"}

    for f in files:
        rel = str(f.relative_to(ROOT_DIR)).replace("\\", "/")
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Only scan application files (outside evals/) for runtime singleton signatures
        if "evals" not in f.relative_to(ROOT_DIR).parts:
            for pattern, role in SINGLETON_SIGNATURES:
                if pattern.search(content):
                    singletons.append((rel, role))
                    break
        if not any(s[0] == rel for s in singletons):
            parts = f.relative_to(ROOT_DIR).parts[:-1]
            if "evals" in parts:
                singletons.append((rel, "RSI Governance / Evaluation Engine"))
            elif any(part in core_dirs for part in parts):
                singletons.append((rel, "Core Infrastructure / Module"))

    print("\n1. Canonical Singletons & Core Modules (Reuse in O(1) - Do Not Duplicate):")
    if singletons:
        for rel, role in singletons[:12]:
            dep_count = len(reverse_deps.get(rel, set()))
            print(f"  - {rel} [{role}] (dependents: {dep_count})")
    else:
        print("  - [INFO] No application singletons detected yet.")

    ranked_hubs = sorted(reverse_deps.items(), key=lambda item: (-len(item[1]), item[0]))
    active_hubs = [(k, v) for k, v in ranked_hubs if len(v) > 0]

    print("\n2. Top Dependency Hubs (Highest Blast Radius):")
    if active_hubs:
        for rel, callers in active_hubs[:8]:
            print(f"  - {rel} -> imported/invoked by {len(callers)} file(s)")
    else:
        print("  - [INFO] No cross-file imports detected yet.")

def analyze_blast_radius(target_file: str) -> None:
    """Computes the reverse dependency Blast Radius for a specific file before modification."""
    norm_target = target_file.replace("\\", "/").lstrip("./")
    files = iter_source_files()
    # Also scan markdown workflows/docs for script invocations
    all_scan_files = files + [
        p for p in ROOT_DIR.rglob("*.md")
        if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts)
    ]

    target_path = Path(norm_target)
    target_stem = target_path.stem
    dependents = []

    for f in all_scan_files:
        caller_rel = str(f.relative_to(ROOT_DIR)).replace("\\", "/")
        if caller_rel.lower() == norm_target.lower():
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if norm_target in content or (
            target_stem not in {"index", "__init__", "main", "route", "page", "layout"}
            and re.search(rf'\b{re.escape(target_stem)}\b', content)
        ):
            dependents.append(caller_rel)

    count = len(dependents)
    if count <= 2:
        tier = "LOW (Localized impact - System 1 safe edit)"
    elif count <= 7:
        tier = "MEDIUM (Shared module - Verify consumer contracts)"
    else:
        tier = "HIGH / CRITICAL (Core hub - System 2 reasoning required; preserve exported signatures)"

    print(f"[RSI Blast Radius] Target: {norm_target}")
    print(f"  |-- Impact Tier : {tier}")
    print(f"  \\-- Dependents  : {count} file(s)")
    for dep in sorted(dependents)[:15]:
        print(f"      * {dep}")
    if count > 15:
        print(f"      * ... and {count - 15} more file(s)")

def main():
    parser = argparse.ArgumentParser(description="RSI Stack Inspector, Topological Map & Blast Radius Analyzer")
    parser.add_argument("--map", action="store_true", help="Generate compact O(1) Topological Map of singletons and hubs")
    parser.add_argument("--impact", type=str, metavar="FILE", help="Analyze reverse-dependency Blast Radius for a file")
    args = parser.parse_args()

    if args.map:
        generate_topological_map()
        sys.exit(0)

    if args.impact:
        analyze_blast_radius(args.impact)
        sys.exit(0)

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
