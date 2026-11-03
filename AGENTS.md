# 🤖 AGENTS.md — Référence Agents IA & Protocole RSI

Ce document régit les directives d'ingénierie, la gouvernance de la codebase et le protocole d'auto-amélioration récursive (RSI).

---

### Résumé des Règles Inviolables

1. **Architecture & Typage Strict :** Zéro erreur de type, inférence forte et validation runtime systématique.
2. **Suivi des Tâches (SSOT Inviolable — `docs/TASKS.md`) :**
   - **Interdiction de coder sans tâche :** Tout travail DOIT être rattaché à une tâche formalisée dans `docs/TASKS.md` (`TASK-DOMAINE-XX`) avec description et critères cochables.
   - **Mise à jour en temps réel :** Marquer `[-]` au début, `[x]` à l'achèvement.
   - **Validation avant clôture :** Ne jamais marquer une tâche terminée sans avoir validé avec le juge déterministe (`python evals/run_fullstack_eval.py`).
   - **Plafond strict :** `docs/TASKS.md` ne doit jamais dépasser **250 lignes** (Rollover vers `docs/archive/tasks/`).
3. **Protocole RSI (Auto-Amélioration Récursive) :**
   - **Mémoire procédurale modulaire :** Consulter `.agents/rules/modules/` pour les règles spécialisées (< 80 lignes par fichier).
   - **Juge Déterministe Adaptatif :** Valider les développements avec `python evals/run_fullstack_eval.py --quick`.
   - **Boucle Méta-Cognitive :** Adopter le rôle `.agents/prompts/meta_optimizer.md` pour extraire les enseignements et enrichir les sous-playbooks en cas d'échec réparé ou d'audit de sécurité.
   - **Workflow Dédié :** Utiliser la commande `/rsi-feature`.
4. **Cadence des Tests Anti-Saturation :**
   - Micro-éditions sans test global -> Jalon avec `--quick` compact -> Clôture avec validation complète.
5. **Dualité Mémoire :**
   - Artefacts IDE pour le suivi épisodique de session ; fichiers `.agents/rules/modules/` pour la mémoire procédurale durable.

