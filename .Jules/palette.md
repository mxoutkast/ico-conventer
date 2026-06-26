## 2024-05-18 - Tkinter Keyboard Accessibility
**Learning:** Tkinter lists (`ttk.Treeview`) lack standard keyboard accessibility out-of-the-box (e.g., `<Delete>` for removal, `<Control-a>` for select all) and require explicit shortcut bindings to function intuitively for keyboard users.
**Action:** Always bind expected keyboard shortcuts explicitly and update UI labels (e.g., "Remove Selected (Del)") to provide visual hints for accessibility.
