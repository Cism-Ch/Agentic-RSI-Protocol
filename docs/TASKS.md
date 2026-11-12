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
| [ ] TASK-INIT-01        |  | [ ] Future task 1       |  | [x] TASK-GIT-01         |
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
+-------------------------+  +-------------------------+  +-------------------------+
```

---

## Active Sprint 01: Project Setup & Initialization

- [x] **`TASK-TELEM-01` - Telemetry-Native Execution & Real Transcript Extraction (v2.1)**
  - **Priority:** HIGH
  - **Target files:** `evals/memory_engine.py`, `evals/run_fullstack_eval.py`, `evals/rsi_orchestrator.py`, `evals/telemetry_hook.py`, `.gitignore`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-TELEM-01.01`: Track active session rules and diagnostic matches in `.agents/telemetry/active_session.json` via `evals/memory_engine.py`.
    - [x] `TASK-TELEM-01.02`: Add per-step `duration_ms`, `checks` array, and `total_duration_ms` to `evals/run_fullstack_eval.py` (`trajectory_latest.json`).
    - [x] `TASK-TELEM-01.03`: Add `parse_active_sprint_id()`, `get_scope_drift_report()`, session initialization on `--pulse`, and enriched telemetry chaining on `--eval` in `evals/rsi_orchestrator.py`.
    - [x] `TASK-TELEM-01.04`: Implement `extract_real_session_metrics()` and standalone `cognitive_state.json` fallback + rule ROI tracking in `evals/telemetry_hook.py`.

- [x] **`TASK-PRUNE-SCOPE-01` - Autonomous Stack Profiler, Lossless Skill Pruning & `[Scope: XS..XL]` Sizing**
  - **Priority:** HIGH
  - **Target files:** `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `.gitignore`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-PRUNE-SCOPE-01.01`: Implement autonomous `discover_project_profile()` and `compute_blast_radius()` in `evals/stack_inspector.py`.
    - [x] `TASK-PRUNE-SCOPE-01.02`: Implement 4-step lossless skill pruner (`--prune-skills`, `.bak` ZIP + `unpacked/`, `PRUNED_SKILLS.log`, `RESTORE_MANIFEST.json`, `restore_skill.py`) in `evals/stack_inspector.py`.
    - [x] `TASK-PRUNE-SCOPE-01.03`: Implement `[Scope: XS / S / M / L / XL]` task sizing and automatic target Blast Radius display in `evals/rsi_orchestrator.py`.
    - [x] `TASK-PRUNE-SCOPE-01.04`: Update `.gitignore`, `README.md`, and `docs/ARCHITECTURE.md`, and validate with `python evals/run_fullstack_eval.py` (`100/100 PASS`).

- [x] **`TASK-TOOL-01` - Tooling Status & Conversational Installation Request in Pulse**
  - **Priority:** HIGH
  - **Target files:** `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-TOOL-01.01`: Enrich `ECOSYSTEM_CATALOG` in `evals/stack_inspector.py` with concrete setup details (`mcp_cmd`, `env_keys`).
    - [x] `TASK-TOOL-01.02`: Integrate tooling check into `run_session_pulse()` in `evals/rsi_orchestrator.py` to instruct agents to summarize missing tools to the user in chat.
    - [x] `TASK-TOOL-01.03`: Validate with deterministic judge (`100/100 PASS`) and ASCII hygiene check.

- [x] **`TASK-DOCS-03` - Comprehensive README Overhaul with Hero Header & Full Protocol Cycle**
  - **Priority:** HIGH
  - **Target files:** `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-DOCS-03.01`: Design an elegant ASCII banner hero header and cohesive typography hierarchy.
    - [x] `TASK-DOCS-03.02`: Document real-world failure scenarios 6 & 7 (Scope Drift & Reinventing Existing Infrastructure).
    - [x] `TASK-DOCS-03.03`: Upgrade the operational Mermaid diagram with the complete end-to-end loop (`--pulse`, `--map`, `--impact`, `--diagnose`, `--scope`, `--rollover`).
    - [x] `TASK-DOCS-03.04`: Validate with deterministic judge (`100/100 PASS`) and ASCII hygiene check.

