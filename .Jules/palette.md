## 2024-03-14 - Keyboard Shortcuts in Tkinter Lists
**Learning:** Tkinter's Treeview doesn't provide default keyboard shortcuts for basic list operations like Select All or Delete. Users expect these to just work. Without explicit bindings and UI hints (like '(Del)' on buttons), keyboard-centric users lose a standard accessibility interaction.
**Action:** Always explicitly bind <Control-a>/<Command-a> for selection and <Delete>/<BackSpace> for removal in Tkinter Treeviews, handle cross-platform TclErrors gracefully, and add visual shortcut hints to related buttons.
