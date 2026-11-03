#!/usr/bin/env python3
"""
RSI Orchestrator (Recursive Self-Improvement)
Drives reflexive retry loops (up to 3 attempts) and verifies integrity guardrails:
- Deterministic score validation
- Guardrails: rule modules compactness (< 80 lines) and TASKS.md ceiling (< 250 lines)
"""

import sys
import subprocess
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
TASKS_PATH = ROOT_DIR / "docs" / "TASKS.md"
MODULES_DIR = ROOT_DIR / ".agents" / "rules" / "modules"
MAX_TASKS_LINES = 250
MAX_MODULE_LINES = 80

def run_evaluation(attempt: int, quick: bool = True) -> bool:
    print(f"\n🔄 [RSI Loop] Launching deterministic evaluation — Attempt {attempt}/3...")
    eval_script = ROOT_DIR / "evals" / "run_fullstack_eval.py"
    cmd = [sys.executable, str(eval_script)]
    if quick:
        cmd.append("--quick")

    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=False)
    passed = res.returncode == 0

    if passed:
        print(f"🎉 [RSI Loop] Deterministic validation passed (Score: 100/100) on attempt {attempt}!")
        return True
    else:
        print(f"⚠️ [RSI Loop] Attempt {attempt} failed. Inspect evals/logs/trajectory_latest.json.")
        return False

def check_guardrails() -> bool:
    print("\n🛡️ [RSI Guardrails] Running strict integrity check...")
    passed = True

    # 1. Compactness check for docs/TASKS.md
    if TASKS_PATH.exists():
        content = TASKS_PATH.read_text(encoding="utf-8")
        lines = len(content.splitlines())
        if lines > MAX_TASKS_LINES:
            print(f"❌ [Guardrail Violated] docs/TASKS.md contains {lines} lines (> {MAX_TASKS_LINES}). Run rollover to docs/archive/tasks/!")
            passed = False
        else:
            print(f"✅ docs/TASKS.md: {lines}/{MAX_TASKS_LINES} lines")

    # 2. Compactness check for rule modules
    if MODULES_DIR.exists():
        for mod in MODULES_DIR.glob("*.md"):
            cnt = len([l for l in mod.read_text(encoding="utf-8").splitlines() if l.strip()])
            if cnt > MAX_MODULE_LINES:
                print(f"❌ [Guardrail Violated] {mod.name} contains {cnt} lines (> {MAX_MODULE_LINES}). Summarize it!")
                passed = False
            else:
                print(f"✅ {mod.name}: {cnt}/{MAX_MODULE_LINES} lines")

    return passed

def main():
    parser = argparse.ArgumentParser(description="RSI Protocol Orchestrator")
    parser.add_argument("--eval", action="store_true", help="Execute reflexive evaluation")
    parser.add_argument("--attempt", type=int, default=1, help="Attempt number (1 to 3)")
    parser.add_argument("--guardrail", action="store_true", help="Only verify integrity guardrails")
    args = parser.parse_args()

    if args.guardrail:
        ok = check_guardrails()
        print(json.dumps({"passed": ok}, indent=2))
        sys.exit(0 if ok else 1)

    if args.eval:
        success = run_evaluation(args.attempt)
        sys.exit(0 if success else 1)

    parser.print_help()

if __name__ == "__main__":
    main()
