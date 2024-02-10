from PySide6.QtWidgets import QWidget, QGridLayout

from oscartnetdesktop.components.show_items import ShowItemsWidget
from pyside6helpers.group import make_group

from oscartnetdesktop.components.daemon_starter.widget import DaemonStarterWidget
from oscartnetdesktop.components.artnet_monitor.widget import ArtnetMonitorWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._daemon_widget = DaemonStarterWidget()
        self._artnet_monitor_widget = ArtnetMonitorWidget()
        self._show_items_widget = ShowItemsWidget()

        self._daemon_widget.started.connect(self._show_items_widget.update_list)

        layout = QGridLayout(self)
        layout.addWidget(self._daemon_widget, 0, 0)
        layout.addWidget(make_group("ArNet Monitor", [self._artnet_monitor_widget]), 1, 0, 1, 2)
        layout.addWidget(make_group("Fixtures", [self._show_items_widget]), 1, 2)
        layout.setRowStretch(1, 100)
        layout.setColumnStretch(1, 100)
