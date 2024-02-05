from PySide6.QtWidgets import QApplication

from oscartnetdesktop.components.listener.widget import ListenerWidget


class Launcher:

    def __init__(self):
        self.app = QApplication()
        self.widget = ListenerWidget()

    def exec(self):
        self.widget.show()
        self.app.exec()
