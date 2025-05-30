import asyncio
import getpass
import json
import logging
import os
import platform
import pty
import re
import shutil
import sys
from typing import Optional, Type, Union

from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.prompts import ListPrompt, SecretPrompt
from tortoise import connections

from bdbot.cache import create_link_cache
from bdbot.comics import ComicsKingdom, Gocomics, Webtoons, initialize_comics
from bdbot.comics.base import BaseComic, WorkingType
from bdbot.db import (
    ChannelSubscription,
    DiscordSubscription,
    ServerSubscription,
    dbinit,
    save_backup,
)
from bdbot.discord_.discord_utils import clean_database
from bdbot.files import (
    BACKUP_FILE_PATH,
    BASE_DATA_PATH,
    DATA_PATH,
    DATABASE_FILE_PATH,
    DETAILS_PATH,
    ENV_FILE,
    FOOTERS_FILE_PATH,
    HELP_EMBED_PATH,
    LOGS_DIRECTORY_PATH,
    PROD_DATA_PATH,
    REQUEST_FILE_PATH,
    load_json,
    save_json,
)
from bdbot.subscription_type import SubscriptionType
from bdbot.time import Weekday

TEMP_FILE_PATH = "misc/comics_not_ready.json"
RETIRED_COMICS_PATH = "misc/retired_comics.json"
EXIT_CHOICE = "Exit"
RETURN_CHOICE = "Return"
INQUIRY = "inquiry"
ENV_VARS: dict[str, dict[str, Union[str, Union[SecretPrompt, ListPrompt]]]] = {
    "TOKEN": {
        "value": "",
        INQUIRY: inquirer.secret(message="Enter the token (The bot discord token):"),
    },
    "CLIENT_ID": {
        "value": "",
        INQUIRY: inquirer.secret(
            message="Enter the client ID (The bot client ID. "
            "To get a invite for the bot):"
        ),
    },
    "PRIVATE_CHANNEL_SUPPORT_ID": {
        "value": "",
        INQUIRY: inquirer.secret(
            message="Enter the ID of the private channel (The ID of the channel where the bot can print"
            " debugging information):"
        ),
    },
    "PRIVATE_SERVER_SUPPORT_ID": {
        "value": "",
        INQUIRY: inquirer.secret(
            message="Enter the ID of the private server (The ID of the server where the bot can allow owner "
            "commands):"
        ),
    },
    "DEBUG": {
        "value": "",
        INQUIRY: inquirer.select(
            message="Is the bot used for development purposes? (Should be False if the bot is supposed to"
            " serve multiple servers):",
            choices=["True", "False"],
        ),
    },
    "BYPASS_GOCOMICS_JS": {
        "value": "",
        INQUIRY: inquirer.select(
            message="Do you want to bypass Gocomic's JS? (Please note that you will need to install Playwright):",
            choices=["True", "False"],
        ),
    },
    "BYPASS_GOCOMICS_SUBSCRIPTION": {
        "value": "",
        INQUIRY: inquirer.select(
            message="Do you want to bypass Gocomic's ~14 day block?:",
            choices=["True", "False"],
        ),
    },
}
LOCAL_SERVICE_PATH = "misc/runbdbot.service"
SERVICE_PATH = "/etc/systemd/system/"
HOME_PATH = "/home/"
COMMAND = "sudo systemctl daemon-reload && sudo systemctl enable --now runbdbot.service"

logger = logging.Logger("manager_logger", logging.INFO)


def main():
    """Add, delete or modify comics in the comic details file"""
    os.chdir(os.path.dirname(__file__))  # Force the current working directory
    load_dotenv()
    # Set the logging handler
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    choices = {
        "Manage bot": manage_bot,
        "Manage comics": manage_comics,
        EXIT_CHOICE: todo,
    }

    action = ""
    while action != EXIT_CHOICE:
        action = inquirer.select(
            message="What do you want to do?",
            choices=list(choices.keys()),
        ).execute()
        choices[action]()


