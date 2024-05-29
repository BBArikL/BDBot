from typing import Any

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.base import BaseRSSComic, Website, WorkingType


class Webtoons(BaseRSSComic):
    WEBSITE_NAME = "Webtoons"
    WEBSITE_HELP = "Use /help webtoons to get all comics that are supported on the Webtoons website."
    WEBSITE_TYPE = Website.Webtoons
    WORKING_TYPE = WorkingType.RSS

    @property
    def website_url(self):
        return self.WEBSITE_TYPE.value

    @property
    def rss_url(self) -> str:
        return (self.main_website + self.web_name).replace("list", "rss")

    @property
    def weekday_token(self):
        return "A"

    @property
    def timezone_token(self):
        return "Z"

    def get_specific_url(self, date: Any):
        pass

    def get_comic(self, action: Action | ExtendedAction):
        pass
