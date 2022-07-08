import discord

from datetime import datetime, timedelta, timezone
from discord.ext import tasks, commands
from src import utils, Web_requests_manager, discord_utils
from typing import Optional


class PosterHandler(commands.Cog):
    """
    Manages automatic posting of hourly comic strips
    """

    def __init__(self, bot: commands.Bot):
        """
        Construct the cog.

        :param bot: The discord bot
        """
        self.bot: commands.Bot = bot
        self.do_cleanup: bool = True

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def start_hourly(self, ctx: commands.Context):
        """Starts the PosterHandler loop"""
        await ctx.send("Hourly loop started! Hourly comics are posted at each hour.")

        await PosterHandler.wait_for_next_hour(self)

    async def wait_for_next_hour(self):
        """Wait for the time to restart the hourly loop"""
        sleep_date = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        await discord.utils.sleep_until(sleep_date)
        await PosterHandler.post_hourly.start(self)

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def force_hourly(self, ctx: commands.Context):
        """Force the push of comics to all subscribed servers

        :param ctx: The context of the where the command was called.
        """
        await ctx.send(f'Trying to force the hourly post for hour {utils.get_hour()}h UTC')
        await self.hourly()

    @tasks.loop(hours=1)
    async def post_hourly(self):
        """Loop to post hourly comics"""
        await self.hourly()

    async def hourly(self):
        """Post hourly comics"""
        discord_utils.logger.info("Starting automatic poster...")
        strip_details: dict = utils.strip_details
        comic_data: dict = utils.load_json(utils.DATABASE_FILE_PATH)
        comic_list: dict = {}
        comic_keys: list[str] = list(strip_details.keys())
        post_days: list[str] = ["D", utils.get_today()]
        hour: str = utils.get_hour()

        if hour == "6":
            utils.save_backup(comic_data, discord_utils.logger)

            if self.do_cleanup:
                utils.clean_database(data=comic_data, logger=discord_utils.logger)

        # Construct the list of what comics need to be sent
        for guild in comic_data:
            guild_data = comic_data[guild]
            self.get_comic_info_for_guild(guild_data, comic_list, post_days, hour)

        await self.check_comics_and_post(comic_list, strip_details, comic_keys)

        utils.save_json(utils.link_cache, utils.COMIC_LATEST_LINKS_PATH)  # Saves the link cache

        discord_utils.logger.info("Finished automatic poster.")

    def get_comic_info_for_guild(self, guild_data: dict, comic_list: dict, post_days: list[str], hour: str):
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
                    comic_list: dict = self.set_comic_to_post(guild_data, channel, comic_list, latest_comics, hour)
                    comic_list[channel].update({"latest_comics": latest_comics})

                # Then check if the comic is wanted for a specific time
                for day in post_days:
                    if "date" in guild_data["channels"][channel]:
                        if day in guild_data["channels"][channel]["date"]:
                            if hour in guild_data["channels"][channel]["date"][day]:
                                hour_specific_comics: list[int] = guild_data["channels"][channel]["date"][day][hour]
                                comic_list: dict = self.set_comic_to_post(guild_data, channel, comic_list,
                                                                  hour_specific_comics, hour)

    def set_comic_to_post(self, guild_data: dict, channel: str, comic_list: dict, comics_to_add: list[int],
                          hour: str) -> dict:
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

            if ('only_daily' in guild_data) and \
                    (not guild_data["only_daily"] or hour == "6") and \
                    ("role" in guild_data) and to_mention:
                # Check if:
                # - A role is set
                # - The role can be mentioned anytime, or it is 6 AM UTC
                # - And the guild wants to be mentioned
                role = discord.Guild.get_role(
                    self.bot.get_guild(guild_data["server_id"]), guild_data["role"])

            comic_list.update({
                channel: {
                    "channel": channel,
                    "comics": comics_to_add,
                    "role": role,
                    "hasBeenMentioned": False,
                    "wantMention": to_mention
                }
            })
        else:
            comic_list[channel]["comics"].extend(comics_to_add)
        return comic_list

    async def check_comics_and_post(self, comic_list: dict, strip_details: dict, comic_keys: list[str],
                                    called_channel: Optional[discord.TextChannel] = None):
        """Load comics and check if they are the latest ones.
        Finally, post the comic to the channels.

        :param comic_list: The information about where to post each comic and how
        :param strip_details: The details of the comic strip
        :param comic_keys: The name of all the comics
        :param called_channel: The channel of where the command was sent from (Should be None for the hourly poster
        and filled when called manually)
        """
        available_channels = {}
        not_available_channels = {}
        nb_of_comics_posted = 0
        # Check if any guild want the comic
        for i in range(len(strip_details)):
            count = 0
            for chan in comic_list:
                if i in comic_list[chan]["comics"]:
                    count += 1
                    break

            if count > 0:
                # Get the details of the comic
                comic_details: Optional[dict]
                try:
                    comic_details = await discord_utils.run_blocking(
                        Web_requests_manager.get_new_comic_details,
                        self.bot,
                        strip_details[comic_keys[i]],
                        "today", latest_check=True
                    )
                except Exception:
                    # Anything can happen (connection problem, etc... and the bot will crash if any error
                    # is raised in the poster loop)
                    comic_details = None

                embed = discord_utils.create_embed(comic_details)  # Creates the embed

                is_latest: bool
                if comic_details is not None:
                    is_latest = comic_details["is_latest"]
                else:
                    is_latest = False

                if is_latest and called_channel is None:
                    # Only updates the link cache if it is done during the hourly loop
                    utils.link_cache[comic_details["Name"]] = comic_details["img_url"]

                for channel in comic_list:  # Finally, sends the comic
                    nb_of_comics_posted += await self.load_channel_and_send(i, comic_list, channel, embed, is_latest,
                                                                            available_channels, not_available_channels,
                                                                            called_channel)
        if called_channel is None:  # Only logs the hourly loop at the end
            discord_utils.logger.info(f"The hourly loop sent {nb_of_comics_posted} comic(s) the "
                                      f"{datetime.now().strftime('%dth of %B %Y at %Hh')}")
        if called_channel is not None and nb_of_comics_posted == 0:
            # If it was called manually ('post' command), and there is no comics to post anywhere in the guild,
            # it will warn in the channel that no comics needed to be sent, and it will conclude
            await called_channel.send("No comics to send!")

    async def load_channel_and_send(self, comic_number: int, comic_list: dict, channel: str,
                                    embed: discord.Embed, is_latest: bool, available_channels: dict,
                                    not_available_channels: dict,
                                    called_channel: Optional[discord.TextChannel] = None) -> int:
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
        latest_comics = comic_list[channel]["latest_comics"] if "latest_comics" in comic_list[channel] else []
        if comic_number in comic_list[channel]["comics"] and (comic_number not in latest_comics
                                                              or (comic_number in latest_comics and is_latest)):
            # Then, gets the channel object by its ID
            channel_id = int(comic_list[channel]["channel"])

            if channel_id not in available_channels:
                chan = self.bot.get_channel(channel_id)  # Retrieves the channel object by the discord client
                # And save it for future use (so it can be looked up later)
                available_channels.update({channel_id: chan})
            else:
                chan = available_channels.get(channel_id)  # Use the cached channel object

            if chan is not None and channel_id not in not_available_channels and \
                    chan.permissions_for(chan.guild.get_member(self.bot.user.id)).send_messages:
                # Makes sure that the channel is available (e.g. channel object is not None and the bot
                # can send messages)
                try:
                    if not comic_list[channel]["hasBeenMentioned"] and comic_list[channel]["wantMention"]:
                        # Checks if the channel want the original mention ('Comics for <date>, <hour> UTC @<role>')
                        if comic_list[channel]["role"] is not None:
                            # Checks if there is a role to mention
                            role_mention = comic_list[channel]["role"].mention
                        else:
                            role_mention = ""

                        await chan.send(f"Comics for "
                                        f"{datetime.now(timezone.utc).strftime('%A %B %dth %Y, %H h UTC')}"
                                        f" {role_mention}")
                        comic_list[channel]["hasBeenMentioned"] = True  # Sets the channel as already mentioned

                    await discord_utils.send_embed(chan, None, [embed])  # Sends the comic embed (most important)
                    return 1
                except Exception as e:
                    # There is too many things that can go wrong here, just catch everything
                    error_msg = f"An error occurred in the hourly poster: {e.__class__.__name__}: {e}"
                    discord_utils.logger.error(error_msg)

                    if called_channel is not None:  # Send the error message to the channel too
                        await called_channel.send(error_msg)
            else:
                not_available_channels.update({channel_id: None})  # Remembers that the channel is not available
                if called_channel is not None:  # If it can, send a message to the channel if an error occurred
                    if chan is None:
                        chan = comic_list[channel]["channel"]
                    else:
                        chan = chan.mention

                    await called_channel.send(f"Could not send message to channel {chan}")
                else:
                    # Logs that a channel is not available but still signed up for a comic
                    discord_utils.logger.warning("A comic could not be posted to a channel.")

        return 0  # If it encountered an issue or there is no comic to send, return 0

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def post(self, ctx: commands.Context, date: str = None, hour: str = None):
        """Force the comic post for a single server.

        :param ctx: The context of the where the command was called.
        :param date: The date to simulate
        :param hour: The hour to simulate
        """
        strip_details: dict = utils.strip_details
        comic_data: dict = utils.load_json(utils.DATABASE_FILE_PATH)
        comic_list: dict = {}
        comic_keys: list[str] = list(strip_details.keys())
        guild_id: str = str(ctx.guild.id)

        if guild_id in comic_data:
            # Gets date and hour of force post
            final_date, final_hour = utils.parse_all(date, hour, default_date=utils.get_today(),
                                                     default_hour=utils.get_hour())
            await ctx.send(f"Looking for comics to post for date: {utils.match_date[final_date]} at "
                           f"{final_hour}h UTC")
            post_days = ["D", final_date]

            final_hour = str(final_hour)

            # Gets the comic info for the guild
            self.get_comic_info_for_guild(comic_data[guild_id], comic_list, post_days, final_hour)

            # If there is comic to send
            if len(comic_list) > 0:
                await self.check_comics_and_post(comic_list, strip_details, comic_keys, called_channel=ctx.channel)
            else:
                await ctx.send("No comics to send!")
        else:  # Warns that no comic are available
            await ctx.send("This server is not subscribed to any comic!")

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def update_database_clean(self, ctx: commands.Context):
        """Clean the database from servers that don't have any comics saved

        :param ctx: The context of the where the command was called.
        """
        nb_removed = utils.clean_database(strict=True, logger=discord_utils.logger)

        await ctx.send(f'Cleaned the database from {nb_removed} inactive server(s).')

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def restore_last_backup(self, ctx: commands.Context):
        """Restore a previous backup

        :param ctx: The context of the where the command was called.
        """
        # Stops the database cleaning and restore the last backup
        self.do_cleanup = False
        utils.restore_backup()

        await ctx.send("Last backup restored! Please reboot the bot to re-enable automatic cleanups!")

    @commands.hybrid_command(hidden=True, guilds=discord_utils.SERVER)
    @commands.is_owner()
    async def do_backup(self, ctx: commands.Context):
        """Force a backup

        :param ctx: The context of the where the command was called.
        """
        # Force a backup
        utils.save_backup(utils.load_json(utils.DATABASE_FILE_PATH), discord_utils.logger)

        await ctx.send("Backup done!")


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord Bot
    """
    await bot.add_cog(PosterHandler(bot))
