import discord
from discord.ext import commands
from src import utils, discord_utils


class Help(commands.Cog):
    """Class responsible for sending help embeds"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.bot: commands.Bot = bot

    @commands.hybrid_group()
    async def help(self, ctx):
        pass

    @help.command()
    async def general(self, ctx: commands.Context):
        """Help for BDBot"""
        embed: discord.Embed
        if discord_utils.HELP_EMBED is None:
            strips = utils.strip_details
            embed = discord.Embed(title="BDBot!")

            embed.add_field(name="Gocomics",
                            value="Use /help gocomics to get all comics that are supported on the Gocomics "
                                  "website.\nCommands:\n`/<name-of-comic> today / random / dd/mm/YYY`.")
            embed.add_field(name="Comics Kingdom",
                            value="Use /help comicskingdom to get all comics that are supported on the Comics Kingdom "
                                  "website.\nCommands:\n`/<name-of-comic> today / random / dd/mm/YYY`.")
            embed.add_field(name="Webtoons",
                            value="Use /help webtoons to get all comics that are supported on the Webtoons "
                                  "website.\nCommands:\n`/<name-of-comic> today / random / dd/mm/YYY`.")
            for strip in strips:
                if strips[strip]["Main_website"] != "https://www.gocomics.com/" \
                        and strips[strip]["Main_website"] != "https://comicskingdom.com/" \
                        and strips[strip]["Main_website"] != "https://www.webtoons.com/en/":
                    embed.add_field(name=strips[strip]['Name'], value=f"{strips[strip]['Helptxt']}\nAliases: "
                                                                      f"{strips[strip]['Aliases']} / random "
                                                                      f"/ # or date of comic.")
            embed.add_field(name="Hourly comics commands.",
                            value="Use /help hourly to see available commands for daily comics. "
                                  "Post daily at 6:00 AM UTC.")

            embed.add_field(name="Request", value="Have a request for the bot? Post your request at "
                                                  "https://github.com/BBArikL/BDBot/issues/new?assignees=&labels"
                                                  "=enhancement&template=comic-request.md&title=New+Comic+request "
                                                  "for maximum visibility or use `/request <your request>` to "
                                                  "leave a message to the developer!")
            embed.add_field(name="Status", value="Gives back the status of the bot.\nCommand:\n`/status`")
            embed.add_field(name="Ping", value="Pong! Gives back the bot latency.\nCommand:\n`/ping`")
            embed.add_field(name="Uptime", value="Gives back the uptime.\nCommand:\n`/up`")
            embed.add_field(name="FAQ", value="Have any question on the bot? This FAQ (`/faq`) might have the response "
                                              "you need!")
            embed.add_field(name="New commands", value="See the the newly added commands by using `/new`")
            embed.add_field(name="Git", value="Gives the link of the git page.\nCommand:\n`/git`")
            embed.add_field(name="Invite", value="Gives a link to add the bot to your servers!\nCommand:\n`/invite`")
            embed.add_field(name="Vote", value="Vote for the bot on Top.gg!\nCommand:\n`/vote`")

            # Saves the embed for later use
            utils.HELP_EMBED = embed
        else:
            embed = discord_utils.HELP_EMBED  # Get the cached value
        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    @help.command()
    async def hourly(self, ctx):
        """Help for hourly commands"""
        embed: discord.Embed

        if discord_utils.HOURLY_EMBED is None:

            embed = discord.Embed(title="Daily commands!", description="Date and hour are optional arguments that can "
                                                                       "specify when the the bot should send the "
                                                                       "comic. A date should be one of the seven days "
                                                                       "of the week and the hour a number "
                                                                       "representing the time in a 24h clock in UTC "
                                                                       "time. If not specified, defaults to the "
                                                                       "current time in UTC.")
            embed.add_field(name="Post", value="The bot did not post the comics or you want to be sure that all comics "
                                               "are correctly set up? Use `/post <date> <hour>` to force the post of "
                                               "comics set at the specified time.")
            embed.add_field(name="Add", value="Use `/<name_of_comic> add <date> <hour>` to add the comic to the daily "
                                              "list of the channel.")
            embed.add_field(name="Add all", value="Use `/add_all <date> <hour>` to add all the comics to a specific "
                                                  "day of the week and hour.")
            embed.add_field(name="Remove", value="Use `/<name_of_comic> remove <date> <hour>` to remove the comic "
                                                 "from the daily list.")
            embed.add_field(name="Remove channel", value="Use `/remove_channel` to unsubscribe your channel from all "
                                                         "the comics")
            embed.add_field(name="Remove all", value="Use `/remove_all` to unsubscribe your server from all the comics "
                                                     "in all the channels.")
            embed.add_field(name="Subscriptions", value="Use `/sub` to view all subscribed comics for this server.")
            embed.add_field(name="Set role mention", value="Use `/set_role @<role>` to add a role to mention for "
                                                           "comics posts. To remove, use `/remove_role`.")
            embed.add_field(name="Mange role mention", value="Use `/set_mention daily/all` to change the mention "
                                                             "policy for the bot in the server. This does not affect "
                                                             "daily comics posted at 6h AM UTC. If the mention policy "
                                                             "is set to 'all',  the bot will mention the role at each "
                                                             "comic post, otherwise  it will only mention the role at "
                                                             "6h AM UTC daily.")
            embed.add_field(name="Enable/Disable mention", value="Use `/post_mention` to enable/disable server-wide "
                                                                 "the mention right before the automatic comic posts.")
            embed.add_field(name="Get mention policy", value="Use `/get_mention` to get the server's mention policy.")

            utils.HOURLY_EMBED = embed
        else:
            embed = discord_utils.HOURLY_EMBED

        embed.set_footer(text=utils.get_random_footer())

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def new(self, ctx):
        """New features of the bot"""
        embed: discord.Embed

        if discord_utils.NEW_EMBED is None:
            embed = discord.Embed(title="New feature", description="Find out what new features have been implemented "
                                                                   "since the last update!")
            embed.add_field(name="Thanks", value="First, I want to take a moment to thank all of you who use BDBot to "
                                                 "view your favorite comics! It recently got approved by Discord and "
                                                 "also has exceeded the 100 server limit which is phenomenal! Thank "
                                                 "you again for your trust into this project! :)")
            embed.add_field(name="New comics", value="The new comics are: Pearls before Swine, Chibird, War and Peas, "
                                                     "Humans are stupid, Maximumble, Poorly Drawn Lines, Heathcliff, "
                                                     "Andy Capp")
            embed.add_field(name="Latest comics", value="You want to have only the latest comics? Put 'latest' in the "
                                                        "date parameter of any comic when adding it to the "
                                                        "subscription list and the bot will aunly give you back the "
                                                        "latest comics when they are available!")
            embed.add_field(name="Post", value="Missed your comics or just want to test that the bot can properly send "
                                               "all comics for a given time? Use `/post <date> <time>` to test it!")
            embed.add_field(name="Enable/Disable post announcement", value="Tired of seeing the announcement of the "
                                                                           "bot before it post scheduled comics? Use "
                                                                           "`/post_mention enable/disable` to change "
                                                                           "if the bot should announce when scheduled "
                                                                           "comics are posted.")
            embed.add_field(name="Status", value="Get the status of the bot with these 3 new commands: `/ping`, "
                                                 "`/uptime` and `/status`.")
            embed.add_field(name="Delete requests", value="Want to delete previous requests that that you sent? Use "
                                                          "`/request_delete` to delete all your previous requests.`")
            embed.add_field(name="FAQ", value="Have any question on the bot? This FAQ (`/faq`) might have the response "
                                              "you need!")
            embed.add_field(name="Optimizations", value="Under the hood, optimizations have been made to the bot to "
                                                        "make it more responsive and support the growth!")
            utils.NEW_EMBED = embed
        else:
            embed = discord_utils.NEW_EMBED

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def faq(self, ctx):
        """FAQ of the bot"""
        embed: discord.Embed

        if discord_utils.FAQ_EMBED is None:
            embed = discord.Embed(title="FAQ", description="Have a question on the bot? This is the place you are "
                                                           "looking for!")
            embed.add_field(name="What is this bot?", value="This bot is a helper to keep up with your favorite "
                                                            "comics! It search each hour more than 40+ pages to fetch "
                                                            "the most up to "
                                                            "date comics for your eyes only!")
            embed.add_field(name="Why can I only go up to 7 comics in the past for ComicKingdom's comics?",
                            value="ComicKingdom use a premium membership to view older comics. You can go on their "
                                  "site to get one and see the comics directly on your browser.")
            embed.add_field(name="How can I support the project?", value="You can vote for the bot on top.gg (`/vote`) "
                                                                         "or star the project on GitHub (`/git`). If "
                                                                         "you want to support one of the comics that "
                                                                         "are presented through this bot, go on their "
                                                                         "page to see how to support them directly!")
            embed.add_field(name="How can I request comics?", value="You can use `/request <request>` to request "
                                                                    "comics or features directly to the developer.")
            embed.add_field(name="How can I receive scheduled comics?", value="You can use `/help daily` to get help "
                                                                              "on how to schedule comics.")
            embed.add_field(name="What information is collected by using this bot?", value="No personal information is "
                                                                                           "used by this bot if you "
                                                                                           "only use it to read "
                                                                                           "comics. The information "
                                                                                           "collected by the bot when "
                                                                                           "a comic is scheduled "
                                                                                           "is: the ID of the server, "
                                                                                           "the ID of the channel, "
                                                                                           "the ID of the role to "
                                                                                           "mention, the server's "
                                                                                           "mention policy and the "
                                                                                           "information about the "
                                                                                           "scheduled comic "
                                                                                           "itself. This information "
                                                                                           "is deleted when the bot "
                                                                                           "loses access to the "
                                                                                           "server or when all comics "
                                                                                           "of the server have "
                                                                                           "been unscheduled. When you "
                                                                                           "use `/request`, "
                                                                                           "your username, "
                                                                                           "your discriminator, "
                                                                                           "the time of the message "
                                                                                           "and the message itself is "
                                                                                           "logged to prevent abuse "
                                                                                           "and relevance of the "
                                                                                           "request. To delete this "
                                                                                           "personal information (and "
                                                                                           "get rid of the requests "
                                                                                           "sent), use "
                                                                                           "`/request_delete`.")
            utils.FAQ_EMBED = embed
        else:
            embed = discord_utils.FAQ_EMBED

        embed.set_footer(text=utils.get_random_footer())
        await ctx.send(embed=embed)

    @help.command(name="gocomics")
    async def gocomics(self, ctx: commands.Context):
        """Gocomics help"""
        website_name = "Gocomics"
        website = "https://www.gocomics.com/"
        embeds: list[discord.Embed]

        if discord_utils.GOCOMICS_EMBED is None:
            embeds = discord_utils.website_specific_embed(website_name, website)
            utils.GOCOMICS_EMBED = embeds
        else:
            embeds = discord_utils.GOCOMICS_EMBED

        await discord_utils.send_embed(ctx, self.bot, embeds)

    @help.command(name="comicskingdom")
    async def comicskingdom(self, ctx: commands.Context):
        """Comics Kingdom help"""
        website_name = "Comics Kingdom"
        website = "https://comicskingdom.com/"
        embeds: list[discord.Embed]

        if discord_utils.KINGDOM_EMBED is None:
            embeds = discord_utils.website_specific_embed(website_name, website)
            utils.KINGDOM_EMBED = embeds
        else:
            embeds = discord_utils.KINGDOM_EMBED

        await discord_utils.send_embed(ctx, self.bot, embeds)

    @help.command(name="webtoons")
    async def webtoons(self, ctx: discord.ext.commands.Context):
        """Webtoons help"""
        website_name = "Webtoons"
        website = "https://www.webtoons.com/en/"
        embeds: list[discord.Embed]

        if discord_utils.WEBTOONS_EMBED is None:
            embeds = discord_utils.website_specific_embed(website_name, website)
            utils.WEBTOONS_EMBED = embeds
        else:
            embeds = discord_utils.WEBTOONS_EMBED

        await discord_utils.send_embed(ctx, self.bot, embeds)


async def setup(bot: commands.Bot):
    """Initialize the cog"""
    await bot.add_cog(Help(bot))
