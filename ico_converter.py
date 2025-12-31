#!/usr/bin/env python3
"""
PNG to ICO Converter - CLI tool for batch converting PNG images to ICO format with multiple sizes
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple
from PIL import Image


# Standard icon sizes for Windows ICO files
DEFAULT_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def collect_files(inputs: List[str], recursive: bool = False) -> List[Path]:
    """
    Collect all PNG files from various input types (files, directories, wildcards).
    
    Args:
        inputs: List of file paths, directory paths, or glob patterns
        recursive: If True, search directories recursively
    
    Returns:
        List of Path objects pointing to PNG files
    """
    files = []
    
    for input_str in inputs:
        input_path = Path(input_str)
        
        # Direct file
        if input_path.is_file():
            if input_path.suffix.lower() in ['.png']:
                files.append(input_path)
            else:
                print(f"Warning: Skipping non-PNG file: {input_path}")
        
        # Directory
        elif input_path.is_dir():
            pattern = '**/*.png' if recursive else '*.png'
            png_files = list(input_path.glob(pattern))
            files.extend(png_files)
            if not png_files:
                print(f"Warning: No PNG files found in directory: {input_path}")
        
        # Glob pattern or non-existent path
        else:
            # Try as glob pattern
            matched = list(Path('.').glob(str(input_path)))
            png_matched = [f for f in matched if f.suffix.lower() == '.png']
            
            if png_matched:
                files.extend(png_matched)
            else:
                print(f"Warning: No files found matching pattern: {input_path}")
    
    # Remove duplicates and sort
    return sorted(list(set(files)))


def convert_png_to_ico(
    input_path: Path,
    output_path: Path,
    sizes: List[Tuple[int, int]],
    verbose: bool = False
) -> bool:
    """
    Convert a PNG image to ICO format with multiple sizes.
    
    Args:
        input_path: Path to input PNG file
        output_path: Path to output ICO file
        sizes: List of (width, height) tuples for icon sizes
        verbose: If True, print detailed information
    
    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        with Image.open(input_path) as img:
            # Get original dimensions
            original_size = img.size
            
            if verbose:
                print(f"  Original size: {original_size[0]}x{original_size[1]}")
                print(f"  Mode: {img.mode}")
            
            # Convert to RGBA if needed (ICO supports transparency)
            if img.mode != 'RGBA':
                if verbose:
                    print(f"  Converting from {img.mode} to RGBA")
                img = img.convert('RGBA')
            
            # Validate minimum size
            max_size = max(s[0] for s in sizes)
            if original_size[0] < max_size or original_size[1] < max_size:
                print(f"Warning: {input_path.name} ({original_size[0]}x{original_size[1]}) "
                      f"is smaller than largest icon size ({max_size}x{max_size})")
            
            # Save as ICO with multiple sizes
            if verbose:
                size_list = ', '.join(f"{w}x{h}" for w, h in sizes)
                print(f"  Generating sizes: {size_list}")
            
            img.save(output_path, format='ICO', sizes=sizes)
            
            if verbose:
                output_size = output_path.stat().st_size
                print(f"  Output size: {output_size / 1024:.1f} KB")
            
            return True
            
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
        return False
    except Exception as e:
        print(f"Error converting {input_path.name}: {e}")
        return False


def parse_sizes(size_args: List[int]) -> List[Tuple[int, int]]:
    """
    Parse size arguments into list of (width, height) tuples.
    Assumes square icons.
    
    Args:
        size_args: List of integer sizes
    
    Returns:
        List of (size, size) tuples
    """
    return [(size, size) for size in sorted(set(size_args))]


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description='Convert PNG images to ICO format with multiple embedded sizes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.png                    # Convert single file (output: image.ico in same dir)
  %(prog)s *.png                        # Convert all PNGs in current directory
  %(prog)s images/                      # Convert all PNGs in a directory
  %(prog)s images/ -r                   # Convert recursively
  %(prog)s image.png -o icons/          # Save to different directory
  %(prog)s *.png -o ./output/           # Batch convert to output folder
  %(prog)s image.png --sizes 16 32 48   # Custom icon sizes
  %(prog)s *.png --dry-run              # Preview without converting
        """
    )
    
    parser.add_argument(
        'inputs',
        nargs='+',
        help='Input PNG files, directories, or glob patterns'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        help='Output directory. If not specified, ICO files are saved in the same directory as their source PNG files'
    )
    
    parser.add_argument(
        '--sizes',
        nargs='+',
        type=int,
        default=[256],
        help='Icon sizes to include (default: 256)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing ICO files without prompting'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be converted without actually converting'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed information during conversion'
    )
    
    parser.add_argument(
        '--suffix',
        type=str,
        default='',
        help='Suffix to add to output filenames (e.g., "_icon")'
    )
    
    args = parser.parse_args()
    
    # Collect all PNG files
    print("Collecting PNG files...")
    png_files = collect_files(args.inputs, args.recursive)
    
    if not png_files:
        print("Error: No PNG files found")
        return 1
    
    print(f"Found {len(png_files)} PNG file(s)")
    
    # Parse sizes
    sizes = parse_sizes(args.sizes)
    if args.verbose or args.dry_run:
        size_list = ', '.join(f"{w}x{h}" for w, h in sizes)
        print(f"Icon sizes: {size_list}")
    
    # Setup output directory
    output_dir = Path(args.output_dir) if args.output_dir else None
    if output_dir:
        if not args.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_dir}")
    
    # Process files
    print()
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, png_file in enumerate(png_files, 1):
        # Determine output path
        if output_dir:
            output_path = output_dir / f"{png_file.stem}{args.suffix}.ico"
        else:
            output_path = png_file.parent / f"{png_file.stem}{args.suffix}.ico"
        
        # Check if output already exists
        if output_path.exists() and not args.overwrite and not args.dry_run:
            print(f"[{i}/{len(png_files)}] Skipping {png_file.name} (output exists: {output_path.name})")
            skip_count += 1
            continue
        
        print(f"[{i}/{len(png_files)}] {png_file.name} -> {output_path.name}")
        
        if args.dry_run:
            success_count += 1
            continue
        
        # Convert
        if convert_png_to_ico(png_file, output_path, sizes, args.verbose):
            success_count += 1
        else:
            error_count += 1
    
    # Summary
    print()
    print("=" * 50)
    if args.dry_run:
        print(f"DRY RUN: Would convert {success_count} file(s)")
    else:
        print(f"Conversion complete!")
        print(f"  Success: {success_count}")
        if skip_count > 0:
            print(f"  Skipped: {skip_count}")
        if error_count > 0:
            print(f"  Errors:  {error_count}")
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
