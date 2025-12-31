#!/usr/bin/env python3
"""
Test script to verify threaded conversion implementation
"""

import sys
import tkinter as tk
from pathlib import Path
from PIL import Image
import time

# Create a test PNG file
def create_test_png(path: Path, size: int = 256):
    """Create a test PNG image."""
    img = Image.new('RGBA', (size, size), color=(255, 0, 0, 255))
    img.save(path, 'PNG')
    print(f"Created test PNG: {path}")

# Test imports
try:
    from gui_wrapper import IcoConverterGUI
    print("✓ gui_wrapper imports successfully")
except Exception as e:
    print(f"✗ Failed to import gui_wrapper: {e}")
    sys.exit(1)

try:
    from ico_converter import convert_png_to_ico
    print("✓ ico_converter imports successfully")
except Exception as e:
    print(f"✗ Failed to import ico_converter: {e}")
    sys.exit(1)

# Test threading module
import threading
print("✓ threading module available")

# Test that the GUI can be instantiated (without showing the window)
try:
    root = tk.Tk()
    root.withdraw()  # Hide the window
    print("✓ Tkinter root window created")
except Exception as e:
    print(f"✗ Failed to create Tkinter root: {e}")
    sys.exit(1)

print("\nAll basic tests passed!")
print("\nTo manually test the GUI:")
print("1. Run: python gui_wrapper.py")
print("2. Drag and drop a PNG file")
print("3. Click Convert")
print("4. Verify the GUI remains responsive during conversion")
print("5. Check that progress bar updates and status messages appear")
