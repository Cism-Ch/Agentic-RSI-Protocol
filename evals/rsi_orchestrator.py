#!/usr/bin/env python3
"""
RSI Orchestrator (Recursive Self-Improvement)
Drives reflexive retry loops (up to 3 attempts) and verifies integrity guardrails:
- Deterministic score validation
- Guardrails: rule modules compactness (< 80 lines) and TASKS.md ceiling (< 250 lines)
"""

import sys
import re
import fnmatch
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
ALWAYS_ALLOWED_GOVERNANCE_FILES = {"docs/TASKS.md", "CHANGELOG.md", "VERSION"}

def run_evaluation(attempt: int, quick: bool = True) -> bool:
    print(f"\n[RSI Loop] Launching deterministic evaluation - Attempt {attempt}/3...")
    eval_script = ROOT_DIR / "evals" / "run_fullstack_eval.py"
    cmd = [sys.executable, str(eval_script)]
    if quick:
        cmd.append("--quick")

    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=False)
    passed = res.returncode == 0

    if passed:
        print(f"[OK] [RSI Loop] Deterministic validation passed (Score: 100/100) on attempt {attempt}!")
        return True
    else:
        print(f"[WARN] [RSI Loop] Attempt {attempt} failed. Inspect evals/logs/trajectory_latest.json.")
        return False

def parse_active_tasks() -> list[dict]:
    """Extracts currently active [-] tasks (or the just-closed topmost [x] sprint task pre-commit) from docs/TASKS.md."""
    if not TASKS_PATH.exists():
        return []

    lines = TASKS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    active_tasks = []
    closed_sprint_tasks = []
    current_task = None
    in_active_sprint = False

    task_active_re = re.compile(r'^-\s*\[-\]\s*\*\*`?(TASK-[A-Z0-9\-]+)`?')
    task_closed_re = re.compile(r'^-\s*\[[xX]\]\s*\*\*`?(TASK-[A-Z0-9\-]+)`?')
    any_top_task_re = re.compile(r'^-\s*\[[ xX\-]\]\s*\*\*`?(TASK-[A-Z0-9\-]+)`?')

    for line in lines:
        if line.startswith("## Active Sprint"):
            in_active_sprint = True
            current_task = None
            continue
        if line.startswith("## ") and not line.startswith("## Active Sprint"):
            in_active_sprint = False
            current_task = None
            continue

        m_active = task_active_re.match(line)
        if m_active:
            current_task = {"id": m_active.group(1), "targets": []}
            active_tasks.append(current_task)
            continue

        m_closed = task_closed_re.match(line)
        if in_active_sprint and m_closed:
            current_task = {"id": m_closed.group(1), "targets": []}
            closed_sprint_tasks.append(current_task)
            continue

        if any_top_task_re.match(line):
            current_task = None
            continue

        if current_task is not None and "Target files:" in line:
            targets = re.findall(r'`([^`]+)`', line)
            current_task["targets"].extend(t.replace("\\", "/").strip() for t in targets)

    if active_tasks:
        return active_tasks
    # During Phase 4 closure (right after marking [-] -> [x] and before git commit), use the latest closed task
    return closed_sprint_tasks[:1]

