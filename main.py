import matplotlib
matplotlib.use('Qt5Agg')

import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpinBox,
    QMenuBar, QMenu, QAction, QFileDialog, QTabWidget,
    QTableView
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        if role == Qt.BackgroundRole and index.row() % 2 == 0:
            return QColor('#f0f0f0')
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
    
    def plot_data(self, data=None):
        self.axes.clear()
        if data is not None and not data.empty:
            # If we have exactly two columns, use them as x and y
            if len(data.columns) == 2:
                x = data.iloc[:, 0]
                y = data.iloc[:, 1]
                self.axes.plot(x, y)
                self.axes.set_xlabel(data.columns[0])
                self.axes.set_ylabel(data.columns[1])
            # Otherwise plot each column as a separate line
            else:
                for column in data.columns:
                    if pd.api.types.is_numeric_dtype(data[column]):
                        self.axes.plot(data[column], label=column)
                self.axes.legend()
        else:
            # Default plot if no data
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            self.axes.plot(x, y)
        self.axes.set_title('Plot View')
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlotGenie")
        self.setGeometry(100, 100, 1000, 800)
        
        # Initialize data
        self.data = pd.DataFrame()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create Plot tab
        plot_tab = QWidget()
        plot_layout = QVBoxLayout(plot_tab)  # Changed to QVBoxLayout for toolbar
        
        # Create horizontal layout for controls and plot
        plot_content = QWidget()
        plot_content_layout = QHBoxLayout(plot_content)
        
        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Add controls
        plot_button = QPushButton("Update Plot")
        plot_button.clicked.connect(self.update_plot)
        
        points_label = QLabel("Number of Points:")
        self.points_spin = QSpinBox()
        self.points_spin.setRange(10, 1000)
        self.points_spin.setValue(100)
        
        left_layout.addWidget(plot_button)
        left_layout.addWidget(points_label)
        left_layout.addWidget(self.points_spin)
        left_layout.addStretch()
        
        # Create the plotting canvas
        self.plot_canvas = PlotCanvas(self)
        
        # Create the navigation toolbar
        self.toolbar = NavigationToolbar(self.plot_canvas, self)
        
        # Add toolbar to plot layout
        plot_layout.addWidget(self.toolbar)
        
        # Add widgets to plot content layout
        plot_content_layout.addWidget(left_panel, stretch=1)
        plot_content_layout.addWidget(self.plot_canvas, stretch=4)
        
        # Add plot content to main plot layout
        plot_layout.addWidget(plot_content)
        
        # Create Data tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        self.table_view = QTableView()
        data_layout.addWidget(self.table_view)
        
        # Add tabs
        self.tabs.addTab(plot_tab, "Plot View")
        self.tabs.addTab(data_tab, "Data View")
        
        # Add tabs to main layout
        layout.addWidget(self.tabs)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Load data action
        load_action = QAction('Load Data', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)
        
        # Save plot action
        save_action = QAction('Save Plot', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_plot)
        file_menu.addAction(save_action)
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data File",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;All Files (*.*)"
        )
        if file_path:
            try:
                if file_path.endswith(('.xlsx', '.xls')):
                    self.data = pd.read_excel(file_path)
                else:
                    self.data = pd.read_csv(file_path)
                
                # Update table view
                model = PandasModel(self.data)
                self.table_view.setModel(model)
                
                # Update plot
                self.plot_canvas.plot_data(self.data)
                
                # Switch to plot tab
                self.tabs.setCurrentIndex(0)
            except Exception as e:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")
    
    def save_plot(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Plot",
            "",
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*.*)"
        )
        if file_path:
            self.plot_canvas.figure.savefig(file_path, bbox_inches='tight', dpi=300)
    
    def update_plot(self):
        if not self.data.empty:
            self.plot_canvas.plot_data(self.data)
        else:
            self.plot_canvas.axes.clear()
            num_points = self.points_spin.value()
            x = np.linspace(0, 10, num_points)
            y = np.sin(x)
            self.plot_canvas.axes.plot(x, y)
            self.plot_canvas.axes.set_title('Sample Plot')
            self.plot_canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
