from shapely.geometry import Point, Polygon
from descartes import PolygonPatch
 
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QPlainTextEdit

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.showMaximized()
        self.figure = plt.figure()
        self.text_edit = QPlainTextEdit()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('RUN')
        self.button.clicked.connect(self.plot)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        layout1 = QVBoxLayout()
        self.button.setStyleSheet("height: 40px; font-size: 20px;")
        layout1.addWidget(self.button)
        self.text_edit.setStyleSheet("font-size: 15px; font-family: 'Space Mono'")
        layout1.addWidget(self.text_edit)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.toolbar)
        layout2.addWidget(self.canvas)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        self.setLayout(main_layout)

    def plot(self):
        self.figure.clear()
        text = self.text_edit.toPlainText()
        
        ax = self.figure.add_subplot(111)
        figure = Point(0,0).buffer(1)
        patch = PolygonPatch(figure)
        ax.add_patch(patch)

        # refresh canvas
        plt.clf()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())