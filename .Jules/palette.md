# Palette's Journal - Critical Learnings

## 2024-05-23 - Keyboard Accessibility in Tkinter Treeview
**Learning:** Users expect standard keyboard shortcuts like Delete and Ctrl+A/Cmd+A to work in file lists, but Tkinter Treeview doesn't provide them by default.
**Action:** Always bind `<Delete>`, `<BackSpace>`, `<Control-a>`, and `<Command-a>` (wrapped in try/except for non-macOS) to list interactions. Add visual hints to buttons (e.g., "Remove Selected (Del)") to improve discoverability.

## 2024-05-23 - Headless UI Testing
**Learning:** Testing Tkinter GUI logic in a headless CI environment requires mocking `sys.modules` for `tkinter`, `tkinter.ttk`, and `PIL` *before* importing the application module.
**Action:** Use `unittest.mock.MagicMock` to stub out GUI dependencies in test scripts to verify logic without a display server.
