"""File containing bot configuration functions"""
import json
import sys
from logging import Logger
from os import path


def get_config(logger: Logger) -> dict[str, str]:
    """Retrieves the configuration file for Mobius or causes the program to exit"""

    CONFIG_PATH: str = f"{path.realpath(
        path.dirname(__file__))}/../config.json"

    if not path.isfile(CONFIG_PATH):
        logger.error("'config.json' not found! Please add it and try again.")
        sys.exit("server terminated")
    else:
        with open(file=CONFIG_PATH, encoding="utf-8") as file:
            return json.load(file)
