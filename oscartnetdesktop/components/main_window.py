import os.path

from PySide6.QtCore import QSettings, Signal
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

        self.load_geometry()

    def closeEvent(self, event):
        self.save_geometry()
        super().closeEvent(event)
        event.accept()

    def showEvent(self, event):
        self.shown.emit()
        event.accept()

    def save_geometry(self):
        settings = QSettings("Frangitron", "OSCArtnetDesktop")
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())

    def load_geometry(self):
        settings = QSettings("Frangitron", "OSCArtnetDesktop")
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('state'))
