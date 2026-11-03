# 🧬 Protocole RSI (Recursive Self-Improvement) — Template Standalone

Ce répertoire contient le **Protocole RSI**, un moteur d'ingénierie et d'auto-amélioration déterministe pour agents d'intelligence artificielle, totalement découplé de tout projet spécifique.

---

## 📁 Architecture du Template

```
temp_rsi_protocol/
├── .agents/
│   ├── prompts/
│   │   └── meta_optimizer.md        # Rôle de réflexion et d'extraction de règles
│   ├── rules/
│   │   ├── system_core.md           # Règles immuables d'ingénierie
│   │   ├── fullstack_playbook.md    # Index et routeur de la mémoire procédurale
│   │   └── modules/                 # Sous-playbooks modulaires (< 80 lignes)
│   │       ├── api_backend.md
│   │       ├── db.md
│   │       ├── integration_ai.md
│   │       ├── security_auth.md
│   │       └── ui_frontend.md
│   └── workflows/
│       └── rsi-feature.md           # Workflow en 4 phases (Cadrage -> Éval -> Méta -> Clôture)
├── evals/
│   ├── memory_engine.py             # Résolution contextuelle & audit de compacité
│   ├── run_fullstack_eval.py        # Juge déterministe agnostique (multi-gestionnaires)
│   ├── stack_inspector.py           # Détection de stack & recommandation MCP/Skills
│   ├── rsi_orchestrator.py          # Boucles de retry (max 3) et guardrails
│   └── version_manager.py           # Incrémentation SemVer & scellement Changelog
├── docs/
│   ├── TASKS.md                     # Registre SSOT avec plafond de 250 lignes
│   └── archive/tasks/               # Dossier de rollover pour les tâches archivées
├── CHANGELOG.md                     # Journal des modifications SemVer
├── AGENTS.md                        # Charte officielle pour les agents IA
└── README.md                        # Ce fichier de documentation
```

---

## 🚀 Comment l'utiliser dans un nouveau projet

1. **Déplacer le contenu :**
   Copiez l'ensemble des dossiers `.agents/`, `evals/`, `docs/`, ainsi que `CHANGELOG.md` et `AGENTS.md` à la racine de votre nouveau projet.

2. **Ajouter les scripts dans votre `package.json` :**
   ```json
   "scripts": {
     "eval:quick": "python evals/run_fullstack_eval.py --quick",
     "eval:fullstack": "python evals/run_fullstack_eval.py",
     "rsi:inspect": "python evals/stack_inspector.py",
     "rsi:memory": "python evals/memory_engine.py --audit"
   }
   ```

3. **Exécuter le premier audit :**
   ```bash
   pnpm run rsi:inspect
   pnpm run eval:quick
   ```

