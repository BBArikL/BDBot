from datetime import datetime

from bdbot.comics import WorkingType
from bdbot.comics.base import BaseDateComic


class ComicsKingdom(BaseDateComic):
    WEBSITE_NAME = "Comics Kingdom"
    WEBSITE_URL = "https://comicskingdom.com/"
    WEBSITE_HELP = "Use /help comicskingdom to get all comics that are supported on the Comics Kingdom website."
    WORKING_TYPE = WorkingType.Date

    @property
    def random_link(self) -> str:
        return f'{self.WEBSITE_URL}{self.web_name}/{self.get_random_comic_date().strftime("%Y-%m-%d")}'

    @property
    def url_date_format(self) -> str:
        return "/%Y-%m-%d"

    def get_link_from_date(self, date: datetime):
        return self.website_url + date.strftime(self.url_date_format)
