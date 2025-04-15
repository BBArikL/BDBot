from __future__ import annotations

import functools
import logging
import os
import random
from datetime import datetime
from typing import Any, Callable, Optional, Union

import discord
from discord import Client
from discord import Embed as DiscordEmbed
from discord import app_commands
from discord.ext import commands

from bdbot.actions import Action, ExtendedAction
from bdbot.cache import link_cache
from bdbot.comics.base import BaseComic, WorkingType
from bdbot.comics.comic_detail import ComicDetail
from bdbot.comics.custom import GarfieldMinusGarfield
from bdbot.db import ChannelSubscription, DiscordSubscription, ServerSubscription
from bdbot.discord_.multi_page_view import MultiPageView
from bdbot.discord_.response_sender import NextSend, ResponseSender
from bdbot.embed import Embed
from bdbot.exceptions import ComicNotFound
from bdbot.mention import MentionPolicy
from bdbot.subscription_type import SubscriptionType
from bdbot.time import Month, Weekday, get_now
from bdbot.utils import all_comics, parse_all

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
        [comic.get_comic_info(await get_sub_status(inter, comic.id))],
        next_send=next_send,
    )


async def comic_send(
    inter: discord.Interaction,
    comic: BaseComic,
    action: Union[Action, ExtendedAction],
    comic_date: datetime | int | None = None,
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

    try:
        details = (await comic.get_comic(action, comic_date=comic_date)).to_embed()
    except ComicNotFound:
        details = ComicDetail.comic_not_found(comic.name)

    # Sends the comic
    await send_embed(
        inter,
        [details],
        NextSend.Deferred if next_send == NextSend.Normal else next_send,
    )


async def parameters_interpreter(
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
            status = await new_change(inter, comic, action, date=date, hour=hour)
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

    if first_date <= comic_date <= datetime.today():
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


async def add_all(
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

    return await modify_database(
        inter, ExtendedAction.Add_all, day=final_date, hour=final_hour
    )


async def new_change(
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
    return await modify_database(
        inter,
        param,
        day=final_date,
        hour=final_hour,
        comic_number=comic.id,
        comic_name=comic.name,
    )


async def modify_database(
    inter: Union[discord.Interaction, discord.abc.GuildChannel, discord.Guild],
    action: Union[Action, ExtendedAction],
    day: Weekday = Weekday.Daily,
    hour: int = 6,
    comic_number: int = None,
    comic_name: str = None,
) -> str:
    """
    Saves the new information in the database

    :param inter:
    :param action:
    :param day:
    :param hour:
    :param comic_number:
    :param comic_name:
    :return:
    """
    hour = str(hour)
    if action in [Action.Add, ExtendedAction.Add_all, ExtendedAction.Add_random]:
        return await add_comic_in_guild(
            inter, action, comic_number, day, hour, comic_name
        )
    if action in [Action.Remove, ExtendedAction.Remove_random]:
        return await remove_comic_in_guild(inter, action, comic_number, day, hour)
    if action in [ExtendedAction.Remove_guild, ExtendedAction.Auto_remove_guild]:
        return await remove_guild_in_db(inter, action)
    if action in [ExtendedAction.Remove_channel, ExtendedAction.Auto_remove_channel]:
        return await remove_channel_in_db(inter, action)
    return "Database action not understood!"


async def remove_channel_in_db(
    inter: discord.Interaction, action: Union[Action, ExtendedAction]
) -> str:
    """

    :param inter:
    :param action:
    :return:
    """
    guild_id = str(inter.guild.id)
    channel = None
    if action == ExtendedAction.Remove_channel:
        channel = inter.channel
    elif action == ExtendedAction.Auto_remove_channel:
        channel = inter  # it is a channel
    # Remove a guild from the list
    channel_id = channel.id

    channel_sub = await ChannelSubscription.filter(id=channel_id).get_or_none()
    if not channel_sub:
        return "This channel is not registered for any scheduled comics!"

    await DiscordSubscription.filter(channel=channel_sub).delete()
    await ChannelSubscription.filter(id=channel_id).delete()
    server = (
        await ServerSubscription.filter(id=guild_id)
        .prefetch_related("channels")
        .get_or_none()
    )

    if server and len(server.channels) == 0:
        await server.delete()

    return (
        f"All daily comics removed successfully from channel"
        f" {channel.mention if action == ExtendedAction.Remove_channel else ''}!"
    )


async def remove_guild_in_db(
    inter: discord.Interaction, action: Union[Action, ExtendedAction]
) -> str:
    """

    :param inter:
    :param action:
    :return:
    """
    guild_id = 0
    if action == ExtendedAction.Remove_guild:
        guild_id = inter.guild.id
    elif action == ExtendedAction.Auto_remove_guild:
        guild_id = inter.id  # it is a guild

    server = await ServerSubscription.filter(id=guild_id).get_or_none()

    if not server:
        return "This server is not registered for any scheduled comics!"

    for channel in await server.channels:
        for sub in await channel.subscriptions:
            await sub.delete()
        await channel.delete()
    await server.delete()

    return (
        f"All daily comics removed successfully from guild "
        f"{inter.guild.name if action == ExtendedAction.Remove_guild else ''}!"
    )


async def add_comic_in_guild(
    inter: discord.Interaction,
    action: Union[Action, ExtendedAction],
    comic: int,
    day: Weekday,
    hour: str,
    comic_name: str,
) -> str:
    """

    :param inter:
    :param action:
    :param comic:
    :param day:
    :param hour:
    :param comic_name:
    :return:
    """
    guild_id = inter.guild.id
    channel_id = inter.channel.id
    subscription_type = SubscriptionType.Normal

    if action == ExtendedAction.Add_random:
        subscription_type = SubscriptionType.Random
        comic = -1

    comics: dict[str, BaseComic] = all_comics()
    comics: list[int] = (
        [comic.id for comic in comics.values()]
        if action == ExtendedAction.Add_all
        else [comic]
    )
    server = (
        await ServerSubscription.filter(id=guild_id)
        .prefetch_related("channels")
        .get_or_none()
    )

    if not server:
        server = ServerSubscription(
            id=guild_id,
            mention_policy=MentionPolicy.All,
            role_id=None,
        )
        await server.save()

    channel = (
        await ChannelSubscription.filter(id=channel_id)
        .prefetch_related("subscriptions")
        .get_or_none()
    )

    if not channel:
        channel = ChannelSubscription(
            id=channel_id,
            server_id=guild_id,
        )
        await channel.save()

    for comic in comics:
        if await DiscordSubscription.filter(
            comic_id=comic,
            channel=channel,
            subscription_type=SubscriptionType.Normal,
            weekday=day,
            hour=hour,
        ).exists():
            continue
        subscription = DiscordSubscription(
            comic_id=comic,
            subscription_type=subscription_type,
            weekday=day,
            hour=hour,
            channel_id=channel.id,
        )
        await subscription.save()

    if action == ExtendedAction.Add_all:
        return "All comics added successfully!"
    if action == ExtendedAction.Add_random:
        return "Random comic added successfully!"
    return f"{comic_name} added successfully!"


async def remove_comic_in_guild(
    inter: discord.Interaction,
    action: Union[Action, ExtendedAction],
    comic: int,
    day: Weekday,
    hour: str,
) -> str:
    """

    :param inter:
    :param action:
    :param comic:
    :param day:
    :param hour:
    :return:
    """
    guild_id = inter.guild.id
    channel_id = inter.channel.id

    subscription_type = SubscriptionType.Normal
    if action == ExtendedAction.Remove_random:
        subscription_type = SubscriptionType.Random
        comic = -1

    server = (
        await ServerSubscription.filter(id=guild_id)
        .prefetch_related("channels")
        .get_or_none()
    )

    if not server:
        return "This server is not registered for any scheduled comics!"

    channel = (
        await ChannelSubscription.filter(id=channel_id)
        .prefetch_related("subscriptions")
        .get_or_none()
    )

    if not channel:
        return "This channel is not registered for any scheduled comics!"

    query = DiscordSubscription.filter(
        comic_id=comic,
        channel=channel,
        subscription_type=subscription_type,
        weekday=day,
        hour=hour,
    )
    if not await query.exists():
        return "This comic is not registered for a scheduled comic at that time!"

    await query.delete()

    if await channel.subscriptions.all().count() == 0:
        await channel.delete()

    if await server.channels.all().count() == 0:
        await server.delete()

    return "The comic was removed successfully!"


async def set_role(inter: discord.Interaction, role: discord.Role) -> str:
    """Set a role in a guild

    :param inter:
    :param role:
    :return:
    """
    server = (
        await ServerSubscription.filter(id=inter.guild.id)
        .prefetch_related("channels")
        .get_or_none()
    )
    if not server:
        return "This server is not registered for any scheduled comic!"
    if server.role_id is None:
        server.mention_policy = MentionPolicy.All
    server.role_id = role.id
    await server.save()
    return (
        "Role successfully added to be notified! "
        "This role will get mentioned at each comic post. "
        "If you wish to be notified only for daily comics happening at 6 AM "
        "UTC, use `/set_mention daily`."
    )


async def set_mention(inter: discord.Interaction, mention_policy: MentionPolicy) -> str:
    """

    :param inter:
    :param mention_policy:
    :return:
    """
    server = (
        await ServerSubscription.filter(id=inter.guild.id)
        .prefetch_related("channels")
        .get_or_none()
    )
    if not server:
        return "This server is not registered for any scheduled comic!"
    server.mention_policy = mention_policy
    await server.save()
    return "Mention set successfully!"


async def get_mention(inter: discord.Interaction, bot: commands.Bot) -> str:
    """

    :param inter:
    :param bot:
    :return:
    """
    server = (
        await ServerSubscription.filter(id=inter.guild.id)
        .prefetch_related("channels")
        .get_or_none()
    )
    if not server:
        return "This server is not registered for any scheduled comic!"
    mention = ""
    match server.mention_policy:
        case MentionPolicy.All:
            mention = "each comic post"
        case MentionPolicy.Daily:
            mention = "daily"
        case MentionPolicy.Deactivated:
            return "Mentions are deactivated!"
    if server.role_id is not None:
        role = bot.get_guild(inter.guild.id).get_role(server.role_id)
        return f"The bot will mention the role {role.mention} {mention}!"
    return f"The server will mention for comics {mention}!"


async def remove_role(inter):
    """

    :param inter:
    :return:
    """
    server = (
        await ServerSubscription.filter(id=inter.guild.id)
        .prefetch_related("channels")
        .get_or_none()
    )
    if not server:
        return "This server is not registered for any scheduled comic!"
    server.role_id = None
    await server.save()
    return "Role mention successfully removed!"


async def get_sub_status(inter, comic_id: int):
    """Check if the comic is subscribed to this guild

    :param inter:
    :param comic_id:
    :return:
    """
    query = ServerSubscription.filter(id=inter.guild.id)
    if not await query.exists():
        return False
    server: ServerSubscription = await query.get()
    for channel in await server.channels:
        if await DiscordSubscription(comic_id=comic_id, channel=channel).exists():
            return True
    return False


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


async def check_comics_and_post(
    bot: discord.Client,
    subscriptions: list[DiscordSubscription],
    called_channel: Optional[discord.TextChannel] = None,
    post_time: datetime = None,
):
    """Load comics and check if they are the latest ones.
    Finally, post the comic to the channels.

    :param bot:
    :param subscriptions: The subscriptions
    :param called_channel: The channel of where the command was sent from (Should be None for the hourly poster
    and filled when called manually)
    :param post_time: The post time
    """
    if post_time is None:
        post_time = get_now()
    available_channels = {}
    not_available_channels = []
    mentioned_channels = []
    nb_of_comics_posted = 0
    # Check if any guild want the comic
    for comic_name, comic in all_comics().items():
        subs = list(filter(lambda s: s.comic_id == comic.id, subscriptions))
        if len(subs) == 0:
            continue
        # Get the details of the comic
        embed: Embed | None
        is_latest: bool
        try:
            details = await comic.get_comic(Action.Today, verify_latest=True)
            embed = details.to_embed()
            is_latest = details.is_latest
            if called_channel is None:
                # Only updates the link cache if it is done during the hourly loop
                link_cache[comic_name] = details.image_url
        except (Exception, ComicNotFound) as e:
            # Anything can happen (connection problem, etc... and the bot will crash if any error
            # is raised in the poster loop)
            logger.error(f"An error occurred while getting a comic: {e}")
            embed = ComicDetail.comic_not_found(comic_name)
            is_latest = False

        for sub in subs:
            # Finally, sends the comic
            nb_of_comics_posted += await load_channel_and_send(
                bot,
                sub,
                embed,
                is_latest,
                available_channels,
                not_available_channels,
                mentioned_channels,
                called_channel,
                post_time,
            )
    random_subs = list(
        filter(lambda s: s.subscription_type == SubscriptionType.Random, subscriptions)
    )
    for sub in random_subs:
        # Get the details of the comic
        embed: Embed | None
        is_latest: bool
        comic = await random.choice(list(all_comics().values()))
        try:
            embed = comic.get_comic(Action.Today).to_embed()
        except Exception as e:
            # Anything can happen (connection problem, etc... and the bot will crash if any error
            # is raised in the poster loop)
            logger.error(f"An error occurred while getting a comic: {e}")
            embed = ComicDetail.comic_not_found(comic.name)
        nb_of_comics_posted += await load_channel_and_send(
            bot,
            sub,
            embed,
            False,
            available_channels,
            not_available_channels,
            mentioned_channels,
            called_channel,
            post_time,
        )

    if called_channel is None:
        # Only logs the hourly loop at the end
        logger.info(
            f"The hourly loop sent {nb_of_comics_posted} comic(s) the "
            f"{get_now().strftime('%dth of %B %Y at %Hh')}"
        )
    if called_channel is not None and nb_of_comics_posted == 0:
        # If it was called manually ('post' command), and there is no comics to post anywhere in the guild,
        # it will warn in the channel that no comics needed to be sent, and it will conclude
        await called_channel.send("No comics to send!")


async def load_channel_and_send(
    bot: discord.Client,
    subscription: DiscordSubscription,
    embed: Embed,
    is_latest: bool,
    available_channels: dict,
    not_available_channels: list[int],
    mentionned_channels: list[int],
    called_channel: Optional[discord.TextChannel] = None,
    post_time: datetime = None,
) -> int:
    """Sends the loaded comic to the specified channel


    :param bot:
    :param subscription:
    :param embed: The embed with the comic
    :param is_latest: If the comic is the latest one
    :param available_channels: The dictionary of available channels
    :param not_available_channels: The dictionary of not-available channels
    :param mentionned_channels:
    :param called_channel: The channel of the where the command was called (None in the hourly loop,
    filled when called through /post).
    :param post_time: The post time

    :returns: 1 if it posted a comic, 0 if it could/did not
    """
    # Check if the comic is the latest and if it even cares about the latest comic
    if subscription.weekday == Weekday.Latest and not is_latest:
        return 0

    # Then, gets the channel object by its ID
    channel = await subscription.channel
    channel_id = channel.id

    if channel_id in available_channels:
        # Use the cached channel object
        channel = available_channels.get(channel_id)
    else:
        # Retrieves the channel object by the discord client
        channel = bot.get_channel(channel_id)
        # And save it for future use (so it can be looked up later)
        available_channels.update({channel_id: channel})

    if (
        channel is None
        or channel_id in not_available_channels
        or not channel.permissions_for(
            channel.guild.get_member(bot.user.id)
        ).send_messages
    ):
        # Remembers that the channel is not available
        not_available_channels.append(channel_id)
        if called_channel is None:
            # Logs that a channel is not available but still signed up for a comic
            logger.warning(
                f"A comic could not be posted to a channel. Channel id: {channel_id}"
            )
            return 0
        # If it can, send a message to the channel if an error occurred
        if channel is None:
            channel = await subscription.channel
            channel = channel.id
        else:
            channel = channel.mention
        await called_channel.send(f"Could not send message to channel {channel}")
        return 0
    # Makes sure that the channel is available (e.g. channel object is not None and the bot
    # can send messages)
    try:
        if channel.id not in mentionned_channels:
            await send_mention(bot, channel, subscription, post_time)
            mentionned_channels.append(channel.id)
        # Sends the comic embed (most important)
        await channel.send(embed=convert_embed(embed))
        return 1
    except Exception as e:
        # There is too many things that can go wrong here, just catch everything
        error_msg = (
            f"An error occurred in the hourly poster: {e.__class__.__name__}: {e}"
        )
        logger.error(error_msg)

        if called_channel is not None:
            # Send the error message to the channel too
            await called_channel.send(error_msg)
    # If it encountered an issue or there is no comic to send, return 0
    return 0


async def send_chan_embed(channel: discord.TextChannel, embed: Embed):
    """Send an embed in a channel

    :param channel: The channel object
    :param embed: The embed to send
    """


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


async def clean_database(
    bot: discord.Client = None,
    strict: bool = False,
    logger_: logging.Logger = None,
) -> int:
    """Clean the database from inactive servers

    :param bot:
    :param strict: Strict clean (Bypass role requirement)
    :param logger_:
    :return:
    """
    if logger_:
        logger_.info("Running database clean...")

    nb_removed = 0

    servers = await ServerSubscription.all()

    for guild in servers:
        # To take in account or not if a server still has a role tied to their info
        to_remove = False

        if bot is not None and bot.get_guild(guild.id) is None:
            # If it cannot find the server, bypass all others checks
            to_remove = True

        if (guild.role_id is None or strict) and not to_remove:
            # The server is available so lets check for other info that might indicate that the server is inactive
            for chan in await guild.channels:
                if await chan.subscriptions.all().count() <= 0:
                    await chan.delete()

        if await guild.channels.all().count() <= 0:
            await guild.delete()
            nb_removed += 1
    if logger_:
        logger_.info(f"Cleaned the database from {nb_removed} servers")
    return nb_removed


async def is_owner(inter: discord.Interaction):
    return inter.user.id == OWNER


async def send_mention(
    bot: Client,
    channel: discord.TextChannel,
    subscription: DiscordSubscription,
    post_time: datetime,
):
    """Send the first mention to the channel ('Comics for <date>, <hour> UTC @<role>')

    :param bot:
    :param channel:
    :param subscription:
    :param post_time:
    :return:
    """
    channel_sub = await subscription.channel
    server: ServerSubscription = await channel_sub.server
    if server.mention_policy == MentionPolicy.Deactivated or (
        server.mention_policy == MentionPolicy.Daily and post_time.hour != 6
    ):
        return
    guild = bot.get_guild(server.id)
    role_mention = guild.get_role(server.role_id) if server.role_id is not None else ""
    await channel.send(
        f"Comics for "
        f"{post_time.strftime('%A %B %dth %Y, %H h UTC')}"
        f" {role_mention}"
    )
