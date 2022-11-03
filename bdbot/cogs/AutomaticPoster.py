from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from bdbot.discord_utils import (
    clean_database,
    create_embed,
    logger,
    run_blocking,
    send_chan_embed,
    SERVER, send_message, is_owner, NextSend,
)
from bdbot.utils import (
    COMIC_LATEST_LINKS_PATH,
    DATABASE_FILE_PATH,
    Action,
    Date,
    date_to_db,
    get_hour,
    get_today,
    link_cache,
    load_json,
    parse_all,
    save_backup,
    save_json,
    strip_details, restore_backup,
)
from bdbot.Web_requests_manager import get_new_comic_details


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
        await send_message(inter, "Hourly loop started! Hourly comics are posted at each hour.")

        await PosterHandler.wait_for_next_hour(self)

    async def wait_for_next_hour(self):
        """Wait for the time to restart the hourly loop"""
        sleep_date = datetime.now(timezone.utc).replace(
            minute=0, second=0, microsecond=0
        ) + timedelta(hours=1)
        await discord.utils.sleep_until(sleep_date)
        await PosterHandler.post_hourly.start(self)

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def force_hourly(self, inter: discord.Interaction, hour: Optional[int] = None):
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
        except Exception as e:
            logger.error(str(e))

    async def hourly(self, hour: Optional[int] = None):
        """Post hourly comics"""
        logger.info("Starting automatic poster...")
        comic_data: dict = load_json(DATABASE_FILE_PATH)
        comic_list: dict = {}
        comic_keys: list[str] = list(strip_details.keys())
        post_days = [Date.Daily, get_today()]

        if not hour:
            hour = get_hour()
        hour = str(hour)

        if hour == "6":
            save_backup(comic_data, logger)

            if self.do_cleanup:
                clean_database(data=comic_data, logger_=logger)

        # Construct the list of what comics need to be sent
        for guild in comic_data:
            guild_data = comic_data[guild]
            self.get_comic_info_for_guild(guild_data, comic_list, post_days, hour)

        await self.check_comics_and_post(comic_list, strip_details, comic_keys)

        save_json(link_cache, COMIC_LATEST_LINKS_PATH)  # Saves the link cache

        logger.info("Finished automatic poster.")

    def get_comic_info_for_guild(
            self, guild_data: dict, comic_list: dict, post_days: Iterable[Date], hour: str
    ):
        """Get the comic info for each server. This method mutate 'comic_list' for each comic.

        :param guild_data: All the information of the server
        :param comic_list: The information about where to post each comic and how
        :param post_days: The days to check for
        :param hour: The current hour
        """
        if "channels" in guild_data:
            for channel in guild_data["channels"]:

                # First check if it wants only the latest comics
                if "latest" in guild_data["channels"][channel]:
                    latest_comics: list[int] = guild_data["channels"][channel]["latest"]
                    comic_list: dict = self.set_comic_to_post(
                        guild_data, channel, comic_list, latest_comics, hour
                    )
                    comic_list[channel].update({"latest_comics": latest_comics})

                # Then check if the comic is wanted for a specific time
                for day in post_days:
                    day = date_to_db(day)
                    if "date" in guild_data["channels"][channel]:
                        if day in guild_data["channels"][channel]["date"]:
                            if hour in guild_data["channels"][channel]["date"][day]:
                                hour_specific_comics: list[int] = guild_data[
                                    "channels"
                                ][channel]["date"][day][hour]
                                comic_list: dict = self.set_comic_to_post(
                                    guild_data,
                                    channel,
                                    comic_list,
                                    hour_specific_comics,
                                    hour,
                                )

    def set_comic_to_post(
            self,
            guild_data: dict,
            channel: str,
            comic_list: dict,
            comics_to_add: list[int],
            hour: str,
    ) -> dict:
        """Set one comic to post on one channel

        :param guild_data: All the information of the server
        :param channel: The string of the ID of the channel to post the comics
        :param comic_list: The information about where to post each comic and how
        :param comics_to_add: The comic number to check for
        :param hour: The current hour
        """
        if channel not in comic_list:  # Assure no duplicates
            to_mention = guild_data["mention"]
            role: Optional[discord.Role] = None

            if (
                    ("only_daily" in guild_data)
                    and (not guild_data["only_daily"] or hour == "6")
                    and ("role" in guild_data)
                    and to_mention
            ):
                # Check if:
                # - A role is set
                # - The role can be mentioned anytime, or it is 6 AM UTC
                # - And the guild wants to be mentioned
                role = discord.Guild.get_role(
                    self.bot.get_guild(guild_data["server_id"]), guild_data["role"]
                )

            comic_list.update(
                {
                    channel: {
                        "channel": channel,
                        "comics": comics_to_add,
                        "role": role,
                        "hasBeenMentioned": False,
                        "wantMention": to_mention,
                    }
                }
            )
        else:
            comic_list[channel]["comics"].extend(comics_to_add)
        return comic_list

    async def check_comics_and_post(
            self,
            comic_list: dict,
            comic_details: dict,
            comic_keys: list[str],
            called_channel: Optional[discord.TextChannel] = None,
    ):
        """Load comics and check if they are the latest ones.
        Finally, post the comic to the channels.

        :param comic_list: The information about where to post each comic and how
        :param comic_details: The details of the comic strip
        :param comic_keys: The name of all the comics
        :param called_channel: The channel of where the command was sent from (Should be None for the hourly poster
        and filled when called manually)
        """
        available_channels = {}
        not_available_channels = {}
        nb_of_comics_posted = 0
        # Check if any guild want the comic
        for i in range(len(comic_details)):
            count = 0
            for chan in comic_list:
                if i in comic_list[chan]["comics"]:
                    count += 1
                    break

            if count > 0:
                # Get the details of the comic
                comic_details: Optional[dict]
                try:
                    comic_details = await run_blocking(
                        get_new_comic_details,
                        self.bot,
                        strip_details[comic_keys[i]],
                        Action.Today,
                        latest_check=True,
                    )
                except Exception as e:
                    # Anything can happen (connection problem, etc... and the bot will crash if any error
                    # is raised in the poster loop)
                    logger.error(f"An error occurred while getting a comic: {e}")
                    comic_details = None

                embed = create_embed(comic_details)  # Creates the embed

                is_latest: bool
                if comic_details is not None:
                    is_latest = comic_details["is_latest"]
                else:
                    is_latest = False

                if is_latest and called_channel is None:
                    # Only updates the link cache if it is done during the hourly loop
                    link_cache[comic_details["Name"]] = comic_details["img_url"]

                for channel in comic_list:  # Finally, sends the comic
                    nb_of_comics_posted += await self.load_channel_and_send(
                        i,
                        comic_list,
                        channel,
                        embed,
                        is_latest,
                        available_channels,
                        not_available_channels,
                        called_channel,
                    )
        if called_channel is None:  # Only logs the hourly loop at the end
            logger.info(
                f"The hourly loop sent {nb_of_comics_posted} comic(s) the "
                f"{datetime.now().strftime('%dth of %B %Y at %Hh')}"
            )
        if called_channel is not None and nb_of_comics_posted == 0:
            # If it was called manually ('post' command), and there is no comics to post anywhere in the guild,
            # it will warn in the channel that no comics needed to be sent, and it will conclude
            await called_channel.send("No comics to send!")

    async def load_channel_and_send(
            self,
            comic_number: int,
            comic_list: dict,
            channel: str,
            embed: discord.Embed,
            is_latest: bool,
            available_channels: dict,
            not_available_channels: dict,
            called_channel: Optional[discord.TextChannel] = None,
    ) -> int:
        """Sends the loaded comic to the specified channel

        :param comic_number: The number of the comic to send
        :param comic_list: The information about where to post each comic and how
        :param channel: The channel where to send the comic to
        :param embed: The embed with the comic
        :param is_latest: If the comic is the latest one
        :param available_channels: The dictionary of available channels
        :param not_available_channels: The dictionary of not-available channels
        :param called_channel: The channel of the where the command was called (None in the hourly loop,
        filled when called through /post).

        :returns: 1 if it posted a comic, 0 if it could/did not
        """
        # First, check that the comic is the latest and if that channel only wants the latest (for this comic)
        latest_comics = (
            comic_list[channel]["latest_comics"]
            if "latest_comics" in comic_list[channel]
            else []
        )
        if comic_number in comic_list[channel]["comics"] and (
                comic_number not in latest_comics
                or (comic_number in latest_comics and is_latest)
        ):
            # Then, gets the channel object by its ID
            channel_id = int(comic_list[channel]["channel"])

            if channel_id not in available_channels:
                chan = self.bot.get_channel(
                    channel_id
                )  # Retrieves the channel object by the discord client
                # And save it for future use (so it can be looked up later)
                available_channels.update({channel_id: chan})
            else:
                chan = available_channels.get(
                    channel_id
                )  # Use the cached channel object

            if (
                    chan is not None
                    and channel_id not in not_available_channels
                    and chan.permissions_for(
                    chan.guild.get_member(self.bot.user.id)
                    ).send_messages
            ):
                # Makes sure that the channel is available (e.g. channel object is not None and the bot
                # can send messages)
                try:
                    if (
                            not comic_list[channel]["hasBeenMentioned"]
                            and comic_list[channel]["wantMention"]
                    ):
                        # Checks if the channel want the original mention ('Comics for <date>, <hour> UTC @<role>')
                        if comic_list[channel]["role"] is not None:
                            # Checks if there is a role to mention
                            role_mention = comic_list[channel]["role"].mention
                        else:
                            role_mention = ""

                        await chan.send(
                            f"Comics for "
                            f"{datetime.now(timezone.utc).strftime('%A %B %dth %Y, %H h UTC')}"
                            f" {role_mention}"
                        )
                        comic_list[channel][
                            "hasBeenMentioned"
                        ] = True  # Sets the channel as already mentioned

                    await send_chan_embed(
                        chan, embed
                    )  # Sends the comic embed (most important)
                    return 1
                except Exception as e:
                    # There is too many things that can go wrong here, just catch everything
                    error_msg = f"An error occurred in the hourly poster: {e.__class__.__name__}: {e}"
                    logger.error(error_msg)

                    if called_channel is not None:
                        # Send the error message to the channel too
                        await called_channel.send(error_msg)
            else:
                not_available_channels.update(
                    {channel_id: None}
                )  # Remembers that the channel is not available
                if (
                        called_channel is not None
                ):  # If it can, send a message to the channel if an error occurred
                    if chan is None:
                        chan = comic_list[channel]["channel"]
                    else:
                        chan = chan.mention

                    await called_channel.send(
                        f"Could not send message to channel {chan}"
                    )
                else:
                    # Logs that a channel is not available but still signed up for a comic
                    logger.warning("A comic could not be posted to a channel.")

        return 0  # If it encountered an issue or there is no comic to send, return 0

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def post(self, inter: discord.Interaction, date: str = None, hour: str = None):
        """Force the comic post for a single server.

        :param inter: The interaction of the where the command was called.
        :param date: The date to simulate
        :param hour: The hour to simulate
        """
        comic_data: dict = load_json(DATABASE_FILE_PATH)
        comic_list: dict = {}
        comic_keys: list[str] = list(strip_details.keys())
        guild_id: str = str(inter.guild.id)

        if guild_id in comic_data:
            # Gets date and hour of force post
            final_date, final_hour = parse_all(
                date,
                hour,
                default_date=get_today(),
                default_hour=get_hour(),
            )
            await send_message(
                inter,
                f"Looking for comics to post for date: {final_date} at "
                f"{final_hour}h UTC"
            )
            post_days = (Date.Daily, final_date)

            final_hour = str(final_hour)

            # Gets the comic info for the guild
            self.get_comic_info_for_guild(
                comic_data[guild_id], comic_list, post_days, final_hour
            )

            # If there is comic to send
            if len(comic_list) > 0:
                await self.check_comics_and_post(
                    comic_list, strip_details, comic_keys, called_channel=inter.channel()
                )
            else:
                await send_message(inter, "No comics to send!", next_send=NextSend.Followup)
        else:  # Warns that no comic are available
            await send_message(inter, "This server is not subscribed to any comic!")

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @app_commands.checks.check(is_owner)
    async def update_database_clean(self, inter: discord.Interaction):
        """Clean the database from servers that don't have any comics saved

        :param inter: The context of the where the command was called.
        """
        nb_removed = clean_database(strict=True, logger_=logger)

        await send_message(inter, f'Cleaned the database from {nb_removed} inactive server(s).')

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def restore_last_backup(self, inter: discord.Interaction):
        """Restore a previous backup

        :param inter: The context of the where the command was called.
        """
        # Stops the database cleaning and restore the last backup
        self.do_cleanup = False
        restore_backup()

        await send_message(inter, "Last backup restored! Please reboot the bot to re-enable automatic cleanups!")

    @app_commands.command()
    @app_commands.guilds(SERVER.id)
    @commands.is_owner()
    async def do_backup(self, inter: discord.Interaction):
        """Force a backup

       :param inter: The context of the where the command was called.
       """
        # Force a backup
        save_backup(load_json(DATABASE_FILE_PATH), logger)
        await send_message(inter, "Backup done!")


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord Bot
    """
    await bot.add_cog(PosterHandler(bot))
