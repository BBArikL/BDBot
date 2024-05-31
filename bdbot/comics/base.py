import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from random import randint
from typing import Any

import aiohttp
from bs4 import BeautifulSoup
from randomtimestamp import randomtimestamp
from rss_parser import RSSParser
from rss_parser.models.rss import RSS

from bdbot.actions import Action
from bdbot.cache import check_if_latest_link
from bdbot.comics.comic_detail import ComicDetail
from bdbot.embed import DEFAULT_FIELDS_PER_EMBED, Embed
from bdbot.exceptions import ComicNotFound
from bdbot.field import Field
from bdbot.time import get_now
from bdbot.utils import get_all_strips

FIRST_DATE_FORMAT = "%Y-%m-%d"


class Website(enum.Enum):
    Gocomics = "https://www.gocomics.com/"
    ComicsKingdom = "https://comicskingdom.com/"
    Webtoons = "https://www.webtoons.com/en/"
    Custom = ""


class WorkingType(enum.Enum):
    Date = "Date"
    RSS = "RSS"
    Number = "Number"
    Custom = "Custom"


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

    _BASE_PARSER: str = "html.parser"

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
    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        pass

    async def get_comic(self, action: Action, verify_latest=False) -> ComicDetail:
        return ComicDetail.from_comic(self)

    @classmethod
    def get_website_help_embed(
        cls, fields_per_embed: int = DEFAULT_FIELDS_PER_EMBED
    ) -> list[Embed]:
        """Create embeds with all the specific comics from a website

        :return: The list of embeds
        """
        strips = get_all_strips()
        count = 0
        embeds: list[Embed] = []

        title = f"{cls.WEBSITE_NAME}!"
        embed = Embed(title)
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
                    embeds.append(Embed(title))
        return embeds

    def get_comic_info(self, is_subbed: bool) -> Embed:
        """Sends comics info in an embed

        :param is_subbed:
        :return:
        """
        embed: Embed = Embed(
            title=f"{self.name} by {self.author}",
            url=self.website_url,
            description=self.description,
            color=self.color,
            thumbnail=self.image,
            fields=[
                Field(name="Working type", value=self.WEBSITE_TYPE.value, inline=True)
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

    @staticmethod
    def extract_meta_content(soup: BeautifulSoup, content_name: str) -> str | None:
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


class BaseDateComic(BaseComic):
    WORKING_TYPE = WorkingType.Date
    _MAX_TRIES = 15

    @abstractmethod
    @property
    def first_comic_date(self) -> datetime:
        pass

    def get_random_comic_date(self) -> datetime:
        return randomtimestamp(
            start=self.first_comic_date,
            end=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        )

    @abstractmethod
    @property
    def random_link(self) -> str:
        pass

    @abstractmethod
    @property
    def url_date_format(self):
        pass

    @abstractmethod
    def get_link_from_date(self, date: datetime):
        pass

    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        pass

    async def get_comic(self, action: Action, verify_latest=False) -> ComicDetail:
        detail = await super().get_comic(action)
        i = 0

        # if comic_date is None:
        # Gets today date
        comic_date = get_now()

        while i < self._MAX_TRIES and detail.image_url == self.image:
            i += 1
            detail.date = comic_date
            if action == Action.Random:
                # TODO: Fix here
                # Random comic
                # , random_date
                detail.url = self.random_link
            else:
                detail.url = self.get_link_from_date(comic_date)

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
            # Finds the final url
            detail.url = self.extract_meta_content(soup, "url")
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


class BaseRSSComic(BaseComic, ABC):
    WORKING_TYPE = WorkingType.RSS
    MAX_ENTRIES = 19

    @abstractmethod
    @property
    def rss_url(self) -> str:
        pass

    @abstractmethod
    @property
    def weekday_token(self):
        pass

    @abstractmethod
    @property
    def timezone_token(self):
        pass

    @property
    def first_comic_date(self) -> int:
        return 1

    @abstractmethod
    def get_specific_url(self, date: Any):
        pass

    def get_comic_specific_date(self, date: Any):
        pass

    def extract_content(
        self, content: str, date: int, detail: ComicDetail
    ) -> ComicDetail:
        rss: RSS = RSSParser.parse(content)
        feed = rss.channel.content.items[date].content

        # To add in the "Finalize comic"? for webtoons
        #   if feed.title.content != "":
        # @     details.title = feed.title.content

        new_date = datetime.strptime(
            feed.pub_date.content,
            f"%{self.weekday_token}, %d %b %Y %H:%M:%S %{self.timezone_token}",
        )
        detail.date = new_date

        detail.url = feed.link.content

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

    async def get_comic(self, action: Action, verify_latest=False) -> ComicDetail:
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


class BaseNumberComic(BaseComic):
    WORKING_TYPE = WorkingType.Number

    @property
    def first_comic_date(self) -> int:
        return 1

    async def get_comic_url(self, action: Action) -> str | None:
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

    async def get_comic(self, action: Action, verify_latest=False) -> ComicDetail:
        detail = await super().get_comic(action)
        detail.url = await self.get_comic_url(action)
        html = await self.read_url_content(detail.url)
        detail = self.extract_content(html, 0, detail)
        if verify_latest:
            detail.is_latest = check_if_latest_link(detail.name, detail.image_url)
        return detail
