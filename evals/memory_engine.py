#!/usr/bin/env python3
"""
Moteur de Résolution et d'Audit de la Mémoire Modulaire RSI
- Indexation et chargement contextuel ciblé des sous-playbooks (.agents/rules/modules/)
- Vérification anti-bloat (< 80 lignes par sous-module)
- Entièrement générique et réutilisable pour tout projet
"""

import sys
import os
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
    """Vérifie que chaque module reste strictement sous le seuil maximal de lignes."""
    if not MODULES_DIR.exists():
        print(f"⚠️ [RSI Memory Audit] Répertoire des modules introuvable à {MODULES_DIR}")
        return True

    modules = list(MODULES_DIR.glob("*.md"))
    if not modules:
        print("ℹ️ [RSI Memory Audit] Aucun module trouvé.")
        return True

    print(f"📊 [RSI Memory Audit] {len(modules)} modules détectés.")
    has_violation = False

    for mod in modules:
        try:
            content = mod.read_text(encoding="utf-8")
            line_count = len([line for line in content.splitlines() if line.strip()])
            if line_count > MAX_LINES_PER_MODULE:
                print(f"  ❌ {mod.name} : {line_count}/{MAX_LINES_PER_MODULE} lignes (SEUIL DÉPASSÉ !)")
                has_violation = True
            else:
                print(f"  ✅ {mod.name} : {line_count}/{MAX_LINES_PER_MODULE} lignes")
        except Exception as e:
            print(f"  ⚠️ Erreur de lecture de {mod.name}: {e}")

    if has_violation:
        print("\n❌ ÉCHEC : Certains modules dépassent la limite autorisée. Synthétisez ou fractionnez !")
        return False
    else:
        print("\n✅ Tous les modules respectent le plafond strict de compacité !")
        return True

def resolve_context(files: list[str]) -> str:
    """Détermine quels modules charger en fonction des fichiers passés en paramètre."""
    matched_modules = set()
    for f in files:
        f_lower = f.lower().replace("\\", "/")
        for mod, keywords in MODULE_TRIGGERS.items():
            if any(k in f_lower for k in keywords):
                matched_modules.add(mod)

    if not matched_modules:
        return "ℹ️ Aucun sous-playbook spécifique requis pour ces fichiers. Consultez fullstack_playbook.md si besoin."

    output = ["🧠 [RSI Dynamic Memory Injection]"]
    for mod in sorted(matched_modules):
        mod_path = MODULES_DIR / mod
        if mod_path.exists():
            output.append(f"\n--- 📖 Module: {mod} ---")
            output.append(mod_path.read_text(encoding="utf-8").strip())

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Moteur de Mémoire Modulaire RSI")
    parser.add_argument("--audit", action="store_true", help="Vérifier la compacité des modules")
    parser.add_argument("--inject", nargs="*", help="Injecter dynamiquement les modules pertinents pour les fichiers spécifiés")
    args = parser.parse_args()

    if args.audit:
        success = audit_memory_modules()
        sys.exit(0 if success else 1)

    if args.inject is not None:
        if len(args.inject) == 0:
            print("Usage: --inject [fichier1] [fichier2] ...")
        else:
            print(resolve_context(args.inject))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()

