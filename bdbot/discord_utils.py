from __future__ import annotations

import copy
import enum
import functools
import logging
import os
from datetime import datetime, timezone
from typing import Any, Callable, Optional, Union

import discord
from discord import app_commands, ui
from discord.ext import commands

from bdbot.utils import (
    DATABASE_FILE_PATH,
    DETAILS_PATH,
    Action,
    Date,
    ExtendedAction,
    Month,
    clean_url,
    date_to_db,
    get_date,
    get_first_date,
    get_link,
    get_random_footer,
    load_json,
    parse_all,
    save_backup,
    save_json,
    strip_details,
)
from bdbot.Web_requests_manager import get_new_comic_details

SERVER: Optional[discord.Object] = None
HELP_EMBED: Optional[discord.Embed] = None
HOURLY_EMBED: Optional[discord.Embed] = None
NEW_EMBED: Optional[discord.Embed] = None
FAQ_EMBED: Optional[discord.Embed] = None
GOCOMICS_EMBED: Optional[list[discord.Embed]] = None
KINGDOM_EMBED: Optional[list[discord.Embed]] = None
WEBTOONS_EMBED: Optional[list[discord.Embed]] = None
logger = logging.getLogger("discord")


class NextSend(enum.Enum):
    Normal = 0
    Deferred = 1
    Followup = 2


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
            embed.add_field(
                name=f"{comic_name} by {author}", value=f"Date: {day}/{month}/{year}"
            )

        embed.set_image(url=img_url)

        embed.set_footer(text=get_random_footer())

        return embed
    else:
        # Error message
        embed = discord.Embed(title="No comic found!")

        embed.add_field(
            name="We could not find a comic at this date / number :thinking:....",
            value="Try another date / number!",
        )

        return embed


async def send_comic_info(
    inter: discord.Interaction,
    comic: dict[str, Union[str, int]],
    next_send: NextSend = NextSend.Normal,
):
    """Sends comics info in an embed

    :param inter:
    :param comic:
    :param next_send:
    :return:
    """
    embed: discord.Embed = discord.Embed(
        title=f'{comic["Name"]} by {comic["Author"]}',
        url=get_link(comic),
        description=comic["Description"],
        color=int(comic["Color"], 16),
    )
    embed.set_thumbnail(url=comic["Image"])
    embed.add_field(name="Working type", value=comic["Working_type"], inline=True)

    if comic["Working_type"] == "date":
        embed.add_field(
            name="First apparition", value=get_date(get_first_date(comic)), inline=True
        )

    if get_sub_status(inter, int(comic["Position"])):
        sub_stat = "Yes"
    else:
        sub_stat = "No"

    embed.add_field(name="Subscribed", value=sub_stat, inline=True)
    embed.set_footer(text="Random footer")
    embed.set_footer(text=get_random_footer())

    await send_embed(inter, [embed], next_send=next_send)


async def comic_send(
    inter: discord.Interaction,
    comic: dict,
    action: Union[Action, ExtendedAction],
    comic_date: Optional[Union[datetime, int]] = None,
    next_send: NextSend = NextSend.Normal,
):
    """Post the strip (with the given parameters)

    :param inter:
    :param comic:
    :param action:
    :param comic_date:
    :param next_send:
    :return:
    """
    if next_send == NextSend.Normal:
        await inter.response.defer()  # Defers the return, so Discord can wait longer

    comic_details = await run_blocking(
        get_new_comic_details, inter.client, comic, action, comic_date=comic_date
    )

    # Sends the comic
    await send_comic_embed(
        inter,
        comic_details,
        next_send=NextSend.Deferred if next_send == NextSend.Normal else next_send,
    )


