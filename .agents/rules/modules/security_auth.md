# 🔒 Module : Sécurité, Auth & Données Sensibles

> Règle Anti-Bloat : Ce module ne doit JAMAIS dépasser **80 lignes**.

- [R-SEC-01] Valider impérativement les sessions et permissions côté serveur en tête de contrôleur ou d'action.
- [R-SEC-02] Ne JAMAIS renvoyer de hashs de mots de passe, tokens ou clés privées au client.
- [R-SEC-03] Chiffrer au repos (AES-256) toutes les clés secrètes ou données sensibles fournies par les utilisateurs.
- [R-SEC-04] Assurer l'intégrité absolue des variables d'environnement (`.env`) sans jamais effacer de clés existantes.

