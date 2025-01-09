import os.path

from PySide6.QtCore import QSettings, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel

from pyside6helpers import icons

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.project_persistence import make_menu_actions


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

        self._file_menu_actions = list()
        self.make_file_menu()

        self.load_geometry()

    def make_file_menu(self):
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("&File")

        self._file_menu_actions += make_menu_actions()
        for action in self._file_menu_actions:
            menu_file.addAction(action)

        menu_file.addSeparator()
        menu_file.addAction("&Exit", self.close)

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
