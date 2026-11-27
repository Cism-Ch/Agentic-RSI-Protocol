<!-- RSI-PROTOCOL:START -->
# AGENTS.md - AI Agent Reference & RSI Protocol

This document governs engineering guidelines, codebase governance, and the Recursive Self-Improvement (RSI) protocol.

---

### Inviolable Rules Summary

1. **Engineering & Security Invariants (SSOT: `.agents/rules/system_core.md` + `modules/`):**
   - Zero type/lint errors, strict runtime validation, UI canonical layout/design-system fidelity with 0 orphaned components (`ui_frontend.md`), and secure-by-default public routes/actions/uploads (`api_backend.md`, `security_auth.md`).
2. **Task Tracking (Inviolable SSOT - `docs/TASKS.md`, `< 250` lines):**
   - **No Unregistered Coding:** Attach every change to a task (`TASK-DOMAIN-XX`) with `Target files` and criteria. Mark `[-]` at start, `[!]` (`BLOCKED`) on unresolvable impasse, `[x]` after `python evals/run_fullstack_eval.py` (`100/100 PASS`). Never weaken tests or validators to bypass a failure without explicit user approval.
   - **Fast-Track `[Scope: XS]`:** For `<= 2` files with `Blast Radius: LOW` outside DB/Auth/API/security, skip `--map`, `--impact`, `rsi-specialist`, and Phase 3 (unless a `Learning Trigger` fires).
3. **RSI Protocol (Recursive Self-Improvement):**
   - **Modular Procedural Memory:** Load targeted `< 80L` modules via `python evals/memory_engine.py --inject [files]` (auto-discovers custom `*.md` modules via `<!-- triggers: ... -->`).
   - **Closed Learning Loop:** On `FAIL -> PASS` recovery (`rsi_learning_trigger`), security audits, or specialist `CAPITALIZATION_CANDIDATE` findings, run `python evals/memory_engine.py --propose` and `--persona meta` if a recurring/structural lesson applies.
   - **On-Demand Specialist Reviews (`rsi-specialist`):** For `M`/`L`/`XL` tasks or sensitive layers, summon an isolated read-only persona via `python evals/memory_engine.py --persona <architect|db|security|ui|qa>`.
   - **Workflow & Operations:** Follow `/rsi-feature` (`.agents/workflows/rsi-feature.md`) and `docs/AGENT_OPERATIONS.md`.
   - **Post-Commit Target Sync:** On the source protocol repo, always ask the user before running `--sync-all` / `--sync-to <dir>` and ask for any other unsynchronized project disk paths. If `--sync-to` backs up a pre-existing `AGENTS.md`, evaluate its rules against `system_core.md` / `modules/` and ask the user how to merge uncovered or conflicting rules.
4. **Anti-Saturation Test Cadence & Memory Duality:**
   - Micro-edits without global suite -> Milestone `--quick` -> Task closure full eval -> Sprint closure `--sprint-gate`. IDE Artifacts for episodic memory; `.agents/rules/modules/` for durable procedural rules.
5. **Mandatory Pre-Commit Security & Performance Audit:**
   - Before any `git commit`, verify `evals/security_audit.py` (0 secrets, anti-patterns, or supply-chain alerts), run `python evals/rsi_orchestrator.py --sprint-gate` (prod CVEs, oversized `public/` assets, N+1 DB loops, LCP review on modified UI pages), and confirm zero unvalidated inputs, missing rate-limits, or insecure shortcuts in the diff.
<!-- RSI-PROTOCOL:END -->

## Project-Specific Rules

<!-- Preserved automatically across --sync-to / --sync-all updates. Add project-specific invariants or overrides below. -->
