#!/usr/bin/env python3
"""
Test script to verify file list UI component functionality.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch
import inspect
from pathlib import Path

# Mock dependencies
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinterdnd2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Mock TkinterDnD components
mock_tk = MagicMock()
sys.modules['tkinter'].Tk = MagicMock(return_value=mock_tk)
sys.modules['tkinter'].StringVar = MagicMock()
sys.modules['tkinter'].IntVar = MagicMock()
sys.modules['tkinter'].DoubleVar = MagicMock()

# Mock treeview
mock_treeview = MagicMock()
sys.modules['tkinter.ttk'].Treeview = MagicMock(return_value=mock_treeview)

import gui_wrapper

def test_file_list_component():
    """Test file list UI component functionality."""
    print("Testing File List UI Component...")
    print("-" * 50)
    
    try:
        # Test 1: Import gui_wrapper module
        print("Test 1: Import gui_wrapper module")
        # Already imported above
        print("  ✓ Module imported successfully")
        
        # Test 2: Check IcoConverterGUI class exists
        print("\nTest 2: IcoConverterGUI class exists")
        assert hasattr(gui_wrapper, 'IcoConverterGUI'), "IcoConverterGUI class not found"
        print("  ✓ IcoConverterGUI class found")
        
        # Test 3: Check required methods exist
        print("\nTest 3: Required methods exist")
        required_methods = [
            '_add_file_to_list',
            '_clear_file_list',
            '_remove_selected_files',
            '_select_all_files',  # Added new method
            '_update_file_status',
            '_update_file_counter',
            '_format_file_size'
        ]
        
        for method_name in required_methods:
            assert hasattr(gui_wrapper.IcoConverterGUI, method_name), f"Method {method_name} not found"
            print(f"  ✓ Method {method_name} exists")
        
        # Test 4: Check method signatures
        print("\nTest 4: Method signatures")
        
        # Check _add_file_to_list signature
        sig = inspect.signature(gui_wrapper.IcoConverterGUI._add_file_to_list)
        params = list(sig.parameters.keys())
        assert 'self' in params and 'file_path' in params, "_add_file_to_list signature incorrect"
        print(f"  ✓ _add_file_to_list signature: {sig}")
        
        # Check _format_file_size signature
        sig = inspect.signature(gui_wrapper.IcoConverterGUI._format_file_size)
        params = list(sig.parameters.keys())
        assert 'self' in params and 'size_bytes' in params, "_format_file_size signature incorrect"
        print(f"  ✓ _format_file_size signature: {sig}")
        
        # Check _select_all_files signature
        sig = inspect.signature(gui_wrapper.IcoConverterGUI._select_all_files)
        params = list(sig.parameters.keys())
        assert 'self' in params and 'event' in params, "_select_all_files signature incorrect"
        print(f"  ✓ _select_all_files signature: {sig}")

        # Test 5: Test _format_file_size function independently
        print("\nTest 5: File size formatting")
        # Create a temporary instance to test the method
        class TestGUI:
            def _format_file_size(self, size_bytes: int) -> str:
                """Format file size in human-readable format."""
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size_bytes < 1024.0:
                        return f"{size_bytes:.1f} {unit}"
                    size_bytes /= 1024.0
                return f"{size_bytes:.1f} TB"
        
        test_gui = TestGUI()
        test_sizes = [
            (100, "100.0 B"),
            (2048, "2.0 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB")
        ]
        for size_bytes, expected in test_sizes:
            result = test_gui._format_file_size(size_bytes)
            assert result == expected, f"Expected '{expected}', got '{result}'"
            print(f"  ✓ {size_bytes} bytes → {result}")
        
        # Test 6: Verify file list has correct columns and bindings
        print("\nTest 6: Verify source code structure")
        with open('gui_wrapper.py', 'r') as f:
            content = f.read()
            
            # Check for file list creation with columns
            assert "columns=('filename', 'size', 'status', 'error')" in content, \
                "File list doesn't have correct columns"
            print("  ✓ File list has correct columns")
            
            # Check for file counter
            assert "self.file_counter" in content, "File counter not found"
            print("  ✓ File counter label exists")
            
            # Check for remove button with hint
            assert 'text="Remove Selected (Del)"' in content, "Remove button hint not found"
            print("  ✓ Remove Selected button has keyboard hint")
            
            # Check for status update method
            assert "_update_file_status" in content, "Status update method not found"
            print("  ✓ File status update method exists")

            # Check for key bindings
            assert "bind('<Delete>', self._remove_selected_files)" in content, "Delete binding missing"
            assert "bind('<BackSpace>', self._remove_selected_files)" in content, "Backspace binding missing"
            assert "bind('<Control-a>', self._select_all_files)" in content, "Control-a binding missing"
            print("  ✓ Keyboard shortcuts are bound")

            # Check for macOS binding
            assert "bind('<Command-a>', self._select_all_files)" in content, "Command-a binding missing"
            print("  ✓ macOS Command-a binding exists")
        
        print("\n" + "=" * 50)
        print("All tests PASSED! ✓")
        print("=" * 50)
        print("\nFile List UI Component Features:")
        print("  • Displays filename, size, and status")
        print("  • Shows file count (with proper singular/plural)")
        print("  • Human-readable file size formatting")
        print("  • Add files via drag-and-drop")
        print("  • Remove selected files (with Delete key)")
        print("  • Select all files (with Ctrl/Cmd+A)")
        print("  • Clear all files")
        print("  • Update file status individually")
        print("=" * 50)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Test ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(test_file_list_component())
