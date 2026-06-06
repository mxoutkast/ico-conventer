## 2024-05-18 - Tkinter Treeview Accessibility and Keyboard Bindings
**Learning:** Tkinter Treeview widgets do not natively support list management keyboard shortcuts (like <Delete> for removing items or <Control-a> for selecting all). Users expect these to work intuitively.
**Action:** Always explicitly bind these keyboard events to the Treeview and add visual text hints to buttons (e.g., 'Remove Selected (Del)') to communicate these shortcuts to the user.
