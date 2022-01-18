import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix='bd!')
client.remove_command("help")  # Removes the default "help" function to replace it by our own

print("Starting Bot...")

# Loads all the cogs
for filename in os.listdir('./Scripts'):
    if filename.endswith('py'):
        client.load_extension(f'Scripts.{filename[:-3]}')

client.run(os.getenv('TOKEN'))  # Runs the bot with the private bot token