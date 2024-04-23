"""Application Access File"""

import os
import sys
from discord import Intents
from dotenv import load_dotenv
from bot.mobius_bot import Mobius
from utils import assemble_intents, assemble_logger, get_config

if __name__ == "__main__":

    # Logger
    print("Starting Mobius bot server... ")
    print("Assembling logger... ")
    LOGGER = assemble_logger()
    LOGGER.info("Logger assembled")

    # Bot Configuration
    LOGGER.info("Collecting config...")
    CONFIG: dict[str, str] = get_config(LOGGER)
    LOGGER.info("Config found")

    # Environment Variables
    LOGGER.info("Loading environment variables... ")
    LOADED = load_dotenv()
    if LOADED is False:
        LOGGER.error("Environment not found!")
        sys.exit("server terminated")
    LOGGER.info("Environment found")

    # Discord Bot Token
    LOGGER.info("Validating TOKEN... ")
    TOKEN: str | None = os.getenv("TOKEN")
    if TOKEN is None:
        LOGGER.error("TOKEN was not provided in the environment")
        sys.exit("exit")
    TOKEN = TOKEN.strip()
    if len(TOKEN) == 0:
        LOGGER.error("Provided TOKEN is empty")
        sys.exit("server terminated")
    LOGGER.info("TOKEN validated")

    # Intents
    LOGGER.info("Assembling Intents... ")
    INTENTS: Intents = assemble_intents()
    LOGGER.info("Client assembled")

    # Initialize Bot
    LOGGER.info("Instantiating Mobius... ")
    BOT = Mobius(config=CONFIG, intents=INTENTS, logger=LOGGER)
    LOGGER.info("Mobius instantiated")

    # Start Bot
    LOGGER.info("Initializing Mobius... ")
    try:
        BOT.run(TOKEN)
    except Exception as e:
        LOGGER.error(msg=f"Mobius failed while running: {
                     type(e).__name__}: {e}", exc_info=True)
