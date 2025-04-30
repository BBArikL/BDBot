from datetime import timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks
from tortoise.expressions import Q

from bdbot.cache import link_cache
from bdbot.db import (
    ChannelSubscription,
    DiscordSubscription,
    ServerSubscription,
    restore_backup,
    save_backup,
)
from bdbot.discord_.discord_utils import (
    SERVER,
    NextSend,
    check_comics_and_post,
    clean_database,
    is_owner,
    logger,
    send_message, update_presence,
)
from bdbot.files import (
    COMIC_LATEST_LINKS_PATH,
    save_json,
)
from bdbot.time import (
    get_hour,
    get_last_corresponding_date,
    get_now,
    get_weekday,
)
from bdbot.utils import Weekday, parse_all


class PosterHandler(commands.Cog):
    """
    Manages automatic posting of hourly comic strips
    """

    def __init__(self, bot: discord.Client):
        """
        Construct the cog.

        :param bot: The discord bot
        """
        self.bot: discord.Client = bot
        self.do_cleanup: bool = True

    # @app_commands.command(hidden=True, guilds=SERVER)
    # @app_commands.is_owner()
    async def start_hourly(self, inter: discord.Interaction):
        """Starts the PosterHandler loop"""
        await send_message(
            inter, "Hourly loop started! Hourly comics are posted at each hour."
        )

        await PosterHandler.wait_for_next_hour(self)

    async def wait_for_next_hour(self):
        """Wait for the time to restart the hourly loop"""
        sleep_date = get_now().replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )
        await discord.utils.sleep_until(sleep_date)
        await PosterHandler.post_hourly.start(self)

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def force_hourly(
        self, inter: discord.Interaction, hour: Optional[int] = None
    ):
        """Force the push of comics to all subscribed servers

        :param inter: The context of the where the command was called.
        :param hour: The hour to simulate
        """
        await inter.response.send_message(
            f"Trying to force the hourly post for hour {get_hour() if not hour else hour}h UTC"
        )
        await self.hourly(hour)

    @tasks.loop(hours=1)
    async def post_hourly(self):
        """Loop to post hourly comics"""
        try:
            await self.hourly()
            await update_presence(self.bot)
        except Exception as e:
            logger.error(str(e))

    async def hourly(self, hour: Optional[int] = None):
        """Post hourly comics"""
        logger.info("Starting automatic poster...")
        if not hour:
            hour = get_hour()
        if hour == 6:
            save_backup(logger)
            if self.do_cleanup:
                await clean_database(logger_=logger)
        # Construct the list of what comics need to be sent
        logger.info("Constructing guild info....")
        # Gets the comic info for the guild
        subscriptions = (
            await DiscordSubscription.filter(
                Q(weekday=get_weekday(), hour=hour)
                | Q(weekday=Weekday.Daily, hour=hour)
                | Q(weekday=Weekday.Latest)
            )
            .order_by("comic_id")
            .all()
        )
        logger.info("Sending comics....")
        await check_comics_and_post(self.bot, subscriptions, post_time=None)
        save_json(link_cache, COMIC_LATEST_LINKS_PATH)  # Saves the link cache
        logger.info("Finished automatic poster.")

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def post(
        self, inter: discord.Interaction, date: Weekday = None, hour: int = None
    ):
        """Force the comic post for a single server.

        :param inter: The interaction of the where the command was called.
        :param date: The date to simulate
        :param hour: The hour to simulate
        """
        server = await ServerSubscription.filter(id=inter.guild.id).get_or_none()
        if server is None:
            # Warns that no comic are available
            await send_message(inter, "This server is not subscribed to any comic!")
        # Gets date and hour of force post
        final_date, final_hour = parse_all(
            date,
            hour,
            default_date=get_weekday(),
            default_hour=get_hour(),
        )
        await send_message(
            inter,
            f"Looking for comics to post for date: {final_date.value} at "
            f"{final_hour}h UTC",
        )
        post_time = get_last_corresponding_date(final_date, final_hour)
        # Gets the comic info for the guild
        channels = await ChannelSubscription.filter(server=server.id)
        queries = []
        for channel in channels:
            queries.append(Q(channel=channel.id))
        subscriptions = await DiscordSubscription.filter(
            (
                Q(weekday=final_date, hour=final_hour)
                | Q(weekday=Weekday.Daily, hour=final_hour)
                | Q(weekday=Weekday.Latest)
            )
            & Q(*(query for query in queries), join_type="OR")
        )
        # If there is no comic to send
        if len(subscriptions) == 0:
            await send_message(inter, "No comics to send!", next_send=NextSend.Followup)
            return
        await check_comics_and_post(
            self.bot, subscriptions, called_channel=inter.channel, post_time=post_time
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def update_database_clean(self, inter: discord.Interaction):
        """Clean the database from servers that don't have any comics saved

        :param inter: The context of the where the command was called.
        """
        save_backup(logger)
        nb_removed = await clean_database(bot=self.bot, strict=True, logger_=logger)
        await send_message(
            inter, f"Cleaned the database from {nb_removed} inactive server(s)."
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def restore_last_backup(self, inter: discord.Interaction):
        """Restore a previous backup

        :param inter: The context of the where the command was called.
        """
        # Stops the database cleaning and restore the last backup
        self.do_cleanup = False
        await restore_backup()
        await send_message(
            inter,
            "Last backup restored! Please reboot the bot to re-enable automatic cleanups!",
        )

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def do_backup(self, inter: discord.Interaction):
        """Force a backup

        :param inter: The context of the where the command was called.
        """
        # Force a backup
        save_backup(logger)
        await send_message(inter, "Backup done!")


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord Bot
    """
    await bot.add_cog(PosterHandler(bot))
