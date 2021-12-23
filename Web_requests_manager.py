from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
from rss_parser import Parser
from requests import get
from randomtimestamp import randomtimestamp
import json
import random
import utils

# Class that makes the web requests to have the fresh comic details

ORIGINAL_DETAILS = {"url": "", "Name": "", "title": "", "author": "", "day": "", "month": "", "year": "",
                    "sub_img_url": "", "img_url": "", "alt": "", "color": 0}
MAX_TRIES = 15


# Only gets the new comic details
def get_new_comic_details(strip_details, param, comic_date=None):
    working_type = strip_details["Working_type"]
    if working_type == 'date':
        # Specific manager for date comics website
        comic_details = get_comic_info_date(strip_details, param=param, comic_date=comic_date)
    elif working_type == 'rss':
        comic_details = get_comic_info_rss(strip_details, param=param, comic_date=comic_date)
    else:  # Works by number
        comic_details = get_comic_info_number(strip_details, param=param)
    return comic_details


# Get the details of comics which site works by date
def get_comic_info_date(strip_details, param=None, comic_date=None):
    details = ORIGINAL_DETAILS.copy()
    random_date = None

    details["Name"] = strip_details["Name"]
    details["author"] = strip_details["Author"]

    if strip_details is not None:
        i = 0

        if comic_date is None:
            # Gets today date
            comic_date = date.today()

        while i < MAX_TRIES and (details["img_url"] == "" or details["img_url"] is None):
            i += 1
            if param != "random":
                details["day"] = comic_date.strftime("%d")
                details["month"] = comic_date.strftime("%m")
                details["year"] = comic_date.strftime("%Y")

                # Gets today /  url
                details["url"] = get_link(strip_details, comic_date)

            else:
                # Random comic
                details["url"], random_date = get_random_link(strip_details)

            # Get the html of the comic site
            try:
                html = urlopen(details["url"]).read()
            except HTTPError:
                html = None

            # Extracts the title of the comic
            details["title"] = extract_meta_content(html, 'title')

            # Finds the url of the image
            details["img_url"] = extract_meta_content(html, 'image')

            # Finds the final url
            details["url"] = extract_meta_content(html, 'url')

            if details["img_url"] is None:  # Go back one day
                comic_date = comic_date - timedelta(days=1)

            if i >= MAX_TRIES and details["img_url"] is None:  # If it hasn't found anything
                return None

        if details is not None:
            details["color"] = int(strip_details["Color"], 16)

            # Finds the date of the random comic
            if details['day'] == "":
                final_date = None
                if random_date is None:
                    # We have to parse the string (Only gocomics)
                    final_date = datetime.strptime(
                        details["url"].replace(f'https://www.gocomics.com/{strip_details["Web_name"]}/', ""),
                        "%Y/%m/%d")
                else:
                    final_date = random_date

                details["day"] = final_date.strftime("%d")
                details["month"] = final_date.strftime("%m")
                details["year"] = final_date.strftime("%Y")
    else:
        return None

    return details


def get_link(strip_details, day):  # Returns the comic url
    date_formatted = ""
    middle_params = ""
    if strip_details["Main_website"] == "https://www.gocomics.com/":
        date_formatted = day.strftime("%Y/%m/%d")
        middle_params = strip_details["Web_name"]
    elif strip_details["Main_website"] == "https://comicskingdom.com/":
        date_formatted = day.strftime("%Y-%m-%d")
        middle_params = strip_details["Web_name"]
    elif strip_details["Main_website"] == "https://dilbert.com/":
        date_formatted = day.strftime("%Y-%m-%d")
        middle_params = "strip"

    return f'{strip_details["Main_website"]}{middle_params}/{date_formatted}'


def get_random_link(strip_details):  # Returns the random comic url
    if strip_details["Main_website"] == "https://www.gocomics.com/":
        return f'{strip_details["Main_website"]}random/{strip_details["Web_name"]}', None
    else:
        first_date = datetime.strptime(utils.get_first_date(strip_details), "%Y, %m, %d")
        random_date = randomtimestamp(start=first_date,
                                      end=datetime.today().replace(hour=0, minute=0, second=0,
                                                                   microsecond=0))
        middle_params = ""
        if strip_details["Main_website"] == "https://comicskingdom.com/":
            middle_params = strip_details["Web_name"]
        elif strip_details["Main_website"] == "https://dilbert.com/":
            middle_params = "strip"

        return f'{strip_details["Main_website"]}{middle_params}/{random_date.strftime("%Y-%m-%d")}', random_date


