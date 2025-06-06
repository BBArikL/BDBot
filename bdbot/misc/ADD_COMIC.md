# Adding a comic

Hey fellow comic fan! I see you venturing across this project, and you look like you want to add a comic. Do not worry, I will show you!

Adding a comic is super easy. It does not even take knowledge in code to do it! There is only 2 steps to make:

Steps (you will need to clone the project: `git clone https://github.com/BBArikL/BDBot.git`):
1. Install the project with at least `InquirerPy` installed.
2. Run `python -m bdbot_manager`
3. Follow the steps to add a new comic
4. Create a pull request to merge the changes.
5. That's it!

Manual steps (without cloning the repo, to do on the web UI):
1. Let's start by searching for the comics and its information. You can find most of the information just by visiting the comic page. With your newly acquired knowledge about the comic, you can start filing this form:
    ```
    "<The name of the comic>":{
        "name": "<The name of the comic>",
        "author": "The name of the author(s).",
        "web_name": "<The way the name is written on the url>",
        "main_website": "<The main website you are taking the comic from>",
        "working_type": "<The way the image should be extracted from the website. For Gocomics and Comics Kingdom: date. If unsure, mark UNSURE>",
        "description": "<A long description about the comic>",
        "position": <Just add +1 to the last comic>,
        "first_date": "YEAR, MONTH, DAY",
        "color": "<Hexadecimal code of the main color of the comic. If unsure, use this website: http://colormind.io/ to extract a color palette from a characteristic image of the comic.>",
        "image": "<A url to the image which represents the comic>",
        "help": "<A very short description of the comic>"
    }
    ```
    When you are done, paste the new information in the [configuration file](comics_details.json) under the last comic information.
2. All done! Thank you for contributing to BDBot!
