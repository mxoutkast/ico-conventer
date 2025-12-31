# Quick Spec: Make 256 Pixels the Default Output Size

## Overview
Change the default icon size from multiple sizes (16, 32, 48, 64, 128, 256) to a single default size of 256 pixels. This simplifies the default behavior while still allowing users to specify custom sizes when needed.

## Workflow Type
Feature - A configuration change that modifies default behavior of the ICO converter tool.

## Task Scope
This task involves modifying the `ico_converter.py` file to:
- Update the `--sizes` argument default value from `[16, 32, 48, 64, 128, 256]` to `[256]`
- Optionally update the `DEFAULT_SIZES` constant for consistency

The change is localized to configuration defaults and does not affect the core conversion logic.

## Success Criteria
- The help text (`python ico_converter.py --help`) shows default size as 256
- Running with `--dry-run` flag displays "Icon sizes: 256x256"
- Custom sizes can still be specified using the `--sizes` flag
- The application runs without errors after the changes

## Task
Change the default icon size from multiple sizes (16, 32, 48, 64, 128, 256) to a single default size of 256 pixels.

## Files to Modify
- `ico_converter.py` - Update the default size argument in argparse

## Change Details
Change the `--sizes` argument default from `[16, 32, 48, 64, 128, 256]` to `[256]` on line 168. This will make 256x256 the only default size when users don't specify custom sizes.

Optionally update `DEFAULT_SIZES` constant on line 12 to `[(256, 256)]` for consistency.

## Verification
- [ ] Run `python ico_converter.py --help` and verify the help text shows default: 256
- [ ] Run `python ico_converter.py test.png --dry-run` and verify it shows "Icon sizes: 256x256"
- [ ] Test that custom sizes still work with `--sizes 16 32 48`

## Notes
- The `DEFAULT_SIZES` constant is not used in the actual argparse default, but updating it maintains consistency
- Users can still specify multiple sizes with `--sizes` flag if needed
