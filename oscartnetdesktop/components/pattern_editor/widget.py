from dataclasses import fields

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QTableView, QGridLayout, QSpinBox, QLabel, QComboBox

from oscartnetdaemon.components.pattern_store.api import PatternStoreAPI
from oscartnetdaemon.core.show.item import ShowItem


class PatternEditorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self.save_pattern)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)

        self.spin_step_count = QSpinBox()
        self.spin_step_count.setRange(0, 32)
        self.spin_step_count.valueChanged.connect(self._set_length)

        self.combo_pattern = QComboBox()
        self.combo_pattern.addItems(["A", "B", "C", "D", "E"])
        self.combo_pattern.setMinimumWidth(60)
        self.combo_pattern.currentIndexChanged.connect(self.update_pattern)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Pattern"), 0, 0)
        layout.addWidget(self.combo_pattern, 0, 1)

        layout.addWidget(QLabel("Step count"), 0, 2)
        layout.addWidget(self.spin_step_count, 0, 3)

        layout.addWidget(QWidget(), 0, 4)

        layout.addWidget(self.table, 1, 0, 1, 5)

        layout.setRowStretch(1, 100)
        layout.setColumnStretch(layout.columnCount() - 1, 100)

        self.table.horizontalHeader().setDefaultSectionSize(20)

        self._show_item: ShowItem = None
        self._field_names: list[str] = list()
        self._is_updating = False

        self.init_data()

    def set_show_item(self, item: ShowItem):
        self._show_item = item
        self.update_pattern()

    def update_pattern(self):
        self._is_updating = True

        self.init_data()

        self._field_names = [field.name for field in fields(self._show_item.fixture.Mapping)]
        self.model.setVerticalHeaderLabels([name.replace('_', ' ').capitalize() for name in self._field_names])

        steps = PatternStoreAPI.get_steps(
            fixture_type=self._show_item.name,
            pattern_index=self.combo_pattern.currentIndex(),
            group_place=self._show_item.group_place
        )

        self.spin_step_count.setValue(len(steps))

        for step_index, step in steps.items():
            for name, value in step.items():
                row = self._field_names.index(name)
                self.model.setItem(row, 0, QStandardItem("X"))
                self.model.setItem(row, step_index + 1, QStandardItem(str(value)))

        self._is_updating = False

    def init_data(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Active"])
        self.spin_step_count.setValue(0)

    def _set_length(self, length):
        if self._show_item is None:
            return

        self.model.setColumnCount(length + 1)
        self.model.setHorizontalHeaderLabels(["Active"] + [str(i + 1) for i in range(length)])
        self.save_pattern()

    def save_pattern(self):
        if self._is_updating:
            return

        steps = dict()

        for col in range(self.spin_step_count.value()):
            step = {}
            for row in range(self.model.rowCount()):
                item = self.model.item(row, col + 1)
                if item is not None:
                    if item.text():
                        step[self._field_names[row]] = int(item.text())
            steps[col] = step

        PatternStoreAPI.set_steps(
            fixture_type=self._show_item.name,
            pattern_index=self.combo_pattern.currentIndex(),
            group_place=self._show_item.group_place,
            steps=steps
        )
