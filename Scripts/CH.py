import discord
from discord.ext import commands
from Scripts import Time_manager

class CH(commands.Cog):
  # Class responsible for sending XKCD comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def CH(self, ctx, *, param=None):
    if(param != None):
      if (param.split(" ")[0] == "today"):
        link = Time_manager.Time_manager.send_link_today(self, 'CalvinandHobbes')
        await ctx.send(link)
    else:  
      await ctx.send('Calvin & Hobbes! https://www.gocomics.com/calvinandhobbes')


def setup(client): # Initialize the cog
  client.add_cog(CH(client))