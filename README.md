# BDBot

Discord bot that post bd strips. Simple as that!

## Comics in the plan to add:
- Garfield https://www.gocomics.com/garfield/
- Garfield classics? https://www.gocomics.com/garfield-classics
- Calvin and Hobbes https://www.gocomics.com/calvinandhobbes/
- XKCD https://xkcd.com/

## Related Github pages: 
CalvinBot : https://github.com/wdr1/CalvinBot

## What to learn from this project?
- More about discord bots.
- Automated / Scheduled tasks.
- RSS feeds.
- Looking for content in web pages.

## Current state of the project
-What changed?
  - Regrouped Comics command in one cog.
  - Divised the code into multiple methods.

-Functionalities
  - For GoComics comics, its easy to add more.
  - Command 'today' and 'daily' working even if 'daily' can only send one comic daily on one server for now.
  - Command 'today' and 'random' working for XKCD even if it just links back to the website for now.
  - '-help' : Help embed
  - '-git' command : Redirects to this github page
  - '-invite' command : Generate a link to invite the bot to your server ([or use this link](https://discord.com/api/oauth2/authorize?client_id=807780409362481163&permissions=0&scope=bot))
  - Tell me if I forgot some commands here!

-Bugs
 - Lots of them!
 - The search method to extract the image for Gocomics seems to be very inconsistent.

-TODO
  - Gocomics:
    - 'Random' and date specific comics.
  - XKCD / Other sites:
    - Do the specific date comic and core functionality of 'Other_sites_manager'.
    - Improve 'Daily' command.
 
-Anything else to know?
  - The error manager ('Errors.py') might be sometimes commented out because I want to see the errors directly in the terminal. Please tell me if I forget to remove those multi-line comments.
  - The bot is in developement and hosted on Replit primarly. Since this bot is not very stable, it isnt continually online. When the bot have all the necessary functions, it will be maintained more.
