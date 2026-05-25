## 2026-05-25 - Keyboard Accessibility Enhancements
**Learning:** Adding explicit keyboard shortcuts for list management is crucial for accessibility, but users need visual hints to discover them. Tkinter's Treeview requires explicit bindings for basic actions like <Delete> and Select All (<Control-a>/<Command-a>), which are not supported by default.
**Action:** When creating custom keyboard bindings, also update UI element text (e.g., button labels) to hint at the shortcut. Always remember to return 'break' in Tkinter event handlers if default event propagation needs to be stopped.
