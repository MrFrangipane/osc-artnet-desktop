from PySide6.QtCore import QObject, Signal, QTimer

from oscartnetdesktop.core.components import Components


class Listener(QObject):
    _framerate = 40
    dataChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timeout)

    def start(self):
        self._timer.start(int(1000 / self._framerate))

    def _timeout(self):
        if Components().daemon_components().fixture_updater is None:
            return

        self.dataChanged.emit(
            Components().daemon_components().fixture_updater.universe  # FIXME create an API for that
        )
