from dataclasses import dataclass


@dataclass
class Configuration:
    resources_folder: str = None
    maximized: bool = None
    auto_start: bool = None
    last_project_filepath: str = None
