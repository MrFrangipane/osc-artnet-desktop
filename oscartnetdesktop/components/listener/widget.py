from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from oscartnetdesktop.components.listener.listener import Listener


class ListenerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)

        self.labels = list()
        for row in range(22):
            self.labels.append(list())
            for column in range(22):
                new_label = QLabel('0')
                self.labels[row].append(new_label)
                layout.addWidget(new_label, row, column)

        self._listener = Listener()
        self._listener.dataChanged.connect(self._on_data_changed)
        self._listener.start()

        self.setFixedSize(450, 450)

    def _on_data_changed(self, channel: int, value:int):
        row = int(channel / 22)
        column = channel % 22
        self.labels[row][column].setText(str(value))
