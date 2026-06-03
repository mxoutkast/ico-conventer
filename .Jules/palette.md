## 2026-06-03 - Tkinter Treeview Keyboard Bindings
**Learning:** Tkinter Treeview widgets require explicit mappings for common keyboard behaviors like item removal (<Delete>, <BackSpace>) and select all (<Control-a>, <Command-a>) to meet user accessibility and interaction expectations.
**Action:** When implementing custom keyboard event bindings in Tkinter, wrap macOS specific keys like <Command-a> in `try...except tk.TclError` to prevent crashes on non-macOS systems, and make sure to return `'break'` to prevent default event propagation.
