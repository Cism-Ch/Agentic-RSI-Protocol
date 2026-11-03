# ⚡ Module: API & Backend

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-API-01] Consistently return predictable structures matching `{ success: true, data } | { success: false, error }`.
- [R-API-02] Protect sensitive endpoints and submission forms with rate-limiting.
- [R-API-03] Process heavy tasks asynchronously via workers or message queues with signature verification.
- [R-API-04] Make asynchronous jobs strictly idempotent to support automatic retries without side effects.
