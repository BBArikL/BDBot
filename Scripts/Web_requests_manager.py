from urllib.request import urlopen
from discord.ext import commands
from datetime import date, timedelta
from bs4 import BeautifulSoup


class GoComicsManager(commands.Cog):

    def __init__(self, client):
        pass

    def Comic_info(self, comic_Name=None, param=None, comic_date=None):
        # Details of the comic
        details = {"url": None, "Name": comic_Name, "title": None, "day": None, "month": None, "year": None,
                   "img_url": None, "alt": None}

        if comic_Name is not None:
            i = 0

            if comic_date is None:
                # Gets today date
                comic_date = date.today()

            while details["img_url"] is None and i < 3:
                i += 1
                if (param != "random"):
                    details["day"] = comic_date.strftime("%d")
                    details["month"] = comic_date.strftime("%m")
                    details["year"] = comic_date.strftime("%Y")

                    # Gets today /  url
                    details["url"] = GoComicsManager.send_link(self, comic_Name, comic_date)

                else:
                    # Random comic
                    details["url"] = GoComicsManager.send_random_link(self, comic_Name)

                # Get the html of the comic site
                html = urlopen(details["url"]).read()

                details["title"] = GoComicsManager.extract_meta_content(self, html,
                                                                        'title')  # Ectracts the title of the comic

                details["img_url"] = GoComicsManager.extract_meta_content(self, html,
                                                                          'image')  # Finds the url of the image

                if details["img_url"] is None and param != "today":  # Go back one day
                    comic_date = comic_date - timedelta(days=1)

            if i == 3:  # S'il n'a rien trouvé
                details = None
        else:
            details = None

        return details

    def send_link(self, comic_Name, day):  # Returns the comic url
        date_formatted = day.strftime("%Y/%m/%d")
        URL = f'https://www.gocomics.com/{comic_Name.lower()}/{date_formatted}'
        return (URL)

    def send_random_link(self, comic_Name):  # Returns the random comic url
        URL = f'https://www.gocomics.com/random/{comic_Name.lower()}'
        return (URL)

    def extract_meta_content(self, html, content):
        # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
        # Extract the image source of the comic
        # Problem : Since the bot is hosted on replit, the site can be at a date where the comic is not accessible
        soup = BeautifulSoup(html, "html.parser")
        content_meta = soup.find('meta', attrs={'property': f'og:{content}', 'content': True})

        if content_meta is not None:  # If it finds the meta properties of the image
            content_value = content_meta['content']

            if content == 'image':
                # Trick RES into displaying the imagine inline
                content_value += '.jpg'

            return content_value

        else:
            return None

        # --- End of GoComicsManager ---#


class OtherSiteManager(commands.Cog):
    # For sites like XKCD, etc...
    def __init__(self, client):
        pass

    # TODO ALL OF THIS SITE MANAGER WITH XKCD AS A TEMPLATE
    def Comic_info(self, comic_Name, main_website, param=None):
        # Details of the comic
        details = {"url": None, "Name": comic_Name, "title": None, "day": None, "month": None, "year": None,
                   "img_url": None, "alt": None}
        if comic_Name is not None:
            # Doesnt work, deactivated Cyanide and happiness to come back later
            # if(comic_Name=='Cyanide and Happinness'):
            #  main_website = OtherSiteManager.extract_id_content(main_website='comic-social-link')

            if comic_Name == 'XKCD':
                if param == "random":
                    main_website = "https://c.xkcd.com/random/comic/"  # Link for random XKCD comic

            details["url"] = OtherSiteManager.extract_url(self, main_website)

            # Gets today date
            if param == "today":
                d = date.today()
                details["day"] = d.strftime("%d")
                details["month"] = d.strftime("%m")
                details["year"] = d.strftime("%Y")

            # Get the html of the comic site
            html = urlopen(details["url"]).read()

            if html is not None:
                details["title"] = OtherSiteManager.extract_meta_content(self, html, 'title')

                details["img_url"] = OtherSiteManager.extract_meta_content(self, html, 'image')

                # if(comic_Name == 'XKCD'): # Extracts the title, the image, and the alt-text of the comic
                # Doesnt work
                # details["alt"] = OtherSiteManager.extract_alt_xk(html)
            else:
                details = None
        else:
            details = None

        return details

    # ---- START of web scraping functions ----#
    def extract_url(self, main_website):
        # Get the html of the comic site
        html = urlopen(main_website).read()
        soup = BeautifulSoup(html, "html.parser")

        url_meta = soup.find('meta', attrs={'property': 'og:url', 'content': True})
        url = url_meta['content']

        return url

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

    def extract_alt_xk(self, html):  # Extract the alt text.
        # TODO
        # Get the html of the comic site
        soup = BeautifulSoup(html, "html5lib")
        # links = soup.find_all('div', {'class': 'img'})
        img = soup.find_all('img')
        print(img[2].find('img')['title'])
        """.find_all('title')"""
        return None

    def extract_id_content(self, main_website, id):
        # Returns the demanded id content (href of an id attribute)
        # TO OPTIMIZE (Doesnt work, the worst implementation of all)
        html = urlopen(main_website).read()
        soup = BeautifulSoup(html, "html5lib")

        # From : https://stackoverflow.com/questions/43814754/python-beautifulsoup-how-to-get-href-attribute-of-a-element
        id_content = []
        for a in soup.find_all('a', href=True):
            if a.text:
                id_content.append(a['href'])
        id_content = id_content[47]

        return main_website + id_content

    # --- End of OtherSiteManager ---#


def setup(client):  # Initialize the cogs
    client.add_cog(GoComicsManager(client))
    client.add_cog(OtherSiteManager(client))
