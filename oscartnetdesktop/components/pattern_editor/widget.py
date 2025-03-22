from copy import deepcopy
from dataclasses import fields

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel, QLineEdit, QPushButton

from pyside6helpers import icons
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

        self.line_pattern_name = QLineEdit()
        self.line_pattern_name.setMaxLength(10)
        self.line_pattern_name.textChanged.connect(self._name_changed)

        self.spin_pattern = QSpinBox()

        self.spin_pattern.setRange(1, 8)
        self.spin_pattern.valueChanged.connect(self.update_pattern)

        self.spin_step_count = QSpinBox()
        self.spin_step_count.setRange(0, 32)
        self.spin_step_count.valueChanged.connect(self._set_length)

        #
        # FIXME better words for fixture/pattern/step !!
        self.button_copy_pattern = QPushButton("Copy pattern")
        self.button_copy_pattern.setIcon(icons.equalizer())
        self.button_copy_pattern.clicked.connect(self._copy_pattern_clicked)

        self.button_paste_pattern = QPushButton("Paste pattern")
        self.button_paste_pattern.setIcon(icons.equalizer())
        self.button_paste_pattern.clicked.connect(self._paste_pattern_clicked)

        self.button_copy_fixture = QPushButton("Copy fixture")
        self.button_copy_fixture.setIcon(icons.lightbulb())
        self.button_copy_fixture.setToolTip("Copy all fixture patterns")
        self.button_copy_fixture.clicked.connect(self._copy_fixture_clicked)

        self.button_paste_fixture = QPushButton("Paste fixture")
        self.button_paste_fixture.setIcon(icons.lightbulb())
        self.button_paste_fixture.setToolTip("Paste all fixture patterns")
        self.button_paste_fixture.clicked.connect(self._paste_fixture_clicked)

        self.button_shift_left = QPushButton("<< shift left")
        self.button_shift_left.setToolTip("Shift all steps to the left")
        self.button_shift_left.clicked.connect(self._shift_left)

        self.button_shift_right = QPushButton("shift right >>")
        self.button_shift_right.setToolTip("Shift all steps to the right")
        self.button_shift_right.clicked.connect(self._shift_right)

        self.button_inerpolate = QPushButton("interpolate")
        self.button_inerpolate.setIcon(icons.wifi())
        self.button_inerpolate.setToolTip("Creates a linear interpolation between first and last selected steps")
        self.button_inerpolate.clicked.connect(self._interpolate)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Pattern"), 0, 0)
        layout.addWidget(self.spin_pattern, 0, 1)
        layout.addWidget(self.line_pattern_name, 0, 2)

        layout.addWidget(QLabel("Step count"), 0, 3)
        layout.addWidget(self.spin_step_count, 0, 4)

        layout.addWidget(QLabel(""), 0, 5)
        layout.addWidget(self.button_copy_pattern, 0, 6)
        layout.addWidget(self.button_paste_pattern, 0, 7)

        layout.addWidget(QLabel(""), 0, 8)
        layout.addWidget(self.button_copy_fixture, 0, 9)
        layout.addWidget(self.button_paste_fixture, 0, 10)

        layout.addWidget(QLabel(""), 0, 11)
        layout.addWidget(self.button_shift_left, 0, 12)
        layout.addWidget(self.button_shift_right, 0, 13)

        layout.addWidget(QLabel(""), 0, 14)
        layout.addWidget(self.button_inerpolate, 0, 15)

        layout.addWidget(QWidget(), 0, 16)

        layout.addWidget(self.table, 1, 0, 1, 17)

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

        # TODO move this to PatterAPI ?
        self._steps_clipboard: dict[int, [dict[str, int]]] = dict()
        self._fixture_clipboard: list[dict[int, dict[str, int]]] = list()
        self.init_data()

    def set_show_item(self, item: ShowItem):
        self._show_item = item
        self.update_pattern()

    def update_pattern_name(self):
        pattern_index = self.spin_pattern.value() - 1
        self.line_pattern_name.setText(
            PatternStoreAPI.pattern_names()[pattern_index]
        )

    def update_pattern(self):
        PatternStoreAPI.set_current_pattern(self.spin_pattern.value() - 1)
        self.update_pattern_name()
        if self._show_item is None:
            return

        steps = PatternStoreAPI.get_steps(
            show_item_info=self._show_item.info,
            pattern_index=self.spin_pattern.value() - 1
        )
        self._set_steps(steps)

    def _set_steps(self, steps: dict[int, [dict[str, int]]]):
        self._dont_save = True
        self.init_data()

        self._field_names = [field.name for field in fields(self._show_item.fixture.Mapping)]
        self.model.setVerticalHeaderLabels([name.replace('_', ' ').capitalize() for name in self._field_names])

        self.spin_step_count.setValue(len(steps))

        for step_index, step in steps.items():
            for name, value in step.items():
                if name not in self._field_names:
                    continue
                row = self._field_names.index(name)
                self.model.setItem(row, 0, QStandardItem("X"))
                self.model.setItem(row, step_index + 1, QStandardItem(str(value)))

        self._dont_save = False

    def init_data(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Active"])
        self.spin_step_count.setValue(0)
        self._current_step = None
        self.update_pattern_name()

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
            pattern_index=self.spin_pattern.value() - 1,
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
            pattern_index=self.spin_pattern.value() - 1,
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
            return min(max(0, int(data)), 255)
        except ValueError:
            return 0

    def _name_changed(self, text):
        PatternStoreAPI.set_pattern_name(
            pattern_index=self.spin_pattern.value() - 1,
            name=text
        )

    def _copy_pattern_clicked(self):
        if self._show_item is None:
            return

        self._steps_clipboard = PatternStoreAPI.get_steps(
            show_item_info=self._show_item.info,
            pattern_index=self.spin_pattern.value() - 1
        )

    def _paste_pattern_clicked(self):
        if self._show_item is None:
            return
        self._set_steps(self._steps_clipboard)
        self.update_pattern()

    def _copy_fixture_clicked(self):
        if self._show_item is None:
            return

        self._fixture_clipboard.clear()
        for pattern_index, pattern in enumerate(PatternStoreAPI.pattern_names()):
            pattern_steps = PatternStoreAPI.get_steps(
                show_item_info=self._show_item.info,
                pattern_index=pattern_index
            )
            self._fixture_clipboard.append(pattern_steps)

    def _paste_fixture_clicked(self):
        if self._show_item is None:
            return

        for pattern_index, pattern_steps in enumerate(self._fixture_clipboard):
            PatternStoreAPI.set_steps(
                show_item_info=self._show_item.info,
                pattern_index=pattern_index,
                steps=pattern_steps
            )

        self.update_pattern()

    def _shift_left(self):
        if self._show_item is None:
            return
        PatternStoreAPI.shift_steps(
            show_item_info=self._show_item.info,
            pattern_index=self.spin_pattern.value() - 1,
            offset=-1
        )
        self.update_pattern()

    def _shift_right(self):
        if self._show_item is None:
            return
        PatternStoreAPI.shift_steps(
            show_item_info=self._show_item.info,
            pattern_index=self.spin_pattern.value() - 1,
            offset=1
        )
        self.update_pattern()

    def _interpolate(self):
        selected_indexes = self.table.selectionModel().selectedIndexes()
        if len(selected_indexes) == 0:
            return

        self._dont_save = True
        self._dont_propagate_edition = True

        rows = dict()
        for index in selected_indexes:
            if index.row() not in rows:
                rows[index.row()] = {index.column(): index}
            else:
                rows[index.row()][index.column()] = index

        for row in rows.values():
            indexes = {key: row[key] for key in sorted(row)}
            steps = list(indexes.keys())
            values = list([int(index.data() if index.data() else 0) for index in indexes.values()])
            size = steps[-1] - steps[0] + 1

            if values[0] == values[-1] or size < 3:
                continue

            increment = (values[-1] - values[0]) / (size - 1)
            for col, index in indexes.items():
                value = values[0] + (col - steps[0]) * increment
                self.model.setData(index, str(int(value)), Qt.EditRole)

        self._dont_save = False
        self._dont_propagate_edition = False

        self._update_fixture()
        self.save_pattern()
