## 2026-05-19 - Added visual hints and keyboard bindings for list interactions
**Learning:** Tkinter Treeview widgets don't have default keyboard shortcuts for actions like "Select All" (`<Control-a>`) or "Remove Selected" (`<Delete>`). Not adding these bindings and their visual hints in the UI creates an unexpected accessibility and usability barrier for keyboard-centric users.
**Action:** When implementing custom interactive lists or treeviews, ensure explicit keyboard events are mapped to corresponding common actions and reflected through intuitive UI text or tooltips.
