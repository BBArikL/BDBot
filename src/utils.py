# Collection of static methods
import logging
import re
import discord
import random
import json

from src import Web_requests_manager
from jsonschema import validate, ValidationError
from datetime import datetime, timedelta, timezone
from randomtimestamp import randomtimestamp
from discord.ext import commands
from typing import Union
from os import getenv, path

DETAILS_PATH = "src/misc/comics_details.json"
FOOTERS_FILE_PATH = 'src/misc/random-footers.txt'
DATABASE_FILE_PATH = "src/data/data.json"
JSON_SCHEMA_PATH = "src/misc/databaseSchema.json"
BACKUP_FILE_PATH = "src/data/backups/BACKUP_DATABASE_"
REQUEST_FILE_PATH = "src/data/requests.txt"
COMIC_LATEST_LINKS_PATH = "src/data/latest_comics.json"
date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "La"]
match_date = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
    "Su": "Sunday",
    "D": "day",
    "La": "Latest"
}
Success = "Success"
logger = logging.getLogger('discord')
strip_details: dict = {}
link_cache: dict = {}
random_footers: list[str] = []
SERVER = None


# Create a comic embed with the given details
def create_embed(comic_details: dict = None):
    if comic_details is not None:
        # Embeds the comic
        comic_name = comic_details["Name"]
        comic_title = comic_details["title"]
        author = comic_details["author"]
        day = comic_details["day"]
        month = comic_details["month"]
        year = comic_details["year"]
        url = comic_details["url"]
        color = comic_details["color"]

        if comic_details["alt"] is not None:
            alt = comic_details["alt"]
        else:
            alt = ""

        if comic_details["sub_img_url"] != "":
            thumbnail = comic_details["sub_img_url"]
        else:
            thumbnail = ""

        img_url = clean_url(comic_details["img_url"])

        # Creates the embed
        embed = discord.Embed(title=comic_title, url=url, description=alt, colour=color)

        if thumbnail != "":  # Thumbnail for Webtoons
            embed.set_thumbnail(url=thumbnail)

        if day is not None and day != "":
            embed.add_field(name=f'{comic_name} by {author}', value=f"Date: {day}/{month}/{year}")

        embed.set_image(url=img_url)

        embed.set_footer(text=get_random_footer())

        return embed
    else:
        # Error message
        embed = discord.Embed(title="No comic found!")

        embed.add_field(name="We could not find a comic at this date / number :thinking:....",
                        value="Try another date / number!")

        embed.set_footer(text=get_random_footer())

        return embed


# Sends comics info in an embed
async def send_comic_info(ctx: commands.Context, comic: dict):
    embed = discord.Embed(title=f'{comic["Name"]} by {comic["Author"]}',
                          url=get_link(comic),
                          description=comic["Description"], color=int(comic["Color"], 16))
    embed.set_thumbnail(url=comic["Image"])
    embed.add_field(name="Working type", value=comic["Working_type"], inline=True)

    if comic["Working_type"] == "date":
        embed.add_field(name="First apparition", value=get_date(get_first_date(comic)), inline=True)
    embed.add_field(name="Aliases", value=comic["Aliases"], inline=True)

    if get_sub_status(ctx, int(comic["Position"])):
        sub_stat = "Yes"
    else:
        sub_stat = "No"

    embed.add_field(name="Subscribed", value=sub_stat, inline=True)
    embed.set_footer(text="Random footer")
    embed.set_footer(text=get_random_footer())

    await ctx.send(embed=embed)


# Post the strip (with the given parameters)
async def comic_send(ctx: commands.Context, comic: dict, param: str, comic_date=None):
    comic_details = Web_requests_manager.get_new_comic_details(comic, param, comic_date=comic_date)

    # Sends the comic
    await send_comic_embed(ctx, comic_details)


