from urllib.request import urlopen
from discord.ext import commands
from datetime import date, timedelta
from bs4 import BeautifulSoup

class GoComics_manager(commands.Cog):

  def __init__(self, client):
    pass

  def Comic_info(self,comic_Name=None,day=None,month=None,year=None):
    # Details of the comic
    details = {"url": None, "Name": comic_Name,"title": None,"day": None, "month": None, "year": None, "img_url": None, "alt": None}
    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today date
        today = date.today()
        while(details["img_url"] == None):
          details["day"] = today.strftime("%d")
          details["month"] = today.strftime("%m")
          details["year"] = today.strftime("%Y")

          # Gets today url
          details["url"] = GoComics_manager.send_link(comic_Name, today)

          # Get the html of the comic site
          html = urlopen(details["url"]).read()
        
          details["title"] = GoComics_manager.extract_meta_content(html, 'title') # Ectracts the title of the comic

          details["img_url"] = GoComics_manager.extract_meta_content(html, 'image') # Finds the url of the image

          if (details["img_url"] == None): 
            today = today - timedelta(days = 1)
    else:
      details = None
    
    return details

  def send_link(comic_Name, day): # Returns the comic title
    date_formatted = day.strftime("%Y/%m/%d")
    URL = f'https://www.gocomics.com/{comic_Name.lower()}/{date_formatted}'
    return (URL)

  def extract_meta_content(html,content):
    # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
    # Extract the image source of the comic
    # Problem : Since the bot is hosted on replit, the site can be at a date where the comic is not accessible
    soup = BeautifulSoup(html, "html.parser")
    content_meta = soup.find('meta', attrs={'property': f'og:{content}', 'content': True})
    
    if(content_meta != None): # If it finds the meta properties of the image
      content_value = content_meta['content']

      if(content == 'image'):
        # Trick RES into displaying the imagine inline
        content_value += '.jpg'

      return content_value
    
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
    details = {"url": None, "Name": comic_Name,"title": None,"day": None, "month": None, "year": None, "img_url": None, "alt": None}    
    if(comic_Name!=None):
      if(day==None and month==None and year==None):
        # Gets today's url

        if(comic_Name=='Cyanide and Happinness'):
          main_website = Other_site_manager.extract_id_content(main_website, 'comic-social-link')

        details["url"] = Other_site_manager.extract_url(main_website)
        
        # Gets today date
        d = date.today()
        details["day"] = d.strftime("%d")
        details["month"] = d.strftime("%m")
        details["year"] = d.strftime("%Y")

        # Get the html of the comic site
        html = urlopen(details["url"]).read()
        
        details["title"] = Other_site_manager.extract_meta_content(html, 'title')
        
        details["img_url"] = Other_site_manager.extract_meta_content(html, 'image')
        
        #if(comic_Name == 'XKCD'): # Extracts the title, the image, and the alt-text of the comic
          # Doesnt work  
          #details["alt"] = Other_site_manager.extract_alt_xk(html)
    else:
      details = None
    
    return details

  #---- START of web scraping functions ----#
  def extract_url(main_website):
    # Get the html of the comic site
    html = urlopen(main_website).read()
    soup = BeautifulSoup(html,"html.parser")
    
    url_meta = soup.find('meta', attrs={'property': 'og:url', 'content': True})
    url = url_meta['content']
    
    return url

  def extract_meta_content(html,content):
    # Copied from CalvinBot : https://github.com/wdr1/CalvinBot/blob/master/CalvinBot.py
    # Extract the image source of the comic
    # Problem : Since the bot is hosted on replit, the site can be at a date where the comic is not accessible
    soup = BeautifulSoup(html, "html.parser")
    content_meta = soup.find('meta', attrs={'property': f'og:{content}', 'content': True})
    
    if(content_meta != None): # If it finds the meta properties of the image
      content_value = content_meta['content']

      return content_value
    
    else:
      return None

  def extract_alt_xk(html): # Extract the alt text. 
    # TODO
    # Get the html of the comic site
    soup = BeautifulSoup(html,"html5lib")
    #links = soup.find_all('div', {'class': 'img'})
    img = soup.find_all('img')
    print(img[2].find('img')['title']) 
    """.find_all('title')"""
    return None

  def extract_id_content(main_website, id):
    # Returns the demanded id content (href of an id attribute)
    # TO OPTIMIZE (It works but it is the worst implementation of all)
    html = urlopen(main_website).read()
    soup = BeautifulSoup(html, "html5lib")

    # From : https://stackoverflow.com/questions/43814754/python-beautifulsoup-how-to-get-href-attribute-of-a-element
    id_content = []
    for a in soup.find_all('a', href=True): 
      if a.text: 
        id_content.append(a['href'])
    id_content = id_content[47]

    return main_website + id_content

  #--- End of Other_site_manager ---#


def setup(client): # Initialize the cogs
  client.add_cog(GoComics_manager(client))
  client.add_cog(Other_site_manager(client))