# 📋 TASKS.md — Registre Central & Suivi Unifié des Tâches (Template RSI)

> **Source Unique de Vérité (SSOT)** pour le pilotage et le suivi de toutes les tâches techniques et fonctionnelles.  
> **Règle absolue pour tout Agent IA :** Ce document DOIT être consulté avant toute tâche et mis à jour immédiatement après chaque réalisation. Plafond strict : **250 lignes**.

---

## 📌 Vue Kanban Synthétique

```
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│ 🚀 EN COURS (SPRINT 01) │  │   ⏳ BACKLOG FUTUR      │  │       ✅ ARCHIVES       │
├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────────┤
│ [ ] TASK-INIT-01        │  │ [ ] Tâche future 1      │  │ [x] TASK-GIT-01         │
│                         │  │                         │  │                         │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

---

## 🚀 Sprint 01 En cours : Initialisation du Projet

- [x] **`TASK-GIT-01` — Initialisation Git & Audits de Sécurité**
  - **Priorité :** 🔴 HAUTE
  - **Fichiers cibles :** `.gitignore`, `evals/security_audit.py`, `evals/run_fullstack_eval.py`, `docs/TASKS.md`
  - **Critères d'acceptation :**
    - [x] `TASK-GIT-01.01` : Création du `.gitignore` complet et sécurisé (protection des secrets, `.env*`, clés privées, logs).
    - [x] `TASK-GIT-01.02` : Initialisation du dépôt Git avec branche principale `main`.
    - [x] `TASK-GIT-01.03` : Tests de sécurité (détection de fuites de secrets, analyse des fichiers d'environnement, vérification des règles de sécurité).
    - [x] `TASK-GIT-01.04` : Validation déterministe avec `python evals/run_fullstack_eval.py` (100/100 PASS).

- [ ] **`TASK-INIT-01` — Cadrage & Mise en Place Initiale du Projet**
  - **Priorité :** 🟡 MOYENNE
  - **Fichiers cibles :** `package.json`, `README.md`
  - **Critères d'acceptation :**
    - [ ] `TASK-INIT-01.01` : Configuration du socle technique et des dépendances.
    - [ ] `TASK-INIT-01.02` : Validation déterministe avec `python evals/run_fullstack_eval.py --quick` (100/100 PASS).

---

## 📜 Historique des Tâches Terminées

| Date | ID Tâche | Titre & Description | Fichiers Créés / Modifiés |
| :--- | :--- | :--- | :--- |
| 2026-11-03 | TASK-GIT-01 | Initialisation Git & Audits de Sécurité | `.gitignore`, `evals/security_audit.py`, `evals/run_fullstack_eval.py`, `docs/TASKS.md` |

