from dataclasses import dataclass
from datetime import datetime, timezone

from bdbot.comics.base import BaseComic
from bdbot.embed import Embed


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
    def from_comic(cls, comic: BaseComic) -> "ComicDetail":
        return cls(
            title=comic.name,
            name=comic.name,
            author=comic.author,
            url=comic.website_url,
            date=datetime.now(tz=timezone.utc),
            image_url=comic.image,
            sub_image_url=None,
            alt="",
            color=comic.color,
            is_latest=False,
        )

    def to_embed(self) -> Embed:
        return Embed(title=self.title)
