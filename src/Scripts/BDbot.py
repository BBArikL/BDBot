import logging
import math
import discord
from discord import ui
from discord.ext import commands
from datetime import datetime, timezone
import os
import topgg
import re

from typing import Union
from src.Scripts.AutomaticPoster import PosterHandler
from src import utils, discord_utils


class BDBot(commands.Cog):
    """Class responsible for main functions of the bot"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.strip_details: dict = utils.load_json(utils.DETAILS_PATH)
        self.bot: commands.Bot = bot
        self.topggpy = None
        self.start_time: datetime = datetime.now(timezone.utc)

    @commands.Cog.listener()
    async def on_ready(self):
        """On start of the bot"""
        # Change the bot activity
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=f'/help in {len(self.bot.guilds)} servers'))
        discord_utils.logger.log(logging.INFO, "Logged in as {0.user}".format(self.bot))
        channel_id: int = int(os.getenv('PRIVATE_CHANNEL_SUPPORT_ID'))

        channel: discord.TextChannel = self.bot.get_channel(channel_id)

        await channel.send(
            "Bot restarted. I will now try to sync the commands.")  # Sends this message whenever restarting the bot

        # Sync the commands
        guild: Union[None, discord.Guild] = None
        command_tree: discord.app_commands.CommandTree = self.bot.tree
        if os.getenv('DEBUG') == "True":
            guild = channel.guild
            command_tree.copy_global_to(guild=guild)
            await channel.send(f"Syncing commands to server {guild.name} ...")
        else:
            await channel.send("Syncing global commands...")

        await command_tree.sync(guild=guild)

        await channel.send("Finished syncing commands. An hour might be needed for global commands to be available!")

        async with self.bot:
            await PosterHandler.wait_for_next_hour(PosterHandler(self.bot))  # Wait for daily poster

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """When the bot is removed from a server"""
        discord_utils.remove_guild(guild, use="auto_remove_guild")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, deleted_channel: discord.abc.GuildChannel):
        """When a guild channel is deleted"""
        discord_utils.remove_channel(deleted_channel, use="auto_remove_channel")

    @commands.Cog.listener()
    async def on_private_channel_delete(self, deleted_channel: discord.abc.GuildChannel):
        """When a private channel is deleted"""
        discord_utils.remove_channel(deleted_channel, use="auto_remove_channel")

    @commands.hybrid_command()
    async def git(self, ctx: discord.ext.commands.Context):
        """GitHub page"""
        await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")

    @commands.hybrid_command()
    async def invite(self, ctx: discord.ext.commands.Context):
        """Get a link to invite the bot"""
        # inv = discord.utils.oauth_url(os.getenv('CLIENT_ID'))
        inv = "https://discord.com/api/oauth2/authorize?client_id=837828249467093032&permissions=311385253888&scope" \
              "=bot%20applications.commands "
        await ctx.send(f'Share the bot! {inv}')

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)  # Only mods can add comics
    async def add_all(self, ctx: discord.ext.commands.Context, date: str = None, hour: str = None):
        """Add all comics to a specific channel. Preferred way to add all comics. Mods only"""
        status = discord_utils.add_all(ctx, date, hour)
        if status == utils.Success:
            await ctx.send("All comics added successfully!")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the server from the database
    async def remove_all(self, ctx: discord.ext.commands.Context):
        """Remove the guild from the database. Preferred way to remove all comics. Mods only"""
        status = discord_utils.remove_guild(ctx)

        if status == utils.Success:
            await ctx.send("All daily comics removed successfully!")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the channel from the database
    async def remove_channel(self, ctx: discord.ext.commands.Context):
        """Remove the channel from the database. Mods only"""
        status = discord_utils.remove_channel(ctx)
        if status == utils.Success:
            await ctx.send("All daily comics removed successfully from this channel!")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)  # Only mods can add a role
    async def set_role(self, ctx: discord.ext.commands.Context, role: discord.Role):
        """Add a role to be notified. Mods only"""
        if discord.Guild.get_role(ctx.guild, role.id) is not None:
            status = discord_utils.set_role(ctx, role)
            if status == utils.Success:
                await ctx.send("Role successfully added to be notified! "
                               "This role will get mentioned at each comic post. "
                               "If you wish to be notified only for daily comics happening at 6 AM "
                               "UTC, use `/set_mention daily`.")
            else:
                await ctx.send(status)
        else:
            await ctx.send("The role is invalid or not provided!")

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the role
    async def remove_role(self, ctx: discord.ext.commands.Context):
        """Deletes the role mention. Mods only"""
        status = discord_utils.remove_role(ctx)

        if status == utils.Success:
            await ctx.send("Role mention successfully removed!")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    async def set_mention(self, ctx: discord.ext.commands.Context, choice: str = ""):
        """Set the role mention policy. Mods only"""
        choice = choice.lower()

        policy = (choice.lower() == "daily")

        if policy or choice == "all":
            status = discord_utils.set_mention(ctx, policy)

            if status == utils.Success:
                await ctx.send("Successfully changed the mention policy for this server!")
            else:
                await ctx.send(status)
        else:
            await ctx.send(
                "Choose between `daily` and `all`to determine the mention policy for this server!")

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    async def get_mention(self, ctx: discord.ext.commands.Context):
        """Get the server's mention policy. Mods only"""
        status, mention_policy = discord_utils.get_mention(ctx, self.bot)

        if status == utils.Success:
            await ctx.send(f"The bot will mention the role {mention_policy}!")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    async def post_mention(self, ctx: discord.ext.commands.Context, choice: str):
        """Change the mention policy for the server. Mods only"""
        status = discord_utils.set_post_mention(ctx, choice.lower() == "enable")

        if status == utils.Success:
            await ctx.send("Successfully changed the mention policy for this server! ")
        else:
            await ctx.send(status)

    @commands.hybrid_command()
    async def vote(self, ctx: discord.ext.commands.Context):
        """Vote for the bot!"""
        await ctx.send(
            "Vote for the bot here: https://top.gg/bot/807780409362481163 and / or here : "
            "https://discordbotlist.com/bots/bdbot"
        )

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def nb_guild(self, ctx: discord.ext.commands.Context):
        """Gets the number of guilds that the bot is in (for analytics)"""

        await ctx.send(
            f"The bot is in {len(self.bot.guilds)} servers. Trying to update status on Top.gg....."
        )

        if self.topggpy is None:
            self.topggpy = topgg.DBLClient(self.bot, str(os.getenv('TOP_GG_TOKEN')))

        try:
            await self.topggpy.post_guild_count()
            await ctx.send(f'Posted server count ({self.topggpy.guild_count})')
        except Exception as e:
            await ctx.send('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

        await ctx.send("Updating status...")
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=f'/help in {len(self.bot.guilds)} servers'))

    @discord.app_commands.command()
    async def request(self, ctx: discord.Interaction):
        """Request something from the developer!"""
        # Adds a request to the database
        await ctx.response.send_modal(BotRequest())

    @commands.hybrid_command()
    async def request_delete(self, ctx: discord.ext.commands.Context):
        """

        :param ctx:
        :return:
        """
        author = f"{ctx.message.author.name}#{ctx.message.author.discriminator}"
        output = []
        count = 0

        with open(utils.REQUEST_FILE_PATH, "rt") as rq:
            # Removes all lines matching with the username and discriminator
            lines = rq.readlines()

        for line in lines:
            if not re.match(f".*\".*\"[^\"]+{author}[^\"]+", line):
                # Tries to be sure that that request can't be used to delete another user's request
                output.append(line)
            else:
                count += 1

        if count > 0:
            with open(utils.REQUEST_FILE_PATH, "wt") as rq:
                rq.writelines("".join(output))  # Rewrites all lines
            await ctx.send(f"Deleted {count} request(s)!")
        else:
            await ctx.send("No requests to delete!")

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    async def sub(self, ctx: discord.ext.commands.Context):
        """Checks if the server is subbed to any comic"""
        guild_data = discord_utils.get_specific_guild_data(ctx)
        max_fields = 5
        hr = "Hour"
        if guild_data is not None:
            comic_list = []
            comic_values: list[dict] = list(utils.strip_details.values())

            for channel in guild_data["channels"]:

                if "latest" in guild_data["channels"][channel]:
                    for comic in guild_data["channels"][channel]["latest"]:
                        comic_list = discord_utils.add_comic_to_list(comic_values, comic, self.bot, channel, comic_list)

                for day in guild_data["channels"][channel]["date"]:
                    for hour in guild_data["channels"][channel]["date"][day]:
                        for comic in guild_data["channels"][channel]["date"][day][hour]:
                            comic_list = discord_utils.add_comic_to_list(comic_values, comic, self.bot, channel,
                                                                         comic_list, hour, day)

            if len(comic_list) > 0:
                nb_fields = 0
                matching_date = utils.match_date
                embeds = [discord.Embed(title="This server is subscribed to:")]
                for comic in comic_list:
                    if nb_fields > max_fields:
                        nb_fields = 0
                        embeds.append(discord.Embed(title="This server is subscribed to:"))

                    mtch_date = matching_date[comic['Date']]
                    embeds[-1].add_field(name=comic['Name'],
                                         value=f"{'Each ' if mtch_date != 'Latest' else ''}{mtch_date}"
                                               f"{f' at {comic[hr]} h UTC' if mtch_date != 'Latest' else ''} in "
                                               f"channel {comic['Channel']}")
                    nb_fields += 1

                await discord_utils.send_embed(ctx, self.bot, embeds, remove_after=False)
            else:
                await ctx.send("This server is not subscribed to any comic!")
        else:
            await ctx.send("This server is not subscribed to any comic!")

    @commands.hybrid_command()
    async def ping(self, ctx: discord.ext.commands.Context):
        """Get the bot latency with discord API"""
        await ctx.send("Pong! " + str(round(self.bot.latency * 1000)) + "ms")

    @commands.hybrid_command()
    async def uptime(self, ctx: discord.ext.commands.Context):
        """Get the bot uptime"""
        delta = (datetime.now(timezone.utc) - self.start_time)
        hours = math.floor(delta.seconds / 3600)
        minutes = math.floor((delta.seconds - hours * 3600) / 60)
        seconds = math.floor(delta.seconds - ((minutes * 60) + (hours * 3600)))
        await ctx.send(
            "The bot has been up for " + str(delta.days) + " days, " + str(hours) + " hours, " +
            str(minutes) + " minutes and " + str(seconds) + " seconds.")

    @commands.hybrid_command()
    async def status(self, ctx: discord.ext.commands.Context):
        """Get status of the bot"""
        await ctx.send(
            "The bot is online, waiting for comics to send. Report any errors by git (`/git`) or by `/request "
            "<your request>`.")

    @commands.hybrid_command(hidden=True, server=discord_utils.SERVER)
    @commands.is_owner()
    async def vrequest(self, ctx: discord.ext.commands.Context):
        """Verifies the requests"""
        with open(utils.REQUEST_FILE_PATH, 'rt') as f:
            r = f.readlines()

        await ctx.send("Here are the requests:\n```\n" + "\n".join(r) + "\n```")

    @commands.hybrid_command(hidden=True, server=discord_utils.SERVER)
    @commands.is_owner()
    async def nb_active(self, ctx: discord.ext.commands.Context):
        """Returns the number of servers using the hourly poster service"""
        await ctx.send("There is " + str(len(utils.load_json(utils.DATABASE_FILE_PATH))) + "servers using the hourly "
                                                                                           "poster service.")

    @commands.hybrid_command(hidden=True, server=discord_utils.SERVER)
    @commands.is_owner()
    async def kill(self, ctx: discord.ext.commands.Context):
        """Close the bot connection"""
        await ctx.send("Closing bot....")

        await self.bot.close()

    @commands.hybrid_command(hidden=True, server=discord_utils.SERVER)
    @commands.is_owner()
    async def reload(self, ctx: discord.ext.commands.Context):
        """
        Reload comics.

        :param ctx: Discord message context.
        """
        await ctx.send("Reloading comics....")
        utils.strip_details = utils.load_json(utils.DETAILS_PATH)
        utils.GOCOMICS_EMBED = None
        utils.KINGDOM_EMBED = None
        utils.WEBTOONS_EMBED = None
        await ctx.send("Reloaded comics!")
    # ---- End of commands ----#
    # ---- End of BDBot ----#


class BotRequest(ui.Modal, title="Request"):
    """Request for the bot"""
    request = ui.TextInput(label="Request")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        utils.save_request(self.request.value, interaction.user.name,
                           interaction.user.discriminator)
        await interaction.response.send_message("Request saved! Thank you for using BDBot!")


async def setup(client):  # Initialize the cog
    await client.add_cog(BDBot(client))
