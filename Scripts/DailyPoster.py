from discord.ext import tasks, commands
import discord
from datetime import datetime, timedelta, time
from Comics_details import comDetails
import utils
import Web_requests_manager


# Manages daily posting
class DailyPosterHandler(commands.Cog):
    # Class responsible for posting daily comic strips

    def __init__(self, client):
        self.client = client
        self.strip_details = comDetails.load_details()

    @commands.command()
    async def start_daily(self, ctx):
        # Starts the DailyPosterHandler loop
        if utils.is_owner(ctx):
            await ctx.send("Daily loop started! Daily comics are posted at 6:00 AM UTC each day.")

            await DailyPosterHandler.wait_for_daily(self)
        else:
            raise commands.CommandNotFound

    # Wait for the time to post the daily strip
    async def wait_for_daily(self):
        sleep_date = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        await discord.utils.sleep_until(sleep_date)
        await DailyPosterHandler.post_daily.start(self)

    # Checks if the daily loop is running
    @commands.command()
    async def is_daily_running(self, ctx):  # Checks the DailyPosterHandler loop
        if utils.is_owner(ctx):
            if DailyPosterHandler.post_daily.is_running():
                await ctx.send("The loop is running.")
            else:
                await ctx.send("The loop is NOT running.")

        else:
            raise commands.CommandNotFound

    # Force the push of comics to all subscribed guilds
    @commands.command()
    async def force_daily(self, ctx):
        if utils.is_owner(ctx):
            await self.daily()
        else:
            raise commands.CommandNotFound

    # Loop to post daily comics
    @tasks.loop(hours=1)  # Hourly loop
    async def post_daily(self):
        await self.daily()

    # Post daily comics
    async def daily(self):
        # Daily loop
        strip_details = self.strip_details
        NB_OF_COMICS = len(strip_details)
        comic_data = utils.get_database_data()
        comic_list = {}
        comic_keys = list(strip_details.keys())
        post_days = ["D", utils.get_today()]
        hour = utils.get_hour()

        # Construct the list of what comics need to be sent
        for pos in range(NB_OF_COMICS):
            for guild in comic_data:
                guild_data = comic_data[guild]
                for channel in guild_data["channels"]:
                    for day in post_days:
                        if day in guild_data["channels"][str(channel)]["date"]:
                            if hour in guild_data["channels"][str(channel)]["date"][day]:
                                if pos in guild_data["channels"][str(channel)]["date"][day][hour]:
                                    if channel not in comic_list:
                                        role = None
                                        if ('only_daily' in guild_data) and ((guild_data["only_daily"] == 0)
                                                                             or (hour == "6")) and ("role" in guild_data):
                                            role = discord.Guild.get_role(
                                                self.client.get_guild(guild_data["server_id"]), guild_data["role"])

                                        comic_list.update({
                                            channel: {
                                                "channel": channel,
                                                "comics": [pos],
                                                "role": role,
                                                "hasBeenMentionned": 0
                                            }
                                        })
                                    else:
                                        comic_list[channel]["comics"].append(pos)

        # Check if any guild want the comic
        for i in range(len(strip_details)):
            count = 0
            for chan in comic_list:
                if i in comic_list[chan]["comics"]:
                    count += 1
                    break

            if count > 0:
                comic_details = Web_requests_manager.get_new_comic_details(strip_details[comic_keys[i]], "today")

                embed = utils.create_embed(comic_details)  # Creates the embed

                for channel in comic_list:
                    # Load the new details
                    # Sends the comic to all subbed guilds
                    if i in comic_list[channel]["comics"]:
                        chan = self.client.get_channel(int(comic_list[channel]["channel"]))

                        if chan is not None:
                            try:
                                if comic_list[channel]["hasBeenMentionned"] == 0:
                                    if comic_list[channel]["role"] is not None:
                                        role_mention = comic_list[channel]["role"].mention
                                    else:
                                        role_mention = ""

                                    await chan.send(f"Comics for "
                                                    f"{datetime.utcnow().strftime('%A the %d %B %Y, %H h UTC')} "
                                                    f"{role_mention}")
                                    comic_list[channel]["hasBeenMentionned"] = 1

                                await chan.send(embed=embed)
                            except Exception:
                                continue

    @commands.command()
    async def updateDatabaseremove(self, ctx, *, number=None):
        # Remove one 0 to each "ComData" when changing the comic list
        if utils.is_owner(ctx):
            data = utils.get_database_data()

            try:
                index = int(number.split(" ")[0])

                if 0 < index <= len(self.strip_details):
                    for guild in data:
                        com_data = list(data[guild]['ComData'])
                        com_data.pop(index - 1)
                        data[guild]['ComData'] = ''.join(com_data)

                    utils.save(data)

                    await ctx.send("Updated the database by removing 1 comic to all servers.")

                else:
                    await ctx.send('Cannot find the index of the comic to remove!')

            except ValueError:
                await ctx.send('This is not a valid comic number!')
        else:
            raise commands.CommandNotFound

    @commands.command()
    async def updateDatabaseclean(self, ctx):
        # Clean the database from servers that don't have any daily comics saved
        if utils.is_owner(ctx):
            data = utils.get_database_data()
            blank_com_data = '0' * len(self.strip_details)
            guilds_to_clean = []
            nb_removed = 0

            for guild in data:
                if data[guild]['ComData'] == blank_com_data:
                    nb_removed += 1
                    guilds_to_clean.append(guild)

            for guild in guilds_to_clean:
                data.pop(guild)

            utils.save(data)

            await ctx.send(f'Cleaned the database from {nb_removed} inactive server(s).')
        else:
            raise commands.CommandNotFound


def setup(client):  # Initialize the cog
    client.add_cog(DailyPosterHandler(client))
