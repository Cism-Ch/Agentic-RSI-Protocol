# Contributing to the Agentic RSI Protocol

Thank you for your interest in contributing to the **Agentic RSI Protocol**!

This framework is built upon strict engineering standards and deterministic guardrails. To keep the project reliable and bug-free across all platforms, please adhere to these guidelines.

---

## Code of Conduct & Core Standards

1. **Zero Non-ASCII Characters in Core Scripts:**
   - All evaluation and automation scripts in `evals/` MUST use pure ASCII output.
   - Do NOT use emojis, smart quotes (`"`, `'`), em-dashes (`—`), or Unicode arrows (`➔`).
   - Use standard tags: `[OK]`, `[FAIL]`, `[WARN]`, `[INFO]`, `->`.
   - Reason: Preserves 100% compatibility across Windows CP1252, ISO-8859-1, and CI environments without `UnicodeEncodeError`.

2. **Strict Compactness Ceiling:**
   - Any rule file in `.agents/rules/modules/` MUST remain strictly under **80 lines**.
   - `docs/TASKS.md` MUST remain strictly under **250 lines** (archive older sprints to `docs/archive/tasks/`).

3. **Deterministic Verification:**
   - Before opening a pull request, verify that all checks pass:
     ```bash
     python evals/run_fullstack_eval.py
     python evals/rsi_orchestrator.py --guardrail
     ```

---

## Development Workflow

1. **Fork and Clone the Repository.**
2. **Create a Feature Branch:**
   ```bash
   git checkout -b feat/my-improvement
   ```
3. **Commit Messages:**
   Follow Conventional Commits:
   - `feat(...)`: New feature or capability
   - `fix(...)`: Bug fix
   - `docs(...)`: Documentation updates
   - `refactor(...)`: Code adjustments without feature changes
   - `test(...)`: Adding or updating evaluations

4. **Verify Encoding & Tests:**
   ```bash
   python -c "
   from pathlib import Path
   for p in Path('evals').glob('*.py'):
       content = p.read_text(encoding='utf-8')
       bad = [l for l in content.splitlines() if any(ord(c) > 127 for c in l)]
       if bad:
           raise ValueError(f'Non-ascii in {p.name}')
   print('All scripts are pure ASCII!')
   "
   ```

5. **Submit a Pull Request:**
   Describe your changes clearly and attach the evaluation output from `run_fullstack_eval.py`.
