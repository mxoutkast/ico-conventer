## 2024-05-30 - Added Keyboard Shortcuts for Tkinter Treeview

**Learning:** In Tkinter, the `ttk.Treeview` widget does not natively bind default list interaction keys such as `<Delete>` or `<BackSpace>` to remove items, nor `<Control-a>` or `<Command-a>` for 'Select All'. It only handles basic navigation and selection with arrow keys and spacebar.

**Action:** Whenever using `ttk.Treeview` in future applications where list items can be selected and manipulated, explicitly bind standard keyboard shortcuts like `<Delete>`, `<BackSpace>`, and 'Select All' (`<Control-a>`, `<Command-a>`). Also ensure that event handlers for these custom bindings return `'break'` to prevent the event from propagating and triggering default system/Tkinter behaviors (e.g. system beeps). Lastly, macOS bindings like `<Command-a>` should be wrapped in `try...except tk.TclError` as they may raise an error on non-macOS systems.
