import discord
from discord.ext import commands

class Help(commands.Cog):
  # Class responsible for sending help embeds
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.command()
  async def help(self, ctx): # Custom Help command
    embed=discord.Embed(title="Comics!")
    embed.add_field(name="Garfield", value="-garf today OR -garf DD/MM/YYYY OR -garf random OR -garf auto")
    embed.add_field(name="Calvin & Hobbes", value="-CH today OR -CH DD/MM/YYYY OR -CH random OR -CH auto")
    embed.add_field(name="XKCD", value="-XKCD today OR -XKCD DD/MM/YYYY OR -XKCD random OR -XKCD auto")
    embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot")
    await ctx.send(embed=embed)

def setup(client): # Initialize the cog
  client.add_cog(Help(client))