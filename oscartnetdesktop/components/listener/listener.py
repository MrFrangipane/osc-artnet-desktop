from PySide6.QtCore import QObject, Signal, QTimer
from stupidArtnet import StupidArtnetServer


class Listener(QObject):
    dataChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stupid_artnet: StupidArtnetServer = None
        self._listener_id = None

        self._previous_universe = [0] * 512

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timeout)
        self._timer.start(int(1000 / 40))

    def start(self):
        self._stupid_artnet = StupidArtnetServer()
        self._listener_id = self._stupid_artnet.register_listener()

    def _timeout(self):
        data = self._stupid_artnet.get_buffer(self._listener_id)
        if data:
            self.dataChanged.emit(data)
