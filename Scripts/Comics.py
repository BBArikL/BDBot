import discord
from discord.ext import commands, tasks
from Scripts import Web_requests_manager,BDbot
import random

class Comic(commands.Cog):
  # Class responsible for sending comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  #--- Start of functions PS: (If you want to add another comic, add it here between this and the 'END of comics parameters')
  #---- Preferably, Gocomics comics are the easiest to implement, so try to stick with that if your comic is hosted there 
  #---- (Literally copy-paste the 'garf' command, change the name of the command and change the comic_name to what it is in the GoComics url, example : https://www.gocomics.com/garfield/ --> comic_name = 'Garfield').  
  #---- If the comic is NOT hosted on GoComics, please open an issue on the git page (https://github.com/BBArikL/BDBot). 
  #---- Any pull requests that wasnt approved from another site will be automatically rejected and you will be asked to follow the procedure cited ----#
  @commands.command(aliases=['CalvinandHobbes', 'C&H', 'c&h', 'ch'])
  async def CH(self, ctx, *, param=None): # Calvin and Hobbes
    comic_name = 'CalvinandHobbes'
    main_website = 'https://www.gocomics.com/'

    # Interprets the parmeters given by the user
    await self.parameters_interpreter(ctx,comic_name,main_website,param)

  @commands.command(aliases=['Garfield', 'Garf', 'garfield'])
  async def garf(self, ctx, *, param=None): # Garfield
    comic_name = 'Garfield'
    main_website = 'https://www.gocomics.com/'

    # Interprets the parmeters given by the user
    await self.parameters_interpreter(ctx,comic_name,main_website,param)

  @commands.command(aliases=['xkcd', 'xk'])
  async def XKCD(self, ctx, *, param=None): # XKCD
    comic_name = 'XKCD'
    main_website = 'https://xkcd.com/'

    # Interprets the parmeters given by the user
    await self.parameters_interpreter(ctx,comic_name,main_website,param)

  # ---- End of Comics parameters ----#

  async def send_request_error(self, ctx):
    await ctx.send('Request not understood.')

  async def send_comic_website(self, ctx,comic_name,main_website):
    if(main_website == 'https://www.gocomics.com/'):
      # GoComics pages : https://www.gocomics.com/name-of-comic/
      await ctx.send(f'{comic_name}! {main_website}{comic_name.lower()}/')

    else: # Other websites that doesnt have the same layout for pages
      await ctx.send(f'{comic_name}! {main_website}')

  #--- END of functions that communicate directly with discord ----

  async def parameters_interpreter(self,ctx,comic_name,main_website, param=None): 
    # Interprets the parameters given by the user
    if(param != None):
      """ Parameters:
      today -> Today's comic
      daily -> Start a loop for the bot to send the comic each day
      stop -> Stops the bot from sending comics each day
      random -> Choose a random comic to send (Only works with XKCD for now)
      """
      if (param.lower().find("today") != -1):
        # Sends the website of today's comic
        await self.today(ctx,comic_name,main_website)

      elif(param.lower().find("daily") != -1):
        # Sends the comic daily
        await self.daily(ctx,comic_name,main_website)

      elif(param.lower().find("stop") != -1 and BDbot.BDBot.post_daily().is_running()):
        BDbot.BDBot.post_daily.stop() # Stops the current loop
      
      elif(param.lower().find("random") != -1 and comic_name == 'XKCD'):
        # Temporary, the bot can only send random XKCD comics
        await self.rand(ctx,comic_name, main_website)

      else: # Return a error because the parameters given doesnt work
        await self.send_request_error(ctx)
    
    else:
      # If the user didn't send any parameters, return the main website of the comic requested
      await self.send_comic_website(ctx,comic_name,main_website)

  async def today(self,ctx,comic_name,main_website):
    # Posts today's strip
    if(main_website == 'https://www.gocomics.com/'):
      # Specific manager for GoComics website
      comic_details = Web_requests_manager.GoComics_manager.Comic_info(self,comic_name)
    
    else: # Other websites
      comic_details = Web_requests_manager.Other_site_manager.Comic_info(self,comic_name, main_website)

    # Sends the comic
    await BDbot.BDBot.send_comic_embed(self, ctx, comic_details)

  async def daily(self,ctx,comic_name,main_website):
    # Posts daily strip
    BDbot.BDBot.post_daily.start(ctx,comic_name,main_website)

  async def rand(self,ctx,comic_name,main_website):
    # TODO random for GoComics comics
    nb=random.randint(0,2421) # Choose a random XKCD comic to send (TODO find a way to increment automatically the number) : *** //c.xkcd.com/random/comic/ ****
    await BDbot.BDBot.send_any(self, ctx,f'XKCD #{nb}! https://xkcd.com/{nb}/')

  #--- END of cog ----#


def setup(client): # Initialize the cog
  client.add_cog(Comic(client))