#!/usr/bin/env python3
"""
PNG to ICO Converter - GUI wrapper with drag-and-drop functionality
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from typing import List, Optional

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    print("Error: tkinterdnd2 is required for drag-and-drop functionality")
    print("Install it with: pip install tkinterdnd2")
    sys.exit(1)


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
        
        # Initialize drag-and-drop
        self._setup_drag_drop()
        
        # Setup UI components
        self._setup_ui()
        
        # State variables
        self.dropped_files: List[Path] = []
        self.output_dir: Optional[Path] = None
        self.selected_sizes: List[tuple] = DEFAULT_SIZES.copy()
    
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
        
        # Drop zone frame
        drop_zone = ttk.LabelFrame(
            main_frame,
            text="Drop Zone",
            padding="10"
        )
        drop_zone.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        drop_zone.columnconfigure(0, weight=1)
        drop_zone.rowconfigure(0, weight=1)
        
        # File list (Treeview)
        self.file_list = ttk.Treeview(
            drop_zone,
            columns=('filename', 'status'),
            show='headings',
            selectmode='extended'
        )
        self.file_list.heading('filename', text='Filename')
        self.file_list.heading('status', text='Status')
        self.file_list.column('filename', width=400)
        self.file_list.column('status', width=100)
        self.file_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for file list
        scrollbar = ttk.Scrollbar(
            drop_zone,
            orient=tk.VERTICAL,
            command=self.file_list.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_list.configure(yscrollcommand=scrollbar.set)
        
        # Configure drag-and-drop for drop zone
        self._setup_drop_zone_drag_drop(drop_zone)
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="Clear List",
            command=self._clear_file_list
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
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
        progress_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=5, column=0, sticky=(tk.W, tk.E))
    
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
            for file_path in file_paths:
                path = Path(file_path)
                if path.is_file() and path.suffix.lower() == '.png':
                    if path not in self.dropped_files:
                        self.dropped_files.append(path)
                        self._add_file_to_list(path)
                        added_count += 1
            
            # Update status
            if added_count > 0:
                self._update_status(f"Added {added_count} file(s) to list")
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
        self.file_list.insert('', tk.END, values=(file_path.name, 'Pending'))
    
    def _clear_file_list(self) -> None:
        """Clear all files from the list."""
        self.dropped_files.clear()
        self.file_list.delete(*self.file_list.get_children())
        self.progress_var.set(0)
        self._update_status("List cleared")
    
    def _convert_files(self) -> None:
        """Start the conversion process for all files in the list."""
        if not self.dropped_files:
            self._update_status("No files to convert")
            return
        
        self._update_status("Conversion not yet implemented")
    
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
