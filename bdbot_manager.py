import json
import logging
import os
import re
import sys

from InquirerPy import inquirer
from InquirerPy.prompts import SecretPrompt, ListPrompt
from src.utils import load_json, DETAILS_PATH, REQUEST_FILE_PATH, DATABASE_FILE_PATH, save_json, save_backup
from src.Web_requests_manager import create_link_cache
from typing import Union, Optional

TEMP_FILE_PATH = "src/misc/comics_not_ready.json"
RETIRED_COMICS_PATH = "src/misc/retired_comics.json"

logger = logging.Logger("manager_logger", logging.INFO)


def main():
    """Add, delete or modify comics in the comic details file"""
    os.chdir(os.path.dirname(__file__))  # Force the current working directory

    # Set the logging handler
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    action = ""
    while action != "Exit":
        action = inquirer.select(message="What do you want to do?", choices=["Manage bot", "Manage comics",
                                                                             "Exit"]).execute()

        if action == "Manage bot":
            manage_bot()
        elif action == "Manage comics":
            manage_comics()


def manage_bot():
    """Manage the bot and its settings"""
    action = inquirer.select(message="What do you want to do?",
                             choices=["Database tools", "Verify requests", "Create image link cache", "Setup Bot"],
                             mandatory=False).execute()

    if action == "Create image link cache":
        logger.info("Running link cache, please wait up to 1-2 minutes...")
        create_link_cache(logger)
        logger.info("Link cache created!")
    if action == "Setup Bot":
        setup_bot()


def setup_bot():
    """Sets up the bot to be able to be launched"""

    logger.info("Setting up environment variables...")

    write_env = True
    if os.path.exists("./env"):
        write_env = inquirer.confirm("The file `.env` already exist. Do you want to overwrite it?")

    if write_env:
        environment_variables: dict[str, dict[str, Union[str, Union[SecretPrompt, ListPrompt]]]] = {
            "TOKEN": {"value": "", "inquiry": inquirer.secret(message="Enter the token (The bot discord token):")},
            "CLIENT_ID": {"value": "", "inquiry": inquirer.secret(message="Enter the client ID (The bot client ID. "
                                                                          "To get a invite for the bot):")},
            "PRIVATE_CHANNEL_SUPPORT_ID": {
                "value": "",
                "inquiry": inquirer.secret(
                    message="Enter the ID of the private channel (The ID of the channel where the bot can print"
                            " debugging information):"
                )
            },
            "PRIVATE_SERVER_SUPPORT_ID": {
                "value": "",
                "inquiry": inquirer.secret(
                    message="Enter the ID of the private server (The ID of the server where the bot can allow owner "
                            "commands):"
                )
            },
            "DEBUG": {
                "value": "",
                "inquiry": inquirer.select(
                    message="Is the bot used for development purposes? (Should be False if the bot is supposed to"
                            " serve multiple servers):",
                    choices=["True", "False"]
                )
            }
        }

        for envv in environment_variables:
            environment_variables[envv]["value"] = environment_variables[envv]["inquiry"].execute()

        output = "\n".join([f"{envv}={environment_variables[envv]['value']}" for envv in environment_variables])
        usage = "w" if os.path.exists(".env") else "x"
        with open(".env", f"{usage}t") as f:
            f.write(output)

    logger.info("Creating folders and files...")
    os.makedirs("src/data/backups", exist_ok=True)
    os.makedirs("src/data/logs", exist_ok=True)

    if not os.path.exists(DATABASE_FILE_PATH):
        with open(DATABASE_FILE_PATH, "xt") as f:
            f.write("{}")

    if not os.path.exists(REQUEST_FILE_PATH):
        with open(REQUEST_FILE_PATH, "xt"):
            pass

    logger.info("Creating link cache, this might take some time...")
    create_link_cache(logger)

    logger.info("All done! You can start the bot with 'python main.py'!")


def manage_comics():
    """Manage comics configuration"""
    logger.info("Loading comics....")
    comics = load_json(DETAILS_PATH)
    logger.info("Comics loaded!")
    action = None
    while action != "Return":
        action = inquirer.select(
            message="What do you want to do with the comics?",
            choices=["Add", "Delete", "Modify", "Return"],
            mandatory=False
        ).execute()

        if action == "Delete" or action == "Modify":
            choose_comic(action, comics)
        elif action == "Add":
            add_comic(comics)
        elif action is None or action == "":
            action = "Return"


def choose_comic(action: str, comics: dict):
    comic = inquirer.fuzzy(
        message=f"What comic do you want to {action.lower()}?",
        choices=[f"{comics[x]['Position']}. {comics[x]['Name']}" for x in comics] + ["Return"],
        mandatory=False
    ).execute()

    if comic is None or comic == "Return":
        return
    elif action == "Delete":
        delete(comics, comic)
    else:
        modify(comics, comic)


