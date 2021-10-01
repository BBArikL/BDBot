import discord
from discord.ext import commands
from Scripts import BDbot
from Comics_details import comDetails


class Help(commands.Cog):
    # Class responsible for sending help embeds

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.stripDetails = comDetails.load_details()

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):  # Custom Help command
        embed = discord.Embed(title="BDBot!")

        embed.add_field(name="Gocomics",
                        value="Use bd!help gocomics to get all comics that are supported on the Gocomics "
                              "website.\nCommands:\n`bd!<name-of-comic> today / random / dd/mm/YYY`.")
        embed.add_field(name="XKCD", value="Aliases: 'xkcd', \n'xk'\nCommands:\nbd!XKCD today / random / # of comic.")
        embed.add_field(name= 'Cyanide and Happiness', value="Aliases: 'Cyanide',\n'cyanide',\n'Cyanide&Happiness', "
                                                             "\n'cyan'\nCommands:\n!cyanide today / random / # of comic.")
        embed.add_field(name= 'Garfield minus Garfield', value="Aliases: 'Garfieldminus', \n'garfminus', \n'gmng', \n'GamnG'"
                                                               "\nCommands:\n!Garfieldminus today / random / date of comic.")
        
        embed.add_field(name="Daily comics commands.",
                        value="Use bd!help daily to see available commands for daily comics. Post daily at 6:00 AM UTC.")
        
        embed.add_field(name="Request", value="Have a request for the bot? Post your request at "
                                              "https://github.com/BBArikL/BDBot/issues/new?assignees=&labels=enhancement&template=comic-request.md&title=New+Comic+request "
                                              "for maximum visibility or use bd!request <your request> to "
                                              "leave a message to the developer!")
        embed.add_field(name="Git", value="Link back to the git page.\nCommand:\n`bd!git`.")
        embed.add_field(name="Invite", value="Gives a link to add the bot to your servers.\nCommand:\n`bd!invite`.")
        
        embed.add_field(name="Vote", value="Link back to the Top.gg page.\nCommand:\n`bd!vote`.")

        embed.set_footer(text=BDbot.BDBot.get_random_footer(self))
        await ctx.send(embed=embed)

    @help.command()
    async def daily(self, ctx):  # help for daily commands
        embed = discord.Embed(title="Daily commands!")

        embed.add_field(name="add", value="Use `bd!<name_of_comic> add` to add the comic to the daily list.")
        embed.add_field(name="remove", value="Use `bd!<name_of_comic> remove` to remove the comic to the daily list.")
        embed.add_field(name="Remove all", value="Use `bd!remove_all` to unsubscribe your server from all the comics")

        embed.set_footer(text=BDbot.BDBot.get_random_footer(self))
        await ctx.send(embed=embed)

    @help.command()
    async def gocomics(self, ctx):
        embed = discord.Embed(title="Gocomics!")

        embed.add_field(name="Garfield", value="Aliases: 'Garf', 'garf', 'garfield'.")
        embed.add_field(name="Garfield classics",
                        value="Aliases: 'GarfieldClassics', 'GarfClassic', 'garfieldclassic', 'garfcl', 'GarfCl'.")
        embed.add_field(name="Calvin and Hobbes", value="Aliases: 'CalvinandHobbes', 'C&H', 'c&h', 'CH', 'ch'.")
        embed.add_field(name="Peanuts", value="Aliases: 'peanut', 'peanuts', 'pean'.")
        embed.add_field(name="Peanuts Begins",
                        value="Aliases: 'PeanutsBegins', 'peanutsbegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'.")
        embed.add_field(name="Dilbert classics", value="Aliases: 'Dilbert', 'dilbert', 'Dilb', 'dilb'.")
        embed.add_field(name="Frazz", value="Aliases:'frazz'.")
        embed.add_field(name='Frank and Ernest by Thaves', value="Aliases: 'Frank', 'frank', 'Ernest', 'ernest', "
                                                                 "'Frank&Ernest', 'frank&ernest'.")
        embed.add_field(name='Broom Hilda', value="Aliases: 'Broom', 'broom', 'Hilda', 'hilda'.")
        embed.add_field(name='Inspector Dangers Crime Quiz', value="Aliases: 'Inspector', 'inspector', 'crime', 'crimequiz'.")
        embed.add_field(name='Cheer up Emo kid', value="Aliases: 'emo', 'Emo', 'Cheerup', 'emokid'.")
        embed.add_field(name='Catana comics', value="Aliases: 'Catana', 'catana', 'littlemoments'.")
        embed.add_field(name='Brevity', value="Aliases: 'brevity', 'brev'.")

        embed.set_footer(text=BDbot.BDBot.get_random_footer(self))
        await ctx.send(embed=embed)


def setup(client):  # Initialize the cog
    client.add_cog(Help(client))
