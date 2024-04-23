"""File for sending responses"""

from discord import message


async def send_response(discord_message: message, response: str, is_private: bool = False) -> None:
    """Function to control where messages are sent"""

    try:
        if is_private:
            await discord_message.author.send(response)
        else:
            await discord_message.channel.send(response)
    except Exception as e:
        print(e)
