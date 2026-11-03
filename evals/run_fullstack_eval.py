#!/usr/bin/env python3
"""
Juge Déterministe RSI Adaptatif & Agnostique
- Détection automatique du gestionnaire de paquets (pnpm, npm, yarn, bun)
- Exécution du typecheck et du linter si configurés
- Validation adaptative des schémas de BDD (Prisma, Drizzle, etc.) si présents
- Vérification de l'hygiène de la mémoire modulaire RSI
- Filtrage compact des erreurs (max 10 lignes signifiantes) pour préserver le contexte des agents IA
"""

import sys
import os
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime

# Configuration encodage console Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT_DIR / "evals" / "logs" / "trajectory_latest.json"

def detect_package_manager() -> str:
    if (ROOT_DIR / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (ROOT_DIR / "bun.lockb").exists() or (ROOT_DIR / "bun.lock").exists():
        return "bun"
    if (ROOT_DIR / "yarn.lock").exists():
        return "yarn"
    if (ROOT_DIR / "package-lock.json").exists():
        return "npm"
    return "pnpm"

def run_cmd(name: str, cmd_str: str, weight: int, timeout_sec: int = 180) -> dict:
    is_windows = os.name == "nt"
    try:
        res = subprocess.run(
            cmd_str,
            shell=True if is_windows else False,
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            encoding="utf-8",
            errors="replace"
        )
        passed = res.returncode == 0
        error_output = ""
        if not passed:
            raw_err = (res.stderr.strip() or res.stdout.strip())
            lines = [l for l in raw_err.split("\n") if l.strip()]
            error_output = "\n".join(lines[-10:]) if len(lines) > 10 else "\n".join(lines)
        return {
            "step": name,
            "passed": passed,
            "score": weight if passed else 0,
            "max_score": weight,
            "error_log": error_output.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            "step": name,
            "passed": False,
            "score": 0,
            "max_score": weight,
            "error_log": f"Timeout dépassé ({timeout_sec}s) lors de l'exécution de: {cmd_str}"
        }
    except Exception as e:
        return {
            "step": name,
            "passed": False,
            "score": 0,
            "max_score": weight,
            "error_log": str(e)
        }

def build_adaptive_checks(quick: bool) -> list[dict]:
    pm = detect_package_manager()
    py = sys.executable
    checks = []

    # 1. Typecheck (si TypeScript présent)
    if (ROOT_DIR / "tsconfig.json").exists():
        checks.append({
            "name": "typecheck",
            "cmd": f"{pm} exec tsc --noEmit",
            "weight": 30 if quick else 25,
            "timeout": 120
        })

    # 2. Linter (si configuré dans package.json)
    has_lint_script = False
    pkg_json = ROOT_DIR / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                has_lint_script = "lint" in data.get("scripts", {})
        except Exception:
            pass

    if has_lint_script:
        checks.append({
            "name": "lint",
            "cmd": f"{pm} run lint",
            "weight": 30 if quick else 25,
            "timeout": 240
        })

    # 3. Validation de BDD / ORM (Optionnelle et Adaptative)
    prisma_schema = ROOT_DIR / "prisma" / "schema.prisma"
    db_validator = ROOT_DIR / ".agents" / "skills" / "db_schema_validator.py"

    if prisma_schema.exists() and db_validator.exists():
        checks.append({
            "name": "prisma_hygiene",
            "cmd": f'"{py}" "{db_validator}"',
            "weight": 25 if quick else 15,
            "timeout": 60
        })
    elif (ROOT_DIR / "drizzle.config.ts").exists() or (ROOT_DIR / "drizzle.config.js").exists():
        checks.append({
            "name": "drizzle_check",
            "cmd": f"{pm} exec drizzle-kit check",
            "weight": 25 if quick else 15,
            "timeout": 60
        })

    # 4. Hygiène de la Mémoire Modulaire RSI
    memory_engine = ROOT_DIR / "evals" / "memory_engine.py"
    if memory_engine.exists():
        checks.append({
            "name": "rsi_memory_hygiene",
            "cmd": f'"{py}" "{memory_engine}" --audit',
            "weight": 15 if quick else 10,
            "timeout": 30
        })

    # 5. Audit de Sécurité Statique (Secrets & .gitignore)
    sec_audit = ROOT_DIR / "evals" / "security_audit.py"
    if sec_audit.exists():
        checks.append({
            "name": "security_audit",
            "cmd": f'"{py}" "{sec_audit}"',
            "weight": 15 if quick else 10,
            "timeout": 30
        })

    # 6. Build de Production (mode complet uniquement)
    if not quick and has_lint_script:
        pkg_has_build = False
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                pkg_has_build = "build" in data.get("scripts", {})
        except Exception:
            pass

        if pkg_has_build:
            checks.append({
                "name": "prod_build",
                "cmd": f"{pm} run build",
                "weight": 25,
                "timeout": 180
            })

    return checks

def main():
    parser = argparse.ArgumentParser(description="Juge Déterministe RSI Adaptatif & Agnostique")
    parser.add_argument("--quick", "-q", action="store_true", help="Ignorer le build de production pour une boucle rapide")
    args = parser.parse_args()

    check_configs = build_adaptive_checks(args.quick)
    executed_checks = []

    for cfg in check_configs:
        res = run_cmd(cfg["name"], cfg["cmd"], weight=cfg["weight"], timeout_sec=cfg["timeout"])
        executed_checks.append(res)

    total_score = sum(c["score"] for c in executed_checks)
    max_possible = sum(c["max_score"] for c in executed_checks)
    normalized_score = int((total_score / max_possible) * 100) if max_possible > 0 else 100

    failed_steps = [c for c in executed_checks if not c["passed"]]

    report = {
        "timestamp": datetime.now().isoformat(),
        "mode": "QUICK" if args.quick else "FULL",
        "total_score": normalized_score,
        "raw_score": total_score,
        "max_score": max_possible,
        "status": "PASS" if normalized_score == 100 else "FAIL",
        "failed_steps": failed_steps,
        "summary": {c["step"]: "PASSED" if c["passed"] else "FAILED" for c in executed_checks}
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    sys.exit(0 if normalized_score == 100 else 1)

if __name__ == "__main__":
    main()

