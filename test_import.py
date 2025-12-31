#!/usr/bin/env python3
"""Test script to verify convert_png_to_ico import"""

try:
    from gui_wrapper import convert_png_to_ico
    print("Import OK")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
