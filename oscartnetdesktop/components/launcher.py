from PySide6.QtWidgets import QApplication
from pyside6helpers import css


from oscartnetdesktop.components.listener.widget import ListenerWidget


class Launcher:

    def __init__(self):
        self.app = QApplication()
        self.widget = ListenerWidget()

        css.load_onto(self.app)

    def exec(self):
        self.widget.show()
        self.app.exec()
