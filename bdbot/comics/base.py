import enum
import xml
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from random import randint
from typing import Any, Type

import aiohttp
from bs4 import BeautifulSoup
from randomtimestamp import randomtimestamp
from rss_parser import RSSParser
from rss_parser.models.rss import RSS

from bdbot.actions import Action
from bdbot.comics.comic_detail import ComicDetail
from bdbot.embed import DEFAULT_FIELDS_PER_EMBED, Embed
from bdbot.exceptions import ComicNotFound
from bdbot.field import Field
from bdbot.time import get_now
from bdbot.utils import comic_details


class WorkingType(enum.Enum):
    Date = "date"
    RSS = "rss"
    Number = "number"


@dataclass
class BaseComic(ABC):
    WEBSITE_NAME: str
    WEBSITE_URL: str
    WEBSITE_HELP: str
    WORKING_TYPE: WorkingType

    name: str
    author: str
    web_name: str
    main_website: str
    working_type: str
    description: str
    id: int
    first_date: datetime
    color: int
    image: str
    help: str

    _BASE_PARSER: str = "html.parser"

    def __post_init__(self):
        # Reformat the color to hexadecimal encoding
        self.color: int = int(self.color, 16)

    @property
    def website_url(self) -> str:
        return self.WEBSITE_URL + self.web_name

    @property
    def fallback_image(self) -> str:
        return self.image

    @property
    @abstractmethod
    def first_comic_date(self) -> any:
        pass

    @property
    @abstractmethod
    def first_date_format(self) -> str:
        pass

    @abstractmethod
    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        pass

    async def get_comic(
        self, action: Action, verify_latest=False, comic_date: any = None
    ) -> ComicDetail:
        return ComicDetail.from_comic(self)

    @classmethod
    def get_website_help_embed(
        cls, fields_per_embed: int = DEFAULT_FIELDS_PER_EMBED
    ) -> list[Embed]:
        """Create embeds with all the specific comics from a website

        :return: The list of embeds
        """
        count = 0
        embeds: list[Embed] = []

        title = cls.WEBSITE_NAME + "!"
        embed = Embed(title)
        embeds.append(embed)
        for comic in comic_details.values():
            if comic.__class__ == cls:
                if count == fields_per_embed:
                    count = 0
                    # Reset the embed to create a new one
                    embed = Embed(title)
                    embeds.append(embed)

                count += 1

                embed.fields.append(Field(name=comic.name, value=comic.help))

        return embeds

    def get_comic_info(self, is_subbed: bool) -> Embed:
        """Sends comics info in an embed

        :param is_subbed: If the server is subbed
        :return: The comic info
        """
        embed: Embed = Embed(
            title=f"{self.name} by {self.author}",
            url=self.website_url,
            description=self.description,
            color=self.color,
            thumbnail=self.image,
            fields=[
                Field(name="Working type", value=self.WORKING_TYPE.value, inline=True)
            ],
        )
        if self.WORKING_TYPE == WorkingType.Date:
            embed.add_field(
                Field(name="First apparition", value=self.first_comic_date, inline=True)
            )
        embed.add_field(
            Field(name="Subscribed", value="Yes" if is_subbed else "No", inline=True)
        )
        return embed

    def to_dict(self):
        d = asdict(self)
        d.pop("WEBSITE_NAME")
        d.pop("WEBSITE_URL")
        d.pop("WEBSITE_HELP")
        d.pop("WORKING_TYPE")
        d.pop("_BASE_PARSER")
        d["first_date"] = self.first_date_format
        d["color"] = hex(self.color).upper()[2:]
        return d

    def extract_meta_content(
        self, soup: BeautifulSoup, content_name: str
    ) -> str | None:
        """Extract the content from the source

        Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py

        :param soup: The HTML source parsed
        :param content_name: The name of the content that we are searching for
        :return: The extracted content or None if it did not find it
        """
        content_meta = soup.find(
            "meta", attrs={"property": f"og:{content_name}", "content": True}
        )
        if content_meta is not None:
            # If it finds the meta properties of the image
            return content_meta["content"]
        return None

    @staticmethod
    async def read_url_content(url: str) -> str:
        content: str
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        return content

    @classmethod
    def get_type(
        cls, main_website: str, working_type: WorkingType
    ) -> Type["BaseComic"]:
        match working_type:
            case WorkingType.Date:
                return BaseDateComic.from_main_website(main_website)
            case WorkingType.Number:
                return BaseNumberComic.from_main_website(main_website)
            case WorkingType.RSS:
                return BaseRSSComic.from_main_website(main_website)
            case _:
                raise Exception("Could not find type of comic!")

    @classmethod
    def from_main_website(cls, main_website: str):
        pass


