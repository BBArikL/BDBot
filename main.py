import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from src import utils

load_dotenv()

client = commands.Bot(command_prefix='bd!')
client.remove_command("help")  # Removes the default "help" function to replace it by our own

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'src/data/logs/discord_{datetime.now().strftime("%Y_%m_%d_1%H_%M")}.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger.log(logging.INFO, "Starting Bot...")

# Loads all the cogs
for filename in os.listdir('src/Scripts'):
    if filename.endswith('py'):
        client.load_extension(f'src.Scripts.{filename[:-3]}')

logger.info("Cogs successfully loaded!")

logger.info("Loading comic details...")
utils.strip_details = utils.load_json(utils.DETAILS_PATH)
logger.info("Loaded comic details!")

logger.info("Loading random footers...")
utils.random_footers = utils.get_footers()
logger.info("Loaded random footers!")

client.run(os.getenv('TOKEN'))  # Runs the bot with the private bot token
