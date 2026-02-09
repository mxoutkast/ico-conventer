## 2024-05-22 - Keyboard Accessibility in Tkinter Treeview
**Learning:** Standard keyboard shortcuts (Delete, Ctrl+A) are not automatically bound to `ttk.Treeview` widgets in Tkinter. Users expect these shortcuts to work for list management.
**Action:** Always explicitly bind `<Delete>`, `<BackSpace>`, and `<Control-a>` (plus `<Command-a>` for macOS) when implementing list views in Tkinter applications.