# Interprets the parameters given by the user
async def parameters_interpreter(ctx: commands.Context, comic_details, param=None, date=None, hour=None):
    if param is not None:
        """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send
            """
        param = param.lower()

        if param == "today" or param == "tod":
            # Sends the website of today's comic
            await comic_send(ctx, comic_details, "today")
        elif param == "random" or param == "rand" or param == "rnd":
            # Random comic
            await comic_send(ctx, comic_details, "random")
        elif param == "add":
            # Add the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                status = new_change(ctx, comic_details, "add", date=date, hour=hour)
                if status == Success:
                    await ctx.send(f"{comic_details['Name']} added successfully as a daily comic!")
                else:
                    await ctx.send(status)
            else:
                await ctx.send("You need `manage_guild` permission to do that!")
        elif param == "remove":
            # Remove the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                status = new_change(ctx, comic_details, "remove", date=date, hour=hour)
                if status == Success:
                    await ctx.send(
                        f"{comic_details['Name']} removed successfully from the daily list!")
                else:
                    await ctx.send(status)
            else:
                await ctx.send("You need `manage_guild` permission to do that!")
        else:
            # Tries to parse date / number of comic
            working_type = comic_details["Working_type"]
            if working_type == "date" or comic_details["Main_website"] == 'https://garfieldminusgarfield.net/':
                # Works by date
                try:
                    comic_date = datetime.strptime(param, "%d/%m/%Y")
                    first_date = datetime.strptime(get_first_date(comic_details), "%Y, %m, %d")
                    if first_date.timestamp() <= comic_date.timestamp() <= datetime.now(timezone.utc).timestamp():
                        await comic_send(ctx, comic_details, "Specific_date", comic_date=comic_date)
                    else:
                        first_date_formatted = datetime.strftime(first_date, "%d/%m/%Y")
                        date_now_formatted = datetime.strftime(datetime.now(timezone.utc), "%d/%m/%Y")
                        await ctx.send(
                            f"Invalid date. Try sending a date between {first_date_formatted} and "
                            f"{date_now_formatted}.")
                except ValueError:
                    await ctx.send("This is not a valid date format! The format is : DD/MM/YYYY.")
            else:
                # Works by number of comic
                try:
                    number = int(param.split(" ")[0])
                    if number >= int(get_first_date(comic_details)):
                        if working_type == "number":
                            comic_details["Main_website"] = comic_details["Main_website"] + str(number) + '/'
                            await comic_send(ctx, comic_details, param=param)
                        else:
                            await comic_send(ctx, comic_details, "Specific_date", comic_date=number)
                    else:
                        await ctx.send("There is no comics with such values!")

                except ValueError:
                    await ctx.send('This is not a valid comic number!')
    else:
        # If the user didn't send any parameters, return the information the comic requested
        await send_comic_info(ctx, comic_details)


def add_all(ctx: commands.Context, date=None, hour=None):
    final_date, final_hour = parse_all(date, hour)

    return modify_database(ctx, "add_all", day=final_date, hour=str(final_hour))


# Make a change in the database
def new_change(ctx: commands.Context, comic, param, date=None, hour=None):
    final_date, final_hour = parse_all(date, hour)

    comic_number = int(comic["Position"])

    return modify_database(ctx, param, day=final_date, hour=str(final_hour), comic_number=comic_number)


# Removes a guild from the database
def remove_guild(ctx: commands.Context, use: str = 'remove_guild'):
    return modify_database(ctx, use)


# Removes a channel from the database
def remove_channel(ctx: commands.Context, use="remove_channel"):
    return modify_database(ctx, use)


