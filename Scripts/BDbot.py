import discord
from discord.ext import commands

class BDBot(commands.Cog):
  # Class responsible for main functions of the bot
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    # Change bot's activity
    await self.client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='-help'))

    # To be sure that the bot is ready
    print('Logged in as {0.user}'.format(self.client))

  @commands.Cog.listener()
  async def git(self, ctx): # Links back to the github page
    await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")


def setup(client): # Initialize the cog
  client.add_cog(BDBot(client))