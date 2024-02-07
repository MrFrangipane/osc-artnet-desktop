from dataclasses import dataclass

from oscartnetdesktop.core.configuration import Configuration
from oscartnetdesktop.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
