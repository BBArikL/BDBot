# Manages daily posting
import json
from discord import utils
from discord.ext import tasks, commands
from Scripts import BDbot, Web_requests_manager
import datetime
import os


class DailyPoster(commands.Cog):  # Class responsible for posting daily comic strips
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start_daily(self, ctx):  # Starts the DailyPoster loop
        if ctx.message.author.id == int(os.getenv('BOT_OWNER_ID')):
            await BDbot.BDBot.send_any(self, ctx,
                                       "Daily loop started! Daily comics are posted at 6:00 AM UTC each day.")

            await DailyPoster.wait_for_daily(self)
        else:
            await BDbot.BDBot.send_any(self, ctx, "You cannot do that.")

    async def wait_for_daily(self):
        wait_until_hour = datetime.time(hour=6, minute=0)

        if datetime.datetime.now().hour < 6:
            day_wait = 0
        else:
            day_wait = 1

        wait_until_date = datetime.date.today() + datetime.timedelta(days=day_wait)
        combined_date = datetime.datetime.combine(wait_until_date, wait_until_hour)

        await utils.sleep_until(combined_date)
        await DailyPoster.post_daily.start(self)

    @commands.command()
    async def is_daily_running(self, ctx):  # Checks the DailyPoster loop
        if ctx.message.author.id == int(os.getenv('BOT_OWNER_ID')):
            if DailyPoster.post_daily.is_running():
                await BDbot.BDBot.send_any(self, ctx, "The loop is running.")
            else:
                await BDbot.BDBot.send_any(self, ctx, "The loop is NOT running.")

        else:
            await BDbot.BDBot.send_any(self, ctx, "You cannot do that.")

    @tasks.loop(hours=24.0)  # Daily loop
    async def post_daily(self):
        # Daily loop
        main_website = ""
        comic_name = ""
        NB_OF_COMICS = int(os.getenv('NB_OF_COMICS'))
        comic_data = DailyPoster.get_database_data(self)
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
                # Define the comic that need to be sent
                if i == 0:
                    comic_name = 'Garfield'
                    main_website = 'https://www.gocomics.com/'
                elif i == 1:
                    comic_name = 'Garfield-Classics'
                    main_website = 'https://www.gocomics.com/'
                elif i == 2:
                    comic_name = 'CalvinandHobbes'
                    main_website = 'https://www.gocomics.com/'
                elif i == 3:
                    comic_name = 'XKCD'
                    main_website = 'https://xkcd.com/'
                elif i == 4:
                    comic_name = 'Peanuts'
                    main_website = 'https://www.gocomics.com/'
                elif i == 5:
                    comic_name = 'Peanuts-Begins'
                    main_website = 'https://www.gocomics.com/'
                elif i == 6:
                    comic_name = 'dilbert-classics'
                    main_website = 'https://www.gocomics.com/'

                if main_website == 'https://www.gocomics.com/':
                    # Specific manager for GoComics website
                    comic_details = Web_requests_manager.GoComicsManager.Comic_info(self, comic_name, param="today")
                else:  # Other websites
                    comic_details = Web_requests_manager.OtherSiteManager.Comic_info(self, comic_name, main_website,
                                                                                     param="today")

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

    def new_change(self, ctx, comic, param):  # Make a change in the database
        if comic == 'Garfield':
            comic_number = 0
        if comic == 'Garfield-Classics':
            comic_number = 1
        elif comic == "CalvinandHobbes":
            comic_number = 2
        elif comic == "XKCD":
            comic_number = 3
        elif comic == 'Peanuts':
            comic_number = 4
        elif comic == 'Peanuts-Begins':
            comic_number = 5
        elif comic == 'dilbert-classics':
            comic_number = 6

        if param == "add":
            DailyPoster.add(self, ctx, comic_number)
        if param == "remove":
            DailyPoster.remove(self, ctx, comic_number)

    def add(self, ctx, comic_number):  # Add a Comic to the comic list
        DailyPoster.save(self, ctx, 'add', comics_number=comic_number)

    def remove(self, ctx, comic_number):  # Remove a Comic to comic list
        DailyPoster.save(self, ctx, 'remove', comics_number=comic_number)

    def remove_guild(self, ctx):  # Removes a guild from the database
        DailyPoster.save(self, ctx, 'remove_guild')

    def updateDatabase(self, ctx):
        pass  # TODO to add/remove one 0 to each "ComData" when changing the comic list

    def save(self, ctx, use, comics_number=None):
        # Saves the new informations in the database
        # Adds or delete the guild_id, the channel id and the comic_strip data
        # Doesnt work, to construct the list THEN save it
        FILE_PATH = "./data/data.json"
        NB_OF_COMICS = int(os.getenv('NB_OF_COMICS'))

        if use == 'add' or use == 'remove':
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
        else:
            guild_id = str(ctx.id)

        data = DailyPoster.get_database_data(self)

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

        # Saves the file
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)


def setup(client):  # Initialize the cog
    client.add_cog(DailyPoster(client))
