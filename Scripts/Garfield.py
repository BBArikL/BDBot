import discord
from discord.ext import commands
from Scripts import Time_manager

class Garfield(commands.Cog):
  # Class responsible for sending Garfield comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def garf(self, ctx, *, param=None):
    if(param != None):
      if (param.split(" ")[0] == "today"):
        link = Time_manager.Time_manager.send_link_today(self,'Garfield')
      await ctx.send(link)
    else:
      await ctx.send('Garfield! https://www.gocomics.com/garfield')


def setup(client): # Initialize the cog
  client.add_cog(Garfield(client))