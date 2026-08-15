"""
parser.py

Loads a PCB design description (components + nets) from a JSON file and
validates that it is well-formed before anything downstream touches it.

Why validate here? If a net references a component ID that doesn't exist,
we want to fail loudly and clearly right at load time, not with a confusing
KeyError three modules later inside the drawing code.
"""

import json
from typing import Any


def load_design(path: str) -> dict[str, Any]:
    """Read a JSON design file from disk and return it as a dict."""
    with open(path, "r", encoding="utf-8") as f:
        design: dict[str, Any] = json.load(f)
    validate_design(design)
    return design


def validate_design(design: dict[str, Any]) -> None:
    """
    Check that the design dict has the shape we expect and that every
    net only refers to components that actually exist.

    Raises ValueError with a clear message if something is wrong.
    """
    if "components" not in design or "nets" not in design:
        raise ValueError("Design file must have 'components' and 'nets' keys.")

    component_ids = set()
    for comp in design["components"]:
        for required_field in ("id", "type"):
            if required_field not in comp:
                raise ValueError(f"Component missing required field '{required_field}': {comp}")
        if comp["id"] in component_ids:
            raise ValueError(f"Duplicate component id found: {comp['id']}")
        component_ids.add(comp["id"])

    for net in design["nets"]:
        if "name" not in net or "connects" not in net:
            raise ValueError(f"Net missing 'name' or 'connects' field: {net}")
        for comp_id in net["connects"]:
            if comp_id not in component_ids:
                raise ValueError(
                    f"Net '{net['name']}' references unknown component id '{comp_id}'. "
                    f"Known ids: {sorted(component_ids)}"
                )
