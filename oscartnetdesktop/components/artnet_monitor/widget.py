from PySide6.QtWidgets import QWidget, QCheckBox, QGridLayout

from oscartnetdaemon.core.show.item_info import ShowItemInfo

from oscartnetdesktop.components.artnet_monitor.listener_wiget import ListenerWidget


class ArtnetMonitorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("OSC Artnet monitor")

        self._listener = ListenerWidget()
        self._checkbox_enabled = QCheckBox("Enabled")
        self._checkbox_enabled.setChecked(True)
        self._checkbox_enabled.stateChanged.connect(self._on_checkbox_enabled)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._checkbox_enabled, 0, 0)
        layout.addWidget(self._listener, 1, 0)
        layout.setRowStretch(1, 100)

        self.setFixedHeight(200)

    def _on_checkbox_enabled(self, value):
        self._listener.setEnabled(self._checkbox_enabled.isChecked())
        self.setFixedHeight(
            200 if self._checkbox_enabled.isChecked() else 25
        )

    def highlight(self, info: ShowItemInfo):
        self._listener.set_highlight(list(range(info.channel_info.first, info.channel_info.last)))
