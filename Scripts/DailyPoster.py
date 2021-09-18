# Manages daily posting
import json
from discord import utils
from discord.ext import tasks, commands
from Scripts import BDbot, Web_requests_manager
import datetime
import os
import Comics_details


class DailyPosterHandler(commands.Cog):  # Class responsible for posting daily comic strips
    stripDet = None

    def __init__(self, client):
        self.client = client


    def isOwner(self, ctx):
        return ctx.message.author.id == int(os.getenv('BOT_OWNER_ID'))

    @commands.command()
    async def start_daily(self, ctx):  # Starts the DailyPosterHandler loop
        if self.isOwner(ctx):
            await BDbot.BDBot.send_any(self, ctx,
                                       "Daily loop started! Daily comics are posted at 6:00 AM UTC each day.")

            await DailyPosterHandler.wait_for_daily(self, Comics_details.comDetails.load_details())
        else:
            raise commands.CommandNotFound

    async def wait_for_daily(self, stripDetails):
        DailyPosterHandler.stripDet = stripDetails
        wait_until_hour = datetime.time(hour=6, minute=0)

        if datetime.datetime.now().hour < 6:
            day_wait = 0
        else:
            day_wait = 1

        wait_until_date = datetime.date.today() + datetime.timedelta(days=day_wait)
        combined_date = datetime.datetime.combine(wait_until_date, wait_until_hour)

        await utils.sleep_until(combined_date)
        await DailyPosterHandler.post_daily.start(self)

    @commands.command()
    async def is_daily_running(self, ctx):  # Checks the DailyPosterHandler loop
        if self.isOwner(ctx):
            if DailyPosterHandler.post_daily.is_running():
                await BDbot.BDBot.send_any(self, ctx, "The loop is running.")
            else:
                await BDbot.BDBot.send_any(self, ctx, "The loop is NOT running.")

        else:
            raise commands.CommandNotFound

    @commands.command()
    async def force_daily(self, ctx):
        if self.isOwner(ctx):
            await self.daily()
        else:
            raise commands.CommandNotFound

    @tasks.loop(hours=24.0)  # Daily loop
    async def post_daily(self):
        await self.daily()

    async def daily(self):
        # Daily loop
        main_website = ""
        stripDetails = self.stripDet
        NB_OF_COMICS = len(stripDetails)
        comic_data = DailyPosterHandler.get_database_data(self)
        comic_list = [""] * NB_OF_COMICS


        # Construct the list of what comics need to be sent
        for guild in comic_data:
            i = 0
            for char in comic_data[str(guild)]["ComData"]:
                if char == "1":
                    comic_list[i] += str(comic_data[str(guild)]["channel_id"]) + ";"

                i += 1

        for i in range(len(comic_list)):
            if comic_list[i] != "":
                if stripDetails[i]["Main_website"] == 'https://www.gocomics.com/':
                    # Specific manager for GoComics website
                    comic_details = Web_requests_manager.ComicsRequestsManager.Comic_info_date(self, stripDetails[i],
                                                                                               param="today")
                else:  # Other websites
                    comic_details = Web_requests_manager.ComicsRequestsManager.Comic_info_date(self, stripDetails[i],
                                                                                          main_website)

                embed = BDbot.BDBot.create_embed(self, comic_details)  # Creates the embed

                # Sends the comic
                for channel in comic_list[i].split(";"):
                    if channel is not None and channel != '':
                        await BDbot.BDBot.send_comic_embed_channel_specific(self, embed, channel)

    def get_database_data(self):
        # Returns the ids and what need to be sent
        FILE_PATH = "./data/data.json"

        # Loads the prefixes file
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)

        return data

    def save(self, data):
        FILE_PATH = "./data/data.json"

        # Saves the file
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)

    def new_change(self, ctx, stripDetails, param):  # Make a change in the database
        comic_number = int(stripDetails["Position"])

        if param == "add":
            DailyPosterHandler.add(self, ctx, comic_number)
        if param == "remove":
            DailyPosterHandler.remove(self, ctx, comic_number)

    def add(self, ctx, comic_number):  # Add a Comic to the comic list
        DailyPosterHandler.modifyDatabase(self, ctx, 'add', comics_number=comic_number)

    def remove(self, ctx, comic_number):  # Remove a Comic to comic list
        DailyPosterHandler.modifyDatabase(self, ctx, 'remove', comics_number=comic_number)

    def remove_guild(self, ctx):  # Removes a guild from the database
        DailyPosterHandler.modifyDatabase(self, ctx, 'remove_guild')

    @commands.command()
    async def updateDatabaseadd(self, ctx):
        # Add one 0 to each "ComData" when changing the comic list
        if self.isOwner(ctx):
            data = self.get_database_data()

            for guild in data:
                data[guild]["ComData"] += "0"

            DailyPosterHandler.save(self, data)

            await ctx.send("Updated the database by adding 1 one comic to all servers.")

    @commands.command()
    async def updateDatabaseremove(self, ctx, *, number=None):
        # Remove one 0 to each "ComData" when changing the comic list
        if self.isOwner(ctx):
            data = self.get_database_data()

            try:
                index = int(number.split(" ")[0])

                if 0 < index <= int(os.getenv('NB_OF_COMICS')):
                    for guild in data:
                        comData = list(data[guild]['ComData'])
                        comData.pop(index - 1)
                        data[guild]['ComData'] = ''.join(comData)

                    DailyPosterHandler.save(self, data)

                    await ctx.send("Updated the database by removing 1 one comic to all servers.")

                else:
                    await ctx.send('Cannot find the index of the comic to remove!')

            except ValueError:
                await ctx.send('This is not a valid comic number!')

    @commands.command()
    async def updateDatabaseclean(self, ctx, *, number=None):
        # Clean the database from servers that don't have any daily comics saved
        if self.isOwner(ctx):
            data = self.get_database_data()
            blank_com_data = '0' * int(os.getenv('NB_OF_COMICS'))
            guilds_to_clean = []
            nb_removed = 0

            for guild in data:
                if data[guild]['ComData'] == blank_com_data:
                    nb_removed += 1
                    guilds_to_clean.append(guild)

            for guild in guilds_to_clean:
                data.pop(guild)

            DailyPosterHandler.save(self, data)

            await ctx.send(f'Cleaned the database from {nb_removed} inactive server(s).')

    def modifyDatabase(self, ctx, use, comics_number=None):
        # Saves the new informations in the database
        # Adds or delete the guild_id, the channel id and the comic_strip data
        NB_OF_COMICS = int(os.getenv('NB_OF_COMICS'))

        if use == 'add' or use == 'remove':
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
        else:
            guild_id = str(ctx.guild.id)

        data = DailyPosterHandler.get_database_data(self)

        if use == 'add':
            d = {
                guild_id: {
                    "server_id": None,
                    "channel_id": None,
                    "ComData": None
                }
            }

            if guild_id in data:  # If this server was already in the database, fill out information
                d[guild_id]["server_id"] = data[guild_id]["server_id"]
                d[guild_id]["channel_id"] = data[guild_id]["channel_id"]
                d[guild_id]["ComData"] = data[guild_id]["ComData"]

                # If there is already comic data stored
                comic_str = list(d[guild_id]["ComData"])

                comic_str[comics_number] = "1"

                d[guild_id]["ComData"] = "".join(comic_str)

            else:
                # Add a comic to the list of comics
                d[guild_id]["server_id"] = int(guild_id)

                d[guild_id]["channel_id"] = int(channel_id)

                # If there was no comic data stored for this guild
                comic_str = ""

                # Construct the string of data
                for i in range(NB_OF_COMICS):
                    if i == comics_number:
                        comic_str += "1"
                    else:
                        comic_str += "0"

                d[guild_id]["ComData"] = comic_str

            data.update(d)

        elif use == "remove":  # Remove comic
            if guild_id in data:
                comic_str = list(data[guild_id]["ComData"])
                if comic_str[comics_number] != "0":
                    comic_str[comics_number] = "0"
                    data[guild_id]["ComData"] = "".join(comic_str)

        elif use == 'remove_guild':  # Remove a guild from the list
            if guild_id in data:
                data.pop(guild_id)

        DailyPosterHandler.save(self, data)

    # Check if the comic is subscribed to this guild
    def get_sub_status(self, guild_id, position, database=None):
        if database is None:  # Gets database if needed
            database = DailyPosterHandler.get_database_data(self)

        if guild_id in database:
            return database[guild_id]["ComData"][position-1] == "1"
        else:
            return False


def setup(client):  # Initialize the cog
    client.add_cog(DailyPosterHandler(client))
