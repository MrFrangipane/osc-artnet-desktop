import argparse

from oscartnetdesktop.core.configuration import Configuration


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m", "--maximized", action="store_true",
        help="Window is maximized at startup"
    )
    parser.add_argument(
        "-s", "--auto-start", action="store_true",
        help="Starts daemon at startup"
    )

    arguments, _ = parser.parse_known_args()

    return Configuration(
        maximized=arguments.maximized,
        auto_start=arguments.auto_start
    )
