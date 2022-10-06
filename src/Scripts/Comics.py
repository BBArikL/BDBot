import discord
import random

from discord import app_commands
from discord.ext import commands
from src.discord_utils import get_possible_hours, parameters_interpreter
from src.utils import Action, Date, get_strip_details, strip_details


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
    @app_commands.choices(hour=get_possible_hours())
    async def garfield(self, inter: discord.Interaction, action: Action,
                       date: Date, hour: int):
        """Garfield"""
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def garfield_classics(self, inter: discord.Interaction, action: Action,
                                date: Date,
                                hour: int):
        """Garfield classics"""
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def calvin_and_hobbes(self, inter: discord.Interaction, action: Action,
                                date: Date, hour: int):
        """Calvin and Hobbes"""
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def xkcd(self, inter: discord.Interaction, action: Action,
                   date: Date, hour: int):
        """XKCD"""
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def peanuts(self, inter: discord.Interaction, action: Action,
                      date: Date, hour: int):
        """Peanuts"""
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def peanuts_begins(self, inter: discord.Interaction, action: Action,
                             date: Date,
                             hour: int):
        """Peanuts begins"""
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def dilbert(self, inter: discord.Interaction, action: Action,
                      date: Date, hour: int):
        """Dilbert"""
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def dilbert_classics(self, inter: discord.Interaction, action: Action,
                               date: Date,
                               hour: int):
        """Dilbert classics"""
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def cyanide_and_happiness(self, inter: discord.Interaction, action: Action,
                                    date: Date,
                                    hour: int):
        """Cyanide and Happiness"""
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def frazz(self, inter: discord.Interaction, action: Action,
                    date: Date, hour: int):
        """Frazz"""
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def garfield_minus_garfield(self, inter: discord.Interaction, action: Action,
                                      date: Date,
                                      hour: int):
        """Garfield minus Garfield"""
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def frank_and_ernest(self, inter: discord.Interaction, action: Action,
                               date: Date,
                               hour: int):
        """Frank and Ernest"""
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def broom_hilda(self, inter: discord.Interaction, action: Action,
                          date: Date,
                          hour: int):
        """Broom Hilda"""
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def cheer_up_emo_kid(self, inter: discord.Interaction, action: Action,
                               date: Date,
                               hour: int):
        """Cheer up emo kid"""
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def brevity(self, inter: discord.Interaction, action: Action,
                      date: Date,
                      hour: int):
        """Brevity"""
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def cats_cafe(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """Cat's cafe"""
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def popeye(self, inter: discord.Interaction, action: Action,
                     date: Date,
                     hour: int):
        """Popeye"""
        comic_name = 'Popeye'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def artic_circle(self, inter: discord.Interaction, action: Action,
                           date: Date,
                           hour: int):
        """Artic Circle"""
        comic_name = 'Artic-Circle'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def lockhorns(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """The Lockhorns"""
        comic_name = 'Lockhorns'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def marvin(self, inter: discord.Interaction, action: Action,
                     date: Date,
                     hour: int):
        """Marvin"""
        comic_name = 'Marvin'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def zits(self, inter: discord.Interaction, action: Action,
                   date: Date, hour: int):
        """Zits"""
        comic_name = 'Zits'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def hi_and_lois(self, inter: discord.Interaction, action: Action,
                          date: Date,
                          hour: int):
        """Hi and Lois"""
        comic_name = 'Hi-and-Lois'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def safely_endangered(self, inter: discord.Interaction, action: Action,
                                date: Date,
                                hour: int):
        """Safely Endangered"""
        comic_name = 'Safely-Endangered'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def carl(self, inter: discord.Interaction, action: Action,
                   date: Date,
                   hour: int):
        """Carl"""
        comic_name = 'Carl'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def bluechair(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """Bluechair"""
        comic_name = 'BlueChair'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def adventures_of_god(self, inter: discord.Interaction, action: Action,
                                date: Date,
                                hour: int):
        """Adventures of God"""
        comic_name = 'Adventures-of-God'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def live_with_yourself(self, inter: discord.Interaction, action: Action,
                                 date: Date,
                                 hour: int):
        """Live with yourself"""
        comic_name = 'Live-with-yourself'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def system32(self, inter: discord.Interaction, action: Action,
                       date: Date, hour: int):
        """System32"""
        comic_name = 'System32comics'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def the_gamer(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """The Gamer"""
        comic_name = 'TheGamer'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def bignate(self, inter: discord.Interaction, action: Action,
                      date: Date, hour: int):
        """Big Nate"""
        comic_name = 'BigNate'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def get_fuzzy(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """Get Fuzzy"""
        comic_name = 'GetFuzzy'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def beetle_bailey(self, inter: discord.Interaction, action: Action,
                            date: Date,
                            hour: int):
        """Beetle Bailey"""
        comic_name = 'BeetleBailey'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def boondocks(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """The Boondocks"""
        comic_name = 'TheBoondocks'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def pickles(self, inter: discord.Interaction, action: Action,
                      date: Date, hour: int):
        """Pickles"""
        comic_name = 'Pickles'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def pearls_before_swine(self, inter: discord.Interaction, action: Action,
                                  date: Date,
                                  hour: int):
        """Pearls before swine"""
        comic_name = 'PearlsBeforeSwine'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def chibird(self, inter: discord.Interaction, action: Action,
                      date: Date,
                      hour: int):
        """Chibird"""
        comic_name = 'Chibird'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def war_and_peas(self, inter: discord.Interaction, action: Action,
                           date: Date,
                           hour: int):
        """War and Peas"""
        comic_name = 'WarAndPeas'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def humans_are_stupid(self, inter: discord.Interaction, action: Action,
                                date: Date,
                                hour: int):
        """Humans are stupid"""
        comic_name = 'HumansAreStupid'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def maximumble(self, inter: discord.Interaction, action: Action,
                         date: Date,
                         hour: int):
        """Maximumble"""
        comic_name = 'Maximumble'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def poorly_drawn_lines(self, inter: discord.Interaction, action: Action,
                                 date: Date,
                                 hour: int):
        """Poorly Drawn Lines"""
        comic_name = 'PoorlyDrawnLines'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def heathcliff(self, inter: discord.Interaction, action: Action,
                         date: Date,
                         hour: int):
        """Heathcliff"""
        comic_name = 'Heathcliff'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def andy_capp(self, inter: discord.Interaction, action: Action,
                        date: Date,
                        hour: int):
        """Andy Capp"""
        comic_name = 'AndyCapp'

        # Interprets the parameters given by the user
        await parameters_interpreter(inter, get_strip_details(comic_name), param=action, date=date,
                                     hour=hour)

    @app_commands.command()
    @app_commands.choices(hour=get_possible_hours())
    async def random(self, inter: discord.Interaction, action: Action,
                     date: Date, hour: int):
        """Random comic"""
        await parameters_interpreter(inter, get_strip_details(random.choice(
            list(strip_details.keys()))), param=action, date=date, hour=hour)

    @app_commands.command()
    @commands.has_permissions(manage_guild=True)
    @app_commands.choices(hour=get_possible_hours())
    async def all(self, inter: discord.Interaction, action: Action,
                  date: Date, hour: int):
        """All comics. Mods only"""
        strp = strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await parameters_interpreter(inter, get_strip_details(com), param=action, date=date,
                                         hour=hour)
    # Special comic commands

    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#
    # --- END of cog ----#


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord bot
    """
    await bot.add_cog(Comic(bot))
