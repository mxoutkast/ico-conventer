#!/usr/bin/env python3
"""Create a test PNG file for testing drag-and-drop."""

from PIL import Image

# Create a simple test PNG
img = Image.new('RGBA', (256, 256), color='blue')
img.save('test.png')
print('Test PNG created: test.png')
