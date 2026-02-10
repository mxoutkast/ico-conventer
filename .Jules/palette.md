## 2025-05-23 - Tkinter Keyboard Accessibility
**Learning:** Standard Tkinter widgets like Treeview lack default keyboard shortcuts for common actions (Delete, Select All).
**Action:** Always manually bind `<Delete>`, `<BackSpace>`, and `<Control-a>` (plus `<Command-a>` for macOS) when implementing list-based interfaces in Tkinter.
