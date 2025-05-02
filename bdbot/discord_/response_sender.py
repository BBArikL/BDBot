import enum
from http.client import HTTPException
from typing import Union

from discord import (
    ClientException,
    Interaction,
    InteractionMessage,
    InteractionResponse,
    NotFound,
    Webhook,
)


class NextSend(enum.Enum):
    Normal = 0
    Deferred = 1
    Followup = 2


class ResponseSender:
    """Class to account for some response types"""

    def __init__(
        self,
        resp: Union[
            InteractionResponse,
            InteractionMessage,
            Webhook,
            None,
        ],
    ):
        self.resp = resp

    @classmethod
    async def from_next_send(
        cls, inter: Interaction, next_send: NextSend
    ) -> "ResponseSender":
        if next_send == NextSend.Normal:
            return cls(inter.response)
        elif next_send == NextSend.Deferred:
            return cls(await inter.original_response())
        else:
            return cls(inter.followup)

    async def send_message(self, *args, **kwargs):
        if isinstance(self.resp, InteractionMessage):
            await self.resp.edit(*args, **kwargs)
        elif isinstance(self.resp, InteractionResponse):
            await self.resp.send_message(*args, **kwargs)
        elif isinstance(self.resp, Webhook):
            await self.resp.send(*args, **kwargs)
        # If none, discard message

    @classmethod
    async def from_interaction(cls, inter: Interaction):
        try:
            await inter.original_response()
            return cls(inter.followup)
        except (HTTPException, NotFound):
            return cls(inter.response)
        except ClientException:
            return cls(None)
