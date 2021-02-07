import discord #Discord libraries
import os
from keepalive import keep_alive # imports the web server that pings the bot continually
from discord.ext import commands

client = discord.Client() # Connects to the discord client
client = commands.Bot(command_prefix = '-')
#discord.ext.commands.Bot(command_prefix = get_prefix, case_insensitive = True)
client.remove_command("help") # Removes the default "help" function to replace it pby our own

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='-help'))

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
  #Handles errors
  if isinstance(error, commands.CommandNotFound): # Command not found
    await ctx.send(f'Invalid command. Try {client.command_prefix}help to search for usable commands.')
  elif isinstance(error, commands.MissingRequiredArgument): # Manque d'arguments
    await ctx.send(f'A required argument is needed. Try {client.command_prefix}help to see required arguments.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the permission to do that.')
  else: # Erreurs non supporté pour le moment
    await ctx.send('Error not supported. Visit https://github.com/BBArikL/BDBot')

@client.group(invoke_without_command=True, case_insensitive = True)
async def help(ctx): # Custom Help command
  embed=discord.Embed(title="Comics!")
  embed.add_field(name="Garfield", value="-garf today OR -garf DD/MM/YYYY OR -garf random OR -garf auto")
  embed.add_field(name="Calvin & Hobbes", value="-CH today OR -CH DD/MM/YYYY OR -CH random OR -CH auto")
  embed.add_field(name="XKCD", value="-XKCD today OR -XKCD DD/MM/YYYY OR -XKCD random OR -XKCD auto")
  embed.set_footer(text="Check the bot here: https://github.com/BBArikL/BDBot")
  await ctx.send(embed=embed)

@client.command()
async def garf(ctx, *, param=None): # Garfield Strips
  await ctx.send('Garfield! https://www.gocomics.com/garfield')

@client.command()
async def CH(ctx, *, param=None): # C&H Strips
  await ctx.send('Calvin & Hobbes! https://www.gocomics.com/calvinandhobbes')

@client.command()
async def XKCD(ctx, *, param=None):
  await ctx.send('XKCD! https://xkcd.com/')

@client.command()
async def git(ctx): # Links back to the github page
  await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")

keep_alive() # Keeps the bot alive

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token