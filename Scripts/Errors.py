import discord
from discord.ext import commands

class Errors(commands.Cog):
  # Class responsible for handling errors
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client
  
  @commands.Cog.listener()
  async def on_command_error(self,ctx,error):
    #Handles errors
    if isinstance(error, commands.CommandNotFound): # Command not found
     await ctx.send(f'Invalid command. Try {self.client.command_prefix}help to search for usable commands.')
    elif isinstance(error, commands.MissingRequiredArgument): # Manque d'arguments
      await ctx.send(f'A required argument is needed. Try {self.client.command_prefix}help to see required arguments.')
    elif isinstance(error, commands.MissingPermissions):
      await ctx.send('You do not have the permission to do that.')
    else: # Erreurs non supporté pour le moment
      await ctx.send('Error not supported. Visit https://github.com/BBArikL/BDBot')

def setup(client): # Initialize the cog
  client.add_cog(Errors(client))
