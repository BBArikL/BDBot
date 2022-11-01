# Collection of static methods
import enum
import json
import logging
import os
import random
import re
from datetime import datetime, timedelta, timezone
from os import path
from typing import Optional

from randomtimestamp import randomtimestamp

BASE_DATA_PATH = (
    f"{os.getenv('LOCALAPPDATA')}/bdbot/"
    if os.name == "nt"
    else f"/home/{os.getenv('USER')}/.local/bdbot/"
)
DETAILS_PATH = f"{BASE_DATA_PATH}misc/comics_details.json"
FOOTERS_FILE_PATH = f"{BASE_DATA_PATH}misc/random-footers.txt"
DATABASE_FILE_PATH = f"{BASE_DATA_PATH}data/data.json"
BACKUP_FILE_PATH = f"{BASE_DATA_PATH}data/backups/BACKUP_DATABASE_"
LOGS_DIRECTORY_PATH = f"{BASE_DATA_PATH}data/logs/"
REQUEST_FILE_PATH = f"{BASE_DATA_PATH}data/requests.txt"
COMIC_LATEST_LINKS_PATH = f"{BASE_DATA_PATH}data/latest_comics.json"
PID_FILE = f"{BASE_DATA_PATH}bdbot.pid"
ENV_FILE = f"{BASE_DATA_PATH}.env"
date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "La"]
strip_details: dict = {}
link_cache: dict = {}
random_footers: list[str] = []


class Action(enum.Enum):
    Today = "Today"
    Random = "Random"
    Specific_date = "Specific date"
    Info = "Info"
    Add = "Add"
    Remove = "Remove"


class ExtendedAction(enum.Enum):
    Specific_date = "Specific_date"
    Remove_channel = "Remove_channel"
    Remove_guild = "Remove_guild"
    Add_all = "Add_all"
    Auto_remove_guild = "auto_remove_guild"
    Auto_remove_channel = "auto_remove_channel"


class Date(enum.Enum):
    Daily = "Daily"
    Latest = "Latest"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


match_date = {
    "Mo": Date.Monday,
    "Tu": Date.Tuesday,
    "We": Date.Wednesday,
    "Th": Date.Thursday,
    "Fr": Date.Friday,
    "Sa": Date.Saturday,
    "Su": Date.Sunday,
    "D": Date.Daily,
    "La": Date.Latest,
}


