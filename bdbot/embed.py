from dataclasses import dataclass, field
from datetime import datetime

from bdbot.field import Field
from bdbot.utils import get_random_footer

DEFAULT_FIELDS_PER_EMBED = 5


@dataclass()
class Embed:
    title: str
    description: str = field(default="")
    url: str = field(default="")
    color: int = field(default=0)
    image: str = field(default="")
    thumbnail: str = field(default="")
    fields: list[Field] = field(default_factory=list)
    footer: str = field(default_factory=get_random_footer)
    timestamp: datetime | None = field(default=None)

    def add_field(self, f: Field):
        self.fields.append(f)

    @classmethod
    def from_dict(cls, obj: dict[str, str | int]) -> "Embed":
        embed = cls(**obj)
        for f in obj["field"]:
            embed.add_field(Field(**f))
        return embed
