import asyncio
import os
import functools

import discord
import logging

from datetime import datetime, timezone
from discord import app_commands, ui
from discord.ext import commands
from typing import Optional, Union, Callable, Any
from src.utils import (clean_url, get_random_footer, get_link, get_date,
                       get_first_date, parse_all, save_json, load_json,
                       Success, strip_details, DATABASE_FILE_PATH, DETAILS_PATH)
from src.Web_requests_manager import get_new_comic_details

SERVER: Optional[discord.Object] = None
HELP_EMBED: Optional[discord.Embed] = None
HOURLY_EMBED: Optional[discord.Embed] = None
NEW_EMBED: Optional[discord.Embed] = None
FAQ_EMBED: Optional[discord.Embed] = None
GOCOMICS_EMBED: Optional[list[discord.Embed]] = None
KINGDOM_EMBED: Optional[list[discord.Embed]] = None
WEBTOONS_EMBED: Optional[list[discord.Embed]] = None
logger = logging.getLogger('discord')


def create_embed(comic_details: Optional[dict] = None):
    """Create a comic embed with the given details

    :param comic_details:
    :return:
    """
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

        return embed


async def send_comic_info(inter: discord.Interaction, comic: dict):
    """Sends comics info in an embed

    :param inter:
    :param comic:
    :return:
    """
    embed: discord.Embed = discord.Embed(title=f'{comic["Name"]} by {comic["Author"]}',
                                         url=get_link(comic),
                                         description=comic["Description"], color=int(comic["Color"], 16))
    embed.set_thumbnail(url=comic["Image"])
    embed.add_field(name="Working type", value=comic["Working_type"], inline=True)

    if comic["Working_type"] == "date":
        embed.add_field(name="First apparition", value=get_date(get_first_date(comic)), inline=True)

    if get_sub_status(inter, int(comic["Position"])):
        sub_stat = "Yes"
    else:
        sub_stat = "No"

    embed.add_field(name="Subscribed", value=sub_stat, inline=True)
    embed.set_footer(text="Random footer")
    embed.set_footer(text=get_random_footer())

    await send_embed(inter, [embed])


async def comic_send(inter: discord.Interaction, comic: dict, param: str, comic_date: Optional[Union[datetime, int]] = None):
    """Post the strip (with the given parameters)

    :param inter:
    :param comic:
    :param param:
    :param comic_date:
    :return:
    """
    await inter.defer()  # Defers the return, so Discord cna wait longer
    comic_details = await run_blocking(get_new_comic_details, inter.bot, comic, param, comic_date=comic_date)

    # Sends the comic
    await send_comic_embed(inter, comic_details)


async def parameters_interpreter(inter: discord.Interaction, comic_details, param=None, date=None, hour=None):
    """Interprets the parameters given by the user

    :param inter:
    :param comic_details:
    :param param:
    :param date:
    :param hour:
    :return:
    """
    if param is not None and param != "Info":
        """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send
            """
        param = param.lower()

        if param == "today" or param == "tod":
            # Sends the website of today's comic
            await comic_send(inter, comic_details, "today")
        elif param == "random" or param == "rand" or param == "rnd":
            # Random comic
            await comic_send(inter, comic_details, "random")
        elif param == "add":
            # Add the comic to the daily list for a guild
            if inter.message.author.guild_permissions.manage_guild:
                status = new_change(inter, comic_details, "add", date=date, hour=hour)
                if status == Success:
                    await send_message(inter, f"{comic_details['Name']} added successfully as a daily comic!", first=False)
                else:
                    await send_message(inter, status)
            else:
                await send_message(inter, "You need `manage_guild` permission to do that!")
        elif param == "remove":
            # Remove the comic to the daily list for a guild
            if inter.message.author.guild_permissions.manage_guild:
                status = new_change(inter, comic_details, "remove", date=date, hour=hour)
                if status == Success:
                    await send_message(inter,
                        f"{comic_details['Name']} removed successfully from the daily list!")
                else:
                    await send_message(inter, status)
            else:
                await send_message(inter, "You need `manage_guild` permission to do that!")
        else:
            # Tries to parse date / number of comic
            working_type = comic_details["Working_type"]
            if working_type == "date" or comic_details["Main_website"] == 'https://garfieldminusgarfield.net/':
                # Works by date
                try:
                    comic_date = datetime.strptime(param, "%d/%m/%Y")
                    first_date = datetime.strptime(get_first_date(comic_details), "%Y, %m, %d")
                    if first_date.timestamp() <= comic_date.timestamp() <= datetime.now(timezone.utc).timestamp():
                        await comic_send(inter, comic_details, "Specific_date", comic_date=comic_date)
                    else:
                        first_date_formatted = datetime.strftime(first_date, "%d/%m/%Y")
                        date_now_formatted = datetime.strftime(datetime.now(timezone.utc), "%d/%m/%Y")
                        await send_message(inter,
                            f"Invalid date. Try sending a date between {first_date_formatted} and "
                            f"{date_now_formatted}.")
                except ValueError:
                    await send_message(inter, "This is not a valid date format! The format is : DD/MM/YYYY.")
            else:
                # Works by number of comic
                try:
                    number = int(param.split(" ")[0])
                    if number >= int(get_first_date(comic_details)):
                        if working_type == "number":
                            comic_details["Main_website"] = comic_details["Main_website"] + str(number) + '/'
                            await comic_send(inter, comic_details, param=param)
                        else:
                            await comic_send(inter, comic_details, "Specific_date", comic_date=number)
                    else:
                        await send_message(inter, "There is no comics with such values!")

                except ValueError:
                    await send_message(inter, 'This is not a valid comic number!')
    else:
        # If the user didn't send any parameters, return the information the comic requested
        await send_comic_info(inter, comic_details)


