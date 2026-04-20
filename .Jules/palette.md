
## 2026-04-20 - Tkinter Treeview Keyboard Accessibility and Visual Hints
**Learning:** Tkinter Treeview widgets require explicit bindings for standard item removal shortcuts like `<Delete>` and `<BackSpace>` (unlike native OS lists). Without these, keyboard-only users cannot remove items. Visual hints (e.g., adding `(Del)` to button text) are highly effective in communicating these shortcuts. Additionally, cross-platform mappings for `<Command-a>` must be wrapped in `try...except tk.TclError` to prevent crashes on non-macOS systems.
**Action:** Always add explicit bindings for expected shortcuts (Delete, Select All) in Tkinter lists, add text hints to associated buttons, and wrap macOS specific bindings (`<Command-*>`) to ensure cross-platform stability.
