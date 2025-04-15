from discord import Interaction
from discord.app_commands import (
    AppCommandError,
    CheckFailure,
    CommandNotFound,
    MissingPermissions,
)

from bdbot.discord_.discord_utils import logger
from bdbot.discord_.response_sender import ResponseSender
from bdbot.exceptions import ComicNotFound


async def on_error(inter: Interaction, error: AppCommandError):
    """

    :param inter:
    :param error:
    :return:
    """
    # Handles errors
    logger.error(f"Handling exception in commands:\n{error.__class__.__name__}:{error}")
    responder = await ResponseSender.from_interaction(inter)

    if isinstance(error, ComicNotFound):
        return await responder.send_message(
            error.message,
            ephemeral=True,
        )
    if isinstance(error, CommandNotFound):  # Command not found
        return await responder.send_message(
            "Invalid command. Try /help general to search for usable commands.",
            ephemeral=True,
        )
    if isinstance(error, MissingPermissions):
        return await responder.send_message(
            "You do not have the permission to do that!", ephemeral=True
        )
    if isinstance(error, CheckFailure):
        return await responder.send_message(
            "One or more checks did not pass... Maybe you need more permissions to run this command!",
            ephemeral=True,
        )
    if isinstance(error, AppCommandError):
        return await responder.send_message(
            "The command failed. Please report this issue on Github here: "
            f"https://github.com/BBArikL/BDBot . The error is: {error.__class__.__name__}: {error.__str__()[:500]}",
            ephemeral=True,
        )
    # Not supported errors
    await responder.send_message(
        f"Error not supported. Visit https://github.com/BBArikL/BDBot to report "
        f"the issue. The error is: {error.__class__.__name__}: {error.__str__()[:500]}",
        ephemeral=True,
    )
