from bdbot.comics.base import BaseRSSComic, Website, WorkingType


class Webtoons(BaseRSSComic):
    WEBSITE_NAME = "Webtoons"
    WEBSITE_HELP = "Use /help webtoons to get all comics that are supported on the Webtoons website."

    website_type = Website.Webtoons
    working_type = WorkingType.RSS

    @property
    def website_url(self):
        return self.website_type.value

    @property
    def rss_url(self) -> str:
        return self.main_website.replace("list", "rss")
