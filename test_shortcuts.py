#!/usr/bin/env python3
"""
Verification script for GUI keyboard shortcuts.
Mocks dependencies to allow testing without GUI environment.
"""

import sys
import unittest
from unittest.mock import MagicMock

# Mock dependencies before importing gui_wrapper
sys.modules['tkinterdnd2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['ico_converter'] = MagicMock()

# Mock tkinter and ttk
tk_mock = MagicMock()
ttk_mock = MagicMock()
sys.modules['tkinter'] = tk_mock
sys.modules['tkinter.ttk'] = ttk_mock

try:
    import gui_wrapper
except ImportError as e:
    print(f"Failed to import gui_wrapper: {e}")
    sys.exit(1)

class TestShortcuts(unittest.TestCase):
    def test_methods_exist(self):
        """Test that the shortcut handler methods exist on the class."""
        self.assertTrue(hasattr(gui_wrapper.IcoConverterGUI, '_on_delete_key'),
                        "Method _on_delete_key not found")
        self.assertTrue(hasattr(gui_wrapper.IcoConverterGUI, '_select_all_files'),
                        "Method _select_all_files not found")

    def test_source_code_bindings(self):
        """Test that the bindings and button text update are present in the source code."""
        with open('gui_wrapper.py', 'r') as f:
            content = f.read()

        # Check for bindings
        self.assertIn("self.file_list.bind('<Delete>', self._on_delete_key)", content,
                     "Delete key binding not found")
        self.assertIn("self.file_list.bind('<BackSpace>', self._on_delete_key)", content,
                     "Backspace key binding not found")

        # Check for Control-a / Command-a binding logic
        self.assertIn("self.file_list.bind('<Command-a>', self._select_all_files)", content,
                     "Command-a binding logic not found")
        self.assertIn("self.file_list.bind('<Control-a>', self._select_all_files)", content,
                     "Control-a binding logic not found")

        # Check for button text update
        self.assertIn('text="Remove Selected (Del)"', content,
                     "Remove button text not updated with hint")

if __name__ == '__main__':
    unittest.main()
