# Manages daily posting
import json
from discord.ext import tasks, commands
from Scripts import BDbot, Web_requests_manager

class dailyposter(commands.Cog): # Class responsible for posting daily comic strips
  def __init__(self, client):
    self.client = client

  async def start_poster(self):
    await dailyposter.post_daily.start(dailyposter) # Starts the dailyposter  

  @tasks.loop(seconds=10) # Daily loop
  async def post_daily(self):
    # Daily loop
    comic_list = []
    comic_data = dailyposter.getComicsData()

    # Construct the list of what comics need to be sent
    for guild_id in comic_data:
      for i in range(len(guild_id["ComData"])):
        if(guild_id["ComData"][i] == "1"):
          comic_list[i] += guild_id["channel_id"]+";"
      
    for i in range(len(comic_list)):
      if(comic_list[i] != None):
        # Define the comic that need to be sent
        if(i==1):
          comic_name = 'Garfield'
          main_website = 'https://www.gocomics.com/'
        elif(i==2):
          comic_name = 'Garfield-Classics'
          main_website = 'https://www.gocomics.com/'
        elif(i==3):
          comic_name = 'CalvinandHobbes'
          main_website = 'https://www.gocomics.com/'
        elif(i==4):
          comic_name = 'XKCD'
          main_website = 'https://xkcd.com/'
        elif(i==5):
          comic_name = 'Peanuts'
          main_website = 'https://www.gocomics.com/'
        elif(i==6):
          comic_name = 'Peanuts-Begins'
          main_website = 'https://www.gocomics.com/'

        if(main_website == 'https://www.gocomics.com/'):
           # Specific manager for GoComics website
          comic_details = Web_requests_manager.GoComics_manager.Comic_info(self,comic_name, param="today")
    
        else: # Other websites
          comic_details = Web_requests_manager.Other_site_manager.Comic_info(self,comic_name, main_website, param="today")

        # Sends the comic
        for channel in comic_list[i].split(";"):
          await BDbot.BDBot.send_comic_embed_channel_specific(self, comic_details, int(channel))
  
  def getComicsData():
    # Returns the ids and what need to be sent
    FILE_PATH = "./data/data.json"

    # Loads the prefixes file
    with open(FILE_PATH,'r') as f:
      data = json.load(f)

    return data

  def new_change(self, ctx, comic, param):
    if(comic == 'Garfield'):
        comic_number = 1
    if(comic == 'Garfield-Classics'):
      comic_number = 2
    elif(comic == "CalvinandHobbes"):
      comic_number = 3
    elif(comic == "XKCD"):
      comic_number = 4
    elif(comic == 'Peanuts'):
      comic_number = 5
    elif(comic == 'Peanuts-Begins'):
      comic_number = 6

    if(param=="add"):
      dailyposter.add(self, ctx, comic_number)
    if(param=="remove"):
      dailyposter.remove(self,ctx,comic_number)
      
  def add(self, ctx, comic_number): # Add a Comic to the comic list
    dailyposter.save(self, ctx, 'add', comics_number=comic_number)

  def remove(self, ctx, comic_number): # Remove a Comic to comic list
    dailyposter.save(self, ctx, 'remove', comics_number=comic_number)

  def remove_guild(self,ctx): # Removes a guild from the database
    dailyposter.save(self, ctx, 'remove_guild')

  def updateDatabase(self,ctx):
    pass # TODO to add/remove one 0 to each "ComData" when changing the comic list

  def save(self, ctx, use, comics_number=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    # Doesnt work, to construct the list THEN save it
    FILE_PATH = "./data/data.json"
    NB_OF_COMICS = 6
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id

    # Loads the prefixes file
    with open(FILE_PATH,'r') as f:
      data = json.load(f)

    if(use == 'add'):
      d = {
        "server_id":  None,
        "channel_id": None,
        "ComData" : None
      }
      
      if(str(guild_id) in data): # If this server was already in the database, fill out information
        d["server_id"] = data[guild_id]["server_id"]
        d["channel_id"] = data[guild_id]["channel_id"]
        d["ComData"] = data[guild_id]["ComData"]

        # If there is already comic data stored
        comic_str = d["ComData"]

        comic_str[comics_number] = "1";

        d["ComData"] = comic_str

      else:
        # Add a comic to the list of comics
        d["server_id"] = str(guild_id)

        d["channel_id"] = str(channel_id)

        # If there was no comic data stored for this guild
        comic_str = ""
      
        # Construct the string of data 
        for i in range (1, NB_OF_COMICS):
          if(i==comics_number):
            comic_str += "1"
          else:
            comic_str += "0"
      
        data[guild_id]["ComData"] = comic_str
      
      data.update(d)

      # await BDbot.BDBot.send_any(self, ctx, f"Daily comic added successfully in channel {d["channel_id"]} !")

    elif (use == "remove"):
      if(str(guild_id) in data):

        if(data[guild_id]["ComData"][comics_number] != "0"):
          data[guild_id]["ComData"][comics_number] = "0"

          # await BDbot.BDBot.send_any(self, ctx, "Comic removed successfully!")
        else:
          # await BDbot.BDBot.send_any(self, ctx, "This comic is already not in the daily list!")
          pass
      else:
        # await BDbot.BDBot.send_any(self, ctx, "This server is not set up to receive daily comics!")
        pass
      data.update(d)
      
    elif(use == 'remove_guild'): #Remove a guild from the list
      if(data[guild_id] != None):
        data.pop(guild_id)
      else:
        # await BDbot.BDBot.send_any(self, ctx,"This server does not appear to be in the database yet!")
        pass

    # Saves the file
    with open(FILE_PATH,'w') as f:
      json.dump(data, f, indent=4)

def setup(client): # Initialize the cog
  client.add_cog(dailyposter(client))