def add_comic(comics: dict):
    """Add a comic to the list of comics.

    :param comics: The dictionary of comics
    """
    websites = {"Gocomics": None, "ComicsKingdom": None, "Webtoon": None}
    socials = ["Website", "Facebook", "Twitter", "Youtube", "Patreon", "About"]
    first_date = {"Year": 0, "Month": 0, "Day": 0}
    name = inquirer.text(message="What is the name of the comic? ", mandatory=False).execute()
    author = inquirer.text(message="Who is the creator of the comic? ", mandatory=False).execute()
    web_name = inquirer.text(message="Enter the name of the comic as it is written in the link to its main "
                                     "page: ", mandatory=False).execute()
    main_website = inquirer.text(message="What is the main website of the comic?",
                                 completer={"Gocomics": None, "ComicsKingdom": None, "Webtoon": None},
                                 mandatory=False).execute()
    if main_website not in websites:
        working_type = inquirer.select(message="What is the working type of the comic? (For example,are comics "
                                               "accessible by specifying a date, a number or is there a rss "
                                               "available?)\nIf you do not know, please choose other. ",
                                       choices=["date", "number", "rss", "other"], mandatory=False).execute()
    elif main_website == "Gocomics" or main_website == "ComicsKingdom":
        working_type = "date"
    else:
        working_type = "rss"

    description = inquirer.text(message="Enter a long description of the comic: ", mandatory=False).execute()
    for social in socials:
        social_link: str = inquirer.text(
            message=f"Does this comic has a {social} page? (leave blank if not applicable) ",
            mandatory=False,
            default="").execute()
        if social_link.strip():
            description += f"\n{social}: {social_link}"

    if working_type == "date":
        for date in first_date:
            first_date[date] = inquirer.number(message=f"What is the first date of the comic? "
                                                       f"Please enter the {date}: ", mandatory=False).execute()
    elif working_type == "number" or working_type == "rss":
        first_date = "1"
    else:
        first_date = ""
    color = inquirer.text(message="Enter the hexadecimal code of the most represented color in this comic "
                                  "(without the 0x)",
                          validate=lambda x: re.match("[\\dA-F]{6}", x) is not None, mandatory=False).execute()
    image = inquirer.text(message="Enter the link of a public image that represents well the comic: ").execute()
    helptxt = inquirer.text(message="Write in one phrase a description of the comic.",
                            validate=lambda x: 100 >= len(x),
                            invalid_message="This short description must be equal or less than 100 characters!",
                            mandatory=False).execute()
    final_comic_dict = process_inputs(name, author, web_name, main_website, working_type, description, len(comics),
                                      first_date, color, image, helptxt)
    logger.info("Final comic data:")
    logger.info(json.dumps(final_comic_dict, indent=4))
    confirm = inquirer.confirm("Is the data good?").execute()
    if confirm:  # Adds the details to the file
        logger.info("Updating the details file....")
        comics.update(final_comic_dict)
        save_json(comics, file_path=DETAILS_PATH)
        logger.info("Update done!")

        # Create a command
        logger.info("Creating command...")
        command = create_command(final_comic_dict)
        logger.info("Here is your command:\n'''")
        logger.info(command)
        logger.info(f"'''\nAdd it to the end of {os.getcwd()}/src/Scripts/Comic.py to make the comic executable.")
    else:  # Adds the details to a temporary file
        absolute_path = os.getcwd() + "/" + TEMP_FILE_PATH
        logger.info(f"Writing dictionary to a temporary location.... ({absolute_path})")
        temp_comic_data = open_json_if_exist(absolute_path)
        temp_comic_data.update(final_comic_dict)
        save_json(temp_comic_data, absolute_path)
        logger.info("Wrote the details to the temporary file! You can edit this file manually or with this tool!")


def process_inputs(name: str, author: str, web_name: str, main_website: str, working_type: str, description: str,
                   position: int, first_date: Union[str, dict], color: str, image: str, helptxt: str) -> dict:
    """

    :param name:
    :param author:
    :param web_name:
    :param main_website:
    :param working_type:
    :param description:
    :param position:
    :param first_date:
    :param color:
    :param image:
    :param helptxt:
    :return:
    """
    websites = {
        "Gocomics": "https://www.gocomics.com/",
        "ComicsKingdom": "https://comicskingdom.com/",
        "Webtoon": "https://www.webtoons.com/en/"
    }
    normalized_name = name.replace(" ", "")
    return {
        normalized_name: {
            "Name": name,
            "Author": author,
            "Web_name": web_name,
            "Main_website": websites[main_website] if main_website in websites else main_website,
            "Working_type": working_type,
            "Description": description,
            "Position": position,
            "First_date": first_date if type(first_date) is str else f"{first_date['Year']}, {first_date['Month']}, "
                                                                     f"{first_date['Day']}",
            "Color": color,
            "Image": image,
            "Helptxt": helptxt
        }
    }


