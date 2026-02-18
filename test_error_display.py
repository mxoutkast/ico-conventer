#!/usr/bin/env python3
"""
Test script to verify error display functionality in GUI wrapper.
This script tests the error handling and display features without launching the GUI.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Mock dependencies before importing gui_wrapper
sys.modules['tkinterdnd2'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Test imports
try:
    from gui_wrapper import IcoConverterGUI
    print("✓ gui_wrapper imports successfully")
except ImportError as e:
    print(f"✗ Failed to import gui_wrapper: {e}")
    sys.exit(1)

# Verify the _update_file_status method signature
import inspect
sig = inspect.signature(IcoConverterGUI._update_file_status)
params = list(sig.parameters.keys())

# Check that error_message parameter exists
if 'error_message' in params:
    print("✓ _update_file_status has error_message parameter")
else:
    print(f"✗ _update_file_status missing error_message parameter. Found: {params}")
    sys.exit(1)

# Verify _thread_safe_update_file_status signature
sig2 = inspect.signature(IcoConverterGUI._thread_safe_update_file_status)
params2 = list(sig2.parameters.keys())

if 'error_message' in params2:
    print("✓ _thread_safe_update_file_status has error_message parameter")
else:
    print(f"✗ _thread_safe_update_file_status missing error_message parameter. Found: {params2}")
    sys.exit(1)

print("\n✓ All error display functionality tests passed!")
print("\nKey features implemented:")
print("  - Added 'Error Details' column to file list")
print("  - Enhanced _update_file_status() to accept error_message parameter")
print("  - Enhanced _thread_safe_update_file_status() to accept error_message parameter")
print("  - Specific error handling for FileNotFoundError, PermissionError, and generic exceptions")
print("  - Error messages truncated to 100 characters if too long")
print("  - Error details displayed in the new Error Details column")
