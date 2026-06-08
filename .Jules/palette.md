## 2024-06-08 - Keyboard Shortcuts for Tkinter Treeview
**Learning:** Tkinter Treeview widgets lack standard OS-level list keyboard behaviors by default (like `Delete` to remove items or `Ctrl-A`/`Cmd-A` to select all). Relying entirely on point-and-click creates accessibility friction for keyboard users.
**Action:** When implementing list interfaces in Tkinter, explicitly bind expected list shortcuts (like `<Delete>`, `<BackSpace>`, `<Control-a>`) and add visual hints to the corresponding UI buttons (e.g., "Remove Selected (Del)") to improve discoverability and accessibility.
