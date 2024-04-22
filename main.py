"""Application Access File"""
import os
from discord import Client
from dotenv import load_dotenv
from bot.bot import run_discord_bot, assemble_client

if __name__ == "__main__":
    print("Starting Mobius bot server... ")
    print("Loading environment variables... ")
    load_dotenv()
    TOKEN: str | None = os.getenv("TOKEN")

    print("Validating TOKEN... ")
    if TOKEN is None:
        raise ValueError("TOKEN was not provided in the environment")

    TOKEN = TOKEN.strip()

    if len(TOKEN) == 0:
        raise ValueError("Provided TOKEN is empty")

    print("TOKEN validated")

    print("Assembling Client... ")
    client: Client = assemble_client()
    print("Client assembled")

    print("Initializing Mobius... ")
    run_discord_bot(token=TOKEN, client=client)
