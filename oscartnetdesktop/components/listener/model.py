from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor


class Model(QAbstractTableModel):
    row_count = 23
    column_count = 23

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = [0] * 512
        self._colors = [QColor(v, v, v) for v in range(256)]

    def rowCount(self, parent=None):
        return self.row_count

    def columnCount(self, parent=None):
        return self.column_count

    def data(self, index, role=Qt.DisplayRole):
        channel = index.row() * self.column_count + index.column()
        if channel > 512:
            return

        value = self._data[channel]

        if role == Qt.DisplayRole:
            return str(value)

        elif role == Qt.BackgroundRole:
            return self._colors[value]

        elif role == Qt.ForegroundRole:
            return self._colors[0] if value > 150 else self._colors[-1]

    def update_data(self, data):
        self._data = data
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.row_count, self.column_count)
        )
