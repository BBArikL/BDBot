from urllib.request import urlopen
from discord.ext import commands
from datetime import date, timedelta
from bs4 import BeautifulSoup
from rss_parser import Parser
from requests import get
import json
import urllib
import random

class GoComicsManager(commands.Cog):
  
  def __init__(self, client):
    pass

  def Comic_info(self, comic_Name=None, param=None, comic_date=None):
    # Details of the comic
    details = {"url": None, "Name": comic_Name, "title": None, "day": None, "month": None, "year": None, "img_url": None, "alt": None, "transcript": None}
    
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

        details["title"] = GoComicsManager.extract_meta_content(self, html, 'title')  # Extracts the title of the comic

        details["img_url"] = GoComicsManager.extract_meta_content(self, html, 'image')  # Finds the url of the image

        if details["img_url"] is None:  # Go back one day
          comic_date = comic_date - timedelta(days=1)

        if i == 4 and details["img_url"] is None:  # If it hasn't found anything
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
  # For sites like XKCD, Cyanide and Happiness
  def __init__(self, client):
    pass

  def Comic_info(self, comic_Name, main_website, param=None):
    # Details of the comic
    details = {"url": None, "Name": comic_Name, "title": None, "day": None, "month": None, "year": None, "img_url": None, "alt": None, "transcript": None}
    
    if comic_Name is not None:
          
      if comic_Name == 'XKCD':
        if param == "random":
          main_website = "https://c.xkcd.com/random/comic/"  # Link for random XKCD comic
          html = urlopen(main_website).read()
          main_website = OtherSiteManager.extract_meta_content(self, html, 'url')

        main_website = main_website + "info.0.json"
        details["url"] = main_website
            
      elif comic_Name == 'Cyanide and Happiness':
        if param == 'random':
          main_website += 'random'
        elif param == 'today':
          main_website += 'latest'
              
        details["url"] = main_website

      else:
        html = urlopen(main_website).read()
        details["url"] = OtherSiteManager.extract_meta_content(self, html, 'url')

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

      if comic_Name != 'XKCD':
        if html is not None:
          details["url"] = OtherSiteManager.extract_meta_content(self, html, 'url')

          details["title"] = OtherSiteManager.extract_meta_content(self, html, 'title')

          details["img_url"] = OtherSiteManager.extract_meta_content(self, html, 'image')
        else:
          details = None
            
      else:
        # XKCD special extractor
        # We requested a json and not a html
        json_details = json.loads(html)

        details["title"] = json_details["title"]
        details["url"] = details["url"].replace("info.0.json", "")
        details["img_url"] = json_details["img"]
        details["alt"] = json_details["alt"]
        # Transcript is not really relevant since there is no transcripts now.... I'll leave it and if I want to add it, I will  
        # details["transcript"] = json_details["transcript"] 
        details["day"] = json_details["day"]
        details["month"] = json_details["month"]
        details["year"] = json_details["year"]

    else:
      details = None

    return details

  # ---- START of web scraping functions ----#
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

  # --- End of OtherSiteManager ---#
    
class RssSiteManager(commands.Cog):
  # For sites that needs to parsed via  their RSS feed
  def __init__(self, client):
    pass

  def Comic_info(self, comic_Name, main_website, param=None, comic_date=None):
    # Details of the comic
    details = {"url": None, "Name": comic_Name, "title": None, "day": None, "month": None, "year": None, "img_url": None, "alt": None, "transcript": None}

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
      
      if param == 'Specific_date':
        date_formatted = comic_date.strftime("%Y/%m/%d")

        main_website += 'day/'+ date_formatted

        details["title"] = comic_Name
        details["url"] = main_website
        details["img_url"] = 'https://64.media.tumblr.com/avatar_02c53466ae58_64.gif'
        details["day"] = comic_date.strftime("%d")
        details["month"] = comic_date.strftime("%m")
        details["year"] = comic_date.strftime("%Y")
      else:
      
        main_website = 'https://garfieldminusgarfield.net/rss'
        rss = Parser(xml=get(main_website).content, limit=None).parse()
    
        # Get informations
        details["title"] = comic_Name

        details["url"] = rss.feed[comic_nb].link

        details["img_url"] = rss.feed[comic_nb].description_images[0].source

    return details


def setup(client):  # Initialize the cogs
    client.add_cog(GoComicsManager(client))
    client.add_cog(OtherSiteManager(client))
    client.add_cog(RssSiteManager(client))
