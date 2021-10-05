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
        wait_until_hour = time(hour=6)  # 6 AM UTC

        if datetime.utcnow().hour < 6:
            day_wait = 0
        else:
            day_wait = 1

        wait_until_date = datetime.utcnow() + timedelta(days=day_wait)
        combined_date = datetime.combine(wait_until_date, wait_until_hour)
        await discord.utils.sleep_until(combined_date)
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
    @tasks.loop(hours=24.0)  # Daily loop
    async def post_daily(self):
        await self.daily()

    # Post daily comics
    async def daily(self):
        # Daily loop
        strip_details = self.strip_details
        NB_OF_COMICS = len(strip_details)
        comic_data = utils.get_database_data()
        comic_list = [""] * NB_OF_COMICS
        comic_keys = list(strip_details.keys())

        # Construct the list of what comics need to be sent
        for guild in comic_data:
            i = 0
            for char in comic_data[str(guild)]["ComData"]:
                if char == "1":
                    comic_list[i] += str(comic_data[str(guild)]["channel_id"]) + ";"

                i += 1

        # Check if any guild want the comic
        for i in range(len(comic_list)):
            if comic_list[i] != "":
                # Load the new details
                comic_details = Web_requests_manager.get_new_comic_details(strip_details[comic_keys[i]], "today")

                embed = utils.create_embed(comic_details)  # Creates the embed

                # Sends the comic to all subbed guilds
                for channel in comic_list[i].split(";"):
                    if channel is not None and channel != '':
                        channel = self.client.get_channel(int(channel))

                        await channel.send(embed=embed)

    # Make a change in the database
    def new_change(self, ctx, strip_details, param):
        comic_number = int(strip_details["Position"])

        utils.modify_database(self.strip_details, ctx, param, comics_number=comic_number)

    # Removes a guild from the database
    def remove_guild(self, ctx):
        utils.modify_database(self.strip_details, ctx, 'remove_guild')

    @commands.command()
    async def updateDatabaseadd(self, ctx):
        # Add one 0 to each "ComData" when changing the comic list
        if utils.is_owner(ctx):
            data = utils.get_database_data()

            for guild in data:
                data[guild]["ComData"] += "0"

            utils.save(data)

            await ctx.send("Updated the database by adding 1 one comic to all servers.")
        else:
            raise commands.CommandNotFound

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
