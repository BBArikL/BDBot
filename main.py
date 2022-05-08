import os
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from src import utils

os.chdir(os.path.dirname(__file__))  # Force the current working directory
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot: discord.ext.commands.Bot = commands.Bot(intents=intents, command_prefix="bd!")
bot.remove_command("help")  # Removes the default "help" function to replace it by our own

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'src/data/logs/discord_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger.info("Starting Bot...")


async def run():
    # Loads all the cogs
    for filename in os.listdir('src/Scripts'):
        if filename.endswith('py'):
            await bot.load_extension(f'src.Scripts.{filename[:-3]}')

    logger.info("Cogs successfully loaded!")

    logger.info("Loading comic details...")
    utils.strip_details = utils.load_json(utils.DETAILS_PATH)
    logger.info("Loaded comic details!")

    logger.info("Loading random footers...")
    utils.random_footers = utils.get_footers()
    logger.info("Loaded random footers!")

    logger.info("Loading latest comic links...")
    utils.link_cache = utils.load_json(utils.COMIC_LATEST_LINKS_PATH)
    logger.info("Loaded comic links!")

    async with bot:
        await bot.start(os.getenv('TOKEN'))


asyncio.run(run())  # Runs the bot with the private bot token
