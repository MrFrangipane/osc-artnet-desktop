from PySide6.QtCore import QObject, Signal

from oscartnetdesktop.core.components import Components


class DaemonStarter(QObject):
    statusChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._is_running = False

    def start_restart(self):
        if self._is_running:
            self.stop()

        self._is_running = True
        Components().daemon.start()
        self.statusChanged.emit(self._is_running)

    def stop(self):
        Components().daemon.stop()

        self._is_running = False
        self.statusChanged.emit(self._is_running)
