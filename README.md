# BDBot

Discord bot that post bd strips. Simple as that!

<img src="https://img.shields.io/github/languages/top/BBArikL/BDBot" alt="Github top language"/>
<img src="https://img.shields.io/discord/982838016945033247" alt="Discord server">
<img src="https://img.shields.io/github/languages/code-size/BBArikL/BDBot" alt="Github code size">
<img src="https://img.shields.io/github/issues/BBArikL/BDBot" alt="Issues in repo BDBot">
<img src="https://img.shields.io/github/issues-pr/BBArikL/BDBot" alt="Pull request in repo BDBot">
<img src="https://img.shields.io/github/license/BBArikL/BDBot" alt="License of BDBot">
<img src="https://img.shields.io/github/last-commit/BBArikL/BDBot" alt="Last commit indicator">

## Comics:
### Added:
- Garfield https://www.gocomics.com/garfield/
- Calvin and Hobbes https://www.gocomics.com/calvinandhobbes/
- XKCD https://xkcd.com/
- Garfield's classics https://www.gocomics.com/garfield-classics
- Peanuts https://www.gocomics.com/peanuts
- Peanuts Begins https://www.gocomics.com/peanuts-begins
- Cyanide and Happiness https://explosm.net/
- Frazz https://www.gocomics.com/frazz
- Garfield minus Garfield https://garfieldminusgarfield.net/
- Frank and Ernest https://www.gocomics.com/frank-and-ernest
- Broom Hilda https://www.gocomics.com/broomhilda
- Brevity https://www.gocomics.com/brevity
- Cats cafe https://www.gocomics.com/cats-cafe
- Popeyes https://comicskingdom.com/popeye
- Artic Circle https://comicskingdom.com/arctic-circle
- Lockhorns https://gocomics.com/lockhorns
- Marvin https://comicskingdom.com/marvin
- Zits https://comicskingdom.com/zits
- Hi and Lois https://comicskingdom.com/hi-and-lois
- Carl https://www.webtoons.com/en/slice-of-life/carl/list?title_no=1216
- BlueChair https://www.webtoons.com/en/slice-of-life/bluechair/list?title_no=199
- Adventures of god https://www.webtoons.com/en/comedy/adventures-of-god/list?title_no=853
- Big Nate https://www.gocomics.com/bignate
- Get Fuzzy https://www.gocomics.com/getfuzzy
- Beetle Bailey https://comicskingdom.com/beetle-bailey-1
- The Boondocks https://www.gocomics.com/boondocks
- Pickles https://www.gocomics.com/pickles
- Pearls Before Swine https://www.gocomics.com/pearlsbeforeswine
- Chibird https://www.webtoons.com/en/challenge/chibird/list?title_no=97265
- War and Peas https://www.webtoons.com/en/challenge/war-and-peas/list?title_no=63305
- Humans are stupid https://www.webtoons.com/en/challenge/humans-are-stupid/list?title_no=54265
- Heathcliff https://www.gocomics.com/heathcliff
- Andy Capp https://www.gocomics.com/andycapp
- Ziggy https://www.gocomics.com/ziggy 
- Junk Drawer https://www.gocomics.com/junk-drawer
- Working Daze https://www.gocomics.com/working-daze
- Compu-Toon https://www.gocomics.com/compu-toon
- Pixie and Brutus https://www.webtoons.com/en/challenge/pixie-and-brutus/list?title_no=452175
- Sarah's Scribbles https://www.gocomics.com/sarahs-scribbles
- Speed Bump https://www.gocomics.com/speedbump
- Wallace the Brave https://www.gocomics.com/wallace-the-brave/characters
- Ripley's believe it or Not https://www.gocomics.com/ripleysbelieveitornot
- Baby Blues
- Outland
- Bloom County
- The Phantom
- Erma
- Cat Bird Dog

### Planned
- Nyazsche
- Saturday Morning Breakfast Cereal
- The Far Side

## Related GitHub pages: 
CalvinBot : https://github.com/wdr1/CalvinBot

Robobert: https://github.com/JTexpo/Robobert

## What to learn from this project?
- More about discord bots.
- Automated / Scheduled tasks.
- Looking for content in web pages.
- Parsing Date.
- Database support.
- GitHub version handling.

