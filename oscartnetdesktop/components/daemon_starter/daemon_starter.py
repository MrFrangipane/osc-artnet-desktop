from PySide6.QtCore import QObject, Signal

from oscartnetdaemon.components.launcher import Launcher as DaemonLauncher


class DaemonStarter(QObject):
    statusChanged = Signal(bool)

    def __init__(self):
        super().__init__()

        self._daemon_launcher = DaemonLauncher()
        self._is_running = False

    def start_restart(self):
        if self._is_running:
            self.stop()
        self._is_running = True
        self._daemon_launcher.exec(blocking=False)
        self.statusChanged.emit(self._is_running)

    def stop(self):
        self._daemon_launcher.stop()
        self._is_running = False
        self.statusChanged.emit(self._is_running)
