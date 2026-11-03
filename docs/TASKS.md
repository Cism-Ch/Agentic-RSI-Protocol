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
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

---

## 🚀 Active Sprint 01: Project Setup & Initialization

- [x] **`TASK-I18N-01` — Repository Internationalization & English Translation**
  - **Priority:** 🔴 HIGH
  - **Target files:** `README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/TASKS.md`, `.agents/**/*`, `evals/**/*`, `.gitignore`
  - **Acceptance criteria:**
    - [x] `TASK-I18N-01.01`: Translate top-level and documentation files (`README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/TASKS.md`) into idiomatic English.
    - [x] `TASK-I18N-01.02`: Translate all agent prompts, core rules, modular sub-playbooks, and workflows in `.agents/` preserving the 80-line limit.
    - [x] `TASK-I18N-01.03`: Translate evaluation scripts and tooling in `evals/` (docstrings, log outputs, CLI help).
    - [x] `TASK-I18N-01.04`: Validate full deterministic evaluation and guardrails (`python evals/run_fullstack_eval.py` and `python evals/rsi_orchestrator.py --guardrail`).

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

