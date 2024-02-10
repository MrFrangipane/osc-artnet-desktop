from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton

from pyside6helpers import icons
from pyside6helpers.group import make_group
from pyside6helpers.hourglass import hourglass_wrapper

from oscartnetdesktop.components.daemon_starter.daemon_starter import DaemonStarter


class DaemonStarterWidget(QWidget):
    started = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._daemon_starter = DaemonStarter()
        self._daemon_starter.statusChanged.connect(self._status_changed)

        self._start_restart_button = QPushButton()
        self._start_restart_button.setFixedHeight(25)
        self._start_restart_button.setIcon(icons.play_button())
        self._start_restart_button.setToolTip("Start daemon")
        self._start_restart_button.clicked.connect(hourglass_wrapper(self._daemon_starter.start_restart))

        self._stop_button = QPushButton()
        self._stop_button.setFixedHeight(25)
        self._stop_button.setIcon(icons.stop())
        self._stop_button.setToolTip("Stop daemon")
        self._stop_button.clicked.connect(self._daemon_starter.stop)

        group = make_group("Daemon", orientation=Qt.Orientation.Horizontal, widgets=[
            self._start_restart_button,
            self._stop_button
        ])
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(group)

    def _status_changed(self, is_playing: bool):
        if is_playing:
            self._start_restart_button.setIcon(icons.refresh())
            self._start_restart_button.setToolTip("Restart daemon")
            # fixme don't nest signals ? (self._daemon_starter.statusChanged)
            self.started.emit()
        else:
            self._start_restart_button.setIcon(icons.play_button())
            self._start_restart_button.setToolTip("Start daemon")
