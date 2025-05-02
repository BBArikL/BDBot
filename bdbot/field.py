from dataclasses import dataclass


@dataclass()
class Field:
    name: str
    value: str
    inline: bool = False
