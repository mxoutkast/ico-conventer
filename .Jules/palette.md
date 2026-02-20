## 2024-05-23 - Keyboard Shortcut Discovery
**Learning:** Users often miss keyboard shortcuts in desktop GUIs. Adding explicit hints to button labels (e.g., "Remove Selected (Del)") is a low-friction way to improve discoverability without dedicated help menus.
**Action:** When adding keyboard shortcuts to list controls, always update the corresponding action button text to include the shortcut key in parentheses.

## 2024-05-23 - Cross-Platform Tkinter Bindings
**Learning:** Tkinter on non-macOS systems throws `TclError` when binding `<Command-...>` keys, crashing the application if not handled.
**Action:** Always wrap macOS-specific bindings in `try...except tk.TclError` blocks to ensure cross-platform compatibility.
