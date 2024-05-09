import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from randomtimestamp import randomtimestamp

from bdbot.comics.comic_detail import ComicDetail
from bdbot.Embed import DEFAULT_FIELDS_PER_EMBED, Embed
from bdbot.field import Field
from bdbot.utils import Action, ExtendedAction, get_all_strips

FIRST_DATE_FORMAT = "%Y-%m-%d"


class Website(enum.Enum):
    Gocomics = "https://www.gocomics.com/"
    ComicsKingdom = "https://comicskingdom.com/"
    Webtoons = "https://www.webtoons.com/en/"
    Custom = ""


class WorkingType(enum.Enum):
    Date = 1
    RSS = 2
    Custom = 3


@dataclass
class BaseComic(ABC):
    WEBSITE_NAME: str
    WEBSITE_HELP: str
    WEBSITE_TYPE: Website
    WORKING_TYPE: WorkingType

    name: str
    author: str
    web_name: str
    main_website: str
    description: str
    position: int
    first_date: datetime
    color: int
    image: str
    help_text: str

    def __post_init__(self):
        # Reformat the color to hexadecimal encoding
        self.color: str
        self.color: int = int(self.color, 16)

    @property
    def website_url(self) -> str:
        return self.WEBSITE_TYPE.value + self.web_name

    @property
    def fallback_image(self) -> str:
        return self.image

    @abstractmethod
    @property
    def first_comic_date(self) -> any:
        pass

    @abstractmethod
    def get_comic(self, action: Action | ExtendedAction):
        return ComicDetail.from_comic(self, action)

    @classmethod
    def get_help_embed(
        cls, fields_per_embed: int = DEFAULT_FIELDS_PER_EMBED
    ) -> list[Embed]:
        strips = get_all_strips()
        count = 0
        embeds: list[Embed] = []

        embed = Embed(title=f"{cls.WEBSITE_NAME}!", description=None, fields=[])
        embeds.append(embed)
        for strip in strips:
            if strips[strip]["Main_website"] == cls.WEBSITE_NAME:
                count += 1

                embed.fields.append(
                    Field(name=strips[strip]["Name"], value=strips[strip]["Helptxt"])
                )
                if count == fields_per_embed:
                    count = 0
                    # Reset the embed to create a new one
                    embed = Embed(
                        title=f"{cls.WEBSITE_NAME}!", description=None, fields=[]
                    )
                    embeds.append(embed)
        return embeds


class BaseDateComic(BaseComic):
    WORKING_TYPE = WorkingType.Date

    @abstractmethod
    @property
    def first_comic_date(self) -> datetime:
        pass

    def get_random_comic_date(self) -> datetime:
        return randomtimestamp(
            start=self.first_comic_date,
            end=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        )
        # elif comic["Main_website"] == "https://dilbert.com/":
        #    middle_params = "strip"

    @abstractmethod
    @property
    def random_link(self) -> str:
        pass


class BaseRSSComic(BaseComic, ABC):
    WORKING_TYPE = WorkingType.RSS

    @abstractmethod
    @property
    def rss_url(self) -> str:
        pass

    @property
    def first_comic_date(self) -> int:
        return 1
