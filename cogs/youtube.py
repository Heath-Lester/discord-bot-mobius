from discord import Color, Embed, FFmpegOpusAudio
from discord.ext.commands import Cog, Context, command, CommandError
from bot import Mobius
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError


class Youtube(Cog, name="Youtube"):
    def __init__(self, bot: Mobius):
        self.bot = bot
        # TODO: Revert is using bot voice client doesn't work out
        # self.voice_client = None
        self.queue: list[str] = list()  # Queue for storing songs (URLs)
        self.ydl_opts: dict = {
            # 'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'default_search': 'ytsearch',  # Enable YouTube search for playlists without IDs
        }

    # TODO: This is a copy of the commands in the voice cog. Will remove if not needed.

    # @command(name='join', aliases=['summon', 'hereboy', 'psspsspss'], description="Have Mobius join your voice chat")
    # async def join_vc(self, context: Context, channel: VoiceChannel | StageChannel | None = None):
    #     """Connects the bot to a voice channel.

    #     Args:
    #         context (discord.ext.commands.Context): Command context.S
    #         channel (discord.VoiceChannel, optional): The voice channel to join. Defaults to the user's voice channel.
    #     """
    #     if context.author is None:
    #         raise CommandError("Author is None")

    #     if isinstance(context.author, Member) and context.author.voice is None:
    #         await context.send("You must be connected to a voice channel to use this command.")
    #         return

    #     # TODO: Experimenting with setting the voice client on the bot instead of the cog so multiple cogs
    #     # can be used playing in voice channels but only one cog at a time playing?

    #     # if self.voice_client is not None and self.voice_client.is_connected():
    #     #     await context.send("I am already connected to a voice channel.")
    #     #     return
    #     if self.bot.voice_client is not None and self.bot.voice_client.is_connected():
    #         await context.send("I am already connected to a voice channel.")
    #         return

    #     if isinstance(context.author, Member) and context.author.voice is not None and context.author.voice.channel is not None:
    #         channel = context.author.voice.channel

    #     if channel is None:
    #         raise CommandError("Channel is None")
    #     try:
    #         # self.voice_client = await channel.connect()
    #         self.bot.voice_client = await channel.connect()
    #         await context.send(f"Whaddup cunts?")
    #     except ClientException as e:
    #         raise CommandError("Failed to connect to voice channel.")

    # @command(name='leave', aliases=['disconnect', 'getout', 'goaway'], description="Have Mobius leave your voice chat")
    # async def leave_vc(self, context: Context):
    #     """Disconnects the bot from the voice channel."""

    #     # if not self.voice_client or not self.voice_client.is_connected():
    #     #     await context.send("I can't stop what I'm not doing... ")
    #     #     return
    #     if not self.bot.voice_client or not self.bot.voice_client.is_connected():
    #         await context.send("I can't stop what I'm not doing... ")
    #         return

    #     # await self.voice_client.disconnect()
    #     await self.bot.voice_client.disconnect()
    #     self.voice_client = None
    #     await context.send("See you cunts!")

    @command(name='play', description="play Youtube audio")
    async def play_or_queue(self, context: Context, *, url: str):
        """Plays a YouTube video or playlist, or queues it if the bot is already playing.

        Args:
            context (discord.ext.commands.Context): Command context.
            url (str): URL of the YouTube video or playlist.
        """
        # TODO: Revert if bot voice client doesn't work out
        # if not self.voice_client or not self.voice_client.is_connected():
        #     await context.send("I am not connected to a voice channel. Use the `join` command first.")
        #     return
        if not self.bot.voice_client or not self.bot.voice_client.is_connected():
            await context.send("Need a room to start a party")
            return

        # Extract information using youtube-dl
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                # Extract info without downloading
                info = ydl.extract_info(url, download=False)
            except ExtractorError as e:
                raise CommandError(f"Could not extract video information: {e}")

        if not isinstance(info, dict):
            raise CommandError("Youtube info is not a dictionary")

        if 'entries' in info:
            # It's a playlist
            for video in info['entries']:
                self.queue.append(video['webpage_url'])
            await context.send(f"Playlist added to queue ({len(self.queue)} songs)")
        else:
            # It's a single video
            self.queue.append(url)
            await context.send(f"Added to queue: {url}")

        # Start playing the queue immediately if it's not empty
        await self.start_next_song(context)

    @command(name='next', aliases=['skip'], description="Skip to the next audio in the queue")
    async def start_next_song(self, context: Context):
        """Starts playing the next song in the queue (if any)."""

        if not self.queue:
            return  # No songs in the queue, do nothing

        # Use a separate task to handle song playback to avoid blocking the command handler
        async def play_song(context: Context, url: str):
            source = FFmpegOpusAudio(url)

            # TODO: Revert if bot voice client doesn't work out
            # self.voice_client.play(
            #     source, after=lambda e: self.start_next_song(context))
            if self.bot.voice_client is None:
                raise CommandError("Bot voice client is None")

            self.bot.voice_client.play(
                source, after=lambda e: self.start_next_song(context))
            # Optional: Add song information to chat (e.g., title)

        # Schedule the play_song coroutine as a task
        # TODO: Verify this is not correct
        # task = context.bot.loop.create_task(play_song(context, self.queue[0]))
        task = self.bot.loop.create_task(play_song(context, self.queue[0]))

        # Remove the song from the queue after it starts playing
        self.queue.pop(0)

    @command(name='queue', aliases=["showqueue"], description="Display the current audio queue")
    async def show_queue(self, context: Context):
        """Displays the current queue and the next song."""

        if not self.queue:
            await context.send("The queue is currently empty.")
            return

        embed = Embed(title="Music Queue", color=Color.red())

        if len(self.queue) == 1:
            # Only one song in the queue
            embed.description = f"1. {self.queue[0]}"
        else:
            # Multiple songs in the queue
            for i, url in enumerate(self.queue):
                # Extract video title using youtube-dl (optional, for a richer embed)
                with YoutubeDL() as ydl:
                    try:
                        info = ydl.extract_info(url, download=False)
                        if isinstance(info, dict):
                            title = info['title'] if 'title' in info else url
                        else:
                            raise ExtractorError("Info is not a dictionary")
                    except ExtractorError:
                        title: str = url
                embed.add_field(name=f"{i+1}.", value=title, inline=False)

        # Show the next song (if any)
        if len(self.queue) > 1:
            embed.set_footer(text=f"Now Playing: {self.queue[0]}")

        await context.send(embed=embed)


async def setup(bot: Mobius) -> None:
    """Used to load cog into bot"""
    await bot.add_cog(Youtube(bot))
