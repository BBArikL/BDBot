# Collection of static methods
import enum
import random
import re
from datetime import datetime
from typing import Optional

from bdbot.files import get_footers
from bdbot.time import Date, get_date_formatted

date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "La"]
strip_details: dict = {}
link_cache: dict = {}
random_footers: list[str] = []


class MentionChoice(enum.Enum):
    Enable = "Enable"
    Disable = "Disable"


class MentionPolicy(enum.Enum):
    Daily = "Daily"
    All = "All"


def clean_url(url: str, file_forms: Optional[list] = None) -> str:
    """Gives back a clean link for a file on the internet, without the arguments after a '?'

    :param url:
    :param file_forms:
    :return:
    """
    if file_forms is None:
        file_forms = ["png", "jpg", "jpeg", "gif", "jfif", "bmp", "tif", "tiff", "eps"]

    for file_form in file_forms:
        url = re.sub(f"\\.{file_form}\\?.*$", f".{file_form}", url)

    return url.replace(" ", "%20")


def get_link(comic: dict, day: Optional[datetime] = None) -> str:
    """Returns the comic url

    :param comic:
    :param day:
    :return:
    """
    date_formatted = ""
    middle_params = ""
    if comic["Main_website"] == "https://www.gocomics.com/":
        date_formatted = get_date_formatted(day=day)
        middle_params = comic["Web_name"]
    elif comic["Main_website"] == "https://comicskingdom.com/":
        date_formatted = get_date_formatted(day=day, form="-")
        middle_params = comic["Web_name"]
    elif comic["Main_website"] == "https://dilbert.com/":
        date_formatted = day.strftime("%Y-%m-%d")
        middle_params = "strip"

    return f'{comic["Main_website"]}{middle_params}/{date_formatted}'


def get_strip_details(comic_name: str):
    """Get the details of a specific comic

    :param comic_name:
    :return:
    """
    return strip_details[comic_name]


def get_all_strips():
    return strip_details


def get_random_footer() -> str:
    """Get a random footer

    :return:
    """
    rnd_footer = random.choice(get_footers())

    return rnd_footer.replace("\n", "")


def parse_all(
    date: Date = None,
    hour: int = None,
    default_date: Date = Date.Daily,
    default_hour: int = 6,
) -> (Date, int):
    """

    :param date:
    :param hour:
    :param default_date:
    :param default_hour:
    :return:
    """
    final_date = default_date if date is None else date
    final_hour = default_hour if hour is None else hour

    return final_date, final_hour


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
