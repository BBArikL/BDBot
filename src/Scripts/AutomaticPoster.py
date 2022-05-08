import logging
from discord.ext import tasks, commands
import discord
from datetime import datetime, timedelta, timezone
from src import utils, Web_requests_manager


# Manages automatic posting
class PosterHandler(commands.Cog):
    # Class responsible for posting hourly comic strips

    def __init__(self, client):
        self.client = client
        self.do_cleanup = True
        self.logger = logging.getLogger('discord')

    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def start_hourly(self, ctx):
        # Starts the PosterHandler loop
        if utils.is_owner(ctx):
            await ctx.send("Hourly loop started! Hourly comics are posted at each hour.")

            await PosterHandler.wait_for_next_hour(self)
        else:
            raise commands.CommandNotFound

    # Wait for the time to restart the hourly loop
    async def wait_for_next_hour(self):
        sleep_date = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        await discord.utils.sleep_until(sleep_date)
        await PosterHandler.post_hourly.start(self)

    # Checks if the hourly loop is running
    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def is_hourly_running(self, ctx):  # Checks the PosterHandler loop
        if utils.is_owner(ctx):
            if PosterHandler.post_hourly.is_running():
                await ctx.send("The loop is running.")
            else:
                await ctx.send("The loop is NOT running.")

        else:
            raise commands.CommandNotFound

    # Force the push of comics to all subscribed guilds
    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def force_hourly(self, ctx):
        if utils.is_owner(ctx):
            await self.hourly()
        else:
            raise commands.CommandNotFound

    # Loop to post hourly comics
    @tasks.loop(hours=1)  # Hourly loop
    async def post_hourly(self):
        await self.hourly()

    # Post hourly comics
    async def hourly(self):
        # Daily loop
        self.logger.info("Starting automatic poster...")
        strip_details = utils.strip_details
        nb_of_comics = len(strip_details)
        comic_data = utils.load_json(utils.DATABASE_FILE_PATH)
        comic_list = {}
        comic_keys = list(strip_details.keys())
        post_days = ["D", utils.get_today()]
        hour = utils.get_hour()

        if hour == "6" and self.do_cleanup:
            utils.clean_database(data=comic_data)
        elif hour == "6":
            utils.save_backup(comic_data)

        # Construct the list of what comics need to be sent
        for comic_number in range(nb_of_comics):
            for guild in comic_data:
                guild_data = comic_data[guild]
                self.get_comic_info_for_guild(guild_data, comic_list, comic_number, post_days, hour)

        await self.check_comics_and_post(comic_list, strip_details, comic_keys)

        utils.save_json(utils.link_cache, utils.COMIC_LATEST_LINKS_PATH)  # Saves the links

        self.logger.info("Finished automatic poster.")

    def get_comic_info_for_guild(self, guild_data, comic_list, comic_number, post_days, hour):
        for channel in guild_data["channels"]:

            # First check if it wants only the latest comics
            if "latest" in guild_data["channels"][channel]:
                if comic_number in guild_data["channels"][channel]["latest"]:
                    comic_list = self.set_comic_to_post(guild_data, channel, comic_list, comic_number, hour)
                    latest_comics = comic_list[channel]["latest_comics"] if "latest_comics" in comic_list[channel] \
                        else []
                    latest_comics.append(comic_number)
                    comic_list[channel].update({"latest_comics": latest_comics})
                    print(comic_list[channel]["latest_comics"])

            for day in post_days:
                if day in guild_data["channels"][str(channel)]["date"]:
                    if hour in guild_data["channels"][str(channel)]["date"][day]:
                        if comic_number in guild_data["channels"][str(channel)]["date"][day][hour]:
                            comic_list = self.set_comic_to_post(guild_data, channel, comic_list, comic_number, hour)

    def set_comic_to_post(self, guild_data: dict, channel: str, comic_list: dict, comic_number: int, hour: str):
        if channel not in comic_list:  # Assure no duplicates
            to_mention = guild_data["mention"]
            role = None

            if ('only_daily' in guild_data) and \
                    (not guild_data["only_daily"] or hour == "6") and \
                    ("role" in guild_data) and to_mention:
                role = discord.Guild.get_role(
                    self.client.get_guild(guild_data["server_id"]), guild_data["role"])

            comic_list.update({
                channel: {
                    "channel": channel,
                    "comics": [comic_number],
                    "role": role,
                    "hasBeenMentioned": False,
                    "wantMention": to_mention
                }
            })
        else:
            if comic_number not in comic_list[channel]["comics"]:
                comic_list[channel]["comics"].append(comic_number)
        return comic_list

    async def check_comics_and_post(self, comic_list, strip_details, comic_keys, ctx=None):
        available_channels = {}
        not_available_channels = []
        nb_of_comics_posted = 0
        print(comic_list)
        # Check if any guild want the comic
        for i in range(len(strip_details)):
            count = 0
            for chan in comic_list:
                if i in comic_list[chan]["comics"]:
                    count += 1
                    break

            if count > 0:
                comic_details = Web_requests_manager.get_new_comic_details(strip_details[comic_keys[i]], "today",
                                                                           latest_check=True)

                embed = utils.create_embed(comic_details)  # Creates the embed

                is_latest = comic_details["is_latest"]

                if is_latest and ctx is None:
                    utils.link_cache[comic_list["Name"]] = comic_list["img_url"]

                for channel in comic_list:
                    # Load the new details
                    # Sends the comic to all subbed guilds
                    latest_comics = comic_list[channel]["latest_comics"] if "latest_comics" in comic_list[channel] \
                        else []
                    if i in comic_list[channel]["comics"] and (i not in latest_comics or
                                                               (i in latest_comics and is_latest)):
                        chanid = int(comic_list[channel]["channel"])

                        if chanid not in available_channels:
                            chan = self.client.get_channel(chanid)
                            available_channels.update({chanid: chan})
                        else:
                            chan = available_channels.get(chanid)

                        if chan is not None \
                                and chanid not in not_available_channels and \
                                chan.permissions_for(chan.guild.get_member(self.client.user.id)).send_messages:
                            try:
                                if not comic_list[channel]["hasBeenMentioned"] and \
                                        comic_list[channel]["wantMention"]:
                                    if comic_list[channel]["role"] is not None:
                                        role_mention = comic_list[channel]["role"].mention
                                    else:
                                        role_mention = ""

                                    await chan.send(f"Comics for "
                                                    f"{datetime.now(timezone.utc).strftime('%A %B %dth %Y, %H h UTC')}"
                                                    f" {role_mention}")
                                    comic_list[channel]["hasBeenMentioned"] = True

                                await chan.send(embed=embed)
                                nb_of_comics_posted += 1
                            except Exception as e:
                                self.logger.error(e)
                                continue
                        else:
                            if ctx is not None:
                                if chan is None:
                                    chan = comic_list[channel]["channel"]
                                else:
                                    chan = chan.mention

                                not_available_channels.append(chanid)

                                await ctx.send(f"Could not send message to channel {chan}")
                            else:
                                self.logger.info("A comic could not be posted to a channel.")

        if ctx is not None and nb_of_comics_posted == 0:
            await ctx.send("No comics to send!")

    @commands.hybrid_command()
    # @commands.has_permissions(manage_guild=True)
    # @commands.check()
    async def post(self, ctx, date: str = None, hour: str = None):
        strip_details = utils.strip_details
        nb_of_comics = len(strip_details)
        comic_data = utils.load_json(utils.DATABASE_FILE_PATH)
        comic_list = {}
        comic_keys = list(strip_details.keys())
        guild_id = str(ctx.guild.id)

        if guild_id in comic_data:
            final_date, final_hour = utils.parse_all(date, hour, default_date=utils.get_today(),
                                                     default_hour=utils.get_hour())
            post_days = ["D", final_date]

            final_hour = str(final_hour)

            for comic_number in range(nb_of_comics):
                self.get_comic_info_for_guild(comic_data[guild_id], comic_list, comic_number, post_days, final_hour)

            if len(comic_list) > 0:
                await self.check_comics_and_post(comic_list, strip_details, comic_keys, ctx=ctx)
            else:
                await ctx.send("No comics to send!")
        else:
            await ctx.send("This guild is not subscribed to any comic!")

    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def update_database_remove(self, inter: discord.Interaction, number: str = None):
        # Remove the comic from all the servers
        if utils.is_owner(inter):
            try:
                number = int(number)
            except ValueError or TypeError:
                inter.response.send_message("This is not a valid comic number!")
                return

            data = utils.load_json(utils.DATABASE_FILE_PATH)
            if 0 <= number <= len(utils.strip_details):
                for guild in data:
                    channels = data[guild]["channels"]
                    for chan in channels:
                        dates = channels[str(chan)]["date"]
                        for date in dates:
                            hours = dates[date]
                            for hour in hours:
                                if number in hours[hour]:
                                    data[guild]["channels"][chan]["date"][date][hour].pop(hours[hour].index(number))

                utils.save_json(data)

                await inter.response.send_message("Updated the database by removing 1 comic to all servers.")

            else:
                await inter.response.send_message('Cannot find the index of the comic to remove!')
        else:
            raise commands.CommandNotFound

    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def update_database_clean(self, inter: discord.Interaction):
        # Clean the database from servers that don't have any comics saved
        if utils.is_owner(inter):
            nb_removed = utils.clean_database(strict=True)

            await inter.response.send_message(f'Cleaned the database from {nb_removed} inactive server(s).')
        else:
            raise commands.CommandNotFound

    @commands.hybrid_command()
    async def restore_last_backup(self, inter: discord.Interaction):
        if utils.is_owner(inter):
            # Stops the database cleaning and restore the last backup
            self.do_cleanup = False
            utils.restore_backup()

            await inter.response.send_message("Last backup restored! Please reboot the bot to re-enable automatic "
                                              "cleanups!")
        else:
            raise commands.CommandNotFound

    @commands.hybrid_command()
    @commands.check(lambda interaction: utils.is_owner(interaction))
    async def do_backup(self, inter: discord.Interaction):
        if utils.is_owner(inter):
            # Force a backup
            utils.save_backup(utils.load_json(utils.DATABASE_FILE_PATH))
            inter.response.send_message("Backup done!")
        else:
            raise commands.CommandNotFound


async def setup(client):  # Initialize the cog
    await client.add_cog(PosterHandler(client))
