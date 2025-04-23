import os.path

from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog

from oscartnetdesktop.core.components import Components


def make_menu_actions() -> list[QAction]:
    new = QAction("&New project")
    new.triggered.connect(_new)

    load = QAction("&Load project...")
    load.triggered.connect(_load)

    save = QAction("&Save project")
    save.triggered.connect(_save)

    save_as = QAction("Save &project as...")
    save_as.triggered.connect(_save_as)

    return [new, load, save, save_as]


def _new():
    Components().daemon.new_project()
    Components().show_items_widget.update_list()
    Components().main_window.setWindowTitle("OSC Artnet Desktop")


def _load():
    filepath = QFileDialog.getOpenFileName(
        caption="Load project",
        dir=os.path.expanduser("~"),
        filter="JSON files (*.oscartnet.json)"
    )[0]
    if not filepath:
        return

    Components().daemon.load_project(filepath)
    Components().show_items_widget.update_list()
    Components().main_window.setWindowTitle("OSC Artnet Desktop - " + filepath)


def _save() -> str:
    if Components().daemon.is_direct_save_available():
        filepath = Components().daemon.save_project()
        Components().main_window.setWindowTitle("OSC Artnet Desktop - " + filepath)
        return filepath
    else:
        return _save_as()


def _save_as() -> str:
    filepath = QFileDialog.getSaveFileName(
        caption="Save project as",
        dir=os.path.expanduser("~"),
        filter="JSON files (*.oscartnet.json)"
    )[0]
    if not filepath:
        return ""

    Components().daemon.save_project_as(filepath)
    Components().main_window.setWindowTitle("OSC Artnet Desktop - " + filepath)
    return filepath


def on_startup():
    settings = QSettings("Frangitron", "OSCArtnetDesktop")
    filepath = settings.value('lastProjectFilepath')

    if filepath:
        Components().daemon.load_project(filepath)
        Components().show_items_widget.update_list()
        Components().main_window.setWindowTitle("OSC Artnet Desktop - " + filepath)
    else:
        _new()


def on_quit():
    settings = QSettings("Frangitron", "OSCArtnetDesktop")
    settings.setValue('lastProjectFilepath', Components().daemon.project_filepath())
