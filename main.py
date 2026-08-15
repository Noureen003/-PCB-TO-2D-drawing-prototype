"""
main.py

Single entry point for the pipeline: JSON design file -> validated data ->
2D SVG drawing.

Usage:
    python main.py samples/sample1_arduino.json output/sample1.svg
"""

import sys
from parser import load_design
from draw import draw_design


def run(input_path: str, output_path: str) -> None:
    """Load, validate, and render one design file to an SVG output file."""
    design = load_design(input_path)
    draw_design(design, output_path)
    n_components = len(design["components"])
    n_nets = len(design["nets"])
    print(f"OK: {input_path} -> {output_path}  ({n_components} components, {n_nets} nets)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_design.json> <output_drawing.svg>")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
