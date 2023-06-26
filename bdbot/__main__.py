import asyncio
import logging
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bdbot import discord_utils, utils
from bdbot.utils import LOGS_DIRECTORY_PATH
from bdbot.Web_requests_manager import create_link_cache


def main():
    """
    Main entry point for the bot
    """
    os.chdir(os.path.dirname(__file__))  # Force the current working directory
    load_dotenv(utils.ENV_FILE)

    intents = discord.Intents.default()
    bot: discord.ext.commands.Bot = commands.Bot(
        intents=intents,
        command_prefix="bd!",
        help_command=None,
        description="BDBot now supports slash commands! Re-invite the bot with /inv!",
    )
    handler = logging.FileHandler(
        filename=os.path.join(
            LOGS_DIRECTORY_PATH,
            f"discord_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.log",
        ),
        encoding="utf-8",
        mode="w",
    )
    log_format = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    discord.utils.setup_logging(
        handler=handler,
        formatter=log_format,
        level=logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO,
        root=False,
    )
    logger = logging.getLogger("discord")

    logger.info("Writing pid file...")
    pid_file = utils.PID_FILE
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
        discord_utils.SERVER = discord.Object(
            id=int(os.getenv("PRIVATE_SERVER_SUPPORT_ID"))
        )
        logger.info("Private server set!")
    except TypeError:
        logger.info(
            "Could not set private server object, please be wary that owner commands are usable everywhere"
        )
        discord_utils.SERVER = None

    logger.info("Loading comic details...")
    utils.strip_details = utils.load_json(utils.DETAILS_PATH)
    logger.info("Loaded comic details!")

    logger.info("Loading random footers...")
    utils.random_footers = utils.get_footers()
    logger.info("Loaded random footers!")

    logger.info("Loading latest comic links...")
    if not os.path.exists(utils.COMIC_LATEST_LINKS_PATH):
        create_link_cache(logger)
    utils.link_cache = utils.load_json(utils.COMIC_LATEST_LINKS_PATH)
    utils.link_cache = utils.fill_cache(utils.strip_details, utils.link_cache)
    logger.info("Loaded comic links!")

    for filename in os.listdir("cogs"):
        if filename.endswith("py") and filename != "__init__.py":
            file_name, _ = os.path.splitext(filename)
            await bot.load_extension(f"bdbot.cogs.{file_name}")

    logger.info("Cogs successfully loaded!")

    async with bot:
        await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
