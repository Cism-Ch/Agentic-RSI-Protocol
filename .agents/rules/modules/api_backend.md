# Module: API & Backend
<!-- triggers: actions, route, api, controller, service, handler, server, redis, queue, webhook, upload -->

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-API-01] Consistently return predictable structures matching `{ success: true, data } | { success: false, error }`.
- [R-API-02] Enforce strict schema validation (e.g., Zod) and invoke the project's rate-limiter on every exposed public route, form, or Server Action (contact, quote/devis, auth, upload).
- [R-API-03] Process heavy tasks asynchronously via workers or message queues with cryptographic signature verification.
- [R-API-04] Make asynchronous jobs strictly idempotent to support automatic retries without side effects.
- [R-API-05] Validate allowed MIME types, maximum file size, and auth/ownership on every file upload or presigned URL endpoint before issuing access.
