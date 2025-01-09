from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtGui import QFont, QPalette
from PySide6.QtCore import Qt, QRect, QSize

from oscartnetdaemon.core.show.item import ShowItem
from oscartnetdaemon.core.show.item_info import ShowItemInfo


class ShowItemDelegate(QStyledItemDelegate):

    GroupWidth = 20
    ChannelsWidth = 70

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """
        Custom rendering for each item.
        """
        show_item_info: ShowItemInfo = index.data(Qt.UserRole)

        painter.save()

        # Group Color
        rect = QRect(option.rect)
        rect.setWidth(self.GroupWidth)

        if show_item_info.group_info.index % 2:
            painter.fillRect(rect, option.palette.color(QPalette.ColorRole.Mid))
        else:
            painter.fillRect(rect, option.palette.color(QPalette.ColorRole.Shadow))

        # Selection
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Group Text
        painter.drawText(
            rect,
            Qt.AlignVCenter | Qt.AlignCenter,
            str(show_item_info.group_info.index),
        )

        # Name
        rect = QRect(option.rect)
        rect.setLeft(rect.left() + self.GroupWidth)
        rect.setWidth(rect.width() - self.GroupWidth)

        painter.drawText(
            QRect(rect.x() + 10, rect.y(), rect.width() - 10, rect.height()),
            Qt.AlignVCenter | Qt.AlignLeft,
            f"{show_item_info.name} {show_item_info.group_info.place + 1:02}",
        )

        # channels
        rect = QRect(option.rect)
        rect.setLeft(rect.left() + rect.width() - self.ChannelsWidth)
        rect.setWidth(self.ChannelsWidth)

        painter.drawText(
            QRect(rect.x() + 10, rect.y(), rect.width() - 10, rect.height()),
            Qt.AlignVCenter | Qt.AlignCenter,
            f"[{show_item_info.channel_info.first} {show_item_info.channel_info.last}]",
        )

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(200, 30)
