# 🗄️ Module: Database & Persistence

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-DB-01] Systematically validate input data using a schema validator (e.g., Zod) before any database write.
- [R-DB-02] Use a singleton client to prevent connection exhaustion on serverless runtimes.
- [R-DB-03] Never perform destructive, unindexed mutations on large datasets.
- [R-DB-04] Always isolate unique identifiers according to the database adapter specification.
