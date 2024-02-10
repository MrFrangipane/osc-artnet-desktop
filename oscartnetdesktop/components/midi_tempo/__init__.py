from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

from pyside6helpers.group import make_group

from oscartnetdesktop.core.components import Components


class MIDITempoWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._bpm_label = QLabel()
        self._beat_counter_label = QLabel()
        self._tap_button = QPushButton("Tap")
        self._tap_button.setFixedHeight(25)
        self._tap_button.clicked.connect(Components().daemon.send_tap_tempo)

        group = make_group("MIDI Tempo", orientation=Qt.Orientation.Horizontal, widgets=[
            self._bpm_label,
            self._beat_counter_label,
            self._tap_button
        ])
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(group)

        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_tempo)
        self._update_timer.start(int(1000/20))

    def _update_tempo(self):
        tempo_info = Components().daemon.tempo_info
        self._bpm_label.setText(f"{tempo_info.bpm:.2f} bpm")
        self._beat_counter_label.setText(f"{tempo_info.beat_counter:.2f} beats")
