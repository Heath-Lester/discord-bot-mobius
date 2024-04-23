"""File for Discord client utility functions"""

from discord import Intents


def assemble_intents() -> Intents:
    """Assembles Discord Client permissions"""
    INTENTS = Intents.default()
    INTENTS.message_content = True
    return INTENTS
