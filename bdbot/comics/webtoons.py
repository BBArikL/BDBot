from typing import Any

from bdbot.comics.base import BaseRSSComic, WorkingType


class Webtoons(BaseRSSComic):
    WEBSITE_NAME = "Webtoons"
    WEBSITE_URL = "https://www.webtoons.com/en/"
    WEBSITE_HELP = "Use /help webtoons to get all comics that are supported on the Webtoons website."
    WORKING_TYPE = WorkingType.RSS

    @property
    def website_url(self):
        return self.WEBSITE_URL

    @property
    def rss_url(self) -> str:
        return (
            (self.website_url + self.web_name)
            .replace("list", "rss")
            .replace("canvas", "challenge")
        )

    @property
    def weekday_token(self):
        return "A"

    @property
    def timezone_token(self):
        return "Z"

    def get_specific_url(self, date: Any):
        return self.website_url + self.web_name + f"&episode_no={date}"
