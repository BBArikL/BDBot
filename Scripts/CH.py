import discord
from discord.ext import commands

class CH(commands.Cog):
  # Class responsible for sending XKCD comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def CH(self, ctx, *, param=None):
    await ctx.send('Calvin & Hobbes! https://www.gocomics.com/calvinandhobbes')


def setup(client): # Initialize the cog
  client.add_cog(CH(client))
