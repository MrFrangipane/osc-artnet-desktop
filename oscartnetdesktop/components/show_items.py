from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from pyside6helpers.layout import clear

from oscartnetdaemon import OSCArtnetDaemonAPI


class ShowItemsWidget(QWidget):
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
        clear(self.scroll_layout)
        for show_item in OSCArtnetDaemonAPI().show_items:
            label = QLabel(
                f"{show_item.name} "
                f"[{show_item.channel_first + 1}, {show_item.channel_first + show_item.channel_count}]"
            )
            self.scroll_layout.addWidget(label)

        spacing_widget = QWidget()
        self.scroll_layout.addWidget(spacing_widget)
        self.scroll_layout.setStretchFactor(spacing_widget, 1)
