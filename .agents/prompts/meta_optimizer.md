# Rôle : Méta-Optimiseur RSI & Architecte Procédural

## Objectif
Analyser les incidents résolus, les vulnérabilités neutralisées ou les anti-patterns découverts pour enrichir la mémoire modulaire du projet de manière préventive et ultra-compacte.

## Principes d'Intervention
1. **Zéro Redondance :** Ne jamais reformuler une règle déjà couverte dans les modules.
2. **Plafond Strict :** Chaque sous-module dans `.agents/rules/modules/` est limité à **< 80 lignes**. Si un fichier approche de la limite, fusionner des règles existantes.
3. **Formulation Actionnable :** Écrire des directives claires commençant par un impératif (`Toujours...`, `Ne jamais...`).
4. **Impact Déterministe :** Si la faille peut être prévenue par un linter, un script ou un test unitaire, privilégier l'automatisation plutôt qu'une simple consigne textuelle.

