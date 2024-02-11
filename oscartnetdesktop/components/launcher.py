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
from oscartnetdesktop.components.argument_parser import parse_args


_logger = logging.getLogger(__name__)


class Launcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        css.load_onto(self._application)

        self._main_window = MainWindow()
        dock_logger_to_main_window(self._main_window)
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        #
        # Daemon fixme: LoggerWidget must exist before logging.Basic ?
        daemon_configuration = Components().daemon.configure_from_command_line()
        daemon_configuration.artnet_target_node_ip = "192.168.20.7"
        Components().daemon.configure(daemon_configuration)

        # self.css_editor = CSSEditor("Frangitron")

    def exec(self) -> int:
        if Components().configuration.maximized:
            self._main_window.showMaximized()
        else:
            self._main_window.show()

        return self._application.exec()
