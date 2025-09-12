#!/usr/bin/env python3
"""
ASCII Art Generator

A Fun Little Project That I Made While Sitting in NEOC, During the Seat Heating Session. 

Converts JPG/PNG images to ASCII art.

Usage examples:
  - Basic (prints to console):
      python ascii_art.py -i path/to/image.jpg
  - Custom width and y-scale (character aspect ratio correction):
      python ascii_art.py -i input.png -w 120 -s 0.5
  - Invert brightness mapping (bright => dark chars):
      python ascii_art.py -i input.png --invert
  - Save to file:
      python ascii_art.py -i input.png -o output.txt
  - Custom gradient string (from darkest to lightest):
      python ascii_art.py -i input.png --gradient "@%#*+=-:. "

Notes:
  - y-scale compensates for the fact that terminal characters are taller than they are wide.
    Typical values: 0.4 to 0.6. Adjust to taste based on your font.
  - Works with most image formats supported by Pillow (e.g., JPG, PNG).
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

try:
    from PIL import Image
except Exception:  # pragma: no cover - handled at runtime
    print(
        "Error: Pillow (PIL) is not installed. Install it with:\n"
        "  python -m pip install pillow\n"
        "or on Windows (if 'python' is not recognized):\n"
        "  py -m pip install pillow",
        file=sys.stderr,
    )
    sys.exit(1)


DEFAULT_GRADIENT = "@%#*+=-:. "  # darkest -> lightest


def image_to_ascii(
    image_path: str,
    width: int = 100,
    y_scale: float = 0.5,
    invert: bool = False,
    gradient: Optional[str] = None,
) -> str:
    """Convert an image to an ASCII art string.

    Args:
        image_path: Path to the input image.
        width: Output character width.
        y_scale: Vertical scale factor to correct for character aspect ratio.
        invert: If True, invert the brightness mapping.
        gradient: String of characters from darkest to lightest.

    Returns:
        A string containing the ASCII art with newline-separated rows.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    gradient = (gradient if gradient is not None else DEFAULT_GRADIENT)
    if len(gradient) < 2:
        raise ValueError("Gradient must contain at least 2 characters.")


    if invert:
        gradient = gradient[::-1]


    with Image.open(image_path) as img:
        img = img.convert("L") 
        orig_w, orig_h = img.size
        if orig_w == 0 or orig_h == 0:
            raise ValueError("Image has invalid dimensions (0).")


        new_h = max(1, int(orig_h * (width / orig_w) * y_scale))
        img = img.resize((width, new_h))

        pixels = img.getdata() 


    n = len(gradient)

    chars = [gradient[p * (n - 1) // 255] for p in pixels]


    lines = ["".join(chars[i : i + width]) for i in range(0, len(chars), width)]
    return "\n".join(lines)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input image (jpg/png/etc.)"
    )
    parser.add_argument(
        "-w", "--width", type=int, default=100, help="Output width in characters (default: 100)"
    )
    parser.add_argument(
        "-s",
        "--y-scale",
        type=float,
        default=0.5,
        help="Vertical scale factor to compensate for character aspect ratio (default: 0.5)",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert brightness mapping (bright pixels use darker characters)",
    )
    parser.add_argument(
        "--gradient",
        type=str,
        default=None,
        help="Custom gradient string from darkest to lightest (e.g. '@%#*+=-:. ')",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Write ASCII art to this file"
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    try:
        ascii_art = image_to_ascii(
            image_path=args.input,
            width=args.width,
            y_scale=args.y_scale,
            invert=args.invert,
            gradient=args.gradient,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(ascii_art)
            print(f"ASCII art written to: {args.output}")
        except Exception as e:
            print(f"Failed to write output file: {e}", file=sys.stderr)
            return 1
    else:
        print(ascii_art)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
