## 2024-03-20 - [Keyboard Accessibility Insights]
**Learning:** Found that `<Delete>` and `<BackSpace>` shortcuts for lists require explicit bindings and visual hints in text to be discoverable. Cross-platform support for macOS requires catching tk.TclError on specific key bindings like `<Command-a>`.
**Action:** Always test keyboard interactions on lists/tables, explicitly bind delete actions, and add visual hints (e.g., "(Del)") to corresponding buttons.
