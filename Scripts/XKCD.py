import discord
from discord.ext import commands

class XKCD(commands.Cog):
  # Class responsible for sending XKCD comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def XKCD(self, ctx, *, param=None):
    await ctx.send('XKCD! https://xkcd.com/')


def setup(client): # Initialize the cog
  client.add_cog(XKCD(client))
