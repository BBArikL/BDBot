import discord
import random
from discord.ext import commands
from src import utils


class Comic(commands.Cog):
    """Class responsible for sending comics"""

    def __init__(self, bot: commands.Bot):
        """Constructor of the cog

        :param bot: The discord Bot
        """
        self.client = bot

    # --- Start of functions --- #
    # --- If you want to add another comic, add it here between this and the 'END OF COMICS PARAMETERS'. --- #

    @commands.hybrid_command()
    async def garf(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Garfield"""
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def garfield_classics(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                hour: str = None):
        """Garfield classics"""
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def calvin_and_hobbes(self, ctx: discord.ext.commands.Context, use: str = None,
                                date: str = None, hour: str = None):
        """Calvin and Hobbes"""
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def xkcd(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """XKCD"""
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def peanuts(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Peanuts"""
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def peanuts_begins(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                             hour: str = None):
        """Peanuts begins"""
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def dilbert(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Dilbert"""
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def dilbert_classics(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                               hour: str = None):
        """Dilbert classics"""
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def cyanide_and_happinness(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                     hour: str = None):
        """Cyanide and Happiness"""
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def frazz(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Frazz"""
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def garfield_minus_garfield(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                      hour: str = None):
        """Garfield minus Garfield"""
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def frank_and_ernest(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                               hour: str = None):
        """Frank and Ernest"""
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def broom_hilda(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Broom Hilda"""
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def cheer_up_emo_kid(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                               hour: str = None):
        """Cheer up emo kid"""
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def brevity(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Brevity"""
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def cats_cafe(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Cat's cafe"""
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def popeye(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Popeye"""
        comic_name = 'Popeye'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def artic_circle(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                           hour: str = None):
        """Artic Circle"""
        comic_name = 'Artic-Circle'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def lockhorns(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """The Lockhorns"""
        comic_name = 'Lockhorns'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def marvin(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Marvin"""
        comic_name = 'Marvin'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def zits(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Zits"""
        comic_name = 'Zits'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def hi_and_lois(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Hi and Lois"""
        comic_name = 'Hi-and-Lois'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def safely_endangered(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                hour: str = None):
        """Safely Endangered"""
        comic_name = 'Safely-Endangered'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def carl(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Carl"""
        comic_name = 'Carl'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def bluechair(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Bluechair"""
        comic_name = 'BlueChair'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def adventures_of_god(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                hour: str = None):
        """Adventures of God"""
        comic_name = 'Adventures-of-God'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def live_with_yourself(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                 hour: str = None):
        """Live with yourself"""
        comic_name = 'Live-with-yourself'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def system32(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """System32"""
        comic_name = 'System32comics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def the_gamer(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """The Gamer"""
        comic_name = 'TheGamer'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def bignate(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Big Nate"""
        comic_name = 'BigNate'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def get_fuzzy(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Get Fuzzy"""
        comic_name = 'GetFuzzy'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def beetle_bailey(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                            hour: str = None):
        """Beetle Bailey"""
        comic_name = 'BeetleBailey'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def boondocks(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """The Boondocks"""
        comic_name = 'TheBoondocks'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def pickles(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Pickles"""
        comic_name = 'Pickles'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def pearls_before_swine(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                  hour: str = None):
        """Pearls before swine"""
        comic_name = 'PearlsBeforeSwine'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def heathcliff(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                         hour: str = None):
        """Heathcliff"""
        comic_name = 'Heathcliff'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    # Special comic commands
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command()
    async def all(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """All comics. Mods only"""
        strp = utils.strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await utils.parameters_interpreter(ctx, utils.get_strip_details(com), param=use, date=date, hour=hour)

    @commands.hybrid_command()
    async def random(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        """Random comic"""
        await utils.parameters_interpreter(ctx, utils.get_strip_details(random.choice(
            list(utils.strip_details.keys()))), param=use, date=date, hour=hour)

    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#
    # --- END of cog ----#


async def setup(bot: commands.Bot):
    """Initialize the cog

    :param bot: The discord bot
    """
    await bot.add_cog(Comic(bot))
