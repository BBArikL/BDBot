from bdbot.comics.base import BaseRSSComic, Website


class GarfieldMinusGarfield(BaseRSSComic):
    website_type = Website.Custom

    @property
    def website_url(self):
        return self.main_website

    @property
    def fallback_image(self):
        return ""

    @property
    def rss_url(self) -> str:
        return self.main_website + "rss"
