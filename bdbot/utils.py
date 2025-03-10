# Collection of static methods
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bdbot.comics import BaseComic
from bdbot.files import get_footers
from bdbot.time import Weekday

strip_details: dict[str, "BaseComic"] = {}
random_footers: list[str] = []


# def clean_url(url: str, file_forms: Optional[list] = None) -> str:
#     """Gives back a clean link for a file on the internet, without the arguments after a '?'
#
#     :param url:
#     :param file_forms:
#     :return:
#     """
#     if file_forms is None:
#         file_forms = ["png", "jpg", "jpeg", "gif", "jfif", "bmp", "tif", "tiff", "eps"]
#
#     for file_form in file_forms:
#         url = re.sub(f"\\.{file_form}\\?.*$", f".{file_form}", url)
#
#     return url.replace(" ", "%20")


def get_strip_details(comic_name: str) -> "BaseComic":
    """Get the details of a specific comic

    :param comic_name:
    :return:
    """
    return strip_details[comic_name]


def get_all_strips() -> dict[str, "BaseComic"]:
    return strip_details


def get_random_footer() -> str:
    """Get a random footer

    :return: A random footer text
    """
    rnd_footer = random.choice(get_footers())

    return rnd_footer.replace("\n", "")


def parse_all(
    date: Weekday = None,
    hour: int = None,
    default_date: Weekday = Weekday.Daily,
    default_hour: int = 6,
) -> (Weekday, int):
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
