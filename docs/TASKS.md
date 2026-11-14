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
|                         |  | [ ] TASK-INIT-01        |  | [x] TASK-MODEL-MAP-01   |
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

- [x] **`TASK-MODEL-MAP-01` - Update Gemini 4 Model Mapping to Hydrogen in Telemetry Hook**
  - **Priority:** MEDIUM
  - **Target files:** `evals/telemetry_hook.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-MODEL-MAP-01.01`: Map generic "gemini 4" and "gemini-4" to "gemini-4-hydrogen" while preserving explicit "argon" and "hydrogen" keywords in `evals/telemetry_hook.py`.
    - [x] `TASK-MODEL-MAP-01.02`: Add pricing entry for `gemini-4-hydrogen` in `FALLBACK_PRICING` dictionary.
    - [x] `TASK-MODEL-MAP-01.03`: Synchronize updated telemetry hook to `OfferAnalyst` and validate with deterministic judge (`100/100 PASS`).

- [x] **`TASK-SEC-FIX-01` - Fix False Positives in security_audit.py (ASCII vs French Accents & Prisma Scope)**
  - **Priority:** HIGH
  - **Target files:** `evals/security_audit.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SEC-FIX-01.01`: Restrict strict ASCII check (ord > 127) to executable Python scripts (`evals/**/*.py`) and exclude third-party `.agents/skills/` and `CHANGELOG.md`.
    - [x] `TASK-SEC-FIX-01.02`: Restrict `new PrismaClient(` audit pattern strictly to application code under `src/` (while preserving `SINGLETON_ALLOWED_FILES`).
    - [x] `TASK-SEC-FIX-01.03`: Validate `python evals/security_audit.py` and `python evals/run_fullstack_eval.py` (100/100 PASS) in Agentic-RSI-Protocol and synced OfferAnalyst.

- [x] **`TASK-V22-ISOLATE-01` - Session Isolation, Contract Verification & OfferAnalyst Deployment (v2.2)**
  - **Priority:** HIGH
  - **Target files:** `evals/rsi_orchestrator.py`, `evals/telemetry_hook.py`, `evals/version_manager.py`, `README.md`, `docs/TASKS.md`, `PLAN_AGENTIC_RSI_PROTOCOL.md`
  - **Acceptance criteria:**
    - [x] `TASK-V22-ISOLATE-01.01`: Implement strict session token isolation on task switch and track attempt timestamps in `evals/rsi_orchestrator.py`.
    - [x] `TASK-V22-ISOLATE-01.02`: Implement `--verify-contract` in `evals/telemetry_hook.py` and align payload structure for `cognitive-rsi-ops`.
    - [x] `TASK-V22-ISOLATE-01.03`: Add `--sync-to` support in `evals/rsi_orchestrator.py` alias and deploy cleanly to `../OfferAnalyst`.
    - [x] `TASK-V22-ISOLATE-01.04`: Validate with deterministic judge (`100/100 PASS`), pure ASCII check, and security audit.

- [x] **`TASK-SYNC-01` - Automated Target Project Sync & Installation CLI (`--sync-to`)**
  - **Priority:** HIGH
  - **Target files:** `evals/version_manager.py`, `README.md`, `docs/TASKS.md`, `docs/archive/tasks/sprint_archive_2026_11.md`
  - **Acceptance criteria:**
    - [x] `TASK-SYNC-01.01`: Implement `--sync-to <target-dir>` and `--init-target <target-dir>` in `evals/version_manager.py` preserving target memories and backlog.
    - [x] `TASK-SYNC-01.02`: Update `README.md` with complete installation and update documentation for target project workspaces.
    - [x] `TASK-SYNC-01.03`: Verify deterministic evaluation with `python evals/run_fullstack_eval.py` (100/100 PASS) and security audit.

- [ ] **`TASK-INIT-01` - Project Scaffolding & Initial Setup**
  - **Priority:** MEDIUM
  - **Target files:** `package.json`, `README.md`
  - **Acceptance criteria:**
    - [ ] `TASK-INIT-01.01`: Technical baseline and dependency configuration.
    - [ ] `TASK-INIT-01.02`: Deterministic validation with `python evals/run_fullstack_eval.py --quick` (100/100 PASS).

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
