"""File for handling Discord bot actions and life cycle"""

from discord import message, Client, Intents
from .responses import handle_response


async def send_message(message: message, user_message: message, is_private: bool = False):
    """Function to control where messages are sent"""
    try:
        response = handle_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot(token: str):
    """Initialize bot actions"""
    client = Client(intents=Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message: message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == "!":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)

        else:
            await send_message(message, user_message, is_private=False)

    client.run(token)
