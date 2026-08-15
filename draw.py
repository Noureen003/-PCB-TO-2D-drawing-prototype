"""
draw.py

Turns (components + positions + nets) into an SVG file.

SVG is just XML text, so we don't need any external drawing library --
we build the file as a list of strings and join them at the end. This
keeps the project dependency-free, which matters for the "fully offline"
spirit of these evaluations.
"""

from typing import Any
from layout import assign_positions, canvas_size, BOX_WIDTH, BOX_HEIGHT

# One fill color per component type, so the diagram is easy to scan visually
TYPE_COLORS = {
    "resistor": "#FFD966",
    "capacitor": "#9FC5E8",
    "ic": "#B6D7A8",
    "led": "#EA9999",
    "connector": "#D5A6BD",
}
DEFAULT_COLOR = "#CCCCCC"


def draw_design(design: dict[str, Any], output_path: str) -> None:
    """
    Render the given design dict to an SVG file at output_path.

    design must already be validated (see parser.validate_design).
    """
    positions = assign_positions(design["components"])
    width, height = canvas_size(positions)

    svg_parts: list[str] = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Arial, sans-serif">'
    )
    svg_parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')

    # --- draw net connections first, so component boxes sit on top of the wires ---
    for net in design["nets"]:
        svg_parts.append(_draw_net(net, positions))

    # --- draw components on top ---
    for comp in design["components"]:
        svg_parts.append(_draw_component(comp, positions[comp["id"]]))

    svg_parts.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))


def _center(pos: tuple[int, int]) -> tuple[int, int]:
    """Return the center point of a component box, used for drawing wires."""
    x, y = pos
    return (x + BOX_WIDTH // 2, y + BOX_HEIGHT // 2)


def _draw_component(comp: dict[str, Any], pos: tuple[int, int]) -> str:
    """Return SVG markup for a single component: a labeled rectangle."""
    x, y = pos
    color = TYPE_COLORS.get(comp["type"], DEFAULT_COLOR)
    label = comp["id"]
    value = comp.get("value", "")

    rect = (
        f'<rect x="{x}" y="{y}" width="{BOX_WIDTH}" height="{BOX_HEIGHT}" '
        f'fill="{color}" stroke="black" stroke-width="1.5" rx="4"/>'
    )
    id_text = f'<text x="{x + BOX_WIDTH / 2}" y="{y + 17}" font-size="12" font-weight="bold" text-anchor="middle">{label}</text>'
    value_text = f'<text x="{x + BOX_WIDTH / 2}" y="{y + 31}" font-size="10" text-anchor="middle">{value}</text>'
    return rect + "\n" + id_text + "\n" + value_text


def _draw_net(net: dict[str, Any], positions: dict[str, tuple[int, int]]) -> str:
    """
    Return SVG markup for one net: a small colored dot at each connected
    component's center, chained together with straight lines, plus a
    label near the first point naming the net (e.g. 'VCC', 'GND').
    """
    ids = net["connects"]
    if len(ids) < 2:
        return ""  # nothing to draw for a net with fewer than 2 endpoints

    points = [_center(positions[i]) for i in ids]
    lines = []
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#CC0000" stroke-width="1.5" stroke-dasharray="4,2"/>'
        )
    label_x, label_y = points[0]
    label = f'<text x="{label_x + 6}" y="{label_y - 6}" font-size="9" fill="#CC0000">{net["name"]}</text>'
    return "\n".join(lines) + "\n" + label