def modify_database(ctx: Union[commands.Context, discord.TextChannel, discord.Guild], use: str, day: str = None,
                    hour: str = None, comic_number: int = None):
    # Saves the new information in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    # All use cases
    add = "add"
    a_all = "add_all"
    remove_c = "remove"
    remove_g = "remove_guild"
    fremove_g = "auto_remove_guild"
    remove_chan = "remove_channel"
    fremove_chan = "auto_remove_guild"
    data = load_json(DATABASE_FILE_PATH)

    if use == add or use == a_all:
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        d = {
            guild_id: {
                "server_id": 0,
                "channels": {
                },
                "mention": True
            }
        }

        """
        Example of a specific channel data:
        channel_specific_data = {
            channel_id: {
                "channel_id": 0,
                "date": {
                    "6":[0],
                }
            },
        }
        """

        if guild_id in data:
            # If this server was already in the database, fill out information
            d[guild_id] = data[guild_id]

            # Checks if the channel was already set
            if channel_id in data[guild_id]["channels"]:
                d[guild_id]["channels"][channel_id] = data[guild_id]["channels"][channel_id]
            else:
                d[guild_id]["channels"].update({channel_id: {"channel_id": int(channel_id), "date": {}}})

            if day is None:
                day = "D"  # Default: Daily

            if hour is None:
                hour = "6"  # Default: 6 AM UTC

            com_list: list[int]
            if use == a_all:
                strips = load_json(DETAILS_PATH)
                com_list = [i for i in range(len(strips))]
            else:
                com_list = [comic_number]

            if day != "La":
                # Checks if the day, the hour and the comic was already set for the channel
                if day not in d[guild_id]["channels"][channel_id]["date"]:
                    d[guild_id]["channels"][channel_id]["date"].update({day: {hour: com_list}})

                elif hour not in d[guild_id]["channels"][channel_id]["date"][day]:
                    d[guild_id]["channels"][channel_id]["date"][day].update({hour: com_list})

                elif comic_number not in d[guild_id]["channels"][channel_id]["date"][day][hour] and len(com_list) == 1:
                    d[guild_id]["channels"][channel_id]["date"][day][hour].extend(comic_number)

                elif len(com_list) > 1:  # Add all comics command
                    d[guild_id]["channels"][channel_id]["date"][day][hour] = com_list

                else:
                    return "This comic is already set at this time!"
            else:
                # Add a comic to be only latest
                if "latest" not in d[guild_id]["channels"][channel_id]:
                    d[guild_id]["channels"][channel_id].update({"latest": com_list})
                elif comic_number not in d[guild_id]["channels"][channel_id]["latest"] and len(com_list) == 1:
                    d[guild_id]["channels"][channel_id]["latest"].extend(com_list)
                elif len(com_list) > 1:
                    d[guild_id]["channels"][channel_id]["latest"] = com_list
                else:
                    return "This comic is already set at this time!"

        else:
            # If there was no comic data stored for this guild
            # Add a comic to the list of comics
            d[guild_id]["server_id"] = int(guild_id)

            com_list: list
            if use == a_all:
                strips = load_json(DETAILS_PATH)
                com_list = [i for i in range(len(strips))]
            else:
                com_list = [comic_number]

            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            if day != "La":
                d[guild_id]["channels"].update({channel_id: {"channel_id": int(channel_id),
                                                             "date": {day: {hour: com_list}}}})
            else:
                d[guild_id]["channels"].update({channel_id: {"channel_id": int(channel_id), "latest": com_list}})
        # Update the main database
        data.update(d)

    elif use == remove_c:
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        # Remove comic
        if guild_id in data and channel_id in data[guild_id]["channels"]:
            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            if day != "La":
                # Verifies that the day and time was set
                if day in data[guild_id]["channels"][channel_id]["date"] and hour in \
                        data[guild_id]["channels"][channel_id]["date"][day]:
                    comic_list: list[int] = data[guild_id]["channels"][channel_id]["date"][day][hour]

                    # Verifies if the comic is in the list
                    if comic_number in comic_list:
                        comic_list.remove(comic_number)
                        data[guild_id]["channels"][channel_id]["date"][day][hour] = comic_list

                    else:
                        return "This comic is not registered for scheduled posts!"
                else:
                    return "This comic is not registered for scheduled posts!"
            else:
                comic_list: list[int] = data[guild_id]["channels"][channel_id]["latest"]
                if comic_number in comic_list:
                    comic_list.remove(comic_number)
                    data[guild_id]["channels"][channel_id]["latest"] = comic_list
                else:
                    return "This comic is not registered for scheduled posts!"
        else:
            return "This guild or channel is not registered for scheduled comics!"

    elif use == remove_g or use == fremove_g:
        guild_id = ""
        if use == 'remove_guild':
            guild_id = str(ctx.guild.id)
        elif use == 'auto_remove_guild':
            guild_id = str(ctx.id)  # it is a guild

        # Remove a guild from the list
        if guild_id in data:
            data.pop(guild_id)
        else:
            return "This guild is not registered for any scheduled comics!"

    elif use == remove_chan or use == fremove_chan:
        guild_id = str(ctx.guild.id)
        channel_id = ""
        if use == 'remove_channel':
            channel_id = str(ctx.channel.id)
        elif use == 'auto_remove_channel':
            channel_id = str(ctx.id)  # it is a channel

        # Remove a guild from the list
        if guild_id in data:
            if channel_id in data[guild_id]["channels"]:
                data[guild_id]["channels"].pop(channel_id)
            else:
                return "This channel is not registered for any scheduled comics!"
        else:
            return "This guild is not registered for any scheduled comics!"

    # Save the database
    save_json(data)

    return Success


