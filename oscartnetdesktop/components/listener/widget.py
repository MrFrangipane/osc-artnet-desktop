from PySide6.QtWidgets import QTableView

from oscartnetdesktop.components.listener.listener import Listener
from oscartnetdesktop.components.listener.model import Model


class ListenerWidget(QTableView):
    row_count = 23
    column_count = 22

    def __init__(self, parent=None):
        super().__init__(parent)

        self._listener = Listener()
        self._model = Model()

        self._listener.dataChanged.connect(self._model.update_data)
        self._listener.start()

        self.setModel(self._model)

        self.horizontalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)

        self.resize(800, 200)
