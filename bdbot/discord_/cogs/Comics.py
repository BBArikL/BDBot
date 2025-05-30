import random
import re
from typing import Any, Callable

import discord
from discord import app_commands
from discord.ext import commands

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.base import BaseComic, WorkingType
from bdbot.comics.custom import GarfieldMinusGarfield
from bdbot.discord_.client import BDBotClient
from bdbot.discord_.discord_utils import (
    NextSend,
    get_possible_hours,
    parameters_interpreter,
)
from bdbot.time import Month, Weekday


def define_comic_callback(bot: BDBotClient, comic: BaseComic):
    async def date_comic_callback(
        inter: discord.Interaction,
        action: Action,
        date: Weekday = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
    ):
        # Interprets the parameters given by the user
        func, params = await parameters_interpreter(
            bot,
            inter,
            comic,
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
        date: Weekday = None,
        hour: int = None,
        comic_number: int = None,
    ):
        # Interprets the parameters given by the user
        func, params = await parameters_interpreter(
            bot,
            inter,
            comic,
            action=action,
            date=date,
            hour=hour,
            comic_number=comic_number,
        )

        await func(**params)

    if comic.WORKING_TYPE == WorkingType.Date or isinstance(
        comic, GarfieldMinusGarfield
    ):
        return date_comic_callback

    return number_comic_callback


class Comic(commands.Cog):
    """Class responsible for sending comics"""

    def __init__(self, bot: BDBotClient):
        """Constructor of the cog

        :param bot: The discord Bot
        """
        self.bot = bot
        for comic in self.bot.comic_details.values():
            normalized_name = comic.name.lower().replace(" ", "_")
            normalized_name = re.sub("([^\\w\\-_]|\\.)", "", normalized_name)
            comic_command = app_commands.Command(
                name=normalized_name,
                description=comic.name,
                callback=define_comic_callback(self.bot, comic),
            )
            # No built-in functions for adding autocomplete choices when creating callbacks in a factory way
            comic_command._params.get("hour").choices = (  # noqa: See above
                get_possible_hours()
            )

            self.bot.tree.add_command(comic_command)

    async def cog_unload(self) -> None:
        for comic in self.bot.comic_details.values():
            comic_name: str = comic.name
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
        date: Weekday = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
        comic_number: int = None,
    ):
        """Random comic"""
        comic = random.choice(list(self.bot.comic_details.values()))
        if action == Action.Add:
            action = ExtendedAction.Add_random
        elif action == Action.Remove:
            action = ExtendedAction.Remove_random
        func, params = await parameters_interpreter(
            self.bot,
            inter,
            comic,
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
        date: Weekday = None,
        hour: int = None,
        day: int = None,
        month: Month = None,
        year: int = None,
        comic_number: int = None,
    ):
        """All comics. Mods only"""
        first = True
        for comic in self.bot.comic_details.values():
            # Interprets the parameters given by the user
            func: Callable
            params: dict[str, Any]
            func, params = await parameters_interpreter(
                self.bot,
                inter,
                comic,
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


async def setup(bot: BDBotClient):
    """Initialize the cog

    :param bot: The discord bot
    """
    await bot.add_cog(Comic(bot))
