"""File for function that handles messages"""

from discord import Message, Client
from .determine_response import determine_response
from .send_response import send_response


async def handle_message(client: Client, discord_message: Message) -> None:
    """Determine how to react to messages based on format of the content"""
    # Prevent Mobius from reacting to itself
    if discord_message.author == client.user:
        return

    if discord_message.content is not None and len(discord_message.content) > 0:

        # mobius_name: str = client.user.name.lower()
        mobius_id: str = str(client.user.id)

        if discord_message.content.startswith("!"):
            response: str = determine_response(discord_message.content[1:])
            await send_response(discord_message, response)
        elif mobius_id in discord_message.content:
            response: str = determine_response(discord_message.content)
            await send_response(discord_message, response)
        # Add for talking shit when mentioned
        # elif mobius_name in discord_message.content.lower():
        #     await send_message(discord_message, discord_message.content, False)