class BaseDateComic(BaseComic):
    WORKING_TYPE = WorkingType.Date
    _MAX_TRIES = 15

    @property
    @abstractmethod
    def first_comic_date(self) -> datetime:
        pass

    @property
    def first_date_format(self) -> str:
        return self.first_date.strftime("%Y-%m-%d")

    def get_random_comic_date(self) -> datetime:
        return randomtimestamp(
            start=self.first_comic_date,
            end=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        )

    @property
    @abstractmethod
    def random_link(self) -> str:
        pass

    @property
    @abstractmethod
    def url_date_format(self):
        pass

    @abstractmethod
    def get_link_from_date(self, date: datetime):
        pass

    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        pass

    async def get_comic(
        self, action: Action, verify_latest=False, comic_date: datetime | None = None
    ) -> ComicDetail:
        from bdbot.cache import check_if_latest_link

        detail = await super().get_comic(action)
        i = 0

        # Gets today date
        if comic_date is None:
            comic_date = get_now()

        while i < self._MAX_TRIES and detail.image_url == self.image:
            i += 1
            detail.date = comic_date
            detail.url = (
                self.random_link
                if action == Action.Random
                else self.get_link_from_date(comic_date)
            )

            # Get the html of the comic site
            content = await self.read_url_content(detail.url)
            soup = BeautifulSoup(content, self._BASE_PARSER)

            # Finds the url of the image
            image_url = self.extract_meta_content(soup, "image")

            if image_url is None:  # Go back one day
                comic_date = comic_date - timedelta(days=1)
                if i >= self._MAX_TRIES:
                    # If it hasn't found anything
                    raise ComicNotFound("Could not find comic!")
                continue

            # Extracts the title of the comic
            detail.title = self.extract_meta_content(soup, "title")
            # Finds the final url (if necessary)
            url = self.extract_meta_content(soup, "url")
            if url:
                detail.url = url
            detail.image_url = image_url
            detail.date = comic_date

        if action == Action.Random:
            detail.date = self.extract_date_from_url(detail.url)

        if verify_latest:
            detail.is_latest = check_if_latest_link(detail.name, detail.image_url)
        return detail

    def extract_date_from_url(self, url: str) -> datetime:
        return datetime.strptime(
            url.removeprefix(self.website_url), self.url_date_format
        )

    @classmethod
    def from_main_website(cls, main_website: str) -> Type["BaseDateComic"]:
        from bdbot.comics import ComicsKingdom, Gocomics

        match main_website:
            case Gocomics.WEBSITE_URL:
                return Gocomics
            case ComicsKingdom.WEBSITE_URL:
                return ComicsKingdom
            case _:
                raise ComicNotFound("Could not find comic type!")


