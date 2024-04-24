"""Discord Bot Cog File"""

from discord import ClientException, Member, VoiceClient, VoiceChannel, StageChannel
from discord.ext.commands import Cog, Context, command, CommandError
from bot import Mobius


class Voice(Cog, name="Voice"):
    """Cog class containing methods for voice channel"""

    def __init__(self, bot: Mobius):
        self.bot = bot
        # self.voice_client: VoiceClient | None = None  # Store the connected voice client

    @command(name='join', aliases=['summon', 'hereboy', 'psspsspss'], description="Have Mobius join your voice chat")
    async def join_vc(self, context: Context, channel: VoiceChannel | StageChannel | None = None):
        """Connects the bot to a voice channel.

        Args:
            context (discord.ext.commands.Context): Command context.S
            channel (discord.VoiceChannel, optional): The voice channel to join. Defaults to the user's voice channel.
        """
        if context.author is None:
            raise CommandError("Author is None")

        if isinstance(context.author, Member) and context.author.voice is None:
            await context.send("Get in a room first dummy")
            return

        # TODO: Experimenting with setting the voice client on the bot instead of the cog so multiple cogs
        # can be used playing in voice channels but only one cog at a time playing?

        # if self.voice_client is not None and self.voice_client.is_connected():
        #     await context.send("I am already connected to a voice channel.")
        #     return
        if self.bot.voice_client is not None and self.bot.voice_client.is_connected():
            await context.send("I am already connected to a voice channel.")
            return

        if isinstance(context.author, Member) and context.author.voice is not None and context.author.voice.channel is not None:
            channel = context.author.voice.channel

        if channel is None:
            raise CommandError("Channel is None")
        try:
            # self.voice_client = await channel.connect()
            self.bot.voice_client = await channel.connect()
            await context.send(f"Whaddup cunts?")
        except ClientException as e:
            raise CommandError("Failed to connect to voice channel.")

    @command(name='leave', aliases=['disconnect', 'getout', 'goaway'], description="Have Mobius leave your voice chat")
    async def leave_vc(self, context: Context):
        """Disconnects the bot from the voice channel."""

        # if not self.voice_client or not self.voice_client.is_connected():
        #     await context.send("I can't stop what I'm not doing... ")
        #     return
        if not self.bot.voice_client or not self.bot.voice_client.is_connected():
            await context.send("I can't stop what I'm not doing... ")
            return

        # await self.voice_client.disconnect()
        await self.bot.voice_client.disconnect()
        self.voice_client = None
        await context.send("See you cunts!")


async def setup(bot: Mobius) -> None:
    """Used to load cog into bot"""
    await bot.add_cog(Voice(bot))
