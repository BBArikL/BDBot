import discord
from discord.ext import commands

class Help(commands.Cog):
  # Class responsible for sending help embeds
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.group(invoke_without_command=True, case_insensitive = True)
  async def help(self, ctx): # Custom Help command
    embed=discord.Embed(title="BDBot!")
    
    embed.add_field(name="Gocomics", value="Currently available: 'Garfield',\n'Garfield classics',\n'Calvin&Hobbes',\n'Peanuts', 'Peanuts Begins'\nCommands:\n`bd!name-of-comic today / random / dd/mm/YYY`.")
    embed.add_field(name="XKCD", value="Aliases: 'xkcd', 'xk'\nCommands:\n`bd!XKCD today / random / # of comic`.")
    #embed.add_field(name= 'Cyanide and Happiness', value="Aliases: 'Cyanide',\n'cyanide',\n'Cyanide&Happiness',\n'cyan'\nCommands:\n!cyanide today")
    embed.add_field(name="Daily comics commands.", value="Use bd!help daily to see available commands for daily comics. Post daily at 2:00 AM UTC.")

    embed.add_field(name="Git", value="Link back to the git page\nCommand:\n`bd!git`.")
    embed.add_field(name="Invite", value="Gives a link to add the bot to your servers\nCommand:\n`bd!invite`.")
    
    embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot.")
    await ctx.send(embed=embed)
  
  @help.command()
  async def daily(self, ctx): # help for daily commands
    embed=discord.Embed(title="Daily commands!")
    
    embed.add_field(name="add", value="Use `bd!<name_of_comic> add` to add the comic to the daily list.")
    embed.add_field(name="remove", value="Use `bd!<name_of_comic> remove` to remove the comic to the daily list.")
    embed.add_field(name="Remove all", value="Use `bd!remove_all` to unsubscribe your server from all the comics")
    
    embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot")
    await ctx.send(embed=embed)

def setup(client): # Initialize the cog
  client.add_cog(Help(client))