class Month(enum.Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


class MentionChoice(enum.Enum):
    Enable = "Enable"
    Disable = "Disable"


class MentionPolicy(enum.Enum):
    Daily = "Daily"
    All = "All"


def load_json(json_path: str) -> dict:
    """
    Load a json.
    DETAILS_PATH -> The comic details.
    DATABASE_FILE_PATH -> The database.
    JSON_SCHEMA_PATH -> The schema of the database.
    BACKUP_FILE_PATH -> The default backup.
    COMIC_LATEST_LINKS_PATH -> The latest links to the images of the comics.

    :param json_path: The path to the json file.
    :return: The json as a dict.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        json_file = json.load(f)

    return json_file


def save_backup(data, logger: logging.Logger):
    """

    :param logger:
    :param data:
    :return:
    """
    logger.info("Running backup...")
    # Creates a new backup and saves it
    backup_file_path = (
        BACKUP_FILE_PATH + datetime.now(timezone.utc).strftime("%Y_%m_%d_%H") + ".json"
    )

    with open(backup_file_path, "w") as f:
        json.dump(data, f)

    logger.info("Backup successfully done")


def restore_backup():
    """Restore a last used backup"""

    utc_date = datetime.now(timezone.utc)
    file_path = BACKUP_FILE_PATH + utc_date.strftime("%Y_%m_%d_%H") + ".json"
    tries = 0

    while not path.exists(file_path) and tries < 25:
        tries += 1
        utc_date = utc_date - timedelta(hours=1)
        file_path = BACKUP_FILE_PATH + utc_date.strftime("%Y_%m_%d_%H") + ".json"

    if tries < 25:
        with open(file_path, "r") as f:
            database = json.load(f)

        if database != "":
            save_json(database)
    else:
        raise Exception("No backup was found in the last 24 hours!!")


def save_json(json_file: dict, file_path: str = DATABASE_FILE_PATH):
    """Saves the json file

    :param json_file:
    :param file_path:
    :return:
    """
    with open(file_path, "w") as f:
        json.dump(json_file, f, indent=4)


def get_date(date: str):
    """Reformat the date from 'YYYY, mm, dd' -> '<Weekday> dd, YYYY'

    :param date:
    :return:
    """
    return datetime.strptime(date, "%Y, %m, %d").strftime("%A %d, %Y")


def get_first_date(comic: dict) -> str:
    """Get the first date of the comic

    :param comic:
    :return:
    """
    if comic["Main_website"] == "https://comicskingdom.com/":
        # Comics kingdom only lets us go back 7 days in the past
        return (datetime.today() - timedelta(days=7)).strftime("%Y, %m, %d")
    else:
        return comic["First_date"]


def get_today() -> Date:
    """Get the day

    :return: The first two letters of the weekday
    """
    return Date(datetime.now(timezone.utc).today().strftime("%A"))


def date_to_db(date: Date) -> str:
    return date.value[:2:] if date != Date.Daily else date.value[:1:]


def get_hour() -> int:
    """Get the current UTC hour

    :return: Current UTC hour
    """
    return datetime.now(timezone.utc).hour


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

    url = url.replace(" ", "%20")

    return url


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


def get_date_formatted(day: Optional[datetime] = None, form: str = "/") -> str:
    """Get the date formatted separated by a string format

    :param day:
    :param form:
    :return:
    """
    if day is not None:
        return day.strftime(f"%Y{form}%m{form}%d")
    else:
        return ""


def get_random_link(comic: dict) -> (str, Optional[datetime]):
    """Returns a random comic url

    :param comic:
    :return:
    """
    if comic["Main_website"] == "https://www.gocomics.com/":
        return f'{comic["Main_website"]}random/{comic["Web_name"]}', None
    else:
        first_date = datetime.strptime(get_first_date(comic), "%Y, %m, %d")
        random_date: datetime = randomtimestamp(
            start=first_date,
            end=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        )
        middle_params = ""
        if comic["Main_website"] == "https://comicskingdom.com/":
            middle_params = comic["Web_name"]
        elif comic["Main_website"] == "https://dilbert.com/":
            middle_params = "strip"

        return (
            f'{comic["Main_website"]}{middle_params}/{random_date.strftime("%Y-%m-%d")}',
            random_date,
        )


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


def get_footers() -> list[str]:
    """

    :return:
    """
    if random_footers is None or random_footers == []:
        with open(FOOTERS_FILE_PATH, "rt") as f:
            lines = f.readlines()
        return lines
    else:
        return random_footers


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


def write_pid(file_path: str):
    """Write pid to a file

    :param file_path: The path to the pid file
    """
    with open(file_path, "wt") as f:
        f.write(str(os.getpid()))


def save_request(req: str, author: str, discriminator: Optional[str] = ""):
    # Tries to get rid of ANSI codes while not destroying the comment itself
    param = re.escape(req)
    param = re.sub("[\\^]*\\\\\\[*", "", param)

    with open(REQUEST_FILE_PATH, "at") as requests:
        requests.write(
            f'Request: "{param}" by {author}#{discriminator} on '
            f"{datetime.now(timezone.utc)}\n"
        )


def fill_cache(details: dict[str, dict[str, str]], cache: dict[str, str], default: str = "") -> dict[str, str]:
    """Fill the cache with missing comic cache

    :param details: The comic details
    :param cache: The comic latest link cache
    :param default: The default to add to the cache
    :return: The cache with an entry for all comics
    """
    for comic in details:
        cache.setdefault(details[comic]["Name"], default)

    return cache
