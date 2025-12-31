# Specification: Create the GUI Wrapper with Drag and Drop Feature

## Overview

This task involves creating a graphical user interface (GUI) wrapper for the existing PNG to ICO converter CLI tool. The GUI will provide drag-and-drop functionality to allow users to easily convert PNG images to ICO format without using the command line. The new GUI will leverage the existing conversion logic from `ico_converter.py` while providing an intuitive, user-friendly interface for batch processing files.

## Workflow Type

**Type**: feature

**Rationale**: This is a feature addition that creates new functionality (GUI interface) without modifying existing CLI behavior. The task involves creating new code that integrates with existing conversion logic.

## Task Scope

### Services Involved
- **main** (primary) - The single Python service that contains the CLI converter and will host the new GUI wrapper

### This Task Will:
- [ ] Create a new GUI interface using tkinter (standard Python library)
- [ ] Implement drag-and-drop functionality for PNG files
- [ ] Integrate existing conversion functions from ico_converter.py
- [ ] Provide visual feedback for conversion progress and status
- [ ] Support batch processing of multiple files via drag-and-drop
- [ ] Display conversion results and errors in the GUI
- [ ] Allow configuration of icon sizes through the GUI

### Out of Scope:
- Modifying the existing CLI functionality
- Creating web-based or mobile interfaces
- Implementing image editing features (cropping, resizing, etc.)
- Adding file format conversion beyond PNG to ICO

## Service Context

### main

**Tech Stack:**
- Language: Python
- Framework: None (using standard library tkinter for GUI)
- Key directories: Root directory (D:\ico-conventer)
- Dependencies: Pillow (already installed)

**Entry Point:** `ico_converter.py` (existing CLI) and new GUI wrapper file

**How to Run:**
```bash
# Existing CLI
python ico_converter.py *.png

# New GUI (to be created)
python gui_wrapper.py
# or
python ico_converter.py --gui  (if integrated)
```

**Port:** N/A (desktop GUI application, no network port)

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `ico_converter.py` | main | Refactor conversion functions to be importable/reusable by GUI (if needed) |
| `requirements.txt` | main | Add tkinter if needed (usually included with Python) |
| `README.md` | main | Add documentation for GUI usage |

## Files to Create

| File | Service | Purpose |
|------|---------|---------|
| `gui_wrapper.py` | main | Main GUI application with drag-and-drop functionality |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `ico_converter.py` | Conversion logic (convert_png_to_ico, collect_files functions) |
| `ico_converter.py` | Error handling and user feedback patterns |
| `ico_converter.py` | DEFAULT_SIZES constant for icon size configuration |

## Patterns to Follow

### Conversion Function Reuse

From `ico_converter.py`:

```python
def convert_png_to_ico(
    input_path: Path,
    output_path: Path,
    sizes: List[Tuple[int, int]],
    verbose: bool = False
) -> bool:
    """Convert a PNG image to ICO format with multiple sizes."""
    try:
        with Image.open(input_path) as img:
            # ... conversion logic
            img.save(output_path, format='ICO', sizes=sizes)
            return True
    except Exception as e:
        print(f"Error converting {input_path.name}: {e}")
        return False
```

**Key Points:**
- Reuse the existing `convert_png_to_ico` function for actual conversion
- Maintain the same error handling pattern
- Keep the same size configuration approach

### File Collection Pattern

From `ico_converter.py`:

```python
def collect_files(inputs: List[str], recursive: bool = False) -> List[Path]:
    """Collect all PNG files from various input types."""
    # ... implementation
```

**Key Points:**
- For GUI, files will come from drag-and-drop events
- Can simplify to just accept Path objects directly
- Validate PNG file extensions before processing

## Requirements

### Functional Requirements

1. **Drag-and-Drop Interface**
   - Description: Users should be able to drag PNG files from file explorer and drop them onto the GUI window
   - Acceptance: Dropping one or more PNG files adds them to a conversion queue/list in the GUI

2. **Batch Conversion**
   - Description: Support converting multiple PNG files in one operation
   - Acceptance: Multiple files can be dropped and processed sequentially with progress feedback

3. **Visual Feedback**
   - Description: Show conversion progress and status for each file
   - Acceptance: GUI displays a list of files with status indicators (pending, converting, success, error)

4. **Size Configuration**
   - Description: Allow users to select which icon sizes to include in the ICO files
   - Acceptance: GUI provides checkboxes or dropdown for selecting sizes (16, 32, 48, 64, 128, 256)

5. **Output Directory Selection**
   - Description: Allow users to choose where to save the converted ICO files
   - Acceptance: GUI includes a "Browse" button to select output directory, with default being same as input

6. **Error Handling**
   - Description: Display clear error messages when conversions fail
   - Acceptance: Failed conversions show error details in the GUI, allowing users to see what went wrong

7. **Conversion Progress**
   - Description: Show overall progress bar when converting multiple files
   - Acceptance: Progress bar updates as each file completes

### Edge Cases

