# ⚡ Module : API & Backend

> Règle Anti-Bloat : Ce module ne doit JAMAIS dépasser **80 lignes**.

- [R-API-01] Renvoyer systématiquement des structures prévisibles de type `{ success: true, data } | { success: false, error }`.
- [R-API-02] Protéger les endpoints sensibles et les formulaires avec du rate-limiting.
- [R-API-03] Traiter les tâches lourdes de manière asynchrone via des workers ou files d'attente avec vérification de signature.
- [R-API-04] Rendre les jobs asynchrones strictement idempotents pour supporter les retries automatiques sans effets de bord.

