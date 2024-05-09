import discord
from discord import ui

from bdbot import utils
from bdbot.discord_utils import send_message


class BotRequest(ui.Modal, title="Request"):
    """Request for the bot"""

    request = ui.TextInput(label="Request")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        utils.save_request(
            self.request.value, interaction.user.name, interaction.user.discriminator
        )
        await send_message(
            interaction, "Request saved! Thank you for using BDBot!", ephemeral=True
        )
