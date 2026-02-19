## 2024-05-23 - Keyboard Shortcuts in Tkinter
**Learning:** Platform-specific bindings (like `<Command-a>` on macOS) can crash the application on other platforms if not wrapped in `try...except tk.TclError`.
**Action:** Always wrap platform-specific bindings in `try...except` blocks to ensure cross-platform compatibility.

## 2024-05-23 - Testing GUI in Headless Environment
**Learning:** GUI tests that import `tkinter` or other GUI libraries often fail in headless environments.
**Action:** Mock GUI dependencies (like `tkinterdnd2`, `PIL`) in test files to allow structural testing without a display server.
