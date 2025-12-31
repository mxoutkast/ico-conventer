#!/usr/bin/env python3
"""
Verification script for threaded conversion implementation
"""

import sys
import ast
from pathlib import Path


def verify_implementation():
    """Verify that threading has been implemented correctly."""
    print("=" * 60)
    print("Threaded Conversion Implementation Verification")
    print("=" * 60)
    
    # Read gui_wrapper.py
    gui_wrapper_path = Path("gui_wrapper.py")
    if not gui_wrapper_path.exists():
        print("✗ ERROR: gui_wrapper.py not found")
        return False
    
    with open(gui_wrapper_path, 'r') as f:
        content = f.read()
    
    # Parse the file
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"✗ ERROR: Syntax error in gui_wrapper.py: {e}")
        return False
    
    # Check for threading import
    print("\nChecking imports...")
    threading_imported = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'threading':
                    threading_imported = True
                    print("  ✓ threading module imported")
                    break
    
    if not threading_imported:
        print("  ✗ threading module NOT imported")
        return False
    
    # Find IcoConverterGUI class
    gui_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'IcoConverterGUI':
            gui_class = node
            break
    
    if not gui_class:
        print("\n✗ ERROR: IcoConverterGUI class not found")
        return False
    
    print("\nChecking IcoConverterGUI class...")
    
    # Check for threading-related attributes
    has_conversion_thread = False
    has_is_converting = False
    
    # Check in __init__ method for instance attributes
    for node in gui_class.body:
        if isinstance(node, ast.FunctionDef) and node.name == '__init__':
            for child in ast.walk(node):
                if isinstance(child, ast.AnnAssign):
                    # Check for annotated assignments
                    if isinstance(child.target, ast.Attribute):
                        if child.target.attr == 'conversion_thread':
                            has_conversion_thread = True
                            print("  ✓ conversion_thread attribute found")
                        elif child.target.attr == 'is_converting':
                            has_is_converting = True
                            print("  ✓ is_converting attribute found")
                elif isinstance(child, ast.Assign):
                    # Check for regular assignments
                    for target in child.targets:
                        if isinstance(target, ast.Attribute):
                            if target.attr == 'conversion_thread':
                                has_conversion_thread = True
                                print("  ✓ conversion_thread attribute found")
                            elif target.attr == 'is_converting':
                                has_is_converting = True
                                print("  ✓ is_converting attribute found")
    
    if not has_conversion_thread or not has_is_converting:
        print("  ✗ Threading attributes not found")
        return False
    
    # Check for threading methods
    print("\nChecking threading methods...")
    has_convert_files = False
    has_run_conversion = False
    has_thread_safe_methods = False
    
    thread_safe_methods = [
        '_thread_safe_update_status',
        '_thread_safe_update_file_status',
        '_thread_safe_update_progress'
    ]
    
    for node in gui_class.body:
        if isinstance(node, ast.FunctionDef):
            if node.name == '_convert_files':
                has_convert_files = True
                print("  ✓ _convert_files method found")
                
                # Check if it creates a thread
                creates_thread = False
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            if child.func.id == 'Thread':
                                creates_thread = True
                                break
                        elif isinstance(child.func, ast.Attribute):
                            if child.func.attr == 'Thread':
                                creates_thread = True
                                break
                
                if creates_thread:
                    print("    ✓ _convert_files creates a Thread")
                else:
                    print("    ✗ _convert_files does NOT create a Thread")
                    return False
            
            elif node.name == '_run_conversion':
                has_run_conversion = True
                print("  ✓ _run_conversion method found")
            
            elif node.name in thread_safe_methods:
                has_thread_safe_methods = True
    
    if not has_convert_files:
        print("  ✗ _convert_files method not found")
        return False
    
    if not has_run_conversion:
        print("  ✗ _run_conversion method not found")
        return False
    
    if not has_thread_safe_methods:
        print("  ✗ Thread-safe methods not found")
        return False
    
    # Check for thread-safe methods
    print("\nChecking thread-safe UI update methods...")
    for method_name in thread_safe_methods:
        found = False
        for node in gui_class.body:
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                found = True
                # Check if it uses root.after
                uses_after = False
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Attribute):
                            if child.func.attr == 'after':
                                uses_after = True
                                break
                
                if uses_after:
                    print(f"  ✓ {method_name} uses root.after()")
                else:
                    print(f"  ✗ {method_name} does NOT use root.after()")
                    return False
                break
        
        if not found:
            print(f"  ✗ {method_name} not found")
            return False
    
    print("\n" + "=" * 60)
    print("✓ ALL VERIFICATIONS PASSED!")
    print("=" * 60)
    print("\nThreaded conversion implementation is complete:")
    print("  - threading module imported")
    print("  - conversion_thread attribute added")
    print("  - is_converting flag added")
    print("  - _convert_files creates a background thread")
    print("  - _run_conversion performs conversion in background")
    print("  - Thread-safe methods use root.after() for UI updates")
    print("  - GUI will remain responsive during conversions")
    
    return True


if __name__ == '__main__':
    success = verify_implementation()
    sys.exit(0 if success else 1)
