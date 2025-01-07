from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget

from oscartnetdaemon.core.show.item import ShowItem

from oscartnetdesktop.core.components import Components


class ShowItemsWidget(QListWidget):

    ShowItemSelected = Signal(ShowItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.currentRowChanged.connect(self._selection_changed)

    def update_list(self):
        self.clear()
        for show_item in Components().daemon.show_items:
            self.addItem(
                f"{show_item.group_place + 1:02d}/{show_item.group_size:02d} - {show_item.name} "
                f"[{show_item.channel_first + 1}, {show_item.channel_first + show_item.channel_count}]"
            )

    def _selection_changed(self, row):
        self.ShowItemSelected.emit(Components().daemon.show_items[row])
