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
    def from_dict(cls, obj: dict[str, dict[str, str]]) -> "Embed":
        embed = cls(**obj)
        # Need to put in a different list because it will try to loop
        # over itself infinitely because of shared references
        fields = []
        for f in obj["fields"]:
            fields.append(Field(**f))
        embed.fields = fields
        return embed
