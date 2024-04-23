"""File containing bot configuration functions"""

import json
import sys
from logging import Logger
from os import path


def get_config(project_directory: str, logger: Logger) -> dict[str, str]:
    """Retrieves the configuration file for Mobius or causes the program to exit"""

    if not path.isfile(f"{project_directory}/config.json"):
        logger.critical(
            "'config.json' not found! Please add it and try again.")
        sys.exit("server terminated")
    else:
        with open(file=f"{project_directory}/config.json", encoding="utf-8") as file:
            return json.load(file)
