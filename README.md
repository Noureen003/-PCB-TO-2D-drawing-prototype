# PCB Schematic to 2D Drawing

This project takes a JSON file containing PCB components and their connections and converts it into a simple **2D SVG drawing**.

For example, the input can contain components like resistors, capacitors, ICs, LEDs, and connectors, along with the nets connecting them.

The program reads the JSON, checks the data, places the components on a grid, and draws the connections between them.

### How It Works

1. Read the PCB details from a JSON file.
2. Check the components and connections.
3. Place the components in a simple grid based on their type.
4. Draw each component as a labeled box.
5. Draw the connections between components as dashed lines.
6. Save the final drawing as an SVG file.

### How to Run

No external libraries are required. It uses Python's standard library.

```bash
python main.py samples/sample1_arduino.json output/sample1.svg
```

Other examples:

```bash
python main.py samples/sample2_motor_driver.json output/sample2.svg
python main.py samples/sample3_sensor_board.json output/sample3.svg
```

Open the generated `.svg` file in any web browser to view the drawing.

### Examples

The `samples/` folder contains three example PCB designs:

* `sample1_arduino.json` – simple Arduino/microcontroller board
* `sample2_motor_driver.json` – motor driver circuit
* `sample3_sensor_board.json` – sensor board with ESP32

### Project Files

* `main.py` – runs the complete process
* `samples/` – sample JSON input files
* `output/` – generated SVG drawings

The project uses **Option B (JSON/Netlist → 2D Drawing)** instead of image-based schematic detection. This keeps the implementation simple, reliable, and easy to test.

