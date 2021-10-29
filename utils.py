# Collection of static methods
import discord
import random
from datetime import datetime, timedelta
import json
import os
import Web_requests_manager

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

        if comic_details["sub_img_url"] != "":
            thumbnail = comic_details["sub_img_url"]
        else:
            thumbnail = ""

        img_url = comic_details["img_url"]

        # Creates the embed
        embed = discord.Embed(title=comic_title, url=url, description=alt, colour=color)

        if thumbnail != "":  # Thumbnail for Webtoons
            embed.set_thumbnail(url=thumbnail)

        if day is not None and day != "":
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


# Sends comics info in a embed
async def send_comic_info(ctx, strip_details):
    embed = discord.Embed(title=strip_details["Name"], url=strip_details["Main_website"],
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
async def parameters_interpreter(ctx, strip_details, param=None):
    if param is not None:
        """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send
            """
        param = param.lower()

        if param.find("today") != -1:
            # Sends the website of today's comic
            await comic_send(ctx, strip_details, "today")
        elif param.find("random") != -1:
            # Random comic
            await comic_send(ctx, strip_details, "random")
        elif param.find("add") != -1:
            # Add the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                new_change(ctx, strip_details, "add")
                await ctx.send(f"{strip_details['Name']} added successfully as a daily comic!")
            else:
                await ctx.send("You need `manage_guild` permission to do that!")
        elif param.find("remove") != -1:
            # Remove the comic to the daily list for a guild
            if ctx.message.author.guild_permissions.manage_guild:
                new_change(ctx, strip_details, "remove")
                await ctx.send(f"{strip_details['Name']} removed successfully from the daily list!")
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
                    if first_date <= comic_date <= datetime.utcnow():
                        await comic_send(ctx, strip_details, "Specific_date", comic_date=comic_date)
                    else:
                        first_date_formatted = datetime.strftime(first_date, "%d/%m/%Y")
                        date_now_formatted = datetime.strftime(datetime.utcnow(), "%d/%m/%Y")
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


def modify_database(ctx, use, day=None, hour=None, comic_number=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
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
                day = "D"  # Default: Daily

            if hour is None:
                hour = "6"  # Default: 6 AM UTC

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
        if use == 'remove_channel':
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


def get_today():
    return datetime.utcnow().today().strftime("%A")[2:]


def get_hour():
    return str(datetime.utcnow().hour)
