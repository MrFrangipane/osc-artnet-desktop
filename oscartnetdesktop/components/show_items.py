from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from oscartnetdesktop.core.components import Components


class ShowItemsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)  # Added this line
        self.scroll_content = QLabel()
        self.scroll_content.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.setFixedWidth(200)

    def update_list(self):
        self.scroll_content.setText("\n".join([
            f"{show_item.name} "
            f"[{show_item.channel_first + 1}, {show_item.channel_first + show_item.channel_count}]"
            for show_item in Components().daemon.show_items
        ]))