1. **Non-PNG files dropped** - Filter out or show warning for unsupported file types
2. **Files with same name** - Handle naming conflicts (overwrite prompt or auto-rename)
3. **Large files** - Show progress and prevent UI freezing during conversion
4. **Empty drag-drop** - Ignore or show helpful message when no files are dropped
5. **Invalid PNG files** - Catch errors and display user-friendly messages
6. **No write permissions** - Show error if output directory is not writable

## Implementation Notes

### DO
- Use tkinter (standard Python library) for the GUI to avoid additional dependencies
- Reuse the `convert_png_to_ico` function from ico_converter.py by importing it
- Run conversions in a separate thread to prevent GUI freezing
- Use Path objects for file handling (consistent with existing code)
- Follow the existing code style and naming conventions
- Provide clear visual feedback for all user actions
- Include tooltips or help text for GUI elements

### DON'T
- Don't duplicate conversion logic - import and reuse existing functions
- Don't block the GUI thread with long-running operations
- Don't use complex third-party GUI libraries when tkinter suffices
- Don't remove or modify the existing CLI functionality
- Don't create a separate Python package - keep it simple as a single script

### Technical Considerations

1. **GUI Framework**: Use tkinter with `tkinterdnd2` for drag-and-drop support (may need to install)
   - Alternative: Use file dialogs if drag-and-drop is too complex
   - Fallback: Simple file selection dialog if drag-and-drop library has issues

2. **Threading**: Use `threading.Thread` or `concurrent.futures` for background conversions
   - Update GUI using `root.after()` or thread-safe methods
   - Prevent multiple simultaneous conversions of the same file

3. **State Management**: Maintain a list of files with their conversion status
   - Update UI as each file completes
   - Allow retrying failed conversions

4. **Configuration**: Save user preferences (sizes, output directory) to a simple config file or use defaults

## Development Environment

### Start Services

```bash
# No server needed - this is a desktop GUI application
# Simply run the Python script directly

# Install dependencies (if needed)
pip install -r requirements.txt

# For drag-and-drop support, may need:
pip install tkinterdnd2
```

### Service URLs
- N/A (desktop application, runs locally)

### Required Environment Variables
- None required

### Testing the GUI
```bash
# Run the GUI wrapper
python gui_wrapper.py

# Test with sample PNG files
# Drag and drop PNG files onto the window
# Verify conversions complete successfully
```

## Success Criteria

The task is complete when:

1. [ ] GUI application launches without errors
2. [ ] Drag-and-drop functionality works for PNG files
3. [ ] Multiple files can be dropped and processed
4. [ ] Conversion progress is displayed visually
5. [ ] Converted ICO files are generated correctly (verify by opening)
6. [ ] Error handling works for invalid files
7. [ ] Size configuration options work
8. [ ] Output directory selection works
9. [ ] No console errors during operation
10. [ ] GUI is responsive during conversions (doesn't freeze)

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| GUI initialization | `gui_wrapper.py` | Window opens without errors, all widgets display correctly |
| File validation | `gui_wrapper.py` | Non-PNG files are rejected or warned about |
| Size selection | `gui_wrapper.py` | Selected sizes are passed correctly to conversion function |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| Conversion integration | GUI ↔ ico_converter.py | GUI successfully calls convert_png_to_ico and handles return values |
| File path handling | GUI ↔ filesystem | Input and output paths are correctly resolved and used |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Single file conversion | 1. Launch GUI 2. Drag one PNG file 3. Click convert 4. Verify output | ICO file created in output directory with correct sizes |
| Batch conversion | 1. Launch GUI 2. Drag multiple PNG files 3. Click convert 4. Verify all outputs | All ICO files created, progress bar updates correctly |
| Custom sizes | 1. Launch GUI 2. Select custom sizes 3. Drag file 4. Convert 5. Verify | ICO contains only selected sizes |
| Error handling | 1. Launch GUI 2. Drag invalid/corrupted PNG 3. Convert | Error message displayed, other files continue processing |

### Browser Verification (if frontend)
N/A - This is a desktop GUI application, not a web interface.

### Database Verification (if applicable)
N/A - No database used in this application.

### Manual Testing Checklist
- [ ] GUI window opens and displays all controls
- [ ] Drag-and-drop accepts PNG files
- [ ] File list updates when files are dropped
- [ ] Convert button starts conversion process
- [ ] Progress bar updates during conversion
- [ ] Success/error status shown for each file
- [ ] Output directory can be changed
- [ ] Size checkboxes work and affect output
- [ ] Multiple files process in sequence
- [ ] GUI remains responsive during conversions
- [ ] Invalid files show appropriate error messages
- [ ] Converted ICO files can be opened and display correctly
- [ ] Application closes cleanly

### QA Sign-off Requirements
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Manual testing checklist complete
- [ ] No regressions in existing CLI functionality
- [ ] Code follows established patterns from ico_converter.py
- [ ] No security vulnerabilities introduced
- [ ] GUI is intuitive and user-friendly
- [ ] Error messages are clear and helpful
- [ ] Documentation (README) updated with GUI usage instructions
