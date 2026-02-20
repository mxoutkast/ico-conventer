
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies that might be missing or require GUI
sys.modules['tkinterdnd2'] = MagicMock()
sys.modules['PIL'] = MagicMock()

# Mock tkinter before importing gui_wrapper
mock_tk = MagicMock()
sys.modules['tkinter'] = mock_tk
mock_ttk = MagicMock()
sys.modules['tkinter.ttk'] = mock_ttk
# Ensure that if gui_wrapper does `from tkinter import ttk`, it gets our mock_ttk
mock_tk.ttk = mock_ttk

sys.modules['tkinter.filedialog'] = MagicMock()

import gui_wrapper

class TestKeyboardShortcuts(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        self.app = gui_wrapper.IcoConverterGUI(self.root)

    def test_remove_selected_binding(self):
        # Check if <Delete> and <BackSpace> are bound to _remove_selected_files
        # The file_list is a ttk.Treeview, which is mocked
        file_list = self.app.file_list

        # We need to find the calls to bind
        # bind is called on the widget
        # The app calls bind on self.file_list

        # Let's see all calls to bind
        bind_calls = file_list.bind.call_args_list

        bindings = {}
        for call in bind_calls:
            event, handler = call[0]
            bindings[event] = handler

        print(f"Found bindings: {bindings.keys()}")

        self.assertIn('<Delete>', bindings, "Delete key not bound")
        self.assertIn('<BackSpace>', bindings, "Backspace key not bound")
        self.assertEqual(bindings['<Delete>'], self.app._remove_selected_files)

    def test_select_all_binding(self):
        file_list = self.app.file_list
        bind_calls = file_list.bind.call_args_list
        bindings = {call[0][0]: call[0][1] for call in bind_calls}

        self.assertIn('<Control-a>', bindings, "Ctrl+A not bound")
        # Check for Command-a on Mac if applicable, but verifying Control-a is good for now

        # Also check if _select_all_files method exists
        self.assertTrue(hasattr(self.app, '_select_all_files'), "_select_all_files method missing")

    def test_remove_button_text(self):
        # We need to find the remove button and check its text
        # Since we mocked ttk.Button, we need to find which one is the remove button
        # The remove button calls _remove_selected_files

        # We can iterate over all mocked Button instantiations
        found = False
        print("Debugging Button calls:")
        for call in sys.modules['tkinter.ttk'].Button.call_args_list:
            kwargs = call[1]
            print(f"Button call kwargs: {kwargs}")
            if 'command' in kwargs and kwargs['command'] == self.app._remove_selected_files:
                text = kwargs.get('text', '')
                if '(Del)' in text:
                    found = True
                    break

        self.assertTrue(found, "Remove button text does not contain shortcut hint '(Del)'")

if __name__ == '__main__':
    unittest.main()