def get_modified_workspace_files() -> list[str]:
    """Returns git-modified and untracked files relative to ROOT_DIR."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=False
        )
        if res.returncode != 0:
            return []
        modified = []
        for raw_line in res.stdout.splitlines():
            if len(raw_line) < 4:
                continue
            path_part = raw_line[3:].strip()
            if " -> " in path_part:
                path_part = path_part.split(" -> ")[-1].strip()
            path_part = path_part.strip('"').replace("\\", "/")
            if path_part.endswith("/"):
                dir_path = ROOT_DIR / path_part
                if dir_path.exists():
                    for sub in dir_path.rglob("*"):
                        if sub.is_file():
                            modified.append(str(sub.relative_to(ROOT_DIR)).replace("\\", "/"))
            else:
                modified.append(path_part)
        return sorted(set(modified))
    except Exception:
        return []

def matches_target_pattern(file_path: str, patterns: list[str]) -> bool:
    if file_path in ALWAYS_ALLOWED_GOVERNANCE_FILES:
        return True
    for pat in patterns:
        if file_path == pat:
            return True
        if fnmatch.fnmatch(file_path, pat):
            return True
        if "**/" in pat:
            prefix = pat.split("**/")[0]
            if file_path.startswith(prefix):
                return True
        if pat.endswith("/") and file_path.startswith(pat):
            return True
    return False

def check_scope_drift(strict: bool = False) -> bool:
    """Verifies that git working tree changes align with an active [-] task in docs/TASKS.md."""
    modified_files = [
        f for f in get_modified_workspace_files()
        if f not in ALWAYS_ALLOWED_GOVERNANCE_FILES
    ]
    active_tasks = parse_active_tasks()

    if not modified_files:
        print("[OK] Scope Guard: Working tree is clean (0 out-of-scope edits).")
        return True

    if not active_tasks:
        tag = "[FAIL]" if strict else "[WARN]"
        print(f"{tag} [Scope Guard] {len(modified_files)} file(s) modified without an active [-] task in docs/TASKS.md:")
        for mf in modified_files[:10]:
            print(f"  - {mf}")
        return not strict

    all_targets = []
    task_ids = []
    for t in active_tasks:
        task_ids.append(t["id"])
        all_targets.extend(t["targets"])

    out_of_scope = [f for f in modified_files if not matches_target_pattern(f, all_targets)]
    if out_of_scope:
        tag = "[FAIL]" if strict else "[WARN]"
        print(f"{tag} [Scope Drift] {len(out_of_scope)} modified file(s) outside declared Target files for {', '.join(task_ids)}:")
        for oof in out_of_scope:
            print(f"  - {oof} (Declare in docs/TASKS.md Target files or revert)")
        return not strict

    print(f"[OK] Scope Guard: All {len(modified_files)} modified file(s) align with active task(s) ({', '.join(task_ids)}).")
    return True

def check_guardrails(strict_scope: bool = False) -> bool:
    print("\n[RSI Guardrails] Running strict integrity check...")
    passed = True

    # 1. Compactness check for docs/TASKS.md
    if TASKS_PATH.exists():
        content = TASKS_PATH.read_text(encoding="utf-8")
        lines = len(content.splitlines())
        if lines > MAX_TASKS_LINES:
            print(f"[FAIL] [Guardrail Violated] docs/TASKS.md contains {lines} lines (> {MAX_TASKS_LINES}). Run rollover to docs/archive/tasks/!")
            passed = False
        else:
            print(f"[OK] docs/TASKS.md: {lines}/{MAX_TASKS_LINES} lines")

    # 2. Compactness check for rule modules
    if MODULES_DIR.exists():
        for mod in sorted(MODULES_DIR.glob("*.md")):
            cnt = len([l for l in mod.read_text(encoding="utf-8").splitlines() if l.strip()])
            if cnt > MAX_MODULE_LINES:
                print(f"[FAIL] [Guardrail Violated] {mod.name} contains {cnt} lines (> {MAX_MODULE_LINES}). Summarize or split it!")
                passed = False
            else:
                print(f"[OK] {mod.name}: {cnt}/{MAX_MODULE_LINES} lines")

    # 3. Scope drift check against active [-] task in docs/TASKS.md
    scope_ok = check_scope_drift(strict=strict_scope)
    if not scope_ok:
        passed = False

    return passed

def main():
    parser = argparse.ArgumentParser(description="RSI Protocol Orchestrator")
    parser.add_argument("--eval", action="store_true", help="Execute reflexive evaluation")
    parser.add_argument("--attempt", type=int, default=1, help="Attempt number (1 to 3)")
    parser.add_argument("--guardrail", action="store_true", help="Verify integrity guardrails and task scope")
    parser.add_argument("--scope", action="store_true", help="Verify working tree alignment with active [-] task Target files")
    parser.add_argument("--strict-scope", action="store_true", help="Fail with exit code 1 on any scope drift or unregistered coding")
    args = parser.parse_args()

    if args.scope or args.strict_scope:
        ok = check_scope_drift(strict=args.strict_scope)
        sys.exit(0 if ok else 1)

    if args.guardrail:
        ok = check_guardrails(strict_scope=args.strict_scope)
        print(json.dumps({"passed": ok}, indent=2))
        sys.exit(0 if ok else 1)

    if args.eval:
        success = run_evaluation(args.attempt)
        sys.exit(0 if success else 1)

    parser.print_help()

if __name__ == "__main__":
    main()
