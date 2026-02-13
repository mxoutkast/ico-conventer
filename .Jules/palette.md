## 2024-05-23 - Tkinter Accessibility Patterns
**Learning:** Tkinter's `ttk.Treeview` lacks built-in keyboard navigation for common actions like deletion or selection.
**Action:** Always manually bind `<Delete>`, `<BackSpace>`, and `<Control-a>` for list components, and explicitly hint these shortcuts in associated button text (e.g., "Remove (Del)").
