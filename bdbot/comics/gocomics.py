import os
import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from bdbot.comics.base import BaseDateComic, WorkingType


class Gocomics(BaseDateComic):
    WEBSITE_NAME = "Gocomics"
    WEBSITE_URL = "https://www.gocomics.com/"
    WEBSITE_HELP = "Use /help gocomics to get all comics that are supported on the Gocomics website."
    WORKING_TYPE = WorkingType.Date
    SECTION_IMAGE_CLASS = re.compile("ShowComicViewer_showComicViewer__[a-zA-Z0-9]+")
    IMAGE_CLASS_REGEX = re.compile("Comic_comic__image__[a-zA-Z0-9]+_[a-zA-Z0-9]+.*")

    @property
    def first_comic_date(self) -> datetime:
        if os.getenv("BYPASS_GOCOMICS_SUBSCRIPTION"):
            return super().first_comic_date
        return datetime.today() - timedelta(days=14)

    @property
    def random_link(self) -> str:
        return f'{self.WEBSITE_URL}{self.web_name}/{self.get_random_comic_date().strftime("%Y/%m/%d")}'

    @property
    def url_date_format(self) -> str:
        return "/%Y/%m/%d"

    def get_link_from_date(self, date: datetime):
        return self.website_url + date.strftime(self.url_date_format)

    def extract_meta_content(
        self, soup: BeautifulSoup, content_name: str
    ) -> str | None:
        if content_name == "image":
            return self.extract_image(soup)
        elif content_name == "url":
            return None
        return super().extract_meta_content(soup, content_name)

    def extract_image(self, soup: BeautifulSoup) -> str | None:
        """Extract the image from Gocomics

        :param soup: The HTML source parsed
        :return: The extracted content or None if it did not find it
        """
        section = soup.find("section", attrs={"class": self.SECTION_IMAGE_CLASS})
        if section is None:
            return None
        image = section.find("img", attrs={"class": self.IMAGE_CLASS_REGEX})
        if image is None:
            return None
        return image["src"]
