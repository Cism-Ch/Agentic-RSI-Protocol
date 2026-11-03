---
description: Développe une fonctionnalité de bout en bout avec cycle d'auto-amélioration RSI déterministe en 4 phases.
---

# Workflow : /rsi-feature

Ce workflow formalise le protocole d'auto-amélioration récursive (RSI) pour tout agent IA.  
Suis scrupuleusement ces 4 phases séquentielles sans en sauter aucune :

---

## 🚀 PHASE 1 : Préparation & Exécution Initiale

1. **Vérification SSOT Tâche (`docs/TASKS.md`) & Artefact IDE :**
   - Assure-toi que la tâche existe dans `docs/TASKS.md` sous la forme `TASK-DOMAINE-XX`.
   - Si elle n'existe pas, formalise-la immédiatement avec ID, priorité, description et critères cochables `[ ]`.
   - Passe son statut à `[-]` (En cours) dans le Kanban et la section active.
   - **Mémoire Épisodique (Artefact IDE) :** Si la tâche nécessite une planification multi-étapes ou un suivi étendu, initialise un Artefact Markdown (`plan.md` ou `task_tracking.md`) dans le dossier Brain de l'IDE. L'artefact sert de tableau de bord visuel hors contexte conversationnel. Ne jamais recopier l'intégralité d'un artefact dans les messages de chat pour préserver les tokens de contexte.

2. **Audit de Stack & Outillage Officiel (Skills & MCP) :**
   - Exécute `python evals/stack_inspector.py` (ou `pnpm run rsi:inspect`).
   - Vérifie qu'aucun outillage officiel (serveurs MCP, skills de framework/ORM) n'est manquant pour éviter de coder à l'aveugle.

3. **Résolution Dynamique de la Mémoire Contextuelle :**
   - Exécute `python evals/memory_engine.py --inject [fichiers_cibles]` pour charger exactement les sous-playbooks atomiques concernés (`.agents/rules/modules/`) sans saturer la fenêtre de contexte.
   - Lis `.agents/rules/system_core.md` pour les règles absolues du projet.

4. **Implémentation de Bout en Bout avec Cadence Anti-Saturation :**
   - **Micro-éditions locales :** Lors de l'écriture ou de l'ajustement de composants/fonctions, n'exécute pas de test global (`tsc`/`lint`). Laisser le flux d'édition se dérouler librement (0 token consommé).
   - **Backend / BDD :** Modélise la couche de données et l'API avec validation stricte en entrée (ex: Zod) et typage fort.
   - **Frontend :** Développe les interfaces avec gestion complète des états (`loading`, `error`, `empty`, `data`).
   - **Hygiène :** Utilise exclusivement les alias d'import propres, supprime les variables et imports inutilisés.

---

## 🧪 PHASE 2 : Évaluation Déterministe & Boucle Réflexive (Max 3 Tentatives)

1. **Exécution du Juge Déterministe (Cadence Jalon vs Clôture) :**
   - **En cours de tâche / Fin de jalon :** Exécute toujours le mode rapide compact :
     ```bash
     python evals/run_fullstack_eval.py --quick
     # ou pnpm run eval:quick
     ```
     La sortie JSON compacte (`failed_steps` tronqués à 10 lignes) évite de saturer la fenêtre de contexte de l'agent.
   - **Avant Clôture finale uniquement :** Exécute le test complet :
     ```bash
     python evals/run_fullstack_eval.py
     # ou pnpm run eval:fullstack
     ```

2. **Si le score est de 100/100 dès la Tentative 1 :**
   - Si la tâche était un **audit de sécurité, un débogage ou une refonte** ayant révélé et corrigé des failles du code existant : **Exécute la PHASE 3** pour consigner ces enseignements critiques dans le playbook.
   - S'il s'agissait d'une création de feature standard sans découverte d'anti-pattern : Passe directement à la **PHASE 4**.

3. **Si le score est inférieur à 100/100 :**
   - Lis le rapport d'échec compact dans `evals/logs/trajectory_latest.json`.
   - Identifie la cause exacte (Typecheck, Lint, Test, ou Schéma).
   - Corrige le code applicatif et relance :
     ```bash
     python evals/rsi_orchestrator.py --eval --attempt 2
     ```
   - Répète jusqu'à obtention du score 100/100 (maximum 3 tentatives).
   - *Si après 3 tentatives le score reste inférieur à 100, interromps le flux et sollicite l'arbitrage humain en expliquant le point de blocage.*

---

## 🧠 PHASE 3 : Mutation Méta-Cognitive (Apprentissage & Amélioration)

Cette phase s'exécute dès qu'un échec a été réparé (> 1 tentative) OU qu'un audit/refactoring a neutralisé des vulnérabilités ou anti-patterns :

1. Adopte le rôle défini dans `.agents/prompts/meta_optimizer.md`.
2. Identifie la couche défaillante (DB, Server Action, UI, Types, Sécurité).
3. Formule une règle générale préventive d'une à deux lignes (ex: `[R-DOM-XX] Toujours...`).
4. **Anti-Bloat & Modularité :** Vérifie que le sous-module cible dans `.agents/rules/modules/` ne dépasse pas 80 lignes. Si c'est le cas, fusionne les règles sémantiquement proches avant d'ajouter la nouvelle règle. Si le domaine est nouveau, crée un nouveau fichier modulaire `[domaine].md`.
5. Édite le sous-module ciblé dans `.agents/rules/modules/` et mets à jour `.agents/rules/fullstack_playbook.md`.

---

## 🛡️ PHASE 4 : Validation Finale, Git Guardrail & Clôture

1. **Vérification des Guardrails :**
   ```bash
   python evals/rsi_orchestrator.py --guardrail
   ```
2. **Double Vérification Déterministe :**
   - Typecheck (0 erreur).
   - Linter (0 erreur / warning).
3. **Scellement Automatique de Version SemVer :**
   - Exécute `python evals/version_manager.py --bump patch` pour incrémenter la version, sceller `CHANGELOG.md` et créer le tag Git.
4. **Clôture SSOT dans `docs/TASKS.md` :**
   - Coche tous les critères d'acceptation `[x]`.
   - Marque la tâche terminée `[x]`.
   - Transfère la tâche dans le tableau `Historique des Tâches Terminées` avec la date et la liste des fichiers créés/modifiés.
   - Mets à jour le tableau Kanban synthétique.
5. **Restitution à l'Utilisateur :**
   - Fonctionnalité livrée et validée à 100/100.
   - Version SemVer scellée.
   - Nombre de tentatives nécessaires.
   - Leçon apprise et nouvelle règle insérée (diff exact le cas échéant).