def parameters_interpreter(
    inter: discord.Interaction,
    comic_details: dict[str, Union[str, int]],
    action: Action = None,
    date: Date = None,
    hour: int = None,
    day: int = None,
    month: Month = None,
    year: int = None,
    comic_number: int = None,
) -> (Callable, dict[str, Any]):
    """Interprets the parameters given by the user

    Actions:
        Info -> Comic information

        Today -> Today's comic

        Random -> Choose a random comic to send

        Specific_Date -> Retrieve that comic at the specific comic date

        Add -> Add the comic to the daily posting list

        Remove -> remove the comic to the daily posting list

    :param inter: The interaction
    :param comic_details: The specific comic details
    :param action: The action the bot need to take
    :param date: The day of the week to add / remove the comic
    :param hour: The hour to set up a comic
    :param day: Day of the month (1 to 31)
    :param month: Month of the year
    :param year: Year (1950 to now)
    :param comic_number: The comic number
    """
    if action is None or action == Action.Info:
        # If the user didn't send any parameters, return the information the comic requested
        # await send_comic_info(inter, comic_details)
        return send_comic_info, {"inter": inter, "comic": comic_details}
    elif action == Action.Today or action == Action.Random:
        # Sends the website of today's comic
        # or random comic
        # await comic_send(inter, comic_details, action)
        return comic_send, {"inter": inter, "comic": comic_details, "action": action}
    elif action in [Action.Add, Action.Random]:
        # Add or remove a comic to the daily list for a guild
        status = new_change(inter, comic_details, action, date=date, hour=hour)
        # await send_message(inter, status)
        return send_message, {"inter": inter, "message": status}
    elif action == Action.Specific_date:
        # Tries to parse date / number of comic
        working_type = comic_details["Working_type"]
        if (
            working_type == "date"
            or comic_details["Main_website"] == "https://garfieldminusgarfield.net/"
        ):
            # Works by date
            # await extract_date_comic(inter, comic_details, day, month, year)
            return extract_date_comic(inter, comic_details, day, month, year)
        else:
            # Works by number of comic
            # await extract_number_comic(
            return extract_number_comic(
                inter, comic_details, action, working_type, comic_number
            )
    else:
        # await send_message(inter, "Command not understood!")
        return send_message, {"inter": inter, "message": "Command not understood!"}


def extract_number_comic(
    inter: discord.Interaction,
    comic_details: dict[str, Union[str, int]],
    action: Action,
    working_type: str,
    comic_number: int,
) -> (Callable, dict[str, Any]):
    """Extract and send a comic based on the number

    :param inter:
    :param comic_details:
    :param action:
    :param working_type:
    :param comic_number:
    :return:
    """
    if comic_number is not None and comic_number >= int(get_first_date(comic_details)):
        if working_type == "number":
            comic_details_ = copy.deepcopy(comic_details)
            comic_details_["Main_website"] = (
                comic_details_["Main_website"] + str(comic_number) + "/"
            )

        return comic_send, {
            "inter": inter,
            "comic": comic_details,
            "action": action,
            "comic_date": comic_number,
        }

    return send_message, {
        "inter": inter,
        "message": "There is no comics with such values!"
        " Please input a comic number instead of a date!",
    }


def extract_date_comic(
    inter: discord.Interaction,
    comic_details: dict[str, Union[str, int]],
    day: int,
    month: Month,
    year: int,
) -> (Callable, dict[str, Any]):
    """Extract and send a comic by date

    :param inter:
    :param comic_details:
    :param day:
    :param month:
    :param year:
    :return:
    """
    try:
        comic_date = datetime(day=day, month=month.value, year=year)
        first_date = datetime.strptime(get_first_date(comic_details), "%Y, %m, %d")
    except ValueError:
        return send_message, {
            "inter": inter,
            "message": "This is not a valid date format! The format is : DD/MM/YYYY.",
        }

    if (
        first_date.timestamp()
        <= comic_date.timestamp()
        <= datetime.now(timezone.utc).timestamp()
    ):
        return comic_send, {
            "inter": inter,
            "comic": comic_details,
            "action": Action.Specific_date,
            "comic_date": comic_date,
        }
    else:
        first_date_formatted = datetime.strftime(first_date, "%d/%m/%Y")
        date_now_formatted = datetime.strftime(datetime.now(timezone.utc), "%d/%m/%Y")

        return send_message, {
            "inter": inter,
            "message": f"Invalid date. Try sending a date between {first_date_formatted} and "
            f"{date_now_formatted}.",
        }


def add_all(
    inter: discord.Interaction, date: Optional[Date] = None, hour: Optional[int] = None
):
    """Add all comics to a channel

    :param inter:
    :param date:
    :param hour:
    :return:
    """
    final_date, final_hour = parse_all(date, hour)

    return modify_database(
        inter, ExtendedAction.Add_all, day=final_date, hour=final_hour
    )


def new_change(
    inter: discord.Interaction,
    comic,
    param: Action,
    date: Date = None,
    hour: int = None,
):
    """Make a change in the database

    :param inter:
    :param comic:
    :param param:
    :param date:
    :param hour:
    :return:
    """
    if not inter.user.guild_permissions.manage_guild:
        return "You need `manage_guild` permission to do that!"

    final_date, final_hour = parse_all(date, hour)

    comic_number = int(comic["Position"])

    return modify_database(
        inter, param, day=final_date, hour=final_hour, comic_number=comic_number
    )


