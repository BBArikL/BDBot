import discord
from discord import app_commands
from discord.ext import commands

from bdbot import discord_utils, utils
from bdbot.comics.base import Website
from bdbot.comics.comicskingdom import ComicsKingdom
from bdbot.comics.gocomics import Gocomics
from bdbot.comics.webtoons import Webtoons
from bdbot.Embed import Embed


class HelpCommands(commands.Cog):
    """Class responsible for sending help embeds"""

    help_group = app_commands.Group(name="help", description="Help commands")

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.bot: commands.Bot = bot

    @help_group.command()
    async def general(self, inter: discord.Interaction):
        """Help commands for BDBot"""
        strips = utils.strip_details
        help_embed: Embed = Embed(title="", description=None, fields=[])
        embed = discord.Embed(title=help_embed.title)

        for website in [Gocomics, ComicsKingdom, Webtoons]:
            embed.add_field(
                name=website.WEBSITE_NAME,
                value=website.WEBSITE_HELP,
            )

        for strip in strips:
            if strips[strip]["Main_website"] not in [
                Website.Gocomics.value,
                Website.ComicsKingdom.value,
                Website.Webtoons.value,
            ]:
                embed.add_field(
                    name=strips[strip]["Name"], value=strips[strip]["Helptxt"]
                )

        for field in help_embed.fields:
            embed.add_field(**field)

        # Saves the embed for later use
        return await discord_utils.send_embed(inter, [embed])

    @help_group.command()
    async def schedule(self, inter: discord.Interaction):
        """Get help to schedule an automatic comic post"""
        schedule_embed: Embed = Embed(title="", description="", fields=[])
        embed = discord.Embed(
            title=schedule_embed.title,
            description=schedule_embed.description,
        )
        for field in schedule_embed.fields:
            embed.add_field(**field)

        return await discord_utils.send_embed(inter, [embed])

    @help_group.command()
    async def gocomics(self, inter: discord.Interaction):
        """Gocomics help"""
        website_name = "Gocomics"
        website = "https://www.gocomics.com/"
        embeds: list[discord.Embed]

        embeds = discord_utils.website_specific_embed(website_name, website)
        await discord_utils.send_embed(inter, embeds)

    @help_group.command()
    async def comicskingdom(self, inter: discord.Interaction):
        """Comics Kingdom help"""
        website_name = "Comics Kingdom"
        website = "https://comicskingdom.com/"
        embeds: list[discord.Embed]

        if discord_utils.KINGDOM_EMBED is None:
            embeds = discord_utils.website_specific_embed(website_name, website)
            utils.KINGDOM_EMBED = embeds
        else:
            embeds = discord_utils.KINGDOM_EMBED

        await discord_utils.send_embed(inter, embeds)

    @help_group.command()
    async def webtoons(self, inter: discord.Interaction):
        """Webtoons help"""
        website_name = "Webtoons"
        website = "https://www.webtoons.com/en/"
        embeds: list[discord.Embed]

        if discord_utils.WEBTOONS_EMBED is None:
            embeds = discord_utils.website_specific_embed(website_name, website)
            utils.WEBTOONS_EMBED = embeds
        else:
            embeds = discord_utils.WEBTOONS_EMBED

        await discord_utils.send_embed(inter, embeds)

    @app_commands.command()
    async def new(self, inter: discord.Interaction):
        """New features of the bot"""
        embed: discord.Embed

        if discord_utils.NEW_EMBED is None:
            embed = discord.Embed(
                title="New features",
                description="Find out what new features have been implemented "
                "since the last update!",
            )
            embed.add_field(
                name="Thanks",
                value="First, I want to take a moment to thank all of you who use BDBot to view your "
                "favorite comics! It recently got approved by Discord and also has exceeded the 100 "
                "server limit which is phenomenal! Thank you again for your trust into this "
                "project! :)",
            )
            embed.add_field(
                name="New comics",
                value="The new comics are: Chibird, War and Peas, Humans are stupid,"
                " Maximumble, Poorly Drawn Lines, Heathcliff, Andy Capp",
            )
            embed.add_field(
                name="Latest comics",
                value="You want to have only the latest comics? Put `latest` in the date parameter of any"
                " comic when adding it to the subscription list and the bot will only give you back"
                " the latest comics when they are available!",
            )
            embed.add_field(
                name="Optimizations",
                value="Under the hood, optimizations have been made to the bot to make it more responsive"
                " and support the growth!",
            )
            utils.NEW_EMBED = embed
        else:
            embed = discord_utils.NEW_EMBED

        await discord_utils.send_embed(inter, [embed])

    @app_commands.command()
    async def faq(self, inter: discord.Interaction):
        """FAQ of the bot"""
        embed: discord.Embed

        if discord_utils.FAQ_EMBED is None:
            embed = discord.Embed(
                title="FAQ",
                description="Have a question on the bot? This is the place you are looking for!",
            )
            embed.add_field(
                name="What is this bot?",
                value="This bot is a helper to keep up with your favorite comics! It search each hour more"
                " than 40+ pages to fetch the most up to date comics for your eyes only!",
            )
            embed.add_field(
                name="Why can I only go up to 7 comics in the past for ComicKingdom's comics?",
                value="ComicKingdom use a premium membership to view older comics. You can go on their "
                "site to get one and see the comics directly in your browser.",
            )
            embed.add_field(
                name="How can I support the project?",
                value="You can vote for the bot on top.gg (`/vote`) or star the project on GitHub (`/git`)."
                " If you want to support one of the comics that are presented through this bot, go on"
                " their page to see how to support them directly!",
            )
            embed.add_field(
                name="How can I request comics?",
                value="You can use `/request` to request comics or features directly to the developer.",
            )
            embed.add_field(
                name="How can I receive scheduled comics?",
                value="You can use `/help schedule` to get help on how to schedule comics.",
            )
            embed.add_field(
                name="What information is collected by using this bot?",
                value="No personal information is used by this bot if you only use it to read comics. The "
                "information collected by the bot when a comic is scheduled is: the ID of the server,"
                " the ID of the channel, the ID of the role to mention, the server's mention policy"
                " and the information about the scheduled comic itself. This information is deleted "
                "when the bot loses access to the server or when all comics of the server have "
                "been unscheduled. When you use `/request`, your username, your discriminator, "
                "the time of the message and the message itself is logged to prevent abuse and "
                "relevance of the request. To delete this personal information (and get rid of the "
                "requests sent), use `/delete_request`.",
                inline=False,
            )
            utils.FAQ_EMBED = embed
        else:
            embed = discord_utils.FAQ_EMBED

        await discord_utils.send_embed(inter, [embed])


async def setup(bot: commands.Bot):
    """Initialize the cog"""
    await bot.add_cog(HelpCommands(bot))
