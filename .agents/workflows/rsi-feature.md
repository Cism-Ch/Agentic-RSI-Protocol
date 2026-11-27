---
description: Develop an end-to-end feature with a deterministic 4-phase Recursive Self-Improvement (RSI) cycle.
---

# Workflow: /rsi-feature

This workflow formalizes the Recursive Self-Improvement (RSI) protocol for any AI agent.

> **Fast-Track `[Scope: XS]`:** For localized micro-edits (`<= 2` files, `Blast Radius: LOW`, outside DB/Auth/API/security), register a compact entry in `docs/TASKS.md`, skip `--map`/`--impact`/`rsi-specialist` and Phase 3 (unless `rsi_learning_trigger` fires), then validate with `run_fullstack_eval.py` and `--guardrail` before closing.

For `S`/`M`/`L`/`XL` tasks, follow these 4 sequential phases:

---

## PHASE 1: Preparation & Initial Execution

1. **Cold-Start Pulse & SSOT Task Check (`docs/TASKS.md`):**
   - Run `python evals/rsi_orchestrator.py --pulse` to get an instant briefing on repository health, active tasks, git workspace, and recommended rule modules.
   - Ensure the task exists in `docs/TASKS.md` in the format `TASK-DOMAIN-XX`.
   - If `docs/TASKS.md` approaches 250 lines, run `python evals/rsi_orchestrator.py --rollover` to archive completed `[x]` sprint blocks into `docs/archive/tasks/`.
   - If the task is missing, formalize it immediately with ID, priority, `Target files`, and checkable criteria `[ ]`.
   - Update its status to `[-]` (In progress) in the Kanban and active section.
   - **Episodic Memory (IDE Artifact):** If the task requires multi-step planning or extended tracking, initialize a Markdown Artifact (`plan.md` or `task_tracking.md`) in the IDE's Brain directory. The artifact acts as an out-of-context visual board. Never dump full artifact contents into chat messages to conserve context tokens.

2. **Stack Audit, Topological Map & Blast Radius:**
   - Run `python evals/stack_inspector.py` (or `pnpm run rsi:inspect`) to verify official tooling (MCP servers, framework/ORM skills).
   - Run `python evals/stack_inspector.py --map` to inspect existing singletons and top dependency hubs in `O(1)` before creating new helpers.
   - Before modifying a shared module or interface, run `python evals/stack_inspector.py --impact [file]` to evaluate its reverse-dependency Blast Radius.

3. **Dynamic Contextual Memory Resolution:**
   - Run `python evals/memory_engine.py --inject [target_files]` to inject only the relevant atomic sub-playbooks (`.agents/rules/modules/`) without saturating the context window.
   - Read `.agents/rules/system_core.md` for project-wide invariant rules.

4. **End-to-End Implementation with Anti-Saturation Cadence:**
   - **Local micro-edits:** During routine component/function coding, do NOT trigger global checks (`tsc`/`lint`). Keep editing flow fluid (0 tokens wasted).
   - **Backend / Database:** Model data persistence and APIs with strict input validation (e.g., Zod) and strong typing.
   - **Frontend:** Build interfaces with complete state coverage (`loading`, `error`, `empty`, `data`).
   - **Hygiene:** Exclusively use clean import aliases, removing any unused variables or imports.

---

## PHASE 2: Deterministic Evaluation & Reflexive Loop (Max 3 Attempts)

1. **Run Deterministic Judge (Milestone vs. Closure Cadence):**
   - **Mid-task / Milestone check:** Always run the compact quick mode:
     ```bash
     python evals/run_fullstack_eval.py --quick
     # or pnpm run eval:quick
     ```
     The compact JSON output (with `failed_steps` truncated to 10 lines) protects the agent's context budget.
   - **Before final closure only:** Run the full test suite:
     ```bash
     python evals/run_fullstack_eval.py
     # or pnpm run eval:fullstack
     ```

2. **If Score is 100/100 on Attempt 1:**
   - If the task was a **security audit, debugging session, or refactor** that exposed and resolved code defects: **Execute PHASE 3** to record critical learnings into the playbook.
   - If it was a standard feature addition without novel anti-patterns: Proceed directly to **PHASE 4**.

3. **If Score is Below 100/100:**
   - Inspect the compact failure report in `evals/logs/trajectory_latest.json`.
   - Identify the exact root cause (Typecheck, Lint, Test, or Schema).
   - Fix application code and re-evaluate:
     ```bash
     python evals/rsi_orchestrator.py --eval --attempt 2
     ```
   - Iterate until reaching 100/100 (maximum 3 attempts), without weakening tests or `evals/` validators to bypass failures.
   - *If the score remains below 100 after 3 attempts, or if an external/structural blocker is hit (missing secret, conflicting rule, suspected validator false positive), halt immediately, mark the task `[!]` (`BLOCKED`) in `docs/TASKS.md`, and request human guidance with exact logs, attempted fixes, and options.*

