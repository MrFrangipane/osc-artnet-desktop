import os.path

from PySide6.QtCore import QSettings, Signal
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QLabel

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.project_persistence import make_menu_actions


class MainWindow(QMainWindow):
    shown = Signal()
    shownOnce = Signal()

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

        self._toggle_log_visibility_action = QAction("Hide &logs")
        self._toggle_log_visibility_action.triggered.connect(self._toggle_log_visibility)

        self._file_menu_actions = list()
        self.make_file_menu()

        self._show_once = False

        self.load_geometry()

    def make_file_menu(self):
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("&File")

        menu_file.addAction(self._toggle_log_visibility_action)
        menu_file.addSeparator()

        self._file_menu_actions += make_menu_actions()
        for action in self._file_menu_actions:
            menu_file.addAction(action)

        menu_file.addSeparator()
        menu_file.addAction("&Exit", self.close)

    def _toggle_log_visibility(self):
        if Components().logger_dock_widget.isVisible():
            Components().logger_dock_widget.hide()
            self._toggle_log_visibility_action.setText("Show &logs")
        else:
            Components().logger_dock_widget.show()
            self._toggle_log_visibility_action.setText("Hide &logs")

    def closeEvent(self, event):
        self.save_geometry()
        super().closeEvent(event)
        event.accept()

    def showEvent(self, event):
        self.shown.emit()
        if not self._show_once:
            self._show_once = True
            self.shownOnce.emit()
        event.accept()

    def save_geometry(self):
        settings = QSettings("Frangitron", "OSCArtnetDesktop")
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())

    def load_geometry(self):
        settings = QSettings("Frangitron", "OSCArtnetDesktop")
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('state'))
