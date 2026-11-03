# 🧬 Agentic RSI Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/RSI%20Judge-100%2F100%20PASS-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![ASCII Safe](https://img.shields.io/badge/Encoding-Pure%20ASCII%20Safe-success.svg)]()

> **The Recursive Self-Improvement (RSI) Protocol for Autonomous AI Coding Agents.**  
> A standalone, language-agnostic template and runtime governance framework that prevents AI hallucination, prevents context saturation, enforces strict deterministic testing, and enables agents to learn continuously from debugging incidents.

---

## 📑 Table of Contents

- [The Problem with AI Coding Agents](#-the-problem-with-ai-coding-agents)
- [The RSI Solution](#-the-rsi-solution)
- [Core Guarantees & Features](#-core-guarantees--features)
- [Quick Start](#-quick-start)
  - [Option A: Use as a GitHub Template](#option-a-use-as-a-github-template)
  - [Option B: Add to an Existing Project](#option-b-add-to-an-existing-project)
- [The 4-Phase RSI Lifecycle (`/rsi-feature`)](#-the-4-phase-rsi-lifecycle-rsi-feature)
- [Resetting Memory for a New Project (`/reset-rsi`)](#-resetting-memory-for-a-new-project-reset-rsi)
- [Repository Architecture](#-repository-architecture)
- [CLI Tooling Reference](#-cli-tooling-reference)
- [Inviolable Rules](#-inviolable-rules)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💥 The Problem with AI Coding Agents

Modern AI coding agents (Claude, Gemini, GPT-4, Cursor, Antigravity) are powerful, but quickly degrade when tackling real-world codebases:
1. **Context Window Saturation:** Agents dump hundreds of lines of prompt rules into chat, exhausting token budgets and degrading model reasoning.
2. **Unguided Coding:** Agents invent unvetted patterns or hallucinate implementations without checking against an agreed task specification.
3. **Repeated Mistakes:** When an agent debugs an issue, the lesson is lost once the session closes; the same bug is introduced again in the next prompt.
4. **Platform Encoding Failures:** Rich Unicode characters and emojis in test scripts trigger `UnicodeEncodeError: 'charmap'` crashes on standard Windows or CI terminals.

---

## 💡 The RSI Solution

The **Agentic RSI Protocol** introduces a self-contained, deterministic feedback loop:

```
+---------------------------------------------------------------------------------+
|                               RSI FEEDBACK LOOP                                 |
|                                                                                 |
|   1. TASK SCOPING       2. CONTEXT INJECTION     3. DETERMINISTIC EVALUATION   |
|   [docs/TASKS.md]   ->   [Modular Rules < 80L] -> [run_fullstack_eval.py]      |
|                                                              |                  |
|                                                  PASS (100)  |  FAIL (< 100)    |
|                                                      v       v                  |
|   5. RELEASE & SEAL     4. META-OPTIMIZATION <---------------+ (Max 3 retries)  |
|   [SemVer Bump Patch]    [Distill Rule into Modules]                            |
+---------------------------------------------------------------------------------+
```

- **Inviolable SSOT (`docs/TASKS.md`):** Agents are strictly forbidden from writing code without an explicit task registered in the tracking board.
- **Memory Duality:** Ephemeral progress stays in IDE artifacts; permanent procedural memory is distilled into tiny domain modules (`< 80 lines`).
- **Reflexive Retry Loop:** The agent has up to 3 automatic attempts to reach a deterministic 100/100 evaluation score.
- **Meta-Cognitive Mutation:** If a bug or vulnerability was fixed, the agent automatically distills a new rule into `.agents/rules/modules/` so the mistake is never repeated.
- **Pure ASCII Tooling:** 100% of the evaluation suite runs in pure ASCII to guarantee zero encoding crashes on Windows (CP1252), Linux, or macOS.

---

## ⚡ Core Guarantees & Features

- **Language & Package Manager Agnostic:** Detects and adapts automatically to `pnpm`, `bun`, `yarn`, `npm`, and `python`.
- **Adaptive Deterministic Judge:** Dynamically tests TypeScript compilation (`tsc --noEmit`), linters, ORM schemas (Prisma, Drizzle), and memory hygiene.
- **Static Security Audit:** Continuously scans for hardcoded API keys, private certificates, AWS/Slack/GitHub tokens, and verifies airtight `.gitignore` settings.
- **Strict Size Guardrails:** Enforces `< 250 lines` on `docs/TASKS.md` (with automatic rollover) and `< 80 lines` on rule sub-modules.
- **Automated SemVer Releases:** Bumps versions, updates `package.json`, seals `CHANGELOG.md`, and prepares Git tags automatically.
- **Instant Project Reset (`/reset-rsi`):** Safely wipe template memory to kick off your own brand-new project with a single command.

---

## 🚀 Quick Start

### Option A: Use as a GitHub Template

1. Click **"Use this template"** > **"Create a new repository"** on GitHub.
2. Clone your new repository locally:
   ```bash
   git clone https://github.com/your-username/your-new-project.git
   cd your-new-project
   ```
3. Reset template task memory to a pristine baseline:
   ```bash
   python evals/reset_rsi.py --force
   ```
4. Verify your clean setup:
   ```bash
   python evals/run_fullstack_eval.py --quick
   ```

### Option B: Add to an Existing Project

Copy the core directories into your existing repository root:
```bash
cp -r .agents/ evals/ docs/ CHANGELOG.md AGENTS.md /path/to/your/project/
```

Add these handy shortcuts to your `package.json`:
```json
{
  "scripts": {
    "eval:quick": "python evals/run_fullstack_eval.py --quick",
    "eval:fullstack": "python evals/run_fullstack_eval.py",
    "rsi:inspect": "python evals/stack_inspector.py",
    "rsi:memory": "python evals/memory_engine.py --audit",
    "rsi:security": "python evals/security_audit.py",
    "rsi:reset": "python evals/reset_rsi.py"
  }
}
```

---

## 🔄 The 4-Phase RSI Lifecycle (`/rsi-feature`)

Whenever you or your AI agent develop a feature, trigger the `/rsi-feature` workflow:

### Phase 1: Scoping & Dynamic Injection
1. Formalize the task in `docs/TASKS.md` with priority and checkable acceptance criteria (`[ ]`).
2. Mark status as `[-]` (In progress).
3. Run `python evals/memory_engine.py --inject [files]` to load only the relevant domain rules.

### Phase 2: Deterministic Evaluation
Run the fast judge during development:
```bash
python evals/run_fullstack_eval.py --quick
```
If checks fail, inspect `evals/logs/trajectory_latest.json`, apply fixes, and re-run through the orchestrator:
```bash
python evals/rsi_orchestrator.py --eval --attempt 2
```

### Phase 3: Meta-Cognitive Mutation
If a bug, edge case, or security leak was repaired during the task:
1. Adopt the persona defined in `.agents/prompts/meta_optimizer.md`.
2. Distill the lesson into a compact, imperative rule (`[R-DOM-XX] Always...`).
3. Add it to the matching module in `.agents/rules/modules/` while keeping the file under 80 lines.

### Phase 4: Final Validation & Closure
1. Verify guardrails: `python evals/rsi_orchestrator.py --guardrail`.
2. Run full evaluation: `python evals/run_fullstack_eval.py` (100/100 required).
3. Bump release: `python evals/version_manager.py --bump patch`.
4. Check off criteria in `docs/TASKS.md` and mark as `[x]`.

---

## 🧹 Resetting Memory for a New Project (`/reset-rsi`)

To start fresh without carrying over previous sprint tasks or changelog entries:

```bash
# Dry run to preview changes
python evals/reset_rsi.py --dry-run

# Execute reset (automatically creates a zip backup in evals/backups/)
python evals/reset_rsi.py --force
```

Or simply tell your AI agent:
> `/reset-rsi`

---

## 📁 Repository Architecture

```
Agentic-RSI-Protocol/
├── .agents/
│   ├── prompts/
│   │   └── meta_optimizer.md        # Reflexive role for post-mortem rule extraction
│   ├── rules/
│   │   ├── system_core.md           # Invariant engineering rules
│   │   ├── fullstack_playbook.md    # Index & routing layer for procedural memory
│   │   └── modules/                 # Atomic domain playbooks (< 80 lines each)
│   │       ├── api_backend.md       # API, route handlers, async jobs, queues
│   │       ├── db.md                # ORM schema, migrations, connection hygiene
│   │       ├── integration_ai.md    # LLM inference, structured output, fallbacks
│   │       ├── security_auth.md     # Secrets, sessions, permissions, encryption
│   │       └── ui_frontend.md       # Responsive UI, accessibility, 4 visual states
│   └── workflows/
│       ├── rsi-feature.md           # 4-phase feature development workflow
│       └── reset-rsi.md             # Clean-slate project reset workflow
├── evals/
│   ├── memory_engine.py             # Memory auditor (< 80L) & contextual rule injector
│   ├── reset_rsi.py                 # Pure ASCII task & changelog reset engine
│   ├── rsi_orchestrator.py          # Retry loop controller (max 3) & guardrail checker
│   ├── run_fullstack_eval.py        # Adaptive deterministic judge (multi-package managers)
│   ├── security_audit.py            # Static secret scanner & .gitignore leak validator
│   ├── stack_inspector.py           # Ecosystem detector & official tooling advisor
│   └── version_manager.py           # SemVer version bump & changelog sealer
├── docs/
│   ├── ARCHITECTURE.md              # Deep architectural overview & diagrams
│   ├── TASKS.md                     # Single Source of Truth task registry (< 250L)
│   └── archive/tasks/               # Archive folder for completed sprint rollovers
├── .gitignore                       # Production-grade airtight secret & cache filter
├── AGENTS.md                        # Formal AI agent contract & behavioral charter
├── CHANGELOG.md                     # Keep-a-Changelog SemVer tracking
├── CONTRIBUTING.md                  # Contribution standards (ASCII, tests, PRs)
├── LICENSE                          # MIT License
└── README.md                        # Documentation & onboarding guide
```

---

## 🛠️ CLI Tooling Reference

All tools are located in `evals/` and require Python 3.10+:

| Command | Purpose | Common Flags |
| :--- | :--- | :--- |
| `python evals/run_fullstack_eval.py` | Runs all deterministic tests (types, lint, security, db) | `--quick` (skips slow build) |
| `python evals/security_audit.py` | Scans for hardcoded secrets, tokens, and checks `.gitignore` | *(None)* |
| `python evals/memory_engine.py` | Audits module line limits or injects rules | `--audit`, `--inject [files...]` |
| `python evals/stack_inspector.py` | Inspects stack dependencies and recommends official tools | *(None)* |
| `python evals/reset_rsi.py` | Resets task board and changelog to clean baseline | `--dry-run`, `--force`, `--no-backup` |
| `python evals/rsi_orchestrator.py` | Runs evaluation loops with retry counters | `--eval`, `--attempt 1..3`, `--guardrail` |
| `python evals/version_manager.py` | Bumps SemVer release and seals changelog | `--bump [major\|minor\|patch]` |

---

## 🛡️ Inviolable Rules

Every AI agent operating in this repository is bound by the rules in `AGENTS.md`:

1. **Strict Typing & Invariant Quality:** Zero type errors (`tsc --noEmit`), zero lint errors.
2. **No Unregistered Coding:** Work must always be attached to a `TASK-DOMAIN-XX` in `docs/TASKS.md`.
3. **Validation Before Closure:** Never close a task without obtaining a 100/100 score from `run_fullstack_eval.py`.
4. **Strict Size Limits:** `docs/TASKS.md` must not exceed **250 lines**; modules must not exceed **80 lines**.
5. **Pure ASCII Output:** No emojis or multi-byte unicode characters in CLI tooling to guarantee cross-platform compatibility.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on pull requests, coding style, and mandatory pure ASCII compatibility.

---

## 📄 License

This project is open-source and distributed under the [MIT License](LICENSE).