---

## PHASE 3: Meta-Cognitive Mutation & Specialist Review (Learning & Optimization)

- **On-Demand Maker / Checker Review (for `M`/`L`/`XL` tasks or sensitive layers):** Before closure, summon an isolated read-only persona via `python evals/memory_engine.py --persona <architect|db|security|ui|qa>` (`0` overhead on `XS`/`S` edits). Collect any `CAPITALIZATION_CANDIDATE` emitted in its verdict.
- **Meta-Cognitive Distillation:** Triggers automatically when `rsi_learning_trigger` fires on `FAIL -> PASS` recovery, after security audits/refactors, or on accepted `CAPITALIZATION_CANDIDATE` items:

1. Run `python evals/memory_engine.py --propose` to review resolved failures and next available `[R-DOM-XX]` IDs.
2. If a recurring or structural lesson applies (skip one-off typos), load `python evals/memory_engine.py --persona meta`.
3. Formulate a general, preventive 1-2 line rule (`- [R-DOM-XX] Always/Never...`) — preferring deterministic linters/tests over prose when automatable.
4. **Anti-Bloat & Auto-Discovery (`< 80` lines):** Merge semantically overlapping rules first; if all rules are distinct and the module nears 80 lines, split into a new `.agents/rules/modules/<domain>.md` with an inline `<!-- triggers: kw1, kw2 -->` header (auto-discovered across `--sync-all` updates) and validate via `python evals/memory_engine.py --audit`.

---

## PHASE 4: Final Validation, Git Guardrail & Closure

1. **Verify Guardrails & Scope Alignment:**
   ```bash
   python evals/rsi_orchestrator.py --guardrail
   ```
   Confirm `docs/TASKS.md` (`< 250L`), modules (`< 80L`), and Scope Guard (`git status` aligned with `Target files` in `docs/TASKS.md`).
2. **Double Deterministic Check & Pre-Closure Quality Gate:**
   - Typecheck (0 errors) and Linter (0 errors / warnings).
   - **UI & Structural Gate:** Confirm any added/edited page inherits the canonical layout (`Header`/`Footer`), uses design-system tokens/primitives, and leaves 0 orphaned components after refactors (verify with `python evals/stack_inspector.py --impact <file>`).
   - **Secure-by-Default Gate:** Confirm any public route/action (contact, quote, upload, auth) applies schema validation + rate-limiting, and any upload/presigned URL enforces MIME type, max size, and auth/ownership checks.
   - **Sprint-End Gate (at Sprint Closure before final commit):** Run `python evals/rsi_orchestrator.py --sprint-gate` for net-new dependency CVE audit, oversized `public/` assets (> 500 KB), static N+1 DB loop patterns, and LCP check reminder on modified UI pages (without re-running already-passed task checks).
3. **Optional Release Sealing (on user request or Sprint release only):**
   - When sealing a release (not required on every individual task), run `python evals/version_manager.py --bump <patch|minor|major>` to bump version and seal `CHANGELOG.md`.
4. **SSOT Task Closure in `docs/TASKS.md`:**
   - Check off all acceptance criteria `[x]`.
   - Mark task completed `[x]`.
   - Move task entry to `Completed Tasks History` with date and list of created/modified files.
   - Update the synthetic Kanban table.
5. **Final User Report:**
   - Delivered and verified feature (100/100 score).
   - Sealed SemVer release.
   - Number of attempts required.
   - Lessons learned and newly registered rules (with exact diff if applicable).
6. **Post-Commit Target Sync (Protocol Repository Only):**
   - After committing changes on `Agentic-RSI-Protocol`, run `python evals/rsi_orchestrator.py --sync-targets` to inspect locally registered target workspaces (`.agents/telemetry/sync_targets.json`).
   - Ask the user for confirmation before executing `python evals/rsi_orchestrator.py --sync-all` or `--sync-to <TARGET_DIR>` on known targets.
   - Also ask the user to signal any other unsynchronized project by providing its disk path / working directory so `--sync-to <TARGET_DIR>` can be executed automatically (explaining that if they do not have the path on hand, they can ask in that project's workspace for its working directory path and paste it into this conversation).
   - If `--sync-to` backs up a pre-existing `AGENTS.md` to `evals/backups/AGENTS.md.<timestamp>.bak`, evaluate its rules against `.agents/rules/system_core.md` and `.agents/rules/modules/` and ask the user whether to preserve uncovered or conflicting project rules in `AGENTS.md` (`## Project-Specific Rules`) or in a domain module.