- [x] **`TASK-ORCH-01` - Cold-Start Session Pulse (`--pulse`) & Automated Task Rollover (`--rollover`)**
  - **Priority:** HIGH
  - **Target files:** `evals/rsi_orchestrator.py`, `.agents/workflows/rsi-feature.md`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-ORCH-01.01`: Implement `--pulse` in `evals/rsi_orchestrator.py` for 1-command cold-start situational awareness (`< 50ms`).
    - [x] `TASK-ORCH-01.02`: Implement `--rollover` (with `--dry-run`) in `evals/rsi_orchestrator.py` to archive completed `[x]` sprint blocks to `docs/archive/tasks/` and keep `docs/TASKS.md` under 250 lines.
    - [x] `TASK-ORCH-01.03`: Update `.agents/workflows/rsi-feature.md`, `README.md`, and `docs/ARCHITECTURE.md`.
    - [x] `TASK-ORCH-01.04`: Validate full deterministic evaluation (`100/100 PASS`) and guardrails.

- [x] **`TASK-TOPO-SCOPE-01` - Topological Repo Map, Blast Radius Analyzer & Scope Drift Guard**
  - **Priority:** HIGH
  - **Target files:** `evals/stack_inspector.py`, `evals/rsi_orchestrator.py`, `.agents/rules/modules/pattern_recognition.md`, `.agents/workflows/rsi-feature.md`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-TOPO-SCOPE-01.01`: Add `--map` (Topological Repo Map & Canonical Singletons) and `--impact <file>` (Blast Radius Predictor) to `evals/stack_inspector.py`.
    - [x] `TASK-TOPO-SCOPE-01.02`: Add `--scope` and `--strict-scope` (Scope Drift Guard vs active `[-]` task in `docs/TASKS.md`) to `evals/rsi_orchestrator.py`.
    - [x] `TASK-TOPO-SCOPE-01.03`: Add `[R-PAT-05]` and `[R-PAT-06]` to `.agents/rules/modules/pattern_recognition.md` and update `.agents/workflows/rsi-feature.md`, `README.md`, and `docs/ARCHITECTURE.md`.
    - [x] `TASK-TOPO-SCOPE-01.04`: Validate full deterministic evaluation (`100/100 PASS`) and guardrails.

- [x] **`TASK-PAT-01` - Hybrid Pattern Recognition & Operational Security Engine**
  - **Priority:** HIGH
  - **Target files:** `.agents/rules/modules/pattern_recognition.md`, `.agents/rules/fullstack_playbook.md`, `evals/memory_engine.py`, `evals/security_audit.py`, `README.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-PAT-01.01`: Create `.agents/rules/modules/pattern_recognition.md` (`< 80` lines, pure ASCII) and index it in `.agents/rules/fullstack_playbook.md`.
    - [x] `TASK-PAT-01.02`: Implement `--diagnose` in `evals/memory_engine.py` for instant deterministic error pattern resolution (`< 10ms`).
    - [x] `TASK-PAT-01.03`: Implement `audit_operational_patterns()` in `evals/security_audit.py` to block runtime anti-patterns.
    - [x] `TASK-PAT-01.04`: Update `README.md` and `docs/ARCHITECTURE.md` and validate full deterministic evaluation (`100/100 PASS`).

- [x] **`TASK-MEM-01` - Refine Memory Consolidation & Module Splitting Protocol**
  - **Priority:** HIGH
  - **Target files:** `README.md`, `docs/ARCHITECTURE.md`, `.agents/prompts/meta_optimizer.md`, `.agents/workflows/rsi-feature.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-MEM-01.01`: Update `README.md` and `docs/ARCHITECTURE.md` to formalize the 2-step anti-bloat strategy (lossless synthesis of redundant rules OR granular module splitting).
    - [x] `TASK-MEM-01.02`: Update `.agents/prompts/meta_optimizer.md` and `.agents/workflows/rsi-feature.md` to forbid lossy compression of distinct technical rules and instruct splitting when needed.
    - [x] `TASK-MEM-01.03`: Validate full deterministic evaluation (100/100 PASS) and guardrails.

- [x] **`TASK-CI-FIX-01` - Fix Linux CI Subprocess Execution in Deterministic Judge**
  - **Priority:** HIGH
  - **Target files:** `evals/run_fullstack_eval.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-CI-FIX-01.01`: Support list-based command execution in `run_cmd` to eliminate string quoting errors on Linux/Unix.
    - [x] `TASK-CI-FIX-01.02`: Pass Python invocations as tokenized argument lists (`[py, str(path), ...]`).
    - [x] `TASK-CI-FIX-01.03`: Enable cross-platform shell execution when shell string commands are passed.
    - [x] `TASK-CI-FIX-01.04`: Validate full deterministic evaluation (100/100 PASS).

- [x] **`TASK-CI-01` - GitHub Actions CI & Automated Release Pipeline**
  - **Priority:** HIGH
  - **Target files:** `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-CI-01.01`: Create `.github/workflows/ci.yml` for pull requests and branch validation.
    - [x] `TASK-CI-01.02`: Create `.github/workflows/release.yml` triggered on tags (`v*`) with deterministic quality gate.
    - [x] `TASK-CI-01.03`: Verify workflow files are tracked by Git and excluded from `.gitignore`.
    - [x] `TASK-CI-01.04`: Validate full deterministic evaluation (100/100 PASS).

