# Manages daily posting
import json
from discord.ext import tasks, commands
from Scripts import BDbot, Web_requests_manager
import datetime
import asyncio
import os

class dailyposter(commands.Cog): # Class responsible for posting daily comic strips
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def start_daily(self,ctx): # Starts the dailyposter loop
    if(ctx.message.author.id == int(os.getenv('BOT_OWNER_ID'))):
      await BDbot.BDBot.send_any(self, ctx, "Daily loop started! Daily comics are posted at 2:00 AM UTC each day.")

      minutes_till_end_hour = 60 - datetime.datetime.now().minute
      await asyncio.sleep(60*minutes_till_end_hour)
      
      hour_now = datetime.datetime.now().hour

      if(hour_now <= 2):
        hours_till_two_AM = 1 - hour_now
      else:
        hours_till_two_AM = (24-hour_now)+2

      await asyncio.sleep(3600*hours_till_two_AM)

      await dailyposter.post_daily.start(self)
    else:
      await BDbot.BDBot.send_any(self, ctx, "You cannot do that.")

  @commands.command()
  async def is_daily_running(self,ctx): # Checks the dailyposter loop
    if(ctx.message.author.id == int(os.getenv('BOT_OWNER_ID'))):
      if(dailyposter.post_daily.is_running()):
        await BDbot.BDBot.send_any(self, ctx, "The loop is running.")
      else:
        await BDbot.BDBot.send_any(self, ctx, "The loop is NOT running.")

    else:
      await BDbot.BDBot.send_any(self, ctx, "You cannot do that.")


  @tasks.loop(hours=24.0) # Daily loop
  async def post_daily(self):
    # Daily loop
    NB_OF_COMICS = 6
    comic_data = dailyposter.get_database_data()
    comic_list = [""]*NB_OF_COMICS

    # Construct the list of what comics need to be sent
    for guild in comic_data:
      i=0
      for char in comic_data[str(guild)]["ComData"]:
        if(char == "1"):
          comic_list[i] += str(comic_data[str(guild)]["channel_id"])+";"
        
        i+=1
      
    for i in range(len(comic_list)):
      if(comic_list[i] != ""):
        # Define the comic that need to be sent
        if(i==0):
          comic_name = 'Garfield'
          main_website = 'https://www.gocomics.com/'
        elif(i==1):
          comic_name = 'Garfield-Classics'
          main_website = 'https://www.gocomics.com/'
        elif(i==2):
          comic_name = 'CalvinandHobbes'
          main_website = 'https://www.gocomics.com/'
        elif(i==3):
          comic_name = 'XKCD'
          main_website = 'https://xkcd.com/'
        elif(i==4):
          comic_name = 'Peanuts'
          main_website = 'https://www.gocomics.com/'
        elif(i==5):
          comic_name = 'Peanuts-Begins'
          main_website = 'https://www.gocomics.com/'

        if(main_website == 'https://www.gocomics.com/'):
          # Specific manager for GoComics website
          comic_details = Web_requests_manager.GoComics_manager.Comic_info(self,comic_name, param="today")
        else: # Other websites
          comic_details = Web_requests_manager.Other_site_manager.Comic_info(self,comic_name, main_website, param="today")

        # Sends the comic
        for channel in comic_list[i].split(";"):
          if(channel != None and channel != ''):
            await BDbot.BDBot.send_comic_embed_channel_specific(self, comic_details, channel)
  
  def get_database_data():
    # Returns the ids and what need to be sent
    FILE_PATH = "./data/data.json"

    # Loads the prefixes file
    with open(FILE_PATH,'r') as f:
      data = json.load(f)

    return data

  def new_change(self, ctx, comic, param): # Make a change in the database
    if(comic == 'Garfield'):
        comic_number = 0
    if(comic == 'Garfield-Classics'):
      comic_number = 1
    elif(comic == "CalvinandHobbes"):
      comic_number = 2
    elif(comic == "XKCD"):
      comic_number = 3
    elif(comic == 'Peanuts'):
      comic_number = 4
    elif(comic == 'Peanuts-Begins'):
      comic_number = 5

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

    if(use == 'add' or use == 'remove'):
      guild_id = str(ctx.guild.id)
      channel_id = str(ctx.channel.id)
    else:
      guild_id = str(ctx.id)

    data = dailyposter.get_database_data()

    if(use == 'add'):
      d = {
        guild_id:{
          "server_id":  None,
          "channel_id": None,
          "ComData" : None
        }
      }
      
      if(guild_id in data): # If this server was already in the database, fill out information
        d[guild_id]["server_id"] = data[guild_id]["server_id"]
        d[guild_id]["channel_id"] = data[guild_id]["channel_id"]
        d[guild_id]["ComData"] = data[guild_id]["ComData"]

        # If there is already comic data stored
        comic_str = list(d[guild_id]["ComData"])

        comic_str[comics_number] = "1";

        d[guild_id]["ComData"] = "".join(comic_str)

      else:
        # Add a comic to the list of comics
        d[guild_id]["server_id"] = int(guild_id)

        d[guild_id]["channel_id"] = int(channel_id)

        # If there was no comic data stored for this guild
        comic_str = ""
      
        # Construct the string of data 
        for i in range(NB_OF_COMICS):
          if(i==comics_number):
            comic_str += "1"
          else:
            comic_str += "0"

        d[guild_id]["ComData"] = comic_str
      
      data.update(d)

    elif (use == "remove"): # Remove comic
      if(guild_id in data):
        comic_str = list(data[guild_id]["ComData"])
        if(comic_str[comics_number] != "0"):
          comic_str[comics_number] = "0"
          data[guild_id]["ComData"] = "".join(comic_str)
      
    elif(use == 'remove_guild'): #Remove a guild from the list
      if(guild_id in data):
        data.pop(guild_id)

    # Saves the file
    with open(FILE_PATH,'w') as f:
      json.dump(data, f, indent=4)

def setup(client): # Initialize the cog
  client.add_cog(dailyposter(client))