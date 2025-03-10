from __future__ import annotations

import functools
import logging
import os
from datetime import datetime
from typing import Any, Callable, Optional, Union

import discord
from discord import Embed as DiscordEmbed
from discord import app_commands
from discord.ext import commands

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.base import BaseComic, WorkingType
from bdbot.comics.comic_detail import ComicDetail
from bdbot.comics.custom import GarfieldMinusGarfield
from bdbot.discord_.multi_page_view import MultiPageView
from bdbot.discord_.response_sender import NextSend, ResponseSender
from bdbot.embed import Embed
from bdbot.files import (
    DATABASE_FILE_PATH,
    DETAILS_PATH,
    load_json,
    save_backup,
    save_json,
)
from bdbot.mention import MentionPolicy
from bdbot.time import Month, Weekday, date_to_db, get_now
from bdbot.utils import parse_all

SERVER: Optional[discord.Object] = None
OWNER: Optional[int] = None
logger = logging.getLogger("discord")


def convert_embed(embed: Embed) -> DiscordEmbed:
    d_embed = DiscordEmbed(
        title=embed.title,
        description=embed.description,
        color=embed.color,
        url=embed.url,
        timestamp=embed.timestamp,
    )
    for field in embed.fields:
        d_embed.add_field(name=field.name, value=field.value, inline=field.inline)
    if embed.thumbnail:
        d_embed.set_thumbnail(url=embed.thumbnail)
    if embed.image:
        d_embed.set_image(url=embed.image)
    d_embed.set_footer(text=embed.footer)
    return d_embed


async def send_comic_info(
    inter: discord.Interaction,
    comic: BaseComic,
    next_send: NextSend = NextSend.Normal,
):
    await send_embed(
        inter,
        [comic.get_comic_info(get_sub_status(inter, comic.position))],
        next_send=next_send,
    )