## Usage
- Get help about the bot
![Help embed](https://github.com/BBArikL/BDBot/blob/assets/help.png)

- Get a comic info
![Comic info](https://github.com/BBArikL/BDBot/blob/assets/comic-info.png)

- Get today's comic
![today's comic](https://github.com/BBArikL/BDBot/blob/assets/comic-demo-1.png)

- Get a random comic
![random comic](https://github.com/BBArikL/BDBot/blob/assets/comic-demo-2.png)

- Get a specific comic
![specific comic](https://github.com/BBArikL/BDBot/blob/assets/comic-demo-3.png)

- Subscribe to a comic
There are 2 ways to set up scheduled comics: 
  - Latest: Get only the latest comics when they are posted, no need to set up an exact day of the week or an hour of the day.
  - Regular: Get the comic at a regular day and hour of the week. A date should be one of the seven days of the week and the hour a number representing the time in a 24h clock in UTC time (0h to 23h). If not specified, defaults to the current time in UTC.

![comic subscription](https://github.com/BBArikL/BDBot/blob/assets/comic-demo-4.png)

## Current state of the project
- Functionalities
  - `/<comic_name>` Use comic <comic_name>
  - `/help general` : Help embed
  - `/git` command : Redirects to this GitHub page
  - `/invite` command : Generate a link to invite the bot to your server ([or use this link](https://discord.com/api/oauth2/authorize?client_id=807780409362481163&permissions=0&scope=bot))
  - Daily Command: use `/<name_of_comic> add/remove` to add or remove a comic from the daily list for the server.
  - Use `/remove_all` to remove all comics from the daily list for the server.
  - Use `/remove_channel` to remove all comics in the channel.
  - Tell me if I forgot some commands here!

- Bugs
  - Cyanide and Happiness specific date returns the latest comic
  - Cyanide and Happiness random comic returns the same comic
 
- Anything else to know?
  - How can I host the bot? The requirements are: Playwright (use 'BYPASS_GOCOMICS_JS=False' to disable that requirement), and python 3.11+.
    1. Install [Playwright](https://playwright.dev/)
    2. Install [pipx](https://pipx.pypa.io/latest/installation/)
    3. Install the bot: `pipx install git+https://github.com/BBArikL/BDBot/`
    4. Create a new bot here https://discord.com/developers/applications and save the credentials.
    5. Run `bdbot_manager` and select the options : 'Manage Bot' > 'Setup Bot'
    6. Go through the prompts.
    7. Run the bot with `bdbot`. If you are on Linux and have selected the service installation, make sure the bot is installed with : `systemctl status runbdbot`.
  - Why can't I go farther than 14 comics on Gocomics? As of April 1st 2025, Gocomics implemented a premium membership to view older comics. You can go on their site to get one and see the comics directly in your browser. Self-host the bot and define `BYPASS_GOCOMICS_SUBSCRIPTION=True` in your environment to view older comics. Distributing the comics for free could cause some undesirable consequences in the future. 
    - Gocomics also added some JS injection to prevent scraping and it seems to be put at random. This means that each gocomics page need to be fully rendered to reliably scrape it. This puts more stress on the host and more memory is used (I am sensing some memory leak with `requests-htmlc`). If you want to disable this, set `BYPASS_GOCOMICS_JS` to false in your .env file. 
  - Why is there only 2 images for Webtoons? Webtoons only gives out two images link to the comic in their rss feed. Finding each image link is way more complicated than this and is not in place now.
  - I requested a comic but it isn't there, why? I personally choose the requests to keep a balance of quality and diversity of comics. I still aim for the bot to be mostly "family-friendly". For some websites requested that could fit but are not here:
    - ComicRocket: It doesn't work for me strangely. And it seems to be just a linker back to other sites.
  - You want to do a pull request to add your favourite comic? 
    - Preferably, Gocomics and Comics Kingdom comics are the easiest to implement, so try to stick with that if your comic is hosted there. 
      - Please see [this README](bdbot/misc/ADD_COMIC.md) for complete instructions
  - If the comic is NOT hosted on GoComics/Comics Kingdom, please open an issue on the git page (https://github.com/BBArikL/BDBot). 
  - Any pull requests that was not approved from another site will be automatically rejected, and you will be asked to follow the procedure cited.
  - 'Beta' and 'main'?
    - The main branch is the current bot running on Discord.
    - Beta branch is for all experiments and additions waiting for approval to add to the current bot. This runs on a (for now) private bot upon completion of current goals.
    - More about branches: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-branches
  - The bot is considered complete feature-wise (but not comic-wise).
  - The bot is on UTC time. The daily comic post happen at 6:00 AM UTC daily.

## Privacy FAQ
- What information is collected by the bot?
  - If you only use the bot time to time: None!
  - If you subscribed to comics for your server:
    - The guild ID
    - The preferences about how to mention in the chat
    - The role ID to mention (if provided)
    - The subscribed channels ID
    - Information about which comics to send and when it needs to be sent
  - If you submitted a request (to prevent abuse and relevance):
    - Discord Username
    - Discord discriminator
    - Date and time of the request
    - The request
    - If you want to delete this information (and the associated requests), use `/delete_request`


