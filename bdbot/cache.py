import logging

from bdbot.actions import Action
from bdbot.comics.base import BaseComic
from bdbot.files import COMIC_LATEST_LINKS_PATH, DETAILS_PATH, load_json, save_json

link_cache: dict = {}


async def create_link_cache(logger_: logging.Logger) -> None:
    """Create a cache of links containing the latest comics links

    :param logger_: The logger to use
    """
    logger_.debug("Running link cache...")
    comics: dict[str, BaseComic] = load_json(DETAILS_PATH)
    for comic in comics:
        logger_.debug(f"Getting image link for comic {comic} ...")
        comic_url: str
        try:
            comic_url = (await comics[comic].get_comic(action=Action.Today)).url
        except (ValueError, AttributeError) as e:
            logger_.error(f"An error occurred for comic {comic}: {e}")
            comic_url = ""
        link_cache.update({comics[comic].name: (comic_url)})

    logger_.debug("Saving comics link...")
    save_json(link_cache, COMIC_LATEST_LINKS_PATH)


def check_if_latest_link(comic_name: str, current_link: str) -> bool:
    """

    :param comic_name:
    :param current_link:
    :return:
    """
    return current_link != link_cache.get(comic_name, "")


def fill_cache(
    details: dict[str, dict[str, str]], cache: dict[str, str], default: str = ""
) -> dict[str, str]:
    """Fill the cache with missing comic cache

    :param details: The comic details
    :param cache: The comic latest link cache
    :param default: The default to add to the cache
    :return: The cache with an entry for all comics
    """
    for comic in details:
        cache.setdefault(details[comic]["Name"], default)

    return cache
