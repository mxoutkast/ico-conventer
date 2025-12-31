#!/usr/bin/env python3
"""
Create a test PNG file for manual GUI responsiveness testing.
"""

from PIL import Image, ImageDraw
from pathlib import Path


def create_test_png(size: int = 1024, filename: str = "test_large.png") -> Path:
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
    return test_path


if __name__ == '__main__':
    test_png = create_test_png(size=1024, filename="test_large.png")
    print(f"Created test PNG: {test_png} (1024x1024)")
    print()
    print("Manual Test Instructions:")
    print("1. Launch the GUI: python gui_wrapper.py")
    print("2. Drag 'test_large.png' onto the GUI window")
    print("3. Click 'Convert' button")
    print("4. While converting, verify:")
    print("   - Window is movable and resizable")
    print("   - Buttons respond to clicks")
    print("   - Progress bar updates smoothly")
    print("   - Status messages update in real-time")
    print()
    print("The window should NOT freeze during conversion!")
