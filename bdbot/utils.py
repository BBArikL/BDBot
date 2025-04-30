# Collection of static methods
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bdbot.comics import BaseComic
from bdbot.files import get_footers
from bdbot.time import Weekday

comic_details: dict[str, "BaseComic"] = {}
random_footers: list[str] = []
headers = {
    "User-Agent": "",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-M215F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.185 Mobile"
    " Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; LM-X220) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile"
    " Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SGP512) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101"
    " Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; LG-US701) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile"
    " Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile"
    " Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66"
    " Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3"
    " Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S901W) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0"
    " Chrome/115.0.0.0 Mobile Safari/537.36",
]


def get_headers() -> dict:
    headers["User-Agent"] = random.choice(USER_AGENTS)
    return headers


def all_comics() -> dict[str, "BaseComic"]:
    return comic_details


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
