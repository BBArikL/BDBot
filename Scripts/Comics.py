import sys

sys.path.insert(0, "./Scripts/")
import random
import discord
from discord.ext import commands
from DailyPoster import DailyPosterHandler
from Comics_details import comDetails
import datetime
import utils
import Web_requests_manager


class Comic(commands.Cog):
    # Class responsible for sending comics

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.strip_details = comDetails.load_details()

    # TODO REDO DOCUMENTATION TO EXPLAIN HOW TO ADD A COMIC
    # --- Start of functions PS: (If you want to add another comic, add it here between this and the 'END of comics
    # parameters'). Preferably, Gocomics comics are the easiest to implement, so try to stick with that if your
    # comic is hosted there. (Literally copy-paste the 'garf' command, change the name of the command and change
    # the comic_name to what it is in the GoComics url, example : https://www.gocomics.com/garfield/ --> comic_name =
    # 'Garfield'). If the comic is NOT hosted on GoComics, please open an issue on the git page (
    # https://github.com/BBArikL/BDBot). Any pull requests that wasnt approved from another site will be
    # automatically rejected and you will be asked to follow the procedure cited

    @commands.command(aliases=['Garfield', 'Garf', 'garfield'])
    async def garf(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def CH(self, ctx, *, param=None):  # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['xkcd', 'xk'])
    async def XKCD(self, ctx, *, param=None):  # XKCD
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx, *, param=None):  # Peanuts
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx, *, param=None):  # Peanuts begins
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx, *, param=None):  # Dilbert
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Dilbertcl', 'Dilbcl', 'dilbcl'])
    async def dilbertcl(self, ctx, *, param=None):  # Dilbert classics
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def CyanideandHappinness(self, ctx, *, param=None):  # Cyanide and Happiness
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Frazz', 'fraz'])
    async def frazz(self, ctx, *, param=None):  # Frazz
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Garfieldminus', 'garfminus', 'gmng'])
    async def GmnG(self, ctx, *, param=None):  # Frazz
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Jon'])
    async def jon(self, ctx, *, param=None):  # Jon
        comic_name = 'Jon'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['frank', 'Ernest', 'ernest', 'Frank&Ernest', 'frank&ernest'])
    async def Frank(self, ctx, *, param=None):  # Frank and Ernest by Thaves
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Broom', 'broom', 'Hilda', 'hilda'])
    async def BroomHilda(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Inspector', 'inspector', 'crime', 'crimequiz'])
    async def InspectorDanger(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Inspector-Dangers-Crime-Quiz'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['emo', 'Emo', 'Cheerup', 'emokid'])
    async def Cheerupemokid(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['Catana', 'littlemoments'])
    async def catana(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'little-moments-of-love'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['brevity', 'brev'])
    async def Brevity(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    @commands.command(aliases=['catscafe', 'Cats', 'cats', 'cafe', 'cat'])
    async def CatsCafe(self, ctx, *, param=None):
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.get_strip_details(comic_name), param)

    # Random comic
    @commands.command(aliases=['rand', 'rnd'])
    async def random(self, ctx, *, param=None):
        await self.parameters_interpreter(ctx, self.get_strip_details(random.choice(
            list(self.strip_details.keys()))), param)

    # ---- End of Comics parameters ----#
    # Sends comics info in a embed
    async def send_comic_info(self, ctx, strip_details):
        embed = discord.Embed(title=strip_details["Name"], url=strip_details["Main_website"],
                              description=strip_details["Description"], color=int(strip_details["Color"], 16))
        embed.set_thumbnail(url=strip_details["Image"])
        embed.add_field(name="Working type", value=strip_details["Working_type"], inline=True)

        if strip_details["Working_type"] == "date":
            embed.add_field(name="First apparition", value=utils.get_date(strip_details["First_date"]), inline=True)
        embed.add_field(name="Aliases", value=strip_details["Aliases"], inline=True)

        if utils.get_sub_status(str(ctx.guild.id), int(strip_details["Position"])):
            sub_stat = "Yes"
        else:
            sub_stat = "No"

        embed.add_field(name="Subscribed", value=sub_stat, inline=True)
        embed.set_footer(text="Random footer")
        embed.set_footer(text=utils.get_random_footer())

        await ctx.send(embed=embed)

    # --- END of functions that communicate directly with discord ----

    # Interprets the parameters given by the user
    async def parameters_interpreter(self, ctx, strip_details, param=None):
        if param is not None:
            """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send
            """
            param = param.lower()

            if param.find("today") != -1:
                # Sends the website of today's comic
                await self.comic_send(ctx, strip_details, "today")
            elif param.find("random") != -1:
                # Random comic
                await self.comic_send(ctx, strip_details, "random")
            elif param.find("add") != -1:
                # Add the comic to the daily list for a guild
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPosterHandler.new_change(self, ctx, strip_details, "add")
                    await ctx.send(f"{strip_details['Name']} added successfully as a daily comic!")
                else:
                    await ctx.send("You need `manage_guild` permission to do that!")
            elif param.find("remove") != -1:
                # Remove the comic to the daily list for a guild
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPosterHandler.new_change(self, ctx, strip_details, "remove")
                    await ctx.send(f"{strip_details['Name']} removed successfully from the daily list!")
                else:
                    await ctx.send("You need `manage_guild` permission to do that!")
            else:
                # Tries to parse date / number of comic
                working_type = strip_details["Working_type"]
                if working_type != "number":
                    # Works by date
                    try:
                        comic_date = datetime.datetime.strptime(param, "%d/%m/%Y")
                        first_date = datetime.datetime.strptime(strip_details["First_date"], "%Y, %m, %d")
                        if first_date <= comic_date <= datetime.datetime.utcnow():
                            await self.comic_send(ctx, strip_details, "Specific_date", comic_date=comic_date)
                        else:
                            first_date_formatted = datetime.datetime.strftime(first_date, "%d/%m/%Y")
                            date_now_formatted = datetime.datetime.strftime(datetime.datetime.utcnow(), "%d/%m/%Y")
                            await ctx.send(
                                f"Invalid date. Try sending a date between {first_date_formatted} and "
                                f"{date_now_formatted}.")
                    except ValueError:
                        await ctx.send("This is not a valid date format! The format is : DD/MM/YYYY.")
                else:
                    # Works by number of comic
                    try:
                        number = int(param.split(" ")[0])
                        if number >= int(strip_details["First_date"]):
                            strip_details["Main_website"] = strip_details["Main_website"] + str(number) + '/'
                            await self.comic_send(ctx, strip_details, param=param)
                        else:
                            await ctx.send("There is no comics with such values!")

                    except ValueError:
                        await ctx.send('This is not a valid comic number!')
        else:
            # If the user didn't send any parameters, return informations the comic requested
            await self.send_comic_info(ctx, strip_details)

    # Post the strip (with the given parameters)
    async def comic_send(self, ctx, strip_details, param, comic_date=None):
        comic_details = Web_requests_manager.get_new_comic_details(strip_details, param, comic_date=comic_date)

        # Sends the comic
        await utils.send_comic_embed(ctx, comic_details)

    def get_strip_details(self, comic_name):
        return self.strip_details[comic_name]

    # --- END of cog ----#


def setup(client):  # Initialize the cog
    client.add_cog(Comic(client))
