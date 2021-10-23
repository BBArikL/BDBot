import random
from discord.ext import commands
from Comics_details import comDetails
import utils


class Comic(commands.Cog):
    # Class responsible for sending comics

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.strip_details = comDetails.load_details()

    # --- Start of functions PS: (If you want to add another comic, add it here between this and the 'END of comics
    # parameters').

    @commands.command(aliases=['Garfield', 'Garf', 'garfield'])
    async def garf(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def CH(self, ctx, *, param=None):  # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['xkcd', 'xk'])
    async def XKCD(self, ctx, *, param=None):  # XKCD
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx, *, param=None):  # Peanuts
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx, *, param=None):  # Peanuts begins
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx, *, param=None):  # Dilbert
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Dilbertcl', 'Dilbcl', 'dilbcl'])
    async def dilbertcl(self, ctx, *, param=None):  # Dilbert classics
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def CyanideandHappinness(self, ctx, *, param=None):  # Cyanide and Happiness
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Frazz', 'fraz'])
    async def frazz(self, ctx, *, param=None):  # Frazz
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Garfieldminus', 'garfminus', 'gmng'])
    async def GmnG(self, ctx, *, param=None):  # Frazz
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Jon'])
    async def jon(self, ctx, *, param=None):  # Jon
        comic_name = 'Jon'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['frank', 'Ernest', 'ernest', 'Frank&Ernest', 'frank&ernest'])
    async def Frank(self, ctx, *, param=None):  # Frank and Ernest by Thaves
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Broom', 'broom', 'Hilda', 'hilda'])
    async def BroomHilda(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Inspector', 'inspector', 'crime', 'crimequiz'])
    async def InspectorDanger(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Inspector-Dangers-Crime-Quiz'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['emo', 'Emo', 'Cheerup', 'emokid'])
    async def Cheerupemokid(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Catana', 'littlemoments'])
    async def catana(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'little-moments-of-love'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['brevity', 'brev'])
    async def Brevity(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['catscafe', 'Cats', 'cats', 'cafe', 'cat'])
    async def CatsCafe(self, ctx, *, param=None):
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['pop', 'Pop', 'Pops', 'Popeye', 'Popeyes', 'popeye'])
    async def popeyes(self, ctx, *, param=None):
        comic_name = 'Popeyes'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    # Random comic
    @commands.command(aliases=['rand', 'rnd'])
    async def random(self, ctx, *, param=None):
        await utils.parameters_interpreter(ctx, self.get_strip_details(random.choice(
            list(self.strip_details.keys()))), param)

    # ---- END OF COMICS PARAMETERS ----#
    # --- END of functions that communicate directly with discord ----#

    def get_strip_details(self, comic_name):
        return self.strip_details[comic_name]

    # --- END of cog ----#


def setup(client):  # Initialize the cog
    client.add_cog(Comic(client))
