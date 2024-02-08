from dataclasses import dataclass

from oscartnetdaemon.components.launcher import Launcher as DaemonLauncher
from oscartnetdaemon.core.components import Components as DaemonComponents

from oscartnetdesktop.core.configuration import Configuration
from oscartnetdesktop.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    # FIXME create an API for what follows
    daemon_launcher = DaemonLauncher()
    daemon_components = DaemonComponents
