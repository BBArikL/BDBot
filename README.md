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
- Dilbert https://dilbert.com/
- Dilbert classics https://www.gocomics.com/dilbert-classics
- Cyanide and Happines https://explosm.net/
- Frazz https://www.gocomics.com/frazz
- Garfield minus Garfield https://garfieldminusgarfield.net/
- Jon
- Frank and Ernest https://www.gocomics.com/frank-and-ernest
- Broom Hilda https://www.gocomics.com/broomhilda
- Inspector Dangers Crime Quiz https://www.gocomics.com/inspector-dangers-crime-quiz
- Cheer up emo kid https://www.gocomics.com/cheer-up-emo-kid
- Catana Comics https://www.gocomics.com/
- Brevity https://www.gocomics.com/brevity
- Cats cafe https://www.gocomics.com/cats-cafe
- Popeyes https://comicskingdom.com/popeye
- Artic Circle https://comicskingdom.com/arctic-circle
- Lockhorns https://comicskingdom.com/lockhorns
- Marvin https://comicskingdom.com/marvin
- Zits https://comicskingdom.com/zits
- Hi and Lois https://comicskingdom.com/hi-and-lois
- Safely endangered https://www.webtoons.com/en/comedy/safely-endangered/list?title_no=352
- Carl https://www.webtoons.com/en/slice-of-life/carl/list?title_no=1216
- BlueChair https://www.webtoons.com/en/slice-of-life/bluechair/list?title_no=199
- Live with yourself https://www.webtoons.com/en/comedy/live-with-yourself/list?title_no=919
- Adventures of god https://www.webtoons.com/en/comedy/adventures-of-god/list?title_no=853
- System32Comics https://www.webtoons.com/en/challenge/system32comics/list?title_no=235074
- The Gamer https://www.webtoons.com/en/action/the-gamer/list?title_no=88
### To Add:
- Poorly drawn lines https://poorlydrawnlines.com/
- War and peas https://warandpeas.com/

## Related Github pages: 
CalvinBot : https://github.com/wdr1/CalvinBot

## What to learn from this project?
- More about discord bots.
- Automated / Scheduled tasks.
- Looking for content in web pages.
- Parsing Date.
- Database support.
- Github version handling.

## Current state of the project
- Functionalities
  - 'bd!<comic_name>' Information embed on the requested comic.
  - 'bd!help' : Help embed
  - 'bd!git' command : Redirects to this github page
  - 'bd!invite' command : Generate a link to invite the bot to your server ([or use this link](https://discord.com/api/oauth2/authorize?client_id=807780409362481163&permissions=0&scope=bot))
  - Daily Command: use 'bd!<name_of_comic> add/remove' to add or remove a comic from the daily list for the server.
  - Use 'bd!remove_all' to remove all comics from the daily list for the server.
  - Use 'bd!remove_channel' to remove all comics in the channel.
  - Tell me if I forgot some commands here!

- Bugs
  - Replit might not save correctly the requests and daily comics. This will be resolved during the next update.
  - None for the moment. Open a issue if you find any! :)

- TODO
  - Sites to add support:
    - See section TO ADD
  - Other:
    - Optimize Web_requests_manager
 
- Anything else to know?
  - Why can't I go farther than 7 comics on Comics Kingdom? Comics Kingdom use a special premium subscription plan to view all comics. There is no known way to get around it and getting the subscription and after distributing the comic for free could cause some undesirable consequences in the future.
  - Why is there only 2 images for Webtoons? Webtoons only gives out two images link to the comic in their rss feed. Finding each image link is way more complicated than this and is not in place now.
  - The error manager ('Errors.py') might be sometimes commented out because I want to see the errors directly in the terminal. Please tell me if I forget to remove those multi-line comments.
  - You want to do a pull request to add your favourite comic? 
    - Preferably, Gocomics and Comics Kingdom comics are the easiest to implement, so try to stick with that if your comic is hosted there. 
      - Steps:
        1. Add a new value in misc/comics_details.json that specifies each value for the comic. (See [this README](misc/ADD_COMIC.md)).
        2. Add a command in Scripts/Comics.py under the latest comic with aliases that are the same that were added to the json file and change the value of 'comic_name' to the name of the comic added.
        3. That's it!
  - If the comic is NOT hosted on GoComics/Comics Kingdom, please open an issue on the git page (https://github.com/BBArikL/BDBot). 
  - Any pull requests that was not approved from another site will be automatically rejected and you will be asked to follow the procedure cited.
  - 'Beta' and 'main'?
    - The main branch is the current bot that is running on Discord.
    - Beta branch is for all experiments and additions waiting for approval to add to the current bot. This runs on a (for now) private bot upon completion of current goals.
    - More about branches: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-branches
  - Core features of the bot are done, and it is hosted on Replit.
  - The bot is on UTC time. The daily comic post happen at 6:00 AM UTC daily.
