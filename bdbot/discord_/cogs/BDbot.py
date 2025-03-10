import asyncio
import os
import re
from datetime import datetime, timezone
from typing import Optional, Union

import discord
import topgg
from discord import app_commands
from discord.app_commands import AppCommand
from discord.ext import commands

from bdbot import time, utils
from bdbot.actions import ExtendedAction
from bdbot.comics import initialize_comics
from bdbot.discord_ import discord_utils
from bdbot.discord_.bot_request import BotRequest
from bdbot.discord_.cogs.AutomaticPoster import PosterHandler
from bdbot.discord_.cogs.Comics import Comic
from bdbot.discord_.discord_utils import SERVER, NextSend, is_owner, send_message
from bdbot.discord_.exceptions import on_error
from bdbot.files import DATABASE_FILE_PATH, DETAILS_PATH, REQUEST_FILE_PATH, load_json
from bdbot.mention import MentionChoice, MentionPolicy
from bdbot.time import Weekday, get_now, get_time_between
from bdbot.utils import strip_details


class BDBot(commands.Cog):
    """Class responsible for main functions of the bot"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.strip_details: dict = initialize_comics(load_json(DETAILS_PATH))
        self.bot: commands.Bot = bot
        self.topggpy = None
        self.start_time: datetime = get_now()
        self.bot.tree.error(on_error)

    @commands.Cog.listener()
    async def on_ready(self):
        """On start of the bot"""
        # Set owner id
        app_info = await self.bot.application_info()
        discord_utils.OWNER = self.bot.owner_id = app_info.owner.id

        # Change the bot activity
        await discord_utils.update_presence(self.bot)
        discord_utils.logger.info(f"Logged in as {self.bot.user}")
        channel_id: int = int(os.getenv("PRIVATE_CHANNEL_SUPPORT_ID"))

        channel: discord.TextChannel = self.bot.get_channel(channel_id)

        # Sends this message whenever restarting the bot
        await channel.send("Bot restarted. I will now try to sync the commands.")

        # Sync the commands
        guild: Union[None, discord.Guild] = None
        command_tree: discord.app_commands.CommandTree = self.bot.tree
        if os.getenv("DEBUG") == "True":
            guild = channel.guild
            command_tree.copy_global_to(guild=guild)
            await channel.send(f"Syncing commands to server {guild.name} ...")
        else:
            await channel.send("Syncing global commands...")

        await command_tree.sync(guild=guild)

        await channel.send(
            "Finished syncing commands. An hour might be needed for global commands to be available!"
        )

        async with self.bot:
            # Wait for daily poster
            await PosterHandler.wait_for_next_hour(PosterHandler(self.bot))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """When the bot is removed from a server"""
        discord_utils.remove_guild(guild, use=ExtendedAction.Auto_remove_guild)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, deleted_channel: discord.abc.GuildChannel):
        """When a guild channel is deleted"""
        discord_utils.remove_channel(
            deleted_channel, use=ExtendedAction.Auto_remove_channel
        )

    @commands.Cog.listener()
    async def on_private_channel_delete(
        self, deleted_channel: discord.abc.GuildChannel
    ):
        """When a private channel is deleted"""
        discord_utils.remove_channel(
            deleted_channel, use=ExtendedAction.Auto_remove_channel
        )

    @commands.Cog.listener()
    async def on_connect(self):
        discord_utils.logger.info("Bot has been connected!")

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id: int):
        discord_utils.logger.info(
            f"Shard of id {shard_id} has been connected to discord gateway."
        )

    @commands.Cog.listener()
    async def on_disconnect(self):
        discord_utils.logger.info("Bot has been disconnected. Retrying to reconnect...")

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id: int):
        discord_utils.logger.info(
            f"Shard of id {shard_id} has been disconnected. Retrying to reconnect..."
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        message_channel: Optional[discord.TextChannel] = None
        channels = guild.text_channels

        for channel in channels:
            if channel.permissions_for(
                guild.get_member(self.bot.user.id)
            ).send_messages:
                message_channel = channel
                break

        if message_channel is not None:
            await message_channel.send(
                "Thanks for choosing BDBot! Use `/help general` for a list of commands and"
                " comics available and `/help schedule` to know how to set up your server to"
                " receive comics automatically!"
            )

    @app_commands.command()
    async def git(self, inter: discord.Interaction):
        """GitHub page"""
        await send_message(
            inter, "Want to help the bot? Go here: https://github.com/BBArikL/BDBot"
        )

    @app_commands.command()
    async def invite(self, inter: discord.Interaction):
        """Get a link to invite the bot"""
        inv = discord_utils.get_url()
        await send_message(inter, f"Share the bot! {inv}")

    # Only mods can add comics
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_all(
        self, inter: discord.Interaction, date: Weekday = None, hour: int = None
    ):
        """Add all comics to a specific channel. Preferred way to add all comics. Mods only"""
        status = discord_utils.add_all(inter, date, hour)
        await send_message(inter, status)

    # Only mods can delete the server from the database
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_all(self, inter: discord.Interaction):
        """Remove the guild from the database. Preferred way to remove all comics.Mods only"""
        status = discord_utils.remove_guild(inter)
        await send_message(inter, status)

    # Only mods can delete the channel from the database
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_channel(self, inter: discord.Interaction):
        """Remove the channel from the database.Mods only"""
        status = discord_utils.remove_channel(inter)
        await send_message(inter, status)

    # Only mods can add a role
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_role(self, inter: discord.Interaction, role: discord.Role):
        """Add a role to be notified. Mods only"""
        if discord.Guild.get_role(inter.guild, role.id) is not None:
            status = discord_utils.set_role(inter, role)
            return await send_message(inter, status)
        await send_message(inter, "The role is invalid or not provided!")

    # Only mods can delete the role
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_role(self, inter: discord.Interaction):
        """Deletes the role mention. Mods only"""
        status = discord_utils.remove_role(inter)
        await send_message(inter, status)

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_mention(self, inter: discord.Interaction, policy: MentionPolicy):
        """Set the role mention policy. Mods only"""
        status = discord_utils.set_mention(inter, policy)
        await send_message(inter, status)

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def get_mention(self, inter: discord.Interaction):
        """Get the server's mention policy. Mods only"""
        status, mention_policy = discord_utils.get_mention(inter, self.bot)
        await send_message(inter, status)

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_mention(self, inter: discord.Interaction, choice: MentionChoice):
        """Change the mention policy for the server. Mods only"""
        status = discord_utils.set_post_mention(inter, choice == MentionChoice.Enable)
        await send_message(inter, status)

    @app_commands.command()
    async def vote(self, inter: discord.Interaction):
        """Vote for the bot!"""
        await send_message(
            inter,
            "Vote for the bot here: https://top.gg/bot/807780409362481163 and / or here : "
            "https://discordbotlist.com/bots/bdbot",
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def nb_guild(self, inter: discord.Interaction):
        """Gets the number of guilds that the bot is in (for analytics)"""

        await send_message(
            inter,
            f"The bot is in {len(self.bot.guilds)} servers. Trying to update status on Top.gg.....",
        )

        if self.topggpy is None:
            self.topggpy = topgg.DBLClient(self.bot, str(os.getenv("TOP_GG_TOKEN")))

        try:
            await self.topggpy.post_guild_count()
            await send_message(
                inter, f"Posted server count ({self.topggpy.guild_count})"
            )
        except Exception as e:
            await send_message(
                inter, "Failed to post server count\n{}: {}".format(type(e).__name__, e)
            )

        await send_message(inter, "Updating status...")
        await discord_utils.update_presence(self.bot)

    @app_commands.command()
    async def request(self, inter: discord.Interaction):
        """Request something from the developer!"""
        # Adds a request to the database
        await inter.response.send_modal(BotRequest())

    @app_commands.command()
    async def delete_requests(self, inter: discord.Interaction):
        """Delete requests sent through 'request'"""
        author = f"{inter.user.name}#{inter.user.discriminator}"
        output = []
        count = 0

        with open(REQUEST_FILE_PATH, "rt") as rq:
            # Removes all lines matching with the username and discriminator
            lines = rq.readlines()

        for line in lines:
            if not re.match(f'.*".*"[^"]+{author}[^"]+', line):
                # Tries to be sure that that request can't be used to delete another user's request
                output.append(line)
            else:
                count += 1

        if count > 0:
            with open(REQUEST_FILE_PATH, "wt") as rq:
                rq.writelines("".join(output))  # Rewrites all lines
            await send_message(inter, f"Deleted {count} request(s)!")
        else:
            await send_message(inter, "No requests to delete!")

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def sub(self, inter: discord.Interaction):
        """Checks if the server is subbed to any comic"""
        await inter.response.defer()
        guild_data = discord_utils.get_specific_guild_data(inter)
        max_fields = 5
        hr = "Hour"
        if guild_data is not None:
            comic_list = []
            comic_values: list[dict] = list(strip_details.values())

            for channel in guild_data["channels"]:

                if "latest" in guild_data["channels"][channel]:
                    for comic in guild_data["channels"][channel]["latest"]:
                        comic_list = discord_utils.add_comic_to_list(
                            comic_values, comic, self.bot, channel, comic_list
                        )

                if "date" in guild_data["channels"][channel]:
                    for day in guild_data["channels"][channel]["date"]:
                        for hour in guild_data["channels"][channel]["date"][day]:
                            for comic in guild_data["channels"][channel]["date"][day][
                                hour
                            ]:
                                comic_list = discord_utils.add_comic_to_list(
                                    comic_values,
                                    comic,
                                    self.bot,
                                    channel,
                                    comic_list,
                                    hour,
                                    day,
                                )

            if len(comic_list) > 0:
                nb_fields = 0
                embeds = [discord.Embed(title="This server is subscribed to:")]
                for comic in comic_list:
                    if nb_fields > max_fields:
                        nb_fields = 0
                        embeds.append(
                            discord.Embed(title="This server is subscribed to:")
                        )

                    match_date = time.match_date[comic["Date"]]
                    embeds[-1].add_field(
                        name=comic["name"],
                        value=f"{'Each ' if match_date not in [Weekday.Latest, Weekday.Daily] else ''}{match_date.name}"
                        f"{f' at {comic[hr]} h UTC' if match_date not in [Weekday.Latest] else ''} in "
                        f"channel {comic['Channel']}",
                    )
                    nb_fields += 1

                await discord_utils.send_embed(inter, embeds, NextSend.Deferred)
            else:
                await send_message(
                    inter,
                    "This server is not subscribed to any comic!",
                    next_send=NextSend.Deferred,
                )
        else:
            await send_message(
                inter,
                "This server is not subscribed to any comic!",
                next_send=NextSend.Deferred,
            )

    @app_commands.command()
    async def ping(self, inter: discord.Interaction):
        """Get the bot latency with discord API"""
        await send_message(inter, "Pong! " + str(round(self.bot.latency * 1000)) + "ms")

    @app_commands.command()
    async def uptime(self, inter: discord.Interaction):
        """Get the bot uptime"""
        delta = get_time_between(self.start_time, datetime.now(timezone.utc))
        await send_message(
            inter,
            f"The bot has been up for {delta.days} days, {delta.hours} hours, {delta.minutes} minutes"
            f" and {delta.seconds} seconds.",
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def reset_all_commands(self, inter: discord.Interaction):
        """Reset all commands"""
        await send_message(inter, "Resetting all commands, this might take a while....")

        error_msg = "An error occurred while resetting commands:"
        try:
            # Clearing bot-aware commands
            self.bot.commands.clear()
            self.bot.tree.clear_commands(guild=None)
            self.bot.tree.clear_commands(guild=SERVER)
        except Exception as e:
            discord_utils.logger.error(f"{error_msg} {e}")

        all_commands = await self.bot.tree.fetch_commands()
        for comm in all_commands:
            await asyncio.sleep(0.5)
            try:
                await comm.delete()
            except Exception as e:
                discord_utils.logger.error(f"{error_msg} {e}")

            try:
                self.bot.tree.remove_command(comm.name, type=AppCommand)
            except Exception as e:
                discord_utils.logger.error(f"{error_msg} {e}")

        server_commands = await self.bot.tree.sync(guild=SERVER)
        global_commands = await self.bot.tree.sync()
        await send_message(
            inter,
            f"All commands reset!\n"
            f"Remaining commands:\n"
            f" - Server commands: {len(server_commands)}\n"
            f" - Global commands: {len(global_commands)}\n"
            f" - Discord commands: {len(await self.bot.tree.fetch_commands())}",
            next_send=NextSend.Followup,
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def nb_active(self, inter: discord.Interaction):
        """Returns the number of servers using the hourly poster service"""
        await send_message(
            inter,
            "There is "
            + str(len(load_json(DATABASE_FILE_PATH)))
            + "servers using the hourly "
            "poster service.",
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def kill(self, inter: discord.Interaction):
        """Close the bot connection"""
        discord_utils.logger.info("Closing bot....")
        await send_message(inter, "Closing bot....")
        await self.bot.close()

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def reload(self, inter: discord.Interaction):
        """
        Reload comics.

        :param inter: Discord message context.
        """
        await send_message(inter, "Reloading comics....")
        await self.bot.remove_cog("Comic")
        utils.strip_details = initialize_comics(load_json(DETAILS_PATH))
        await self.bot.add_cog(Comic(self.bot))
        await send_message(inter, "Reloaded comics!", next_send=NextSend.Followup)

    # ---- End of commands ----#
    # ---- End of BDBot ----#


async def setup(bot: discord.ext.commands.Bot):  # Initialize the cog
    await bot.add_cog(BDBot(bot))
