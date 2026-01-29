import sys
import unittest
from unittest.mock import MagicMock
import types

# Mock tkinter and dependencies
mock_tk = MagicMock()
mock_tk.Tk = MagicMock
mock_tk.IntVar = MagicMock
mock_tk.StringVar = MagicMock
mock_tk.DoubleVar = MagicMock
mock_tk.Frame = MagicMock
mock_tk.Label = MagicMock
mock_tk.Button = MagicMock
mock_tk.Checkbutton = MagicMock
mock_tk.LabelFrame = MagicMock
mock_tk.Scrollbar = MagicMock
mock_tk.Event = MagicMock
mock_tk.W = 'w'
mock_tk.E = 'e'
mock_tk.N = 'n'
mock_tk.S = 's'
mock_tk.LEFT = 'left'
mock_tk.VERTICAL = 'vertical'
mock_tk.SUNKEN = 'sunken'
mock_tk.SOLID = 'solid'
mock_tk.GROOVE = 'groove'
mock_tk.END = 'end'
mock_tk.NORMAL = 'normal'
mock_tk.DISABLED = 'disabled'

mock_ttk = MagicMock()
mock_ttk.Frame = MagicMock
mock_ttk.Label = MagicMock
mock_ttk.LabelFrame = MagicMock
mock_ttk.Button = MagicMock
mock_ttk.Checkbutton = MagicMock
mock_ttk.Treeview = MagicMock
mock_ttk.Scrollbar = MagicMock
mock_ttk.Progressbar = MagicMock

mock_dnd = MagicMock()
mock_dnd.TkinterDnD = MagicMock
mock_dnd.DND_FILES = 'DND_FILES'

# Apply mocks
sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = mock_ttk
sys.modules['tkinterdnd2'] = mock_dnd

# Now import the module under test
import gui_wrapper

class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.root = mock_tk.Tk()
        self.app = gui_wrapper.IcoConverterGUI(self.root)

    def test_select_all_files(self):
        # Mock treeview children
        self.app.file_list.get_children.return_value = ['item1', 'item2']

        # Call the method
        result = self.app._select_all_files()

        # Verify it selects all children
        self.app.file_list.selection_set.assert_called_with(['item1', 'item2'])
        # Verify it returns "break"
        self.assertEqual(result, "break")

    def test_remove_selected_files_signature(self):
        # Verify it accepts an event argument
        try:
            self.app._remove_selected_files(event="dummy_event")
        except TypeError:
            self.fail("_remove_selected_files should accept an event argument")

    def test_shortcuts_registered(self):
        # Check that bind was called on file_list for Delete and BackSpace

        # file_list.bind calls
        bind_calls = self.app.file_list.bind.call_args_list
        bound_keys = [args[0] for args, kwargs in bind_calls]

        self.assertIn('<Delete>', bound_keys)
        self.assertIn('<BackSpace>', bound_keys)

        # root.bind calls
        root_bind_calls = self.root.bind.call_args_list
        root_bound_keys = [args[0] for args, kwargs in root_bind_calls]

        self.assertIn('<Control-a>', root_bound_keys)

if __name__ == '__main__':
    unittest.main()
