#!/usr/bin/env python3
"""
PNG to ICO Converter - CLI tool for batch converting PNG images to ICO format with multiple sizes
Also supports conversion to other formats (JPEG, WEBP, PNG).
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image


# Standard icon sizes for Windows ICO files
DEFAULT_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
SUPPORTED_FORMATS = ['ICO', 'PNG', 'JPEG', 'WEBP']


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


def convert_image(
    input_path: Path,
    output_path: Path,
    format: str = 'ICO',
    sizes: Optional[List[Tuple[int, int]]] = None,
    verbose: bool = False
) -> bool:
    """
    Convert a PNG image to the specified format.
    
    Args:
        input_path: Path to input PNG file
        output_path: Path to output file
        format: Output format ('ICO', 'PNG', 'JPEG', 'WEBP')
        sizes: List of (width, height) tuples (only used for ICO)
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
            
            format = format.upper()
            if format not in SUPPORTED_FORMATS:
                print(f"Error: Unsupported format: {format}")
                return False

            # Format specific handling
            if format == 'ICO':
                # Convert to RGBA if needed (ICO supports transparency)
                if img.mode != 'RGBA':
                    if verbose:
                        print(f"  Converting from {img.mode} to RGBA")
                    img = img.convert('RGBA')

                # Use default sizes if none provided
                target_sizes = sizes if sizes else DEFAULT_SIZES

                # Validate minimum size
                max_size = max(s[0] for s in target_sizes)
                if original_size[0] < max_size or original_size[1] < max_size:
                    print(f"Warning: {input_path.name} ({original_size[0]}x{original_size[1]}) "
                          f"is smaller than largest icon size ({max_size}x{max_size})")

                if verbose:
                    size_list = ', '.join(f"{w}x{h}" for w, h in target_sizes)
                    print(f"  Generating sizes: {size_list}")

                img.save(output_path, format='ICO', sizes=target_sizes)

            elif format == 'JPEG':
                # JPEG does not support transparency
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    if verbose:
                        print(f"  Converting from {img.mode} to RGB (handling transparency)")
                    # Create white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    # Handle P mode transparency
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                img.save(output_path, format='JPEG', quality=90)

            else: # PNG, WEBP
                # These formats support transparency, just ensure compatible mode if needed
                # WEBP supports RGBA. PNG supports RGBA.
                img.save(output_path, format=format)
            
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


def convert_png_to_ico(
    input_path: Path,
    output_path: Path,
    sizes: List[Tuple[int, int]],
    verbose: bool = False
) -> bool:
    """
    Wrapper for backward compatibility.
    """
    return convert_image(input_path, output_path, format='ICO', sizes=sizes, verbose=verbose)


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
        description='Convert PNG images to ICO or other formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.png                    # Convert single file (output: image.ico in same dir)
  %(prog)s *.png                        # Convert all PNGs in current directory
  %(prog)s image.png --format JPEG      # Convert to JPEG
  %(prog)s image.png --sizes 16 32 48   # Custom icon sizes (ICO only)
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
        help='Output directory. If not specified, output files are saved in the same directory as their source PNG files'
    )

    parser.add_argument(
        '-f', '--format',
        type=str,
        default='ICO',
        choices=SUPPORTED_FORMATS,
        help='Output format (default: ICO)'
    )
    
    parser.add_argument(
        '--sizes',
        nargs='+',
        type=int,
        default=[16, 32, 48, 64, 128, 256],
        help='Icon sizes to include (ICO only, default: 16 32 48 64 128 256)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files without prompting'
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
    format = args.format.upper()

    if args.verbose or args.dry_run:
        print(f"Output format: {format}")
        if format == 'ICO':
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
    
    # Extension mapping
    extensions = {
        'ICO': '.ico',
        'PNG': '.png',
        'JPEG': '.jpg',
        'WEBP': '.webp'
    }
    ext = extensions.get(format, '.ico')

    for i, png_file in enumerate(png_files, 1):
        # Determine output path
        if output_dir:
            output_path = output_dir / f"{png_file.stem}{args.suffix}{ext}"
        else:
            output_path = png_file.parent / f"{png_file.stem}{args.suffix}{ext}"
        
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
        if convert_image(png_file, output_path, format=format, sizes=sizes, verbose=args.verbose):
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
