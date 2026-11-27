#!/usr/bin/env python3
"""
RSI Modular Memory Resolution and Audit Engine
- Targeted contextual indexing and loading of sub-playbooks (.agents/rules/modules/)
- Anti-bloat verification (< 80 lines per sub-module)
- Fully generic and reusable across projects
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT_DIR / ".agents" / "rules" / "modules"
SPECIALIST_CATALOG_FILE = ROOT_DIR / ".agents" / "prompts" / "rsi_specialist.md"
TRAJECTORY_FILE = ROOT_DIR / "evals" / "logs" / "trajectory_latest.json"
ACTIVE_SESSION_FILE = ROOT_DIR / ".agents" / "telemetry" / "active_session.json"
MAX_LINES_PER_MODULE = 80
MAX_LINES_PER_PERSONA = 40
RULE_ID_PATTERN = re.compile(r"\[(R-[A-Z0-9\-]+)\]")
RULE_LINE_RE = re.compile(r"^\s*-\s*\[(R-[A-Z0-9\-]+)\]\s*(.+)$")
TRIGGER_COMMENT_RE = re.compile(r"<!--\s*triggers:\s*(.+?)\s*-->", re.IGNORECASE)
PERSONA_BLOCK_RE = re.compile(
    r"<!--\s*PERSONA:([a-zA-Z0-9_\-]+):START\s*-->(.*?)<!--\s*PERSONA:\1:END\s*-->",
    re.DOTALL,
)

MODULE_TRIGGERS = {
    "db.md": ["prisma", "schema", "model", "migration", "database", "sql", "mongo", "db", "drizzle"],
    "api_backend.md": ["actions", "route", "api", "controller", "service", "handler", "server", "redis", "queue"],
    "ui_frontend.md": ["component", "components", "page", "layout", "view", "css", "tailwind", "tsx", "jsx", "styles"],
    "security_auth.md": ["auth", "session", "crypto", "token", "jwt", "permission", "security", "hash", "secret"],
    "integration_ai.md": ["ai", "llm", "agent", "prompt", "openai", "gemini", "anthropic", "openrouter", "rag"],
    "pattern_recognition.md": ["pattern", "architecture", "core", "utils", "lib", "helper", "config", "eval"]
}

KNOWN_ERROR_PATTERNS = [
    (
        re.compile(r"Non-ASCII / Emoji Character|UnicodeEncodeError|charmap", re.IGNORECASE),
        "[CORE-ASCII] ASCII & Emoji Hygiene Violation",
        "Strip all emojis, smart quotes, em-dashes, and Unicode arrows (>127) from evals/**/*.py scripts and CLI output."
    ),
    (
        re.compile(r"LIMIT EXCEEDED|exceed the maximum allowed line count", re.IGNORECASE),
        "[CORE-MEM-80L] Module or Persona Line Ceiling Exceeded",
        "Synthesize redundant rules without losing specificity, or split the module into finer domain files with <!-- triggers: ... -->."
    ),
    (
        re.compile(r"Errno 2.*No such file or directory.*python", re.IGNORECASE),
        "[R-PAT-03] Subprocess Shell Quoting Mismatch on Unix/CI",
        "Pass tokenized command lists [sys.executable, str(script_path), '--flag'] to subprocess.run with shell=False."
    ),
    (
        re.compile(r"potential secret leak|Hardcoded Auth Secret|Private Key", re.IGNORECASE),
        "[R-SEC-02] Exposed Secret or Credential in Source",
        "Move the credential immediately to .env (git-ignored) and reference it via validated server environment variables."
    ),
    (
        re.compile(r"Operational Anti-Pattern|PrismaClient|NEXT_PUBLIC_|VITE_", re.IGNORECASE),
        "[R-PAT-04] Operational Security or Singleton Violation",
        "Remove secret keys from public frontend env vars and instantiate ORM clients strictly inside a dedicated singleton file."
    ),
    (
        re.compile(r"TS\d{4}:|error TS|Type '.*' is not assignable", re.IGNORECASE),
        "[CORE-STRICT-TS] Strict TypeScript Type Mismatch",
        "Align explicit return types and validate external payloads with Zod before passing to typed functions."
    )
]


def discover_module_triggers(modules_dir: Path | None = None) -> dict[str, list[str]]:
    """Auto-discovers all *.md modules and their triggers (inline <!-- triggers: --> + defaults + filename tokens)."""
    target_dir = modules_dir or MODULES_DIR
    discovered: dict[str, list[str]] = {}
    if not target_dir.exists():
        return dict(MODULE_TRIGGERS)

    for mod in sorted(target_dir.glob("*.md")):
        triggers: list[str] = []
        try:
            head_lines = mod.read_text(encoding="utf-8", errors="ignore").splitlines()[:8]
            for ln in head_lines:
                m = TRIGGER_COMMENT_RE.search(ln)
                if m:
                    for raw_kw in m.group(1).split(","):
                        kw = raw_kw.strip().lower()
                        if kw and kw not in triggers:
                            triggers.append(kw)
                    break
        except Exception:
            pass

        if not triggers and mod.name in MODULE_TRIGGERS:
            triggers.extend(MODULE_TRIGGERS[mod.name])

        for tok in re.split(r"[_\-\s]+", mod.stem.lower()):
            if len(tok) >= 2 and tok not in triggers:
                triggers.append(tok)

        discovered[mod.name] = triggers
    return discovered


def compute_next_rule_ids(modules_dir: Path | None = None) -> dict[str, str]:
    """Computes the next available [R-XXX-NN] rule identifier for every module."""
    target_dir = modules_dir or MODULES_DIR
    next_ids: dict[str, str] = {}
    if not target_dir.exists():
        return next_ids

    for mod in sorted(target_dir.glob("*.md")):
        prefix_counts: dict[str, int] = {}
        max_num = 0
        try:
            for ln in mod.read_text(encoding="utf-8", errors="ignore").splitlines():
                for rid in RULE_ID_PATTERN.findall(ln):
                    m = re.match(r"^(R-[A-Z0-9]+)-(\d+)$", rid)
                    if m:
                        pref, num = m.group(1), int(m.group(2))
                        prefix_counts[pref] = prefix_counts.get(pref, 0) + 1
                        if num > max_num:
                            max_num = num
        except Exception:
            pass

        if prefix_counts:
            best_prefix = max(prefix_counts.items(), key=lambda kv: kv[1])[0]
        else:
            stem_tok = re.sub(r"[^A-Z0-9]", "", mod.stem.split("_")[0].upper())[:6] or "MOD"
            best_prefix = f"R-{stem_tok}"
        next_ids[mod.name] = f"[{best_prefix}-{max_num + 1:02d}]"
    return next_ids

def parse_specialist_personas(catalog_path: Path | None = None) -> tuple[str, dict[str, str]]:
    """Parses CORE and tagged PERSONA blocks from .agents/prompts/rsi_specialist.md."""
    target = catalog_path or SPECIALIST_CATALOG_FILE
    if not target.exists():
        return "", {}
    text = target.read_text(encoding="utf-8", errors="ignore")
    core = ""
    personas: dict[str, str] = {}
    for match in PERSONA_BLOCK_RE.finditer(text):
        key = match.group(1).strip().lower()
        body = match.group(2).strip()
        if key == "core":
            core = body
        else:
            personas[key] = body
    return core, personas

def resolve_persona(persona_name: str, catalog_path: Path | None = None) -> tuple[bool, str]:
    """Extracts CORE + requested specialist persona block without loading unrelated personas."""
    core, personas = parse_specialist_personas(catalog_path)
    if not personas:
        return False, "[WARN] Specialist catalog not found or contains 0 tagged personas."
    key = persona_name.strip().lower()
    if key not in personas:
        avail = ", ".join(sorted(personas.keys()))
        return False, f"[FAIL] Unknown persona '{persona_name}'. Available personas: {avail}"
    parts = [f"[RSI Specialist Persona: {key}]"]
    if core:
        parts.append("\n" + core)
    parts.append("\n" + personas[key])
    return True, "\n".join(parts)

def list_personas(catalog_path: Path | None = None) -> list[str]:
    """Prints available specialist personas with non-empty line counts."""
    _, personas = parse_specialist_personas(catalog_path)
    if not personas:
        print("[INFO] No specialist personas configured in .agents/prompts/rsi_specialist.md.")
        return []
    print(f"[RSI Specialist Catalog] {len(personas)} available persona(s):")
    for name in sorted(personas.keys()):
        lines = len([ln for ln in personas[name].splitlines() if ln.strip()])
        print(f"  - {name} ({lines}/{MAX_LINES_PER_PERSONA} lines) -> python evals/memory_engine.py --persona {name}")
    return sorted(personas.keys())

def audit_memory_modules(modules_dir: Path | None = None, catalog_path: Path | None = None) -> bool:
    """Verifies module (<80L), specialist persona (<40L), and duplicate rule ID integrity."""
    has_violation = False
    target_modules_dir = modules_dir or MODULES_DIR
    target_catalog = catalog_path or SPECIALIST_CATALOG_FILE

    if not target_modules_dir.exists():
        print(f"[WARN] [RSI Memory Audit] Modules directory not found at {target_modules_dir}")
    else:
        modules = sorted(target_modules_dir.glob("*.md"))
        if not modules:
            print("[INFO] [RSI Memory Audit] No modules found.")
        else:
            print(f"[RSI Memory Audit] {len(modules)} modules detected.")
            seen_rule_ids: dict[str, str] = {}
            for mod in modules:
                try:
                    content = mod.read_text(encoding="utf-8")
                    line_count = len([line for line in content.splitlines() if line.strip()])
                    if line_count > MAX_LINES_PER_MODULE:
                        print(f"  [FAIL] {mod.name}: {line_count}/{MAX_LINES_PER_MODULE} lines (LIMIT EXCEEDED!)")
                        has_violation = True
                    else:
                        print(f"  [OK] {mod.name}: {line_count}/{MAX_LINES_PER_MODULE} lines")
                    for ln in content.splitlines():
                        m_rule = RULE_LINE_RE.match(ln)
                        if m_rule:
                            rid = m_rule.group(1)
                            if rid in seen_rule_ids:
                                print(f"  [FAIL] Duplicate rule ID [{rid}] in {mod.name} (already defined in {seen_rule_ids[rid]})")
                                has_violation = True
                            else:
                                seen_rule_ids[rid] = mod.name
                except Exception as e:
                    print(f"  [WARN] Error reading {mod.name}: {e}")

    if target_catalog.exists():
        core, personas = parse_specialist_personas(target_catalog)
        print(f"[RSI Specialist Audit] {len(personas)} persona block(s) detected in rsi_specialist.md.")
        if core:
            core_lines = len([ln for ln in core.splitlines() if ln.strip()])
            if core_lines > MAX_LINES_PER_PERSONA:
                print(f"  [FAIL] persona:CORE: {core_lines}/{MAX_LINES_PER_PERSONA} lines (LIMIT EXCEEDED!)")
                has_violation = True
            else:
                print(f"  [OK] persona:CORE: {core_lines}/{MAX_LINES_PER_PERSONA} lines")
        for name, body in sorted(personas.items()):
            p_lines = len([ln for ln in body.splitlines() if ln.strip()])
            if p_lines > MAX_LINES_PER_PERSONA:
                print(f"  [FAIL] persona:{name}: {p_lines}/{MAX_LINES_PER_PERSONA} lines (LIMIT EXCEEDED!)")
                has_violation = True
            else:
                print(f"  [OK] persona:{name}: {p_lines}/{MAX_LINES_PER_PERSONA} lines")

    if has_violation:
        print("\n[FAIL] Memory audit failed (line ceiling or duplicate rule ID violation).")
        return False
    else:
        print("\n[OK] All modules and specialist personas comply with strict compactness and unique-ID limits!")
        return True

def load_active_session() -> dict:
    """Loads ephemeral session state from .agents/telemetry/active_session.json."""
    if not ACTIVE_SESSION_FILE.exists():
        return {}
    try:
        data = json.loads(ACTIVE_SESSION_FILE.read_text(encoding="utf-8", errors="ignore"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def save_active_session(session: dict) -> None:
    """Persists ephemeral session state atomically to .agents/telemetry/active_session.json."""
    try:
        ACTIVE_SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = ACTIVE_SESSION_FILE.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
        os.replace(tmp_path, ACTIVE_SESSION_FILE)
    except Exception:
        pass

def resolve_context(files: list[str], modules_dir: Path | None = None) -> str:
    """Determines which modules to load based on input file paths and tracks injected rule IDs."""
    target_modules_dir = modules_dir or MODULES_DIR
    triggers_map = discover_module_triggers(target_modules_dir)
    matched_modules = set()
    normalized_files = []
    for f in files:
        norm = f.replace("\\", "/")
        normalized_files.append(norm)
        f_lower = norm.lower()
        for mod, keywords in triggers_map.items():
            if any(k in f_lower for k in keywords):
                matched_modules.add(mod)

    sorted_modules = sorted(matched_modules)
    injected_rule_ids = []
    output = ["[RSI Dynamic Memory Injection]"]

    for mod in sorted_modules:
        mod_path = target_modules_dir / mod
        if mod_path.exists():
            mod_text = mod_path.read_text(encoding="utf-8").strip()
            output.append(f"\n--- [Module: {mod}] ---")
            output.append(mod_text)
            for rid in RULE_ID_PATTERN.findall(mod_text):
                if rid not in injected_rule_ids:
                    injected_rule_ids.append(rid)

    # Persist injection trace into active_session.json (only when using default workspace dir)
    if modules_dir is None:
        sess = load_active_session()
        if not sess.get("session_started_at"):
            sess["session_started_at"] = datetime.now(timezone.utc).isoformat()
        sess["target_files_queried"] = list(dict.fromkeys(sess.get("target_files_queried", []) + normalized_files))
        sess["injected_modules"] = list(dict.fromkeys(sess.get("injected_modules", []) + sorted_modules))
        sess["injected_rule_ids"] = list(dict.fromkeys(sess.get("injected_rule_ids", []) + injected_rule_ids))
        if "last_diagnosis_matches" not in sess:
            sess["last_diagnosis_matches"] = []
        save_active_session(sess)

    if not matched_modules:
        return "[INFO] No specific sub-playbook required for these files. Refer to fullstack_playbook.md if needed."

    return "\n".join(output)


def _match_project_rules(error_log: str, modules_dir: Path | None = None, limit: int = 2) -> list[tuple[str, str, str]]:
    """Lightweight keyword fallback matching unclassified errors against actual project rules in modules/*.md."""
    target_dir = modules_dir or MODULES_DIR
    if not target_dir.exists() or not error_log.strip():
        return []
    stop_words = {"this", "that", "with", "from", "into", "never", "always", "file", "line", "error", "failed", "check"}
    err_tokens = {w for w in re.findall(r"[a-z0-9_]{4,}", error_log.lower()) if w not in stop_words}
    if not err_tokens:
        return []
    scored: list[tuple[int, str, str, str]] = []
    for mod in sorted(target_dir.glob("*.md")):
        try:
            for ln in mod.read_text(encoding="utf-8", errors="ignore").splitlines():
                m = RULE_LINE_RE.match(ln)
                if not m:
                    continue
                rid, text = m.group(1), m.group(2).strip()
                rule_tokens = {w for w in re.findall(r"[a-z0-9_]{4,}", text.lower()) if w not in stop_words}
                overlap = len(err_tokens & rule_tokens)
                if overlap >= 2:
                    scored.append((overlap, mod.name, rid, text))
        except Exception:
            continue
    scored.sort(key=lambda item: -item[0])
    return [(mod_name, rid, text) for _, mod_name, rid, text in scored[:limit]]


def propose_learning_candidates(modules_dir: Path | None = None, session_file: Path | None = None) -> str:
    """Outputs a compact (<15 lines) Phase 3 briefing: resolved failures + next available rule IDs."""
    sess_path = session_file or ACTIVE_SESSION_FILE
    sess = {}
    if sess_path.exists():
        try:
            raw = json.loads(sess_path.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(raw, dict):
                sess = raw
        except Exception:
            sess = {}

    resolved = list(sess.get("last_resolved_failures") or sess.get("pending_failures") or [])
    next_ids = compute_next_rule_ids(modules_dir)
    lines = ["=== [RSI LEARNING PROPOSAL BRIEF] ==="]
    if resolved:
        lines.append(f"1. Resolved Failures ({len(resolved)}):")
        for item in resolved[:3]:
            step = item.get("step", "unknown")
            excerpt = str(item.get("error_excerpt", ""))[:95]
            lines.append(f"   - [{step}] {excerpt}")
    else:
        lines.append("1. Resolved Failures : [OK] None pending from recent FAIL -> PASS recovery.")

    if next_ids:
        id_summary = ", ".join(f"{k} -> {v}" for k, v in sorted(next_ids.items()))
        lines.append(f"2. Next Rule IDs     : {id_summary}")
    lines.append("3. Next Action       : Load 'python evals/memory_engine.py --persona meta' ONLY if a recurring/structural lesson applies.")
    lines.append("   (Prefer deterministic linters/tests over prose; skip if one-off typo.)")
    return "\n".join(lines)

def diagnose_trajectory() -> bool:
    """Fast-fail reflex: matches recent failure logs against known error signatures in <10ms."""
    if not TRAJECTORY_FILE.exists():
        print("[INFO] [RSI Pattern Diagnosis] No trajectory log found at evals/logs/trajectory_latest.json.")
        return True

    try:
        data = json.loads(TRAJECTORY_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARN] [RSI Pattern Diagnosis] Could not parse trajectory file: {e}")
        return False

    failed_steps = data.get("failed_steps", [])
    sess = load_active_session()
    if not sess.get("session_started_at"):
        sess["session_started_at"] = datetime.now(timezone.utc).isoformat()

    if not failed_steps:
        print("[OK] [RSI Pattern Diagnosis] Last trajectory status is PASS (0 failed steps).")
        sess["last_diagnosis_matches"] = []
        save_active_session(sess)
        return True

    print(f"[RSI Pattern Diagnosis] Analyzing {len(failed_steps)} failed step(s)...")
    matched_any = False
    diag_matches = []
    for step_info in failed_steps:
        step_name = step_info.get("step", "unknown")
        error_log = step_info.get("error_log", "")
        print(f"\n  -> Step Failed: [{step_name}]")
        step_matched = False
        for pattern, rule_label, fix in KNOWN_ERROR_PATTERNS:
            if pattern.search(error_log):
                print(f"     [MATCH] {rule_label}")
                print(f"     [FIX]   {fix}")
                step_matched = True
                matched_any = True
                matched_rids = RULE_ID_PATTERN.findall(rule_label)
                diag_matches.append({
                    "step": step_name,
                    "rule_ids": matched_rids,
                    "label": rule_label,
                    "fix": fix
                })
        if not step_matched:
            project_hints = _match_project_rules(error_log)
            if project_hints:
                for mod_name, rid, rule_text in project_hints:
                    print(f"     [PROJECT-RULE-HINT] [{rid}] ({mod_name}): {rule_text[:110]}")
                    diag_matches.append({
                        "step": step_name,
                        "rule_ids": [rid],
                        "label": f"[{rid}] ({mod_name})",
                        "fix": rule_text[:140]
                    })
                matched_any = True
            else:
                snippet = error_log.strip().splitlines()[0] if error_log.strip() else "Empty error log"
                print(f"     [UNCLASSIFIED] Escalate to System 2 reasoning. Log sample: {snippet[:90]}")
                diag_matches.append({
                    "step": step_name,
                    "rule_ids": [],
                    "label": "UNCLASSIFIED",
                    "fix": "Escalate to System 2 architectural reasoning."
                })

    sess["last_diagnosis_matches"] = diag_matches
    if "target_files_queried" not in sess:
        sess["target_files_queried"] = []
    if "injected_modules" not in sess:
        sess["injected_modules"] = []
    if "injected_rule_ids" not in sess:
        sess["injected_rule_ids"] = []
    save_active_session(sess)

    return matched_any

def main():
    parser = argparse.ArgumentParser(description="RSI Modular Memory Engine")
    parser.add_argument("--audit", action="store_true", help="Verify module (<80L) and specialist persona (<40L) ceilings")
    parser.add_argument("--inject", nargs="*", help="Dynamically inject relevant rule modules for specified files")
    parser.add_argument("--diagnose", action="store_true", help="Instant pattern diagnosis on latest failed trajectory")
    parser.add_argument("--persona", type=str, metavar="NAME", help="Extract CORE + targeted specialist persona from rsi_specialist.md")
    parser.add_argument("--list-personas", action="store_true", help="List available specialist personas and line counts")
    parser.add_argument("--propose", action="store_true", help="Show resolved failures awaiting Phase 3 review and next available rule IDs")
    args = parser.parse_args()

    if args.audit:
        success = audit_memory_modules()
        sys.exit(0 if success else 1)

    if args.propose:
        print(propose_learning_candidates())
        sys.exit(0)

    if args.list_personas:
        list_personas()
        sys.exit(0)

    if args.persona:
        ok, output = resolve_persona(args.persona)
        print(output)
        sys.exit(0 if ok else 1)

    if args.diagnose:
        diagnose_trajectory()
        sys.exit(0)

    if args.inject is not None:
        if len(args.inject) == 0:
            print("Usage: --inject [file1] [file2] ...")
        else:
            print(resolve_context(args.inject))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