def set_role(ctx: commands.Context, role_id):
    gid = str(ctx.guild.id)
    role = "role"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "Please re-enable the mention before daily post by using `bd!post_mention enable`!"

        if role not in data[gid]:
            data[gid].update({
                "role": role_id.id,
                "only_daily": False
            })
        else:
            data[gid]["role"] = role_id.id

        save_json(data)

        return Success
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before entering a role to add."


def set_mention(ctx: commands.Context, choice):
    gid = str(ctx.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "The base mention is disabled in this guild! " \
                   "Re-enable the mention before daily post by using `bd!post_mention enable`."

        if only_daily in data[gid]:
            data[gid][only_daily] = choice

            save_json(data)

            return Success
        else:
            return "This guild has no role set up! Please use `bd!set_up <role>` to add a role before deciding if " \
                   "you want to be notified of all comic or only the daily ones."
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before deciding when you want " \
               "to be mentioned!"


def get_mention(ctx):
    gid = str(ctx.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "The base mention is disabled in this guild! " \
                   "Re-enable the mention before hourly post by using `bd!post_mention enable`.", ""

        if only_daily in data[gid]:
            men = "only for daily comics posts"
            if not data[gid][only_daily]:
                men = "for all comic posts"

            return Success, men
        else:
            return "This guild has no role set up! Please use `bd!set_role @<role>` to add a role before deciding if " \
                   "you want to be notified of all comic or only the daily ones.", ""
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before deciding when you want " \
               "to be mentioned!", ""


def remove_role(ctx):
    gid = str(ctx.guild.id)
    role = "role"
    only_daily = "only_daily"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if role in data[gid]:

            data[gid].pop(role)
            data[gid].pop(only_daily)

            save_json(data)

            return Success
        else:
            return "This guild is not set to mention any role!"
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before managing the role " \
               "mentions!"


# Change if the bot says a phrase before posting daily comics
def set_post_mention(ctx, choice):
    gid = str(ctx.guild.id)
    mention = "mention"
    role = "role"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if role not in data[gid]:
            data[gid][mention] = choice
        else:
            return "A role is already set up to be mentioned daily! Remove the role before changing the post mention" \
                   " by using `bd!remove_role`."

        save_json(data)

        return Success
    else:
        return "This server is not registered for any comics!"


def load_json(json_path: str) -> dict:
    """
    Load a json.
    DETAILS_PATH -> The comic details.
    DATABASE_FILE_PATH -> The database.
    JSON_SCHEMA_PATH -> The schema of the database.
    BACKUP_FILE_PATH -> The default backup.
    COMIC_LATEST_LINKS_PATH -> The latest links to the images of the comics.

    :param json_path: The path to the json file.
    :return: The json as a dict.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)

    return json_file


# Returns a specific guild's data
def get_specific_guild_data(ctx: discord.Interaction):
    database = load_json(DATABASE_FILE_PATH)
    guild_id = str(ctx.guild.id)

    if guild_id in database:
        return database[guild_id]
    else:
        return None


def clean_database(data: dict = None, do_backup: bool = True, strict: bool = False):
    logger.info("Running database clean...")
    # Cleans the database from inactive servers
    if data is None:
        data = load_json(DATABASE_FILE_PATH)

    if do_backup:
        save_backup(data)

    guilds_to_clean = []
    nb_removed = 0

    for guild in data:
        # To take in account or not if a server still has a role tied to their info
        if "role" not in data[guild] or strict:
            to_remove = True
            channels = data[guild]["channels"]
            for chan in channels:
                dates = channels[chan]["date"]
                for date in dates:
                    hours = dates[date]
                    for hour in hours:
                        if len(hours[hour]) > 0:
                            to_remove = False
                            break
                    if not to_remove:
                        break
                if not to_remove:
                    break

            if to_remove:
                guilds_to_clean.append(guild)
                nb_removed += 1

    if nb_removed > 0:
        save_json(data)

    logger.info(f"Cleaned the database from {nb_removed} servers")
    return nb_removed


def save_backup(data):
    logger.info("Running backup...")
    # Creates a new backup and saves it
    backupfp = BACKUP_FILE_PATH + datetime.now(timezone.utc).strftime("%Y_%m_%d_%H") + ".json"

    with open(backupfp, 'w') as f:
        json.dump(data, f)

    logger.info("Backup successfully done")


def restore_backup():
    # Restore a last used backup
    utc_date = datetime.now(timezone.utc)
    file_path = BACKUP_FILE_PATH + utc_date.strftime("%Y_%m_%d_%H") + ".json"
    tries = 0

    while not path.exists(file_path) and tries < 25:
        tries += 1
        utc_date = utc_date - timedelta(hours=1)
        file_path = BACKUP_FILE_PATH + utc_date.strftime("%Y_%m_%d_%H") + ".json"

    if tries < 25:
        with open(file_path, 'r') as f:
            database = json.load(f)

        if database != "":
            save_json(database)
    else:
        raise Exception("No backup was found in the last 24 hours!!")


def save_json(json_file: dict, file_path: str = DATABASE_FILE_PATH):
    # Saves the json file
    with open(file_path, 'w') as f:
        json.dump(json_file, f, indent=4)


def verify_json():
    # Verifies the database according to a particular json schema to assure the integrity of it
    data = load_json(DATABASE_FILE_PATH)
    schema = load_json(JSON_SCHEMA_PATH)

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False


# Check if the comic is subscribed to this guild
def get_sub_status(ctx, position: int, database: dict = None):
    if database is None:  # Gets database if needed
        database = load_json(DATABASE_FILE_PATH)

    guild_id = str(ctx.guild.id)

    if guild_id in database:
        guild_data = database[guild_id]
        for channel in guild_data["channels"]:
            for day in guild_data["channels"][channel]["date"]:
                for hour in guild_data["channels"][channel]["date"][day]:
                    if position in guild_data["channels"][channel]["date"][day][hour]:
                        return True
        return False
    else:
        return False


# Send a comic embed
async def send_comic_embed(ctx: commands.Context, comic_details):
    embed = create_embed(comic_details=comic_details)  # Creates the embed

    await ctx.send(embed=embed)  # Send the comic


# If the request is not understood
async def send_request_error(ctx: commands.Context):
    await ctx.send('Request not understood. Try bd!help for usable commands.')


def is_owner(ctx: commands.Context):  # Returns if it is the owner who did the command
    return ctx.message.author.id == int(getenv('BOT_OWNER_ID'))


async def website_specific_embed(ctx: commands.Context, website_name, website):
    nb_per_embed = 25
    strips = strip_details
    i = 0

    embed = discord.Embed(title=f"{website_name}!")
    embed.set_footer(text=get_random_footer())
    for strip in strips:
        if strips[strip]["Main_website"] == website:
            i += 1

            embed.add_field(name=strips[strip]['Name'], value=f"{strips[strip]['Helptxt']}\nAliases: "
                                                              f"{strips[strip]['Aliases']}")
            if i == nb_per_embed:
                await ctx.send(embed=embed)
                i = 0
                # Reset the embed to create a new one
                embed = discord.Embed(title=f"{website_name}!")
                embed.set_footer(text=get_random_footer())

    if i != 0:
        await ctx.send(embed=embed)


# -------------------------------------------------------------------------------------------------------------------

# Reformat the date
def get_date(date: str):
    return datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")


def get_first_date(comic: dict):
    if comic["Main_website"] == "https://comicskingdom.com/":
        # Comics kingdom only lets us go back 7 days in the past
        return (datetime.today() - timedelta(days=7)).strftime("%Y, %m, %d")
    else:
        return comic["First_date"]


def get_today():
    return datetime.now(timezone.utc).today().strftime("%A")[0:2]


def get_hour():
    return str(datetime.now(timezone.utc).hour)


def clean_url(url: str, file_forms: list = None):
    # Gives back a clean link for a file on the internet, without the arguments after a "?"
    if file_forms is None:
        file_forms = ["png", "jpg", "jpeg", "gif", "jfif", "bmp", "tif", "tiff", "eps"]

    for file_form in file_forms:
        url = re.sub(f"\\.{file_form}\\?.*$", f".{file_form}", url)

    url = url.replace(" ", "%20")

    return url


def get_link(comic: dict, day: datetime = None):  # Returns the comic url
    date_formatted = ""
    middle_params = ""
    if comic["Main_website"] == "https://www.gocomics.com/":
        date_formatted = get_date_formatted(day=day)
        middle_params = comic["Web_name"]
    elif comic["Main_website"] == "https://comicskingdom.com/":
        date_formatted = get_date_formatted(day=day, form="-")
        middle_params = comic["Web_name"]
    elif comic["Main_website"] == "https://dilbert.com/":
        date_formatted = day.strftime("%Y-%m-%d")
        middle_params = "strip"

    return f'{comic["Main_website"]}{middle_params}/{date_formatted}'


def get_date_formatted(day: datetime = None, form="/"):
    if day is not None:
        return day.strftime(f"%Y{form}%m{form}%d")
    else:
        return ""


def get_random_link(comic: dict):  # Returns the random comic url
    if comic["Main_website"] == "https://www.gocomics.com/":
        return f'{comic["Main_website"]}random/{comic["Web_name"]}', None
    else:
        first_date = datetime.strptime(get_first_date(comic), "%Y, %m, %d")
        random_date = randomtimestamp(start=first_date,
                                      end=datetime.today().replace(hour=0, minute=0, second=0,
                                                                   microsecond=0))
        middle_params = ""
        if comic["Main_website"] == "https://comicskingdom.com/":
            middle_params = comic["Web_name"]
        elif comic["Main_website"] == "https://dilbert.com/":
            middle_params = "strip"

        return f'{comic["Main_website"]}{middle_params}/{random_date.strftime("%Y-%m-%d")}', random_date


def get_strip_details(comic_name: str):
    return strip_details[comic_name]


def create_link_cache() -> None:
    logger.debug("Running link cache...")
    comics = load_json(DETAILS_PATH)
    for comic in comics:
        logger.debug(f"Getting image link for comic {comic} ...")
        try:
            comic_url = Web_requests_manager.get_new_comic_details(comics[comic], param="today")
        except (ValueError, AttributeError) as e:
            logger.error(f"An error occurred for comic {comic}: {e}")
            comic_url = None
        link_cache.update({comics[comic]["Name"]: comic_url["img_url"] if comic_url is not None else ""})

    logger.debug("Saving comics link...")
    save_json(link_cache, COMIC_LATEST_LINKS_PATH)


# Get a random footer
def get_random_footer() -> str:
    rnd_footer = random.choice(get_footers())

    return rnd_footer.replace('\n', '')


def get_footers() -> list[str]:
    if random_footers is None or random_footers == []:
        return open(FOOTERS_FILE_PATH, 'rt').readlines()
    else:
        return random_footers


def parse_all(date=None, hour=None, default_date="D", default_hour=6) -> (str, str):
    final_date = default_date
    final_hour = default_hour

    final_date, final_hour = parse_try(date, final_date, final_hour)
    final_date, final_hour = parse_try(hour, final_date, final_hour)

    return final_date, final_hour


def parse_try(to_parse, final_date, final_hour) -> (str, str):
    if to_parse is not None:
        if len(str(to_parse)) >= 2:
            date = to_parse[0:1].capitalize() + to_parse[1:2].lower()

            if date in date_tries:
                final_date = date
            else:
                try:
                    final_hour = int(to_parse)
                except ValueError:
                    pass
        else:
            try:
                final_hour = int(to_parse)
            except ValueError:
                pass

    return final_date, final_hour


def check_if_latest_link(comic_name: str, current_link: str) -> bool:
    return current_link != link_cache[comic_name]