def manage_bot():
    """Manage the bot and its settings"""
    action = ""
    while action != RETURN_CHOICE:
        choices = {
            "Database tools": spawn_tortoise_shell,
            "Verify requests": view_requests,
            "Create image link cache": link_cache_generate,
            "Refresh configuration files (to do after every update)": refresh_conf_files,
            "Migrate from v4 to v5": migrate_v4_v5,
            "Setup Bot": setup_bot,
            "Uninstall Bot": uninstall_bot,
            RETURN_CHOICE: todo,
        }

        action = inquirer.select(
            message="What do you want to do?",
            choices=list(choices.keys()),
            mandatory=False,
        ).execute()

        choices[action]()


def spawn_tortoise_shell():
    print(
        "Import the subscription object with:\n"
        "from bdbot.db.discord_subscription import *\n\n"
        "After, you can fetch data from with 'await' statements "
        "and standard tortoise functions.\n"
        "Documentation can be found here: https://github.com/tortoise/tortoise-cli"
    )
    pty.spawn(["tortoise-cli", "-c", "bdbot.db.TORTOISE_ORM", "shell"])


def view_requests():
    print("Here are the current requests:")
    if not os.path.exists(REQUEST_FILE_PATH):
        print("There are no requests yet")
        return
    with open(REQUEST_FILE_PATH, "r") as file:
        for line in file:
            print(f"> {line}")


def uninstall_bot():
    """Uninstall bot files"""
    if inquirer.confirm("Are you sure you want to uninstall the bot?").execute():
        return os.rmdir(BASE_DATA_PATH)
    logger.info("Canceled bot uninstallation")
    return None


def link_cache_generate():
    """Regenerate the link cache"""
    logger.info("Running link cache, please wait up to 1-2 minutes...")
    os.makedirs("data", exist_ok=True)
    asyncio.run(create_link_cache(logger))
    logger.info("Link cache created!")


async def migrate_db():
    # 1. initialize db
    print("Initializing database...")
    await dbinit()

    try:
        # 2. Load old database
        print("Loading old database...")
        old_db_path = os.path.join(DATA_PATH, "data.json")
        db = load_json(old_db_path)

        # 3. Migrate data
        print("Creating the sqlite database...")
        for server_id, server in db.items():
            if "channels" not in server:
                continue
            role_id = None
            if "role" in server:
                role_id = server["role"]

            server_ = ServerSubscription(
                id=int(server_id),
                role_id=role_id,
            )
            await server_.save()

            match_date = {
                "Mo": Weekday.Monday,
                "Tu": Weekday.Tuesday,
                "We": Weekday.Wednesday,
                "Th": Weekday.Thursday,
                "Fr": Weekday.Friday,
                "Sa": Weekday.Saturday,
                "Su": Weekday.Sunday,
                "D": Weekday.Daily,
                "La": Weekday.Latest,
            }
            for channel_id, channel in server["channels"].items():
                channel_ = ChannelSubscription(
                    id=int(channel_id), server_id=int(server_id)
                )
                await channel_.save()
                if "date" in channel:
                    for date_str, date in channel["date"].items():
                        for hour_str, hour in date.items():
                            for comic in hour:
                                if comic in [1, 20, 36, 26, 25, 24, 11]:
                                    continue
                                sub = DiscordSubscription(
                                    comic_id=comic,
                                    subscription_type=SubscriptionType.Normal,
                                    weekday=Weekday(match_date[date_str]),
                                    hour=int(hour_str),
                                    channel_id=int(channel_id),
                                )
                                await sub.save()
                if "latest" in channel:
                    for comic in channel["latest"]:
                        if comic in [1, 20, 36, 26, 25, 24, 11]:
                            continue
                        sub = await DiscordSubscription(
                            comic_id=comic,
                            subscription_type=SubscriptionType.Normal,
                            weekday=Weekday.Latest,
                            hour=-1,
                            channel_id=int(channel_id),
                        )
                        await sub.save()

    finally:
        await connections.close_all()