def extract_meta_content(html, content):
    # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
    # Extract the image source of the comic
    # Problem : Since the bot is hosted on replit, the site can be at a date where the comic is not accessible
    soup = BeautifulSoup(html, "html.parser")
    content_meta = soup.find('meta', attrs={'property': f'og:{content}', 'content': True})

    if content_meta is not None:  # If it finds the meta properties of the image
        content_value = content_meta['content']

        return content_value
    else:
        return None


# For sites which works by number
def get_comic_info_number(strip_details, param=None):
    # Details of the comic
    details = ORIGINAL_DETAILS.copy()

    details["Name"] = strip_details["Name"]
    details["author"] = strip_details["Author"]

    if strip_details["Name"] is not None:
        main_website = strip_details["Main_website"]

        if strip_details["Name"] == 'xkcd':
            if param == "random":
                # Link for random XKCD comic
                main_website = "https://c.xkcd.com/random/comic/"
                html = urlopen(main_website).read()
                main_website = extract_meta_content(html, 'url')

            main_website = main_website + "info.0.json"
            details["url"] = main_website

        elif strip_details["Name"] == 'Cyanide and Happiness':
            if param == 'random':
                main_website += param
            elif param == 'today':
                main_website += 'latest'

            details["url"] = main_website

        else:
            html = urlopen(main_website).read()
            details["url"] = extract_meta_content(html, 'url')

        # Gets today date
        if param == "today":
            d = date.today()
            details["day"] = d.strftime("%d")
            details["month"] = d.strftime("%m")
            details["year"] = d.strftime("%Y")

        # Get the html of the comic site
        try:
            html = urlopen(details["url"]).read()
        except HTTPError:
            html = None

        if strip_details["Name"] != 'xkcd':
            # General extractor
            if html is not None:
                details["url"] = extract_meta_content(html, 'url')

                details["title"] = extract_meta_content(html, 'title')

                details["img_url"] = extract_meta_content(html, 'image')

                details = None # TODO fix CYANIDE AND HAPPINESS
            else:
                return None

        else:
            if html is not None:
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
                return None
        if details is not None:
            details["color"] = int(strip_details["Color"], 16)
    else:
        return None

    return details

    # --- End of OtherSiteManager ---#


# For comics which can only be found by rss
def get_comic_info_rss(strip_details, param=None, comic_date=None):
    # Details of the comic
    fall_back_img = ""
    rss_site = ""
    max_entries = 19  # Max entries for rss files : 20
    details = ORIGINAL_DETAILS.copy()
    comic_nb = 0

    details["Name"] = strip_details["Name"]
    details["author"] = strip_details["Author"]
    main_website = strip_details["Main_website"]

    if main_website == 'https://garfieldminusgarfield.net/':
        fall_back_img = 'https://64.media.tumblr.com/avatar_02c53466ae58_64.gif'
        rss_site = 'https://garfieldminusgarfield.net/rss'
    else:
        main_website += strip_details["Web_name"]
        fall_back_img = strip_details["Image"]
        rss_site = main_website.replace("list", "rss")

    # Gets today date
    if param == "today":
        # First comic in the rss feed
        comic_nb = 0
    elif param == 'random':
        comic_nb = random.randint(0, max_entries)

    details["title"] = strip_details["Name"]

    if param == 'Specific_date':
        details["img_url"] = fall_back_img

        if main_website == 'https://garfieldminusgarfield.net/':
            # Garfield minus Garfield
            date_formatted = comic_date.strftime("%Y/%m/%d")

            main_website += 'day/' + date_formatted
            details["url"] = main_website
            details["day"] = comic_date.strftime("%d")
            details["month"] = comic_date.strftime("%m")
            details["year"] = comic_date.strftime("%Y")
        else:
            # Webtoon
            details["url"] = main_website + f"&episode_no={comic_date}"
    else:
        feed = Parser(xml=get(rss_site).content, limit=comic_nb+1).parse().feed[comic_nb]
        # Get informations
        tz = ""
        weekday = ""
        if strip_details["Main_website"] == 'https://www.webtoons.com/en/':
            if feed.title != "":
                details["title"] = f"{feed.title}"
            weekday = "A"
            tz = "Z"
        else:
            weekday = "a"
            tz = "z"

        new_date = datetime.strptime(feed.publish_date, f"%{weekday}, %d %b %Y %H:%M:%S %{tz}")
        details["day"] = new_date.strftime("%d")
        details["month"] = new_date.strftime("%m")
        details["year"] = new_date.strftime("%Y")

        details["url"] = feed.link

        img_index = 0
        if strip_details["Main_website"] == 'https://www.webtoons.com/en/':
            details["sub_img_url"] = feed.description_images[img_index].source
            img_index += 1

        details["img_url"] = feed.description_images[img_index].source

    if details is not None:
        details["color"] = int(strip_details["Color"], 16)

    return details
