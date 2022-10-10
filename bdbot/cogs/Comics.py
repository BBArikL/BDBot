import random

import discord
from discord import app_commands
from discord.ext import commands

from bdbot.discord_utils import get_possible_hours, parameters_interpreter
from bdbot.utils import Action, Date, Month, get_strip_details, strip_details


class Comic(commands.Cog):
    """Class responsible for sending comics"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        :param bot: The discord Bot
        """
        self.client = bot

    # --- Start of functions --- #
    # --- If you want to add another comic, add it here between this and the 'END OF COMICS PARAMETERS'. --- #

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def garfield(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Garfield"""
        comic_name = "Garfield"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def garfield_classics(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Garfield classics"""
        comic_name = "Garfield_Classics"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def calvin_and_hobbes(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Calvin and Hobbes"""
        comic_name = "CalvinandHobbes"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def xkcd(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """XKCD"""
        comic_name = "XKCD"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def peanuts(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Peanuts"""
        comic_name = "Peanuts"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def peanuts_begins(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Peanuts begins"""
        comic_name = "Peanuts_Begins"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def dilbert(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Dilbert"""
        comic_name = "Dilbert"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def dilbert_classics(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Dilbert classics"""
        comic_name = "Dilbert-Classics"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def cyanide_and_happiness(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Cyanide and Happiness"""
        comic_name = "Cyanide_and_Happiness"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def frazz(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Frazz"""
        comic_name = "Frazz"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def garfield_minus_garfield(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Garfield minus Garfield"""
        comic_name = "Garfield_minus_Garfield"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def frank_and_ernest(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Frank and Ernest"""
        comic_name = "Frank-and-Ernest"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def broom_hilda(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Broom Hilda"""
        comic_name = "BroomHilda"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def cheer_up_emo_kid(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Cheer up emo kid"""
        comic_name = "Cheer-up-emo-kid"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def brevity(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Brevity"""
        comic_name = "brevity"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def cats_cafe(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Cat's cafe"""
        comic_name = "Cats-Cafe"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def popeye(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Popeye"""
        comic_name = "Popeye"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def artic_circle(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Artic Circle"""
        comic_name = "Artic-Circle"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def lockhorns(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """The Lockhorns"""
        comic_name = "Lockhorns"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def marvin(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Marvin"""
        comic_name = "Marvin"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def zits(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Zits"""
        comic_name = "Zits"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def hi_and_lois(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Hi and Lois"""
        comic_name = "Hi-and-Lois"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def safely_endangered(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Safely Endangered"""
        comic_name = "Safely-Endangered"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def carl(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Carl"""
        comic_name = "Carl"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def bluechair(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Bluechair"""
        comic_name = "BlueChair"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def adventures_of_god(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Adventures of God"""
        comic_name = "Adventures-of-God"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def live_with_yourself(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Live with yourself"""
        comic_name = "Live-with-yourself"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def system32(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """System32"""
        comic_name = "System32comics"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def the_gamer(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """The Gamer"""
        comic_name = "TheGamer"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def bignate(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Big Nate"""
        comic_name = "BigNate"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def get_fuzzy(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Get Fuzzy"""
        comic_name = "GetFuzzy"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def beetle_bailey(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Beetle Bailey"""
        comic_name = "BeetleBailey"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def boondocks(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """The Boondocks"""
        comic_name = "TheBoondocks"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def pickles(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Pickles"""
        comic_name = "Pickles"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def pearls_before_swine(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Pearls before swine"""
        comic_name = "PearlsBeforeSwine"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def chibird(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Chibird"""
        comic_name = "Chibird"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def war_and_peas(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """War and Peas"""
        comic_name = "WarAndPeas"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def humans_are_stupid(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Humans are stupid"""
        comic_name = "HumansAreStupid"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def maximumble(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Maximumble"""
        comic_name = "Maximumble"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def poorly_drawn_lines(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Poorly Drawn Lines"""
        comic_name = "PoorlyDrawnLines"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def heathcliff(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Heathcliff"""
        comic_name = "Heathcliff"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def andy_capp(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Andy Capp"""
        comic_name = "AndyCapp"

        # Interprets the parameters given by the user
        await parameters_interpreter(
            inter,
            get_strip_details(comic_name),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def random(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """Random comic"""
        await parameters_interpreter(
            inter,
            get_strip_details(random.choice(list(strip_details.keys()))),
            action=action,
            date=date,
            hour=hour,
            day=day,
            month=month,
            year=year,
        )

    @app_commands.command()
    @commands.has_permissions(manage_guild=True)
    @app_commands.choices(
        hour=get_possible_hours(), day=get_possible_days(), year=get_possible_years()
    )
    async def all(
        self,
        inter: discord.Interaction,
        action: Action,
        date: Date = None,
        hour: int = None,
        day: int = 1,
        month: Month = Month.February,
        year: int = 1950,
    ):
        """All comics. Mods only"""
        strp = strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await parameters_interpreter(
                inter,
                get_strip_details(com),
                action=action,
                date=date,
                hour=hour,
                day=day,
                month=month,
                year=year,
            )

    # Special comic commands

    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#
    # --- END of cog ----#


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord bot
    """
    await bot.add_cog(Comic(bot))
