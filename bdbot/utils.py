# Collection of static methods
import random
import re

from bdbot.files import get_footers
from bdbot.time import Weekday

headers = {
    "User-Agent": "",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
}

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:160.0) Gecko/20100101 Firefox/160.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:160.0) Gecko/20100101 Firefox/160.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/158.0.0.0 Safari/537.36",
]


def clean_url(url: str) -> str:
    """Gives back a clean link for a file on the internet, without the arguments after a '?'"""
    file_forms = ["png", "jpg", "jpeg", "gif", "jfif", "bmp", "tif", "tiff", "eps"]
    for file_form in file_forms:
        url = re.sub(f"\\.{file_form}\\?.*$", f".{file_form}", url)
    url = re.sub("\\?.*$", "", url)
    return url.replace(" ", "%20")


def get_headers() -> dict:
    headers["User-Agent"] = random.choice(USER_AGENTS)
    return headers


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


def save_page_content(url, html):
    """Very useful, keep for debugging"""
    with open(f"{url.replace('/', '-').replace(':', '')}.html", "w") as f:
        f.write(html.html)
