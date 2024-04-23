"""File for handling Discord bot actions and life cycle"""

import random
from os import listdir, name as os_name
from logging import Logger
from platform import python_version, system, release
from aiosqlite import connect
from discord import Message, Game, Embed, Intents
from discord import __version__ as discord_version
from discord.ext.tasks import loop
from discord.ext.commands import Bot, Context, CommandOnCooldown, NotOwner, MissingPermissions, BotMissingPermissions, MissingRequiredArgument, CheckFailure, UserInputError, CommandError
from discord.ext.commands import when_mentioned_or
from utils import initialize_sqlite_database
from database import DatabaseManager


class Mobius(Bot):
    """Class for Mobius bot"""

    def __init__(self, config: dict[str, str], intents: Intents, project_directory: str, logger: Logger) -> None:
        super().__init__(
            command_prefix=when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )

        self.logger = logger
        self.config = config
        self.project_directory = project_directory
        self.database: DatabaseManager = None

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in listdir(f"{self.project_directory}/cogs"):
            if file.endswith(".py") and 'template' not in file:
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @loop(minutes=2.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["with explosives :boom:", "with dolphins :dolphin:",
                    "by himself :waxing_crescent_moon:", "with fish :tropical_fish:", "your mom :woman_bowing:"]
        await self.change_presence(activity=Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info("Initializing database... ")
        await initialize_sqlite_database(self.project_directory)
        self.logger.info("Database initialized")
        self.logger.info("Loading cogs... ")
        await self.load_cogs()
        self.logger.info("Cogs loaded")
        self.logger.info("Initializing status task loop... ")
        self.status_task.start()  # pylint: disable=no-member
        self.logger.info("Status task loop initialized... ")
        self.logger.info("Initializing database manager... ")
        self.database = DatabaseManager(
            connection=await connect(f"{self.project_directory}/database/database.db")
        )
        self.logger.info("Database manager initialized")
        self.logger.info("Mobius initialization complete")
        self.logger.info("-------------------")
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord_version}")
        self.logger.info(f"Python version: {python_version()}")
        self.logger.info(f"Running on: {system()} {release()} ({os_name})")

    async def on_message(self=None, message: Message = None) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {
                    context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {
                    context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self=None, context: Context = None, error: CommandError | CheckFailure | UserInputError = None) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {
                    f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, NotOwner):
            embed = Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {
                        context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {
                        context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, MissingPermissions):
            embed = Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, MissingRequiredArgument):
            embed = Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
