# 🔒 Module: Security, Auth & Sensitive Data

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-SEC-01] Strictly validate sessions and permissions server-side at the start of every controller or action.
- [R-SEC-02] NEVER expose password hashes, tokens, or private keys to the client.
- [R-SEC-03] Encrypt at rest (AES-256) all user-provided secrets, tokens, or sensitive credentials.
- [R-SEC-04] Guarantee absolute integrity of environment variables (`.env`) without deleting existing keys.
