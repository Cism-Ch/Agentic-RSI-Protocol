# 🧬 RSI Protocol (Recursive Self-Improvement) — Standalone Template

This repository contains the **RSI Protocol**, an engineering engine and deterministic self-improvement framework for AI agents, completely decoupled from any specific project.

---

## 📁 Template Architecture

```
Agentic-RSI-Protocol/
├── .agents/
│   ├── prompts/
│   │   └── meta_optimizer.md        # Reflexive role for rule extraction and post-mortem optimization
│   ├── rules/
│   │   ├── system_core.md           # Immutable core engineering rules
│   │   ├── fullstack_playbook.md    # Index and routing layer for procedural memory
│   │   └── modules/                 # Modular sub-playbooks (< 80 lines each)
│   │       ├── api_backend.md
│   │       ├── db.md
│   │       ├── integration_ai.md
│   │       ├── security_auth.md
│   │       └── ui_frontend.md
│   └── workflows/
│       └── rsi-feature.md           # 4-phase workflow (Scoping -> Eval -> Meta -> Closure)
├── evals/
│   ├── memory_engine.py             # Contextual rule resolution & compactness auditor
│   ├── run_fullstack_eval.py        # Agnostic deterministic judge (multi-package managers)
│   ├── security_audit.py            # Static security scanner & leak detector
│   ├── stack_inspector.py           # Stack detection & official MCP/Skills recommendations
│   ├── rsi_orchestrator.py          # Retry loop controller (max 3) & integrity guardrails
│   └── version_manager.py           # SemVer incrementation & Changelog sealing
├── docs/
│   ├── TASKS.md                     # SSOT registry with strict 250-line ceiling
│   └── archive/tasks/               # Rollover directory for archived tasks
├── CHANGELOG.md                     # SemVer change history
├── AGENTS.md                        # Official charter & standards for AI agents
└── README.md                        # Documentation and onboarding guide
```

---

## 🚀 How to Use in a New Project

1. **Copy the Core Directories:**
   Copy `.agents/`, `evals/`, `docs/`, `CHANGELOG.md`, and `AGENTS.md` into the root of your target project.

2. **Add Script Aliases to `package.json`:**
   ```json
   "scripts": {
     "eval:quick": "python evals/run_fullstack_eval.py --quick",
     "eval:fullstack": "python evals/run_fullstack_eval.py",
     "rsi:inspect": "python evals/stack_inspector.py",
     "rsi:memory": "python evals/memory_engine.py --audit",
     "rsi:security": "python evals/security_audit.py"
   }
   ```

3. **Run the Initial Audit:**
   ```bash
   pnpm run rsi:inspect
   pnpm run eval:quick
   ```
