from dataclasses import dataclass

from oscartnetdesktop.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    pass
