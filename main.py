import discord  # Discord libraries
import os
from keepalive import keep_alive  # imports the web server that pings the bot continually
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# client = discord.Client()  # Connects to the discord client
client = commands.Bot(command_prefix='bd!')
# discord.ext.commands.Bot(command_prefix = get_prefix, case_insensitive = True)
client.remove_command("help")  # Removes the default "help" function to replace it by our own

# END OF FUNCTIONS ON MAIN.PY
print("Starting Bot...")

keep_alive()  # Keeps the bot alive

# Loads all the cogs
for filename in os.listdir('./Scripts'):
    if filename.endswith('py'):
        client.load_extension(f'Scripts.{filename[:-3]}')

client.run(os.getenv('TOKEN'))  # Runs the bot with the private bot token
