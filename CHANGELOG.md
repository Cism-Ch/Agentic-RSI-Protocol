# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-11-27

### Added
- Automatic `FAIL -> PASS` `rsi_learning_trigger` in `evals/run_fullstack_eval.py` and `evals/rsi_orchestrator.py` (with session failure tracking so resolved failures are never lost on pass).
- Sync-resilient auto-discovery of custom `.agents/rules/modules/*.md` modules via inline `<!-- triggers: ... -->` headers in `evals/memory_engine.py`, duplicate rule ID detection in `--audit`, project-rule keyword fallback in `--diagnose`, and compact Phase 3 briefing CLI (`--propose`).
- Official `[Scope: XS]` Fast-Track workflow across `AGENTS.md`, `.agents/workflows/rsi-feature.md`, `docs/AGENT_OPERATIONS.md`, and `README.md`.
- 5 new standard-library unit tests in `evals/tests/test_evals.py` (20 tests total).

### Changed
- Replaced synthetic `R-AUTO-XX` rule mutations in `evals/telemetry_hook.py` with real module rule diffs, live `failure_taxonomy` aggregation, and automatic `PROBATION -> PROVEN` promotion at `prevented_errors_count >= 3`.
- Deduplicated SSOT rule layers (`AGENTS.md`, `system_core.md`, `api_backend.md`, `security_auth.md`), turned `meta_optimizer.md` into a thin alias pointer to `--persona meta`, and made `version_manager.py --bump` optional per release in `rsi-feature.md`.

### Fixed
- Eliminated false-positive `Blast Radius: HIGH / CRITICAL` (`[Scope: XL]`) warnings on documentation and metadata files (`VERSION`, `README.md`, `CHANGELOG.md`, `docs/TASKS.md`) in `evals/stack_inspector.py` and `evals/rsi_orchestrator.py`.

## [0.3.0] - 2026-11-26

### Added
- On-demand single Checker/Reviewer specialist agent catalog (`.agents/prompts/rsi_specialist.md`) combining a shared Maker/Checker `CORE` contract (`VERDICT`, `FINDINGS`, optional `CAPITALIZATION_CANDIDATE`) with 6 tagged domain personas (`< 40` non-empty lines each): `architect`, `db`, `security`, `ui`, `qa`, and `meta`.
- Persona extraction and `< 40`-line structural enforcement in `evals/memory_engine.py` (`--list-personas`, `--persona <name>`, integrated into `rsi_memory_hygiene`) with unit test coverage in `evals/tests/test_evals.py`.
- Dedicated Agent Operations Guide (`docs/AGENT_OPERATIONS.md`) detailing end-to-end agent behavior, Maker/Checker specialist reviews, `CAPITALIZATION_CANDIDATE -> meta` rule capitalization, Fail-Loud / `[!] BLOCKED` handling, memory duality, and non-destructive `AGENTS.md` synchronization.

### Changed
- Linked `docs/AGENT_OPERATIONS.md` prominently in `README.md` and `AGENTS.md`, added Section 12 (`On-Demand Specialist Agent (rsi-specialist) & Pre-Commit Sprint Gate`) to `README.md`, and updated `.agents/workflows/rsi-feature.md` Phase 3 with the specialist review and capitalization pipeline.

## [0.2.2] - 2026-11-25

### Added
- Net-new Sprint-End Security & Performance Gate (`python evals/rsi_orchestrator.py --sprint-gate`): production dependency CVE audit (`high`/`critical`), oversized `public/` assets (`> 500 KB`), static N+1 DB loop detection in `src/`, and modified UI page LCP review reminder without re-running passed task suites.
- Mandatory Pre-Commit Security & Performance Audit rule (Rule 6) inside the `RSI-PROTOCOL:START/END` block of `AGENTS.md`.

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
