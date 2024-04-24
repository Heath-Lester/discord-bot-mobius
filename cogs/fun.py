"""Discord Bot Cog File"""

import random
from aiohttp import ClientSession
from discord import ButtonStyle, Interaction, SelectOption, Embed
from discord.app_commands import describe
from discord.ext.commands import Cog, Context
from discord.ext.commands import hybrid_command
from discord.ui import View, Select, Button
from discord.ui import button
from bot import Mobius


class Choice(View):
    """Choice view for Heads and Tails Game"""

    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @button(label="Heads", style=ButtonStyle.blurple)
    async def confirm(self, interaction: Interaction, button: Button) -> None:
        """Heads button"""
        self.value = "heads"
        self.stop()

    @button(label="Tails", style=ButtonStyle.blurple)
    async def cancel(self, interaction: Interaction, button: Button) -> None:
        """Tails button"""
        self.value = "tails"
        self.stop()


class RockPaperScissors(Select):
    """Rock Paper Scissors Select Game"""

    def __init__(self) -> None:
        options = [
            SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**That's a draw!**\nYou've chosen {
                user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**You won!**\nYou've chosen {
                user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**You lost!**\nYou've chosen {
                user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(View):
    """View for Rock Paper Scissors Game"""

    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(Cog, name="Fun"):
    """Class containing Bot Text Games"""

    def __init__(self, bot: Mobius) -> None:
        self.bot = bot

    @hybrid_command(name="randomfact", aliases=['factoid'], description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = Embed(
                        description=data["text"], color=0xD75BF4)
                else:
                    embed = Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @hybrid_command(
        name="coinflip", aliases=['headsortails'], description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = Embed(
                description=f"Correct! You guessed `{
                    buttons.value}` and I flipped the coin to `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{
                    result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @hybrid_command(
        name="rps", aliases=["rockpaperscissors", "rock paper scissors"], description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    @hybrid_command(
        name="8ball",
        aliases=['eightball'],
        description="Ask any question to the bot.",
    )
    @describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"The question was: {question}")
        await context.send(embed=embed)


async def setup(bot: Mobius) -> None:
    """Used to load cog into bot"""
    await bot.add_cog(Fun(bot))
