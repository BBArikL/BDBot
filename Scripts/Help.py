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
    
    embed.add_field(name="Gocomics", value="Currently available: 'Garfield',\n'Garfield classics',\n'Calvin&Hobbes',\n'Peanuts', 'Peanuts Begins'\nCommands:\nbd!name-of-comic today / random>")
    embed.add_field(name="XKCD", value="Aliases: 'xkcd', 'xk'\nCommands:\nbd!XKCD today / random")
    #embed.add_field(name= 'Cyanide and Happiness', value="Aliases: 'Cyanide',\n'cyanide',\n'Cyanide&Happiness',\n'cyan'\nCommands:\n!cyanide today")
  
    embed.add_field(name="Git", value="Link back to the git page\nCommand:\nbd!git")
    embed.add_field(name="Invite", value="Gives a link to add the bot to your servers\nCommand:\nbd!invite")
    
    embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot")
    await ctx.send(embed=embed)

def setup(client): # Initialize the cog
  client.add_cog(Help(client))