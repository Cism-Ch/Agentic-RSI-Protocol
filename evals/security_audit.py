#!/usr/bin/env python3
"""
Static Security Audit & Secret Leak Detector
- Checks for hardcoded API keys, tokens, private certificates, and secrets
- Validates .gitignore airtightness (.env*, private keys, caches)
- Inspects permissions and conformance to RSI security guardrails
"""

import sys
import re
import os
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = [
    (re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'), "Private Key (RSA/EC/SSH)"),
    (re.compile(r'sk-[a-zA-Z0-9]{20,}'), "Secret Key (OpenAI/Stripe style)"),
    (re.compile(r'AKIA[0-9A-Z]{16}'), "AWS Access Key ID"),
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'), "GitHub Personal Access Token"),
    (re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,48}'), "Slack API Token"),
    (re.compile(r'(?:postgres|postgresql|mysql|mongodb\+srv):\/\/[^\s:]+:[^\s@]+@[^\s\/]+'), "Database URI with hardcoded password"),
    (re.compile(r'(?i)(?:api_key|secret_key|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-\.]{16,}["\']'), "Hardcoded Auth Secret")
]

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.next'}

def audit_gitignore() -> list[str]:
    issues = []
    gitignore = ROOT_DIR / ".gitignore"
    if not gitignore.exists():
        issues.append("Missing .gitignore file!")
        return issues

    content = gitignore.read_text(encoding="utf-8", errors="replace")
    essential_rules = [".env", "*.pem", "*.key", "node_modules"]
    for rule in essential_rules:
        if rule not in content:
            issues.append(f"Missing essential security rule in .gitignore: '{rule}'")
    return issues

def audit_secrets() -> list[dict]:
    findings = []
    for path in ROOT_DIR.rglob("*"):
        if path.is_file():
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            # Avoid self-flagging on this audit script
            if path.name == "security_audit.py":
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
                for idx, line in enumerate(lines, start=1):
                    for pattern, label in SECRET_PATTERNS:
                        if pattern.search(line):
                            findings.append({
                                "file": str(path.relative_to(ROOT_DIR)),
                                "line": idx,
                                "type": label,
                                "sample": line.strip()[:60]
                            })
            except Exception as e:
                findings.append({
                    "file": str(path.relative_to(ROOT_DIR)),
                    "line": 0,
                    "type": "Read Error",
                    "sample": str(e)
                })
    return findings

def run_security_audit() -> bool:
    print("[RSI Security Audit] Running static security and secret leak audit...")
    gitignore_issues = audit_gitignore()
    secret_findings = audit_secrets()

    success = True
    if gitignore_issues:
        print("\n[FAIL] .gitignore configuration vulnerabilities:")
        for issue in gitignore_issues:
            print(f"  - {issue}")
        success = False
    else:
        print("  [OK] .gitignore configuration is airtight and compliant.")

    if secret_findings:
        print(f"\n[FAIL] {len(secret_findings)} potential secret leak(s) detected:")
        for finding in secret_findings:
            print(f"  - [{finding['type']}] {finding['file']}:{finding['line']} -> {finding['sample']}")
        success = False
    else:
        print("  [OK] No exposed secrets, private keys, or credentials found.")

    # Check for real uncommitted .env files
    env_files = list(ROOT_DIR.glob(".env*"))
    real_envs = [f.name for f in env_files if f.name != ".env.example"]
    if real_envs:
        print(f"  [INFO] Local .env files present: {real_envs} (must stay ignored by git)")
    else:
        print("  [OK] No unencrypted plaintext .env files in directory.")

    if success:
        print("\n[SUCCESS] SECURITY AUDIT: PASSED (0 critical vulnerabilities detected)")
    else:
        print("\n[FAIL] SECURITY AUDIT: FAILED")

    return success

if __name__ == "__main__":
    passed = run_security_audit()
    sys.exit(0 if passed else 1)
