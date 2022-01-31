import discord
from discord.ext import commands
from src import utils


class Help(commands.Cog):
    # Class responsible for sending help embeds

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.strip_details = utils.load_details()

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):  # Custom Help command
        strips = self.strip_details
        embed = discord.Embed(title="BDBot!")

        embed.add_field(name="Gocomics",
                        value="Use bd!help gocomics to get all comics that are supported on the Gocomics "
                              "website.\nCommands:\n`bd!<name-of-comic> today / random / dd/mm/YYY`.")
        embed.add_field(name="Comics Kingdom",
                        value="Use bd!help comicskingdom to get all comics that are supported on the Comics Kingdom "
                              "website.\nCommands:\n`bd!<name-of-comic> today / random / dd/mm/YYY`.")
        embed.add_field(name="Webtoons",
                        value="Use bd!help webtoons to get all comics that are supported on the Webtoons "
                              "website.\nCommands:\n`bd!<name-of-comic> today / random / dd/mm/YYY`.")
        for strip in strips:
            if strips[strip]["Main_website"] != "https://www.gocomics.com/" \
                    and strips[strip]["Main_website"] != "https://comicskingdom.com/" \
                    and strips[strip]["Main_website"] != "https://www.webtoons.com/en/" :
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
        embed.add_field(name="Status", value="Gives back the status of the bot.\nCommand:\n`bd!status`")
        embed.add_field(name="Ping", value="Pong! Gives back the bot latency.\nCommand:\n`bd!ping`")
        embed.add_field(name="Uptime", value="Gives back the uptime.\nCommand:\n`bd!up`")
        embed.add_field(name="Git", value="Gives the link of the git page.\nCommand:\n`bd!git`")
        embed.add_field(name="Invite", value="Gives a link to add the bot to your servers!\nCommand:\n`bd!invite`")

        embed.add_field(name="Vote", value="Vote for the bot on Top.gg!\nCommand:\n`bd!vote`")

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    @help.command()
    async def daily(self, ctx):  # help for daily commands
        embed = discord.Embed(title="Daily commands!", description="Date and hour are optional arguments that can "
                                                                   "specify when the the bot should send the comic. A "
                                                                   "date should be one of the seven days of the week"
                                                                   "and the hour a number representing the time in a "
                                                                   "24h clock in UTC time. If not specified, "
                                                                   "defaults to the current time in UTC.")
        embed.add_field(name="Post", value="The bot did not post the comics or you want to be sure that all comics "
                                           "are correctly set up? Use `bd!post <date> <hour>` to force the post of "
                                           "comics set at the specified time.")
        embed.add_field(name="Add", value="Use `bd!<name_of_comic> add <date> <hour>` to add the comic to the daily "
                                          "list of the channel.")
        embed.add_field(name="Add all", value="Use `bd!add_all <date> <hour>` to add all the comics to a specific day "
                                              "of the week and hour.")
        embed.add_field(name="Remove", value="Use `bd!<name_of_comic> remove <date> <hour>` to remove the comic "
                                             "from the daily list.")
        embed.add_field(name="Remove channel", value="Use `bd!remove_channel` to unsubscribe your channel from all the "
                                                     "comics")
        embed.add_field(name="Remove all", value="Use `bd!remove_all` to unsubscribe your server from all the comics "
                                                 "in all the channels.")
        embed.add_field(name="Subscriptions", value="Use `bd!sub` to view all subscribed comics for this server.")
        embed.add_field(name="Set role mention", value="Use `bd!set_role @<role>` to add a role to mention for "
                                                       "comics posts. To remove, use `bd!remove_role`.")
        embed.add_field(name="Mange role mention", value="Use `bd!set_mention daily/all` to change the mention policy "
                                                         "for the bot in the server. This does not affect daily comics "
                                                         "posted at 6h AM UTC. If the mention policy is set to 'all',"
                                                         " the bot will mention the role at each comic post, otherwise"
                                                         " it will only mention the role at 6h AM UTC daily.")
        embed.add_field(name="Enable/Disable mention", value="Use `bd!post_mention` to enable/disable server-wide the "
                                                             "mention right before the automatic comic posts.")
        embed.add_field(name="Get mention policy", value="Use `bd!get_mention` to get the server's mention policy.")

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    # Gocomics help embed
    @help.command()
    async def gocomics(self, ctx):
        website_name = "Gocomics"
        website = "https://www.gocomics.com/"

        await self.website_specific_embed(ctx, website_name, website)

    # Comics Kingdom help embed
    @help.command()
    async def comicskingdom(self, ctx):
        website_name = "Comics Kingdom"
        website = "https://comicskingdom.com/"

        await self.website_specific_embed(ctx, website_name, website)

    # Webtoons help embed
    @help.command()
    async def webtoons(self, ctx):
        website_name = "Webtoons"
        website = "https://www.webtoons.com/en/"

        await self.website_specific_embed(ctx, website_name, website)

    # Create a embed with all the specific comics from a website
    async def website_specific_embed(self, ctx, website_name, website):
        nb_per_embed = 25
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
                    embed = discord.Embed(title=f"{website_name}!")
                    embed.set_footer(text=utils.get_random_footer())

        if i != 0:
            await ctx.send(embed=embed)


def setup(client):  # Initialize the cog
    client.add_cog(Help(client))
