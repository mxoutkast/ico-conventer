#!/usr/bin/env python3
"""Test import of gui_wrapper module."""

try:
    from gui_wrapper import IcoConverterGUI, threading
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
    exit(1)
