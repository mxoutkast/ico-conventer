## 2024-05-24 - File List Keyboard Shortcuts
**Learning:** Tkinter Treeview widgets do not have default keyboard bindings for standard file list operations like "Delete" or "Select All". These must be explicitly bound.
**Action:** When implementing list-based UI components in Tkinter, always add explicit bindings for `<Delete>`, `<BackSpace>`, and `<Control/Command-a>` to match user expectations from native file explorers.
