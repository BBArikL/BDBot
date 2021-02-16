import discord
from discord.ext import commands, tasks
from Scripts import Web_requests_manager

class BDBot(commands.Cog):
  # Class responsible for main functions of the bot
  
  def __init__(self, client):
    # Constructor of the cog
    # Initialize all the properties of the cog
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    # Change bot's activity
    await self.client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='*help'))

    # To be sure that the bot is ready
    print('Logged in as {0.user}'.format(self.client))

  @commands.command(aliases = ['Git','github','Github'])
  async def git(self, ctx): # Links back to the github page
    await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")

  @commands.command(aliases = ['inv'])
  async def invite(self,ctx): # Creates a Oauth2 link to share the bot
    inv = "https://discord.com/oauth2/authorize?client_id=807780409362481163&permissions=0&scope=bot" # Dynamic linking not working for the moment : discord.utils.oauth_url(self.client.id)
    await ctx.send(f'Share the bot! {inv}')

  #---- End of commands ----#  

  def create_Embed(comic_details=None):
    if(comic_details!=None):
      # Embeds the comic
      comic_name = comic_details["Name"]
      comic_title = comic_details["title"]
      day = comic_details["day"]
      month = comic_details["month"]
      year = comic_details["year"]
      url = comic_details["url"]

      embed=discord.Embed(title=f"{comic_title}", url = url)
      
      embed.add_field(name=comic_name, value=f"Date: {day}/{month}/{year}")

      if(comic_details["alt"]!=None): # If there is alt text (Text when you hover your mouse on the image)
        alt = comic_details["alt"]
        embed.add_field(name="Alt text",value=alt)

      embed.set_image(url=comic_details["img_url"])

      embed.set_footer(text="Check out the bot here! https://github.com/BBArikL/BDBot")
      return embed
    else:
      # Error message
      embed=discord.Embed(title = "Error", url = "https://github.com/BBArikL/BDBot")

      embed.set_field(name = "An error occured :sob: . Maybe you tried to access a comic that is inaccessible? Open an issue at https://github.com/BBArikL/BDBot to let us know what arrived.")

      embed.set_footer(text="Check out the bot here! https://github.com/BBArikL/BDBot")
      return embed
  
  async def send_comic_embed(self, ctx, comic_details):
    embed = BDBot.create_Embed(comic_details) # Creates the embed
    
    await ctx.send(embed=embed) # Send the comic

  async def send_any(self,ctx,text):
    # Send any text given. Mostly for debugging purposes
    await ctx.send(text)

  #---- End of BDBot ----#

class dailyposter(): # Class responsible for posting daily comic strips
  def __init__(self, ctx, comic_name, main_website):
    self.post_daily.start(ctx, comic_name, main_website)

  @tasks.loop(hours=24.0) # Daily loop
  async def post_daily(self, ctx, comic_name, main_website):
    # Loop that post daily a comic
    if(main_website == 'https://www.gocomics.com/'):
      comic_details = Web_requests_manager.GoComics_manager.Comic_info(self,comic_name)
    
    else:
      comic_details = None # Placeholder for OtherSitesManager when its working
        
    BDBot.send_comic_embed(ctx, comic_details) # Sends the embed with the comics details

def setup(client): # Initialize the cog
  client.add_cog(BDBot(client))