- [x] **`TASK-DECOUPLE-01` - Decouple Workflow Protocol from Application Package.json**
  - **Priority:** HIGH
  - **Target files:** `package.json`, `VERSION`, `evals/version_manager.py`, `README.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-DECOUPLE-01.01`: Remove premature application `package.json` to maintain true language-agnostic template purity.
    - [x] `TASK-DECOUPLE-01.02`: Ensure `evals/version_manager.py` cleanly operates with `VERSION` and `CHANGELOG.md` alone.
    - [x] `TASK-DECOUPLE-01.03`: Clarify in `README.md` that `package.json` belongs to the application layer (`TASK-INIT-01`).
    - [x] `TASK-DECOUPLE-01.04`: Validate full deterministic evaluation (100/100 PASS).

- [x] **`TASK-RSI-SPEC-01` - Protocol Versioning, Real IDE Use Cases & Deterministic Emoji Guard**
  - **Priority:** HIGH
  - **Target files:** `VERSION`, `package.json`, `evals/security_audit.py`, `evals/run_fullstack_eval.py`, `.agents/rules/system_core.md`, `README.md`
  - **Acceptance criteria:**
    - [x] `TASK-RSI-SPEC-01.01`: Establish official protocol versioning via `VERSION` file, `package.json`, and SemVer synchronization.
    - [x] `TASK-RSI-SPEC-01.02`: Implement deterministic ASCII and Emoji guard in `evals/security_audit.py` to block agents from committing emojis or non-ASCII characters.
    - [x] `TASK-RSI-SPEC-01.03`: Add real-world, battle-tested failure scenarios in `README.md` (Cursor, Windsurf, Claude Code, Cline).
    - [x] `TASK-RSI-SPEC-01.04`: Add `[R-SYS-05]` in `.agents/rules/system_core.md` and validate with deterministic judge (100/100 PASS).

- [x] **`TASK-DOCS-02` - Comprehensive Documentation Overhaul (No Emojis, Agentic IDEs, Mermaid)**
  - **Priority:** HIGH
  - **Target files:** `README.md`, `docs/ARCHITECTURE.md`, `AGENTS.md`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-DOCS-02.01`: Remove all emojis across `README.md` and related docs for clean, professional presentation.
    - [x] `TASK-DOCS-02.02`: Frame context around modern agentic coding environments (Cursor, Windsurf, Google Antigravity, Claude Code, Copilot Workspace, Cline).
    - [x] `TASK-DOCS-02.03`: Replace crude loop ASCII graph with a clean, high-clarity GitHub-native Mermaid diagram.
    - [x] `TASK-DOCS-02.04`: Provide thorough, production-grade documentation of memory duality, dynamic injection, the 4-phase cycle, and deterministic evaluation.
    - [x] `TASK-DOCS-02.05`: Validate deterministic evaluation (100/100 PASS) and guardrails.

- [x] **`TASK-RSI-RESET-01` - Standalone RSI Reset Engine & `/reset-rsi` Workflow**
  - **Priority:** HIGH
  - **Target files:** `evals/reset_rsi.py`, `.agents/workflows/reset-rsi.md`, `evals/run_fullstack_eval.py`
  - **Acceptance criteria:**
    - [x] `TASK-RSI-RESET-01.01`: Create `evals/reset_rsi.py` with pure ASCII output supporting `--dry-run`, `--hard`, `--keep-rules`, `--backup`.
    - [x] `TASK-RSI-RESET-01.02`: Create workflow `.agents/workflows/reset-rsi.md` for conversational agent execution (`/reset-rsi`).
    - [x] `TASK-RSI-RESET-01.03`: Deterministic validation and test execution.

- [x] **`TASK-DOCS-01` - GitHub Documentation Suite & Open Source Readiness**
  - **Priority:** HIGH
  - **Target files:** `README.md`, `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `LICENSE`
  - **Acceptance criteria:**
    - [x] `TASK-DOCS-01.01`: Overhaul `README.md` with complete GitHub badges, quickstart, CLI reference, and architecture diagrams.
    - [x] `TASK-DOCS-01.02`: Create deep-dive `docs/ARCHITECTURE.md` (feedback loops, evaluation harness, memory duality).
    - [x] `TASK-DOCS-01.03`: Add `CONTRIBUTING.md` and MIT `LICENSE` for public open-source usage.
    - [x] `TASK-DOCS-01.04`: Validate full deterministic evaluation (100/100 PASS) and guardrails.

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
