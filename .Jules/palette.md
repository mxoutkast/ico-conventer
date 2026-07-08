
## 2024-06-25 - Custom Tkinter Bindings Visual Hinting
**Learning:** Tkinter's Treeview component lacks default keyboard shortcuts for actions like removing items (`<Delete>`) or selecting all (`<Control-a>`), requiring explicit event bindings. Furthermore, since these are not system defaults for this widget type, users have no way to discover them without visual hints in the UI (e.g., updating button text from "Remove Selected" to "Remove Selected (Del)").
**Action:** When adding custom keyboard shortcuts to non-standard widgets (like Treeview) in Tkinter, always update the relevant UI labels or tooltips to visually hint the shortcut to the user for discoverability.
