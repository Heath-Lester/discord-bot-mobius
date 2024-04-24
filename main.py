"""Application Access File"""

import sys
from os import getenv
from os.path import realpath, dirname
from discord import Intents
from dotenv import load_dotenv
from bot import Mobius
from utils import assemble_intents, assemble_logger, get_config

if __name__ == "__main__":

    # Logger
    print("Initiating Mobius boot sequence... ")
    print("Assembling logger... ")
    LOGGER = assemble_logger()
    LOGGER.info("Logger assembled")

    PROJECT_DIRECTORY = f"{realpath(dirname(__file__))}"

    # Bot Configuration
    LOGGER.info("Collecting config...")
    CONFIG: dict[str, str] = get_config(PROJECT_DIRECTORY, LOGGER)
    LOGGER.info("Config found")

    # Environment Variables
    LOGGER.info("Loading environment variables... ")
    LOADED = load_dotenv()
    if LOADED is False:
        LOGGER.critical("Environment not found!")
        sys.exit("server terminated")
    LOGGER.info("Environment found")

    # Discord Bot Token
    LOGGER.info("Validating TOKEN... ")
    TOKEN: str | None = getenv("TOKEN")
    if TOKEN is None:
        LOGGER.critical("TOKEN was not provided in the environment")
        sys.exit("server terminated")
    TOKEN = TOKEN.strip()
    if len(TOKEN) == 0:
        LOGGER.critical("Provided TOKEN is empty")
        sys.exit("server terminated")
    LOGGER.info("TOKEN validated")

    # Intents
    LOGGER.info("Assembling Intents... ")
    INTENTS: Intents = assemble_intents()
    LOGGER.info("Intents assembled")

    # Initialize Bot
    LOGGER.info("Instantiating Mobius... ")
    BOT = Mobius(config=CONFIG, intents=INTENTS,
                 project_directory=PROJECT_DIRECTORY, logger=LOGGER)
    LOGGER.info("Mobius instantiated")

    # Start Bot
    LOGGER.info("Initializing Mobius... ")
    try:
        BOT.run(TOKEN)
    except Exception as e:
        LOGGER.error(msg=f"Mobius failed while running: {
                     type(e).__name__}: {e}", exc_info=True)
