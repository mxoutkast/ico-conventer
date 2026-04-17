## 2026-04-17 - Keyboard Shortcuts for File List
**Learning:** Adding explicit keyboard shortcuts like `<Delete>` and `<Control-a>` to Tkinter `Treeview` widgets significantly improves usability and accessibility, as these behaviors are not provided by default. macOS bindings (`<Command-a>`) require error handling to prevent cross-platform issues. Visual hints in button text help users discover these shortcuts.
**Action:** Always include keyboard event bindings and visual UI hints (e.g., button text labels) for bulk selection and deletion operations in list-based UI components.
