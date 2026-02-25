import sys
from unittest.mock import MagicMock

# Mock modules before importing gui_wrapper
mock_tk = MagicMock()
mock_tk.Tk = MagicMock()
mock_tk.TclError = Exception
# Need to mock verify so instance checks work?
# No, MagicMock handles most things.

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = mock_tk.ttk # ttk is often submodule
sys.modules['tkinter.filedialog'] = MagicMock()

mock_dnd = MagicMock()
sys.modules['tkinterdnd2'] = mock_dnd

# Mock PIL
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Now import
try:
    import gui_wrapper
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

def test_shortcuts():
    # Setup mock root
    root = mock_tk.Tk()

    # Instantiate GUI
    # The __init__ calls _setup_ui which creates ttk.Treeview
    try:
        app = gui_wrapper.IcoConverterGUI(root)
    except Exception as e:
        print(f"Error initializing GUI: {e}")
        return

    # file_list should be a mock object from ttk.Treeview()
    # Let's inspect its bind calls

    if not hasattr(app, 'file_list'):
        print("FAILURE: app has no file_list")
        return

    bind_calls = app.file_list.bind.call_args_list

    # We look for calls like bind('<Delete>', ...) or bind('<BackSpace>', ...)
    # call_args_list is a list of calls. Each call is (args, kwargs)
    # args[0] is the event sequence

    bound_keys = []
    for call in bind_calls:
        if call.args:
            bound_keys.append(call.args[0])

    print(f"Bound keys on file_list: {bound_keys}")

    has_delete = '<Delete>' in bound_keys
    has_backspace = '<BackSpace>' in bound_keys

    # Also check button text
    # We need to find the remove button. It's created in _setup_ui
    # self.remove_button isn't stored as attribute in __init__, but we can traverse children if real tk...
    # But since everything is mocked, we can't easily traverse unless we mock that structure too.
    # However, we can check if ttk.Button was initialized with specific text.

    button_calls = mock_tk.ttk.Button.call_args_list
    remove_button_text_updated = False
    for call in button_calls:
        # Check kwargs for text
        if 'text' in call.kwargs:
            if "Remove Selected (Del)" in call.kwargs['text']:
                remove_button_text_updated = True
                break

    if has_delete and has_backspace:
        print("SUCCESS: Shortcuts bound")
    else:
        print("FAILURE: Shortcuts not bound")
        sys.exit(1)

    if remove_button_text_updated:
        print("SUCCESS: Button text updated")
    else:
        print("FAILURE: Button text not updated")
        sys.exit(1)

if __name__ == "__main__":
    test_shortcuts()
