## 2026-02-21 - Tkinter Treeview Accessibility
**Learning:** Tkinter Treeview widgets do not have built-in keyboard navigation for selection and deletion by default, creating a significant accessibility gap.
**Action:** Always manually bind `<Delete>`, `<BackSpace>`, and `<Control-a>` to list-based widgets in Tkinter applications to meet user expectations.
