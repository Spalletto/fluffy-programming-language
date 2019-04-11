import sys

import matplotlib.pyplot as plt
from descartes import PolygonPatch
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout,
                             QPlainTextEdit, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QIcon

from lexer import Lexer, PATCHES
from local_parser import Parser


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
        self.ax = self.figure.add_subplot(111)
        self.i = 0

    def initUI(self):
        self.setWindowTitle("Fluffy.Graphics")
        icon = QIcon(r"resources/icon.png")
        self.setWindowIcon(icon)
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
        self.ax.cla()
        PATCHES.clear()
        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)
        input_text = self.text_edit.toPlainText()
        
        lexer = Lexer(input_text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        program.execute()

        for patch in PATCHES:
            self.ax.add_patch(patch)
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