def remove_guild(
    inter: Union[discord.Interaction, discord.Guild],
    use: Union[Action, ExtendedAction] = ExtendedAction.Remove_guild,
):
    """Removes a guild from the database

    :param inter:
    :param use:
    :return:
    """
    return modify_database(inter, use)


def remove_channel(
    inter: Union[discord.Interaction, discord.abc.GuildChannel],
    use: Union[Action, ExtendedAction] = ExtendedAction.Remove_channel,
):
    """Removes a channel from the database

    :param inter:
    :param use:
    :return:
    """
    return modify_database(inter, use)


def modify_database(
    inter: Union[discord.Interaction, discord.abc.GuildChannel, discord.Guild],
    action: Union[Action, ExtendedAction],
    day: Date = Date.Daily,
    hour: int = 6,
    comic_number: int = None,
):
    """
    Saves the new information in the database

    Adds or delete the guild_id, the channel id and the comic_strip data

    :param inter:
    :param action:
    :param day:
    :param hour:
    :param comic_number:
    :return:
    """
    data = load_json(DATABASE_FILE_PATH)
    hour = str(hour)

    if action == Action.Add or action == ExtendedAction.Add_all:
        return add_comic_in_guild(inter, action, comic_number, data, day, hour)
    elif action == ExtendedAction.Remove_channel:
        return remove_comic_in_guild(inter, comic_number, data, day, hour)
    elif (
        action == ExtendedAction.Remove_guild
        or action == ExtendedAction.Auto_remove_guild
    ):
        return remove_guild_in_db(inter, action, data)
    elif (
        action == ExtendedAction.Remove_channel
        or action == ExtendedAction.Auto_remove_channel
    ):
        return remove_channel_in_db(inter, action, data)

    return None


def remove_channel_in_db(
    inter: discord.Interaction, action: Union[Action, ExtendedAction], data: dict
) -> str:
    """

    :param inter:
    :param action:
    :param data:
    :return:
    """
    guild_id = str(inter.guild.id)
    channel_id = ""
    if action == "remove_channel":
        channel_id = str(inter.channel.id)
    elif action == "auto_remove_channel":
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
    return "All daily comics removed successfully from this channel!"


def remove_guild_in_db(
    inter: discord.Interaction, action: Union[Action, ExtendedAction], data: dict
) -> str:
    """

    :param inter:
    :param action:
    :param data:
    :return:
    """
    guild_id = ""
    if action == "remove_guild":
        guild_id = str(inter.guild.id)
    elif action == "auto_remove_guild":
        guild_id = str(inter.id)  # it is a guild
    # Remove a guild from the list
    if guild_id in data:
        data.pop(guild_id)
    else:
        return "This server is not registered for any scheduled comics!"
    # Save the database
    save_json(data)
    return "All daily comics removed successfully!"


def add_comic_in_guild(
    inter: discord.Interaction,
    action: Union[Action, ExtendedAction],
    comic_number: int,
    data: dict,
    day: Date,
    hour: str,
) -> str:
    """

    :param inter:
    :param action:
    :param comic_number:
    :param data:
    :param day:
    :param hour:
    :return:
    """
    guild_id = str(inter.guild.id)
    channel_id = str(inter.channel.id)
    d = {guild_id: {"server_id": 0, "channels": {}, "mention": True}}

    com_list: list[int]
    if action == ExtendedAction.Add_all:
        strips = load_json(DETAILS_PATH)
        com_list = [i for i in range(len(strips))]
    else:
        com_list = [comic_number]

    if guild_id in data:
        # If this server was already in the database, fill out information
        d[guild_id] = data[guild_id]

        # Checks if the channel was already set
        if channel_id in data[guild_id]["channels"]:
            d[guild_id]["channels"][channel_id] = data[guild_id]["channels"][channel_id]
        else:
            d[guild_id]["channels"].update(
                {channel_id: {"channel_id": int(channel_id), "date": {}}}
            )

        if day != Date.Latest:
            # Checks if the day, the hour and the comic was already set for the channel
            day = date_to_db(day)

            if day not in d[guild_id]["channels"][channel_id]["date"]:
                d[guild_id]["channels"][channel_id]["date"].update(
                    {day: {hour: com_list}}
                )

            elif hour not in d[guild_id]["channels"][channel_id]["date"][day]:
                d[guild_id]["channels"][channel_id]["date"][day].update(
                    {hour: com_list}
                )

            elif (
                comic_number
                not in d[guild_id]["channels"][channel_id]["date"][day][hour]
                and len(com_list) == 1
            ):
                d[guild_id]["channels"][channel_id]["date"][day][hour].extend(com_list)

            elif len(com_list) > 1:  # Add all comics command
                d[guild_id]["channels"][channel_id]["date"][day][hour] = com_list

            else:
                return "This comic is already set at this time!"
        else:
            # Add a comic to be only latest
            if "latest" not in d[guild_id]["channels"][channel_id]:
                d[guild_id]["channels"][channel_id].update({"latest": com_list})
            elif (
                comic_number not in d[guild_id]["channels"][channel_id]["latest"]
                and len(com_list) == 1
            ):
                d[guild_id]["channels"][channel_id]["latest"].extend(com_list)
            elif len(com_list) > 1:
                d[guild_id]["channels"][channel_id]["latest"] = com_list
            else:
                return "This comic is already set at this time!"

    else:
        d = add_guild_in_db(channel_id, com_list, d, day, guild_id, hour)

    # Update the main database
    data.update(d)

    # Save the database
    save_json(data)

    if action == ExtendedAction.Add_all:
        return "All comics added successfully!"
    else:
        return f"{comic_number} added successfully as a daily comic!"


