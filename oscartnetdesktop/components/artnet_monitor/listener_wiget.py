from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QPainter
from PySide6.QtWidgets import QWidget

from oscartnetdesktop.components.artnet_monitor.channel_info import ChannelInfo
from oscartnetdesktop.components.artnet_monitor.listener import Listener


class ListenerWidget(QWidget):
    column_width = 30
    column_height = 20

    def __init__(self, parent=None):
        super().__init__(parent)

        self._channels_info: list[ChannelInfo] = [ChannelInfo()] * 512
        self._listener = Listener()
        self._listener.dataChanged.connect(self._new_data)
        self._listener.start()

        self._highlighted_channels: list[int] = list()

    def set_highlight(self, channels: list[int]):
        self._highlighted_channels = channels
        self.update()

    def paintEvent(self, event):
        if not self.isEnabled() or not self._channels_info:
            return

        column_count = max(1, int(float(self.width()) / self.column_width))
        row_count = max(1, int(len(self._channels_info) / column_count) + len(self._channels_info) % column_count)

        painter = QPainter()
        painter.begin(self)

        index = 0
        for row in range(0, row_count):
            if index >= len(self._channels_info):
                break

            for col in range(0, column_count):
                if index >= len(self._channels_info):
                    break
                rect = QRectF(
                    col * self.column_width, row * self.column_height,
                    self.column_width - 1, self.column_height - 1
                )
                info = self._channels_info[index]

                if index in self._highlighted_channels:
                    info.fixture_color = info.fixture_color.darker(170)

                # background
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(info.fixture_color))
                painter.drawRect(rect)

                # group
                painter.setBrush(QBrush(info.group_color))
                painter.drawRect(rect.adjusted(0, rect.height() * 0.9, 0, 0))

                # text
                painter.setPen(info.text_color)
                painter.drawText(rect, str(info.value), Qt.AlignHCenter | Qt.AlignVCenter)

                index += 1

        painter.end()

    def _new_data(self, channels_info):
        if self.isEnabled():
            self._channels_info = channels_info
            self.update()
