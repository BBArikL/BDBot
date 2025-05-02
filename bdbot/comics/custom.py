import json
import logging
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from bdbot.actions import Action
from bdbot.comics.base import BaseNumberComic, BaseRSSComic, WorkingType
from bdbot.comics.comic_detail import ComicDetail


class GarfieldMinusGarfield(BaseRSSComic):
    WEBSITE_NAME = "Garfield Minus Garfield"
    WEBSITE_URL = "https://garfieldminusgarfield.net/"
    WORKING_TYPE = WorkingType.RSS
    WEBSITE_HELP = ""

    @property
    def website_url(self):
        return self.WEBSITE_URL

    @property
    def fallback_image(self):
        return self.image

    @property
    def rss_url(self) -> str:
        return self.website_url + "rss"

    @property
    def weekday_token(self):
        return "a"

    @property
    def timezone_token(self):
        return "z"

    def get_specific_url(self, date: Any):
        return self.website_url + "day/" + date.strftime("%Y/%m/%d")


class CyanideAndHappiness(BaseNumberComic):
    WEBSITE_NAME = "Cyanide and Happiness"
    WEBSITE_URL = "https://explosm.net/comics/"
    WORKING_TYPE = WorkingType.Number
    WEBSITE_HELP = ""

    async def get_comic_url(self, action: Action, comic_date=None) -> str | None:
        return self.WEBSITE_URL + "latest"

    async def extract_content(
        self, content: str, date: int, detail: ComicDetail, action: Action | None = None
    ) -> ComicDetail:
        # Cyanide and Happiness special extractor
        # heavily inspired by https://github.com/JTexpo/Robobert
        # Parse the json that is embedded into the end of the page
        logger = logging.getLogger("discord")
        soup = BeautifulSoup(content, self._BASE_PARSER)
        data = soup.find("script", id="__NEXT_DATA__").get_text()
        logger.debug("Loading json data...")
        json_data = json.loads(data)
        logger.debug("Getting urql states...")
        urql_states = json_data["props"]["pageProps"]["urqlState"]
        for state_id in urql_states:
            # Bruteforce the json entries to find the one contains the content of the comic
            logger.debug(f"Trying state id: {state_id}...")
            state_data = urql_states[state_id]
            state_json = json.loads(state_data["data"])
            if "comic" in state_json:
                logger.debug("Found comic content, extracting...")
                detail = await self.extract_json_content(detail, state_json, action)
                break
        return detail

    async def extract_json_content(
        self, detail: ComicDetail, middle_data, action: Action | None
    ) -> ComicDetail:
        comic_data = middle_data["comic"]
        logger = logging.getLogger("discord")
        logger.debug(f"Extracting comic data with action {action}...")
        if action == Action.Random:
            logger.debug("Requested random Cyanide and Happiness comic...")
            random_url = self.WEBSITE_URL + comic_data["navigation"][0]["randomSlug"]
            logger.debug(f"Random url: {random_url}...")
            html = await self.read_url_content(random_url)
            logger.debug(
                "Comic could be found, extracting content "
                "(entering recursion, if you see this more this more than ounce, it will probably recurse infinitely)"
            )
            # Set action to "Today" to avoid infinite recursion
            return await self.extract_content(html, 0, detail, Action.Today)
        comic_details = comic_data["comicDetails"]
        logger.debug("Getting author details...")
        author_details = comic_details["author"]["authorDetails"]
        detail.author = author_details["name"]
        detail.sub_image_url = author_details["image"]["mediaItemUrl"]
        logger.debug("Getting exact url...")
        detail.url = self.WEBSITE_URL + comic_data["slug"]
        detail.title = comic_data["title"]
        logger.debug("Getting image url...")
        detail.image_url = None
        if "comicimgurl" in comic_details and comic_details["comicimgurl"] is not None:
            # Legacy comics
            detail.image_url = (
                "https://files.explosm.net/comics/" + comic_details["comicimgurl"]
            )
        elif (
            "comicimgstaticbucketurl" in comic_details
            and comic_details["comicimgstaticbucketurl"] is not None
        ):
            # modern comics
            image_static = comic_details["comicimgstaticbucketurl"]
            if image_static is not None and "mediaItemUrl" in image_static:
                detail.image_url = image_static["mediaItemUrl"]
        if detail.image_url is None:
            logger.debug("Could not find image url, using fallback...")
            logger.debug(f"Current comic_details are : {comic_details}")
            detail.image_url = self.fallback_image
        logger.debug("Getting date...")
        detail.date = datetime.strptime(comic_data["date"], "%Y-%m-%dT%H:%M:%S")
        return detail


class XKCD(BaseNumberComic):
    WEBSITE_NAME = "XKCD"
    WEBSITE_URL = "https://xkcd.com/"
    WORKING_TYPE = WorkingType.Number
    WEBSITE_HELP = ""
    _RANDOM_COMICS = "https://c.xkcd.com/random/comic/"
    _JSON_API_SUFFIX = "info.0.json"

    async def get_comic_url(self, action: Action, comic_date=None) -> str | None:
        url: str = self.WEBSITE_URL
        if action == Action.Random:
            url = self.extract_meta_content(
                BeautifulSoup(
                    await self.read_url_content(self._RANDOM_COMICS), self._BASE_PARSER
                ),
                "url",
            )
        elif action == Action.Specific_date:
            url += f"{comic_date}/"
        return url + self._JSON_API_SUFFIX

    async def extract_content(
        self, content: str, date: Any, detail: ComicDetail, action=None
    ) -> ComicDetail:
        # XKCD special extractor
        # We requested a json and not a html
        json_details = json.loads(content)
        detail.title = json_details["title"]
        detail.url = self.WEBSITE_URL + str(json_details["num"])
        detail.image_url = json_details["img"]
        detail.alt = json_details["alt"]
        detail.date = datetime(
            year=int(json_details["year"]),
            month=int(json_details["month"]),
            day=int(json_details["day"]),
        )
        return detail
