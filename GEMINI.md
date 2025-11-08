# Project: PDF Handwriting Sheet Generator

This document outlines the requirements for a tool that generates primary ruled (handwriting) paper in PDF format with custom text.

## Core Features

1.  **Generate Ruled Paper:** Programmatically generate a PDF document with primary ruled lines (top line, dashed midline, baseline). **There must be a vertical gap between the baseline of one ruled set and the top line of the set directly below it.**
2.  **Text Input:** Accept a string of text (sentences) as input.
3.  **Baseline Alignment:** Render the input text onto the ruled lines, adhering to the following rules:
    * Text must be correctly aligned with the **baseline**.
    * **The top of standard lowercase letters (x-height, e.g., 'a', 'c', 'x') must align with the dashed midline.**
    * Ascenders (e.g., 'b', 'd', 'h') should generally reach the **top line**.
    * Descenders (e.g., 'g', 'p', 'y') must drop **below the baseline**.
    * Text should flow to the next line as needed.
4.  **Font Customization:** Allow the user to specify the font (e.g., provide a `.ttf` file path) used for rendering the text.
5.  **Line Sizing:** Allow the user to change the size and spacing of the rule lines (e.g., the distance between the baseline and the midline).
6.  **PDF Output:** The final result must be saved as a PDF file.

## Development Environment

* **Language:** Python
* **Environment:** The project must be developed using a Python virtual environment (`venv`) to manage dependencies.