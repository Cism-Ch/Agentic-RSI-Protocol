# [SSOT] TASKS.md - Central Registry & Task Tracker

> Single Source of Truth (SSOT) for orchestrating technical and functional tasks.
> Absolute rule for AI Agents: Consult before every task, update immediately on completion.
> Strict ceiling: 250 lines.

---

## Synthetic Kanban View

```
+-------------------------+  +-------------------------+  +-------------------------+
| [>] IN PROGRESS (SP 01) |  |   [?] FUTURE BACKLOG    |  |       [X] ARCHIVES      |
+-------------------------+  +-------------------------+  +-------------------------+
|                         |  |                         |  | [x] TASK-SPECIALIST-01  |
|                         |  |                         |  | [x] TASK-REL-04         |
|                         |  |                         |  | [x] TASK-PRECOMMIT-01   |
|                         |  |                         |  | [x] TASK-SPRINT-GATE-01 |
|                         |  |                         |  | [x] TASK-REL-03         |
|                         |  |                         |  | [x] TASK-RULES-SYNC-01  |
|                         |  |                         |  | [x] TASK-REL-02         |
|                         |  |                         |  | [x] TASK-TEST-SECRET-01 |
|                         |  |                         |  | [x] TASK-PRIVACY-MODEL-01|
|                         |  |                         |  | [x] TASK-DOCS-07        |
|                         |  |                         |  | [x] TASK-SYNC-IGNORE-01 |
|                         |  |                         |  | [x] TASK-SYNC-SCOPE-01  |
|                         |  |                         |  | [x] TASK-SEC-HARDEN-01  |
|                         |  |                         |  | [x] TASK-SEC-PERF-01    |
|                         |  |                         |  | [x] TASK-FRICTION-01    |
|                         |  |                         |  | [x] TASK-DOCS-06        |
|                         |  |                         |  | [x] TASK-DOCS-05        |
|                         |  |                         |  | [x] TASK-HONESTY-01     |
|                         |  |                         |  | [x] TASK-MODEL-MAP-01   |
|                         |  |                         |  | [x] TASK-SEC-FIX-01     |
|                         |  |                         |  | [x] TASK-V22-ISOLATE-01 |
|                         |  |                         |  | [x] TASK-SYNC-01        |
|                         |  |                         |  | [x] TASK-GIT-01         |
|                         |  |                         |  | [x] TASK-I18N-01        |
|                         |  |                         |  | [x] TASK-SCRIPTS-01     |
|                         |  |                         |  | [x] TASK-RSI-RESET-01   |
|                         |  |                         |  | [x] TASK-DOCS-01        |
|                         |  |                         |  | [x] TASK-DOCS-02        |
|                         |  |                         |  | [x] TASK-RSI-SPEC-01    |
|                         |  |                         |  | [x] TASK-DECOUPLE-01    |
|                         |  |                         |  | [x] TASK-CI-01          |
|                         |  |                         |  | [x] TASK-CI-FIX-01      |
|                         |  |                         |  | [x] TASK-MEM-01         |
|                         |  |                         |  | [x] TASK-PAT-01         |
|                         |  |                         |  | [x] TASK-TOPO-SCOPE-01  |
|                         |  |                         |  | [x] TASK-ORCH-01        |
|                         |  |                         |  | [x] TASK-DOCS-03        |
|                         |  |                         |  | [x] TASK-TOOL-01        |
|                         |  |                         |  | [x] TASK-PRUNE-SCOPE-01 |
|                         |  |                         |  | [x] TASK-TELEM-01       |
|                         |  |                         |  | [x] TASK-DOCS-04        |
+-------------------------+  +-------------------------+  +-------------------------+
```

---

## Active Sprint 01: Project Setup & Initialization

