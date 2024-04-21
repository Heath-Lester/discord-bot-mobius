"""Application Access File"""
import os
from dotenv import load_dotenv
from bot.bot import run_discord_bot

if __name__ == "__main__":
    # Access environment variables (.env file)
    load_dotenv()
    TOKEN: str | None = os.getenv("TOKEN")

    # Validate TOKEN
    if TOKEN is None:
        raise ValueError("TOKEN was not provided in environment")

    TOKEN = TOKEN.strip()

    if TOKEN.__len__ == 0:
        raise ValueError("TOKEN is is empty")

    print("TOKEN validated")

    # Run bot
    run_discord_bot(token=TOKEN)