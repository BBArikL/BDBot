from typing import Any

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.base import BaseRSSComic, Website


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

    def get_comic(self, action: Action | ExtendedAction):
        pass
