from dataclasses import dataclass

from bdbot.field import Field

DEFAULT_FIELDS_PER_EMBED = 5


@dataclass()
class Embed:
    title: str
    description: str | None
    fields: list[Field]