class BaseRSSComic(BaseComic, ABC):
    WORKING_TYPE = WorkingType.RSS
    MAX_ENTRIES = 19

    @property
    @abstractmethod
    def rss_url(self) -> str:
        pass

    @property
    @abstractmethod
    def weekday_token(self):
        pass

    @property
    @abstractmethod
    def timezone_token(self):
        pass

    @property
    def first_comic_date(self) -> int:
        return 1

    @property
    def first_date_format(self) -> str:
        return ""

    @abstractmethod
    def get_specific_url(self, date: Any):
        pass

    def get_comic_specific_date(self, date: Any):
        pass

    def extract_content(
        self, content: str, date: int, detail: ComicDetail
    ) -> ComicDetail:
        try:
            rss: RSS = RSSParser.parse(content)
        except xml.parsers.expat.ExpatError:
            raise ComicNotFound(f"The rss feed for comic '{self.name}' was invalid!")
        feed = rss.channel.content.items[date].content

        new_date = datetime.strptime(
            feed.pub_date.content,
            f"%{self.weekday_token}, %d %b %Y %H:%M:%S %{self.timezone_token}",
        )
        detail.date = new_date

        detail.url = feed.links[0].content

        description_soup = BeautifulSoup(feed.description.content, "html.parser")
        description_images = [
            {"alt": image.get("alt", ""), "source": image.get("src")}
            for image in description_soup.findAll("img")
        ]
        if len(description_images) > 0:
            img_index = 0
            if len(description_images) > 1:
                # general check for a second image to embed
                detail.sub_image_url = description_images[img_index]["source"]
                img_index += 1
            detail.image_url = description_images[img_index]["source"]
        else:
            detail.image_url = self.fallback_image
        return detail

    async def get_comic(
        self, action: Action, verify_latest=False, comic_date: int | None = None
    ) -> ComicDetail:
        from bdbot.cache import check_if_latest_link

        detail = await super().get_comic(action)

        if action == Action.Specific_date:
            detail.image_url = self.fallback_image
            detail.url = self.get_specific_url(get_now())
            return detail

        comic_nb: int = 0
        if action == Action.Random:
            # Random comic
            comic_nb = randint(0, self.MAX_ENTRIES)

        content = await self.read_url_content(self.rss_url)

        detail = self.extract_content(content, comic_nb, detail)

        if verify_latest:
            detail.is_latest = check_if_latest_link(detail.name, detail.image_url)
        return detail

    @classmethod
    def from_main_website(cls, main_website: str) -> Type["BaseRSSComic"]:
        from bdbot.comics import GarfieldMinusGarfield, Webtoons

        match main_website:
            case Webtoons.WEBSITE_URL:
                return Webtoons
            case GarfieldMinusGarfield.WEBSITE_URL:
                return GarfieldMinusGarfield
            case _:
                raise ComicNotFound("Could not find comic type!")


class BaseNumberComic(BaseComic):
    WORKING_TYPE = WorkingType.Number

    @property
    def first_comic_date(self) -> int:
        return 1

    @property
    def first_date_format(self) -> str:
        return "1"

    async def get_comic_url(
        self, action: Action, comic_date: int | None = None
    ) -> str | None:
        return self.extract_meta_content(
            BeautifulSoup(
                await self.read_url_content(self.main_website), self._BASE_PARSER
            ),
            "url",
        )

    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        # General extractor
        soup = BeautifulSoup(content, self._BASE_PARSER)
        detail.url = self.extract_meta_content(soup, "url")
        detail.title = self.extract_meta_content(soup, "title")
        detail.image_url = self.extract_meta_content(soup, "image")
        return detail

    async def get_comic(
        self, action: Action, verify_latest=False, comic_date: int | None = None
    ) -> ComicDetail:
        from bdbot.cache import check_if_latest_link

        detail = await super().get_comic(action)
        detail.url = await self.get_comic_url(action, comic_date)
        html = await self.read_url_content(detail.url)
        detail = self.extract_content(html, 0, detail)
        if verify_latest:
            detail.is_latest = check_if_latest_link(detail.name, detail.image_url)
        return detail

    @classmethod
    def from_main_website(cls, main_website: str) -> Type["BaseNumberComic"]:
        from bdbot.comics import XKCD, CyanideAndHappiness

        match main_website:
            case CyanideAndHappiness.WEBSITE_URL:
                return CyanideAndHappiness
            case XKCD.WEBSITE_URL:
                return XKCD
            case _:
                raise ComicNotFound("Could not find comic type!")
