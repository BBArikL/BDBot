# Collection of static methods
import logging
import re
import discord
import random
import json
import os

from src import Web_requests_manager
from jsonschema import validate, ValidationError
from datetime import datetime, timedelta, timezone
from randomtimestamp import randomtimestamp

DETAILS_PATH = "src/misc/comics_details.json"
FOOTERS_FILE_PATH = 'src/misc/random-footers.txt'
DATABASE_FILE_PATH = "src/data/data.json"
JSON_SCHEMA_FILE_PATH = "src/misc/databaseSchema.json"
BACKUP_FILE_PATH = "src/data/backups/BACKUP_DATABASE_"
REQUEST_FILE_PATH = "src/data/requests.txt"
date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
match_date = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
    "Su": "Sunday",
    "D": "day"
}
Success = "Success"
logger = logging.getLogger('discord')


# Get a random footer
def get_random_footer():
    footers = open(FOOTERS_FILE_PATH, 'r')

    rnd_footer = random.choice(footers.readlines())

    return rnd_footer.replace('\n', '')


# Create a comic embed with the given details
def create_embed(comic_details=None):
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


# Sends comics info in a embed
async def send_comic_info(ctx, strip_details):
    embed = discord.Embed(title=f'{strip_details["Name"]} by {strip_details["Author"]}',
                          url=get_link(strip_details),
                          description=strip_details["Description"], color=int(strip_details["Color"], 16))
    embed.set_thumbnail(url=strip_details["Image"])
    embed.add_field(name="Working type", value=strip_details["Working_type"], inline=True)

    if strip_details["Working_type"] == "date":
        embed.add_field(name="First apparition", value=get_date(get_first_date(strip_details)), inline=True)
    embed.add_field(name="Aliases", value=strip_details["Aliases"], inline=True)

    if get_sub_status(ctx, int(strip_details["Position"])):
        sub_stat = "Yes"
    else:
        sub_stat = "No"

    embed.add_field(name="Subscribed", value=sub_stat, inline=True)
    embed.set_footer(text="Random footer")
    embed.set_footer(text=get_random_footer())

    await ctx.send(embed=embed)


# Post the strip (with the given parameters)
async def comic_send(ctx, strip_details, param, comic_date=None):
    comic_details = Web_requests_manager.get_new_comic_details(strip_details, param, comic_date=comic_date)

    # Sends the comic
    await send_comic_embed(ctx, comic_details)


# Interprets the parameters given by the user
async def parameters_interpreter(ctx, strip_details, param=None, date=None, hour=None):
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
            await comic_send(ctx, strip_details, "today")
        elif param == "random" or param == "rand" or param == "rnd":
            # Random comic
            await comic_send(ctx, strip_details, "random")
        elif param == "add":
            # Add the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                status = new_change(ctx, strip_details, "add", date=date, hour=hour)
                if status == Success:
                    await ctx.send(f"{strip_details['Name']} added successfully as a daily comic!")
                else:
                    await ctx.send(status)
            else:
                await ctx.send("You need `manage_guild` permission to do that!")
        elif param == "remove":
            # Remove the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                status = new_change(ctx, strip_details, "remove", date=date, hour=hour)
                if status == Success:
                    await ctx.send(f"{strip_details['Name']} removed successfully from the daily list!")
                else:
                    await ctx.send(status)
            else:
                await ctx.send("You need `manage_guild` permission to do that!")
        else:
            # Tries to parse date / number of comic
            working_type = strip_details["Working_type"]
            if working_type == "date" or strip_details["Main_website"] == 'https://garfieldminusgarfield.net/':
                # Works by date
                try:
                    comic_date = datetime.strptime(param, "%d/%m/%Y")
                    first_date = datetime.strptime(get_first_date(strip_details), "%Y, %m, %d")
                    if first_date.timestamp() <= comic_date.timestamp() <= datetime.now(timezone.utc).timestamp():
                        await comic_send(ctx, strip_details, "Specific_date", comic_date=comic_date)
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
                    if number >= int(get_first_date(strip_details)):
                        if working_type == "number":
                            strip_details["Main_website"] = strip_details["Main_website"] + str(number) + '/'
                            await comic_send(ctx, strip_details, param=param)
                        else:
                            await comic_send(ctx, strip_details, "Specific_date", comic_date=number)
                    else:
                        await ctx.send("There is no comics with such values!")

                except ValueError:
                    await ctx.send('This is not a valid comic number!')
    else:
        # If the user didn't send any parameters, return informations the comic requested
        await send_comic_info(ctx, strip_details)


