from bdbot.comics.base import BaseComic, WorkingType


def initialize_comics(comics: dict) -> dict[str, BaseComic]:
    c: dict[str, BaseComic] = {}
    for comic_name, comic in comics.items():
        comic_type = BaseComic.get_type(
            comic["main_website"], WorkingType(comic["working_type"])
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
