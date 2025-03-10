from typing import Any

from discord import ButtonStyle, Embed, Interaction, ui


class MultiPageView(ui.View):
    def __init__(self, author: int, embeds: list[Embed], timeout: float = 60):
        super().__init__(timeout=timeout)
        self.author_id = author
        self.embeds = embeds
        self.current_embed = 0

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        return interaction.user.id == self.author_id

    async def on_error(
        self,
        interaction: Interaction,
        error: Exception,
        item: ui.Item[Any],
        /,
    ) -> None:
        await interaction.followup.send(content=error)

    @ui.button(label="Last")
    async def last_embed(self, interaction: Interaction, button: ui.Button):  # noqa
        if self.current_embed > 0:
            self.current_embed -= 1

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    @ui.button(label="Next")
    async def next_embed(self, interaction: Interaction, button: ui.Button):  # noqa
        if self.current_embed < len(self.embeds) - 1:
            self.current_embed += 1

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    @ui.button(label="Exit", style=ButtonStyle.danger)
    async def exit_embed(self, interaction: Interaction, button: ui.Button):
        self.next_embed.disabled = True
        self.last_embed.disabled = True
        button.disabled = True

        await interaction.response.edit_message(
            embed=self.embeds[self.current_embed], view=self
        )

    async def on_timeout(self) -> None:
        self.clear_items()
        self.embeds = None
        self.author_id = 0
        self.current_embed = 0
