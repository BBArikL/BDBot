import json
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from bdbot.actions import Action
from bdbot.comics.base import BaseDateComic, BaseNumberComic, BaseRSSComic, Website
from bdbot.comics.comic_detail import ComicDetail


class GarfieldMinusGarfield(BaseRSSComic):
    WEBSITE_TYPE = Website.Custom

    @property
    def website_url(self):
        return self.main_website

    @property
    def fallback_image(self):
        return "https://64.media.tumblr.com/avatar_02c53466ae58_64.gif"

    @property
    def rss_url(self) -> str:
        return self.main_website + "rss"

    @property
    def weekday_token(self):
        return "a"

    @property
    def timezone_token(self):
        return "z"

    def get_specific_url(self, date: Any):
        return self.main_website + "day/" + date.strftime("%Y/%m/%d")


class CyanideAndHappiness(BaseNumberComic):
    WEBSITE_TYPE = Website.Custom

    _COMICS_URL = "https://explosm.net/comics/"

    async def get_comic_url(self, action: Action) -> str | None:
        suffix: str = ""
        match action:
            case Action.Random:
                suffix = "random"
            case Action.Today:
                suffix = "latest"
        return self.main_website + suffix

    def extract_content(
        self, content: str, action: Action, detail: ComicDetail
    ) -> ComicDetail:
        # Cyanide and Happiness special extractor
        # heavily inspired by https://github.com/JTexpo/Robobert
        # Parse the json that is embedded into the end of the page
        soup = BeautifulSoup(content, self._BASE_PARSER)
        data = soup.find("script", id="__NEXT_DATA__").get_text()

        json_data = json.loads(data)

        urql_states = json_data["props"]["pageProps"]["urqlState"]

        for state_id in urql_states:
            # Bruteforce the json entries to find the one contains the content of the comic
            state_data = urql_states[state_id]
            state_json = json.loads(state_data["data"])

            if "comic" in state_json:
                detail = self.extract_json_content(detail, state_json)
                break
        return detail

    def extract_json_content(self, detail: ComicDetail, middle_data) -> ComicDetail:
        comdata = middle_data["comic"]
        comic_det = comdata["comicDetails"]
        author_det = comic_det["author"]["authorDetails"]
        detail.url = self._COMICS_URL + comdata["slug"]
        detail.title = comdata["title"]
        if "comicmgurl" in comic_det:
            # Legacy comics
            detail.image_url = comic_det["comicmgurl"]
        else:
            # modern comics
            detail.image_url = comic_det["comicimgstaticbucketurl"]["mediaItemUrl"]
        detail.author = author_det["name"]
        detail.sub_image_url = author_det["image"]["mediaItemUrl"]
        detail.date = datetime.strptime(comdata["date"], "%Y-%m-%dT%H:%M:%S")
        return detail


class XKCD(BaseNumberComic):
    WEBSITE_TYPE = Website.Custom

    _RANDOM_COMICS = "https://c.xkcd.com/random/comic/"
    _JSON_API_SUFFIX = "info.0.json"

    async def get_comic_url(self, action: Action) -> str | None:
        url: str = self.main_website
        if action == Action.Random:
            url = self.extract_meta_content(
                BeautifulSoup(
                    await self.read_url_content(self._RANDOM_COMICS), self._BASE_PARSER
                ),
                "url",
            )
        return url + self._JSON_API_SUFFIX

    def extract_content(
        self, content: str, date: Any, detail: ComicDetail
    ) -> ComicDetail:
        # XKCD special extractor
        # We requested a json and not a html
        json_details = json.loads(content)

        detail.title = json_details["title"]
        detail.url = detail.url.removesuffix(self._JSON_API_SUFFIX)
        detail.image_url = json_details["img"]
        detail.alt = json_details["alt"]
        detail.date = datetime(
            year=int(json_details["year"]),
            month=int(json_details["month"]),
            day=int(json_details["day"]),
        )
        return detail


class Dilbert(BaseDateComic):
    WEBSITE_TYPE = Website.Custom

    @property
    def first_comic_date(self) -> datetime:
        return self.first_date

    @property
    def random_link(self) -> str:
        return ""

    @property
    def url_date_format(self) -> str:
        return "%Y-%m-%d"

    def get_link_from_date(self, date: datetime) -> str:
        return self.main_website + "strip" + "/" + date.strftime(self.url_date_format)
