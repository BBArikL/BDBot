import discord
from discord.ext import commands
import random

class XKCD(commands.Cog):
  # Class responsible for sending XKCD comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def XKCD(self, ctx, *, param=None):
    if(param != None):
      if((param.split(" ")[0]) == "today"):
        # Takes the last comic number and add it to the link
        await ctx.send('XKCD today! https://xkcd.com/')
    
      elif ((param.split(" ")[0]) == "random"):
        nb=random.randint(0,2421) # Choose a random XKCD comic
        await ctx.send(f'XKCD #{nb}! https://xkcd.com/{nb}/')
    
    else: # Links to the main website
      await ctx.send('XKCD! https://xkcd.com/')


def setup(client): # Initialize the cog
  client.add_cog(XKCD(client))