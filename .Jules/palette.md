## 2026-02-24 - Tkinter Treeview Keyboard Accessibility
**Learning:** Tkinter Treeview widgets do not implement default keyboard shortcuts for item removal (Delete/Backspace), which users expect for list management.
**Action:** Always manually bind `<Delete>` and `<BackSpace>` to removal handlers when implementing list or tree components in Tkinter.
