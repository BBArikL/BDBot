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
    embed=discord.Embed(title="BDBot!")
    
    embed.add_field(name="Garfield", value="Aliases: 'garf', 'garfield','Garf'\nCommands:\n*garf today")
    embed.add_field(name="Calvin & Hobbes", value="Aliases: 'CalvinandHobbes', 'C&H', 'c&h', 'ch'\nCommands:\n*CH today")
    embed.add_field(name="XKCD", value="Aliases: 'xkcd', 'xk'\nCommands:\n*XKCD today\n*XKCD random")

    embed.add_field(name="Git", value="Link back to the git page\nCommand:\n*git")
    embed.add_field(name="Git", value="Gives a link to add the bot to your servers\nCommand:\n*invite")
    
    embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot")
    await ctx.send(embed=embed)

def setup(client): # Initialize the cog
  client.add_cog(Help(client))