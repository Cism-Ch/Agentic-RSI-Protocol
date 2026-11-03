# 🧠 Index & Routeur de la Mémoire Procédurale RSI

> Ce fichier sert de catalogue et d'index de routage vers les sous-modules de mémoire situés dans `.agents/rules/modules/`.  
> L'agent IA utilise le moteur `evals/memory_engine.py --inject [fichiers]` pour charger dynamiquement uniquement les règles du domaine concerné.

---

### Cartographie des Sous-Modules Spécialisés (< 80 lignes par fichier)

| Domaine | Fichier de Règle | Périmètre & Déclencheurs |
| :--- | :--- | :--- |
| **Base de Données** | [db.md](modules/db.md) | Modélisation, migrations, transactions, validation de schéma ORM. |
| **API & Backend** | [api_backend.md](modules/api_backend.md) | Routes serveur, actions, background jobs, cache, idempotence. |
| **Frontend & UI** | [ui_frontend.md](modules/ui_frontend.md) | Composants, accessibilité, styles, mobile-first, gestion des 4 états. |
| **Sécurité & Auth** | [security_auth.md](modules/security_auth.md) | Authentification, sessions, rôles, chiffrement, sanitisation. |
| **Intégration IA** | [integration_ai.md](modules/integration_ai.md) | Modèles LLM, invites, gestion des clés API, parsing structuré. |