def add_all(inter: discord.Interaction, date: Optional[str] = None, hour: Optional[str] = None):
    """Add all comics to a channel

    :param inter:
    :param date:
    :param hour:
    :return:
    """
    final_date, final_hour = parse_all(date, hour)

    return modify_database(inter, "add_all", day=final_date, hour=str(final_hour))


def new_change(inter: discord.Interaction, comic, param, date=None, hour=None):
    """Make a change in the database

    :param inter:
    :param comic:
    :param param:
    :param date:
    :param hour:
    :return:
    """
    final_date, final_hour = parse_all(date, hour)

    comic_number = int(comic["Position"])

    return modify_database(inter, param, day=final_date, hour=str(final_hour), comic_number=comic_number)


def remove_guild(inter: Union[discord.Interaction, discord.Guild], use: str = 'remove_guild'):
    """Removes a guild from the database

    :param inter:
    :param use:
    :return:
    """
    return modify_database(inter, use)


def remove_channel(inter: Union[discord.Interaction, discord.abc.GuildChannel], use="remove_channel"):
    """Removes a channel from the database

    :param inter:
    :param use:
    :return:
    """
    return modify_database(inter, use)


def modify_database(inter: Union[discord.Interaction, discord.abc.GuildChannel, discord.Guild], use: str, day: str = None,
                    hour: str = None, comic_number: int = None):
    """
    Saves the new information in the database

    Adds or delete the guild_id, the channel id and the comic_strip data

    :param inter:
    :param use:
    :param day:
    :param hour:
    :param comic_number:
    :return:
    """
    add = "add"
    a_all = "add_all"
    remove_c = "remove"
    remove_g = "remove_guild"
    fremove_g = "auto_remove_guild"
    remove_chan = "remove_channel"
    fremove_chan = "auto_remove_guild"
    data = load_json(DATABASE_FILE_PATH)

    if use == add or use == a_all:
        guild_id = str(inter.guild.id)
        channel_id = str(inter.channel.id)
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
                    d[guild_id]["channels"][channel_id]["date"][day][hour].extend(com_list)

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
        guild_id = str(inter.guild.id)
        channel_id = str(inter.channel.id)
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
            return "This server or channel is not registered for scheduled comics!"

    elif use == remove_g or use == fremove_g:
        guild_id = ""
        if use == 'remove_guild':
            guild_id = str(inter.guild.id)
        elif use == 'auto_remove_guild':
            guild_id = str(inter.id)  # it is a guild

        # Remove a guild from the list
        if guild_id in data:
            data.pop(guild_id)
        else:
            return "This server is not registered for any scheduled comics!"

    elif use == remove_chan or use == fremove_chan:
        guild_id = str(inter.guild.id)
        channel_id = ""
        if use == 'remove_channel':
            channel_id = str(inter.channel.id)
        elif use == 'auto_remove_channel':
            channel_id = str(inter.id)  # it is a channel

        # Remove a guild from the list
        if guild_id in data:
            if channel_id in data[guild_id]["channels"]:
                data[guild_id]["channels"].pop(channel_id)
            else:
                return "This channel is not registered for any scheduled comics!"
        else:
            return "This server is not registered for any scheduled comics!"

    # Save the database
    save_json(data)

    return Success


def set_role(inter: discord.Interaction, role_id) -> str:
    """

    :param inter:
    :param role_id:
    :return:
    """
    gid = str(inter.guild.id)
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
        return "This server is not subscribed to any comic! Please subscribe to a comic before entering a role to add."


