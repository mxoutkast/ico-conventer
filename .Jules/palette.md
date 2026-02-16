## 2025-05-18 - Tkinter Treeview Keyboard Shortcuts
**Learning:** Tkinter's `ttk.Treeview` does not have default bindings for common list operations like `<Delete>`, `<BackSpace>`, or `<Control-a>` (Select All). These must be implemented manually.
**Action:** When implementing lists in Tkinter, always add explicit bindings for these keys to ensure standard keyboard accessibility. Remember to handle macOS-specific bindings (e.g., `<Command-a>`) separately inside a `try...except` block to avoid crashes on other platforms.
