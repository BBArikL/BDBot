import json
import os
import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    pass


MAX_BACKUP_TRIES = 25
PROD_DATA_PATH = (
    os.path.join(os.getenv("LOCALAPPDATA"), "bdbot")
    if os.name == "nt"
    else os.path.join("/home", os.getenv("USER", ""), ".local", "share", "bdbot")
)
DEV_DATA_PATH = os.path.dirname(__file__)
BASE_DATA_PATH = PROD_DATA_PATH if not os.getenv("DEBUG") else DEV_DATA_PATH
MISC_PATH = os.path.join(BASE_DATA_PATH, "misc")
DATA_PATH = os.path.join(BASE_DATA_PATH, "data")
DETAILS_PATH = os.path.join(MISC_PATH, "comics_details.json")
FOOTERS_FILE_PATH = os.path.join(MISC_PATH, "random-footers.txt")
HELP_EMBED_PATH = os.path.join(MISC_PATH, "help_embeds.json")
DATABASE_FILE_PATH = os.path.join(DATA_PATH, "data.sqlite3")
BACKUPS_PATH = os.path.join(DATA_PATH, "backups")
BACKUP_FILE_PATH = os.path.join(BACKUPS_PATH, "BACKUP_DATABASE_")
LOGS_DIRECTORY_PATH = os.path.join(DATA_PATH, "logs/")
REQUEST_FILE_PATH = os.path.join(DATA_PATH, "requests.txt")
COMIC_LATEST_LINKS_PATH = os.path.join(BASE_DATA_PATH, "latest_comics.json")
PID_FILE = os.path.join(BASE_DATA_PATH, "bdbot.pid")
ENV_FILE = os.path.abspath(os.path.join(BASE_DATA_PATH, "..", ".env"))


def get_footers() -> list[str]:
    """

    :return:
    """
    with open(FOOTERS_FILE_PATH, "rt") as f:
        lines = f.readlines()
    return lines


def load_json(json_path: str) -> dict[str, Any]:
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


def save_json(json_file: dict, file_path: str = DATABASE_FILE_PATH):
    """Saves the json file

    :param json_file:
    :param file_path:
    :return:
    """
    with open(file_path, "w") as f:
        json.dump(json_file, f, indent=4)


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
