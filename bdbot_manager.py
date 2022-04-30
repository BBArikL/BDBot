import json
import os
import re

from InquirerPy import inquirer
from src.utils import load_json, DETAILS_PATH, save_json, DATABASE_FILE_PATH, save_backup, create_link_cache
from typing import Union, Optional

TEMP_FILE_PATH = "src/misc/comics_not_ready.json"
RETIRED_COMICS_PATH = "src/misc/retired_comics.json"


def main():
    """
    Add, delete or modify comics in the comic details file.
    """
    os.chdir(os.path.dirname(__file__))  # Force the current working directory
    action = ""
    while action != "Exit":
        action = inquirer.select(message="What do you want to do?", choices=["Manage bot", "Manage comics",
                                                                             "Exit"]).execute()

        if action == "Manage bot":
            manage_bot()
        elif action == "Manage comics":
            manage_comics()


def manage_bot():
    action = inquirer.select(message="What do you want to do?",
                             choices=["Verify Database", "Verify requests", "Create image link cache", "Setup Bot"],
                             mandatory=False).execute()

    if action == "Create image link cache":
        print("Running link cache, please wait up to 1-2 minutes...")
        create_link_cache()
        print("Link cache created!")
    if action == "Setup Bot":
        setup_bot()


def manage_comics():
    print("Loading comics....")
    comics = load_json(DETAILS_PATH)
    print("Comics loaded!")
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
    :return:
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
        working_type = inquirer.select(message="What is the working type of the comic? (For exemplee,are comics "
                                               "accessible by specifying a date, a number or is there a rss "
                                               "available?)\nIf you do not know, please choose other. ",
                                       choices=["date", "number", "rss", "other"], mandatory=False).execute()
    elif main_website == "Gocomics" or main_website == "ComicsKingdom":
        working_type = "date"
    else:
        working_type = "rss"

    description = inquirer.text(message="Enter a long description of the comic: ", mandatory=False).execute()
    for social in socials:
        social_link = inquirer.text(
            message=f"Does this comic has a {social} page? (leave blank if not applicable) ", mandatory=False).execute()
        if social_link != "" or social_link is not None:
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
                          validate=lambda x: re.match("[0-9A-F]{6}", x) is not None, mandatory=False).execute()
    image = inquirer.text(message="Enter the link of a public image that represents well the comic: ").execute()
    helptxt = inquirer.text(message="Write in one phrase a description of the comic.",
                            validate=lambda x: 50 > len(x),
                            invalid_message="This short description must be less than 50 characters!",
                            mandatory=False).execute()
    final_comic_dict = process_inputs(name, author, web_name, main_website, working_type, description, len(comics) + 1,
                                      first_date, color, image, helptxt)
    print("Final comic data:")
    print(json.dumps(final_comic_dict, indent=4))
    confirm = inquirer.confirm("Is the data good?").execute()
    if confirm:  # Adds the details to the file
        print("Updating the details file....")
        comics.update(final_comic_dict)
        save_json(comics, file_path=DETAILS_PATH)
        print("Update done!")

        # Create a command
        print("Creating command...")
        command = create_command(final_comic_dict)
        print("Here is your command:\n'''")
        print(command)
        print(f"'''\nAdd it to the end of {os.getcwd()}/src/Scripts/Comic.py to make the comic executable.")
    else:  # Adds the details to a temporary file
        absolute_path = os.getcwd() + "/" + TEMP_FILE_PATH
        print(f"Writing dictionary to a temporary location.... ({absolute_path})")
        temp_comic_data = open_json_if_exist(absolute_path)
        temp_comic_data.update(final_comic_dict)
        save_json(temp_comic_data, absolute_path)
        print("Wrote the details to the temporary file! You can edit this file manually or with this tool!")


def process_inputs(name: str, author: str, web_name: str, main_website: str, working_type: str, descritption: str,
                   position: int, first_date: Union[str, dict], color: str, image: str, helptxt: str) -> dict:
    websites = {
        "Gocomics": "https://www.gocomics.com/",
        "ComicsKngdom": "https://comicskingdom.com/",
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
            "Description": descritption,
            "Position": position,
            "First_date": first_date if type(first_date) is str else f"{first_date['Year']}, {first_date['Month']}, "
                                                                     f"{first_date['Day']}",
            "Color": color,
            "Image": image,
            "Aliases": f"'{normalized_name}', '{normalized_name.lower()}', '{normalized_name[:3]}', "
                       f"'{normalized_name[:3].lower()}'",
            "Helptxt": helptxt
        }
    }


def create_command(cmc: dict):
    comic = cmc.get(list(cmc.keys())[0])
    normalized_name = comic['Name'].replace(" ", "")
    return f"""
    @commands.command(aliases=[{comic['Aliases']}])
    async def {normalized_name}(self, ctx, use=None, date=None, hour=None):
        comic_name = '{normalized_name}'

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
        print(f"Moving comic to {abs_path} ...")
        # Retires the comic from the main config file
        comic_name = list(comics.keys())[comic_number]
        retired_comic: dict = comics.pop(comic_name)

        print("Changing positions of the next comics...")
        for cmc in comics:
            pos = comics[cmc]["Position"]
            comics[cmc]["Position"] = pos - 1 if pos > comic_number else pos

        save_json(comics, DETAILS_PATH)

        retired_comics = open_json_if_exist(abs_path)  # Moves the comic
        retired_comics.update({comic_name: retired_comic})
        save_json(retired_comics, abs_path)
        print("Deletion successful in the details file!")

        update_database = inquirer.confirm(message="Do you want to update the database as well? (Note: A backup will "
                                                   "be made in case this step breaks the database.)").execute()
        if update_database:
            database_update(comic_number)
        else:
            print("The database has not been modified.")

    else:
        print("Deletion aborted.")


def open_json_if_exist(absolute_path: str):
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
    print("Updating database....")
    data = open_json_if_exist(DATABASE_FILE_PATH)
    comic_number_remove = comic_number  # the comic number to remove
    save_backup(data)
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
    print("Database update done!")


def modify(comics: dict, comic: str):
    property: str = ""
    comic_number, comic_name = comic.split(". ")
    comic_number = int(comic_number)
    comic_dict_key = list(comics.keys())[comic_number]
    comic_dict = comics[comic_dict_key]

    while property != "Return":
        property = inquirer.select(message=f"Which property of the comic {comic_name} do you want to edit?",
                                   choices=[prop for prop in comic_dict]+["Return"], mandatory=False).execute()

        if property != "" and property != "Return":
            comic_dict = modify_property(comic_dict, property)

    # Saves the modifications
    comics.update({comic_dict_key: comic_dict})
    save_json(comics, file_path=DETAILS_PATH)


def modify_property(comic_dict: dict, property: str) -> dict:
    property_value = comic_dict[property]
    print(f"Current {property!r} value:\n`\n{comic_dict[property]}\n`")

    completer: Optional[dict] = None
    if type(property_value) is str:
        completer = {word: None for word in property_value}

    new_value = inquirer.text(message="What new value do you want to give this property?", mandatory=False,
                              completer=completer).execute()

    if new_value == "":
        print(f"{property!r} has not been changed.")
    else:
        confirm = inquirer.confirm(message=f"Are you sure your want to set "
                                   f"{property!r} to \n`\n{new_value}\n` ?").execute()

        if confirm:
            print(f"Updating property {property!r}...")
            comic_dict.update({property: new_value})
        else:
            print(f"{property!r} has not been changed.")

    return comic_dict


def setup_bot():
    pass


if __name__ == "__main__":
    main()