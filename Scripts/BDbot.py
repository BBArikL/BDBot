import sys

sys.path.insert(0, "./Scripts/")
import discord
from discord.ext import commands
from datetime import datetime, timezone
import os
import topgg
from Comics_details import comDetails
from DailyPoster import DailyPosterHandler
import utils


class BDBot(commands.Cog):
    # Class responsible for main functions of the bot

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.strip_details = comDetails.load_details()
        self.client = client
        dbl_token = str(os.getenv('TOP_GG_TOKEN'))  # top.gg token
        self.topggpy = topgg.DBLClient(client, dbl_token)

    @commands.Cog.listener()
    async def on_ready(self):
        # Change bot's activity
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='bd!help'))

        print("Logged in as {0.user}".format(self.client))
        channel_id = int(os.getenv('PRIVATE_CHANNEL_SUPPORT_ID'))

        channel = self.client.get_channel(channel_id)

        await channel.send(
            "Bot restarted. I will now try to restart the loop.")  # Sends this message whenever restarting the bot

        await DailyPosterHandler.wait_for_daily(DailyPosterHandler(client=self.client))  # Wait for daily poster

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        utils.remove_guild(guild, use="auto_remove_guild")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, deleted_channel):
        utils.remove_channel(deleted_channel, use="auto_remove_channel")

    @commands.command(aliases=['Git', 'github', 'Github'])
    async def git(self, ctx):  # Links back to the github page
        await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):  # Creates a Oauth2 link to share the bot
        inv = discord.utils.oauth_url(os.getenv('CLIENT_ID'))
        await ctx.send(f'Share the bot! {inv}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)  # Only mods can add comics
    async def add_all(self, ctx, date=None, hour=None):  # Adds all comics to a specific channel
        status = utils.add_all(ctx, date, hour)
        if status == utils.Success:
            await ctx.send("All comics added successfully!")
        else:
            await ctx.send(status)

    @commands.command(aliases=["remove_guild"])
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the server from the database
    async def remove_all(self, ctx):  # Remove the guild from the database
        status = utils.remove_guild(ctx)

        if status == utils.Success:
            await ctx.send("All daily comics removed successfully!")
        else:
            await ctx.send(status)

    @commands.command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the channel from the database
    async def remove_channel(self, ctx):  # Remove the channel from the database
        status = utils.remove_channel(ctx)
        if status == utils.Success:
            await ctx.send("All daily comics removed successfully from this channel!")
        else:
            await ctx.send(status)

    @commands.command()
    @commands.has_permissions(manage_guild=True)  # Only mods can add a role
    async def set_role(self, ctx, role: discord.Role):  # Add a role to be notified
        if discord.Guild.get_role(ctx.guild, role.id) is not None:
            status = utils.set_role(ctx, role)
            if status == utils.Success:
                await ctx.send("Role successfully added to be notified! "
                               "This role will get mentioned at each comic post. "
                               "If you wish to be only notified for daily comics happening at 6 AM UTC, use "
                               "`bd!set_mention no`.")
            else:
                await ctx.send(status)
        else:
            await ctx.send("The role is invalid or not provided!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the role
    async def remove_role(self, ctx):  # Deletes the role mention
        status = utils.remove_role(ctx)

        if status == utils.Success:
            await ctx.send("Role mention successfully removed!")
        else:
            await ctx.send(status)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def set_mention(self, ctx, choice):  # Change the mention
        choice = (0, 1)[choice.lower()[0] == "y"]

        status = utils.set_mention(ctx, choice)

        if status == utils.Success:
            await ctx.send("Successfully changed the mention policy for this server!")
        else:
            await ctx.send(status)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def get_mention(self, ctx):  # Get the mention policy
        status, mention_policy = utils.get_mention(ctx)

        if status == utils.Success:
            await ctx.send(f"The bot will mention the role {mention_policy}!")
        else:
            await ctx.send(status)

    @commands.command()
    async def vote(self, ctx):  # Links back to the github page
        await ctx.send(
            "Vote for the bot here: https://top.gg/bot/807780409362481163 and / or here : "
            "https://discordbotlist.com/bots/bdbot")

    @commands.command()
    async def nb_guild(self, ctx):  # Gets the number of guilds that the bot is in (for analytics)
        if ctx.message.author.id == int(os.getenv('BOT_OWNER_ID')):
            await ctx.send(f"The bot is in {len(self.client.guilds)} guilds. Trying to update status on Top.gg.....")

            try:
                await self.topggpy.post_guild_count()
                await ctx.send(f'Posted server count ({self.topggpy.guild_count})')
            except Exception as e:
                await ctx.send('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.command()
    async def request(self, ctx, *, param=None):
        # Adds a request to the database
        FILE_PATH = './data/requests.txt'

        requests = open(FILE_PATH, 'a')

        requests.write(
            f'Request: "{param}" by {ctx.author.name}#{ctx.author.discriminator} on {datetime.now(timezone.utc)}\n')

        requests.close()

        await ctx.send("Request saved! Thank you for using BDBot!")

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["subs", "subscriptions", "subscription"])
    async def sub(self, ctx):  # Checks if the server is subbed to any comic
        guild_data = utils.get_specific_guild_data(ctx)

        if guild_data is not None:
            comic_list = []
            comic_values = list(self.strip_details.values())

            for channel in guild_data["channels"]:
                for day in guild_data["channels"][channel]["date"]:
                    for hour in guild_data["channels"][channel]["date"][day]:
                        for comic in guild_data["channels"][channel]["date"][day][hour]:
                            comic_name = comic_values[comic]["Name"]
                            comic_list.append({
                                "Name": comic_name,
                                "Hour": hour,
                                "Date": day,
                                "Channel": self.client.get_channel(int(channel)).mention
                            })

            if len(comic_list) > 0:
                matching_date = utils.match_date
                embed = discord.Embed(title="This guild is subscribed to:")
                for comic in comic_list:
                    embed.add_field(name=comic['Name'], value=f"Each {matching_date[comic['Date']]} at {comic['Hour']}h"
                                                              f" UTC in channel {comic['Channel']}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("This guild is not subscribed to any comic!")
        else:
            await ctx.send("This guild is not subscribed to any comic!")

    @commands.command()
    async def kill(self, ctx):
        if utils.is_owner(ctx):
            # Close the bot connection
            await ctx.send("Closing bot....")

            await self.client.close()
        else:
            raise discord.ext.commands.CommandNotFound

    # ---- End of commands ----#
    # ---- End of BDBot ----#


def setup(client):  # Initialize the cog
    client.add_cog(BDBot(client))
