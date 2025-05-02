import asyncio
import os
import re
from datetime import datetime, timezone
from typing import Optional, Union

import discord
from discord import app_commands
from discord.app_commands import AppCommand
from discord.ext import commands

from bdbot import utils
from bdbot.actions import ExtendedAction
from bdbot.comics import initialize_comics
from bdbot.db import DiscordSubscription, ServerSubscription
from bdbot.discord_ import discord_utils
from bdbot.discord_.bot_request import BotRequest
from bdbot.discord_.client import BDBotClient
from bdbot.discord_.cogs.AutomaticPoster import PosterHandler
from bdbot.discord_.cogs.Comics import Comic
from bdbot.discord_.discord_utils import SERVER, NextSend, is_owner, send_message
from bdbot.discord_.exceptions import on_error
from bdbot.embed import Embed
from bdbot.field import Field
from bdbot.files import DETAILS_PATH, REQUEST_FILE_PATH, load_json
from bdbot.time import Weekday, get_now, get_time_between


class BDBot(commands.Cog):
    """Class responsible for main functions of the bot"""

    def __init__(self, bot: BDBotClient):
        """Constructor of the cog

        Initialize all the properties of the cog"""
        self.bot: BDBotClient = bot
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
        await discord_utils.modify_database(
            self.bot, guild, ExtendedAction.Auto_remove_guild
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, deleted_channel: discord.abc.GuildChannel):
        """When a guild channel is deleted"""
        await discord_utils.modify_database(
            self.bot, deleted_channel, ExtendedAction.Auto_remove_channel
        )

    @commands.Cog.listener()
    async def on_private_channel_delete(
        self, deleted_channel: discord.abc.GuildChannel
    ):
        """When a private channel is deleted"""
        await discord_utils.modify_database(
            self.bot, deleted_channel, ExtendedAction.Auto_remove_channel
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

    # Only mods can add comics
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_all(
        self, inter: discord.Interaction, date: Weekday = None, hour: int = None
    ):
        """Add all comics to a specific channel. Preferred way to add all comics. Mods only"""
        status = await discord_utils.add_all(self.bot, inter, date, hour)
        await send_message(inter, status)

    # Only mods can delete the server from the database
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_all(self, inter: discord.Interaction):
        """Remove the guild from the database. Preferred way to remove all comics.Mods only"""
        status = await discord_utils.modify_database(
            self.bot, inter, ExtendedAction.Remove_guild
        )
        await send_message(inter, status)

    # Only mods can delete the channel from the database
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_channel(self, inter: discord.Interaction):
        """Remove the channel from the database.Mods only"""
        status = await discord_utils.modify_database(
            self.bot, inter, ExtendedAction.Remove_channel
        )
        await send_message(inter, status)

    # Only mods can add a role
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_role(self, inter: discord.Interaction, role: discord.Role) -> None:
        """Add a role to be notified. Mods only"""
        if discord.Guild.get_role(inter.guild, role.id) is not None:
            status = await discord_utils.set_role(inter, role)
            return await send_message(inter, status)
        return await send_message(inter, "The role is invalid or not provided!")

    # Only mods can delete the role
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_role(self, inter: discord.Interaction):
        """Deletes the role mention. Mods only"""
        status = await discord_utils.remove_role(inter)
        await send_message(inter, status)

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def get_mention(self, inter: discord.Interaction):
        """Get the server's mention policy. Mods only"""
        status = await discord_utils.get_mention(inter, self.bot)
        await send_message(inter, status)

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
        server = (
            await ServerSubscription.filter(id=inter.guild.id)
            .prefetch_related("channels")
            .get_or_none()
        )
        max_fields = 5
        if server is None:
            await send_message(
                inter,
                "This server is not subscribed to any comic!",
                next_send=NextSend.Deferred,
            )
            return

        subscriptions: list[DiscordSubscription] = []
        for channel in server.channels:
            subscriptions.extend(await DiscordSubscription().filter(channel=channel.id))

        if len(subscriptions) == 0:
            await send_message(
                inter,
                "This server is not subscribed to any comic!",
                next_send=NextSend.Deferred,
            )
            return
        nb_fields = 0
        embeds = [Embed(title="This server is subscribed to:")]
        for sub in subscriptions:
            matching_comic = list(
                filter(lambda c: c.id == sub.comic_id, self.bot.comic_details.values())
            )
            if len(matching_comic) == 0:
                # Could not find matching comic, continuing
                continue
            comic = matching_comic[0]

            if nb_fields > max_fields:
                nb_fields = 0
                embeds.append(Embed(title="This server is subscribed to:"))

            channel = await sub.channel
            channel = self.bot.get_channel(channel.id)
            if channel is None:
                channel = sub.channel.id
            else:
                channel = channel.mention
            embeds[-1].add_field(
                Field(
                    name=comic.name,
                    value=f"{'Each ' if sub.weekday not in [Weekday.Latest, Weekday.Daily] else ''}{sub.weekday.name}"
                    f"{f' at {sub.hour} h UTC' if sub.weekday not in [Weekday.Latest] else ''} in "
                    f"channel {channel}",
                    inline=True,
                )
            )
            nb_fields += 1
        await discord_utils.send_embed(inter, embeds, NextSend.Deferred)

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
        active = await ServerSubscription.all().count()
        await send_message(
            inter,
            f"There is {active} server(s) using the hourly poster service.",
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
        utils.comic_details = initialize_comics(load_json(DETAILS_PATH))
        await self.bot.add_cog(Comic(self.bot))
        await send_message(inter, "Reloaded comics!", next_send=NextSend.Followup)

    # ---- End of commands ----#
    # ---- End of BDBot ----#


async def setup(bot: BDBotClient):  # Initialize the cog
    await bot.add_cog(BDBot(bot))
