import json
import os
import re

from InquirerPy import inquirer
from src.utils import load_json, DETAILS_PATH, save_json
from typing import Union

TEMP_FILE_PATH = "src/misc/comics_not_ready.json"
RETIRED_COMICS_PATH = "src/misc/retired_comics.json"


def main():
    """
    Add, delete or modify comics in the comic details file.
    """
    print("Loading comics....")
    comics = load_json(DETAILS_PATH)
    print("Comics loaded!")
    action = None
    while action is None:
        action = inquirer.select(
            message="What do you want to do with the comics?",
            choices=["Add", "Delete", "Modify", "Exit"]
        ).execute()
        if action != "Exit":
            choose_comic(action, comics)
            action = None


def choose_comic(action: str, comics: dict):
    if action == "Add":
        add_comic(comics)
    else:
        comic = inquirer.fuzzy(
            message=f"What comic do you want to {action.lower()}?",
            choices=[f"{comics[x]['Position']}. {comics[x]['Name']}" for x in comics]
        ).execute()

        if action == "Delete":
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
    name = inquirer.text(message="What is the name of the comic? ").execute()
    author = inquirer.text(message="Who is the creator of the comic? ").execute()
    web_name = inquirer.text(message="Enter the name of the comic as it is written in the link to its main "
                                     "page: ").execute()
    main_website = inquirer.text(message="What is the main website of the comic?",
                                 completer={"Gocomics": None, "ComicsKingdom": None, "Webtoon": None}).execute()
    if main_website not in websites:
        working_type = inquirer.select(message="What is the working type of the comic? (For exemplee,are comics "
                                               "accessible by specifying a date, a number or is there a rss "
                                               "available?)\nIf you do not know, please choose other. ",
                                       choices=["date", "number", "rss", "other"]).execute()
    elif main_website == "Gocomics" or main_website == "ComicsKingdom":
        working_type = "date"
    else:
        working_type = "rss"

    description = inquirer.text(message="Enter a long description of the comic: ").execute()
    for social in socials:
        social_link = inquirer.text(
            message=f"Does this comic has a {social} page? (leave blank if not applicable) ").execute()
        if social_link != "":
            description += f"\n{social}: {social_link}"

    if working_type == "date":
        for date in first_date:
            first_date[date] = inquirer.number(message=f"What is the first date of the comic? "
                                                       f"Please enter the {date}: ").execute()
    elif working_type == "number" or working_type == "rss":
        first_date = "1"
    else:
        first_date = ""
    color = inquirer.text(message="Enter the hexadecimal code of the most represented color in this comic "
                                  "(without the 0x)",
                          validate=lambda x: re.match("[1-9|A-f]{6}", x) is not None).execute()
    image = inquirer.text(message="Enter the link of a public image that represents well the comic: ").execute()
    helptxt = inquirer.text(message="Write in one phrase a description of the comic.",
                            validate=lambda x: 50 > len(x),
                            invalid_message="This short description must be less than 50 characters!").execute()
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

        print("Creating ")

    else:  # Adds the details to a temporary file
        absolute_path = os.getcwd() + "\\" + TEMP_FILE_PATH
        temp_comic_data = {}
        print(f"Writing dictionary to a temporary location.... ({absolute_path})")
        if os.path.exists(absolute_path):
            temp_comic_data = load_json(absolute_path)
        else:
            open(absolute_path, 'x').close()
        temp_comic_data.update(final_comic_dict)
        save_json(temp_comic_data, absolute_path)
        print("Wrote the details to the temporary file! You can edit this file manually or still with this tool!")


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
            "Main_website": getattr(websites, main_website, main_website),
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


def create_command():
    pass


def delete(comics: dict, comic: str):
    pass


def modify(comics: dict, comic: str):
    pass


if __name__ == "__main__":
    main()
