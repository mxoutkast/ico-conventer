#!/usr/bin/env python3
"""
PNG to ICO Converter - GUI wrapper with drag-and-drop functionality
"""

import sys
from pathlib import Path
from typing import List, Tuple
import tkinter as tk
from tkinter import ttk, filedialog

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("Error: tkinterdnd2 is required. Install it with: pip install tkinterdnd2")
    sys.exit(1)


# Standard icon sizes for Windows ICO files
DEFAULT_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


class IcoConverterGUI:
    """Main GUI application for PNG to ICO converter with drag-and-drop support."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("PNG to ICO Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # State variables
        self.files: List[Path] = []
        self.output_dir: Path = Path.cwd()
        self.selected_sizes: List[Tuple[int, int]] = DEFAULT_SIZES.copy()
        self.converting = False
        
        # Setup drag-and-drop
        self._setup_drag_drop()
        
        # Create UI
        self._create_widgets()
    
    def _setup_drag_drop(self) -> None:
        """
        Setup drag-and-drop functionality for the root window.
        """
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self._on_drop)
        except Exception as e:
            print(f"Warning: Could not initialize drag-and-drop: {e}")
    
    def _create_widgets(self) -> None:
        """
        Create and layout all GUI widgets.
        """
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="PNG to ICO Converter",
            font=('TkDefaultFont', 14, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Drag and drop PNG files here, or click 'Add Files' to select files",
            foreground='gray'
        )
        instructions.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # File list frame
        file_list_frame = ttk.LabelFrame(main_frame, text="Files to Convert", padding="5")
        file_list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_list_frame.columnconfigure(0, weight=1)
        file_list_frame.rowconfigure(0, weight=1)
        
        # File list with scrollbar
        scrollbar = ttk.Scrollbar(file_list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.file_list = tk.Listbox(
            file_list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED
        )
        self.file_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_list.yview)
        
        # File buttons
        button_frame = ttk.Frame(file_list_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        add_button = ttk.Button(button_frame, text="Add Files", command=self._add_files_dialog)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = ttk.Button(button_frame, text="Clear All", command=self._clear_files)
        clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_button = ttk.Button(button_frame, text="Remove Selected", command=self._remove_selected)
        remove_button.pack(side=tk.LEFT)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        
        output_dir_frame = ttk.Frame(options_frame)
        output_dir_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        output_dir_frame.columnconfigure(0, weight=1)
        
        self.output_dir_var = tk.StringVar(value=str(self.output_dir))
        output_dir_entry = ttk.Entry(output_dir_frame, textvariable=self.output_dir_var)
        output_dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_button = ttk.Button(output_dir_frame, text="Browse...", command=self._browse_output_dir)
        browse_button.grid(row=0, column=1)
        
        # Size selection
        ttk.Label(options_frame, text="Icon Sizes:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        size_frame = ttk.Frame(options_frame)
        size_frame.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        self.size_vars = {}
        for i, size in enumerate(DEFAULT_SIZES):
            size_str = f"{size[0]}x{size[1]}"
            var = tk.BooleanVar(value=True)
            self.size_vars[size] = var
            checkbox = ttk.Checkbutton(size_frame, text=size_str, variable=var)
            checkbox.grid(row=0, column=i, padx=2)
        
        # Convert button
        convert_button = ttk.Button(
            main_frame,
            text="Convert to ICO",
            command=self._convert_files,
            style='Accent.TButton'
        )
        convert_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def _on_drop(self, event) -> None:
        """
        Handle drag-and-drop file drop events.
        
        Args:
            event: The drop event containing file paths
        """
        if self.converting:
            self.status_var.set("Cannot add files while converting")
            return
        
        # Parse dropped files
        files = self.root.tk.splitlist(event.data)
        self._add_files(files)
    
    def _add_files_dialog(self) -> None:
        """Open file dialog to select PNG files."""
        if self.converting:
            self.status_var.set("Cannot add files while converting")
            return
        
        files = filedialog.askopenfilenames(
            title="Select PNG Files",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        
        if files:
            self._add_files(files)
    
    def _add_files(self, file_paths: List[str]) -> None:
        """
        Add files to the conversion list.
        
        Args:
            file_paths: List of file paths to add
        """
        added_count = 0
        for file_path in file_paths:
            path = Path(file_path)
            
            # Check if it's a PNG file
            if path.suffix.lower() != '.png':
                self.status_var.set(f"Skipped {path.name}: Not a PNG file")
                continue
            
            # Check for duplicates
            if path not in self.files:
                self.files.append(path)
                self.file_list.insert(tk.END, path.name)
                added_count += 1
        
        if added_count > 0:
            self.status_var.set(f"Added {added_count} file(s)")
        else:
            self.status_var.set("No new files added")
    
    def _clear_files(self) -> None:
        """Clear all files from the list."""
        if self.converting:
            self.status_var.set("Cannot clear files while converting")
            return
        
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.status_var.set("Cleared all files")
    
    def _remove_selected(self) -> None:
        """Remove selected files from the list."""
        if self.converting:
            self.status_var.set("Cannot remove files while converting")
            return
        
        selection = self.file_list.curselection()
        if not selection:
            return
        
        # Remove in reverse order to maintain indices
        for index in reversed(selection):
            self.file_list.delete(index)
            del self.files[index]
        
        self.status_var.set(f"Removed {len(selection)} file(s)")
    
    def _browse_output_dir(self) -> None:
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=str(self.output_dir)
        )
        
        if directory:
            self.output_dir = Path(directory)
            self.output_dir_var.set(str(self.output_dir))
            self.status_var.set(f"Output directory: {self.output_dir}")
    
    def _convert_files(self) -> None:
        """
        Convert all files in the list to ICO format.
        This is a placeholder for now - will be implemented in later subtasks.
        """
        if not self.files:
            self.status_var.set("No files to convert")
            return
        
        # Update selected sizes
        self.selected_sizes = [size for size, var in self.size_vars.items() if var.get()]
        
        if not self.selected_sizes:
            self.status_var.set("Please select at least one icon size")
            return
        
        self.status_var.set(f"Conversion will be implemented in next subtask. {len(self.files)} file(s) ready.")


def main():
    """Main entry point for the GUI application."""
    try:
        # Create root window with DnD support
        root = TkinterDnD.Tk()
        
        # Create application
        app = IcoConverterGUI(root)
        
        # Start main loop
        root.mainloop()
        
        return 0
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