- [x] **`TASK-SPECIALIST-01` - Add Single Specialist Reviewer Agent (6 Personas), Agent Operations Guide & README Updates**
  - **Priority:** HIGH
  - **Target files:** `.agents/prompts/rsi_specialist.md`, `evals/memory_engine.py`, `evals/tests/test_evals.py`, `.agents/workflows/rsi-feature.md`, `AGENTS.md`, `docs/AGENT_OPERATIONS.md`, `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SPECIALIST-01.01`: Create `.agents/prompts/rsi_specialist.md` with common Maker/Checker core (`CAPITALIZATION_CANDIDATE`) and 6 tagged personas (`< 40` lines each): `architect`, `db`, `security`, `ui`, `qa`, `meta`.
    - [x] `TASK-SPECIALIST-01.02`: Add `--persona`, `--list-personas`, and `< 40L` persona audit in `evals/memory_engine.py` with unit tests in `evals/tests/test_evals.py`.
    - [x] `TASK-SPECIALIST-01.03`: Create `docs/AGENT_OPERATIONS.md`, link it in `README.md`, update `AGENTS.md` / `.agents/workflows/rsi-feature.md`, and validate `100/100 PASS`.

- [x] **`TASK-REL-04` - Seal & Publish Protocol Release v0.2.2 and Sync Registered Targets**
  - **Priority:** HIGH
  - **Target files:** `VERSION`, `CHANGELOG.md`, `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-REL-04.01`: Update `CHANGELOG.md`, bump `VERSION` to `0.2.2`, and update `README.md` version badge.
    - [x] `TASK-REL-04.02`: Validate `100/100 PASS`, commit, push tag `v0.2.2`, and run `--sync-all` on registered targets.

- [x] **`TASK-PRECOMMIT-01` - Add Mandatory Pre-Commit Security & Performance Audit Rule in AGENTS.md**
  - **Priority:** HIGH
  - **Target files:** `AGENTS.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-PRECOMMIT-01.01`: Add Rule 6 (`Mandatory Pre-Commit Security & Performance Audit`) inside the `RSI-PROTOCOL:START/END` block of `AGENTS.md`.
    - [x] `TASK-PRECOMMIT-01.02`: Validate with `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-SPRINT-GATE-01` - Add Net-New Sprint-End Security & Performance Gate (--sprint-gate)**
  - **Priority:** MEDIUM
  - **Target files:** `evals/rsi_orchestrator.py`, `.agents/workflows/rsi-feature.md`, `AGENTS.md`, `evals/tests/test_evals.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SPRINT-GATE-01.01`: Implement `--sprint-gate` in `evals/rsi_orchestrator.py` running only net-new sprint-end checks (dependency CVE audit, heavy `public/` assets > 500 KB, static `src/` N+1 loop queries, touched UI page LCP reminder) without re-running passed task suites.
    - [x] `TASK-SPRINT-GATE-01.02`: Reference `--sprint-gate` in `AGENTS.md` and `.agents/workflows/rsi-feature.md`.
    - [x] `TASK-SPRINT-GATE-01.03`: Add unit tests in `evals/tests/test_evals.py` and validate `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-REL-03` - Seal & Publish Protocol Release v0.2.1 and Sync Registered Targets**
  - **Priority:** HIGH
  - **Target files:** `VERSION`, `CHANGELOG.md`, `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-REL-03.01`: Update `CHANGELOG.md`, bump `VERSION` to `0.2.1`, and update `README.md` version badge.
    - [x] `TASK-REL-03.02`: Validate `100/100 PASS`, commit, push tag `v0.2.1`, and run `--sync-all` on registered targets.

