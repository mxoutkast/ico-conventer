#!/usr/bin/env python3
"""
Test script to verify keyboard shortcuts in the GUI.
"""

import sys
import unittest.mock as mock

# Mock external dependencies
sys.modules['tkinterdnd2'] = mock.MagicMock()
sys.modules['PIL'] = mock.MagicMock()
sys.modules['PIL.Image'] = mock.MagicMock()

# Now import the module to test
try:
    import gui_wrapper
except ImportError:
    # If it fails, we can't test it
    pass

def test_shortcuts():
    """Test keyboard shortcuts implementation."""
    print("Testing Keyboard Shortcuts...")
    print("-" * 50)

    try:
        # Read the source code directly to check for bindings without needing to instantiate the GUI
        with open('gui_wrapper.py', 'r') as f:
            content = f.read()

        # Check for Delete/Backspace binding
        print("Test 1: Check for Delete/Backspace bindings")
        has_delete_binding = "self.file_list.bind('<Delete>'," in content or "self.file_list.bind('<Delete>'," in content or 'self.file_list.bind("<Delete>",' in content
        has_backspace_binding = "self.file_list.bind('<BackSpace>'," in content or "self.file_list.bind('<BackSpace>'," in content or 'self.file_list.bind("<BackSpace>",' in content

        if has_delete_binding:
            print("  ✓ Delete key binding found")
        else:
            print("  ✗ Delete key binding NOT found")

        if has_backspace_binding:
            print("  ✓ Backspace key binding found")
        else:
            print("  ✗ Backspace key binding NOT found")

        # Check for Select All binding
        print("\nTest 2: Check for Select All binding")
        # Check for both Windows/Linux (Control-a) and Mac (Command-a) or a cross-platform approach
        has_ctrl_a_binding = "self.file_list.bind('<Control-a>'," in content or 'self.file_list.bind("<Control-a>",' in content

        if has_ctrl_a_binding:
            print("  ✓ Control-a binding found")
        else:
            print("  ✗ Control-a binding NOT found")

        # Check for Select All method
        print("\nTest 3: Check for _select_all_files method")
        has_select_all_method = "def _select_all_files(self" in content

        if has_select_all_method:
            print("  ✓ _select_all_files method found")
        else:
            print("  ✗ _select_all_files method NOT found")

        # Check for button text update
        print("\nTest 4: Check for button text hint")
        has_button_hint = 'text="Remove Selected (Del)"' in content

        if has_button_hint:
            print("  ✓ Button text hint found")
        else:
            print("  ✗ Button text hint NOT found")

        # Overall result
        if (has_delete_binding and has_backspace_binding and
            has_ctrl_a_binding and has_select_all_method and has_button_hint):
            print("\n" + "=" * 50)
            print("All shortcut tests PASSED! ✓")
            print("=" * 50)
            return 0
        else:
            print("\n" + "=" * 50)
            print("Some shortcut tests FAILED. ✗")
            print("=" * 50)
            return 1

    except Exception as e:
        print(f"\n✗ Test ERROR: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(test_shortcuts())
