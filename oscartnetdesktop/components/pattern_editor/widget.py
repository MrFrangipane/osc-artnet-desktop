from dataclasses import fields

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QComboBox

from pyside6helpers.item_delegates.boolean import BooleanDelegate
from pyside6helpers.table_view import TableView

from oscartnetdaemon.components.pattern_store.api import PatternStoreAPI
from oscartnetdaemon.core.show.item import ShowItem



class PatternEditorWidget(QWidget):
    WheelChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self._item_changed)

        self.table = TableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setItemDelegateForColumn(0, BooleanDelegate())
        self.table.beginPaste.connect(lambda: setattr(self, '_dont_propagate_edition', True))
        self.table.endPaste.connect(lambda: setattr(self, '_dont_propagate_edition', False))
        self.table.endPaste.connect(self.save_pattern)

        selection_model = self.table.selectionModel()
        selection_model.selectionChanged.connect(self._selection_changed)

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
        self._dont_save = False
        self._dont_propagate_edition = False
        self._current_step: int = None

        PatternStoreAPI.set_wheel_callback(self.wheel_changed)
        self.WheelChanged.connect(self._wheel_changed)  # FIXME use a QObject on the other side ?

        self.init_data()

    def set_show_item(self, item: ShowItem):
        self._show_item = item
        self.update_pattern()

    def update_pattern(self):
        if self._show_item is None:
            return

        self._dont_save = True
        self.init_data()

        self._field_names = [field.name for field in fields(self._show_item.fixture.Mapping)]
        self.model.setVerticalHeaderLabels([name.replace('_', ' ').capitalize() for name in self._field_names])

        steps = PatternStoreAPI.get_steps(
            show_item_info=self._show_item.info,
            pattern_index=self.combo_pattern.currentIndex()
        )

        self.spin_step_count.setValue(len(steps))

        for step_index, step in steps.items():
            for name, value in step.items():
                row = self._field_names.index(name)
                self.model.setItem(row, 0, QStandardItem("X"))
                self.model.setItem(row, step_index + 1, QStandardItem(str(value)))

        self._dont_save = False

    def init_data(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Active"])
        self.spin_step_count.setValue(0)
        self._current_step = None

    def save_pattern(self):
        if self._dont_save:
            return

        if self._show_item is None:
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
            show_item_info=self._show_item.info,
            pattern_index=self.combo_pattern.currentIndex(),
            steps=steps
        )

    def wheel_changed(self, value):
        self.WheelChanged.emit(value)

    def _wheel_changed(self, value):
        value = int(value * 255)
        selected_indexes = self.table.selectionModel().selectedIndexes()
        if len(selected_indexes) == 0:
            return

        self._dont_save = True
        for index in selected_indexes:
            self.model.setData(index, str(value), Qt.EditRole)

        self._dont_save = False

        self._update_fixture()
        self.save_pattern()

    def _selection_changed(self, selected, deselected):
        selected_indexes = selected.indexes()
        if len(selected_indexes) != 1:
            return

        index = selected_indexes[0]
        if index.column() == 0:
            return

        self._current_step = index.column() - 1
        self._update_fixture()

        PatternStoreAPI.set_wheel_value(float(self._value(index)) / 255.0)

    def _set_length(self, length):
        if self._show_item is None:
            return

        self.model.setColumnCount(length + 1)
        self.model.setHorizontalHeaderLabels(["Active"] + [str(i + 1) for i in range(length)])
        self.save_pattern()

    # fixme: a bit messy, unify PatternStoreAPI and fixtureUpdater  apis ?
    def _update_fixture(self):
        if self._show_item is None or self._current_step is None:
            return

        PatternStoreAPI.set_current_step(
            show_item_info=self._show_item.info,
            pattern_index=self.combo_pattern.currentIndex(),
            step_index=self._current_step
        )

    def _item_changed(self, item):
        if item.column() == 0 or self._dont_propagate_edition:
            return

        self._dont_save = True
        for index in self.table.selectionModel().selectedIndexes():
            self.model.setData(index, str(self._value(item)), Qt.EditRole)
        self._dont_save = False

        PatternStoreAPI.set_wheel_value(float(self._value(item)) / 255.0)
        self.save_pattern()

    @staticmethod
    def _value(item):
        if item is None:
            return 0

        data = item.data(Qt.DisplayRole)
        if data is None:
            return 0

        try:
            return int(data)
        except ValueError:
            return 0

        else:
            return min(max(0, int(data)), 255)
