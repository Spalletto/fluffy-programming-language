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
from PyQt5.QtCore import QRect, pyqtSignal, pyqtSlot

from lexer import Lexer, PATCHES
from local_parser import Parser
from signals import output


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.showMaximized()
        self.figure = plt.figure()
        self.text_edit = QPlainTextEdit()
        self.output = QPlainTextEdit()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('RUN')
        self.button.clicked.connect(self.plot)
        self.initUI()
        self.ax = self.figure.add_subplot(111)

    def initUI(self):
        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)

        output.trigger.connect(self.print_to_output)

        self.setWindowTitle("Fluffy.Graphics")
        icon = QIcon(r"resources/icon.png")
        self.setWindowIcon(icon)
        main_layout = QVBoxLayout()
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        layout1 = QVBoxLayout()
        self.button.setStyleSheet("height: 40px; font-size: 20px;")
        layout1.addWidget(self.button)
        self.text_edit.setStyleSheet("font-size: 15px; font-family: 'Space Mono'")
        layout1.addWidget(self.text_edit)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.toolbar)
        layout2.addWidget(self.canvas)

        h_layout.addLayout(layout1)
        h_layout.addLayout(layout2)
        
        self.output.setFixedHeight(150)
        self.output.setStyleSheet("font-size: 15px; font-family: 'Space Mono'; font-weight: bold")
        v_layout.addWidget(self.output)
        main_layout.addLayout(h_layout)
        main_layout.addLayout(v_layout)
        
        self.setLayout(main_layout)

    def plot(self):
        self.output.clear()
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
    
    def on_signal_str(self, value):
        print("XKTYYYYYYYYYYYYYYYYYYYYYYY")
        assert isinstance(value, str)
    
    @pyqtSlot(str)
    def print_to_output(self, text):
        self.output.appendPlainText(text)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
