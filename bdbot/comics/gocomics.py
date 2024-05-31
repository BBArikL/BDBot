from datetime import datetime

from bdbot.comics.base import BaseDateComic, Website


class Gocomics(BaseDateComic):
    WEBSITE_NAME = "Gocomics"
    WEBSITE_HELP = "Use /help gocomics to get all comics that are supported on the Gocomics website."
    WEBSITE_TYPE = Website.Gocomics

    @property
    def first_comic_date(self) -> datetime:
        return self.first_date

    @property
    def random_link(self) -> str:
        return f"{self.main_website}random/{self.web_name}"

    @property
    def url_date_format(self) -> str:
        return "%Y/%m/%d"

    def get_link_from_date(self, date: datetime):
        return self.website_url + "/" + date.strftime(self.url_date_format)
