# Module: Frontend & User Interfaces

> Anti-Bloat Rule: This module must NEVER exceed **80 lines**.

- [R-UI-01] Strictly adopt a Mobile-First approach: write base styles for mobile, then expand with responsive breakpoints.
- [R-UI-02] Systematically handle all 4 visual states: loading (skeleton), error (feedback), empty (placeholder), and data.
- [R-UI-03] Ensure minimal touch targets of 44x44px for all interactive elements.
- [R-UI-04] Leverage accessible component primitives (e.g., Radix UI / shadcn) rather than rolling custom dialogs or menus manually.
- [R-UI-05] Inherit the project's canonical page layout (`Header`, `Footer`, navigation, container) on every public page; never build isolated pages missing core chrome unless explicitly auth/embed.
- [R-UI-06] Strictly use semantic design-system tokens (CSS variables / Tailwind theme) and existing UI primitives; never hardcode arbitrary hex colors (`bg-[#...]`) or ad-hoc inline styles.
- [R-UI-07] Zero orphan components: when replacing or refactoring a component, verify incoming imports (`stack_inspector.py --impact`) and delete obsolete unused files.
