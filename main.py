import os
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from src import utils


def main():
    """
    Main entry point for the bot
    """
    os.chdir(os.path.dirname(__file__))  # Force the current working directory
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    bot: discord.ext.commands.Bot = commands.Bot(intents=intents, command_prefix="bd!")
    bot.remove_command("help")  # Removes the default "help" function to replace it by our own

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG if os.getenv('DEBUG') == "True" else logging.INFO)
    handler = logging.FileHandler(filename=f'src/data/logs/discord_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.log',
                                  encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    logger.info("Writing pid file...")
    pid_file = "bdbot.pid"
    try:
        utils.write_pid(pid_file)
        logger.info(f"Wrote pid to file {pid_file}")
    except OSError:
        logger.info(f"Could not write to pid file {pid_file}")

    logger.info("Starting Bot...")

    asyncio.run(run(bot, logger))  # Runs the bot with the private bot token


async def run(bot: commands.Bot, logger: logging.Logger):
    """Loads all the cogs and start the bot

    :param bot: The bot
    :param logger: The logging object
    """
    logger.info("Setting up private server object")
    try:
        utils.SERVER = discord.Object(id=os.getenv("PRIVATE_SERVER_SUPPORT_ID"))
        logger.info("Private server set!")
    except TypeError:
        logger.info("Could not set private server object, please be wary that owner commands are usable everywhere")
        utils.SERVER = None

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

if __name__ == "__main__":
    main()
