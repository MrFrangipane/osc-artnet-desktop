from dataclasses import dataclass

from PySide6.QtGui import QColor


@dataclass
class ChannelInfo:
    fixture_color = QColor()
    group_color = QColor(0, 0, 0, 0)
    text_color = QColor(255, 255, 255)
    value: int = 0
