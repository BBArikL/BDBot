from bdbot.comics.base import BaseComic, WorkingType
from bdbot.comics.comicskingdom import ComicsKingdom
from bdbot.comics.custom import XKCD, CyanideAndHappiness, GarfieldMinusGarfield
from bdbot.comics.gocomics import Gocomics
from bdbot.comics.webtoons import Webtoons


def initialize_comics(
    comics: dict, base_on_error: bool = False
) -> dict[str, BaseComic]:
    c: dict[str, BaseComic] = {}
    for comic_name, comic in comics.items():
        comic_type = BaseComic.get_type(
            comic["main_website"], WorkingType(comic["working_type"]), base_on_error
        )
        c.update(
            {
                comic_name: comic_type(
                    WEBSITE_NAME=comic_type.WEBSITE_NAME,
                    WEBSITE_URL=comic_type.WEBSITE_URL,
                    WEBSITE_HELP=comic_type.WEBSITE_HELP,
                    WORKING_TYPE=comic_type.WORKING_TYPE,
                    **comic,
                )
            }
        )
    return c


__all__ = [
    Gocomics,
    Webtoons,
    ComicsKingdom,
    GarfieldMinusGarfield,
    XKCD,
    CyanideAndHappiness,
]