def add_all(ctx, date=None, hour=None):
    final_date, final_hour = parse_all(date, hour)

    return modify_database(ctx, "add_all", day=final_date, hour=str(final_hour))


# Make a change in the database
def new_change(ctx, strip_details, param, date=None, hour=None):
    final_date, final_hour = parse_all(date, hour)

    comic_number = int(strip_details["Position"])

    return modify_database(ctx, param, comic_number=comic_number, day=final_date, hour=str(final_hour))


def parse_all(date=None, hour=None, default_date="D", default_hour=6):
    final_date = default_date
    final_hour = default_hour

    final_date, final_hour = parse_try(date, final_date, final_hour)
    final_date, final_hour = parse_try(hour, final_date, final_hour)

    return final_date, final_hour


def parse_try(to_parse, final_date, final_hour):
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


# Removes a guild from the database
def remove_guild(guild, use=None):
    if use is None:
        use = 'remove_guild'

    return modify_database(guild, use)


# Removes a channel from the database
def remove_channel(ctx, use=None):
    if use is None:
        use = "remove_channel"

    return modify_database(ctx, use)


def modify_database(ctx, use, day=None, hour=None, comic_number=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    # All use cases
    add = "add"
    aAll = "add_all"
    removeC = "remove"
    removeG = "remove_guild"
    fremoveG = "auto_remove_guild"
    removeChan = "remove_channel"
    fremoveChan = "auto_remove_guild"
    data = get_database_data()

    if use == add or use == aAll:
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
        channel_specifc_data = {
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

            comList = []
            if use == aAll:
                strips = load_details()
                comList = [i for i in range(len(strips))]
            else:
                comList = [comic_number]

            # Checks if the day, the hour and the comic was already set for the channel
            if day not in d[guild_id]["channels"][channel_id]["date"]:
                d[guild_id]["channels"][channel_id]["date"].update({day: {hour: comList}})

            elif hour not in d[guild_id]["channels"][channel_id]["date"][day]:
                d[guild_id]["channels"][channel_id]["date"][day].update({hour: comList})

            elif comic_number not in d[guild_id]["channels"][channel_id]["date"][day][hour] and len(comList) == 1:
                d[guild_id]["channels"][channel_id]["date"][day][hour].append(comic_number)

            elif len(comList) > 1:  # Add all comics command
                d[guild_id]["channels"][channel_id]["date"][day][hour] = comList

            else:
                return "This comic is already set at this time!"

        else:
            # If there was no comic data stored for this guild
            # Add a comic to the list of comics
            d[guild_id]["server_id"] = int(guild_id)

            comList = []
            if use == aAll:
                strips = load_details()
                comList = [i for i in range(len(strips))]
            else:
                comList = [comic_number]

            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            d[guild_id]["channels"].update({channel_id: {"channel_id": int(channel_id),
                                                         "date": {day: {hour: comList}}}})
        # Update the main database
        data.update(d)

    elif use == removeC:
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        # Remove comic
        if guild_id in data and channel_id in data[guild_id]["channels"]:
            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            # Verifies that the day and time was set
            if day in data[guild_id]["channels"][channel_id]["date"] and hour in \
                    data[guild_id]["channels"][channel_id]["date"][day]:
                comic_list = data[guild_id]["channels"][channel_id]["date"][day][hour]

                # Verifies if the comic is in the list
                if comic_number in comic_list:
                    comic_list.remove(comic_number)
                    data[guild_id]["channels"][channel_id]["date"][day][hour] = comic_list

                else:
                    return "This comic is not registered for scheduled posts!"
            else:
                return "This comic is not registered for scheduled posts!"
        else:
            return "This guild or channel is not registered for scheduled comics!"

    elif use == removeG or use == fremoveG:
        guild_id = ""
        if use == 'remove_guild':
            guild_id = str(ctx.guild.id)
        elif use == 'auto_remove_guild':
            guild_id = str(ctx.id)

        # Remove a guild from the list
        if guild_id in data:
            data.pop(guild_id)
        else:
            return "This guild is not registered for any scheduled comics!"

    elif use == removeChan or use == fremoveChan:
        guild_id = str(ctx.guild.id)
        channel_id = ""
        if use == 'remove_channel':
            channel_id = str(ctx.channel.id)
        elif use == 'auto_remove_channel':
            channel_id = str(ctx.id)

        # Remove a guild from the list
        if guild_id in data:
            if channel_id in data[guild_id]["channels"]:
                data[guild_id]["channels"].pop(channel_id)
            else:
                return "This channel is not registered for any scheduled comics!"
        else:
            return "This guild is not registered for any scheduled comics!"

    # Save the database
    save(data)

    return Success


def set_role(ctx, roleID):
    gid = str(ctx.guild.id)
    role = "role"
    mention = "mention"
    data = get_database_data()

    if gid in data:
        if not data[gid][mention]:
            return "Please re-enable the mention before daily post by using `bd!post_mention enable`!"

        if role not in data[gid]:
            data[gid].update({
                "role": roleID.id,
                "only_daily": False
            })
        else:
            data[gid]["role"] = roleID.id

        save(data)

        return Success
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before entering a role to add."


def set_mention(ctx, choice):
    gid = str(ctx.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = get_database_data()

    if gid in data:
        if not data[gid][mention]:
            return "The base mention is disabled in this guild! " \
                   "Re-enable the mention before daily post by using `bd!post_mention enable`."

        if only_daily in data[gid]:
            data[gid][only_daily] = choice

            save(data)

            return Success
        else:
            return "This guild has no role set up! Please use `bd!set_up <role>` to add a role before deciding if " \
                   "you want to be notified of all comic or only the daily ones."
    else:
        return "This guild is not subscribed to any comic! Please subscribe to a comic before deciding when you want " \
               "to be mentionned!"


def get_mention(ctx):
    gid = str(ctx.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = get_database_data()

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
               "to be mentionned!", ""


def remove_role(ctx):
    gid = str(ctx.guild.id)
    role = "role"
    only_daily = "only_daily"
    data = get_database_data()

    if gid in data:
        if role in data[gid]:

            data[gid].pop(role)
            data[gid].pop(only_daily)

            save(data)

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
    data = get_database_data()

    if gid in data:
        if role not in data[gid]:
            data[gid][mention] = choice
        else:
            return "A role is already set up to be mentioned daily! Remove the role before changing the post mention" \
                   " by using `bd!remove_role`."

        save(data)

        return Success
    else:
        return "This server is not registered for any comics!"


def load_details():
    # Returns the comic details
    # Loads the comic details file
    with open(DETAILS_PATH, 'r', encoding='utf-8') as f:
        com_data = json.load(f)

    return com_data


# Returns the ids and what need to be sent
def get_database_data():
    # Loads the prefixes file
    with open(DATABASE_FILE_PATH, 'r') as f:
        data = json.load(f)

    return data


# Returns a specific guild's data
def get_specific_guild_data(ctx):
    database = get_database_data()
    guild_id = str(ctx.guild.id)

    if guild_id in database:
        return database[guild_id]
    else:
        return None


def clean_database(data=None, do_backup=True, strict=False):
    logger.info("Running database clean...")
    # Cleans the database from inactive servers
    if data is None:
        data = get_database_data()

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
        save(data)

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
    database = ""
    tries = 0

    while not os.path.exists(file_path) and tries < 25:
        tries += 1
        utc_date = utc_date - timedelta(hours=1)
        file_path = BACKUP_FILE_PATH + utc_date.strftime("%Y_%m_%d_%H") + ".json"

    if tries < 25:
        with open(file_path, 'r') as f:
            database = json.load(f)

        if database != "":
            save(database)
    else:
        raise Exception("No backup was found in the last 24 hours!!")


# Save the database
def save(data):
    # Saves the file
    with open(DATABASE_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)


def verify_json():
    # Verifies the database according to a particular json schema to assure the integrity of it
    data = get_database_data()
    schema = None

    with open(JSON_SCHEMA_FILE_PATH, 'r') as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False


# Check if the comic is subscribed to this guild
def get_sub_status(ctx, position, database=None):
    if database is None:  # Gets database if needed
        database = get_database_data()

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
async def send_comic_embed(ctx, comic_details):
    embed = create_embed(comic_details=comic_details)  # Creates the embed

    await ctx.send(embed=embed)  # Send the comic


# If the request is not understood
async def send_request_error(ctx):
    await ctx.send('Request not understood. Try bd!help for usable commands.')


def is_owner(ctx):  # Returns if it is the owner who did the command
    return ctx.message.author.id == int(os.getenv('BOT_OWNER_ID'))


# Reformat the date
def get_date(date):
    return datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")


def get_first_date(strip_details):
    if strip_details["Main_website"] == "https://comicskingdom.com/":
        # Comics kingdom only lets us go back 7 days in the past
        return (datetime.today() - timedelta(days=7)).strftime("%Y, %m, %d")
    else:
        return strip_details["First_date"]


def get_today():
    return datetime.now(timezone.utc).today().strftime("%A")[0:2]


def get_hour():
    return str(datetime.now(timezone.utc).hour)


def clean_url(url, file_forms=None):
    # Gives back a clean link for a file on the internet, without the arguments after a "?"
    if file_forms is None:
        file_forms = ["png", "jpg", "jpeg", "gif", "jfif", "bmp", "tif", "tiff", "eps"]

    for file_form in file_forms:
        url = re.sub(f"\\.{file_form}\\?.*$", f".{file_form}", url)

    url = url.replace(" ", "%20")

    return url


def get_link(strip_details, day=None):  # Returns the comic url
    date_formatted = ""
    middle_params = ""
    if strip_details["Main_website"] == "https://www.gocomics.com/":
        date_formatted = get_date_formatted(day=day)
        middle_params = strip_details["Web_name"]
    elif strip_details["Main_website"] == "https://comicskingdom.com/":
        date_formatted = get_date_formatted(day=day, form="-")
        middle_params = strip_details["Web_name"]
    elif strip_details["Main_website"] == "https://dilbert.com/":
        date_formatted = day.strftime("%Y-%m-%d")
        middle_params = "strip"

    return f'{strip_details["Main_website"]}{middle_params}/{date_formatted}'


def get_date_formatted(day=None, form="/"):
    if day is not None:
        return day.strftime(f"%Y{form}%m{form}%d")
    else:
        return ""


def get_random_link(strip_details):  # Returns the random comic url
    if strip_details["Main_website"] == "https://www.gocomics.com/":
        return f'{strip_details["Main_website"]}random/{strip_details["Web_name"]}', None
    else:
        first_date = datetime.strptime(get_first_date(strip_details), "%Y, %m, %d")
        random_date = randomtimestamp(start=first_date,
                                      end=datetime.today().replace(hour=0, minute=0, second=0,
                                                                   microsecond=0))
        middle_params = ""
        if strip_details["Main_website"] == "https://comicskingdom.com/":
            middle_params = strip_details["Web_name"]
        elif strip_details["Main_website"] == "https://dilbert.com/":
            middle_params = "strip"

        return f'{strip_details["Main_website"]}{middle_params}/{random_date.strftime("%Y-%m-%d")}', random_date
