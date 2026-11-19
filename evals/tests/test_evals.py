#!/usr/bin/env python3
"""
Unit tests for Agentic RSI Protocol deterministic engine scripts.
Uses only Python standard library (unittest + tempfile + unittest.mock)
and executes cleanly in both source and synced target repositories.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

EVALS_DIR = Path(__file__).resolve().parent.parent
if str(EVALS_DIR) not in sys.path:
    sys.path.insert(0, str(EVALS_DIR))

import rsi_orchestrator
import security_audit
import telemetry_hook
import version_manager


class TestTelemetryHook(unittest.TestCase):
    def test_normalize_model_label_gemini4_defaults_to_hydrogen(self):
        self.assertEqual(telemetry_hook._normalize_model_label("Gemini 4 (Medium)"), "gemini-4-hydrogen")
        self.assertEqual(telemetry_hook._normalize_model_label("gemini-4-hydrogen"), "gemini-4-hydrogen")
        self.assertEqual(telemetry_hook._normalize_model_label("Gemini 4 Argon"), "gemini-4-argon")
        self.assertEqual(telemetry_hook._normalize_model_label("Gemini 3.8 Flash"), "gemini-3.8-flash")

    def test_verify_contract_accepts_backfill_and_live_rejects_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "evals" / "logs").mkdir(parents=True)
            (base / ".agents" / "telemetry").mkdir(parents=True)

            (base / "evals" / "logs" / "trajectory_latest.json").write_text(
                json.dumps({
                    "timestamp": "2026-11-17T00:00:00+00:00",
                    "mode": "FULL",
                    "task_id": "TASK-TEST-01",
                    "status": "PASS",
                    "total_score": 100,
                    "checks": [{"step": "unit", "passed": True, "duration_ms": 10}],
                }),
                encoding="utf-8",
            )

            state_path = base / ".agents" / "telemetry" / "cognitive_state.json"
            base_state = {
                "project_meta": {"project_name": "tmp"},
                "summary_kpis": {},
                "active_rules": [],
                "runs_history": [{
                    "run_id": "run_001",
                    "status": "SUCCESS",
                    "eval_score": 100,
                    "telemetry_source": "TASKS_MD_BACKFILL",
                    "metrics": {
                        "prompt_tokens": 100,
                        "output_tokens": 50,
                        "useful_actions": 2,
                        "wasted_actions": 0,
                    },
                }],
            }
            state_path.write_text(json.dumps(base_state), encoding="utf-8")
            self.assertTrue(telemetry_hook.verify_contract(base))

            base_state["runs_history"][0]["telemetry_source"] = "BOGUS_SOURCE"
            state_path.write_text(json.dumps(base_state), encoding="utf-8")
            self.assertFalse(telemetry_hook.verify_contract(base))


class TestOrchestratorParsers(unittest.TestCase):
    SAMPLE_TASKS = (
        "# [SSOT] TASKS.md\n\n"
        "## Active Sprint 01: Core\n\n"
        "- [-] **`TASK-ACT-01` - Active Task**\n"
        "  - **Target files:** `src/a.ts`\n\n"
        "- [!] **`TASK-BLK-01` - Blocked Impasse**\n"
        "  - **Target files:** `src/blocked.ts`\n\n"
        "- [x] **`TASK-DONE-01` - Closed Task**\n"
        "  - **Target files:** `src/done.ts`\n"
    )

    CLOSED_ONLY_TASKS = (
        "# [SSOT] TASKS.md\n\n"
        "## Active Sprint 01: Core\n\n"
        "- [!] **`TASK-BLK-01` - Blocked Impasse**\n"
        "  - **Target files:** `src/blocked.ts`\n\n"
        "- [x] **`TASK-DONE-01` - Closed Task**\n"
        "  - **Target files:** `src/done.ts`\n"
    )

    def test_parse_active_and_blocked_without_target_bleeding(self):
        with tempfile.TemporaryDirectory() as tmp:
            tasks_file = Path(tmp) / "TASKS.md"
            tasks_file.write_text(self.SAMPLE_TASKS, encoding="utf-8")
            with patch.object(rsi_orchestrator, "TASKS_PATH", tasks_file):
                active = rsi_orchestrator.parse_active_tasks(include_just_closed=False)
                self.assertEqual(len(active), 1)
                self.assertEqual(active[0]["id"], "TASK-ACT-01")
                self.assertEqual(active[0]["targets"], ["src/a.ts"])
                self.assertEqual(active[0]["status"], "active")

                blocked = rsi_orchestrator.parse_blocked_tasks()
                self.assertEqual(len(blocked), 1)
                self.assertEqual(blocked[0]["id"], "TASK-BLK-01")

    def test_parse_active_tasks_clean_post_commit_toggle(self):
        with tempfile.TemporaryDirectory() as tmp:
            tasks_file = Path(tmp) / "TASKS.md"
            tasks_file.write_text(self.CLOSED_ONLY_TASKS, encoding="utf-8")
            with patch.object(rsi_orchestrator, "TASKS_PATH", tasks_file):
                self.assertEqual(rsi_orchestrator.parse_active_tasks(include_just_closed=False), [])
                just_closed = rsi_orchestrator.parse_active_tasks(include_just_closed=True)
                self.assertEqual(len(just_closed), 1)
                self.assertEqual(just_closed[0]["id"], "TASK-DONE-01")
                self.assertEqual(just_closed[0]["status"], "closed")


class TestSecurityAudit(unittest.TestCase):
    def test_secrets_ascii_and_prisma_scope_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text(".env\n*.pem\n*.key\nnode_modules\n", encoding="utf-8")
            (root / ".env.example").write_text(
                'DATABASE_URL="postgresql://postgres.[VOTRE-PROJECT-REF]:[VOTRE-PASSWORD]@db.host:5432/postgres"\n',
                encoding="utf-8",
            )
            (root / "docs").mkdir()
            (root / "docs" / "README_FR.md").write_text(
                "Accent fran\u00e7ais: s\u00e9curit\u00e9 et int\u00e9grit\u00e9.\n"
                'DATABASE_URL="mongodb+srv://offeranalyst:YOUR_PASSWORD@cluster.mongodb.net"\n',
                encoding="utf-8",
            )
            (root / ".agents" / "skills" / "demo").mkdir(parents=True)
            (root / ".agents" / "skills" / "demo" / "SKILL.md").write_text(
                "sprintf('postgresql://%s:%s@%s:%s/%s')\n",
                encoding="utf-8",
            )
            (root / "scripts").mkdir()
            (root / "scripts" / "seed.mjs").write_text("const p = new PrismaClient();\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "bad.ts").write_text("const p = new PrismaClient();\n", encoding="utf-8")
            (root / "evals").mkdir()
            (root / "evals" / "clean.py").write_text("print('pure ascii')\n", encoding="utf-8")

            with patch.object(security_audit, "ROOT_DIR", root):
                self.assertEqual(security_audit.audit_secrets(), [])
                self.assertEqual(security_audit.audit_ascii_hygiene(), [])
                patterns = security_audit.audit_operational_patterns()
                self.assertEqual(len(patterns), 1)
                self.assertEqual(patterns[0]["file"], "src/bad.ts")

                sample_uri = "postgresql://" + "admin:r3alS3cr3tP4ss" + "@prod.internal:5432/app"
                (root / "src" / "leak.ts").write_text(
                    f'const url = "{sample_uri}";\n',
                    encoding="utf-8",
                )
                leaks = security_audit.audit_secrets()
                self.assertEqual(len(leaks), 1)
                self.assertEqual(leaks[0]["file"], "src/leak.ts")

    def test_skips_lockfiles_telemetry_and_binaries_without_coverage_loss(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text(".env\n*.pem\n*.key\nnode_modules\n", encoding="utf-8")
            (root / ".agents" / "telemetry").mkdir(parents=True)
            (root / ".agents" / "telemetry" / "cognitive_state.json").write_text(
                '{"note": "api_key = \\"super_secret_value_12345\\""}\n',
                encoding="utf-8",
            )
            (root / "pnpm-lock.yaml").write_text(
                'resolved: "https://registry.npmjs.org/pkg"\n',
                encoding="utf-8",
            )
            (root / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
            (root / "src").mkdir()
            sample_key_name = "API_" + "KEY"
            sample_key_val = "prod_tok_" + "9876543210abcdef"
            (root / "src" / "auth.ts").write_text(
                f'{sample_key_name} = "{sample_key_val}"\n'
                '// eval("commented out")\n'
                'eval("danger")\n',
                encoding="utf-8",
            )

            with patch.object(security_audit, "ROOT_DIR", root):
                leaks = security_audit.audit_secrets()
                self.assertEqual(len(leaks), 1)
                self.assertEqual(leaks[0]["file"], "src/auth.ts")
                self.assertEqual(leaks[0]["line"], 1)

                ops = security_audit.audit_operational_patterns()
                self.assertEqual(len(ops), 1)
                self.assertEqual(ops[0]["file"], "src/auth.ts")
                self.assertEqual(ops[0]["line"], 3)


class TestSyncTargetsRegistry(unittest.TestCase):
    def test_register_and_load_deduplicates_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg_file = Path(tmp) / "sync_targets.json"
            target_dir = Path(tmp) / "MyConsumerApp"
            target_dir.mkdir()
            with patch.object(version_manager, "SYNC_TARGETS_PATH", reg_file):
                version_manager.register_sync_target(target_dir, "0.1.0")
                version_manager.register_sync_target(target_dir, "0.2.0")
                targets = version_manager.load_sync_targets()
                self.assertEqual(len(targets), 1)
                self.assertEqual(targets[0]["protocol_version"], "0.2.0")
                self.assertEqual(targets[0]["name"], "MyConsumerApp")


if __name__ == "__main__":
    unittest.main()
