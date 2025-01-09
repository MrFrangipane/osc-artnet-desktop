from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from oscartnetdaemon.core.show.item import ShowItem

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.show_items.delegate import ShowItemDelegate


class ShowItemsWidget(QListWidget):

    showItemSelected = Signal(ShowItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.currentRowChanged.connect(self._selection_changed)

        self._delegate = ShowItemDelegate()
        self.setItemDelegate(self._delegate)

    def update_list(self):
        self.clear()
        for show_item in Components().daemon.show_items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, show_item.info)
            self.addItem(item)

    def _selection_changed(self, row):
        self.showItemSelected.emit(Components().daemon.show_items[row])
