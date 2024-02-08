from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton

from pyside6helpers.group import make_group

from oscartnetdesktop.components.daemon_starter.widget import DaemonStarterWidget
from oscartnetdesktop.components.artnet_monitor.widget import ArtNetMonitorWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._engine_widget = DaemonStarterWidget()
        self._artnet_monitor = ArtNetMonitorWidget()

        layout = QGridLayout(self)
        layout.addWidget(self._engine_widget)
        layout.addWidget(make_group("ArNet Monitor", [self._artnet_monitor]))
        layout.setRowStretch(1, 100)
