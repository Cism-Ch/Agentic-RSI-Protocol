# 📋 TASKS.md — Central Registry & Unified Task Tracker (RSI Template)

> **Single Source of Truth (SSOT)** for orchestrating and tracking all technical and functional tasks.  
> **Absolute rule for any AI Agent:** This document MUST be consulted before every task and updated immediately upon completion. Strict ceiling: **250 lines**.

---

## 📌 Synthetic Kanban View

```
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│ 🚀 IN PROGRESS (SP 01)  │  │   ⏳ FUTURE BACKLOG     │  │       ✅ ARCHIVES       │
├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────────┤
│ [ ] TASK-INIT-01        │  │ [ ] Future task 1       │  │ [x] TASK-GIT-01         │
│                         │  │                         │  │ [x] TASK-I18N-01        │
│                         │  │                         │  │ [x] TASK-SCRIPTS-01     │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

---

## 🚀 Active Sprint 01: Project Setup & Initialization

- [x] **`TASK-SCRIPTS-01` — Clean Emojis & Standardize ASCII Logging in Scripts**
  - **Priority:** 🔴 HIGH
  - **Target files:** `evals/memory_engine.py`, `evals/rsi_orchestrator.py`, `evals/run_fullstack_eval.py`, `evals/security_audit.py`, `evals/stack_inspector.py`, `evals/version_manager.py`, `docs/TASKS.md`
  - **Acceptance criteria:**
    - [x] `TASK-SCRIPTS-01.01`: Replace all emojis with robust ASCII tags (`[OK]`, `[FAIL]`, `[WARN]`, `[INFO]`, `->`) across all scripts in `evals/`.
    - [x] `TASK-SCRIPTS-01.02`: Ensure 100% pure ASCII compatibility without character encoding errors on any terminal (CP1252 / ISO).
    - [x] `TASK-SCRIPTS-01.03`: Validate deterministic evaluation passes (`python evals/run_fullstack_eval.py` 100/100 PASS).

- [ ] **`TASK-INIT-01` — Project Scaffolding & Initial Setup**
  - **Priority:** 🟡 MEDIUM
  - **Target files:** `package.json`, `README.md`
  - **Acceptance criteria:**
    - [ ] `TASK-INIT-01.01`: Technical baseline and dependency configuration.
    - [ ] `TASK-INIT-01.02`: Deterministic validation with `python evals/run_fullstack_eval.py --quick` (100/100 PASS).

---

## 📜 Completed Tasks History

| Date | Task ID | Title & Description | Created / Modified Files |
| :--- | :--- | :--- | :--- |
| 2026-11-03 | TASK-GIT-01 | Git Initialization & Security Audits | `.gitignore`, `evals/security_audit.py`, `evals/run_fullstack_eval.py`, `docs/TASKS.md` |
| 2026-11-03 | TASK-I18N-01 | Complete Repository Internationalization (EN) | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/TASKS.md`, `.agents/**/*`, `evals/**/*`, `.gitignore` |
| 2026-11-03 | TASK-SCRIPTS-01 | Clean Emojis & Pure ASCII Output in Scripts | `evals/memory_engine.py`, `evals/rsi_orchestrator.py`, `evals/security_audit.py`, `evals/stack_inspector.py`, `evals/version_manager.py`, `docs/TASKS.md` |

