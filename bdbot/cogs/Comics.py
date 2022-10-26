import random
from typing import Any, Callable, Union

import discord
from discord import app_commands
from discord.ext import commands

from bdbot.discord_utils import get_possible_hours, parameters_interpreter, NextSend
from bdbot.utils import Action, Date, Month, get_strip_details, get_all_strips


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
            comic_number: int = None
    ):
        # Interprets the parameters given by the user
        func, params = parameters_interpreter(
            inter,
            comic_strip_details,
            action=action,
            date=date,
            hour=hour,
            comic_number=comic_number
        )

        await func(**params)

    comic_callback_func: Callable

    if comic_strip_details["Working_type"] == "date" or \
            comic_strip_details["Main_website"] == "https://garfieldminusgarfield.net/":
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
        self.client = bot

        comics_details = get_all_strips()

        for comic in comics_details:
            comic_name: str = comics_details[comic]["Name"]
            comic_command = app_commands.Command(
                name=comic_name.lower().replace(" ", "_"),
                description=comic_name,
                callback=define_comic_callback(comics_details[comic]))
            # No built-in functions for adding autocomplete choices when creating callbacks in a factory way
            comic_command._params.update({"hour": get_possible_hours()})  # noqa: See above

            self.client.add_command(comic_command)

    # --- Start of functions --- #
    # --- If you want to add another comic, add it here between this and the 'END OF COMICS PARAMETERS'. --- #

    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def garfield(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Garfield"""
    #     comic_name = "Garfield"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def garfield_classics(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Garfield classics"""
    #     comic_name = "Garfield_Classics"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def calvin_and_hobbes(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Calvin and Hobbes"""
    #     comic_name = "CalvinandHobbes"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def xkcd(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """XKCD"""
    #     comic_name = "XKCD"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def peanuts(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Peanuts"""
    #     comic_name = "Peanuts"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def peanuts_begins(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Peanuts begins"""
    #     comic_name = "Peanuts_Begins"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def dilbert(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Dilbert"""
    #     comic_name = "Dilbert"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def dilbert_classics(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Dilbert classics"""
    #     comic_name = "Dilbert-Classics"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def cyanide_and_happiness(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Cyanide and Happiness"""
    #     comic_name = "Cyanide_and_Happiness"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def frazz(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Frazz"""
    #     comic_name = "Frazz"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def garfield_minus_garfield(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Garfield minus Garfield"""
    #     comic_name = "Garfield_minus_Garfield"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def frank_and_ernest(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Frank and Ernest"""
    #     comic_name = "Frank-and-Ernest"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def broom_hilda(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Broom Hilda"""
    #     comic_name = "BroomHilda"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def cheer_up_emo_kid(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Cheer up emo kid"""
    #     comic_name = "Cheer-up-emo-kid"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def brevity(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Brevity"""
    #     comic_name = "brevity"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def cats_cafe(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Cat's cafe"""
    #     comic_name = "Cats-Cafe"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def popeye(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Popeye"""
    #     comic_name = "Popeye"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def artic_circle(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Artic Circle"""
    #     comic_name = "Artic-Circle"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def lockhorns(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """The Lockhorns"""
    #     comic_name = "Lockhorns"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def marvin(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Marvin"""
    #     comic_name = "Marvin"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def zits(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Zits"""
    #     comic_name = "Zits"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def hi_and_lois(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Hi and Lois"""
    #     comic_name = "Hi-and-Lois"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def safely_endangered(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Safely Endangered"""
    #     comic_name = "Safely-Endangered"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def carl(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Carl"""
    #     comic_name = "Carl"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def bluechair(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Bluechair"""
    #     comic_name = "BlueChair"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def adventures_of_god(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Adventures of God"""
    #     comic_name = "Adventures-of-God"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def live_with_yourself(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Live with yourself"""
    #     comic_name = "Live-with-yourself"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def system32(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """System32"""
    #     comic_name = "System32comics"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def the_gamer(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """The Gamer"""
    #     comic_name = "TheGamer"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def bignate(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Big Nate"""
    #     comic_name = "BigNate"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def get_fuzzy(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Get Fuzzy"""
    #     comic_name = "GetFuzzy"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def beetle_bailey(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Beetle Bailey"""
    #     comic_name = "BeetleBailey"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def boondocks(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """The Boondocks"""
    #     comic_name = "TheBoondocks"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def pickles(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Pickles"""
    #     comic_name = "Pickles"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def pearls_before_swine(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Pearls before swine"""
    #     comic_name = "PearlsBeforeSwine"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def chibird(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Chibird"""
    #     comic_name = "Chibird"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def war_and_peas(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """War and Peas"""
    #     comic_name = "WarAndPeas"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def humans_are_stupid(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Humans are stupid"""
    #     comic_name = "HumansAreStupid"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def maximumble(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Maximumble"""
    #     comic_name = "Maximumble"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def poorly_drawn_lines(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Poorly Drawn Lines"""
    #     comic_name = "PoorlyDrawnLines"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def heathcliff(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Heathcliff"""
    #     comic_name = "Heathcliff"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)
    #
    # @app_commands.command()
    # @app_commands.choices(hour=get_possible_hours())
    # async def andy_capp(
    #     self,
    #     inter: discord.Interaction,
    #     action: Action,
    #     date: Date = None,
    #     hour: int = None,
    #     day: int = None,
    #     month: Month = None,
    #     year: int = None,
    #     comic_number: int = None,
    # ):
    #     """Andy Capp"""
    #     comic_name = "AndyCapp"
    #
    #     # Interprets the parameters given by the user
    #     func, params = parameters_interpreter(
    #         inter,
    #         get_strip_details(comic_name),
    #         action=action,
    #         date=date,
    #         hour=hour,
    #         day=day,
    #         month=month,
    #         year=year,
    #         comic_number=comic_number,
    #     )
    #     await func(**params)

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
