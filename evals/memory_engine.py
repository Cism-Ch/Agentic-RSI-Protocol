#!/usr/bin/env python3
"""
RSI Modular Memory Resolution and Audit Engine
- Targeted contextual indexing and loading of sub-playbooks (.agents/rules/modules/)
- Anti-bloat verification (< 80 lines per sub-module)
- Fully generic and reusable across projects
"""

import sys
import os
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
MODULES_DIR = ROOT_DIR / ".agents" / "rules" / "modules"
TRAJECTORY_FILE = ROOT_DIR / "evals" / "logs" / "trajectory_latest.json"
MAX_LINES_PER_MODULE = 80

MODULE_TRIGGERS = {
    "db.md": ["prisma", "schema", "model", "migration", "database", "sql", "mongo", "db", "drizzle"],
    "api_backend.md": ["actions", "route", "api", "controller", "service", "handler", "server", "redis", "queue"],
    "ui_frontend.md": ["component", "components", "page", "layout", "view", "css", "tailwind", "tsx", "jsx", "styles"],
    "security_auth.md": ["auth", "session", "crypto", "token", "jwt", "permission", "security", "hash", "secret"],
    "integration_ai.md": ["ai", "llm", "agent", "prompt", "openai", "gemini", "anthropic", "openrouter", "rag"],
    "pattern_recognition.md": ["pattern", "architecture", "core", "utils", "lib", "helper", "config", "eval"]
}

KNOWN_ERROR_PATTERNS = [
    (
        re.compile(r"Non-ASCII / Emoji Character|UnicodeEncodeError|charmap", re.IGNORECASE),
        "[R-SYS-05] ASCII & Emoji Hygiene Violation",
        "Strip all emojis, smart quotes, em-dashes, and Unicode arrows (>127) from scripts and markdown files."
    ),
    (
        re.compile(r"LIMIT EXCEEDED|exceed the maximum allowed line count", re.IGNORECASE),
        "[R-MEM-01] Module Line Ceiling Exceeded (>80 lines)",
        "Synthesize redundant rules without losing specificity, or split the module into finer domain files and register in fullstack_playbook.md."
    ),
    (
        re.compile(r"Errno 2.*No such file or directory.*python", re.IGNORECASE),
        "[R-PAT-03] Subprocess Shell Quoting Mismatch on Unix/CI",
        "Pass tokenized command lists [sys.executable, str(script_path), '--flag'] to subprocess.run with shell=False."
    ),
    (
        re.compile(r"potential secret leak|Hardcoded Auth Secret|Private Key", re.IGNORECASE),
        "[R-SEC-02] Exposed Secret or Credential in Source",
        "Move the credential immediately to .env (git-ignored) and reference it via validated server environment variables."
    ),
    (
        re.compile(r"Operational Anti-Pattern|PrismaClient|NEXT_PUBLIC_|VITE_", re.IGNORECASE),
        "[R-PAT-04] Operational Security or Singleton Violation",
        "Remove secret keys from public frontend env vars and instantiate ORM clients strictly inside a dedicated singleton file."
    ),
    (
        re.compile(r"TS\d{4}:|error TS|Type '.*' is not assignable", re.IGNORECASE),
        "[R-SYS-01] Strict TypeScript Type Mismatch",
        "Align explicit return types and validate external payloads with Zod before passing to typed functions."
    )
]

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

def diagnose_trajectory() -> bool:
    """Fast-fail reflex: matches recent failure logs against known error signatures in <10ms."""
    if not TRAJECTORY_FILE.exists():
        print("[INFO] [RSI Pattern Diagnosis] No trajectory log found at evals/logs/trajectory_latest.json.")
        return True

    try:
        data = json.loads(TRAJECTORY_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARN] [RSI Pattern Diagnosis] Could not parse trajectory file: {e}")
        return False

    failed_steps = data.get("failed_steps", [])
    if not failed_steps:
        print("[OK] [RSI Pattern Diagnosis] Last trajectory status is PASS (0 failed steps).")
        return True

    print(f"[RSI Pattern Diagnosis] Analyzing {len(failed_steps)} failed step(s)...")
    matched_any = False
    for step_info in failed_steps:
        step_name = step_info.get("step", "unknown")
        error_log = step_info.get("error_log", "")
        print(f"\n  -> Step Failed: [{step_name}]")
        step_matched = False
        for pattern, rule_label, fix in KNOWN_ERROR_PATTERNS:
            if pattern.search(error_log):
                print(f"     [MATCH] {rule_label}")
                print(f"     [FIX]   {fix}")
                step_matched = True
                matched_any = True
        if not step_matched:
            snippet = error_log.strip().splitlines()[0] if error_log.strip() else "Empty error log"
            print(f"     [UNCLASSIFIED] Escalate to System 2 reasoning. Log sample: {snippet[:90]}")

    return matched_any

def main():
    parser = argparse.ArgumentParser(description="RSI Modular Memory Engine")
    parser.add_argument("--audit", action="store_true", help="Verify module compactness ceiling")
    parser.add_argument("--inject", nargs="*", help="Dynamically inject relevant rule modules for specified files")
    parser.add_argument("--diagnose", action="store_true", help="Instant pattern diagnosis on latest failed trajectory")
    args = parser.parse_args()

    if args.audit:
        success = audit_memory_modules()
        sys.exit(0 if success else 1)

    if args.diagnose:
        diagnose_trajectory()
        sys.exit(0)

    if args.inject is not None:
        if len(args.inject) == 0:
            print("Usage: --inject [file1] [file2] ...")
        else:
            print(resolve_context(args.inject))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
