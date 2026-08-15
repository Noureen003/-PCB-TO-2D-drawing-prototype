# PCB Schematic to 2D Drawing — Option B (Netlist/JSON → 2D Layout)

## What I built

A dependency-free Python pipeline that takes a structured JSON description of
a PCB (a list of components plus a list of nets/connections between them) and
renders it as a 2D SVG drawing: each component is drawn as a labeled,
color-coded box, and each net is drawn as a dashed line connecting the
components it touches.

Pipeline: **JSON file → parse & validate → assign grid positions → render SVG**

## Why Option B instead of Option A (image → drawing)

Option A requires component detection from a raster schematic image, which
needs either a trained vision model or careful OpenCV heuristics (edge
detection, template matching) that are unreliable without a labeled dataset.
Option B lets me demonstrate a complete, correct, and honestly-evaluated
pipeline within the expected effort window, rather than a fragile image
pipeline with unpredictable accuracy. This is exactly the trade-off the
problem statement invites ("depth in one well-reasoned approach matters more
than attempting everything").

## Assumptions

- Input is a valid JSON file with a fixed schema: `components` (each with
  `id`, `type`, optional `value`) and `nets` (each with `name` and a
  `connects` list of component ids).
- Component placement uses a **simple grid layout, grouped by component
  type** (all resistors together, all ICs together, etc.). This is NOT true
  auto-placement / routing optimization — it prioritizes a clean, readable,
  and fully deterministic diagram over minimizing wire crossings.
- Nets are drawn as straight dashed lines chained through their connected
  components in the order listed, not as orthogonal PCB-style traces.
- Component types are matched to a small fixed color palette (resistor,
  capacitor, ic, led, connector); unrecognized types fall back to gray, so
  the system doesn't crash on new component types.

## How to run

No external dependencies are required — everything uses the Python standard
library only (`json`, plus plain string-built SVG).

```bash
# from the project root
python main.py samples/sample1_arduino.json output/sample1.svg
python main.py samples/sample2_motor_driver.json output/sample2.svg
python main.py samples/sample3_sensor_board.json output/sample3.svg
```

Open any `output/*.svg` file in a web browser to view the drawing.

## Sample runs included

| Input | Description | Components | Nets |
|---|---|---|---|
| `samples/sample1_arduino.json` | Simple microcontroller board (ATMEGA328P + reset + LED) | 7 | 4 |
| `samples/sample2_motor_driver.json` | H-bridge motor driver (L298N) | 8 | 6 |
| `samples/sample3_sensor_board.json` | Larger I2C sensor board (ESP32 + heart-rate sensor) | 12 | 6 |

## What works

- Full pipeline runs end-to-end from a single command on all 3 samples.
- Input validation catches malformed files early (missing fields, nets
  referencing unknown component ids) with clear error messages.
- Layout scales automatically — canvas size grows to fit however many
  components are given.
- Zero external dependencies — fully offline, no install step beyond Python 3.11+.

## What does not work / known limitations

- Placement is grid-based, not optimized — wires can cross each other
  visually on more densely connected designs (visible in `sample3`, which has
  several 4+ component nets like GND and 3V3).
- No real PCB semantics: no layer information, no trace width, no board
  outline, no design rule checking (DRC).
- Net lines are chained straight segments, not right-angle PCB-style traces.
- No image/OCR input path (Option A) is implemented.

## What I would improve with more time

- Force-directed or simulated-annealing placement to reduce wire crossings.
- Route nets as orthogonal (Manhattan-style) traces instead of straight lines,
  which is much closer to how real PCB layouts read visually.
- Add a board outline and mounting holes for a more realistic look.
- Support KiCad `.net` file parsing directly, so real EDA exports could be
  used as input instead of hand-written JSON.
