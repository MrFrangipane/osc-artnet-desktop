from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton

from oscartnetdesktop.components.daemon_starter.widget import DaemonStarterWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._engine_widget = DaemonStarterWidget()

        layout = QGridLayout(self)
        layout.addWidget(self._engine_widget)
