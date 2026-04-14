## 2024-04-14 - Keyboard Accessibility for File List
**Learning:** Tkinter's Treeview component lacks native support for standard keyboard list interactions (like `<Delete>` for removal and `<Ctrl-a>` for bulk selection), making the file list inaccessible to keyboard users by default.
**Action:** Always implement and explicitly bind `<Delete>`, `<BackSpace>`, and platform-specific `<Control-a>`/`<Command-a>` shortcuts to list components, and surface these bindings visually in the UI text (e.g., "Remove Selected (Del)").

## 2026-04-14 - File List Keyboard Accessibility
**Learning:** As noted, Tkinter's Treeview component requires custom keyboard bindings to behave like a standard accessible list. Making sure it has full keyboard functionality (Delete, Select All) paired with clear visual hints on UI buttons like "Remove Selected (Del)" is crucial for accessibility.
**Action:** Ensure bindings for `<Delete>`, `<BackSpace>`, `<Control-a>` and `<Command-a>` are applied to the Treeview, and update associated action buttons to display the shortcut visually.
