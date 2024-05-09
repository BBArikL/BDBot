from dataclasses import dataclass
from datetime import datetime

from bdbot.comics.base import BaseComic
from bdbot.Embed import Embed
from bdbot.utils import Action


@dataclass()
class ComicDetail:
    title: str
    name: str
    author: str
    url: str
    date: datetime
    image_url: str
    sub_image_url: str | None
    alt: str
    color: int
    is_latest: bool

    @classmethod
    def from_comic(cls, comic: BaseComic, action: Action) -> "ComicDetail":
        return cls(**comic)

    def to_embed(self) -> Embed:
        return Embed(title=self.title, description=None, fields=[])
