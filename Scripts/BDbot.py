import discord
from discord.ext import commands
from Scripts import DailyPoster
import os
import topgg


class BDBot(commands.Cog):
    # Class responsible for main functions of the bot

    def __init__(self, client):
        # Constructor of the cog
        # Initialize all the properties of the cog
        self.client = client
        dbl_token = str(os.getenv('TOP_GG_TOKEN'))  # top.gg token
        self.dblpy = topgg.DBLClient(client, dbl_token)

    @commands.Cog.listener()
    async def on_ready(self):
        # Change bot's activity
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='bd!help'))

        print("Logged in as {0.user}".format(self.client))
        channel_id = int(os.getenv('PRIVATE_CHANNEL_SUPPORT_ID'))

        channel = self.client.get_channel(channel_id)

        await channel.send(
            "Bot restarted. I will now try to restart the loop.")  # Sends this message whenever restarting the bot

        await DailyPoster.DailyPoster.wait_for_daily(self)  # Wait for daily poster

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        DailyPoster.DailyPoster.remove_guild(self, guild)
        print(f"Bot got removed from {guild}")

    @commands.command(aliases=['Git', 'github', 'Github'])
    async def git(self, ctx):  # Links back to the github page
        await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/BDBot")

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):  # Creates a Oauth2 link to share the bot
        inv = discord.utils.oauth_url(os.getenv('CLIENT_ID'))
        await ctx.send(f'Share the bot! {inv}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)  # Only mods can delete the server from the database
    async def remove_all(self, ctx):  # Remove the guild from the database
        DailyPoster.DailyPoster.remove_guild(self, ctx.guild)
        await ctx.send("All daily commands removed successfully!")

    @commands.command()
    async def vote(self, ctx):  # Links back to the github page
        await ctx.send("Vote for the bot here: https://top.gg/bot/807780409362481163")

    @commands.command()
    async def nb_guild(self, ctx):  # Gets the number of guilds that the bot is in (for analytics)
        if ctx.message.author.id == int(os.getenv('BOT_OWNER_ID')):
            await ctx.send(f"The bot is in {len(self.client.guilds)} guilds. Trying to update status on Top.gg.....")
            """This function runs every 30 minutes to automatically update your server count."""
            try:
                await self.dblpy.post_guild_count()
                await ctx.send(f'Posted server count ({self.dblpy.guild_count})')
            except Exception as e:
                await ctx.send('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    # @bot.check
    # async def globally_block_dms(ctx):
    # return ctx.guild is not None

    # ---- End of commands ----#

    def create_embed(self, comic_details=None):
        if comic_details is not None:
            # Embeds the comic
            comic_name = comic_details["Name"]
            comic_title = comic_details["title"]
            day = comic_details["day"]
            month = comic_details["month"]
            year = comic_details["year"]
            url = comic_details["url"]

            embed = discord.Embed(title=f"{comic_title}", url=url)

            if day is not None:
                embed.add_field(name=comic_name, value=f"Date: {day}/{month}/{year}")

            if comic_details["alt"] is not None:
                # If there is alt text (Text when you hover your mouse on the image)
                alt = comic_details["alt"]
                embed.add_field(name="Alt text", value=alt)

            embed.set_image(url=comic_details["img_url"])

            embed.set_footer(text="Check out the bot here! https://github.com/BBArikL/BDBot")
            return embed

        else:
            # Error message
            embed = discord.Embed(title="No comic found!")

            embed.add_field(name="We could not find a comic at this date :thinking:....", value="Try another date!")

            embed.set_footer(text="Check out the bot here! https://github.com/BBArikL/BDBot")
            return embed

    async def send_comic_embed(self, ctx, comic_details):
        embed = BDBot.create_embed(self, comic_details)  # Creates the embed

        await ctx.send(embed=embed)  # Send the comic

    # Send a comic embed to a specific channel
    async def send_comic_embed_channel_specific(self, embed, channel_id):
        channel = self.client.get_channel(int(channel_id))

        await channel.send(embed=embed)

    async def send_any(self, ctx, text):
        # Send any text given. Mostly for debugging purposes
        await ctx.send(text)

    # ---- End of BDBot ----#


def setup(client):  # Initialize the cog
    client.add_cog(BDBot(client))
