import json
import logging
from datetime import date, datetime, timedelta
from typing import Optional, Union
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from bdbot.actions import Action, ExtendedAction
from bdbot.files import COMIC_LATEST_LINKS_PATH, DETAILS_PATH, load_json, save_json
from bdbot.utils import Date, check_if_latest_link, get_link, link_cache

logger = logging.getLogger("discord")

# Utilities for web requests to have the fresh comic details

ORIGINAL_DETAILS = {
    "url": "",
    "Name": "",
    "title": "",
    "author": "",
    "day": "",
    "month": "",
    "year": "",
    "sub_img_url": "",
    "img_url": "",
    "alt": "",
    "color": 0,
    "is_latest": False,
}
MAX_TRIES = 15


def create_link_cache(logger_: logging.Logger) -> None:
    """Create a cache of links containing the latest comics links

    :param logger_: The logger to use
    """
    logger_.debug("Running link cache...")
    comics: dict = load_json(DETAILS_PATH)
    for comic in comics:
        logger_.debug(f"Getting image link for comic {comic} ...")
        comic_url: Optional[dict[str, str]]
        try:
            comic_url = get_new_comic_details(comics[comic], action=Action.Today)
        except (ValueError, AttributeError) as e:
            logger_.error(f"An error occurred for comic {comic}: {e}")
            comic_url = None
        link_cache.update(
            {
                comics[comic]["Name"]: (
                    comic_url["img_url"] if comic_url is not None else ""
                )
            }
        )

    logger_.debug("Saving comics link...")
    save_json(link_cache, COMIC_LATEST_LINKS_PATH)


def get_new_comic_details(
    strip_details: dict,
    action: Union[Action, ExtendedAction],
    comic_date: Optional[Union[datetime, int]] = None,
    latest_check: Optional[bool] = False,
) -> Optional[dict[str, Union[str, int, bool]]]:
    """Gets the comics details from the internet

    :param strip_details:
    :param action:
    :param comic_date:
    :param latest_check:
    :return:
    """
    working_type = strip_details["Working_type"]
    comic_details: Optional[dict[str, str]]
    if working_type == "date":  # Specific manager for date comics website
        comic_details = get_comic_info_date(
            strip_details,
            action=action,
            comic_date=comic_date,
            latest_check=latest_check,
        )
    elif working_type == "rss":  # Works by rss
        comic_details = get_comic_info_rss()
    else:  # Works by number
        comic_details = get_comic_info_number(
            strip_details, action=action, latest_check=latest_check
        )
    return comic_details


def get_comic_info_date(
    strip_details,
    action: Union[Action, ExtendedAction] = None,
    comic_date: Date = None,
    latest_check: bool = False,
) -> Optional[dict[str, str]]:
    """Get the details of comics which site works by date

    :param strip_details:
    :param action:
    :param comic_date:
    :param latest_check:
    :return:
    """
    details = ORIGINAL_DETAILS.copy()
    random_date = None

    details["Name"] = strip_details["Name"]
    details["author"] = strip_details["Author"]

    if strip_details is not None:
        i = 0

        if comic_date is None:
            # Gets today date
            comic_date = date.today()

        while i < MAX_TRIES and (
            details["img_url"] == "" or details["img_url"] is None
        ):
            i += 1
            if action != Action.Random:
                details["day"] = comic_date.strftime("%d")
                details["month"] = comic_date.strftime("%m")
                details["year"] = comic_date.strftime("%Y")

                # Gets today /  url
                details["url"] = get_link(strip_details, comic_date)

            # TODO: Fix here
            # else:
            # Random comic
            #    details["url"], random_date = get_random_link(strip_details)

            # Get the html of the comic site
            try:
                html = urlopen(details["url"]).read()
            except HTTPError as e:
                logger.error(f"An html error occurred: {e}")
                html = None

            if html is not None or html != "":
                # Extracts the title of the comic
                details["title"] = extract_meta_content(html, "title")

                # Finds the url of the image
                details["img_url"] = extract_meta_content(html, "image")

                # Finds the final url
                details["url"] = extract_meta_content(html, "url")

                if details["img_url"] is None:  # Go back one day
                    comic_date = comic_date - timedelta(days=1)

            if i >= MAX_TRIES and details["img_url"] is None:
                # If it hasn't found anything
                return None

        if details is not None:
            finalize_comic(strip_details, details, latest_check)

            # Finds the date of the random comic
            if details["day"] == "":
                final_date: datetime
                if random_date is None:
                    # We have to parse the string (Only gocomics)
                    final_date = datetime.strptime(
                        details["url"].replace(
                            f'https://www.gocomics.com/{strip_details["Web_name"]}/', ""
                        ),
                        "%Y/%m/%d",
                    )
                else:
                    final_date = random_date

                details["day"] = final_date.strftime("%d")
                details["month"] = final_date.strftime("%m")
                details["year"] = final_date.strftime("%Y")
    else:
        return None

    return details


