# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-11-24

### Added
- UI & Structural Integrity (Anti-AI Slop) and Secure-by-Default Endpoint/Upload rules in `AGENTS.md`, `.agents/rules/system_core.md`, `.agents/workflows/rsi-feature.md`, and `.agents/rules/modules/` (`ui_frontend.md`, `api_backend.md`, `security_auth.md`).
- Non-destructive `AGENTS.md` sync (`sync_agents_md_safely()` in `evals/version_manager.py`) using `<!-- RSI-PROTOCOL:START / END -->` markers, automatic backup of pre-existing custom `AGENTS.md` to `evals/backups/AGENTS.md.<timestamp>.bak`, and human-review `[ACTION REQUIRED]` prompt.

## [0.2.0] - 2026-11-21

### Added
- Automated target project sync CLI (`--sync-to`, `--init-target`, `--sync-targets`, `--sync-all`) with local git-ignored target registry (`.agents/telemetry/sync_targets.json`), automatic `package.json` 9-script injection, and idempotent target `.gitignore` hygiene.
- Fail-Loud Honesty & Zero Reward Hacking invariant rule (`.agents/rules/system_core.md`, `AGENTS.md`) and formal `[!] BLOCKED` escalation status in `docs/TASKS.md` and `evals/rsi_orchestrator.py --pulse`.
- Supply-chain & agent integrity guard (`audit_supply_chain_and_agent_integrity()`), private target/host path leak guard (`audit_private_context_leaks()`), safe target directory validation (`validate_safe_target_dir()`), and `ALLOWED_SYNC_EVAL_FILES` allowlist.
- Standard-library protocol engine unit test suite (`evals/tests/test_evals.py`, 12 tests) integrated directly into `evals/run_fullstack_eval.py`.
- Dynamic LLM model slugification and tier-based fallback pricing in `evals/telemetry_hook.py` supporting any current or future model family.
- AI Operating System architecture mapping, `Plan -> Act -> Evaluate -> Improve` lifecycle, and Applied Harness-Level RSI documentation in `README.md`.

### Changed
- Eliminated `shell=True` in `evals/run_fullstack_eval.py` (using `shutil.which` and `shell=False`), added path confinement and CPU/RAM caps in `evals/stack_inspector.py`, and hardened `.github/workflows/ci.yml` and `release.yml` with least-privilege permissions and timeouts.
- Optimized `evals/security_audit.py` with whole-file C regex pre-filtering and lockfile/binary/telemetry exclusions.
- Scoped strict ASCII validation to `evals/**/*.py` (preserving accented Markdown prose) and `new PrismaClient()` detection to `src/` application code.
- Exempted synced protocol files from `Scope Guard` drift warnings in consumer repositories while preserving strict enforcement on the source protocol repo.
