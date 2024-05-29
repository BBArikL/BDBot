import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from random import randint
from typing import Any

import aiohttp
from bs4 import BeautifulSoup
from randomtimestamp import randomtimestamp
from rss_parser import RSSParser
from rss_parser.models.rss import RSS

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.comic_detail import ComicDetail
from bdbot.embed import DEFAULT_FIELDS_PER_EMBED, Embed
from bdbot.field import Field
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
    async def get_comic(self, action: Action | ExtendedAction) -> ComicDetail:
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
            thumbnails=[self.image],
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

    async def get_comic(self, action: Action | ExtendedAction) -> ComicDetail:
        details = await super().get_comic(action)
        if action == Action.Today:
            # First comic in the rss feed
            comic_nb = 0
        elif action == Action.Random:
            comic_nb = randint(0, self.MAX_ENTRIES)

        if action == Action.Specific_date:
            details.image_url = self.fallback_image
            date = datetime.now()
            details.url = self.get_specific_url(date)
            return details

        site_content: str
        async with aiohttp.ClientSession() as session:
            async with session.get(self.rss_url) as response:
                site_content = await response.text()

        if site_content is None or site_content == "":
            return None

        rss: RSS = RSSParser.parse(site_content)
        feed = rss.channel.content.items[comic_nb].content

        # To add in the "Finalize comic"?
        #   if feed.title.content != "":
        # @     details.title = feed.title.content

        new_date = datetime.strptime(
            feed.pub_date.content,
            f"%{self.weekday_token}, %d %b %Y %H:%M:%S %{self.timezone_token}",
        )
        details.date = new_date

        details.url = feed.link.content

        description_soup = BeautifulSoup(feed.description.content, "html.parser")
        description_images = [
            {"alt": image.get("alt", ""), "source": image.get("src")}
            for image in description_soup.findAll("img")
        ]
        if len(description_images) > 0:
            img_index = 0
            if len(description_images) > 1:
                # general check for a second image to embed
                details.sub_image_url = description_images[img_index]["source"]
                img_index += 1
            details.image_url = description_images[img_index]["source"]
        else:
            details.image_url = self.fallback_image
        # finalize_comic(strip_details, details, latest_check)
        return details
