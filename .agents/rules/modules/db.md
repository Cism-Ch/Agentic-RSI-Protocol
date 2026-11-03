# 🗄️ Module : Base de Données & Persistance

> Règle Anti-Bloat : Ce module ne doit JAMAIS dépasser **80 lignes**.

- [R-DB-01] Valider systématiquement les données entrantes via un schéma de validation (ex. Zod) avant toute écriture en base.
- [R-DB-02] Utiliser un client singleton pour éviter l'épuisement des connexions sur les runtimes serverless.
- [R-DB-03] Ne jamais faire de mutations destructives non indexées sur de grands volumes.
- [R-DB-04] Toujours isoler les identifiants uniques selon la spécification de l'adaptateur de base de données.