- [x] **`TASK-RULES-SYNC-01` - Anti-AI-Slop & Secure-by-Default Rules + Non-Destructive AGENTS.md Backup/Merge**
  - **Priority:** HIGH
  - **Target files:** `AGENTS.md`, `.agents/rules/system_core.md`, `.agents/workflows/rsi-feature.md`, `.agents/rules/modules/ui_frontend.md`, `.agents/rules/modules/api_backend.md`, `.agents/rules/modules/security_auth.md`, `evals/version_manager.py`, `evals/tests/test_evals.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-RULES-SYNC-01.01`: Add UI structural/design-system integrity, zero orphan components, and secure-by-default endpoint/upload rules to `AGENTS.md`, `system_core.md`, `rsi-feature.md`, and `.agents/rules/modules/`.
    - [x] `TASK-RULES-SYNC-01.02`: Implement `sync_agents_md_safely()` in `evals/version_manager.py` with `evals/backups/AGENTS.md.<ts>.bak` backup, `RSI-PROTOCOL:START/END` non-destructive merge, and human-review `[ACTION REQUIRED]` prompt.
    - [x] `TASK-RULES-SYNC-01.03`: Add unit test in `evals/tests/test_evals.py` and validate `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-REL-02` - Seal & Publish Protocol Release v0.2.0**
  - **Priority:** HIGH
  - **Target files:** `VERSION`, `CHANGELOG.md`, `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-REL-02.01`: Update `CHANGELOG.md` release notes, bump `VERSION` to `0.2.0`, and update `README.md` version badge.
    - [x] `TASK-REL-02.02`: Validate `python evals/run_fullstack_eval.py` (`100/100 PASS`), commit, tag `v0.2.0`, and push tag to trigger GitHub Release.

- [x] **`TASK-TEST-SECRET-01` - Build Synthetic Secret Fixtures Dynamically to Avoid GitHub Secret Scanning Alerts**
  - **Priority:** HIGH
  - **Target files:** `evals/tests/test_evals.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-TEST-SECRET-01.01`: Construct all synthetic DB URI and API key test fixtures dynamically at runtime in `evals/tests/test_evals.py` so zero literal connection strings appear in source.
    - [x] `TASK-TEST-SECRET-01.02`: Validate with `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-PRIVACY-MODEL-01` - Anonymize Personal Targets, Add Private Context Leak Guard & Dynamic LLM Model Detection**
  - **Priority:** HIGH
  - **Target files:** `evals/security_audit.py`, `evals/telemetry_hook.py`, `evals/tests/test_evals.py`, `docs/TASKS.md`, `docs/archive/tasks/sprint_archive_2026_11.md`
  - **Acceptance criteria:**
    - [x] `TASK-PRIVACY-MODEL-01.01`: Remove personal project names from tracked docs and unit tests.
    - [x] `TASK-PRIVACY-MODEL-01.02`: Add `audit_private_context_leaks()` in `evals/security_audit.py` to block private synced target names and local home paths on the source protocol repo.
    - [x] `TASK-PRIVACY-MODEL-01.03`: Make `_normalize_model_label()` and `_resolve_model_pricing()` dynamic for any future LLM in `evals/telemetry_hook.py` and validate `100/100 PASS`.

- [x] **`TASK-DOCS-07` - Align README.md with Current Security, Sync, ASCII & Test Capabilities**
  - **Priority:** MEDIUM
  - **Target files:** `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-DOCS-07.01`: Correct ASCII hygiene scope (`evals/**/*.py`), Prisma `src/` scope, `package.json` 9-script block, repository layout (`evals/tests/test_evals.py`), and CLI reference flags (`--sync-targets`, `--sync-all`).
    - [x] `TASK-DOCS-07.02`: Document supply-chain/agent integrity guardrails, `shell=False` execution, target `.gitignore` hygiene, consumer `Scope Guard` exemption, and Fail-Loud / `[!] BLOCKED` rule.
    - [x] `TASK-DOCS-07.03`: Validate with `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-SYNC-IGNORE-01` - Expand Target Gitignore Hygiene Entries in version_manager.py & Sync Targets**
  - **Priority:** MEDIUM
  - **Target files:** `evals/version_manager.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SYNC-IGNORE-01.01`: Add `evals/backups/`, `backups/skills/`, `.agents/telemetry/*.tmp`, `__pycache__/`, and `*.pyc` to `EPHEMERAL_GITIGNORE_ENTRIES` in `evals/version_manager.py`.
    - [x] `TASK-SYNC-IGNORE-01.02`: Validate `python evals/run_fullstack_eval.py` (`100/100 PASS`) and run `--sync-all` on registered target projects.

