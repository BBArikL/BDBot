from datetime import datetime, timedelta

from bdbot.actions import Action, ExtendedAction
from bdbot.comics.base import BaseDateComic, Website


class ComicsKingdom(BaseDateComic):
    WEBSITE_NAME = "Comics Kingdom"
    WEBSITE_HELP = "Use /help comicskingdom to get all comics that are supported on the Comics Kingdom website."
    website_type = Website.ComicsKingdom

    @property
    def first_comic_date(self) -> datetime:
        return datetime.today() - timedelta(days=7)

    @property
    def random_link(self) -> str:
        return f'{self.main_website}{self.web_name}/{self.get_random_comic_date().strftime("%Y-%m-%d")}'

    def get_comic(self, action: Action | ExtendedAction):
        pass
