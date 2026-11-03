#!/usr/bin/env python3
"""
RSI Modular Memory Resolution and Audit Engine
- Targeted contextual indexing and loading of sub-playbooks (.agents/rules/modules/)
- Anti-bloat verification (< 80 lines per sub-module)
- Fully generic and reusable across projects
"""

import sys
import os
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
MODULES_DIR = ROOT_DIR / ".agents" / "rules" / "modules"
MAX_LINES_PER_MODULE = 80

MODULE_TRIGGERS = {
    "db.md": ["prisma", "schema", "model", "migration", "database", "sql", "mongo", "db", "drizzle"],
    "api_backend.md": ["actions", "route", "api", "controller", "service", "handler", "server", "redis", "queue"],
    "ui_frontend.md": ["component", "components", "page", "layout", "view", "css", "tailwind", "tsx", "jsx", "styles"],
    "security_auth.md": ["auth", "session", "crypto", "token", "jwt", "permission", "security", "hash", "secret"],
    "integration_ai.md": ["ai", "llm", "agent", "prompt", "openai", "gemini", "anthropic", "openrouter", "rag"]
}

def audit_memory_modules() -> bool:
    """Verifies that each module strictly remains under the maximum line ceiling."""
    if not MODULES_DIR.exists():
        print(f"[WARN] [RSI Memory Audit] Modules directory not found at {MODULES_DIR}")
        return True

    modules = list(MODULES_DIR.glob("*.md"))
    if not modules:
        print("[INFO] [RSI Memory Audit] No modules found.")
        return True

    print(f"[RSI Memory Audit] {len(modules)} modules detected.")
    has_violation = False

    for mod in modules:
        try:
            content = mod.read_text(encoding="utf-8")
            line_count = len([line for line in content.splitlines() if line.strip()])
            if line_count > MAX_LINES_PER_MODULE:
                print(f"  [FAIL] {mod.name}: {line_count}/{MAX_LINES_PER_MODULE} lines (LIMIT EXCEEDED!)")
                has_violation = True
            else:
                print(f"  [OK] {mod.name}: {line_count}/{MAX_LINES_PER_MODULE} lines")
        except Exception as e:
            print(f"  [WARN] Error reading {mod.name}: {e}")

    if has_violation:
        print("\n[FAIL] Some modules exceed the maximum allowed line count. Summarize or split them!")
        return False
    else:
        print("\n[OK] All modules comply with the strict compactness limit!")
        return True

def resolve_context(files: list[str]) -> str:
    """Determines which modules to load based on input file paths."""
    matched_modules = set()
    for f in files:
        f_lower = f.lower().replace("\\", "/")
        for mod, keywords in MODULE_TRIGGERS.items():
            if any(k in f_lower for k in keywords):
                matched_modules.add(mod)

    if not matched_modules:
        return "[INFO] No specific sub-playbook required for these files. Refer to fullstack_playbook.md if needed."

    output = ["[RSI Dynamic Memory Injection]"]
    for mod in sorted(matched_modules):
        mod_path = MODULES_DIR / mod
        if mod_path.exists():
            output.append(f"\n--- [Module: {mod}] ---")
            output.append(mod_path.read_text(encoding="utf-8").strip())

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="RSI Modular Memory Engine")
    parser.add_argument("--audit", action="store_true", help="Verify module compactness ceiling")
    parser.add_argument("--inject", nargs="*", help="Dynamically inject relevant rule modules for specified files")
    args = parser.parse_args()

    if args.audit:
        success = audit_memory_modules()
        sys.exit(0 if success else 1)

    if args.inject is not None:
        if len(args.inject) == 0:
            print("Usage: --inject [file1] [file2] ...")
        else:
            print(resolve_context(args.inject))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
