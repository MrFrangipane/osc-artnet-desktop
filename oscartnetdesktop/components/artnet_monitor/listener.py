from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtGui import QColor, QColorConstants

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.artnet_monitor.channel_info import ChannelInfo as UiChannelInfo


class Listener(QObject):
    _framerate = 100
    dataChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._palette_fixtures = [QColor("#A1CCD1"), QColor("#F4F2DE")]
        self._palette_groups = [QColor(255, 0, 0, 128), QColor(0, 255, 0, 128)]

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timeout)

    def start(self):
        self._timer.start(int(1000 / self._framerate))

    def _timeout(self):
        ui_channels_info = list()
        for channel_info in Components().daemon.channels_info:

            fixture_color = QColor(self._palette_fixtures[channel_info.fixture_index % 2])
            fixture_color.setAlpha(channel_info.value / 2 + 128)

            group_color = QColor(self._palette_groups[channel_info.group_index % 2]) \
                if channel_info.group_index else QColor(0, 0, 0, 0)

            new_ui_channel_info = UiChannelInfo()
            new_ui_channel_info.fixture_color = fixture_color
            new_ui_channel_info.group_color = group_color
            new_ui_channel_info.text_color = QColorConstants.White if channel_info.value < 128 else QColorConstants.Black
            new_ui_channel_info.value = channel_info.value

            ui_channels_info.append(new_ui_channel_info)

        self.dataChanged.emit(ui_channels_info)
