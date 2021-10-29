from discord.ext import commands


class Errors(commands.Cog):
    # Class responsible for handling errors

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client

    # For debugging purposes, you can make multi-line comments around this function to clearly see the errors in the
    # terminal. But you should at least not forget to remove the comments when your bot goes live ;)

    """@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handles errors
        if isinstance(error, commands.CommandNotFound):  # Command not found
            await ctx.send('Invalid command. Try bd!help to search for usable commands.')
        elif isinstance(error, commands.MissingRequiredArgument):  # Manque d'arguments
            await ctx.send('A required argument is needed. Try bd!help to see required arguments.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permission to do that.')
        else:  # Not supported errors
            await ctx.send(f'Error not supported. Visit https://github.com/BBArikL/BDBot to report the issue. '
                           f'The error is: {error}')"""


def setup(client):  # Initialize the cog
    client.add_cog(Errors(client))
