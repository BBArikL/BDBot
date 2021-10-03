# Collection of static methods
import discord
import random
import datetime
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

        if day is not None:
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
    return datetime.datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")
