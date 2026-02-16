#!/usr/bin/env python3
"""
Test script to verify keyboard shortcuts implementation.
"""

import sys
import types
from unittest.mock import MagicMock

# Mock tkinterdnd2 to allow import of gui_wrapper
mock_dnd = types.ModuleType('tkinterdnd2')
mock_dnd.TkinterDnD = MagicMock()
mock_dnd.DND_FILES = 'DND_Files'
sys.modules['tkinterdnd2'] = mock_dnd

# Also mock ico_converter since we might need it
mock_ico = types.ModuleType('ico_converter')
mock_ico.convert_png_to_ico = MagicMock()
sys.modules['ico_converter'] = mock_ico

import gui_wrapper
import inspect

def test_shortcuts():
    """Test keyboard shortcuts implementation."""
    print("Testing Keyboard Shortcuts Implementation...")
    print("-" * 50)

    # Track pass/fail
    failed = False

    try:
        # Test 1: Check new methods exist
        print("Test 1: Check for new methods")
        new_methods = [
            '_setup_shortcuts',
            '_select_all_files'
        ]

        for method_name in new_methods:
            if hasattr(gui_wrapper.IcoConverterGUI, method_name):
                print(f"  ✓ Method {method_name} exists")
            else:
                print(f"  ✗ Method {method_name} missing")
                failed = True

        # Test 2: Check _remove_selected_files accepts an argument (event)
        print("\nTest 2: Check _remove_selected_files signature")
        if hasattr(gui_wrapper.IcoConverterGUI, '_remove_selected_files'):
            sig = inspect.signature(gui_wrapper.IcoConverterGUI._remove_selected_files)
            params = list(sig.parameters.keys())
            # Should have 'self' and potentially 'event' or use *args/**kwargs
            # Standard method has 'self' as first param in signature
            if 'event' in params or len(params) > 1:
                 print(f"  ✓ _remove_selected_files accepts arguments: {sig}")
            else:
                 print(f"  ✗ _remove_selected_files signature incorrect: {sig}")
                 failed = True
        else:
             print("  ✗ _remove_selected_files method missing")
             failed = True

        # Test 3: Verify bindings in source code
        print("\nTest 3: Verify bindings in source code")
        with open('gui_wrapper.py', 'r') as f:
            content = f.read()

            # Check for delete binding
            if "bind('<Delete>'" in content or 'bind("<Delete>"' in content:
                print("  ✓ <Delete> binding found")
            else:
                print("  ✗ <Delete> binding missing")
                failed = True

            # Check for backspace binding
            if "bind('<BackSpace>'" in content or 'bind("<BackSpace>"' in content:
                print("  ✓ <BackSpace> binding found")
            else:
                print("  ✗ <BackSpace> binding missing")
                failed = True

            # Check for select all binding
            if "bind('<Control-a>'" in content or 'bind("<Control-a>"' in content:
                print("  ✓ <Control-a> binding found")
            else:
                print("  ✗ <Control-a> binding missing")
                failed = True

            # Check for button text update
            if '"Remove Selected (Del)"' in content or "'Remove Selected (Del)'" in content:
                print("  ✓ Button text updated")
            else:
                print("  ✗ Button text not updated")
                failed = True

        print("\n" + "=" * 50)

        if failed:
            print("Tests FAILED")
            return 1
        else:
            print("Tests PASSED")
            return 0

    except Exception as e:
        print(f"\n✗ Test ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(test_shortcuts())
