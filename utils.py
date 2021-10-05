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


def modify_database(strip_details, ctx, use, comics_number=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    NB_OF_COMICS = len(strip_details)

    guild_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)

    data = get_database_data()

    if use == 'add':
        d = {
            guild_id: {
                "server_id": 0,
                "channel_id": 0,
                "ComData": ""
            }
        }

        if guild_id in data:
            # If this server was already in the database, fill out information
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

    elif use == "remove":
        # Remove comic
        if guild_id in data:
            comic_str = list(data[guild_id]["ComData"])
            if comic_str[comics_number] != "0":
                comic_str[comics_number] = "0"
                data[guild_id]["ComData"] = "".join(comic_str)

    elif use == 'remove_guild':
        # Remove a guild from the list
        if guild_id in data:
            data.pop(guild_id)

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
def get_sub_status(guild_id, position, database=None):
    if database is None:  # Gets database if needed
        database = get_database_data()

    if guild_id in database:
        return database[guild_id]["ComData"][position] == "1"
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
