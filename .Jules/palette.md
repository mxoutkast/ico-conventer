## 2026-03-03 - Tkinter Treeview Keyboard Shortcuts
**Learning:** Tkinter `Treeview` widgets don't come with default shortcuts for basic file operations like deletion (`Delete`/`BackSpace`) or select-all (`Control-a`/`Command-a`). Furthermore, macOS shortcuts like `<Command-a>` will crash non-macOS platforms with a `tk.TclError` if not caught.
**Action:** When using `ttk.Treeview` for lists, explicitly bind standard keyboard shortcuts for UX, wrap macOS bindings in a `try...except tk.TclError`, and add visual hints in the UI (e.g., changing button text to "Remove Selected (Del)").
