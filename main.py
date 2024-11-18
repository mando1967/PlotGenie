import matplotlib
matplotlib.use('Qt5Agg')

import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpinBox,
    QMenuBar, QMenu, QAction, QFileDialog, QTabWidget,
    QTableView, QSizePolicy, QLineEdit, QFontDialog
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QColor, QFont
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

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Set default font
        self.setFont(QFont("Arial", 10))

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        
        # Font submenu
        font_menu = QMenu("Font", self)
        
        # Font size actions
        size_menu = QMenu("Size", self)
        sizes = [8, 10, 12, 14, 16, 18, 20]
        for size in sizes:
            action = QAction(f"{size}pt", self)
            action.triggered.connect(lambda checked, s=size: self.change_font_size(s))
            size_menu.addAction(action)
        
        # Font family action
        select_font_action = QAction("Select Font...", self)
        select_font_action.triggered.connect(self.select_font)
        
        # Add submenus and actions
        font_menu.addMenu(size_menu)
        font_menu.addAction(select_font_action)
        context_menu.addMenu(font_menu)
        
        # Add standard context menu items
        context_menu.addSeparator()
        
        # Standard edit actions
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.undo)
        undo_action.setEnabled(self.isUndoAvailable())
        
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.redo)
        redo_action.setEnabled(self.isRedoAvailable())
        
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.cut)
        cut_action.setEnabled(self.hasSelectedText())
        
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy)
        copy_action.setEnabled(self.hasSelectedText())
        
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste)
        paste_action.setEnabled(QApplication.clipboard().text() != '')
        
        select_all_action = QAction("Select All", self)
        select_all_action.triggered.connect(self.selectAll)
        select_all_action.setEnabled(len(self.text()) > 0)
        
        context_menu.addAction(undo_action)
        context_menu.addAction(redo_action)
        context_menu.addSeparator()
        context_menu.addAction(cut_action)
        context_menu.addAction(copy_action)
        context_menu.addAction(paste_action)
        context_menu.addAction(select_all_action)
        
        # Show the menu
        context_menu.exec_(self.mapToGlobal(pos))
    
    def change_font_size(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
    
    def select_font(self):
        font, ok = QFontDialog.getFont(self.font(), self)
        if ok:
            self.setFont(font)

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
        plot_layout = QVBoxLayout(plot_tab)
        plot_layout.setContentsMargins(0, 0, 0, 0)  
        plot_layout.setSpacing(0)  

        # Create the plotting canvas
        self.plot_canvas = PlotCanvas(self)
        self.plot_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        
        # Create the navigation toolbar and center it
        toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_container)
        self.toolbar = NavigationToolbar(self.plot_canvas, self)
        toolbar_layout.addWidget(self.toolbar, alignment=Qt.AlignCenter)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add widgets to plot layout
        plot_layout.addWidget(toolbar_container)
        plot_layout.addWidget(self.plot_canvas)

        # Create equation input interface
        equation_container = QWidget()
        equation_layout = QHBoxLayout(equation_container)
        equation_layout.setContentsMargins(10, 5, 10, 5)

        equation_label = QLabel("f(x) = ")
        self.equation_input = CustomLineEdit()
        self.equation_input.setPlaceholderText("Enter mathematical equation (e.g., sin(x) + x**2)")
        plot_equation_button = QPushButton("Plot")
        plot_equation_button.clicked.connect(self.plot_equation)

        equation_layout.addWidget(equation_label)
        equation_layout.addWidget(self.equation_input, stretch=1)
        equation_layout.addWidget(plot_equation_button)

        plot_layout.addWidget(equation_container)

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

    def convert_to_latex(self, equation):
        # Dictionary of replacements for LaTeX formatting
        replacements = {
            'sin': r'\sin',
            'cos': r'\cos',
            'tan': r'\tan',
            'exp': r'\exp',
            'log': r'\ln',
            '**2': '^2',
            '**3': '^3',
            '**': '^',
            '*': r'\cdot ',
            'sqrt': r'\sqrt',
            'pi': r'\pi'
        }
        
        latex_eq = equation
        for old, new in replacements.items():
            latex_eq = latex_eq.replace(old, new)
        
        return f'$f(x) = {latex_eq}$'

    def plot_equation(self):
        equation = self.equation_input.text()
        try:
            x = np.linspace(-10, 10, 400)
            # Add more numpy functions to the evaluation namespace
            namespace = {
                'x': x,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'exp': np.exp,
                'log': np.log,
                'sqrt': np.sqrt,
                'pi': np.pi
            }
            y = eval(equation, namespace)
            self.plot_canvas.axes.clear()
            self.plot_canvas.axes.plot(x, y)
            
            # Set title with LaTeX equation
            latex_equation = self.convert_to_latex(equation)
            self.plot_canvas.axes.set_title(latex_equation, fontsize=12, pad=10)
            
            self.plot_canvas.draw()
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error plotting equation: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