- [x] **`TASK-SYNC-SCOPE-01` - Exempt Synced Protocol Files in Consumer Scope Guard & Enforce Target Gitignore Hygiene**
  - **Priority:** MEDIUM
  - **Target files:** `evals/rsi_orchestrator.py`, `evals/version_manager.py`, `evals/tests/test_evals.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SYNC-SCOPE-01.01`: Exempt synced RSI protocol files from `Scope Guard` drift warnings on consumer projects while keeping strict enforcement on the source protocol repo.
    - [x] `TASK-SYNC-SCOPE-01.02`: Ensure `--sync-to` idempotently adds ephemeral RSI telemetry/log entries to target `.gitignore` (`ensure_target_gitignore_hygiene`).
    - [x] `TASK-SYNC-SCOPE-01.03`: Add unit tests in `evals/tests/test_evals.py` and validate `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-SEC-HARDEN-01` - Supply-Chain, Host Hardware & Agent Integrity Hardening**
  - **Priority:** HIGH
  - **Target files:** `evals/security_audit.py`, `evals/version_manager.py`, `evals/telemetry_hook.py`, `evals/run_fullstack_eval.py`, `evals/stack_inspector.py`, `evals/tests/test_evals.py`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SEC-HARDEN-01.01`: Add `audit_supply_chain_and_agent_integrity()` in `evals/security_audit.py` (evals allowlist, symlink rejection, pipe-to-shell, destructive OS commands, and prompt-injection checks).
    - [x] `TASK-SEC-HARDEN-01.02`: Add `validate_safe_target_dir()` and `ALLOWED_SYNC_EVAL_FILES` allowlist in `evals/version_manager.py` to prevent arbitrary path overwrite or rogue file propagation during `--sync-to`.
    - [x] `TASK-SEC-HARDEN-01.03`: Eliminate `shell=True` in `evals/run_fullstack_eval.py`, verify `cli.py` authenticity + timeout in `evals/telemetry_hook.py`, and add path-confinement + RAM/CPU caps in `evals/stack_inspector.py`.
    - [x] `TASK-SEC-HARDEN-01.04`: Harden `.github/workflows/ci.yml` and `release.yml` (least-privilege permissions and timeouts) and add unit tests in `evals/tests/test_evals.py` (`100/100 PASS`).

- [x] **`TASK-SEC-PERF-01` - Optimize security_audit.py Performance (< 2s) Without Coverage Loss**
  - **Priority:** HIGH
  - **Target files:** `evals/security_audit.py`, `evals/tests/test_evals.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SEC-PERF-01.01`: Add file-level combined regex pre-filtering (`COMBINED_SECRET_RE`, `COMBINED_OPERATIONAL_RE`) in `evals/security_audit.py`.
    - [x] `TASK-SEC-PERF-01.02`: Exclude lockfiles, ephemeral telemetry files, binary extensions, and oversized/null-byte artifacts in `audit_secrets()`, and expand `IGNORE_DIRS`.
    - [x] `TASK-SEC-PERF-01.03`: Add unit tests in `evals/tests/test_evals.py` verifying skipped files and lossless secret/anti-pattern detection, and pass `python evals/run_fullstack_eval.py` (`100/100 PASS`).

---

## Completed Tasks History

| Date | Task ID | Title & Description | Created / Modified Files |
| :--- | :--- | :--- | :--- |
| 2026-11-03 | TASK-GIT-01 | Git Initialization & Security Audits | `.gitignore`, `evals/security_audit.py`, `evals/run_fullstack_eval.py`, `docs/TASKS.md` |
| 2026-11-03 | TASK-I18N-01 | Complete Repository Internationalization (EN) | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/TASKS.md`, `.agents/**/*`, `evals/**/*`, `.gitignore` |
| 2026-11-03 | TASK-SCRIPTS-01 | Clean Emojis & Pure ASCII Output in Scripts | `evals/memory_engine.py`, `evals/rsi_orchestrator.py`, `evals/security_audit.py`, `evals/stack_inspector.py`, `evals/version_manager.py`, `docs/TASKS.md` |
| 2026-11-03 | TASK-RSI-RESET-01 | RSI Reset Engine & `/reset-rsi` Workflow | `evals/reset_rsi.py`, `.agents/workflows/reset-rsi.md`, `docs/TASKS.md` |
| 2026-11-03 | TASK-DOCS-01 | GitHub Documentation Suite & Open Source Readiness | `README.md`, `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `LICENSE`, `docs/TASKS.md` |
| 2026-11-04 | TASK-DOCS-02 | Production-Grade Docs, Pure ASCII, Modern Agentic IDEs & Mermaid | `README.md`, `docs/ARCHITECTURE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.agents/**/*`, `docs/TASKS.md` |
| 2026-11-04 | TASK-RSI-SPEC-01 | Protocol Versioning, Battle-Tested IDE Use Cases & Deterministic Emoji Guard | `VERSION`, `package.json`, `evals/security_audit.py`, `evals/version_manager.py`, `.agents/rules/system_core.md`, `README.md`, `docs/TASKS.md` |
| 2026-11-04 | TASK-DECOUPLE-01 | Decouple Protocol from Application Layer, Remove Premature package.json | `VERSION`, `evals/version_manager.py`, `README.md`, `docs/TASKS.md` |
| 2026-11-04 | TASK-CI-01 | GitHub Actions CI & Automated Release Pipelines | `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `docs/TASKS.md` |
| 2026-11-04 | TASK-CI-FIX-01 | Fix Linux CI Subprocess Execution in Deterministic Judge | `evals/run_fullstack_eval.py`, `docs/TASKS.md` |
| 2026-11-05 | TASK-MEM-01 | Refine 2-Step Lossless Memory Consolidation & Module Splitting | `README.md`, `docs/ARCHITECTURE.md`, `.agents/prompts/meta_optimizer.md`, `.agents/workflows/rsi-feature.md`, `docs/TASKS.md` |
| 2026-11-05 | TASK-PAT-01 | Hybrid Pattern Recognition & Operational Security Engine | `.agents/rules/modules/pattern_recognition.md`, `.agents/rules/fullstack_playbook.md`, `evals/memory_engine.py`, `evals/security_audit.py`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md` |
| 2026-11-05 | TASK-TOPO-SCOPE-01 | Topological Repo Map, Blast Radius Analyzer & Scope Drift Guard | `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `.agents/rules/modules/pattern_recognition.md`, `.agents/workflows/rsi-feature.md`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md` |
| 2026-11-05 | TASK-ORCH-01 | Cold-Start Session Pulse (`--pulse`) & Automated Task Rollover (`--rollover`) | `evals/rsi_orchestrator.py`, `.agents/workflows/rsi-feature.md`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md` |
| 2026-11-05 | TASK-DOCS-03 | Comprehensive README Overhaul with Hero Header & Full Protocol Cycle | `README.md`, `docs/TASKS.md` |
| 2026-11-05 | TASK-TOOL-01 | Tooling Status & Conversational Installation Request in Pulse | `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `docs/TASKS.md` |
| 2026-11-06 | TASK-PRUNE-SCOPE-01 | Autonomous Stack Profiler, Lossless Skill Pruning & `[Scope: XS..XL]` Sizing | `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `.gitignore`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md` |
| 2026-11-12 | TASK-TELEM-01 | Telemetry-Native Execution & Real Transcript Extraction (v2.1) | `evals/memory_engine.py`, `evals/run_fullstack_eval.py`, `evals/rsi_orchestrator.py`, `evals/telemetry_hook.py`, `.gitignore`, `docs/TASKS.md` |
| 2026-11-12 | TASK-DOCS-04 | Update README for v2.1 Telemetry-Native Capabilities | `README.md`, `docs/TASKS.md` |
