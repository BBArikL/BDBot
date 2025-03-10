import discord
from discord import ui

from bdbot.discord_.discord_utils import send_message
from bdbot.files import save_request


class BotRequest(ui.Modal, title="Request"):
    """Request for the bot"""

    request = ui.TextInput(label="Request")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        save_request(
            self.request.value, interaction.user.name, interaction.user.discriminator
        )
        await send_message(
            interaction, "Request saved! Thank you for using BDBot!", ephemeral=True
        )
