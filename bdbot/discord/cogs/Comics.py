import random
import re
from typing import Any, Callable, Union

import discord
from discord import app_commands
from discord.ext import commands

from bdbot.discord_utils import NextSend, get_possible_hours, parameters_interpreter
from bdbot.utils import Action, Date, Month, get_all_strips, get_strip_details


def define_comic_callback(comic_strip_details: dict[str, Union[str, int]]):
    async def date_comic_callback(
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
    ):
        # Interprets the parameters given by the user
        func, params = parameters_interpreter(
            inter,
            comic_strip_details,
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )
        await func(**params)

    async def number_comic_callback(
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        comic_number: int = None,
    ):
        # Interprets the parameters given by the user
        func, params = parameters_interpreter(
            inter,
            comic_strip_details,
            action=action,
            date=date,
            hour=hour,
            comic_number=comic_number,
        )

        await func(**params)

    comic_callback_func: Callable

    if (
        comic_strip_details["Working_type"] == "date"
        or comic_strip_details["Main_website"] == "https://garfieldminusgarfield.net/"
    ):
        comic_callback_func = date_comic_callback
    else:
        comic_callback_func = number_comic_callback

    return comic_callback_func


class Comic(commands.Cog):
    """Class responsible for sending comics"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        :param bot: The discord Bot
        """
        self.bot = bot

        comics_details = get_all_strips()

        for comic in comics_details:
            comic_name: str = comics_details[comic]["Name"]
            normalized_name = comic_name.lower().replace(" ", "_")
            normalized_name = re.sub("[^\\w\\-_]", "", normalized_name)
            comic_command = app_commands.Command(
                name=normalized_name,
                description=comic_name,
                callback=define_comic_callback(comics_details[comic]),
            )
            # No built-in functions for adding autocomplete choices when creating callbacks in a factory way
            comic_command._params.get("hour").choices = (  # noqa: See above
                get_possible_hours()
            )

            self.bot.tree.add_command(comic_command)

    async def cog_unload(self) -> None:
        comics_details = get_all_strips()

        for comic in comics_details:
            comic_name: str = comics_details[comic]["Name"]
            normalized_name = comic_name.lower().replace(" ", "_")
            normalized_name = re.sub("[^\\w\\-_]", "", normalized_name)
            self.bot.tree.remove_command(normalized_name)

    # --- Start of functions --- #
    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def random(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
        comic_number: int = None,
    ):
        """Random comic"""
        func, params = parameters_interpreter(
            inter,
            get_strip_details(random.choice(list(get_all_strips().keys()))),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
            comic_number=comic_number,
        )
        await func(**params)

    @app_commands.command()
    @commands.has_permissions(manage_guild=True)
    @app_commands.choices(hour=get_possible_hours())
    async def all(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
        comic_number: int = None,
    ):
        """All comics. Mods only"""
        first = True
        for com in get_all_strips():
            # Interprets the parameters given by the user
            func: Callable
            params: dict[str, Any]
            func, params = parameters_interpreter(
                inter,
                get_strip_details(com),
                action=action,
                date=date,
                hour=hour,
                day=day,
                month=month,
                year=year,
                comic_number=comic_number,
            )

            if first:
                first = False
            else:
                params.update({"next_send": NextSend.Followup})

            await func(**params)

    # Special comic commands

    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#
    # --- END of cog ----#


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord bot
    """
    await bot.add_cog(Comic(bot))