def migrate_v4_v5():
    # 1. Move from $HOME/.local/bdbot to $HOME/.local/share/bdbot
    if platform.system() == "Linux":
        old_path = os.path.join("/home", os.getenv("USER", ""), ".local", "bdbot")
        if os.path.exists(old_path):
            print(f"Migrating conf files from {old_path} to {PROD_DATA_PATH}...")
            shutil.move(old_path, PROD_DATA_PATH)

    # 2. Update config files
    print("Updating the configuration files...")
    refresh_conf_files()

    # 3. Migrate the database
    print("Migrating the database...")
    asyncio.run(migrate_db())

    print("Creating the link cache...")
    asyncio.run(create_link_cache(logger))
    print("Link cache created!")

    print("The 'data.json' file can now be deleted.")


def setup_bot():
    """Sets up the bot to be able to be launched"""
    os.makedirs(BASE_DATA_PATH, exist_ok=True)

    logger.info("Setting up environment variables...")

    write_env = True
    if os.path.exists(ENV_FILE):
        write_env = inquirer.confirm(
            "The file `.env` already exist. Do you want to overwrite it?"
        ).execute()

    if write_env:
        responses = []
        for envv in ENV_VARS:
            responses.append(ENV_VARS[envv][INQUIRY].execute())

        output = "\n".join(
            [f"{envv}={response}" for envv, response in zip(ENV_VARS, responses)]
        )
        usage = "w" if os.path.exists(ENV_FILE) else "x"
        with open(ENV_FILE, f"{usage}t") as f:
            f.write(output)

    logger.info("Creating folders and files...")
    os.makedirs(os.path.dirname(BACKUP_FILE_PATH), exist_ok=True)
    os.makedirs(LOGS_DIRECTORY_PATH, exist_ok=True)
    os.makedirs(os.path.dirname(DETAILS_PATH), exist_ok=True)

    if not os.path.exists(DATABASE_FILE_PATH):
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(dbinit())
        finally:
            loop.close()

    if not os.path.exists(REQUEST_FILE_PATH):
        open(REQUEST_FILE_PATH, "xt").close()

    logger.info("Copying details and footer files...")
    continue_copy = True
    if os.path.exists(DETAILS_PATH):
        continue_copy = inquirer.confirm(
            "Details file already seem present, do you want to overwrite them?"
        ).execute()

    if continue_copy:
        shutil.copy("misc/comics_details.json", DETAILS_PATH)
        shutil.copy("misc/random-footers.txt", FOOTERS_FILE_PATH)
        shutil.copy("misc/help_embeds.json", HELP_EMBED_PATH)

    logger.info("Creating link cache, this might take some time...")
    asyncio.run(create_link_cache(logger))

    if platform.system() == "Linux":
        install_linux_service()

    logger.info("All done! You can start the bot with 'python -m bdbot'!")


def install_linux_service():
    # Tries to install service file and command to run the bot only on Linux
    user = getpass.getuser()
    install_service = inquirer.confirm(
        "Do you want to install the service file which will let you run the bot automatically in the"
        f" background?\n The file will need to be copied manually at {SERVICE_PATH} with root privileges and\n"
        f" enabled with '{COMMAND}'?"
    ).execute()
    if not install_service:
        return
    dst_service_path = os.path.join(HOME_PATH, user)
    with open(LOCAL_SERVICE_PATH, "rt") as f:
        service_file = f.read()

    service_file = service_file.replace("{USER}", user)
    service_file = service_file.replace("{PACKAGE_DIRECTORY}", os.getcwd())

    with open(f"{dst_service_path}/runbdbot.service", "wt") as f:
        f.write(service_file)

    logger.info(
        f"The service file is now available at {dst_service_path} and is ready to be moved to"
        f" {SERVICE_PATH}. Do not forget to enable the service with {COMMAND}!"
    )


