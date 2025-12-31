#!/usr/bin/env python3
"""Test script for drag-and-drop functionality."""

import sys
import tkinter as tk
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui_wrapper import IcoConverterGUI


def test_on_drop_handler():
    """Test the _on_drop event handler."""
    print("Testing _on_drop handler...")
    
    # Create a mock root window
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create GUI instance
    gui = IcoConverterGUI(root)
    
    # Create a mock event with file data
    event = Mock()
    event.data = str(Path('test.png').absolute())
    
    # Call the handler
    gui._on_drop(event)
    
    # Verify file was added
    assert len(gui.dropped_files) == 1, f"Expected 1 file, got {len(gui.dropped_files)}"
    assert gui.dropped_files[0].name == 'test.png', f"Expected test.png, got {gui.dropped_files[0].name}"
    
    # Verify file appears in list
    children = gui.file_list.get_children()
    assert len(children) == 1, f"Expected 1 item in list, got {len(children)}"
    
    values = gui.file_list.item(children[0])['values']
    assert values[0] == 'test.png', f"Expected 'test.png' in list, got {values[0]}"
    assert values[1] == 'Pending', f"Expected 'Pending' status, got {values[1]}"
    
    print("✓ _on_drop handler test passed")
    
    root.destroy()


def test_parse_drop_paths():
    """Test the _parse_drop_paths method."""
    print("Testing _parse_drop_paths...")
    
    root = tk.Tk()
    root.withdraw()
    gui = IcoConverterGUI(root)
    
    # Test single path
    paths = gui._parse_drop_paths('test.png')
    assert len(paths) == 1, f"Expected 1 path, got {len(paths)}"
    assert paths[0] == 'test.png', f"Expected 'test.png', got {paths[0]}"
    print("  ✓ Single path test passed")
    
    # Test multiple paths (space separated)
    paths = gui._parse_drop_paths('test1.png test2.png test3.png')
    assert len(paths) == 3, f"Expected 3 paths, got {len(paths)}"
    print("  ✓ Multiple paths test passed")
    
    # Test Windows format with braces
    paths = gui._parse_drop_paths('{test1.png} {test2.png}')
    assert len(paths) == 2, f"Expected 2 paths, got {len(paths)}"
    print("  ✓ Windows brace format test passed")
    
    # Test quoted paths
    paths = gui._parse_drop_paths('"test file.png" another.png')
    assert len(paths) == 2, f"Expected 2 paths, got {len(paths)}"
    print("  ✓ Quoted paths test passed")
    
    root.destroy()
    print("✓ _parse_drop_paths test passed")


def test_drag_enter_leave():
    """Test drag enter and leave handlers."""
    print("Testing _on_drag_enter and _on_drag_leave...")
    
    root = tk.Tk()
    root.withdraw()
    gui = IcoConverterGUI(root)
    
    # Test drag enter
    event = Mock()
    gui._on_drag_enter(event)
    assert gui.status_label.cget('text') == 'Drop PNG files here...', \
        f"Expected 'Drop PNG files here...', got '{gui.status_label.cget('text')}'"
    print("  ✓ Drag enter test passed")
    
    # Test drag leave
    gui._on_drag_leave(event)
    assert gui.status_label.cget('text') == 'Ready', \
        f"Expected 'Ready', got '{gui.status_label.cget('text')}'"
    print("  ✓ Drag leave test passed")
    
    root.destroy()
    print("✓ Drag enter/leave test passed")


def test_non_png_filtering():
    """Test that non-PNG files are filtered out."""
    print("Testing non-PNG file filtering...")
    
    root = tk.Tk()
    root.withdraw()
    gui = IcoConverterGUI(root)
    
    # Create test files
    Path('test.txt').touch()
    Path('test.jpg').touch()
    
    try:
        # Try to drop non-PNG files
        event = Mock()
        event.data = f"{Path('test.txt').absolute()} {Path('test.jpg').absolute()}"
        gui._on_drop(event)
        
        # Verify no files were added
        assert len(gui.dropped_files) == 0, f"Expected 0 files (non-PNG filtered), got {len(gui.dropped_files)}"
        print("  ✓ Non-PNG files filtered correctly")
        
        # Now drop a PNG file
        event.data = str(Path('test.png').absolute())
        gui._on_drop(event)
        
        assert len(gui.dropped_files) == 1, f"Expected 1 file (PNG), got {len(gui.dropped_files)}"
        print("  ✓ PNG file added correctly")
        
    finally:
        # Cleanup
        Path('test.txt').unlink(missing_ok=True)
        Path('test.jpg').unlink(missing_ok=True)
    
    root.destroy()
    print("✓ Non-PNG filtering test passed")


def test_duplicate_files():
    """Test that duplicate files are not added."""
    print("Testing duplicate file handling...")
    
    root = tk.Tk()
    root.withdraw()
    gui = IcoConverterGUI(root)
    
    # Drop the same file twice
    event = Mock()
    event.data = str(Path('test.png').absolute())
    
    gui._on_drop(event)
    assert len(gui.dropped_files) == 1, f"Expected 1 file after first drop, got {len(gui.dropped_files)}"
    
    gui._on_drop(event)
    assert len(gui.dropped_files) == 1, f"Expected 1 file after duplicate drop, got {len(gui.dropped_files)}"
    
    root.destroy()
    print("✓ Duplicate file handling test passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Drag-and-Drop Event Handler Tests")
    print("=" * 60)
    print()
    
    try:
        test_on_drop_handler()
        print()
        test_parse_drop_paths()
        print()
        test_drag_enter_leave()
        print()
        test_non_png_filtering()
        print()
        test_duplicate_files()
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"Test failed: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
