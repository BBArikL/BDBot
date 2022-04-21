import discord
import random
from discord.ext import commands
from src import utils


class Comic(commands.Cog):
    # Class responsible for sending comics

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client

    # --- Start of functions --- #
    # --- If you want to add another comic, add it here between this and the 'END OF COMICS PARAMETERS'. --- #

    @commands.hybrid_command()  # aliases=['Garfield', 'Garf', 'garfield'])
    async def garf(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):  # Garfield
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Garfield classics
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def calvinandhobbes(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['xkcd', 'xk'])
    async def xkcd(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):  # XKCD
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):  # Peanuts
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Peanuts begins
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):  # Dilbert
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Dilbertcl', 'Dilbcl', 'dilbcl'])
    async def dilbertcl(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Dilbert classics
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def cyanideandhappinness(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                   hour: str = None):
        # Cyanide and Happiness
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Frazz', 'fraz'])
    async def frazz(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):  # Frazz
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Garfieldminus', 'garfminus', 'gmng'])
    async def gmng(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['frank', 'Ernest', 'ernest', 'Frank&Ernest', 'frank&ernest'])
    async def frank(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Frank and Ernest by Thaves
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Broom', 'broom', 'Hilda', 'hilda'])
    async def broomhilda(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        # Broom  Hilda
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['emo', 'Emo', 'Cheerup', 'emokid'])
    async def cheerupemokid(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['brevity', 'brev'])
    async def brevity(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['catscafe', 'Cats', 'cats', 'cafe', 'cat'])
    async def catscafe(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['pop', 'Pop', 'Pops', 'Popeye'])
    async def popeye(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Popeye'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['Articcircle', 'articCircle', 'articcircle', 'Artic', 'artic', 'Circle', 'circle'])
    async def articcircle(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Artic-Circle'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['lockhorns', 'Lock', 'lock'])
    async def lockhorns(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Lockhorns'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['marvin', 'Marv', 'marv'])
    async def marvin(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Marvin'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['zits', 'Zit', 'zit'])
    async def zits(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Zits'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['hiandlois', 'Hi', 'hi', 'Lois', 'lois'])
    async def hiandlois(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Hi-and-Lois'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['SafelyEndangered', 'safelyendangered', 'Safely', 'safely', 'Safe'])
    async def safe(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Safely-Endangered'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['carl'])
    async def carl(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Carl'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['blueChair', 'Bluechair', 'bluechair', 'blue', 'chair'])
    async def bluechair(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'BlueChair'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['adventuresOfGod', 'adventuresGod', 'adventuresofgod', 'AOO', 'AOGod', 'aogod'])
    async def adventuresofgod(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Adventures-of-God'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['livewithyourself', 'Live', 'live', 'LWY', 'lwy'])
    async def livewithyourself(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Live-with-yourself'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['system32', 'Sys32', 'sys32', 'sys'])
    async def system32(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'System32comics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['theGamer', 'thegamer', 'Gamer', 'gamer', 'game'])
    async def thegamer(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'TheGamer'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['bignate', 'Nate', 'nate'])
    async def bignate(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'BigNate'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['getfuzzy', 'Fuzzy', 'fuzzy', 'fuzz'])
    async def getfuzzy(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'GetFuzzy'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['beetle', 'Bailey', 'bailey'])
    async def beetle(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'BeetleBailey'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['boondocks', 'Boon', 'boon'])
    async def boondocks(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'TheBoondocks'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['pickles', 'pick'])
    async def pickles(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'Pickles'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.hybrid_command()  # aliases=['pearls', 'Swine', 'swine'])
    async def pearls(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        comic_name = 'PearlsBeforeSwine'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    # Special comic commands
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command()
    async def all(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        strp = utils.strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await utils.parameters_interpreter(ctx, utils.get_strip_details(com), param=use, date=date, hour=hour)

    # Random comic
    @commands.hybrid_command()  # aliases=['rand', 'rnd'])
    async def random(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None, hour: str = None):
        await utils.parameters_interpreter(ctx, utils.get_strip_details(random.choice(
            list(utils.strip_details.keys()))), param=use, date=date, hour=hour)
    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#

    # --- END of cog ----#


async def setup(client):  # Initialize the cog
    await client.add_cog(Comic(client))