def manage_comics():
    """Manage comics configuration"""
    logger.info("Loading comics....")
    logger.info("Comics loaded!")
    action = None
    while action != "Return":
        comics = initialize_comics(load_json(DETAILS_PATH), base_on_error=True)
        action = inquirer.select(
            message="What do you want to do with the comics?",
            choices=["Add", "Delete", "Modify", "Return"],
            mandatory=False,
        ).execute()

        if action == "Delete" or action == "Modify":
            choose_comic(action, comics)
        elif action == "Add":
            add_comic(comics)
        elif action is None or action == "":
            action = "Return"


def choose_comic(action: str, comics: dict):
    """Choose a comic

    :param action: The action to do with the comic
    :param comics: The list of comics
    """
    comic_map = {
        f"{comic.id}. {comic.name}": comic_name for comic_name, comic in comics.items()
    }
    comic = inquirer.fuzzy(
        message=f"What comic do you want to {action.lower()}?",
        choices=[comic for comic in comic_map.keys()] + ["Return"],
        mandatory=False,
    ).execute()

    if comic is None or comic == "Return":
        return
    elif action == "Delete":
        delete(comics, comic_map[comic])
    else:
        modify(comics, comic_map[comic])


def add_comic(comics: dict[str, BaseComic]):
    """Add a comic to the list of comics.

    :param comics: The dictionary of comics
    """
    socials = ["Website", "Facebook", "Twitter", "Youtube", "Patreon", "About"]
    first_date = {"Year": 0, "Month": 0, "Day": 0}
    name = inquirer.text(
        message="What is the name of the comic? ", mandatory=False
    ).execute()
    author = inquirer.text(
        message="Who is the creator of the comic? ", mandatory=False
    ).execute()
    web_name = inquirer.text(
        message="Enter the name of the comic as it is written in the link to its main "
        "page: ",
        mandatory=False,
    ).execute()
    main_website = inquirer.text(
        message="What is the main website of the comic?",
        completer={
            website: None
            for website in [
                Gocomics.WEBSITE_NAME,
                ComicsKingdom.WEBSITE_NAME,
                Webtoons.WEBSITE_NAME,
            ]
        },
        mandatory=False,
    ).execute()

    working_type: str
    match main_website:
        case Gocomics.WEBSITE_NAME | ComicsKingdom.WEBSITE_NAME:
            working_type = WorkingType.Date.value
        case Webtoons.WEBSITE_NAME:
            working_type = WorkingType.RSS.value
        case _:
            working_type = inquirer.select(
                message="What is the working type of the comic? (For example,are comics "
                "accessible by specifying a date, a number or is there a rss "
                "available?)\nIf you do not know, please choose other. ",
                choices=[working_type.name for working_type in WorkingType],
                mandatory=False,
            ).execute()
    working_type: WorkingType = WorkingType(working_type.lower())

    description = inquirer.text(
        message="Enter a long description of the comic: ", mandatory=False
    ).execute()
    for social in socials:
        social_link: str = inquirer.text(
            message=f"Does this comic has a {social} page? (leave blank if not applicable) ",
            mandatory=False,
            default="",
        ).execute()
        if social_link.strip():
            description += f"\n{social}: {social_link}"

    if working_type == WorkingType.Date:
        for date in first_date:
            first_date[date] = inquirer.number(
                message=f"What is the first date of the comic? "
                f"Please enter the {date}: ",
                mandatory=False,
            ).execute()
        first_date = f"{first_date['Year']}-{first_date['Month']}-{first_date['Day']}"
    elif working_type in [WorkingType.Number, WorkingType.RSS]:
        first_date = "1"
    else:
        first_date = ""
    color = inquirer.text(
        message="Enter the hexadecimal code of the most represented color in this comic "
        "(without the 0x)",
        validate=lambda x: re.match("[\\dA-F]{6}", x) is not None,
        mandatory=False,
    ).execute()
    image = inquirer.text(
        message="Enter the link of a public image that represents well the comic: ",
        mandatory=False,
    ).execute()
    help_txt = inquirer.text(
        message="Write in one phrase a description of the comic.",
        validate=lambda x: 100 >= len(x),
        invalid_message="This short description must be equal or less than 100 characters!",
        mandatory=False,
    ).execute()
    last_comic_id = list(comics.values())[-1].id + 1
    final_comic_dict = process_inputs(
        name,
        author,
        web_name,
        main_website,
        working_type,
        description,
        last_comic_id,
        first_date,
        color,
        image,
        help_txt,
    )
    logger.info("Final comic data:")
    logger.info(json.dumps(final_comic_dict, indent=4))
    name = name.replace(" ", "")
    confirm = inquirer.confirm("Is the data good?").execute()
    if confirm:  # Adds the details to the file
        logger.info("Updating the details file....")
        comics.update({name: final_comic_dict})
        comics = {
            cmc: comic.to_dict() if isinstance(comic, BaseComic) else comic
            for cmc, comic in comics.items()
        }
        save_json(comics, file_path=DETAILS_PATH)
        logger.info("Update done!")
        return
    # Adds the details to a temporary file
    absolute_path = os.path.join(os.getcwd(), TEMP_FILE_PATH)
    logger.info(f"Writing dictionary to a temporary location.... ({absolute_path})")
    temp_comic_data = open_json_if_exist(absolute_path)
    temp_comic_data.update({name: final_comic_dict})
    save_json(temp_comic_data, absolute_path)
    logger.info(
        "Wrote the details to the temporary file! You can edit this file manually or with this tool!"
    )


