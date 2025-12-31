#!/usr/bin/env python3
"""
Manual test script to verify GUI remains responsive during threaded conversion.
This script creates a test PNG and provides instructions for manual testing.
"""

from PIL import Image, ImageDraw
from pathlib import Path


def create_test_png(size: int = 512, filename: str = "test_large.png") -> Path:
    """Create a test PNG file with specified size."""
    # Create a simple image with some content
    img = Image.new('RGBA', (size, size), color=(100, 150, 200, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes to make the conversion take some time
    for i in range(10, size // 2, 20):
        draw.rectangle([i, i, size-i, size-i], outline=(255, 255, 255, 255), width=2)
    
    # Save the image
    test_path = Path(filename)
    img.save(test_path, 'PNG')
    print(f"Created test PNG: {test_path} ({size}x{size})")
    return test_path


def main():
    print("=" * 70)
    print("GUI Responsiveness Test - Manual Verification")
    print("=" * 70)
    print()
    
    # Create a test PNG file
    test_png = create_test_png(size=1024, filename="test_large_responsive.png")
    
    print()
    print("Manual Test Instructions:")
    print("-" * 70)
    print()
    print("1. Launch the GUI:")
    print("   python gui_wrapper.py")
    print()
    print("2. Drag the test file 'test_large_responsive.png' onto the GUI window")
    print()
    print("3. Click the 'Convert' button")
    print()
    print("4. While conversion is in progress:")
    print("   - Try to move the window around")
    print("   - Try to resize the window")
    print("   - Try to click on other buttons (Clear, Remove Selected)")
    print("   - Observe that the window remains responsive")
    print()
    print("5. Expected behavior:")
    print("   ✓ The window should NOT freeze")
    print("   ✓ The window should be movable and resizable")
    print("   ✓ Buttons should still respond to clicks")
    print("   ✓ Progress bar should update smoothly")
    print("   ✓ Status messages should update in real-time")
    print()
    print("6. After conversion completes:")
    print("   - Verify the ICO file was created successfully")
    print("   - Check that the status shows 'Success' or 'Failed'")
    print()
    print("-" * 70)
    print()
    print("Test file created: test_large_responsive.png")
    print()
    print("Press Ctrl+C to exit this script after testing")
    print()
    
    # Note: The script will create the test file and exit automatically
    # For manual testing, launch gui_wrapper.py and drag the test file onto it
    
    # Clean up test file
    if test_png.exists():
        test_png.unlink()
        print(f"Cleaned up test file: {test_png}")


if __name__ == '__main__':
    main()
