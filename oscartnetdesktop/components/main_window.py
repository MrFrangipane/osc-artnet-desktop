import os.path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel

from oscartnetdesktop.core.components import Components


class MainWindow(QMainWindow):
    shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OSC Artnet Desktop")

        icon_filepath = os.path.join(Components().configuration.resources_folder, "application-icon.png")
        self.setWindowIcon(QIcon(icon_filepath))

        logo_filepath = os.path.join(Components().configuration.resources_folder, "frangitron-logo.png")
        logo_pixmap = QPixmap(logo_filepath)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        self.statusBar().addPermanentWidget(logo_label)

    def showEvent(self, event):
        self.shown.emit()
        event.accept()
