# Palette Journal
## 2025-04-08 - Added keyboard shortcuts for file removal and selection in Treeview
**Learning:** Tkinter Treeview widgets require explicit manual event bindings for common UX expectations like `Delete` for removal or `Ctrl+A` for selection, as these are not provided by default. Additionally, cross-platform bindings (like macOS `Command-A`) need to be wrapped in `try...except tk.TclError` to prevent crashes on non-macOS environments. Visually hinting the keyboard shortcuts in button labels helps discoverability.
**Action:** When working with Tkinter collections/lists, proactively add explicit `<Delete>` and `<BackSpace>` bindings and indicate these shortcuts in related action buttons. Always use `try...except` for OS-specific bindings.
