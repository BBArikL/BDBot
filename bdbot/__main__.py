import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bdbot import cache, utils
from bdbot.cache import create_link_cache, fill_cache
from bdbot.comics import initialize_comics
from bdbot.discord_ import discord_utils
from bdbot.files import (
    COMIC_LATEST_LINKS_PATH,
    DETAILS_PATH,
    ENV_FILE,
    LOGS_DIRECTORY_PATH,
    PID_FILE,
    get_footers,
    load_json,
    write_pid,
)
from bdbot.time import get_now


def main():
    """
    Main entry point for the bot
    """
    os.chdir(os.path.dirname(__file__))  # Force the current working directory
    load_dotenv(ENV_FILE)

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
            f"discord_{get_now().strftime('%Y_%m_%d_%H_%M')}.log",
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
    try:
        write_pid(PID_FILE)
        logger.info(f"Wrote pid to file {PID_FILE}")
    except OSError:
        logger.info(f"Could not write to pid file {PID_FILE}")

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
        logger.warning(
            "Could not set private server object, please be wary that owner commands are usable everywhere"
        )
        discord_utils.SERVER = None

    logger.info("Loading comic details...")
    utils.strip_details = initialize_comics(load_json(DETAILS_PATH))
    logger.info("Loaded comic details!")

    logger.info("Loading random footers...")
    utils.random_footers = get_footers()
    logger.info("Loaded random footers!")

    logger.info("Loading latest comic links...")
    if not os.path.exists(COMIC_LATEST_LINKS_PATH):
        await create_link_cache(logger)
    utils.link_cache = load_json(COMIC_LATEST_LINKS_PATH)
    cache.link_cache = fill_cache(utils.strip_details, cache.link_cache)
    logger.info("Loaded comic links!")

    for filename in os.listdir("discord_/cogs"):
        if filename.endswith("py") and filename != "__init__.py":
            file_name, _ = os.path.splitext(filename)
            await bot.load_extension(f"bdbot.discord_.cogs.{file_name}")

    logger.info("Cogs successfully loaded!")

    async with bot:
        await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