def process_inputs(
    name: str,
    author: str,
    web_name: str,
    main_website: str,
    working_type: WorkingType,
    description: str,
    id: int,
    first_date: Union[str, dict],
    color: str,
    image: str,
    helptxt: str,
) -> dict:
    """Create the comic object

    :param name: Comic name
    :param author: Comic author
    :param web_name: Comic website
    :param main_website: Comic's main website
    :param working_type: Comic's working type
    :param description: Comic description
    :param id: Comic id
    :param first_date: Comic first date
    :param color: Comic color
    :param image: Comic image
    :param helptxt: Comic help text
    :return: The comic dict
    """
    comic_type: Type[BaseComic] = BaseComic.get_type(
        main_website, working_type, base_on_error=True
    )
    return comic_type(
        WEBSITE_NAME=comic_type.WEBSITE_NAME,
        WEBSITE_URL=comic_type.WEBSITE_URL,
        WEBSITE_HELP=comic_type.WEBSITE_HELP,
        WORKING_TYPE=comic_type.WORKING_TYPE,
        name=name,
        author=author,
        web_name=web_name,
        main_website=main_website,
        working_type=working_type.value,
        description=description,
        id=id,
        first_date=first_date,
        color=color,
        image=image,
        help=helptxt,
    ).to_dict()


def delete(comics: dict[str, BaseComic], comic_name: str):
    """Removes a comic from the main configuration file and move it to a retired configuration file.

    :param comics: Main configuration dictionary.
    :param comic_name: The comic name to remove.
    """
    comic = comics[comic_name]
    confirm = inquirer.confirm(
        message=f"Are you sure you want to delete {comic_name}?"
    ).execute()

    if not confirm:
        logger.info("Deletion aborted.")
        return

    abs_path = os.path.join(os.getcwd(), RETIRED_COMICS_PATH)
    logger.info(f"Moving comic to {abs_path} ...")
    # Retires the comic from the main config file
    retired_comic: BaseComic = comics.pop(comic_name)

    cmcs = {cmc: comic.to_dict() for cmc, comic in comics.items()}
    save_json(cmcs, DETAILS_PATH)

    retired_comics = open_json_if_exist(abs_path)  # Moves the comic
    retired_comics.update({comic_name: retired_comic.to_dict()})
    save_json(retired_comics, abs_path)
    logger.info("Deletion successful in the details file!")

    update_database = inquirer.confirm(
        message="Do you want to update the database as well? (Note: A backup will "
        "be made in case this step breaks the database.)"
    ).execute()
    if not update_database:
        logger.info("The database has not been modified.")
        return
    remove_comic_from_database(comic.id)


