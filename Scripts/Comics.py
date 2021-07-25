from discord.ext import commands
from Scripts import Web_requests_manager, BDbot, DailyPoster
import datetime


class Comic(commands.Cog):
    # Class responsible for sending comics

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client

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
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(1978, 6, 19)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['GarfieldClassics', 'GarfClassic', 'garfieldclass', 'GarfCl'])
    async def garfcl(self, ctx, *, param=None):  # Garfield
        comic_name = 'Garfield-Classics'
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(2016, 6, 20)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
    async def CH(self, ctx, *, param=None):  # Calvin and Hobbes
        comic_name = 'CalvinandHobbes'
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(1985, 11, 18)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['xkcd', 'xk'])
    async def XKCD(self, ctx, *, param=None):  # XKCD
        comic_name = 'XKCD'
        main_website = 'https://xkcd.com/'
        first_date = 1

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['Peanuts', 'peanut', 'pean'])
    async def peanuts(self, ctx, *, param=None):  # Garfield
        comic_name = 'Peanuts'
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(1950, 10, 2)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['PeanutsBegins', 'peanutbegin', 'peanutsbegin', 'peanbeg'])
    async def peanutsbegins(self, ctx, *, param=None):  # Garfield
        comic_name = 'Peanuts-Begins'
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(1950, 10, 2)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)

    @commands.command(aliases=['Dilbert', 'Dilb', 'dilb'])
    async def dilbert(self, ctx, *, param=None):  # Garfield
        comic_name = 'dilbert-classics'
        main_website = 'https://www.gocomics.com/'
        first_date = datetime.datetime(2012, 6, 13)

        # Interprets the parmeters given by the user
        await self.parameters_interpreter(ctx, comic_name, main_website, param, first_date)
        
    @commands.command(aliases=['Cyanide', 'cyanide', 'Cyanide&Happiness', 'cyan'])
    async def CyanideandHappinness(self, ctx, *, param=None): # XKCD
      comic_name = 'Cyanide and Happiness'
      main_website = 'https://explosm.net/comics/'
      first_date = 1

      # Interprets the parmeters given by the user
      await self.parameters_interpreter(ctx,comic_name,main_website,param, first_date)

    # ---- End of Comics parameters ----#

    async def send_request_error(self, ctx):
        await ctx.send('Request not understood. Try bd!help for usable commands.')

    async def send_comic_website(self, ctx, comic_name, main_website):
        if main_website == 'https://www.gocomics.com/':
            # GoComics pages : https://www.gocomics.com/name-of-comic/
            await ctx.send(f'{comic_name}! {main_website}{comic_name.lower()}/')

        else:  # Other websites that doesnt have the same layout for pages
            await ctx.send(f'{comic_name}! {main_website}')

    # --- END of functions that communicate directly with discord ----

    async def parameters_interpreter(self, ctx, comic_name, main_website, param=None, first_date=None):
        # Interprets the parameters given by the user
        if param is not None:
            """ Parameters:
            today -> Today's comic
            add -> Add the comic to the daily posting list
            remove -> remove the comic to the daily posting list
            random -> Choose a random comic to send (Only works with XKCD for now)
            """

            if param.lower().find("today") != -1:
                # Sends the website of today's comic
                await self.comic_send(ctx, comic_name, main_website, "today")
            elif param.lower().find("random") != -1:
                # Random comic
                await self.comic_send(ctx, comic_name, main_website, "random")
            elif param.lower().find("add") != -1:
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPoster.DailyPoster.new_change(self, ctx, comic_name, "add")
                    await BDbot.BDBot.send_any(self, ctx, "Daily comic added successfully!")
                else:
                    await BDbot.BDBot.send_any(self, ctx, "You need `manage_guild` permission to do that!")
            elif param.lower().find("remove") != -1:
                if ctx.message.author.guild_permissions.manage_guild:
                    DailyPoster.DailyPoster.new_change(self, ctx, comic_name, "remove")
                    await BDbot.BDBot.send_any(self, ctx, "Daily comic removed successfully!")
                else:
                    await BDbot.BDBot.send_any(self, ctx, "You need `manage_guild` permission to do that!")
            else:
                # Tries to parse date / numbe rof comic
                if main_website == "https://www.gocomics.com/":
                    # Works by date
                    try:
                        comic_date = datetime.datetime.strptime(param, "%d/%m/%Y")

                        if first_date < comic_date < datetime.datetime.utcnow():
                            await self.comic_send(ctx, comic_name, main_website, "Specific_date", comic_date=comic_date)
                        else:
                            first_date_formatted = datetime.datetime.strftime(first_date, "%d/%m/%Y")
                            date_now_formatted = datetime.datetime.strftime(datetime.datetime.utcnow(), "%d/%m/%Y")
                            await BDbot.BDBot.send_any(self, ctx,
                                                       f"Invalid date. Try sending a date between "
                                                       f"{first_date_formatted} and {date_now_formatted}.")
                    except ValueError:
                        await BDbot.BDBot.send_any(self, ctx,
                                                   "This is not a valid date format! The format is : dd/mm/YYYY.")
                else:
                  # Works by number of comic
                    try:
                        number = int(param.split(" ")[0])
                        if number >= first_date:
                            main_website = main_website + str(number) + '/'
                            await self.comic_send(ctx, comic_name, main_website, param=param)
                        else:
                            await BDbot.BDBot.send_any(self, ctx, "There is no comics with such values!")

                    except ValueError:
                        await ctx.send('This is not a valid date / comic number!')
        else:
            # If the user didn't send any parameters, return the main website of the comic requested
            await self.send_comic_website(ctx, comic_name, main_website)

    async def comic_send(self, ctx, comic_name, main_website, param, comic_date=None):
        # Posts the strip (with the given parameters)
        if main_website == 'https://www.gocomics.com/':
            # Specific manager for GoComics website
            comic_details = Web_requests_manager.GoComicsManager.Comic_info(self, comic_name, param=param,
                                                                            comic_date=comic_date)

        else:  # Other websites
            comic_details = Web_requests_manager.OtherSiteManager.Comic_info(self, comic_name, main_website,
                                                                             param=param)

        # Sends the comic
        await BDbot.BDBot.send_comic_embed(self, ctx, comic_details)

    # --- END of cog ----#

def setup(client):  # Initialize the cog
    client.add_cog(Comic(client))
