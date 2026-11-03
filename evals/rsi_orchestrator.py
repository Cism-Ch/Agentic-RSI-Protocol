#!/usr/bin/env python3
"""
Orchestrateur RSI (Recursive Self-Improvement)
Pilote les boucles réflexives (jusqu'à 3 tentatives) et vérifie les guardrails d'intégrité :
- Vérification du score déterministe
- Guardrails : intégrité des modules (< 80 lignes) et plafonds de TASKS.md (< 250 lignes)
"""

import sys
import subprocess
import json
import argparse
from pathlib import Path

# UTF-8 pour Windows
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
    print(f"\n🔄 [RSI Loop] Lancement de l'évaluation déterministe — Tentative {attempt}/3...")
    eval_script = ROOT_DIR / "evals" / "run_fullstack_eval.py"
    cmd = [sys.executable, str(eval_script)]
    if quick:
        cmd.append("--quick")

    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=False)
    passed = res.returncode == 0

    if passed:
        print(f"🎉 [RSI Loop] Succès déterministe validé (Score: 100/100) à la tentative {attempt} !")
        return True
    else:
        print(f"⚠️ [RSI Loop] Échec de la tentative {attempt}. Consultez evals/logs/trajectory_latest.json.")
        return False

def check_guardrails() -> bool:
    print("\n🛡️ [RSI Guardrails] Contrôle strict d'intégrité...")
    passed = True

    # 1. Vérification de la compacité de TASKS.md
    if TASKS_PATH.exists():
        content = TASKS_PATH.read_text(encoding="utf-8")
        lines = len(content.splitlines())
        if lines > MAX_TASKS_LINES:
            print(f"❌ [Guardrail Violé] docs/TASKS.md contient {lines} lignes (> {MAX_TASKS_LINES}). Exécutez un Rollover vers docs/archive/tasks/ !")
            passed = False
        else:
            print(f"✅ docs/TASKS.md : {lines}/{MAX_TASKS_LINES} lignes")

    # 2. Vérification des modules de règles
    if MODULES_DIR.exists():
        for mod in MODULES_DIR.glob("*.md"):
            cnt = len([l for l in mod.read_text(encoding="utf-8").splitlines() if l.strip()])
            if cnt > MAX_MODULE_LINES:
                print(f"❌ [Guardrail Violé] {mod.name} contient {cnt} lignes (> {MAX_MODULE_LINES}). Synthétisez !")
                passed = False
            else:
                print(f"✅ {mod.name} : {cnt}/{MAX_MODULE_LINES} lignes")

    return passed

def main():
    parser = argparse.ArgumentParser(description="Orchestrateur du Protocole RSI")
    parser.add_argument("--eval", action="store_true", help="Exécuter une évaluation réflexive")
    parser.add_argument("--attempt", type=int, default=1, help="Numéro de tentative (1 à 3)")
    parser.add_argument("--guardrail", action="store_true", help="Vérifier uniquement les guardrails")
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