def open_json_if_exist(absolute_path: str) -> dict:
    """Load a JSON from a file if it exists, create it otherwise.
    :param absolute_path: The path to the dictionary
    :return: Data in the JSON file
    """
    temp_comic_data = {}
    if os.path.exists(absolute_path):
        return load_json(absolute_path)
    open(absolute_path, "x").close()
    return temp_comic_data


def remove_comic_from_database(comic_number: int):
    """Remove comic from the database, based on comic number

    :param comic_number: The comic number to remove
    """
    logger.info("Updating database....")
    save_backup(logger)

    async def update_db():
        await dbinit()
        subs = await DiscordSubscription.filter(comic_id=comic_number).delete()
        print(f"{subs} subscription(s) deleted.")
        await clean_database()

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(update_db())
    finally:
        loop.close()
    logger.info("Database update done!")


def modify(comics: dict[str, BaseComic], comic_name: str):
    """Modify a comic

    :param comics: The list of comics
    :param comic_name: The name of the comic to modify
    """
    comic_property = ""
    comic = comics[comic_name]

    while comic_property != RETURN_CHOICE:
        comic_property = inquirer.select(
            message=f"Which property of the comic {comic_name} do you want to edit?",
            choices=[prop.capitalize() for prop in comic.to_dict().keys()]
            + [RETURN_CHOICE],
            mandatory=False,
        ).execute()

        if comic_property != "" and comic_property != "Return":
            comic = modify_property(comic, comic_property.lower())

    # Saves the modifications
    comics.update({comic_name: comic})
    comics = {cmc: comic.to_dict() for cmc, comic in comics.items()}
    save_json(comics, file_path=DETAILS_PATH)


def modify_property(comic: BaseComic, comic_property: str) -> BaseComic:
    """Modify a comic's property

    :param comic: The information about the comic
    :param comic_property: The property to change
    :return: The modified comic
    """
    property_value = getattr(comic, comic_property)
    logger.info(f"Current {comic_property!r} value:\n`\n{property_value}\n`")

    completer: Optional[dict] = None
    if type(property_value) is str:
        completer = {word: None for word in property_value}

    new_value = inquirer.text(
        message="What new value do you want to give this property?",
        mandatory=False,
        completer=completer,
    ).execute()

    if new_value == "":
        logger.info(f"{comic_property!r} has not been changed.")
        return comic

    confirm = inquirer.confirm(
        message=f"Are you sure your want to set "
        f"{comic_property!r} to \n`\n{new_value}\n`\n ?"
    ).execute()

    if not confirm:
        logger.info(f"{comic_property!r} has not been changed.")
        return comic

    logger.info(f"Updating property {comic_property!r}...")
    setattr(comic, comic_property, new_value)

    return comic


def refresh_conf_files():
    """Refresh config (misc files)"""
    logger.info("Refreshing config files...")
    logger.info(
        "If you made changes to the existing config files,"
        " please stash them away because this process will crush them."
    )
    conf = inquirer.confirm("Please confirm to continue the process").execute()

    if not conf:
        logger.info("Operation aborted")
        return

    # Copy files over
    shutil.copy("misc/comics_details.json", DETAILS_PATH)
    shutil.copy("misc/random-footers.txt", FOOTERS_FILE_PATH)
    shutil.copy("misc/help_embeds.json", HELP_EMBED_PATH)


def todo():
    pass


if __name__ == "__main__":
    main()
