## 2024-05-21 - Keyboard Accessibility for List Views
**Learning:** Users instinctively expect standard keyboard shortcuts (Delete, Ctrl+A) in file lists, but Tkinter's Treeview does not provide these by default, making the interface feel "dead" to keyboard users.
**Action:** Always manually bind `<Delete>`, `<BackSpace>`, and `<Control-a>` events when implementing list or tree components to match OS-native behavior.
