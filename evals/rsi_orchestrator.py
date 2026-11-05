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
from datetime import datetime
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
ARCHIVE_DIR = ROOT_DIR / "docs" / "archive" / "tasks"
MODULES_DIR = ROOT_DIR / ".agents" / "rules" / "modules"
TRAJECTORY_FILE = ROOT_DIR / "evals" / "logs" / "trajectory_latest.json"
VERSION_FILE = ROOT_DIR / "VERSION"
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

def rollover_tasks(dry_run: bool = False) -> bool:
    """Deterministically archives completed [x] blocks from Active Sprint in docs/TASKS.md to docs/archive/tasks/."""
    if not TASKS_PATH.exists():
        print("[WARN] [RSI Rollover] docs/TASKS.md not found.")
        return False

    lines = TASKS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    before_count = len(lines)

    kept_lines = []
    archived_blocks = []
    current_archived_block = []
    in_active_sprint = False
    archiving_task = False

    task_closed_re = re.compile(r'^-\s*\[[xX]\]\s*\*\*`?(TASK-[A-Z0-9\-]+)`?')
    any_top_task_re = re.compile(r'^-\s*\[[ xX\-]\]\s*\*\*`?(TASK-[A-Z0-9\-]+)`?')

    for line in lines:
        if line.startswith("## Active Sprint"):
            in_active_sprint = True
            archiving_task = False
            kept_lines.append(line)
            continue

        if line.startswith("## ") and not line.startswith("## Active Sprint"):
            if current_archived_block:
                archived_blocks.append("\n".join(current_archived_block).rstrip())
                current_archived_block = []
            in_active_sprint = False
            archiving_task = False
            kept_lines.append(line)
            continue

        if in_active_sprint:
            if task_closed_re.match(line):
                if current_archived_block:
                    archived_blocks.append("\n".join(current_archived_block).rstrip())
                current_archived_block = [line]
                archiving_task = True
                continue
            elif any_top_task_re.match(line) or line.strip() == "---":
                if current_archived_block:
                    archived_blocks.append("\n".join(current_archived_block).rstrip())
                    current_archived_block = []
                archiving_task = False
                kept_lines.append(line)
                continue
            elif archiving_task:
                current_archived_block.append(line)
                continue

        kept_lines.append(line)

    if current_archived_block:
        archived_blocks.append("\n".join(current_archived_block).rstrip())

    if not archived_blocks:
        print(f"[INFO] [RSI Rollover] 0 completed [x] task blocks found in Active Sprint ({before_count}/{MAX_TASKS_LINES} lines).")
        return True

    archive_filename = f"sprint_archive_{datetime.now().strftime('%Y_%m')}.md"
    archive_path = ARCHIVE_DIR / archive_filename
    after_count = len(kept_lines)

    if dry_run:
        print(f"[INFO] [RSI Rollover Dry-Run] Would archive {len(archived_blocks)} completed task block(s) to docs/archive/tasks/{archive_filename}.")
        print(f"       Line count reduction: {before_count} -> {after_count}/{MAX_TASKS_LINES} lines.")
        return True

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    header = f"# Archived Sprint Tasks ({datetime.now().strftime('%Y-%m')})\n\n"
    existing = archive_path.read_text(encoding="utf-8") if archive_path.exists() else header
    if not existing.endswith("\n\n"):
        existing = existing.rstrip() + "\n\n"
    updated_archive = existing + "\n\n".join(archived_blocks) + "\n"
    archive_path.write_text(updated_archive, encoding="utf-8")

    TASKS_PATH.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")
    print(f"[OK] [RSI Rollover] Archived {len(archived_blocks)} completed task block(s) -> docs/archive/tasks/{archive_filename}")
    print(f"     docs/TASKS.md compacted: {before_count} -> {after_count}/{MAX_TASKS_LINES} lines.")
    return True

def run_session_pulse() -> None:
    """Outputs a <25 line Cold-Start Cockpit Briefing for instant agent situational awareness."""
    version = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "0.1.0"
    tasks_lines = len(TASKS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()) if TASKS_PATH.exists() else 0

    eval_status = "UNINITIALIZED"
    if TRAJECTORY_FILE.exists():
        try:
            tdata = json.loads(TRAJECTORY_FILE.read_text(encoding="utf-8"))
            eval_status = f"{tdata.get('status', 'UNKNOWN')} ({tdata.get('total_score', 0)}/100, mode={tdata.get('mode', 'FULL')})"
        except Exception:
            eval_status = "PARSE_ERROR"

    print(f"=== [RSI SESSION PULSE | Protocol v{version}] ===")
    print(f"1. Health & Judge : {eval_status} | TASKS.md capacity: {tasks_lines}/{MAX_TASKS_LINES} lines")

    # Active & pending tasks
    active = parse_active_tasks()
    if active:
        for t in active:
            t_files = ", ".join(t["targets"][:5]) if t["targets"] else "None declared"
            print(f"2. Active Task    : {t['id']} -> Targets: {t_files}")
    else:
        print("2. Active Task    : None marked [-]. Mark a task [-] in docs/TASKS.md before editing code.")

    # Working tree & scope status
    mod_files = get_modified_workspace_files()
    if mod_files:
        print(f"3. Git Workspace  : {len(mod_files)} modified file(s): {', '.join(mod_files[:5])}")
    else:
        print("3. Git Workspace  : Clean working tree (0 uncommitted changes)")

    check_scope_drift(strict=False)

    # Auto-resolve relevant rule modules for active target files + modified files
    candidate_files = list(mod_files)
    for t in active:
        candidate_files.extend(t["targets"])
    if candidate_files:
        try:
            from memory_engine import MODULE_TRIGGERS
            matched_mods = set()
            for cf in candidate_files:
                cf_low = cf.lower().replace("\\", "/")
                for mod, kw_list in MODULE_TRIGGERS.items():
                    if any(k in cf_low for k in kw_list):
                        matched_mods.add(mod)
            if matched_mods:
                print(f"4. Rule Modules   : {', '.join(sorted(matched_mods))} (run 'memory_engine.py --inject' to load)")
            else:
                print("4. Rule Modules   : system_core.md (default invariant rules)")
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="RSI Protocol Orchestrator")
    parser.add_argument("--pulse", action="store_true", help="1-command Cold-Start Cockpit Briefing (<50ms)")
    parser.add_argument("--eval", action="store_true", help="Execute reflexive evaluation")
    parser.add_argument("--attempt", type=int, default=1, help="Attempt number (1 to 3)")
    parser.add_argument("--guardrail", action="store_true", help="Verify integrity guardrails and task scope")
    parser.add_argument("--scope", action="store_true", help="Verify working tree alignment with active [-] task Target files")
    parser.add_argument("--strict-scope", action="store_true", help="Fail with exit code 1 on any scope drift or unregistered coding")
    parser.add_argument("--rollover", action="store_true", help="Archive completed [x] sprint blocks from docs/TASKS.md to docs/archive/tasks/")
    parser.add_argument("--dry-run", action="store_true", help="Preview --rollover without modifying files")
    args = parser.parse_args()

    if args.pulse:
        run_session_pulse()
        sys.exit(0)

    if args.rollover:
        ok = rollover_tasks(dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

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
