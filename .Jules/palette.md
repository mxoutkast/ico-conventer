## 2026-06-09 - Add Keyboard Shortcut Hints and Bindings
**Learning:** Tkinter Treeview widgets don't have default keyboard bindings for common list operations like Delete to remove or Ctrl+A to select all. Users expect these to "just work".
**Action:** Always explicitly bind <Delete>, <BackSpace>, <Control-a>, and <Command-a> to list components and add visual hints (like '(Del)') to corresponding UI buttons.