def create_command(cmc: dict) -> str:
    """

    :param cmc:
    :return:
    """
    comic = cmc.get(list(cmc.keys())[0])
    normalized_name = comic['Name'].replace(" ", "_").lower()
    return f"""
    @commands.hybrid_command()
    async def {normalized_name}(self, ctx: discord.ext.commands.Context, use: str = None, date: str = None,
                                hour: str = None):
        \"\"\"{comic['Name']}\"\"\"
        comic_name = '{comic['Name'].replace(" ", "")}'

        # Interprets the parameters given by the user
        await utils.parameters_interpreter(ctx, utils.get_strip_details(comic_name), param=use, date=date, hour=hour)
    """


def delete(comics: dict, comic: str):
    """
    Removes a comic from the main configuration file and move it to a retired configuration file.

    :param comics: Main configuration dictionary.
    :param comic: The comic to remove.
    """
    comic_number, comic_name = comic.split(". ")
    comic_number = int(comic_number)
    confirm = inquirer.confirm(message=f"Are you sure you want to delete {comic_name}?").execute()

    if confirm:
        abs_path = os.getcwd() + "/" + RETIRED_COMICS_PATH
        logger.info(f"Moving comic to {abs_path} ...")
        # Retires the comic from the main config file
        comic_name = list(comics.keys())[comic_number]
        retired_comic: dict = comics.pop(comic_name)

        logger.info("Changing positions of the next comics...")
        for cmc in comics:
            pos = comics[cmc]["Position"]
            comics[cmc]["Position"] = pos - 1 if pos > comic_number else pos

        save_json(comics, DETAILS_PATH)

        retired_comics = open_json_if_exist(abs_path)  # Moves the comic
        retired_comics.update({comic_name: retired_comic})
        save_json(retired_comics, abs_path)
        logger.info("Deletion successful in the details file!")

        update_database = inquirer.confirm(message="Do you want to update the database as well? (Note: A backup will "
                                                   "be made in case this step breaks the database.)").execute()
        if update_database:
            database_update(comic_number)
        else:
            logger.info("The database has not been modified.")

    else:
        logger.info("Deletion aborted.")


def open_json_if_exist(absolute_path: str) -> dict:
    """
    Load a json from a file if it exists, create it otherwise.

    :param absolute_path: The path to the
    :return: The dictionary of data in the json file
    """
    temp_comic_data = {}
    if os.path.exists(absolute_path):
        return load_json(absolute_path)
    else:
        open(absolute_path, 'x').close()
        return temp_comic_data


def database_update(comic_number: int):
    """

    :param comic_number:
    :return:
    """
    logger.info("Updating database....")
    data = open_json_if_exist(DATABASE_FILE_PATH)
    comic_number_remove = comic_number  # the comic number to remove
    save_backup(data, logger)
    # Removes a comic permanently
    for gid in data:
        guild = data[gid]
        for channel in guild["channels"]:
            channel_data = guild["channels"][channel]
            for date in channel_data["date"]:
                date_data = channel_data["date"][date]
                for hour in date_data:
                    hour_data: list = date_data[hour]
                    if comic_number_remove in hour_data:
                        hour_data.remove(comic_number_remove)

                    new_hour_data = []
                    for cmc_nb in hour_data:
                        if cmc_nb > comic_number_remove:
                            new_hour_data.append(cmc_nb - 1)
                        else:
                            new_hour_data.append(cmc_nb)
                    data[gid]["channels"][channel]["date"][date][hour] = new_hour_data

    save_json(data)
    logger.info("Database update done!")


def modify(comics: dict, comic: str):
    """

    :param comics:
    :param comic:
    :return:
    """
    comic_property: str = ""
    comic_number, comic_name = comic.split(". ")
    comic_number = int(comic_number)
    comic_dict_key = list(comics.keys())[comic_number]
    comic_dict = comics[comic_dict_key]

    while comic_property != "Return":
        comic_property = inquirer.select(message=f"Which comic_property of the comic {comic_name} do you want to edit?",
                                         choices=[prop for prop in comic_dict] + ["Return"], mandatory=False).execute()

        if comic_property != "" and comic_property != "Return":
            comic_dict = modify_property(comic_dict, comic_property)

    # Saves the modifications
    comics.update({comic_dict_key: comic_dict})
    save_json(comics, file_path=DETAILS_PATH)


def modify_property(comic_dict: dict, comic_property: str) -> dict:
    """

    :param comic_dict:
    :param comic_property:
    :return:
    """
    property_value = comic_dict[comic_property]
    logger.info(f"Current {comic_property!r} value:\n`\n{comic_dict[comic_property]}\n`")

    completer: Optional[dict] = None
    if type(property_value) is str:
        completer = {word: None for word in property_value}

    new_value = inquirer.text(message="What new value do you want to give this property?", mandatory=False,
                              completer=completer).execute()

    if new_value == "":
        logger.info(f"{comic_property!r} has not been changed.")
    else:
        confirm = inquirer.confirm(message=f"Are you sure your want to set "
                                           f"{comic_property!r} to \n`\n{new_value}\n` ?").execute()

        if confirm:
            logger.info(f"Updating property {comic_property!r}...")
            comic_dict.update({comic_property: new_value})
        else:
            logger.info(f"{comic_property!r} has not been changed.")

    return comic_dict


if __name__ == "__main__":
    main()
