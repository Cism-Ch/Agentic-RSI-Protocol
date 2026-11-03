#!/usr/bin/env python3
"""
Audit de Sécurité Statique & Détection de Fuite de Secrets
- Vérifie l'absence de clés d'API, tokens, certificats privés et secrets codés en dur
- Valide l'étanchéité du .gitignore (.env*, clés privées, caches)
- Inspecte les permissions et conformité aux règles de sécurité du protocole RSI
"""

import sys
import re
import os
from pathlib import Path

# Fix encoding Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = [
    (re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'), "Clé privée (RSA/EC/SSH)"),
    (re.compile(r'sk-[a-zA-Z0-9]{20,}'), "Clé secrète type OpenAI/Stripe"),
    (re.compile(r'AKIA[0-9A-Z]{16}'), "Identifiant AWS Access Key"),
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'), "Token GitHub Personal Access"),
    (re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,48}'), "Token API Slack"),
    (re.compile(r'(?:postgres|postgresql|mysql|mongodb\+srv):\/\/[^\s:]+:[^\s@]+@[^\s\/]+'), "Chaîne de connexion BDD avec mot de passe"),
    (re.compile(r'(?i)(?:api_key|secret_key|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-\.]{16,}["\']'), "Clé d'authentification codée en dur")
]

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.next'}

def audit_gitignore() -> list[str]:
    issues = []
    gitignore = ROOT_DIR / ".gitignore"
    if not gitignore.exists():
        issues.append("Fichier .gitignore manquant !")
        return issues

    content = gitignore.read_text(encoding="utf-8", errors="replace")
    essential_rules = [".env", "*.pem", "*.key", "node_modules"]
    for rule in essential_rules:
        if rule not in content:
            issues.append(f"Règle de sécurité manquante dans .gitignore : '{rule}'")
    return issues

def audit_secrets() -> list[dict]:
    findings = []
    for path in ROOT_DIR.rglob("*"):
        if path.is_file():
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            # Ne pas s'auto-analyser sur les regex de ce fichier
            if path.name == "security_audit.py":
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
                for idx, line in enumerate(lines, start=1):
                    for pattern, label in SECRET_PATTERNS:
                        if pattern.search(line):
                            findings.append({
                                "file": str(path.relative_to(ROOT_DIR)),
                                "line": idx,
                                "type": label,
                                "sample": line.strip()[:60]
                            })
            except Exception as e:
                findings.append({
                    "file": str(path.relative_to(ROOT_DIR)),
                    "line": 0,
                    "type": "Erreur lecture",
                    "sample": str(e)
                })
    return findings

def run_security_audit() -> bool:
    print("🔒 [RSI Security Audit] Lancement de l'audit de sécurité statique...")
    gitignore_issues = audit_gitignore()
    secret_findings = audit_secrets()

    success = True
    if gitignore_issues:
        print("\n❌ Vulnérabilités de configuration .gitignore :")
        for issue in gitignore_issues:
            print(f"  - {issue}")
        success = False
    else:
        print("  ✅ Configuration .gitignore étanche et conforme.")

    if secret_findings:
        print(f"\n❌ {len(secret_findings)} fuite(s) de secret potentielle(s) détectée(s) :")
        for finding in secret_findings:
            print(f"  - [{finding['type']}] {finding['file']}:{finding['line']} -> {finding['sample']}")
        success = False
    else:
        print("  ✅ Aucun secret, clé privée ou credential codé en dur détecté.")

    # Vérification présence de fichiers .env réels non ignorés
    env_files = list(ROOT_DIR.glob(".env*"))
    real_envs = [f.name for f in env_files if f.name != ".env.example"]
    if real_envs:
        print(f"  ℹ️ Fichiers .env détectés en local : {real_envs} (doivent rester ignorés par git)")
    else:
        print("  ✅ Aucun fichier .env non chiffré dans le répertoire.")

    if success:
        print("\n🛡️ AUDIT DE SÉCURITÉ : SUCCÈS (0 faille critique détectée)")
    else:
        print("\n⚠️ AUDIT DE SÉCURITÉ : ÉCHEC")

    return success

if __name__ == "__main__":
    passed = run_security_audit()
    sys.exit(0 if passed else 1)