def add_guild_in_db(channel_id, com_list, d, day, guild_id, hour):
    # If there was no comic data stored for this guild
    # Add a comic to the list of comics
    d[guild_id]["server_id"] = int(guild_id)
    if day != Date.Latest:
        d[guild_id]["channels"].update(
            {
                channel_id: {
                    "channel_id": int(channel_id),
                    "date": {date_to_db(day): {hour: com_list}},
                }
            }
        )
    else:
        d[guild_id]["channels"].update(
            {channel_id: {"channel_id": int(channel_id), "latest": com_list}}
        )
    return d


def remove_comic_in_guild(
    inter: discord.Interaction, comic_number: int, data: dict, day: Date, hour: str
) -> str:
    """

    :param inter:
    :param comic_number:
    :param data:
    :param day:
    :param hour:
    :return:
    """
    guild_id = str(inter.guild.id)
    channel_id = str(inter.channel.id)
    # Remove comic
    if guild_id in data and channel_id in data[guild_id]["channels"]:
        if day != Date.Latest:
            # Verifies that the day and time was set
            day = date_to_db(day)
            if (
                day in data[guild_id]["channels"][channel_id]["date"]
                and hour in data[guild_id]["channels"][channel_id]["date"][day]
            ):
                # fmt: off
                comic_list: list[int] = data[guild_id]["channels"][channel_id]["date"][day][hour]
                # fmt: on

                # Verifies if the comic is in the list
                if comic_number in comic_list:
                    comic_list.remove(comic_number)
                    # fmt: off
                    data[guild_id]["channels"][channel_id]["date"][day][hour] = comic_list
                    # fmt: on

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

    # Save the database
    save_json(data)

    return f"{comic_number} removed successfully from the daily list!"


def set_role(inter: discord.Interaction, role: discord.Role) -> str:
    """Set a role in a guild

    :param inter:
    :param role:
    :return:
    """
    gid = str(inter.guild.id)
    role_str = "role"
    mention = "mention"
    data = load_json(DATABASE_FILE_PATH)

    if gid in data:
        if not data[gid][mention]:
            return "Please re-enable the mention before daily post by using `bd!post_mention enable`!"

        if role not in data[gid]:
            data[gid].update({role_str: role.id, "only_daily": False})
        else:
            data[gid][role_str] = role.id

        save_json(data)

        return (
            "Role successfully added to be notified! "
            "This role will get mentioned at each comic post. "
            "If you wish to be notified only for daily comics happening at 6 AM "
            "UTC, use `/set_mention daily`."
        )
    else:
        return "This server is not subscribed to any comic! Please subscribe to a comic before entering a role to add."