def set_mention(inter: discord.Interaction, choice) -> str:
    """

    :param inter:
    :param choice:
    :return:
    """
    gid = str(inter.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "The base mention is disabled in this server! " \
                   "Re-enable the mention before daily post by using `bd!post_mention enable`."

        if only_daily in data[gid]:
            data[gid][only_daily] = choice

            save_json(data)

            return Success
        else:
            return "This server has no role set up! Please use `bd!set_up <role>` to add a role before deciding if " \
                   "you want to be notified of all comic or only the daily ones."
    else:
        return "This server is not subscribed to any comic! Please subscribe to a comic before deciding" \
               " when you want to be mentioned!"


def get_mention(inter: discord.Interaction, bot: commands.Bot) -> (str, str):
    """

    :param inter:
    :param bot:
    :return:
    """
    gid = str(inter.guild.id)
    only_daily = "only_daily"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "The base mention is disabled in this server! " \
                   "Re-enable the mention before hourly post by using `bd!post_mention enable`.", ""
        role: discord.Role = discord.Guild.get_role(bot.get_guild(data[gid]["server_id"]), int(data[gid]["Role"]))
        role_mention: str
        if role is not None:
            role_mention = role.name
        else:
            role_mention = data[gid]["Role"]

        if only_daily in data[gid]:
            men = f"{role_mention} only for daily comics posts"
            if not data[gid][only_daily]:
                men = f"{role_mention} for all comic posts"

            return Success, men
        else:
            return "This server has no role set up! Please use `bd!set_role @<role>` to add a role " \
                   "before deciding if you want to be notified of all comic or only the daily ones.", ""
    else:
        return "This server is not subscribed to any comic! Please subscribe to a comic before " \
               "deciding when you want to be mentioned!", ""


def remove_role(inter):
    """

    :param inter:
    :return:
    """
    gid = str(inter.guild.id)
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
            return "This server is not set to mention any role!"
    else:
        return "This server is not subscribed to any comic! Please subscribe to a comic before managing the role " \
               "mentions!"


def set_post_mention(inter, choice):
    """Change if the bot says a phrase before posting daily comics

    :param inter:
    :param choice:
    :return:
    """
    gid = str(inter.guild.id)
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


def get_specific_guild_data(inter: discord.Interaction) -> Optional[dict]:
    """Returns a specific guild's data"""
    database = load_json(DATABASE_FILE_PATH)
    guild_id = str(inter.guild.id)

    if guild_id in database:
        return database[guild_id]
    else:
        return None


def get_sub_status(inter, position: int, database: Optional[dict] = None):
    """Check if the comic is subscribed to this guild

    :param inter:
    :param position:
    :param database:
    :return:
    """
    if database is None:  # Gets database if needed
        database = load_json(DATABASE_FILE_PATH)

    guild_id = str(inter.guild.id)

    if guild_id in database:
        guild_data = database[guild_id]
        for channel in guild_data["channels"]:

            if "latest" in guild_data["channels"][channel]:
                if position in guild_data["channels"][channel]["latest"]:
                    return True

            for day in guild_data["channels"][channel]["date"]:
                for hour in guild_data["channels"][channel]["date"][day]:
                    if position in guild_data["channels"][channel]["date"][day][hour]:
                        return True
        return False
    else:
        return False


def add_comic_to_list(comic_values: list[dict], comic: int, bot: commands.Bot, channel: str, comic_list: list[dict],
                      hour: str = "", day: str = "La") -> list[dict]:
    comic_name = comic_values[comic]["Name"]

    # Check if channel exist
    chan = bot.get_channel(int(channel))
    if chan is not None:
        chan = chan.mention
    else:
        chan = channel

    comic_list.append({
        "Name": comic_name,
        "Hour": hour,
        "Date": day,
        "Channel": chan
    })

    return comic_list


async def send_comic_embed(inter: discord.Interaction, comic_details: dict):
    """Send a comic embed

    :param inter:
    :param comic_details:
    :return:
    """
    embed = create_embed(comic_details=comic_details)  # Creates the embed

    await send_embed(inter, [embed])  # Send the comic


async def send_request_error(inter: discord.Interaction):
    """If the request is not understood

    :param inter:
    :return:
    """
    await send_message(inter, "Request not understood. Try '/help general' for usable commands.")


def website_specific_embed(website_name: str, website: str, nb_per_embed=5) -> list[discord.Embed]:
    """Create embeds with all the specific comics from a website

    :param nb_per_embed:
    :param website_name:
    :param website:
    :return: The list of embeds
    """
    strips = strip_details
    i = 0
    embeds: list[discord.Embed] = []

    embed = discord.Embed(title=f"{website_name}!")
    embeds.append(embed)
    for strip in strips:
        if strips[strip]["Main_website"] == website:
            i += 1

            embed.add_field(name=strips[strip]['Name'], value=strips[strip]['Helptxt'])
            if i == nb_per_embed:
                i = 0
                # Reset the embed to create a new one
                embed = discord.Embed(title=f"{website_name}!")
                embeds.append(embed)

    return embeds


async def send_embed(inter: discord.Interaction, embeds: list[discord.Embed]):
    """Send embeds, can be of multiple pages

    From https://stackoverflow.com/questions/61787520/i-want-to-make-a-multi-page-help-command-using-discord-py

    :param inter: Discord interaction
    :param embeds: The list of embeds to send
    """
    pages = len(embeds)
    current = 1

    for embed in embeds:
        embed.set_footer(text=get_random_footer())

    response: discord.InteractionResponse = inter.response

    if pages == 1:
        await response.send_message(embed=embeds[current - 1])
    else:
        # For more than one embed
        multi_page_view = MultiPageView(inter.message.author.id)
        multi_page_view.add_item(ui.Button(label="Last"))
        multi_page_view.add_item(ui.Button(label="Next"))
        multi_page_view.add_item(ui.Button(style=discord.ButtonStyle.danger, label="Exit"))

        await response.send_message(embed=embeds[current - 1], view=multi_page_view)

        """

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this example

                if str(reaction.emoji) == btn_right and current != pages:
                    current += 1
                    await msg.edit(embed=embeds[current - 1])
                    await msg.remove_reaction(reaction, user)

                elif str(reaction.emoji) == btn_left and current > 1:
                    current -= 1
                    await msg.edit(embed=embeds[current - 1])
                    await msg.remove_reaction(reaction, user)

                elif str(reaction.emoji) == btn_cancel:
                    await msg.remove_reaction(reaction, user)
                    await msg.delete()
                    break
                else:
                    await msg.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                if remove_after:
                    await msg.delete()
                else:
                    for button in buttons:
                        await msg.remove_reaction(button, bot.user)
                break
                # ending the loop if user doesn't react after x seconds"""


async def comic_action_autocomplete(
        interaction: discord.Interaction,
        current: str,
):
    actions = ['Today', 'Random', 'Info', 'add', 'remove']
    return [
        app_commands.Choice(name=action, value=action)
        for action in actions if current.lower() in action.lower()
    ]


async def comic_date_autocomplete(
        interaction: discord.Interaction,
        current: str,
):
    days = ['Daily', 'Latest', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return [
        app_commands.Choice(name=day, value=day)
        for day in days if current.lower() in day.lower()
    ]


async def comic_hour_autocomplete(
        interaction: discord.Interaction,
        current: str,
):
    hours = [str(h) for h in range(1, 24)]
    return [
        app_commands.Choice(name=hour, value=hour)
        for hour in hours if current.lower() in hour.lower()
    ]


def get_url() -> str:
    perms = discord.Permissions()
    perms.update(
        read_messages=True,
        read_messages_history=True,
        send_messages=True,
        send_messages_in_threads=True,
        embed_links=True,
        attach_files=True,
        mention_everyone=True,
        add_reactions=True,
        use_application_commands=True,
        manage_messages=True
    )

    return discord.utils.oauth_url(
        os.getenv('CLIENT_ID'),
        permissions=perms,
        scopes=('bot', 'applications.commands')
    )


async def update_presence(bot: commands.Bot):
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f'slash commands and \'/help general\' in'
                 f' {len(bot.guilds)} servers!'
        )
    )


async def run_blocking(blocking_func: Callable, bot: commands.Bot, *args, **kwargs) -> \
        Optional[dict[str, Union[str, int, bool]]]:
    """Run a blocking function as a non-blocking one

    From https://stackoverflow.com/questions/65881761/discord-gateway-warning-shard-id-none-heartbeat-blocked-for-more-than-10-second

    :param blocking_func:
    :param bot:
    :param args:
    :param kwargs:
    :return:
    """
    func = functools.partial(blocking_func, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)


class MultiPageView(ui.View):

    def __init__(self, author: int, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.author_id = author

    def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return interaction.message.author.id == self.author_id


class MultiPageButton(ui.Button):

    def callback(self, interaction: discord.Interaction) -> Any:
        interaction.followup.send_message(f"You clicked on button {self.label}")


async def send_message(inter: discord.Interaction, message: Optional[str] = None, embed: Optional[discord.Embed]= None, first: bool = True):
    if first:
        await inter.response.send_message(message=message, embed=embed)
    else:
        await inter.followup.send_message(message=message, embed=embed)
