import discord
from discord import app_commands
from discord.ext import commands


class Errors(commands.Cog):
    """Class responsible for handling errors"""

    def __init__(self, bot: commands.Bot):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.bot: commands.Bot = bot

    # For debugging purposes, you can make multi-line comments around this function to clearly see the errors in the
    # terminal. But you should at least not forget to remove the comments when your bot goes live ;)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ext.commands.Context, error: Exception):
        # Handles errors
        channel = ctx.channel
        if isinstance(error, app_commands.errors.CommandNotFound):  # Command not found
            await channel.send('Invalid command. Try /help general to search for usable commands.')
        elif isinstance(error, app_commands.errors.MissingPermissions):
            await channel.send('You do not have the permission to do that.')
        elif isinstance(error, app_commands.errors.AppCommandError):
            await channel.send('The command failed. Please report this issue on Github here: '
                               f'https://github.com/BBArikL/BDBot . The error is: {error.__class__}: {error}')
        # elif isinstance(error, app_commands.errors.NotOwner):
        #    await channel.send('You do not own this bot.')
        else:  # Not supported errors
            await channel.send(f'Error not supported. Visit https://github.com/BBArikL/BDBot to report '
                               f'the issue. The error is: {error.__class__}: {error}')


async def setup(bot: commands.Bot):
    """Initialize the cog"""
    await bot.add_cog(Errors(bot))
