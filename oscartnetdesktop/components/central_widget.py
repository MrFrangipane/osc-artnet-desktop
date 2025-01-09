from PySide6.QtWidgets import QWidget, QGridLayout

from pyside6helpers.group import make_group

from oscartnetdaemon.core.show.item import ShowItem

from oscartnetdesktop.components.artnet_monitor.widget import ArtnetMonitorWidget
from oscartnetdesktop.components.daemon_starter.widget import DaemonStarterWidget
from oscartnetdesktop.components.midi_tempo import MIDITempoWidget
from oscartnetdesktop.components.pattern_editor.widget import PatternEditorWidget
from oscartnetdesktop.components.show_items.widget import ShowItemsWidget
from oscartnetdesktop.core.components import Components


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._daemon_widget = DaemonStarterWidget()
        self._midi_tempo_widget = MIDITempoWidget()
        self._artnet_monitor_widget = ArtnetMonitorWidget()
        self._show_items_widget = ShowItemsWidget()
        self._pattern_editor_widget = PatternEditorWidget()

        Components().show_items_widget = self._show_items_widget

        self._daemon_widget.started.connect(self._show_items_widget.update_list)
        self._show_items_widget.showItemSelected.connect(self._pattern_editor_widget.set_show_item)
        self._show_items_widget.showItemSelected.connect(
            lambda show_item: self._artnet_monitor_widget.highlight(show_item.info)
        )

        layout = QGridLayout(self)
        layout.addWidget(self._daemon_widget, 0, 0)
        layout.addWidget(self._midi_tempo_widget, 0, 1)
        layout.addWidget(make_group("Fixtures", [self._show_items_widget]), 1, 0, 1, 2)
        layout.addWidget(make_group("Pattern Editor", [self._pattern_editor_widget]), 1, 3)
        layout.addWidget(make_group("ArNet Monitor", [self._artnet_monitor_widget]), 2, 0, 1, 4)
        layout.setRowStretch(1, 100)
        layout.setRowStretch(2, 50)
        layout.setColumnStretch(3, 100)

        self._show_items_widget.update_list()
