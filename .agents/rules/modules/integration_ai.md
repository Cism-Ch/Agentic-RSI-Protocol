# Module: AI Integration, Agents & LLMs

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-AI-01] Systematically structure LLM outputs using strict JSON formatting validated against schemas.
- [R-AI-02] Isolate model calls behind a fallback interface to gracefully handle single-provider outages.
- [R-AI-03] Never store third-party API keys in plaintext within code or public repositories.
- [R-AI-04] Control and truncate context streams to respect agent inference windows and token budgets.
