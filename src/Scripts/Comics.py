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

    @commands.command(aliases=['Garfield', 'Garf', 'garfield'])
    async def garf(self, ctx, use=None, date=None, hour=None):  # Garfield
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx, use=None, date=None, hour=None):  # Garfield classics
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def CH(self, ctx, use=None, date=None, hour=None):  # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['xkcd', 'xk'])
    async def XKCD(self, ctx, use=None, date=None, hour=None):  # XKCD
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx, use=None, date=None, hour=None):  # Peanuts
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx, use=None, date=None, hour=None):  # Peanuts begins
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx, use=None, date=None, hour=None):  # Dilbert
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Dilbertcl', 'Dilbcl', 'dilbcl'])
    async def dilbertcl(self, ctx, use=None, date=None, hour=None):  # Dilbert classics
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def CyanideandHappinness(self, ctx, use=None, date=None, hour=None):  # Cyanide and Happiness
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Frazz', 'fraz'])
    async def frazz(self, ctx, use=None, date=None, hour=None):  # Frazz
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Garfieldminus', 'garfminus', 'gmng'])
    async def GmnG(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    """@commands.command(aliases=['Jon'])
    async def jon(self, ctx, use=None, date=None, hour=None):  # Jon
        comic_name = 'Jon'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)"""

    @commands.command(aliases=['frank', 'Ernest', 'ernest', 'Frank&Ernest', 'frank&ernest'])
    async def Frank(self, ctx, use=None, date=None, hour=None):  # Frank and Ernest by Thaves
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Broom', 'broom', 'Hilda', 'hilda'])
    async def BroomHilda(self, ctx, use=None, date=None, hour=None):  # Broom  Hilda
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Inspector', 'inspector', 'crime', 'crimequiz'])
    async def InspectorDanger(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Inspector-Dangers-Crime-Quiz'

        await ctx.send("""Without any notice, this comic has stopped being posted on GoComics. This command will then 
        sunset during the next update. This is a particularly sad moment to see a comic like this disappear. You can 
        still find the book online (Amazon or Apple books (I am not affiliated in any way)), but most of the 
        documentation and newer comics are mostly gone. The wayback machine has some pages stored (
        <https://web.archive.org/web/*/https://www.gocomics.com/inspector-dangers-crime-quiz*>) too. Finally, 
        this incident wil give to this bot a new purpose (in the next update): Whenever a comic is requested at 6 AM 
        UTC, the page will be saved and archived through the internet archive. Thank you for using BDBot!""")

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['emo', 'Emo', 'Cheerup', 'emokid'])
    async def Cheerupemokid(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['brevity', 'brev'])
    async def Brevity(self, ctx, use=None, date=None, hour=None):
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['catscafe', 'Cats', 'cats', 'cafe', 'cat'])
    async def CatsCafe(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['pop', 'Pop', 'Pops', 'Popeye'])
    async def popeye(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Popeye'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['Articcircle', 'articCircle', 'articcircle', 'Artic', 'artic', 'Circle', 'circle'])
    async def ArticCircle(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Artic-Circle'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['lockhorns', 'Lock', 'lock'])
    async def Lockhorns(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Lockhorns'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['marvin', 'Marv', 'marv'])
    async def Marvin(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Marvin'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['zits', 'Zit', 'zit'])
    async def Zits(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Zits'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['hiandlois', 'Hi', 'hi', 'Lois', 'lois'])
    async def HiandLois(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Hi-and-Lois'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['SafelyEndangered', 'safelyendangered', 'Safely', 'safely', 'Safe'])
    async def safe(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Safely-Endangered'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['carl'])
    async def Carl(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Carl'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['blueChair', 'Bluechair', 'bluechair', 'blue', 'chair'])
    async def BlueChair(self, ctx, use=None, date=None, hour=None):
        comic_name = 'BlueChair'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['adventuresOfGod', 'adventuresGod', 'adventuresofgod', 'AOO', 'AOGod', 'aogod'])
    async def AdventuresOfGod(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Adventures-of-God'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['livewithyourself', 'Live', 'live', 'LWY', 'lwy'])
    async def LiveWithYourself(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Live-with-yourself'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['system32', 'Sys32', 'sys32', 'sys'])
    async def System32(self, ctx, use=None, date=None, hour=None):
        comic_name = 'System32comics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['theGamer', 'thegamer', 'Gamer', 'gamer', 'game'])
    async def TheGamer(self, ctx, use=None, date=None, hour=None):
        comic_name = 'TheGamer'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['bignate', 'Nate', 'nate'])
    async def BigNate(self, ctx, use=None, date=None, hour=None):
        comic_name = 'BigNate'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['getfuzzy', 'Fuzzy', 'fuzzy', 'fuzz'])
    async def GetFuzzy(self, ctx, use=None, date=None, hour=None):
        comic_name = 'GetFuzzy'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['beetle', 'Bailey', 'bailey'])
    async def Beetle(self, ctx, use=None, date=None, hour=None):
        comic_name = 'BeetleBailey'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['boondocks', 'Boon', 'boon'])
    async def Boondocks(self, ctx, use=None, date=None, hour=None):
        comic_name = 'TheBoondocks'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['pickles', 'pick'])
    async def Pickles(self, ctx, use=None, date=None, hour=None):
        comic_name = 'Pickles'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    @commands.command(aliases=['pearls', 'Swine', 'swine'])
    async def Pearls(self, ctx, use=None, date=None, hour=None):
        comic_name = 'PearlsBeforeSwine'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)

    # Special comic commands
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def all(self, ctx, use=None, date=None, hour=None):
        strp = utils.strip_details
        for com in strp:
            # Interprets the parameters given by the user
            await utils.parameters_interpreter(ctx, utils.get_strip_details(com), param=use, date=date, hour=hour)

    # Random comic
    @commands.command(aliases=['rand', 'rnd'])
    async def random(self, ctx, use=None, date=None, hour=None):
        await utils.parameters_interpreter(ctx, utils.get_strip_details(random.choice(
            list(utils.strip_details.keys()))), param=use, date=date, hour=hour)
    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#

    # --- END of cog ----#


def setup(client):  # Initialize the cog
    client.add_cog(Comic(client))
