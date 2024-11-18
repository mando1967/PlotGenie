# PlotGenie

A PyQt-based plotting application that provides an interactive interface for mathematical equation plotting and data visualization using Matplotlib.

## Features
- Interactive Matplotlib plotting with zoom, pan, and navigation controls
- Mathematical equation plotting with LaTeX-formatted titles
- Support for advanced mathematical functions:
  - Trigonometric: sin, cos, tan
  - Inverse trigonometric: arcsin, arccos, arctan
  - Hyperbolic: sinh, cosh, tanh
  - Exponential and logarithmic: exp, log
  - Square root and power functions
  - Absolute value
- Customizable equation input with font selection
- Data table view for spreadsheet-like data inspection
- File loading support for CSV and Excel files
- Plot saving in multiple formats (PNG, PDF, SVG)
- Modern, streamlined PyQt5-based user interface
- Real-time plot updates
- Grid display and axis labels
- Comprehensive error handling with user-friendly messages

## Installation

1. Create a Conda environment:
```bash
conda create -n plotgenie python=3.10
conda activate plotgenie
```

2. Install dependencies:
```bash
conda install pyqt matplotlib numpy pandas
```

## Running the Application

```bash
python main.py
```

## Usage

1. Launch the application using the command above
2. Use File -> Load Data to open CSV or Excel files
3. Switch between Plot View and Data View tabs
4. Enter mathematical equations in the input field at the bottom of the Plot tab
   - Example equations:
     * sin(x) + cos(x)
     * exp(-x**2)
     * sqrt(abs(x))
     * sinh(x) + tanh(x)
5. Right-click the equation input field to:
   - Change font size
   - Select font family
   - Access standard edit operations (cut, copy, paste)
6. Use the navigation toolbar to:
   - Zoom: Click the magnifying glass and drag to zoom
   - Pan: Click the hand icon to pan around
   - Reset: Click the home icon to reset the view
   - Save: Save the current plot as an image

## Requirements
- Python 3.10+
- PyQt5
- Matplotlib
- NumPy
- Pandas
