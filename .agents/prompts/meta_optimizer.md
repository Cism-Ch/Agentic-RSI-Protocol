# Role: RSI Meta-Optimizer (Alias Pointer)

> **Canonical SSOT:** The authoritative `meta` persona lives in `.agents/prompts/rsi_specialist.md` (`PERSONA:meta`).
> Load it cleanly on demand via:
> ```bash
> python evals/memory_engine.py --propose
> python evals/memory_engine.py --persona meta
> ```
>
> **Core Invariants:** Zero redundancy, `< 80` lines per `.agents/rules/modules/*.md` (lossless merge first, or split with `<!-- triggers: ... -->`), imperative phrasing (`[R-DOM-XX] Always/Never...`), and prefer deterministic linters/tests over prose.
