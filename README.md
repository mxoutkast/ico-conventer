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

## GUI Usage

The PNG to ICO Converter also includes a user-friendly graphical interface with drag-and-drop functionality.

### GUI Setup

#### Install GUI Dependencies

The GUI requires an additional package for drag-and-drop functionality:

```bash
pip install tkinterdnd2
```

#### Running the GUI

```bash
python gui_wrapper.py
```

### GUI Features

- **Drag and Drop**: Simply drag PNG files from your file explorer and drop them into the application window
- **Icon Size Selection**: Choose which icon sizes to embed (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
- **Output Directory**: Select a custom output directory or save ICO files alongside the original PNGs
- **Batch Processing**: Convert multiple files at once
- **Progress Tracking**: Real-time progress bar and status updates
- **Error Display**: Detailed error messages for any conversion failures
- **File Management**: View file list, remove selected files, or clear the entire list
- **Keyboard Shortcuts**: Use `Delete` to remove files and `Ctrl+A` (or `Cmd+A`) to select all

### Using the GUI

1. **Launch the application**: Run `python gui_wrapper.py`
2. **Add files**: Drag and drop PNG files into the drop zone, or use the file browser (coming soon)
3. **Configure options**:
   - Select desired icon sizes using the checkboxes
   - Optionally choose an output directory (click "Browse..." to select, or "Clear" to save with input files)
4. **Convert**: Click the "Convert" button to start the conversion process
5. **View results**: Check the status column for success/error messages

### GUI Requirements

- Python 3.6+
- Pillow >= 9.0.0
- tkinterdnd2 >= 0.3.0

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
