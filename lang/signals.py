from PyQt5.QtCore import pyqtSignal, QObject

class Output(QObject):
    trigger = pyqtSignal(str)
    def __init__(self):
        QObject.__init__(self)

    def send(self, text):
        self.trigger.emit(text)


output = Output()