def set_mention(inter: discord.Interaction, choice: bool) -> str:
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
            return (
                "The base mention is disabled in this server! "
                "Re-enable the mention before daily post by using `bd!post_mention enable`."
            )

        if only_daily in data[gid]:
            data[gid][only_daily] = choice

            save_json(data)

            return "Successfully changed the mention policy for this server!"
        else:
            return (
                "This server has no role set up! Please use `bd!set_up <role>` to add a role before deciding if "
                "you want to be notified of all comic or only the daily ones."
            )
    else:
        return (
            "This server is not subscribed to any comic! Please subscribe to a comic before deciding"
            " when you want to be mentioned!"
        )


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
            return (
                "The base mention is disabled in this server! "
                "Re-enable the mention before hourly post by using `bd!post_mention enable`.",
                "",
            )
        role: discord.Role = discord.Guild.get_role(
            bot.get_guild(data[gid]["server_id"]), int(data[gid]["Role"])
        )
        role_mention: str
        if role is not None:
            role_mention = role.name
        else:
            role_mention = data[gid]["Role"]

        if only_daily in data[gid]:
            men = f"{role_mention} only for daily comics posts"
            if not data[gid][only_daily]:
                men = f"{role_mention} for all comic posts"

            return f"The bot will mention the role {men}!"
        else:
            return (
                "This server has no role set up! Please use `bd!set_role @<role>` to add a role "
                "before deciding if you want to be notified of all comic or only the daily ones.",
                "",
            )
    else:
        return (
            "This server is not subscribed to any comic! Please subscribe to a comic before "
            "deciding when you want to be mentioned!",
            "",
        )


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

            return "Role mention successfully removed!"
        else:
            return "This server is not set to mention any role!"
    else:
        return (
            "This server is not subscribed to any comic! Please subscribe to a comic before managing the role "
            "mentions!"
        )


def set_post_mention(inter: discord.Interaction, choice: bool):
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
            return (
                "A role is already set up to be mentioned daily! Remove the role before changing the post mention"
                " by using `bd!remove_role`."
            )

        save_json(data)

        return "Successfully changed the mention policy for this server! "
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


def add_comic_to_list(
    comic_values: list[dict],
    comic: int,
    bot: commands.Bot,
    channel: str,
    comic_list: list[dict],
    hour: str = "",
    day: str = "La",
) -> list[dict]:
    comic_name = comic_values[comic]["Name"]

    # Check if channel exist
    chan = bot.get_channel(int(channel))
    if chan is not None:
        chan = chan.mention
    else:
        chan = channel

    comic_list.append({"Name": comic_name, "Hour": hour, "Date": day, "Channel": chan})

    return comic_list


async def send_comic_embed(
    inter: discord.Interaction,
    comic_details: dict[str, Union[str, int]],
    next_send: NextSend = NextSend.Deferred,
):
    """Send a comic embed

    :param inter:
    :param comic_details:
    :param next_send:
    :return:
    """
    embed = create_embed(comic_details=comic_details)  # Creates the embed

    await send_embed(inter, [embed], next_send)  # Send the comic


async def send_request_error(inter: discord.Interaction):
    """If the request is not understood

    :param inter:
    :return:
    """
    await send_message(
        inter, "Request not understood. Try '/help general' for usable commands."
    )


def website_specific_embed(
    website_name: str, website: str, nb_per_embed=5
) -> list[discord.Embed]:
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

            embed.add_field(name=strips[strip]["Name"], value=strips[strip]["Helptxt"])
            if i == nb_per_embed:
                i = 0
                # Reset the embed to create a new one
                embed = discord.Embed(title=f"{website_name}!")
                embeds.append(embed)

    return embeds


class ResponseSender:
    """Class to account for some response types"""

    def __init__(
        self,
        resp: [
            discord.InteractionResponse,
            discord.InteractionMessage,
            discord.Webhook,
        ],
    ):
        self.resp = resp

    @classmethod
    async def from_next_send(
        cls, inter: discord.Interaction, next_send: NextSend
    ) -> ResponseSender:
        if next_send == NextSend.Normal:
            return cls(inter.response)
        elif next_send == NextSend.Deferred:
            return cls(await inter.original_response())
        else:
            return cls(inter.followup)

    async def send_message(self, *args, **kwargs):
        if isinstance(self.resp, discord.InteractionMessage):
            await self.resp.edit(*args, **kwargs)
        elif isinstance(self.resp, discord.InteractionResponse):
            await self.resp.send_message(*args, **kwargs)
        elif isinstance(self.resp, discord.Webhook):
            await self.resp.send(*args, **kwargs)


