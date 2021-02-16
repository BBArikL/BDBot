from urllib.request import urlopen
from discord.ext import commands
from datetime import date, timedelta
from bs4 import BeautifulSoup

class GoComics_manager(commands.Cog):

  def __init__(self, client):
    pass

  def Comic_info(self,comic_Name=None,day=None,month=None,year=None):
    # Details of the comic
    details = {"url": "", "Name": comic_Name,"title": "","day": "", "month": "", "year":"", "img_url":"", "alt": None}
    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today date
        today = date.today()
        details["day"] = today.strftime("%d")
        details["month"] = today.strftime("%m")
        details["year"] = today.strftime("%Y")

        # Gets today url
        details["url"] = GoComics_manager.send_link(comic_Name, today)

        # Get the html of the comic site
        html = urlopen(details["url"]).read()
        
        details["title"] = GoComics_manager.extract_title(html) # Ectracts the title of the comic

        details["img_url"] = GoComics_manager.extract_img(html) # Finds the url of the image

        if (details["img_url"] == None): 
          # If the bot didnt find the url of the image, we will assume for now that replit is too in advance for the site and try to do the same thing but with the day before
          yesterday = today - timedelta(days = 1)

          details["day"] = yesterday.strftime("%d")
          details["month"] = yesterday.strftime("%m")
          details["year"] = yesterday.strftime("%Y")

          # Gets today's url
          details["url"] = GoComics_manager.send_link(comic_Name, today)
        
          # Get the html of the comic site
          html = urlopen(details["url"]).read()
        
          details["img_url"] = GoComics_manager.extract_img(html)

    else:
      details = None
    
    return details

  def send_link(comic_Name, day): # Returns the comic title
    date_formatted = day.strftime("%Y/%m/%d")
    URL = f'https://www.gocomics.com/{comic_Name.lower()}/{date_formatted}'
    return (URL)

  def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title_meta = soup.find('meta', attrs={'property': 'og:title', 'content': True})
    
    if(title_meta != None): # If it finds the meta properties of the image
      title = title_meta['content']
      return title
    
    else:
      return None

  def extract_img(html):
    # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
    # Extract the image source of the comic
    # Problem : Since the bot is hosted on replit, the site can be at a date where the comic is not accessible
    soup = BeautifulSoup(html, "html.parser")
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    
    if(url_meta != None): # If it finds the meta properties of the image
      url = url_meta['content']
      # Trick RES into displaying the imagine inline
      url += '.jpg'
      return url
    
    else:
      return None

    #--- End of GoComics_manager ---#


class Other_site_manager(commands.Cog):
  # For sites like XKCD, etc...
  def __init__(self, client):
    pass
  
  # TODO ALL OF THIS SITE MANAGER WITH XKCD AS A TEMPLATE
  def Comic_info(self,comic_Name,main_website,day=None,month=None,year=None):
    # Details of the comic
    details = {"url": "", "Name": comic_Name, "day": "", "month": "", "year":"", "img_url":"", "alt": ""}
    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today's url
        if(comic_Name == 'XKCD'):
          details["url"] = Other_site_manager.extract_url_xk(main_website)
        
        # Gets today date
        d = date.today()
        details["day"] = d.strftime("%d")
        details["month"] = d.strftime("%m")
        details["year"] = d.strftime("%Y")

        # Get the html of the comic site
        html = urlopen(details["url"]).read()
        
        if(comic_Name == 'XKCD'): # Extracts the title, the image, and the alt-text of the comic
          # TO OPTMISE
          details["title"] = Other_site_manager.extract_title_xk(html)
          details["img_url"] = Other_site_manager.extract_img_xk(html)
          details["alt"] = Other_site_manager.extract_alt_xk(html)

    else:
      details = None
    
    return details

  #---- START XKCD specific functions ----#
  def extract_url_xk(main_website):
    # Get the html of the comic site
    html = urlopen(main_website).read()
    soup = BeautifulSoup(html,"html.parser")
    
    url_meta = soup.find('meta', attrs={'property': 'og:url', 'content': True})
    url = url_meta['content']
    
    return url

  def extract_title_xk(html):
    # Get the html of the comic site
    soup = BeautifulSoup(html,"html.parser")
    
    title_meta = soup.find('meta', attrs={'property': 'og:title', 'content': True})
    title = title_meta['content']
    
    return title
  
  def extract_img_xk(html): # Extracts the image url
    soup = BeautifulSoup(html,"html5lib")
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    img_url = url_meta['content']
    return img_url

  def extract_alt_xk(html): # Extract the alt text. 
    # I am not sure how to dissect the 'comic' class to get the alt text for now
    """
    Here is an example of what it gives back if I only the comic :

    """ 
    soup = BeautifulSoup(html,"html.parser")
    alt_meta = soup.find(id="comic")
    alt = alt_meta.find("title")
    print(alt_meta)
    return alt

  #--- End of Other_site_manager ---#


def setup(client): # Initialize the cogs
  client.add_cog(GoComics_manager(client))
  client.add_cog(Other_site_manager(client))