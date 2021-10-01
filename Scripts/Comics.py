import random
import discord
from discord.ext import commands
from Scripts import Web_requests_manager, BDbot, DailyPoster
from Comics_details import comDetails
import datetime


class Comic(commands.Cog):
    # Class responsible for sending comics

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        self.stripDetails = comDetails.load_details()

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
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield_Classics'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def CH(self, ctx, *, param=None):  # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['xkcd', 'xk'])
    async def XKCD(self, ctx, *, param=None):  # XKCD
        comic_name = 'XKCD'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx, *, param=None):  # Peanuts
        comic_name = 'Peanuts'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx, *, param=None):  # Peanuts begins
        comic_name = 'Peanuts_Begins'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx, *, param=None):  # Dilbert
        comic_name = 'Dilbert'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Dilbertcl', 'Dilbcl', 'dilbcl'])
    async def dilbertcl(self, ctx, *, param=None):  # Dilbert classics
        comic_name = 'Dilbert-Classics'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def CyanideandHappinness(self, ctx, *, param=None):  # Cyanide and Happiness
        comic_name = 'Cyanide_and_Happiness'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Frazz', 'fraz'])
    async def frazz(self, ctx, *, param=None):  # Frazz
        comic_name = 'Frazz'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Garfieldminus', 'garfminus', 'gmng'])
    async def GmnG(self, ctx, *, param=None):  # Frazz
        comic_name = 'Garfield_minus_Garfield'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Jon'])
    async def jon(self, ctx, *, param=None):  # Jon
        comic_name = 'Jon'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['frank', 'Ernest', 'ernest', 'Frank&Ernest', 'frank&ernest'])
    async def Frank(self, ctx, *, param=None):  # Frank and Ernest by Thaves
        comic_name = 'Frank-and-Ernest'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Broom', 'broom', 'Hilda', 'hilda'])
    async def BroomHilda(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'BroomHilda'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Inspector', 'inspector', 'crime', 'crimequiz'])
    async def InspectorDanger(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Inspector-Dangers-Crime-Quiz'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['emo', 'Emo', 'Cheerup', 'emokid'])
    async def Cheerupemokid(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'Cheer-up-emo-kid'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['Catana', 'littlemoments'])
    async def catana(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'little-moments-of-love'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['brevity', 'brev'])
    async def Brevity(self, ctx, *, param=None):  # Broom  Hilda
        comic_name = 'brevity'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    @commands.command(aliases=['catscafe', 'Cats', 'cats', 'cafe', 'cat'])
    async def CatsCafe(self, ctx, *, param=None):
        comic_name = 'Cats-Cafe'

        # Interprets the parameters given by the user
        await self.parameters_interpreter(ctx, self.getStripDet(comic_name), param)

    # Random comic
    @commands.command(aliases=['rand', 'rnd'])
    async def random(self, ctx, *, param=None):
        await self.parameters_interpreter(ctx,
                                          self.getStripDet(random.choice(
                                              list(self.stripDetails.keys()))), param)

    # ---- End of Comics parameters ----#

    async def send_request_error(self, ctx):
        await ctx.send('Request not understood. Try bd!help for usable commands.')

    # Sends comics info
    async def send_comic_info(self, ctx, stripDetails):
        embed = discord.Embed(title=stripDetails["Name"], url=stripDetails["Main_website"],
                              description=stripDetails["Description"], color=int(stripDetails["Color"], 16))
        embed.set_thumbnail(url=stripDetails["Image"])
        embed.add_field(name="Working type", value=stripDetails["Working_type"], inline=True)
        if stripDetails["Working_type"] == "date":
            embed.add_field(name="First apparition", value=self.get_date(stripDetails["First_date"]), inline=True)
        embed.add_field(name="Aliases", value=stripDetails["Aliases"], inline=True)

        sub_stat = ""
        if DailyPoster.DailyPosterHandler.get_sub_status(self, str(ctx.guild.id), int(stripDetails["Position"])):
            sub_stat = "Yes"
        else:
            sub_stat = "No"

        embed.add_field(name="Subscribed", value=sub_stat, inline=True)
        embed.set_footer(text="Random footer")
        embed.set_footer(text=BDbot.BDBot.get_random_footer(self))

        await ctx.send(embed=embed)

    # --- END of functions that communicate directly with discord ----

    async def parameters_interpreter(self, ctx, stripDetails, param=None):
        print(stripDetails['Name'])
        # Interprets the parameters given by the user
        if param is not None:
            """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send
            """

            if param.lower().find("today") != -1:
                # Sends the website of today's comic
                await self.comic_send(ctx, stripDetails, "today")
            elif param.lower().find("random") != -1:
                # Random comic
                await self.comic_send(ctx, stripDetails, "random")
            elif param.lower().find("add") != -1:
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPoster.DailyPosterHandler.new_change(self, ctx, stripDetails, "add")
                    await BDbot.BDBot.send_any(self, ctx, "Daily comic added successfully!")
                else:
                    await BDbot.BDBot.send_any(self, ctx, "You need `manage_guild` permission to do that!")
            elif param.lower().find("remove") != -1:
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPoster.DailyPosterHandler.new_change(self, ctx, stripDetails, "remove")
                    await BDbot.BDBot.send_any(self, ctx, "Daily comic removed successfully!")
                else:
                    await BDbot.BDBot.send_any(self, ctx, "You need `manage_guild` permission to do that!")
            else:
                # Tries to parse date / numbe of comic
                if stripDetails["Main_website"] == "https://www.gocomics.com/" or \
                        stripDetails["Main_website"] == 'https://garfieldminusgarfield.net/':
                    # Works by date
                    try:
                        comic_date = datetime.datetime.strptime(param, "%d/%m/%Y")
                        first_date = datetime.datetime.strptime(stripDetails["First_date"], "%Y, %m, %d")
                        if first_date <= comic_date <= datetime.datetime.utcnow():
                            await self.comic_send(ctx, stripDetails, "Specific_date", comic_date=comic_date)
                        else:
                            first_date_formatted = datetime.datetime.strftime(first_date, "%d/%m/%Y")
                            date_now_formatted = datetime.datetime.strftime(datetime.datetime.utcnow(), "%d/%m/%Y")
                            await BDbot.BDBot.send_any(self, ctx,
                                                       f"Invalid date. Try sending a date between "
                                                       f"{first_date_formatted} and {date_now_formatted}.")
                    except ValueError:
                        await BDbot.BDBot.send_any(self, ctx,
                                                   "This is not a valid date format! The format is : DD/MM/YYYY.")
                else:
                    # Works by number of comic
                    try:
                        number = int(param.split(" ")[0])
                        if number >= int(stripDetails["First_date"]):
                            stripDetails["Main_website"] = stripDetails["Main_website"] + str(number) + '/'
                            await self.comic_send(ctx, stripDetails, param=param)
                        else:
                            await BDbot.BDBot.send_any(self, ctx, "There is no comics with such values!")

                    except ValueError:
                        await ctx.send('This is not a valid date / comic number!')
        else:
            # If the user didn't send any parameters, return the main website of the comic requested
            await self.send_comic_info(ctx, stripDetails)

    async def comic_send(self, ctx, stripDetails, param, comic_date=None):
        # Posts the strip (with the given parameters)
        if stripDetails["Working_type"] == 'date':
            # Specific manager for date comics website
            comic_details = Web_requests_manager.ComicsRequestsManager.Comic_info_date(self, stripDetails, param=param,
                                                                                       comic_date=comic_date)
        elif stripDetails["Working_type"] == 'rss':
            comic_details = Web_requests_manager.ComicsRequestsManager.Comic_info_rss(self, stripDetails,
                                                                                      param=param,
                                                                                      comic_date=comic_date)
        else:  # Other websites
            comic_details = Web_requests_manager.ComicsRequestsManager.Comic_info_number(self, stripDetails,
                                                                                         param=param)

        # Sends the comic
        await BDbot.BDBot.send_comic_embed(self, ctx, comic_details)

    def getStripDet(self, comic_name):
        return self.stripDetails[comic_name]

    def get_date(self, date):
        return datetime.datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")

    # --- END of cog ----#


def setup(client):  # Initialize the cog
    client.add_cog(Comic(client))
