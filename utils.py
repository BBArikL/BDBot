# Collection of static methods
import discord
import random
from datetime import datetime, timedelta
import json
import os

FOOTERS_FILE_PATH = 'misc/random-footers.txt'
DATABASE_FILE_PATH = "data/data.json"


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
        day = comic_details["day"]
        month = comic_details["month"]
        year = comic_details["year"]
        url = comic_details["url"]
        color = comic_details["color"]

        if comic_details["alt"] is not None:
            alt = comic_details["alt"]
        else:
            alt = ""

        img_url = comic_details["img_url"]

        embed = discord.Embed(title=comic_title, url=url, description=alt, colour=color)

        if day is not None or day != "":
            embed.add_field(name=comic_name, value=f"Date: {day}/{month}/{year}")

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

# Make a change in the database
def new_change(ctx, strip_details, param):
    comic_number = int(strip_details["Position"])

    modify_database(ctx, param, comic_number=comic_number)

# Removes a guild from the database
def remove_guild(guild, use=None):
    if use is None:
        use = 'remove_guild'

    modify_database(guild, use)


# Removes a channel from the database
def remove_channel(ctx, use=None):
    if use is None:
        use = "remove_channel"

    modify_database(ctx, use)


def modify_database(ctx, use, day=None, hour=None, comic_number=None, channels=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    data = get_database_data()

    data = get_database_data()

    if use == 'add':
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        d = {
            guild_id: {
                "server_id": 0,
                "channels": {
                },
                "role": 0,
                "only-daily": 0,
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
            d[guild_id]["server_id"] = data[guild_id]["server_id"]
            d[guild_id]["channels"] = data[guild_id]["channels"]

            # Checks if the channel was already set
            if channel_id in data[guild_id]["channels"]:
                d[guild_id]["channels"][channel_id] = data[guild_id]["channels"][channel_id]
            else:
                d[guild_id]["channels"].update({channel_id: {"channel_id": 0, "date": {}}})

            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            # Checks if the day, the hour and the comic was already set for the channel
            if day not in d[guild_id]["channels"][channel_id]["date"]:
                d[guild_id]["channels"][channel_id]["date"].update({day: {hour: [comic_number]}})

            elif hour not in d[guild_id]["channels"][channel_id]["date"][day]:
                d[guild_id]["channels"][channel_id]["date"][day].update({hour: [comic_number]})

            elif comic_number not in d[guild_id]["channels"][channel_id]["date"][day][hour]:
                d[guild_id]["channels"][channel_id]["date"][day][hour].append(comic_number)

        else:
            # If there was no comic data stored for this guild
            # Add a comic to the list of comics
            d[guild_id]["server_id"] = int(guild_id)

            comics_number = [comic_number]

            if day is None:
                day = "D"

            if hour is None:
                hour = "6"

            d[guild_id]["channels"].update({channel_id: {"channel_id": int(channel_id),
                                                         "date": {day: {hour: comics_number}}}})
        # Update the main database
        data.update(d)

    elif use == "remove":
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

    elif use == 'remove_guild' or use == 'auto_remove_guild':
        guild_id = ""
        if use == 'remove_guild':
            guild_id = str(ctx.guild.id)
        elif use == 'auto_remove_guild':
            guild_id = str(ctx.id)

        # Remove a guild from the list
        if guild_id in data:
            data.pop(guild_id)

    elif use == 'remove_channel' or use == 'auto_remove_channel':
        guild_id = str(ctx.guild.id)
        channel_id = ""
        if use == 'remove_guild':
            channel_id = str(ctx.channel.id)
        elif use == 'auto_remove_channel':
            channel_id = str(ctx.id)

        # Remove a guild from the list
        if guild_id in data:
            if channel_id in data[guild_id]["channels"]:
                data[guild_id]["channels"].pop(channel_id)

    # Save the database
    save(data)


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


# Save the database
def save(data):
    # Saves the file
    with open(DATABASE_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)


# Check if the comic is subscribed to this guild
def get_sub_status(ctx, position, database=None):
    if database is None:  # Gets database if needed
        database = get_database_data()

    guild_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)

    if guild_id in database and channel_id in database[guild_id]["channels"]:
        # TODO CHECK ALL DATES AND HOURS
        return position in database[guild_id]["channels"][channel_id]["date"]['D']['6']
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
