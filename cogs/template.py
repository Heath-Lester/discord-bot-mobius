"""Discord Bot Cog File"""

from discord.ext import commands
from discord.ext.commands import Context
from bot import Mobius


# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="Template"):
    """Template Cog Class"""

    def __init__(self, bot: Mobius) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="testcommand",
        description="This is a testing command that does nothing.",
    )
    async def testcommand(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot: Mobius) -> None:
    """Used to load cog into bot"""
    await bot.add_cog(Template(bot))
