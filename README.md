# PNG to ICO Converter

A simple CLI tool to convert PNG images to ICO format with multiple embedded icon sizes.

## Setup

### 1. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Convert a single file
python ico_converter.py image.png

# Convert multiple files
python ico_converter.py file1.png file2.png file3.png

# Convert all PNGs in current directory
python ico_converter.py *.png

# Convert all PNGs in a directory
python ico_converter.py images/

# Convert recursively through subdirectories
python ico_converter.py images/ -r
```

### Advanced Options

```bash
# Specify output directory (default: same directory as input files)
python ico_converter.py *.png -o icons/

# Custom icon sizes (default: 16 32 48 64 128 256)
python ico_converter.py image.png --sizes 16 32 48

# Add suffix to output filenames
python ico_converter.py *.png --suffix _icon

# Overwrite existing files
python ico_converter.py *.png --overwrite

# Dry run (preview without converting)
python ico_converter.py *.png --dry-run

# Verbose output
python ico_converter.py image.png -v
```

## Features

- **Multiple Icon Sizes**: Embeds standard Windows icon sizes (16, 32, 48, 64, 128, 256) in a single ICO file
- **Batch Processing**: Convert multiple files at once using wildcards or directory input
- **Recursive Search**: Process entire directory trees with the `-r` flag
- **Smart Input Handling**: Accepts individual files, directories, or glob patterns
- **Error Handling**: Continues processing remaining files if one fails
- **RGBA Support**: Automatically converts images to RGBA for proper transparency
- **Overwrite Protection**: Prompts before overwriting existing files (unless `--overwrite` is used)

## Requirements

- Python 3.6+
- Pillow >= 9.0.0

## Input Requirements

- Format: PNG
- Recommended size: 1024x1024 pixels (or at least 256x256)
- The tool will warn if input is smaller than the largest requested icon size

## Output

- Format: ICO (Windows Icon)
- Default sizes embedded: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
- All sizes are embedded in a single .ico file
