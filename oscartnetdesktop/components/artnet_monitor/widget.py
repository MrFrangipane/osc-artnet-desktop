from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import QWidget

from oscartnetdesktop.components.artnet_monitor.listener import Listener


class ArtNetMonitorWidget(QWidget):
    row_count = 23
    column_count = 23

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OSC ArtNet monitor")

        self._color_ramp = [QColor(v, v, v) for v in range(0, 256)]

        self._universe = bytearray(512)

        self._listener = Listener()
        self._listener.dataChanged.connect(self._new_data)
        self._listener.start()

    def paintEvent(self, event):
        super().paintEvent(event)

        width = self.width() / self.column_count
        height = self.height() / self.row_count

        painter = QPainter()
        painter.begin(self)

        index = 0
        for row in range(0, self.row_count):
            if index >= 512:
                break

            for col in range(0, self.column_count):
                if index >= 512:
                    break
                rect = QRectF(col * width, row * height, width - 1, height - 1)

                value = int(self._universe[index])

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(self._color_ramp[value]))
                painter.drawRect(rect)

                painter.setPen(
                    self._color_ramp[255 - int(value / 2)] if value < 128
                    else self._color_ramp[128 - int(value / 2)]
                )
                painter.drawText(rect, str(value), Qt.AlignHCenter | Qt.AlignVCenter)

                index += 1

        painter.end()

    def _new_data(self, data):
        self._universe = data
        self.update()
