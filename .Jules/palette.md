## 2024-05-22 - Keyboard Accessibility Pattern
**Learning:** Adding standard keyboard shortcuts (Delete, Backspace, Ctrl+A) to the file list significantly improves accessibility for keyboard users. Binding these keys directly to the Treeview widget ensures they work when the list has focus.
**Action:** Always implement `_select_all` and `_remove_selected` handlers with optional `event=None` arguments to support both button clicks and key bindings, and update button text to include shortcut hints (e.g., "Remove (Del)").
