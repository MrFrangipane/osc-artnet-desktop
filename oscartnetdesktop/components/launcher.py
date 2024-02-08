import logging
import os.path

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QApplication, QDockWidget

# from pyside6helpers.css.editor import CSSEditor
from pyside6helpers import css
from pyside6helpers.logger import dock_logger_to_main_window

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.central_widget import CentralWidget
from oscartnetdesktop.components.main_window import MainWindow


_logger = logging.getLogger(__name__)


class Launcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        Components().daemon.configure_from_command_line()
        Components().configuration.resources_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources"
        )

        self._application = QApplication()
        self._application.aboutToQuit.connect(Components().daemon.stop)
        css.load_onto(self._application)

        self._main_window = MainWindow()
        dock_logger_to_main_window(self._main_window)
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)
        self._main_window.resize(800, 800)

        # self.css_editor = CSSEditor("Frangitron")

    def exec(self) -> int:
        self._main_window.show()
        return self._application.exec()
