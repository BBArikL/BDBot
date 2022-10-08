# Collection of static methods
import calendar
import enum
import logging
import os
import re
import random
import json

# from src import Web_requests_manager
from datetime import datetime, timedelta, timezone
from randomtimestamp import randomtimestamp
from typing import Optional
from os import path

DETAILS_PATH = "src/misc/comics_details.json"
FOOTERS_FILE_PATH = 'src/misc/random-footers.txt'
DATABASE_FILE_PATH = "src/data/data.json"
BACKUP_FILE_PATH = "src/data/backups/BACKUP_DATABASE_"
REQUEST_FILE_PATH = "src/data/requests.txt"
COMIC_LATEST_LINKS_PATH = "src/data/latest_comics.json"
date_tries = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "La"]
match_date = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
    "Su": "Sunday",
    "D": "day",
    "La": "Latest"
}
strip_details: dict = {}
link_cache: dict = {}
random_footers: list[str] = []


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
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)

    return json_file


def clean_database(data: dict = None, do_backup: bool = True, strict: bool = False, logger: logging.Logger = None):
    """

    :param data:
    :param do_backup:
    :param strict:
    :param logger:
    :return:
    """
    logger.info("Running database clean...")
    # Cleans the database from inactive servers
    if data is None:
        data = load_json(DATABASE_FILE_PATH)

    if do_backup:
        save_backup(data, logger)

    guilds_to_clean = []
    nb_removed = 0

    for guild in data:
        # To take in account or not if a server still has a role tied to their info
        if "role" not in data[guild] or strict:
            to_remove = True
            channels = data[guild]["channels"]
            for chan in channels:
                if "date" in channels[chan]:
                    dates = channels[chan]["date"]
                    for date in dates:
                        hours = dates[date]
                        for hour in hours:
                            if len(hours[hour]) > 0:
                                to_remove = False
                                break
                        if not to_remove:
                            break
                    if not to_remove:
                        break

            if to_remove:
                guilds_to_clean.append(guild)
                nb_removed += 1

    if nb_removed > 0:
        save_json(data)

    logger.info(f"Cleaned the database from {nb_removed} servers")
    return nb_removed


def save_backup(data, logger: logging.Logger):
    """

    :param logger:
    :param data:
    :return:
    """
    logger.info("Running backup...")
    # Creates a new backup and saves it
    backupfp = BACKUP_FILE_PATH + datetime.now(timezone.utc).strftime("%Y_%m_%d_%H") + ".json"

    with open(backupfp, 'w') as f:
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
        with open(file_path, 'r') as f:
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
    with open(file_path, 'w') as f:
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


def get_today() -> str:
    """Get the first two letters of the current weekday in UTC

    :return: The first two letters of the weekday
    """
    return datetime.now(timezone.utc).today().strftime("%A")[0:2]


def get_hour() -> str:
    """Get the current UTC hour

    :return: Current UTC hour
    """
    return str(datetime.now(timezone.utc).hour)


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
        random_date: datetime = randomtimestamp(start=first_date,
                                                end=datetime.today().replace(hour=0, minute=0, second=0,
                                                                             microsecond=0))
        middle_params = ""
        if comic["Main_website"] == "https://comicskingdom.com/":
            middle_params = comic["Web_name"]
        elif comic["Main_website"] == "https://dilbert.com/":
            middle_params = "strip"

        return f'{comic["Main_website"]}{middle_params}/{random_date.strftime("%Y-%m-%d")}', random_date


def get_strip_details(comic_name: str):
    """Get the details of a specific comic

    :param comic_name:
    :return:
    """
    return strip_details[comic_name]


def get_random_footer() -> str:
    """Get a random footer

    :return:
    """
    rnd_footer = random.choice(get_footers())

    return rnd_footer.replace('\n', '')


def get_footers() -> list[str]:
    """

    :return:
    """
    if random_footers is None or random_footers == []:
        return open(FOOTERS_FILE_PATH, 'rt').readlines()
    else:
        return random_footers


def parse_all(date=None, hour=None, default_date="D", default_hour=6) -> (str, str):
    """

    :param date:
    :param hour:
    :param default_date:
    :param default_hour:
    :return:
    """
    final_date = default_date
    final_hour = default_hour

    final_date, final_hour = parse_try(date, final_date, final_hour)
    final_date, final_hour = parse_try(hour, final_date, final_hour)

    return final_date, final_hour


def parse_try(to_parse, final_date, final_hour) -> (str, str):
    """

    :param to_parse:
    :param final_date:
    :param final_hour:
    :return:
    """
    if to_parse is not None:
        if len(str(to_parse)) >= 2:
            date = to_parse[0:1].capitalize() + to_parse[1:2].lower()

            if date in date_tries:
                final_date = date
            else:
                try:
                    final_hour = int(to_parse)
                except ValueError:
                    pass
        else:
            try:
                final_hour = int(to_parse)
            except ValueError:
                pass

    return final_date, final_hour


def check_if_latest_link(comic_name: str, current_link: str) -> bool:
    """

    :param comic_name:
    :param current_link:
    :return:
    """
    return current_link != link_cache[comic_name]


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
        requests.write(f'Request: "{param}" by {author}#{discriminator} on '
                       f'{datetime.now(timezone.utc)}\n')


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
    Wednesday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


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