async def comic_send(
    inter: discord.Interaction,
    comic: BaseComic,
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
        # Defers the return, so Discord can wait longer
        await inter.response.defer()

    # Use comic_date!!!
    details: ComicDetail = await comic.get_comic(action)

    # Sends the comic
    await send_embed(
        inter,
        [details.to_embed()],
        NextSend.Deferred if next_send == NextSend.Normal else next_send,
    )


def parameters_interpreter(
    inter: discord.Interaction,
    comic: BaseComic,
    action: Action = None,
    date: Weekday = None,
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
    :param comic: The comic
    :param action: The action the bot need to take
    :param date: The day of the week to add / remove the comic
    :param hour: The hour to set up a comic
    :param day: Day of the month (1 to 31)
    :param month: Month of the year
    :param year: Year (1950 to now)
    :param comic_number: The comic number
    """
    match action:
        case None | Action.Info:
            # If the user didn't send any parameters, return the information the comic requested
            # await send_comic_info(inter, comic)
            return send_comic_info, {"inter": inter, "comic": comic}
        case Action.Today | Action.Random:
            # Sends the website of today's comic
            # or random comic
            # await comic_send(inter, comic, action)
            return comic_send, {"inter": inter, "comic": comic, "action": action}
        case Action.Add | Action.Remove:
            # Add or remove a comic to the daily list for a guild
            status = new_change(inter, comic, action, date=date, hour=hour)
            # await send_message(inter, status)
            return send_message, {"inter": inter, "message": status}
        case Action.Specific_date:
            # Tries to parse date / number of comic
            if comic.WORKING_TYPE == WorkingType.Date or isinstance(
                comic, GarfieldMinusGarfield
            ):
                # Works by date
                # await extract_date_comic(inter, comic, day, month, year)
                return extract_date_comic(inter, comic, day, month, year)

            # Works by number of comic
            # await extract_number_comic(
            return extract_number_comic(
                inter, comic, action, comic.WORKING_TYPE, comic_number
            )
        case _:
            # await send_message(inter, "Command not understood!")
            return send_message, {"inter": inter, "message": "Command not understood!"}


def extract_number_comic(
    inter: discord.Interaction,
    comic: BaseComic,
    action: Action,
    working_type: WorkingType,
    comic_number: int,
) -> (Callable, dict[str, Any]):
    """Extract and send a comic based on the number

    :param inter:
    :param comic:
    :param action:
    :param working_type:
    :param comic_number:
    :return:
    """
    if comic_number is not None and comic_number >= comic.first_comic_date:
        if working_type == WorkingType.Number:
            comic.main_website = comic.main_website + str(comic_number) + "/"

        return comic_send, {
            "inter": inter,
            "comic": comic,
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
    comic: BaseComic,
    day: int,
    month: Month,
    year: int,
) -> (Callable, dict[str, Any]):
    """Extract and send a comic by date

    :param inter:
    :param comic:
    :param day:
    :param month:
    :param year:
    :return:
    """
    try:
        comic_date = datetime(day=day, month=month.value, year=year)
        first_date = comic.first_comic_date
    except (ValueError, AttributeError, TypeError):
        return send_message, {
            "inter": inter,
            "message": "This is not a valid date format! Please input a day, a month and a year!",
        }

    if first_date <= comic_date <= get_now():
        return comic_send, {
            "inter": inter,
            "comic": comic,
            "action": Action.Specific_date,
            "comic_date": comic_date,
        }

    first_date_formatted = datetime.strftime(first_date, "%d/%m/%Y")
    date_now_formatted = datetime.strftime(get_now(), "%d/%m/%Y")

    return send_message, {
        "inter": inter,
        "message": f"Invalid date. Try sending a date between {first_date_formatted} and "
        f"{date_now_formatted}.",
    }


def add_all(
    inter: discord.Interaction,
    date: Optional[Weekday] = None,
    hour: Optional[int] = None,
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
    comic: BaseComic,
    param: Action,
    date: Weekday = None,
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

    comic_number = int(comic.position)

    return modify_database(
        inter,
        param,
        day=final_date,
        hour=final_hour,
        comic_number=comic_number,
        comic_name=comic.name,
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
    day: Weekday = Weekday.Daily,
    hour: int = 6,
    comic_number: int = None,
    comic_name: str = None,
) -> str:
    """
    Saves the new information in the database

    Adds or delete the guild_id, the channel id and the comic_strip data

    :param inter:
    :param action:
    :param day:
    :param hour:
    :param comic_number:
    :param comic_name:
    :return:
    """
    data = load_json(DATABASE_FILE_PATH)
    hour = str(hour)

    if action == Action.Add or action == ExtendedAction.Add_all:
        return add_comic_in_guild(
            inter, action, comic_number, data, day, hour, comic_name
        )
    if action == Action.Remove:
        return remove_comic_in_guild(inter, comic_number, data, day, hour, comic_name)
    if (
        action == ExtendedAction.Remove_guild
        or action == ExtendedAction.Auto_remove_guild
    ):
        return remove_guild_in_db(inter, action, data)
    if (
        action == ExtendedAction.Remove_channel
        or action == ExtendedAction.Auto_remove_channel
    ):
        return remove_channel_in_db(inter, action, data)

    return "Database action not understood!"


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
    if action == ExtendedAction.Remove_channel:
        channel_id = str(inter.channel.id)
    elif action == ExtendedAction.Auto_remove_channel:
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
    return (
        f"All daily comics removed successfully from channel"
        f" {inter.message.channel.mention if action == ExtendedAction.Remove_channel else ''}!"
    )


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
    if action == ExtendedAction.Remove_guild:
        guild_id = str(inter.guild.id)
    elif action == ExtendedAction.Auto_remove_guild:
        guild_id = str(inter.id)  # it is a guild
    # Remove a guild from the list
    if guild_id in data:
        data.pop(guild_id)
    else:
        return "This server is not registered for any scheduled comics!"
    # Save the database
    save_json(data)
    return (
        f"All daily comics removed successfully from guild "
        f"{inter.guild.name if action == ExtendedAction.Remove_guild else ''}!"
    )


def add_comic_in_guild(
    inter: discord.Interaction,
    action: Union[Action, ExtendedAction],
    comic_number: int,
    data: dict,
    day: Weekday,
    hour: str,
    comic_name: str,
) -> str:
    """

    :param inter:
    :param action:
    :param comic_number:
    :param data:
    :param day:
    :param hour:
    :param comic_name:
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

        if day != Weekday.Latest:
            # Checks if the day, the hour and the comic was already set for the channel
            day = date_to_db(day)

            if "date" not in d[guild_id]["channels"][channel_id]:
                d[guild_id]["channels"][channel_id].update({"date": {}})

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
        return f"{comic_name} added successfully as a daily comic!"


def add_guild_in_db(channel_id, com_list, d, day, guild_id, hour):
    # If there was no comic data stored for this guild
    # Add a comic to the list of comics
    d[guild_id]["server_id"] = int(guild_id)
    if day != Weekday.Latest:
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
    inter: discord.Interaction,
    comic_number: int,
    data: dict,
    day: Weekday,
    hour: str,
    comic_name: str,
) -> str:
    """

    :param inter:
    :param comic_number:
    :param data:
    :param day:
    :param hour:
    :param comic_name:
    :return:
    """
    guild_id = str(inter.guild.id)
    channel_id = str(inter.channel.id)
    # Remove comic
    if guild_id in data and channel_id in data[guild_id]["channels"]:
        if day != Weekday.Latest:
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
    return f"{comic_name} removed successfully from the daily list!"


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


def set_mention(inter: discord.Interaction, mention_policy: MentionPolicy) -> str:
    """

    :param inter:
    :param mention_policy:
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
            data[gid][only_daily] = mention_policy == MentionPolicy.Daily

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
            bot.get_guild(data[gid]["server_id"]), int(data[gid].get("Role", 0))
        )
        role_mention: str
        if role is not None:
            role_mention = role.name
        else:
            role_mention = data[gid].get("Role", 0)

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
    comic_name = comic_values[comic]["name"]

    # Check if channel exist
    chan = bot.get_channel(int(channel))
    if chan is not None:
        chan = chan.mention
    else:
        chan = channel

    comic_list.append({"name": comic_name, "Hour": hour, "Date": day, "Channel": chan})

    return comic_list


async def send_request_error(inter: discord.Interaction):
    """If the request is not understood

    :param inter:
    :return:
    """
    await send_message(
        inter, "Request not understood. Try '/help general' for usable commands."
    )


async def send_embed(
    inter: discord.Interaction,
    embeds: list[Embed],
    next_send: NextSend = NextSend.Normal,
):
    """Send embeds, can be of multiple pages

    :param inter: Discord interaction
    :param embeds: The list of embeds to send
    :param next_send: How to handle the next send
    """
    d_embeds: list[DiscordEmbed] = list(map(convert_embed, embeds))

    resp = await ResponseSender.from_next_send(inter, next_send)

    if len(d_embeds) == 1:
        await resp.send_message(embed=d_embeds[0])
        return
    # For more than one embed
    await resp.send_message(
        embed=d_embeds[0], view=MultiPageView(inter.user.id, d_embeds)
    )


async def send_chan_embed(channel: discord.TextChannel, embed: discord.Embed):
    """Send an embed in a channel

    :param channel: The channel object
    :param embed: The embed to send
    """

    await channel.send(embed=embed)


def get_possible_hours():
    return [app_commands.Choice(name=str(h), value=h) for h in range(0, 24)]


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
    return await bot.loop.run_in_executor(None, func, ())


async def send_message(
    inter: discord.Interaction,
    message: Optional[str] = None,
    embed: Optional[discord.Embed] = None,
    next_send: NextSend = NextSend.Normal,
    **kwargs,
):
    resp = await ResponseSender.from_next_send(inter, next_send)
    await resp.send_message(content=message, embed=embed, **kwargs)


def clean_database(
    bot: discord.Client = None,
    data: dict = None,
    do_backup: bool = True,
    strict: bool = False,
    logger_: logging.Logger = None,
) -> int:
    """Clean the database from inactive servers

    :param bot:
    :param data:
    :param do_backup:
    :param strict: Strict clean (Bypass role requirement)
    :param logger_:
    :return:
    """
    logger_.info("Running database clean...")
    # Cleans the database from inactive servers
    if data is None:
        data = load_json(DATABASE_FILE_PATH)

    if do_backup:
        save_backup(data, logger_)

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
                # Check if the channel has any latest comics scheduled
                if "latest" in channels[chan]:
                    if len(channels[chan]["latest"]) != 0:
                        to_remove = False
                        break

                # Check if the channel has any comics scheduled at a fixed hour
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

    logger_.info(f"Cleaned the database from {nb_removed} servers")
    return nb_removed


async def is_owner(inter: discord.Interaction):
    return inter.user.id == OWNER


async def send_mention(
    chan: discord.TextChannel,
    channel: str,
    comic_list: dict[str, Any],
    post_time: datetime,
):
    """

    :param chan:
    :param channel:
    :param comic_list:
    :param post_time:
    :return:
    """
    if (
        not comic_list[channel]["hasBeenMentioned"]
        and comic_list[channel]["wantMention"]
    ):
        # Checks if the channel want the original mention ('Comics for <date>, <hour> UTC @<role>')
        if comic_list[channel]["role"] is not None:
            # Checks if there is a role to mention
            role_mention = comic_list[channel]["role"].mention
        else:
            role_mention = ""

        await chan.send(
            f"Comics for "
            f"{post_time.strftime('%A %B %dth %Y, %H h UTC')}"
            f" {role_mention}"
        )
        # Sets the channel as already mentioned
        comic_list[channel]["hasBeenMentioned"] = True
