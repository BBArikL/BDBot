import discord
import random

from discord import app_commands
from discord.ext import commands
from src import utils, discord_utils


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
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def garfield(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Garfield"""
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def garfield_classics(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                hour: str = None):
        """Garfield classics"""
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def calvin_and_hobbes(self, ctx: discord.ext.commands.Context, action: str = None,
                                date: str = None, hour: str = None):
        """Calvin and Hobbes"""
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def xkcd(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """XKCD"""
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def peanuts(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Peanuts"""
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def peanuts_begins(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                             hour: str = None):
        """Peanuts begins"""
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def dilbert(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Dilbert"""
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def dilbert_classics(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                               hour: str = None):
        """Dilbert classics"""
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def cyanide_and_happiness(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                    hour: str = None):
        """Cyanide and Happiness"""
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def frazz(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Frazz"""
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def garfield_minus_garfield(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                      hour: str = None):
        """Garfield minus Garfield"""
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def frank_and_ernest(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                               hour: str = None):
        """Frank and Ernest"""
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def broom_hilda(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                          hour: str = None):
        """Broom Hilda"""
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def cheer_up_emo_kid(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                               hour: str = None):
        """Cheer up emo kid"""
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def brevity(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                      hour: str = None):
        """Brevity"""
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def cats_cafe(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """Cat's cafe"""
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def popeye(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                     hour: str = None):
        """Popeye"""
        comic_name = 'Popeye'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def artic_circle(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                           hour: str = None):
        """Artic Circle"""
        comic_name = 'Artic-Circle'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def lockhorns(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """The Lockhorns"""
        comic_name = 'Lockhorns'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def marvin(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                     hour: str = None):
        """Marvin"""
        comic_name = 'Marvin'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def zits(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Zits"""
        comic_name = 'Zits'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def hi_and_lois(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                          hour: str = None):
        """Hi and Lois"""
        comic_name = 'Hi-and-Lois'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def safely_endangered(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                hour: str = None):
        """Safely Endangered"""
        comic_name = 'Safely-Endangered'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def carl(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                   hour: str = None):
        """Carl"""
        comic_name = 'Carl'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def bluechair(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """Bluechair"""
        comic_name = 'BlueChair'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def adventures_of_god(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                hour: str = None):
        """Adventures of God"""
        comic_name = 'Adventures-of-God'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def live_with_yourself(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                 hour: str = None):
        """Live with yourself"""
        comic_name = 'Live-with-yourself'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def system32(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """System32"""
        comic_name = 'System32comics'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def the_gamer(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """The Gamer"""
        comic_name = 'TheGamer'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def bignate(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Big Nate"""
        comic_name = 'BigNate'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def get_fuzzy(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """Get Fuzzy"""
        comic_name = 'GetFuzzy'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def beetle_bailey(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                            hour: str = None):
        """Beetle Bailey"""
        comic_name = 'BeetleBailey'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def boondocks(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """The Boondocks"""
        comic_name = 'TheBoondocks'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def pickles(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Pickles"""
        comic_name = 'Pickles'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def pearls_before_swine(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                  hour: str = None):
        """Pearls before swine"""
        comic_name = 'PearlsBeforeSwine'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def chibird(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                      hour: str = None):
        """Chibird"""
        comic_name = 'Chibird'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def war_and_peas(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                           hour: str = None):
        """War and Peas"""
        comic_name = 'WarAndPeas'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def humans_are_stupid(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                hour: str = None):
        """Humans are stupid"""
        comic_name = 'HumansAreStupid'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def maximumble(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                         hour: str = None):
        """Maximumble"""
        comic_name = 'Maximumble'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def poorly_drawn_lines(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                                 hour: str = None):
        """Poorly Drawn Lines"""
        comic_name = 'PoorlyDrawnLines'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def heathcliff(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                         hour: str = None):
        """Heathcliff"""
        comic_name = 'Heathcliff'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def andy_capp(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None,
                        hour: str = None):
        """Andy Capp"""
        comic_name = 'AndyCapp'

        # Interprets the parameters given by the user
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=action, date=date,
                                                   hour=hour)

    @app_commands.command()
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def random(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """Random comic"""
        await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(random.choice(
            list(utils.strip_details.keys()))), param=action, date=date, hour=hour)

    @app_commands.command()
    @commands.has_permissions(manage_guild=True)
    @app_commands.autocomplete(action=discord_utils.comic_action_autocomplete,
                               date=discord_utils.comic_date_autocomplete,
                               hour=discord_utils.comic_hour_autocomplete)
    async def all(self, ctx: discord.ext.commands.Context, action: str = None, date: str = None, hour: str = None):
        """All comics. Mods only"""
        strp = utils.strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await discord_utils.parameters_interpreter(ctx, utils.get_strip_details(com), param=action, date=date,
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
