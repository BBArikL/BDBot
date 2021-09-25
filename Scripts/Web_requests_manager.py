from urllib.request import urlopen
from discord.ext import commands
from datetime import date, timedelta
from bs4 import BeautifulSoup
from rss_parser import Parser
from requests import get
import json
import urllib
import random


class ComicsRequestsManager(commands.Cog):
    ORIGINAL_DETAILS = {"url": None, "Name": None, "title": None, "day": None, "month": None, "year": None,
                        "img_url": None, "alt": None, "color":None}

    def __init__(self, client):
        pass

    def Comic_info_date(self, stripDetails, param=None, comic_date=None):
        # Details of the comic
        MAX_TRIES = 30
        details = ComicsRequestsManager.ORIGINAL_DETAILS.copy()

        details["Name"] = stripDetails["Name"]

        if stripDetails is not None:
            i = 0

            if comic_date is None:
                # Gets today date
                comic_date = date.today()

            while  i < MAX_TRIES and details["img_url"] is None:
                i += 1
                if param != "random":
                    details["day"] = comic_date.strftime("%d")
                    details["month"] = comic_date.strftime("%m")
                    details["year"] = comic_date.strftime("%Y")

                    # Gets today /  url
                    details["url"] = ComicsRequestsManager.get_link(self, stripDetails, comic_date)

                else:
                    # Random comic
                    details["url"] = ComicsRequestsManager.get_random_link(self, stripDetails)

                # Get the html of the comic site
                try:
                    html = urlopen(details["url"]).read()
                except urllib.error.HTTPError:
                    html = None

                details["title"] = ComicsRequestsManager.extract_meta_content(self, html,
                                                                              'title')  # Extracts the title of the comic

                details["img_url"] = ComicsRequestsManager.extract_meta_content(self, html,
                                                                                'image')  # Finds the url of the image

                if details["img_url"] is None:  # Go back one day
                    comic_date = comic_date - timedelta(days=1)

                if i >= MAX_TRIES and details["img_url"] is None:  # If it hasn't found anything
                    details = None

            if details is not None:
                details["color"] = int(stripDetails["Color"], 16)
        else:
            details = None

        return details

    def get_link(self, stripDetails, day):  # Returns the comic url
        date_formatted = day.strftime("%Y/%m/%d")
        URL = f'{stripDetails["Main_website"]}{stripDetails["Web_name"]}/{date_formatted}'
        return URL

    def get_random_link(self, stripDetails):  # Returns the random comic url
        URL = f'{stripDetails["Main_website"]}random/{stripDetails["Web_name"]}'
        return URL

    def extract_meta_content(self, html, content):
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

    # For sites like XKCD, Cyanide and Happiness
    def Comic_info_number(self, stripDetails, param=None):
        # Details of the comic
        details = ComicsRequestsManager.ORIGINAL_DETAILS.copy()

        details["Name"] = stripDetails["Name"]

        if stripDetails["Name"] is not None:
            main_website = stripDetails["Main_website"]

            if stripDetails["Name"] == 'xkcd':
                if param == "random":
                    main_website = "https://c.xkcd.com/random/comic/"  # Link for random XKCD comic
                    html = urlopen(main_website).read()
                    main_website = ComicsRequestsManager.extract_meta_content(self, html, 'url')

                main_website = main_website + "info.0.json"
                details["url"] = main_website

            elif stripDetails["Name"] == 'Cyanide and Happiness':
                if param == 'random':
                    main_website += 'random'
                elif param == 'today':
                    main_website += 'latest'

                details["url"] = main_website

            else:
                html = urlopen(main_website).read()
                details["url"] = ComicsRequestsManager.extract_meta_content(self, html, 'url')

            # Gets today date
            if param == "today":
                d = date.today()
                details["day"] = d.strftime("%d")
                details["month"] = d.strftime("%m")
                details["year"] = d.strftime("%Y")

            # Get the html of the comic site
            try:
                html = urlopen(details["url"]).read()
            except urllib.error.HTTPError:
                html = None

            if stripDetails["Name"] != 'xkcd':
                if html is not None:
                    details["url"] = ComicsRequestsManager.extract_meta_content(self, html, 'url')

                    details["title"] = ComicsRequestsManager.extract_meta_content(self, html, 'title')

                    details["img_url"] = ComicsRequestsManager.extract_meta_content(self, html, 'image')
                else:
                    details = None

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
                    details = None
            if details is not None:
                details["color"] = int(stripDetails["Color"], 16)
        else:
            details = None

        return details

    # --- End of OtherSiteManager ---#

    # For rss comics
    def Comic_info_rss(self, stripDetails, param=None, comic_date=None):
        # Details of the comic
        details = ComicsRequestsManager.ORIGINAL_DETAILS.copy()

        details["Name"] = stripDetails["Name"]
        main_website = stripDetails["Main_website"]

        # Gets today date
        if param == "today":
            d = date.today()
            details["day"] = d.strftime("%d")
            details["month"] = d.strftime("%m")
            details["year"] = d.strftime("%Y")

        # Get the RSS of the comic site
        if main_website == 'https://garfieldminusgarfield.net/':
            if param == 'random':
                # Random comic in the rss feed (Go as far as July 11 2018)
                comic_nb = random.randint(0, 19)
            elif param == 'today':
                # First comic in the rss feed
                comic_nb = 0

            details["title"] = stripDetails["Name"]

            if param == 'Specific_date':
                date_formatted = comic_date.strftime("%Y/%m/%d")

                main_website += 'day/' + date_formatted

                details["url"] = main_website
                details["img_url"] = 'https://64.media.tumblr.com/avatar_02c53466ae58_64.gif'
                details["day"] = comic_date.strftime("%d")
                details["month"] = comic_date.strftime("%m")
                details["year"] = comic_date.strftime("%Y")
            else:

                main_website = 'https://garfieldminusgarfield.net/rss'
                rss = Parser(xml=get(main_website).content, limit=None).parse()

                # Get informations
                details["url"] = rss.feed[comic_nb].link

                details["img_url"] = rss.feed[comic_nb].description_images[0].source

            if details is not None:
                details["color"] = int(stripDetails["Color"], 16)
        else:
            details = None

        return details


def setup(client):  # Initialize the cogs
    client.add_cog(ComicsRequestsManager(client))
