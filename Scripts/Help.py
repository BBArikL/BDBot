import discord
from discord.ext import commands
from Comics_details import comDetails
import utils


class Help(commands.Cog):
    # Class responsible for sending help embeds

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.strip_details = comDetails.load_details()

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):  # Custom Help command
        strips = self.strip_details
        embed = discord.Embed(title="BDBot!")

        embed.add_field(name="Gocomics",
                        value="Use bd!help gocomics to get all comics that are supported on the Gocomics "
                              "website.\nCommands:\n`bd!<name-of-comic> today / random / dd/mm/YYY`.")
        for strip in strips:
            if strips[strip]["Main_website"] != "https://www.gocomics.com/":
                embed.add_field(name=strips[strip]['Name'], value=f"{strips[strip]['Helptxt']}\nAliases: "
                                                                  f"{strips[strip]['Aliases']} / random "
                                                                  f"/ # or date of comic.")
        embed.add_field(name="Daily comics commands.",
                        value="Use bd!help daily to see available commands for daily comics. "
                              "Post daily at 6:00 AM UTC.")

        embed.add_field(name="Request", value="Have a request for the bot? Post your request at "
                                              "https://github.com/BBArikL/BDBot/issues/new?assignees=&labels"
                                              "=enhancement&template=comic-request.md&title=New+Comic+request "
                                              "for maximum visibility or use `bd!request <your request>` to "
                                              "leave a message to the developer!")
        embed.add_field(name="Git", value="Gives the link of the git page.\nCommand:\n`bd!git`.")
        embed.add_field(name="Invite", value="Gives a link to add the bot to your servers!\nCommand:\n`bd!invite`.")

        embed.add_field(name="Vote", value="Vote for the bot on Top.gg!\nCommand:\n`bd!vote`.")

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    @help.command()
    async def daily(self, ctx):  # help for daily commands
        embed = discord.Embed(title="Daily commands!")

        embed.add_field(name="add", value="Use `bd!<name_of_comic> add` to add the comic to the daily list.")
        embed.add_field(name="remove", value="Use `bd!<name_of_comic> remove` to remove the comic to the daily list.")
        embed.add_field(name="Remove all", value="Use `bd!remove_all` to unsubscribe your server from all the comics")

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    # Gocomics help embed
    @help.command()
    async def gocomics(self, ctx):
        website_name = "Gocomics"
        website = "https://www.gocomics.com/"

        await self.website_specific_embed(ctx, website_name, website)

    # Create a embed with all the specific comics from a website
    async def website_specific_embed(self, ctx, website_name, website, nb_per_embed=1000000):
        strips = self.strip_details
        i = 0

        embed = discord.Embed(title=f"{website_name}!")
        embed.set_footer(text=utils.get_random_footer())
        for strip in strips:
            if strips[strip]["Main_website"] == website:
                i += 1

                embed.add_field(name=strips[strip]['Name'], value=f"{strips[strip]['Helptxt']}\nAliases: "
                                                                  f"{strips[strip]['Aliases']}")
                if i == nb_per_embed:
                    await ctx.send(embed=embed)
                    i = 0
                    # Reset the embed to create a new one
                    embed = embed = discord.Embed(title=f"{website_name}!")
                    embed.set_footer(text=utils.get_random_footer())

        if i != 0:
            await ctx.send(embed=embed)


def setup(client):  # Initialize the cog
    client.add_cog(Help(client))
