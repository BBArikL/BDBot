import discord
from discord.ext import commands

class Garfield(commands.Cog):
  # Class responsible for sending Garfield comics
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def garf(self, ctx, *, param=None):
    await ctx.send('Garfield! https://www.gocomics.com/garfield')


def setup(client): # Initialize the cog
  client.add_cog(Garfield(client))
