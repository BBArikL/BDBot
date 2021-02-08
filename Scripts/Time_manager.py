from discord.ext import commands
from datetime import date

class Time_manager(commands.Cog):

  def __init__(self, client):
    pass

  def send_link_today(self, comic_Name):
    d = date.today()
    date_formatted = d.strftime("%Y/%m/%d")
    URL = f'https://www.gocomics.com/{comic_Name.lower()}/{date_formatted}'
    return (f'{comic_Name} today! {URL}')

def setup(client): # Initialize the cog
  client.add_cog(Time_manager(client))