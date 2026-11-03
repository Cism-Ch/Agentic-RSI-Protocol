# 🛡️ System Core Rules — Règles Fondamentales d'Ingénierie du Projet

> **STATUT : IMMUABLE.** Ces règles constituent le contrat technique non négociable du projet.  
> Tout agent IA DOIT s'y conformer strictement avant et pendant chaque tâche.

---

## 1. ⚡ Règles Fondamentales

1. **Typage Strict :** Zéro erreur de compilation de type (`tsc --noEmit` ou équivalent selon langage).
2. **Qualité & Linter :** 0 avertissement ou erreur sur la suite de linting officielle.
3. **Architecture & Modularité :** Séparer clairement la couche de données, les routes/APIs et la présentation.
4. **Sécurité & Secrets :** Ne JAMAIS commiter ou exposer de clés privées, tokens ou mots de passe. Conserver l'intégrité absolue des variables d'environnement.
5. **Gestion des Erreurs :** Toujours typer et capturer les erreurs de manière prédictible.
6. **Cadence des Tests Anti-Saturation :**
   - *Niveau 1 (Micro-éditions) :* Ne pas exécuter de suite globale à chaque retouche pour laisser le flux fluide.
   - *Niveau 2 (Fin de composant / Jalon) :* Valider avec `python evals/run_fullstack_eval.py --quick` qui renvoie un rapport JSON compacté.
   - *Niveau 3 (Clôture de tâche) :* Exécuter la suite complète avec 0 erreur tolérée.
7. **Dualité Mémoire (Artefacts IDE vs Règles Procédurales) :**
   - *Mémoire Épisodique :* Utiliser les Artefacts IDE pour le suivi de session, les plans complexes et les rapports sans saturer le chat.
   - *Mémoire Procédurale :* Enrichir exclusivement les modules ciblés dans `.agents/rules/modules/` (< 80 lignes par fichier).

---

## 2. 📋 SSOT Inviolable — Gestion des Tâches (`docs/TASKS.md`)

- **Interdiction de coder sans tâche :** Tout travail doit correspondre à une entrée formalisée (`TASK-DOMAINE-XX`) dans `docs/TASKS.md`.
- **Mise à jour en temps réel :** Marquer `[-]` (En cours) dès le démarrage ; cocher `[x]` à l'achèvement.
- **Plafond strict :** `docs/TASKS.md` ne doit pas dépasser 250 lignes (Rollover périodique vers `docs/archive/tasks/`).

