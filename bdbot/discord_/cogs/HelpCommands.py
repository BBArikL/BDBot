import discord
from discord import app_commands
from discord.ext import commands

from bdbot.comics.comicskingdom import ComicsKingdom
from bdbot.comics.gocomics import Gocomics
from bdbot.comics.webtoons import Webtoons
from bdbot.discord_.client import BDBotClient
from bdbot.discord_.discord_utils import send_embed
from bdbot.embed import Embed
from bdbot.files import HELP_EMBED_PATH, load_json
from bdbot.help import (
    HELP_FAQ_NAME,
    HELP_GENERAL_NAME,
    HELP_NEW_NAME,
    HELP_SCHEDULE_NAME,
    get_general_help,
)


class HelpCommands(commands.Cog):
    """Class responsible for sending help embeds"""

    help_group = app_commands.Group(name="help", description="Help commands")
    help_dict: dict[str, dict[str, dict[str, str]]]

    def __init__(self, bot: BDBotClient):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.bot: BDBotClient = bot
        self.help_dict = load_json(HELP_EMBED_PATH)

    @help_group.command()
    async def general(self, inter: discord.Interaction):
        """Help commands for BDBot"""
        return await send_embed(
            inter,
            [
                get_general_help(
                    self.help_dict[HELP_GENERAL_NAME], self.bot.comic_details
                )
            ],
        )

    @help_group.command()
    async def schedule(self, inter: discord.Interaction):
        """Get help to schedule an automatic comic post"""
        return await send_embed(
            inter, [Embed.from_dict(self.help_dict[HELP_SCHEDULE_NAME])]
        )

    @help_group.command()
    async def gocomics(self, inter: discord.Interaction):
        """Gocomics help"""
        await send_embed(inter, Gocomics.get_website_help_embed(self.bot))

    @help_group.command()
    async def comicskingdom(self, inter: discord.Interaction):
        """Comics Kingdom help"""
        await send_embed(inter, ComicsKingdom.get_website_help_embed(self.bot))

    @help_group.command()
    async def webtoons(self, inter: discord.Interaction):
        """Webtoons help"""
        await send_embed(inter, Webtoons.get_website_help_embed(self.bot))

    @app_commands.command()
    async def new(self, inter: discord.Interaction):
        """New features of the bot"""
        await send_embed(inter, [Embed.from_dict(self.help_dict[HELP_NEW_NAME])])

    @app_commands.command()
    async def faq(self, inter: discord.Interaction):
        """FAQ of the bot"""
        await send_embed(inter, [Embed.from_dict(self.help_dict[HELP_FAQ_NAME])])


async def setup(bot: BDBotClient):
    """Initialize the cog"""
    await bot.add_cog(HelpCommands(bot))
