from dataclasses import dataclass, field

from bdbot.field import Field
from bdbot.utils import get_random_footer

DEFAULT_FIELDS_PER_EMBED = 5


@dataclass()
class Embed:
    title: str
    description: str = field(default="")
    url: str = field(default="")
    color: int = field(default=0)
    thumbnails: list[str] = field(default_factory=list)
    fields: list[Field] = field(default_factory=list)
    footer: str = field(default_factory=get_random_footer)

    def add_field(self, f: Field):
        self.fields.append(f)
