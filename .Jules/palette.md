## 2024-05-22 - Headless GUI Verification & Shortcuts
**Learning:** This codebase verifies GUI components using static analysis and inspection rather than instantiation, due to headless environment constraints. Also, `command=` handlers often need `event=None` to support dual use (button click + key binding).
**Action:** When adding GUI features, update static checks in tests and ensure handlers accept `event` arguments. Bind platform-specific keys (like Cmd-A) inside try-except blocks.
