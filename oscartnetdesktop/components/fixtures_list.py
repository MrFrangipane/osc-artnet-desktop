from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from pyside6helpers.layout import clear

from oscartnetdaemon import OSCArtnetDaemonAPI, FixtureInfo


class FixturesListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)  # Added this line
        self.scroll_content = QWidget()

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.setFixedWidth(200)

    def update_list(self):
        fixtures_info = OSCArtnetDaemonAPI().fixtures_info

        clear(self.scroll_layout)
        for fixture_info in fixtures_info:
            label = QLabel(
                f"{fixture_info.name} "
                f"[{fixture_info.channel_start + 1}, {fixture_info.channel_start + fixture_info.channel_count}]"
            )
            self.scroll_layout.addWidget(label)

        spacing_widget = QWidget()
        self.scroll_layout.addWidget(spacing_widget)
        self.scroll_layout.setStretchFactor(spacing_widget, 1)
