## 2025-05-23 - Headless Tkinter Testing
**Learning:** Testing Tkinter GUI components in a headless environment requires extensive mocking of dependencies like `tkinterdnd2` and `Pillow`. `sys.modules` mocking is necessary before importing the module under test.
**Action:** When creating tests for GUI components in this repo, always mock `tkinterdnd2`, `PIL`, and `PIL.Image` in `sys.modules` at the start of the test script.

## 2025-05-23 - Cross-Platform Tkinter Bindings
**Learning:** Binding macOS-specific keys like `<Command-a>` in Tkinter raises `TclError` on non-macOS systems, crashing the application.
**Action:** Always wrap platform-specific bindings in a `try...except tk.TclError` block to ensure cross-platform compatibility.
