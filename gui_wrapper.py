#!/usr/bin/env python3
"""
PNG to ICO Converter - GUI wrapper with drag-and-drop functionality
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from typing import List, Optional
import threading

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    print("Error: tkinterdnd2 is required for drag-and-drop functionality")
    print("Install it with: pip install tkinterdnd2")
    sys.exit(1)

# Import conversion function from ico_converter
from ico_converter import convert_png_to_ico


# Standard icon sizes for Windows ICO files (from ico_converter.py)
DEFAULT_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


class IcoConverterGUI:
    """Main GUI application for PNG to ICO converter."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.
        
        Args:
            root: The root Tk window
        """
        self.root = root
        self.root.title("PNG to ICO Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # State variables
        self.dropped_files: List[Path] = []
        self.output_dir: Optional[Path] = None
        self.selected_sizes: List[tuple] = DEFAULT_SIZES.copy()
        
        # Size checkbox variables
        self.size_vars = {
            16: tk.IntVar(value=1),
            32: tk.IntVar(value=1),
            48: tk.IntVar(value=1),
            64: tk.IntVar(value=1),
            128: tk.IntVar(value=1),
            256: tk.IntVar(value=1)
        }
        
        # Output directory display variable
        self.output_dir_var = tk.StringVar(value="Same as input files")
        
        # Threading state
        self.conversion_thread: Optional[threading.Thread] = None
        self.is_converting: bool = False
        
        # Initialize drag-and-drop
        self._setup_drag_drop()
        
        # Setup UI components
        self._setup_ui()
    
    def _setup_drag_drop(self) -> None:
        """Configure drag-and-drop functionality for the main window."""
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self._on_drop)
            self.root.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.root.dnd_bind('<<DragLeave>>', self._on_drag_leave)
        except Exception as e:
            print(f"Warning: Could not initialize drag-and-drop: {e}")
    
    def _setup_ui(self) -> None:
        """Create and layout all UI components."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame,
            text="PNG to ICO Converter",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Instructions label
        instructions = ttk.Label(
            main_frame,
            text="Drag and drop PNG files here to convert them to ICO format",
            font=('Helvetica', 10)
        )
        instructions.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)
        
        # Configuration frame for size selection
        config_frame = ttk.LabelFrame(
            main_frame,
            text="Icon Sizes",
            padding="10"
        )
        config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Size checkboxes
        sizes = [16, 32, 48, 64, 128, 256]
        for i, size in enumerate(sizes):
            checkbox = ttk.Checkbutton(
                config_frame,
                text=f"{size}x{size}",
                variable=self.size_vars[size],
                command=self._update_selected_sizes
            )
            checkbox.grid(row=0, column=i, padx=5)
        
        # Output directory frame
        output_frame = ttk.LabelFrame(
            main_frame,
            text="Output Directory",
            padding="10"
        )
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        
        # Output directory path display
        output_path_label = ttk.Label(
            output_frame,
            textvariable=self.output_dir_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        output_path_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Browse button
        browse_button = ttk.Button(
            output_frame,
            text="Browse...",
            command=self._browse_output_directory
        )
        browse_button.grid(row=0, column=1, sticky=tk.E)
        
        # Clear output directory button
        clear_output_button = ttk.Button(
            output_frame,
            text="Clear",
            command=self._clear_output_directory
        )
        clear_output_button.grid(row=0, column=2, sticky=tk.E, padx=(5, 0))
        
        # Drop zone frame
        drop_zone = ttk.LabelFrame(
            main_frame,
            text="Drop Zone",
            padding="10"
        )
        drop_zone.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        drop_zone.columnconfigure(0, weight=1)
        drop_zone.rowconfigure(0, weight=1)
        
        # File list (Treeview)
        self.file_list = ttk.Treeview(
            drop_zone,
            columns=('filename', 'size', 'status', 'error'),
            show='headings',
            selectmode='extended'
        )
        self.file_list.heading('filename', text='Filename')
        self.file_list.heading('size', text='Size')
        self.file_list.heading('status', text='Status')
        self.file_list.heading('error', text='Error Details')
        self.file_list.column('filename', width=250, minwidth=150)
        self.file_list.column('size', width=80, minwidth=60)
        self.file_list.column('status', width=100, minwidth=80)
        self.file_list.column('error', width=300, minwidth=200)
        self.file_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure tags for different statuses with colors
        self.file_list.tag_configure('success', foreground='green')
        self.file_list.tag_configure('error', foreground='red')
        self.file_list.tag_configure('failed', foreground='red')
        self.file_list.tag_configure('pending', foreground='gray')
        self.file_list.tag_configure('converting', foreground='blue')
        
        # Keyboard shortcuts for file list
        self.file_list.bind('<Delete>', self._remove_selected_files)
        self.file_list.bind('<BackSpace>', self._remove_selected_files)
        self.file_list.bind('<Control-a>', self._select_all_files)
        try:
            self.file_list.bind('<Command-a>', self._select_all_files)
        except tk.TclError:
            pass # macOS specific key, ignore on other platforms

        # Scrollbar for file list
        scrollbar = ttk.Scrollbar(
            drop_zone,
            orient=tk.VERTICAL,
            command=self.file_list.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_list.configure(yscrollcommand=scrollbar.set)
        
        # File counter label
        self.file_counter = ttk.Label(
            drop_zone,
            text="0 files",
            font=('Helvetica', 9)
        )
        self.file_counter.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Configure drag-and-drop for drop zone
        self._setup_drop_zone_drag_drop(drop_zone)
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(0, 10), sticky=tk.W)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="Clear List",
            command=self._clear_file_list
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove selected button
        remove_button = ttk.Button(
            button_frame,
            text="Remove Selected (Del)",
            command=self._remove_selected_files
        )
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        convert_button = ttk.Button(
            button_frame,
            text="Convert",
            command=self._convert_files
        )
        convert_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        progress_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=7, column=0, sticky=(tk.W, tk.E))
    
    def _browse_output_directory(self) -> None:
        """Open directory browser dialog to select output directory."""
        try:
            # Open directory selection dialog
            directory = filedialog.askdirectory(
                title="Select Output Directory",
                initialdir=str(self.output_dir) if self.output_dir else None
            )
            
            if directory:
                self.output_dir = Path(directory)
                # Update display to show relative path if possible, otherwise absolute
                try:
                    rel_path = self.output_dir.relative_to(Path.cwd())
                    display_path = f"./{rel_path}"
                except ValueError:
                    display_path = str(self.output_dir)
                self.output_dir_var.set(display_path)
                self._update_status(f"Output directory set to: {display_path}")
        except Exception as e:
            self._update_status(f"Error selecting directory: {e}")
    
    def _clear_output_directory(self) -> None:
        """Clear the selected output directory (revert to default)."""
        self.output_dir = None
        self.output_dir_var.set("Same as input files")
        self._update_status("Output directory cleared (will save with input files)")
    
    def _setup_drop_zone_drag_drop(self, widget: tk.Widget) -> None:
        """
        Configure drag-and-drop for a specific widget.
        
        Args:
            widget: The widget to configure for drag-and-drop
        """
        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', self._on_drop)
            widget.dnd_bind('<<DragEnter>>', lambda e: widget.configure(relief=tk.SOLID))
            widget.dnd_bind('<<DragLeave>>', lambda e: widget.configure(relief=tk.GROOVE))
        except Exception as e:
            print(f"Warning: Could not configure drag-and-drop for widget: {e}")
    
    def _update_selected_sizes(self) -> None:
        """Update the selected_sizes list based on checkbox states."""
        self.selected_sizes = []
        for size, var in self.size_vars.items():
            if var.get() == 1:
                self.selected_sizes.append((size, size))
        self.selected_sizes.sort()
    
    def _on_drop(self, event: tk.Event) -> None:
        """
        Handle file drop event.
        
        Args:
            event: The drop event containing file paths
        """
        try:
            # Get dropped files
            files = event.data
            if not files:
                return
            
            # Parse file paths (handle different formats)
            file_paths = self._parse_drop_paths(files)
            
            # Add valid PNG files to the list
            added_count = 0
            skipped_count = 0
            invalid_count = 0
            invalid_files = []
            
            for file_path in file_paths:
                path = Path(file_path)
                if path.is_file() and path.suffix.lower() == '.png':
                    if path not in self.dropped_files:
                        self.dropped_files.append(path)
                        self._add_file_to_list(path)
                        added_count += 1
                    else:
                        skipped_count += 1
                else:
                    invalid_count += 1
                    invalid_files.append(path.name)
            
            # Update status with detailed feedback
            if added_count > 0:
                message = f"Added {added_count} file(s) to list"
                if skipped_count > 0:
                    message += f" (skipped {skipped_count} duplicate(s))"
                if invalid_count > 0:
                    message += f" (ignored {invalid_count} non-PNG file(s))"
                self._update_status(message)
                
                # Show individual warnings for non-PNG files (following pattern from ico_converter.py)
                for invalid_file in invalid_files:
                    self._update_status(f"Warning: Skipping non-PNG file: {invalid_file}")
            elif skipped_count > 0:
                self._update_status(f"All files already in list (skipped {skipped_count} duplicate(s))")
            elif invalid_count > 0:
                self._update_status(f"No valid PNG files found (ignored {invalid_count} non-PNG file(s))")
                for invalid_file in invalid_files:
                    self._update_status(f"Warning: Skipping non-PNG file: {invalid_file}")
            else:
                self._update_status("No valid PNG files found")
                
        except Exception as e:
            self._update_status(f"Error processing dropped files: {e}")
    
    def _on_drag_enter(self, event: tk.Event) -> None:
        """Handle drag enter event."""
        self._update_status("Drop PNG files here...")
    
    def _on_drag_leave(self, event: tk.Event) -> None:
        """Handle drag leave event."""
        self._update_status("Ready")
    
    def _parse_drop_paths(self, data: str) -> List[str]:
        """
        Parse file paths from drop event data.

        Args:
            data: Raw drop event data

        Returns:
            List of file paths
        """
        # Handle different formats:
        # - Windows: paths enclosed in braces {path1} {path2} (each path wrapped)
        # - Windows: entire list wrapped {path1 path2}
        # - Unix: space-separated paths

        paths = []
        data = data.strip()

        # Check if individual paths are wrapped in braces
        # Pattern: {path1} {path2}
        import re
        brace_matches = re.findall(r'\{([^}]+)\}', data)

        if brace_matches and len(brace_matches) > 1:
            # Found multiple individually wrapped paths
            paths = brace_matches
        elif data.startswith('{') and data.endswith('}'):
            # Entire string is wrapped in braces (single path or space-separated list)
            # Remove outer braces
            inner_data = data[1:-1]
            # Split by whitespace
            paths = inner_data.split()
        else:
            # No braces, handle as space-separated or quoted paths
            import shlex
            try:
                paths = shlex.split(data)
            except ValueError:
                # Fallback to simple split
                paths = data.split()

        # Clean up paths (remove quotes and whitespace)
        cleaned_paths = []
        for path in paths:
            path = path.strip().strip('"').strip("'")
            if path:
                cleaned_paths.append(path)

        return cleaned_paths
    
    def _add_file_to_list(self, file_path: Path) -> None:
        """
        Add a file to the file list display.
        
        Args:
            file_path: Path to the file to add
        """
        try:
            # Get file size in human-readable format
            file_size = file_path.stat().st_size
            size_str = self._format_file_size(file_size)
            
            # Insert file into list with empty error column and pending tag
            self.file_list.insert('', tk.END, values=(file_path.name, size_str, 'Pending', ''), tags=('pending',))
        except Exception as e:
            # If we can't get file size, still add the file
            self.file_list.insert('', tk.END, values=(file_path.name, 'N/A', 'Pending', ''), tags=('pending',))
        
        # Update file counter
        self._update_file_counter()
    
    def _update_file_counter(self) -> None:
        """Update the file counter label."""
        count = len(self.dropped_files)
        self.file_counter.config(text=f"{count} file{'s' if count != 1 else ''}")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: File size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _clear_file_list(self) -> None:
        """Clear all files from the list."""
        self.dropped_files.clear()
        self.file_list.delete(*self.file_list.get_children())
        self.progress_var.set(0)
        self._update_file_counter()
        self._update_status("List cleared")
    
    def _select_all_files(self, event: tk.Event | None = None) -> str:
        """
        Select all files in the list.

        Args:
            event: The Tkinter event that triggered the binding, if any.

        Returns:
            'break' to prevent default Tkinter event propagation.
        """
        for item_id in self.file_list.get_children():
            self.file_list.selection_add(item_id)
        return 'break'

    def _remove_selected_files(self, event: tk.Event | None = None) -> str:
        """
        Remove selected files from the list.

        Args:
            event: The Tkinter event that triggered the binding, if any.

        Returns:
            'break' to prevent default Tkinter event propagation.
        """
        selected_items = self.file_list.selection()
        if not selected_items:
            self._update_status("No files selected")
            return 'break'
        
        # Get filenames of selected items
        selected_filenames = set()
        for item_id in selected_items:
            values = self.file_list.item(item_id)['values']
            if values:
                selected_filenames.add(values[0])
        
        # Remove from dropped_files list
        self.dropped_files = [
            path for path in self.dropped_files
            if path.name not in selected_filenames
        ]
        
        # Remove from treeview
        for item_id in selected_items:
            self.file_list.delete(item_id)
        
        self._update_file_counter()
        self._update_status(f"Removed {len(selected_items)} file(s)")
        return 'break'
    
    def _update_file_status(self, file_path: Path, status: str, error_message: str = '') -> None:
        """
        Update the status of a specific file in the list.
        
        Args:
            file_path: Path to the file to update
            status: New status string
            error_message: Optional error message to display
        """
        for item_id in self.file_list.get_children():
            values = self.file_list.item(item_id)['values']
            if values and values[0] == file_path.name:
                # Determine tag based on status
                tag = 'pending'
                if status == 'Success':
                    tag = 'success'
                elif status == 'Error':
                    tag = 'error'
                elif status == 'Failed':
                    tag = 'failed'
                elif status == 'Converting':
                    tag = 'converting'
                
                self.file_list.item(item_id, values=(values[0], values[1], status, error_message), tags=(tag,))
                break
    
    def _convert_files(self) -> None:
        """Start the conversion process for all files in the list in a separate thread."""
        if not self.dropped_files:
            self._update_status("No files to convert")
            return
        
        if self.is_converting:
            self._update_status("Conversion already in progress...")
            return
        
        # Reset file statuses and clear error messages with pending tag
        for item_id in self.file_list.get_children():
            values = self.file_list.item(item_id)['values']
            if values:
                self.file_list.item(item_id, values=(values[0], values[1], 'Pending', ''), tags=('pending',))
        
        # Update UI to show converting state
        self._set_converting_state(True)
        
        # Start conversion in a separate thread
        self.is_converting = True
        self.conversion_thread = threading.Thread(target=self._run_conversion, daemon=True)
        self.conversion_thread.start()
    
    def _run_conversion(self) -> None:
        """Run the conversion process in a background thread."""
        total_files = len(self.dropped_files)
        success_count = 0
        error_count = 0
        
        # Update status using thread-safe method
        self._thread_safe_update_status(f"Converting {total_files} file(s)...")
        
        for i, input_path in enumerate(self.dropped_files, 1):
            error_message = ''
            try:
                # Update status to "Converting" before processing
                self._thread_safe_update_file_status(input_path, "Converting", '')
                
                # Determine output path
                if self.output_dir:
                    output_path = self.output_dir / f"{input_path.stem}.ico"
                else:
                    output_path = input_path.parent / f"{input_path.stem}.ico"
                
                # Update status to show current file
                self._thread_safe_update_status(f"Converting [{i}/{total_files}]: {input_path.name}")
                
                # Convert the file
                if convert_png_to_ico(input_path, output_path, self.selected_sizes, verbose=False):
                    self._thread_safe_update_file_status(input_path, "Success", '')
                    success_count += 1
                else:
                    # Conversion failed but didn't raise an exception
                    error_message = "Conversion failed - see console for details"
                    self._thread_safe_update_file_status(input_path, "Failed", error_message)
                    error_count += 1
                
                # Update progress bar
                progress = (i / total_files) * 100
                self._thread_safe_update_progress(progress)
                
            except FileNotFoundError as e:
                # File not found error
                error_message = f"File not found: {e}"
                self._thread_safe_update_file_status(input_path, "Error", error_message)
                error_count += 1
                
            except PermissionError as e:
                # Permission error
                error_message = f"Permission denied: {e}"
                self._thread_safe_update_file_status(input_path, "Error", error_message)
                error_count += 1
                
            except Exception as e:
                # Other errors - provide detailed error message following pattern from ico_converter.py
                error_message = str(e)
                # If error is too long, truncate it
                if len(error_message) > 100:
                    error_message = error_message[:97] + "..."
                self._thread_safe_update_file_status(input_path, "Error", error_message)
                error_count += 1
        
        # Show summary and reset converting state
        self.is_converting = False
        self._thread_safe_set_converting_state(False)
        
        # Build detailed completion summary
        if error_count == 0:
            summary = f"✓ Conversion complete! Successfully converted {success_count} file(s)"
        else:
            summary = f"Conversion complete! Success: {success_count}, Errors: {error_count}"
        
        self._thread_safe_update_status(summary)
    
    def _set_converting_state(self, converting: bool) -> None:
        """
        Update UI elements based on conversion state.
        Disables buttons during conversion to prevent concurrent operations.
        
        Args:
            converting: Whether conversion is in progress
        """
        # Find the button frame and update its children
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame) and any(
                        isinstance(btn, ttk.Button) for btn in child.winfo_children()
                    ):
                        # This is the button frame
                        for btn in child.winfo_children():
                            if isinstance(btn, ttk.Button):
                                btn_text = btn.cget('text')
                                if btn_text == 'Convert':
                                    if converting:
                                        btn.configure(text='Converting...', state=tk.DISABLED)
                                    else:
                                        btn.configure(text='Convert', state=tk.NORMAL)
                                elif converting:
                                    btn.configure(state=tk.DISABLED)
                                else:
                                    btn.configure(state=tk.NORMAL)
    
    def _thread_safe_set_converting_state(self, converting: bool) -> None:
        """
        Thread-safe method to update the converting state.
        
        Args:
            converting: Whether conversion is in progress
        """
        self.root.after(0, lambda: self._set_converting_state(converting))
    
    def _thread_safe_update_status(self, message: str) -> None:
        """
        Update the status label in a thread-safe manner.
        
        Args:
            message: Status message to display
        """
        self.root.after(0, lambda: self._update_status(message))
    
    def _thread_safe_update_file_status(self, file_path: Path, status: str, error_message: str = '') -> None:
        """
        Update the status of a specific file in a thread-safe manner.
        
        Args:
            file_path: Path to the file to update
            status: New status string
            error_message: Optional error message to display
        """
        self.root.after(0, lambda: self._update_file_status(file_path, status, error_message))
    
    def _thread_safe_update_progress(self, value: float) -> None:
        """
        Update the progress bar in a thread-safe manner.
        
        Args:
            value: Progress value (0-100)
        """
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def _update_status(self, message: str) -> None:
        """
        Update the status label.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)


def main() -> int:
    """
    Main entry point for the GUI application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Create root window with drag-and-drop support
        root = TkinterDnD.Tk()
        
        # Create application
        app = IcoConverterGUI(root)
        
        # Start main loop
        root.mainloop()
        
        return 0
        
    except Exception as e:
        print(f"Error starting GUI: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
