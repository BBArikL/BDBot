from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bdbot.comics import BaseComic

from bdbot.embed import Embed
from bdbot.field import Field
from bdbot.time import get_now
from bdbot.utils import get_random_footer


@dataclass()
class ComicDetail:
    title: str
    name: str
    author: str
    url: str
    date: datetime | None
    image_url: str
    sub_image_url: str | None
    alt: str
    color: int
    is_latest: bool

    @classmethod
    def from_comic(cls, comic: "BaseComic") -> "ComicDetail":
        return cls(
            title=comic.name,
            name=comic.name,
            author=comic.author,
            url=comic.website_url,
            date=get_now(),
            image_url=comic.image,
            sub_image_url=None,
            alt="",
            color=comic.color,
            is_latest=False,
        )

    def to_embed(self) -> Embed:
        embed = Embed(
            title=self.title,
            url=self.url,
            description=self.alt,
            color=self.color,
            image=self.image_url,
            thumbnail=self.sub_image_url,
            footer=get_random_footer(),
            timestamp=self.date,
        )

        if self.date:
            embed.add_field(
                Field(
                    name=f"{self.name} by {self.author}",
                    value=f"Date: {self.date.strftime('%d/%m/%Y')}",
                )
            )
        return embed

    @classmethod
    def comic_not_found(
        cls, comic_name: str | None = None, message: str | None = None
    ) -> Embed:
        title_comic_name = f" for '{comic_name}'" if comic_name else ""
        embed = Embed(title=f"No comic found{title_comic_name}!")

        message = (
            message
            if message is not None
            else "We could not find a comic at this time :thinking:...."
        )
        embed.add_field(
            Field(
                name=message,
                value="Try another time!",
            )
        )
        return embed

    @classmethod
    def comic_extraction_failed(cls, name: str, message: str):
        embed = Embed(title=f"Comic '{name}' failed to extract")

        embed.add_field(
            Field(
                name="An error occurred while extracting comic",
                value=message,
            )
        )
        embed.footer = "Report the problem at https://github.com/BBArikL/BDBot/"
        return embed
