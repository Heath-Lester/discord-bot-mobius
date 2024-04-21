"""File for handling Discord bot actions and life cycle"""

from discord import message, Client, Intents
from .responses import handle_response


async def send_message(discord_message: message, command: str, is_private: bool = False):
    """Function to control where messages are sent"""

    print(f"{discord_message.author} said: '{
          command}' ({discord_message.channel})")

    try:
        response = handle_response(command)
        if is_private:
            await discord_message.author.send(response)
        else:
            await discord_message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot(token: str, client: Client) -> None:
    """Initialize bot actions"""
    mobius_id: str = ""
    mobius_name: str = ""

    @client.event
    async def on_ready():
        # Set Mobius properties used for comparison once after initialization
        mobius_id = str(client.user.id)
        mobius_name = client.user.name.lower()
        print(f'{client.user} is now online!')

    @client.event
    async def on_message(discord_message: message):
        # Prevent Mobius from reacting to itself
        if discord_message.author == client.user:
            return

        if discord_message.content is not None and len(discord_message.content) > 0:
            if discord_message.content.startswith("!"):
                await send_message(discord_message, discord_message.content[1:], False)
            elif mobius_name in discord_message.content.lower():
                await send_message(discord_message, discord_message.content, False)
            elif mobius_id in discord_message.content:
                await send_message(discord_message, discord_message.content, False)

    client.run(token)


def assemble_client() -> Client:
    """Assembles Discord Client with bot permissions"""
    intents = Intents.default()
    intents.message_content = True
    return Client(intents=intents)
