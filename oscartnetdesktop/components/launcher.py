import logging
import os.path

from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication

# from pyside6helpers.css.editor import CSSEditor
from pyside6helpers import css
from pyside6helpers.logger import dock_logger_to_main_window
from pyside6helpers.logger.string_io_capture import StringIOCapture

from oscartnetdesktop.core.components import Components
from oscartnetdesktop.components.central_widget import CentralWidget
from oscartnetdesktop.components.main_window import MainWindow
from oscartnetdesktop.components.argument_parser import parse_args
from oscartnetdesktop.components import project_persistence


_logger = logging.getLogger(__name__)


class Launcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        #
        # Hacky logging
        self._log_stream = StringIOCapture()
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(self._log_stream)])

        #
        # Configuration
        Components().configuration = parse_args()
        Components().configuration.resources_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources"
        )

        #
        # Application
        self._application = QApplication()
        self._application.aboutToQuit.connect(Components().daemon.stop)
        self._application.aboutToQuit.connect(project_persistence.on_quit)
        css.load_onto(self._application)

        #
        # Main Window
        self._main_window = MainWindow()
        dock_logger_to_main_window(self._main_window, self._log_stream)
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        #
        # Project
        project_persistence.on_startup()

        # self.css_editor = CSSEditor("Frangitron")

    def exec(self) -> int:
        if Components().configuration.maximized:
            self._main_window.showMaximized()
        else:
            self._main_window.show()

        return self._application.exec()
