from urllib.request import urlopen
from discord.ext import commands
from datetime import date
from bs4 import BeautifulSoup

class GoComics_manager(commands.Cog):

  def __init__(self, client):
    pass

  def Comic_info(self,comic_Name=None,day=None,month=None,year=None):
    # Details of the comic
    details = {"url": "", "Name": comic_Name, "day": "", "month": "", "year":"", "img_url":"", "alt": None}
    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today's url
        details["url"] = GoComics_manager.send_link_today(comic_Name)
        
        # Gets today date
        d = date.today()
        details["day"] = d.strftime("%d")
        details["month"] = d.strftime("%m")
        details["year"] = d.strftime("%Y")

        # Get the html of the comic site
        html = urlopen(details["url"]).read()
        
        details["img_url"] = GoComics_manager.extract_img(html)

    else:
      details = None
    
    return details

  def send_link_today(comic_Name): # Returns today's link
    d = date.today()
    date_formatted = d.strftime("%Y/%m/%d")
    URL = f'https://www.gocomics.com/{comic_Name.lower()}/{date_formatted}'
    return (URL)

  def extract_img(html):
    # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
    # Extract the image source of the comic
    soup = BeautifulSoup(html, "html.parser")
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    url = url_meta['content']
    # Trick RES into displaying the imagine inline
    url += '.jpg'
    return url

    #--- End of GoComics_manager ---#


class Other_site_manager(commands.Cog):
  # For sites like XKCD, etc...
  def __init__(self, client):
    pass
  
  # TODO ALL OF THIS SITE MANAGER WITH XKCD AS A TEMPLATE
  def Comic_info(self,comic_Name,main_website,day=None,month=None,year=None):
    # Details of the comic
    details = {"url": "", "Name": comic_Name, "day": "", "month": "", "year":"", "img_url":"", "alt": None}
    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today's url
        details["url"] = main_website
        
        # Gets today date
        d = date.today()
        details["day"] = d.strftime("%d")
        details["month"] = d.strftime("%m")
        details["year"] = d.strftime("%Y")

        # Get the html of the comic site
        html = urlopen(details["url"]).read()
        
        if(comic_Name == 'XKCD'):
          details["img_url"] = Other_site_manager.extract_img_xk(html)
          details["alt"] = Other_site_manager.extract_alt_xk(html)

    else:
      details = None
    
    return details

  #---- START XKCD specific functions ----#
  def extract_img_xk(html):
    pass # TODO extract the image

  def extract_alt_xk(html):
    pass # TODO extract the alt text

    #--- End of Other_site_manager ---#


def setup(client): # Initialize the cog
  client.add_cog(GoComics_manager(client))
  client.add_cog(Other_site_manager(client))