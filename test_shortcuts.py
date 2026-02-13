import sys
from unittest.mock import MagicMock
import tkinter as tk

# Mock tkinterdnd2 BEFORE importing gui_wrapper
mock_tkdnd = MagicMock()
sys.modules['tkinterdnd2'] = mock_tkdnd

# Mock PIL (required by ico_converter which is imported by gui_wrapper)
mock_pillow = MagicMock()
sys.modules['PIL'] = mock_pillow

# Mock Image module specifically as it's often imported directly
sys.modules['PIL.Image'] = MagicMock()

# Now we can safely import gui_wrapper
import gui_wrapper

def test_shortcuts():
    print("Testing GUI Shortcuts Implementation...")

    failed = False

    # 1. Check if _select_all_files method exists
    if hasattr(gui_wrapper.IcoConverterGUI, '_select_all_files'):
        print("✓ _select_all_files method exists")
    else:
        print("✗ _select_all_files method MISSING")
        failed = True

    # 2. Check source code for bindings (static analysis)
    with open('gui_wrapper.py', 'r') as f:
        content = f.read()

    # Check for Select All binding
    if "bind('<Control-a>'" in content or 'bind("<Control-a>"' in content:
        print("✓ Control-a binding found in source")
    else:
        print("✗ Control-a binding MISSING in source")
        failed = True

    # Check for Delete binding
    if "bind('<Delete>'" in content or 'bind("<Delete>"' in content:
        print("✓ Delete binding found in source")
    else:
        print("✗ Delete binding MISSING in source")
        failed = True

    # Check for BackSpace binding
    if "bind('<BackSpace>'" in content or 'bind("<BackSpace>"' in content:
        print("✓ BackSpace binding found in source")
    else:
        print("✗ BackSpace binding MISSING in source")
        failed = True

    # Check for button text update
    if 'text="Remove Selected (Del)"' in content or "text='Remove Selected (Del)'" in content:
        print("✓ Button text updated with shortcut hint")
    else:
        print("✗ Button text missing shortcut hint")
        failed = True

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    test_shortcuts()
