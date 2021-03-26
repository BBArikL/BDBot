# Manages daily posting
import json
from discord.ext import tasks


class dailyposter(): # Class responsible for posting daily comic strips
  def __init__(self, ctx, comic_name, main_website):
    self.post_daily.start()

  @tasks.loop(hours=24.0) # Daily loop
  async def post_daily(self, ctx, comic_name, main_website):
    # TODO
    dailyposter.getComicsData()
    
     # Sends the embed with the comics details
  
  def getData():
    pass

  def remove(ctx): # Removes a guild from the database
    dailyposter.save(str(ctx.guild.id), 'remove_guild')

  def add(ctx, comic_number): # Add a 
    
    if(not dailyposter.verifyDuplicateChannel(ctx.guild.id, ctx.channel.id)):
      dailyposter.save(ctx.guild.id, 'add', ctx.channel.id, comic_number)

  def save(guild_id, use, channel_id=None, comics_number=None):
    # Saves the new informations in the database
    # Adds or delete the guild_id, the channel id and the comic_strip data
    FILE_PATH = "./data/data.json"
    NB_OF_COMICS = 6

    # Loads the prefixes file
    with open(FILE_PATH,'r') as f:
      data = json.load(f)

    if(use == 'add'):
      # Add a comic to the list of comics
      data[guild_id] = guild_id
      data[guild_id]["channel_id"] = channel_id

      if(data[guild_id]["ComData"] != None):
        comic_str = data[guild_id]["ComData"]
      else:
        comic_str = ""
      
      # Construct the string of data 
      for i in range (1, NB_OF_COMICS):
        if(i==comics_number):
          comic_str += "1"
        else:
          comic_str += "0"

      data[guild_id]["ComData"] = comic_str

    elif (use == "remove"):
      # TODO
      pass

    elif(use == 'remove_guild'):
      data.pop(guild_id)

    # Saves the file
    with open(FILE_PATH,'w') as f:
      json.dump(data, f, indent=4)

  def verifyDuplicateChannel(guild, channel):
    # Verifies if the channel is not the same as the one stored in the datatbase
    # If its not the same, returns true
    # If its the same, returns false
    # TODO
    isAduplicate = False

    return isAduplicate

def setup(client): # Initialize the cog
  client.add_cog(dailyposter(client))