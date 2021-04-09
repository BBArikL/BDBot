# BDBot

Discord bot that post bd strips. Simple as that!

## Comics:
### Added:
- Garfield https://www.gocomics.com/garfield/
- Calvin and Hobbes https://www.gocomics.com/calvinandhobbes/
- XKCD https://xkcd.com/
- Garfield classics https://www.gocomics.com/garfield-classics
- Peanuts https://www.gocomics.com/peanuts
- Peanuts Begins https://www.gocomics.com/peanuts-begins
- Cyanide and Happines https://explosm.net/ (Need rework)
### To Add:
- Poorly drawn lines https://poorlydrawnlines.com/
- Safely endangered https://www.webtoons.com/en/comedy/safely-endangered/list?title_no=352
- Carl https://www.webtoons.com/en/slice-of-life/carl/list?title_no=1216
- BlueChair https://www.webtoons.com/en/slice-of-life/bluechair/list?title_no=199
- Live with yourself https://www.webtoons.com/en/comedy/live-with-yourself/list?title_no=919
- Adventures of god https://www.webtoons.com/en/comedy/adventures-of-god/list?title_no=853&page=1
- War and peas https://warandpeas.com/

## Related Github pages: 
CalvinBot : https://github.com/wdr1/CalvinBot

## What to learn from this project?
- More about discord bots.
- Automated / Scheduled tasks.
- Looking for content in web pages.

## Current state of the project
- Functionalities
  - For GoComics comics, its easy to add more.
  - Command 'today' and 'random' working. (Deactivated 'daily' until ready)
  - Command 'today' and 'random' working for XKCD.
  - 'bd!help' : Help embed
  - 'bd!git' command : Redirects to this github page
  - 'bd!invite' command : Generate a link to invite the bot to your server ([or use this link](https://discord.com/api/oauth2/authorize?client_id=807780409362481163&permissions=0&scope=bot))
  - Tell me if I forgot some commands here!

- Bugs
  - The search method to extract the image for Gocomics seems to be very inconsistent. EDIT: Should be fixed (theoratically). My guess is that since the bot is hosted on Replit, the server where the bot is hosted is in advance compared to the GoComics site. The fix used is not the best approach, I must admit, but it should work.

- TODO
  - Gocomics:
    - Date specific comic
  - XKCD / Other sites:
    - Show the alt-text
    - Do the specific date / number comic command.
    - Go back and see the extract_id_content() method in Web_requests_manager to fix the poor implementation of the link (For Cyanide and Happines). EDIT: Deactivated until its ready.
  - Other:
    - 'Daily' command
    - Optimize Web_requests_manager
 
- Anything else to know?
  - The error manager ('Errors.py') might be sometimes commented out because I want to see the errors directly in the terminal. Please tell me if I forget to remove those multi-line comments.
  - You want to do a pull request to add your favourite comic? 
    - Preferably, Gocomics comics are the easiest to implement, so try to stick with that if your comic is hosted there (Literally copy-paste the 'garf' command, change the name of the command and change the comic_name to what it is in the GoComics url, example : https://www.gocomics.com/garfield/ --> comic_name = 'Garfield').
    - If the comic is NOT hosted on GoComics, please open an issue on the git page (https://github.com/BBArikL/BDBot). 
    - Any pull requests that wasnt approved from another site will be automatically rejected and you will be asked to follow the procedure cited.
  - The bot is in developement and hosted on Replit.
