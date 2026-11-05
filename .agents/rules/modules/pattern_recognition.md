# Module: Pattern Recognition & Operational Reflexes

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-PAT-01] Cognitive Routing (System 1 vs System 2): Route routine CRUD, UI boilerplate, and standard tests to fast execution without redundant exploration; reserve deep architectural reasoning strictly for security boundaries, state synchronization, and concurrency.
- [R-PAT-02] Structural Mimicry (O(1) Reuse): Never invent a new architectural pattern (auth wrapper, DB singleton, API error response) if one already exists in the codebase; locate and replicate the canonical reference pattern.
- [R-PAT-03] Fast-Fail Diagnostic Reflex: Before manually debugging a test or CI failure, run `python evals/memory_engine.py --diagnose` to match known error signatures against deterministic 1-line fixes.
- [R-PAT-04] Operational Anti-Pattern Blockade: Never expose secret keys in public frontend variables (`NEXT_PUBLIC_*`, `VITE_*`, `PUBLIC_*`), never instantiate ORM clients outside a dedicated singleton, and never execute dynamic code (`eval`, `new Function`).
