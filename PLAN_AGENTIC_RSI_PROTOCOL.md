# Plan d'Implementation : Agentic-RSI-Protocol v2.2 (Fiabilisation Multi-Taches, Contrat JSON & Deploiement OfferAnalyst)

> **Objectif :** Finaliser l'integration entre `Agentic-RSI-Protocol` (v2.1 deja implemente) et `cognitive-rsi-ops` v2.2 en garantissant l'isolation stricte des sessions de tokens par tache, la validation automatique du contrat JSON, et le deploiement reel sur le projet pilote `OfferAnalyst`.

---

## 1. Contexte & Acquis (v2.1 Termine)

Les commits recents sur `Agentic-RSI-Protocol` (`105d7cd`, `04a5eb4`, `46eb1e6`) ont deja livre :
- Le chronometrage par etape (`duration_ms`) dans `evals/run_fullstack_eval.py`.
- Le suivi de session active (`.agents/telemetry/active_session.json`) dans `evals/memory_engine.py`.
- Le rapport de Scope Drift, `sprint_id`, `task_elapsed_sec` et l'appel automatique au hook dans `evals/rsi_orchestrator.py`.
- L'extraction des tokens reels depuis `transcript.jsonl` dans `evals/telemetry_hook.py`.
- La commande de synchronisation `--sync-to` dans `evals/rsi_orchestrator.py`.

**Points a verrouiller avant le passage en production sur `OfferAnalyst` :**
1. **Isolation des tokens entre deux taches** : Si une tache est interrompue ou remplacee sans `PASS`, `session_started_at` dans `active_session.json` risque de cumuler les tokens de la tache precedente depuis `transcript.jsonl`.
2. **Transmission complete vers `cognitive-rsi-ops`** : Verifier que `telemetry_hook.py` transmet bien `scope_report`, `checks` (`duration_ms`), `telemetry_source`, `injected_rule_ids` et les vrais compteurs de tokens sans perte ni fallback silencieux.
3. **Validation du contrat JSON & Deploiement `OfferAnalyst`** : Aucun test automatise ne verifie encore la conformite de `trajectory_latest.json` et `cognitive_state.json` apres `--sync-to`.

---

## 2. Modifications Proposees par Composant

### 2.1 Isolation Hermetique des Sessions (`evals/rsi_orchestrator.py` & `evals/memory_engine.py`)

#### [MODIFY] `evals/rsi_orchestrator.py`
- **Lors de `--pulse`** :
  - Comparer le `task_id` courant de `docs/TASKS.md` avec `active_session.json["task_id"]`.
  - Si le `task_id` a change (tache precedente abandonnee ou basculee manuellement), reinitialiser immediatement `session_started_at` a `now()` (UTC) et vider `injected_rule_ids` / `last_diagnosis_matches` pour eviter toute contamination des tokens entre taches.
- **Horodatage de fin de tentative** :
  - Mettre a jour `last_eval_at` dans `active_session.json` apres chaque `--eval`, afin que si une tache echoue (`attempt 1`) puis reussit (`attempt 2`), les etapes entre les deux tentatives soient comptabilisees proprement sans double comptage lors d'un re-enregistrement.

---

### 2.2 Fiabilisation du Hook & Verification de Contrat (`evals/telemetry_hook.py`)

#### [MODIFY] `evals/telemetry_hook.py`
- **Alignement strict du payload `cognitive_state.json`** :
  - S'assurer que lors d'une ecriture autonome (ou via `cognitive-rsi-ops/cli.py record`), les champs suivants sont systematiquement ecrits sur le run :
    - `telemetry_source` (`"LIVE_TRANSCRIPT"` ou `"ESTIMATED_FALLBACK"`).
    - `scope_report` (copie depuis `evals/logs/trajectory_latest.json`).
    - `trajectory.steps` avec `ms` = `duration_ms` de chaque check (`typecheck`, `lint`, `prod_build`, etc.).
    - `injected_rules` (liste des `[R-DOM-XX]` credites).
    - `metrics.prompt_tokens`, `metrics.output_tokens`, `metrics.cached_tokens`, `metrics.useful_actions`, `metrics.wasted_actions`.
- **Nouvelle option CLI `--verify-contract`** :
  - Verifier que `evals/logs/trajectory_latest.json` et `.agents/telemetry/cognitive_state.json` existent, sont du JSON valide, contiennent les cles attendues par `cognitive-rsi-ops`, et afficher un resume clair (`PASS` / `FAIL` en Pure ASCII).

---

### 2.3 Deploiement & Validation Reelle sur `OfferAnalyst`

#### [SYNC] Projet Pilote `../OfferAnalyst`
1. **Synchroniser le protocole** depuis `Agentic-RSI-Protocol` vers `OfferAnalyst` :
   ```bash
   python evals/rsi_orchestrator.py --sync-to ../OfferAnalyst
   ```
2. **Verifier l'integrite des regles locales d'`OfferAnalyst`** :
   - Confirmer qu'aucune regle locale (`[R-DOM-XX]`) dans `OfferAnalyst/.agents/rules/modules/` n'a ete ecrasee ou supprimee (invariant Zero-Deletion).
   - Verifier que `OfferAnalyst/AGENTS.md` reference bien le cycle `--pulse` -> `--inject` -> `--eval`.
3. **Executer un cycle de validation reel sur `OfferAnalyst`** :
   ```bash
   python evals/rsi_orchestrator.py --pulse
   python evals/rsi_orchestrator.py --eval --attempt 1 --quick
   python evals/telemetry_hook.py --verify-contract
   ```

---

## 3. Plan de Verification (Commandes Exactes)

1. **Compilation & Pure ASCII sur `Agentic-RSI-Protocol`** :
   ```bash
   python -m py_compile evals/memory_engine.py evals/run_fullstack_eval.py evals/rsi_orchestrator.py evals/telemetry_hook.py
   ```
2. **Test d'isolation de session & contrat JSON** :
   ```bash
   python evals/rsi_orchestrator.py --pulse
   python evals/memory_engine.py --inject evals/memory_engine.py
   python evals/rsi_orchestrator.py --eval --attempt 1
   python evals/telemetry_hook.py --verify-contract
   ```
3. **Validation Croisee dans `cognitive-rsi-ops`** :
   - Lancer `python cli.py status` et ouvrir le Dashboard sur `OfferAnalyst` pour confirmer que le mode est `FULL_RSI_PROTOCOL`, que les tokens sont `ACTIVE_REAL`, et que la carte d'economie de tokens affiche des donnees reelles.