async def send_embed(
    inter: discord.Interaction,
    embeds: list[discord.Embed],
    next_send: NextSend = NextSend.Normal,
):
    """Send embeds, can be of multiple pages

    :param inter: Discord interaction
    :param embeds: The list of embeds to send
    :param next_send: How to handle the next send
    """
    for embed in embeds:
        embed.set_footer(text=get_random_footer())

    resp = await ResponseSender.from_next_send(inter, next_send)

    if len(embeds) == 1:
        await resp.send_message(embed=embeds[0])
    else:
        # For more than one embed
        multi_page_view = MultiPageView(inter.user.id, embeds)

        await resp.send_message(embed=embeds[0], view=multi_page_view)


async def send_chan_embed(channel: discord.TextChannel, embed: discord.Embed):
    """Send an embed in a channel

    :param channel: The channel object
    :param embed: The embed to send
    """
    embed.set_footer(text=get_random_footer())

    await channel.send(embed=embed)


def get_possible_hours():
    return [app_commands.Choice(name=str(h), value=h) for h in range(1, 25)]


def get_possible_days():
    return [app_commands.Choice(name=str(d), value=d) for d in range(1, 32)]


def get_possible_years():
    return [
        app_commands.Choice(name=str(d), value=d)
        for d in range(1950, datetime.now().year + 1)
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
        manage_messages=True,
    )

    return discord.utils.oauth_url(
        os.getenv("CLIENT_ID"),
        permissions=perms,
        scopes=("bot", "applications.commands"),
    )


async def update_presence(bot: discord.Client):
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"slash commands and '/help general' in"
            f" {len(bot.guilds)} servers!",
        ),
    )


async def run_blocking(
    blocking_func: Callable, bot: discord.Client, *args, **kwargs
) -> Optional[dict[str, Union[str, int, bool]]]:
    """Run a blocking function as a non-blocking one

    From https://stackoverflow.com/q/65881761

    :param blocking_func:
    :param bot:
    :param args:
    :param kwargs:
    :return:
    """
    func = functools.partial(blocking_func, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)


class MultiPageView(ui.View):
    def __init__(self, author: int, embeds: list[discord.Embed], timeout: float = 60):
        super().__init__(timeout=timeout)
        self.author_id = author
        self.embeds = embeds
        self.current_embed = 0

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return interaction.user.id == self.author_id

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
        /,
    ) -> None:
        await interaction.followup.send(content=error)

    @discord.ui.button(label="Last")
    async def last_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button  # noqa
    ):
        if self.current_embed > 0:
            self.current_embed -= 1

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    @discord.ui.button(label="Next")
    async def next_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button  # noqa
    ):
        if self.current_embed < len(self.embeds) - 1:
            self.current_embed += 1

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger)
    async def exit_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.next_embed.disabled = True
        self.last_embed.disabled = True
        button.disabled = True

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    async def on_timeout(self) -> None:
        self.clear_items()
        self.embeds = None
        self.author_id = 0
        self.current_embed = 0


async def send_message(
    inter: discord.Interaction,
    message: Optional[str] = None,
    embed: Optional[discord.Embed] = None,
    next_send: NextSend = NextSend.Normal,
):
    resp = await ResponseSender.from_next_send(inter, next_send)
    await resp.send_message(content=message, embed=embed)


def clean_database(
    bot: discord.Client = None,
    data: dict = None,
    do_backup: bool = True,
    strict: bool = False,
    logger: logging.Logger = None,
) -> int:
    """Clean the database from inactive servers

    :param bot:
    :param data:
    :param do_backup:
    :param strict: Strict clean (Bypass role requirement)
    :param logger:
    :return:
    """
    logger.info("Running database clean...")
    # Cleans the database from inactive servers
    if data is None:
        data = load_json(DATABASE_FILE_PATH)

    if do_backup:
        save_backup(data, logger)

    guilds_to_clean = []
    nb_removed = 0

    for guild in data:
        # To take in account or not if a server still has a role tied to their info
        to_remove = False

        if bot is not None and bot.get_guild(guild) is None:
            # If it cannot find the server, bypass all others checks
            to_remove = True

        if ("role" not in data[guild] or strict) and not to_remove:
            # The server is available so lets check for other info that might indicate that the server is inactive
            to_remove = True
            channels = data[guild]["channels"]
            for chan in channels:
                if "latest" in channels[chan]:
                    if len(channels[chan]["latest"]) != 0:
                        to_remove = False
                        break

                if "date" in channels[chan]:
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

    # Removes the servers that need to be removed
    for guild in guilds_to_clean:
        if guild in data:
            data.pop(guild)

    if nb_removed > 0:
        save_json(data)

    logger.info(f"Cleaned the database from {nb_removed} servers")
    return nb_removed
