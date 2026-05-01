## 2025-05-15 - Explicit Keyboard Bindings for Treeview

**Learning:** Tkinter Treeview widgets do not come with default keyboard bindings for actions like deleting items or selecting all. For keyboard accessibility, explicit bindings are required (e.g., `<Delete>`, `<BackSpace>` for deletion, and `<Control-a>`, `<Command-a>` for "select all" to support macOS as well).

**Action:** Whenever using a Treeview widget or similar lists, remember to bind appropriate keys to support standard actions, making the interface more accessible for keyboard users. Provide visual hints on the buttons (e.g. "(Del)").
