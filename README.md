# PlotGenie

A PyQt-based plotting application that provides an interactive interface for data visualization using Matplotlib.

## Features
- Interactive Matplotlib plotting with zoom, pan, and navigation controls
- Data table view for spreadsheet-like data inspection
- File loading support for CSV and Excel files
- Plot saving in multiple formats (PNG, PDF, SVG)
- Modern PyQt5-based user interface
- Real-time plot updates

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
4. Use the navigation toolbar to:
   - Zoom: Click the magnifying glass and drag to zoom
   - Pan: Click the hand icon to pan around
   - Reset: Click the home icon to reset the view
   - Save: Save the current plot as an image
5. Adjust the number of points and click "Update Plot" to modify the demo plot

## Requirements
- Python 3.10+
- PyQt5
- Matplotlib
- NumPy
- Pandas