def extract_meta_content(html, content) -> Optional[str]:
    """Extract the image source of the comic

    Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py

    :param html:
    :param content:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")
    content_meta = soup.find(
        "meta", attrs={"property": f"og:{content}", "content": True}
    )

    if content_meta is not None:  # If it finds the meta properties of the image
        content_value = content_meta["content"]

        return content_value
    else:
        return None


def get_comic_info_number(
    strip_details,
    action: Union[Action, ExtendedAction] = None,
    latest_check=False,
):
    """For sites which works by number

    :param strip_details:
    :param action:
    :param latest_check:
    :return:
    """
    details = ORIGINAL_DETAILS.copy()

    details["Name"] = strip_details["Name"]
    details["author"] = strip_details["Author"]

    if strip_details["Name"] is not None:
        main_website = strip_details["Main_website"]

        if strip_details["Name"] == "xkcd":
            if action == Action.Random:
                # Link for random XKCD comic
                main_website = "https://c.xkcd.com/random/comic/"
                html = urlopen(main_website).read()
                main_website = extract_meta_content(html, "url")

            main_website = main_website + "info.0.json"
            details["url"] = main_website

        elif strip_details["Name"] == "Cyanide and Happiness":
            if action == Action.Random:
                main_website += "random"
            elif action == Action.Today:
                main_website += "latest"

            details["url"] = main_website

        else:
            html = urlopen(main_website).read()
            details["url"] = extract_meta_content(html, "url")

        # Get the html of the comic site
        try:
            html = urlopen(details["url"]).read()
        except HTTPError as e:
            logger.error(f"An html error occurred: {e}")
            html = None

        if html is not None:
            if strip_details["Name"] == "Cyanide and Happiness":
                # Cyanide and Happiness special extractor
                # heavily inspired by https://github.com/JTexpo/Robobert
                # Parse the json that is embedded into the end of the page
                soup = BeautifulSoup(html, "html.parser")
                dat = soup.find("script", id="__NEXT_DATA__").get_text()

                js = json.loads(dat)

                urql_states = js["props"]["pageProps"]["urqlState"]

                for state_id in urql_states:
                    # Bruteforce the json entries to find the one contains the content of the comic
                    state_data = urql_states[state_id]
                    middle_data = json.loads(state_data["data"])

                    if "comic" in middle_data:
                        comdata = middle_data["comic"]

                        comic_det = comdata["comicDetails"]
                        author_det = comic_det["author"]["authorDetails"]

                        details["url"] = f"https://explosm.net/comics/{comdata['slug']}"

                        details["title"] = comdata["title"]

                        # Legacy comics
                        if "comicmgurl" in comic_det:
                            details["img_url"] = comic_det["comicmgurl"]
                        else:
                            # modern comics
                            details["img_url"] = comic_det["comicimgstaticbucketurl"][
                                "mediaItemUrl"
                            ]

                        details["author"] = author_det["name"]
                        details["sub_img_url"] = author_det["image"]["mediaItemUrl"]

                        post_date = datetime.strptime(
                            comdata["date"], "%Y-%m-%dT%H:%M:%S"
                        )

                        details["day"] = post_date.day
                        details["month"] = post_date.month
                        details["year"] = post_date.year
                        break

            elif strip_details["Name"] == "xkcd":
                # XKCD special extractor
                # We requested a json and not a html
                json_details = json.loads(html)

                details["title"] = json_details["title"]
                details["url"] = details["url"].replace("info.0.json", "")
                details["img_url"] = json_details["img"]
                details["alt"] = json_details["alt"]
                details["day"] = json_details["day"]
                details["month"] = json_details["month"]
                details["year"] = json_details["year"]
            else:
                # General extractor

                details["url"] = extract_meta_content(html, "url")

                details["title"] = extract_meta_content(html, "title")

                details["img_url"] = extract_meta_content(html, "image")
        else:
            return None

        if details is not None:
            finalize_comic(strip_details, details, latest_check)

    else:
        return None

    return details


def get_comic_info_rss() -> Optional[dict[str, str]]:
    """For comics which can only be found by rss

    :return:
    """
    # Details of the comic

    return ORIGINAL_DETAILS.copy()


def finalize_comic(strip_details: dict, details: dict, latest_link: bool) -> None:
    """

    :param strip_details:
    :param details:
    :param latest_link:
    :return:
    """
    details["color"] = int(strip_details["Color"], 16)
    if latest_link:
        details["is_latest"] = check_if_latest_link(details["Name"], details["img_url"])
