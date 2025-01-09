from dataclasses import dataclass

from PySide6.QtWidgets import QDockWidget

from oscartnetdaemon import OSCArtnetDaemonAPI

from oscartnetdesktop.core.configuration import Configuration
from oscartnetdesktop.python_extensions.singleton_metaclass import SingletonMetaclass
# from oscartnetdesktop.components.abstract_show_items import AbstractShowItemsWidget


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    daemon = OSCArtnetDaemonAPI()
    show_items_widget = None  # TODO use abstract class
    logger_dock_widget: QDockWidget = None
