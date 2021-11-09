# Adding a comic

Hey fellow comic enjoyer! I see you venturing across this project and you look like you want to add a comic. Do not worry, I will show you!

Adding a comic is super easy. It does not even takes knowledge in code to do it! There is only 2 steps to make:
    
1. Let's start by searching for the comics and its information. You can find most of the information just by visiting the comic page. With your newly aquired knowledge     about the comic, you can start filing this form:
    ```
    "<The name of the comic>":{
        "Name": "<The name of the comic>",
        "Author": "The name of the author(s).",
        "Web_name": "<The way the name is written on the url>",
        "Main_website": "<The main website you are taking the comic from>",
        "Working_type": "<The way the image should be extracted from the website. For Gocomics and Comics Kingdom: date. If unsure, mark UNSURE>",
        "Description": "<A long description about the comic>",
        "Position": <Just add +1 to the last comic>,
        "First_date": "YEAR, MONTH, DAY",
        "Color": "<Hexadecimal code of the main color of the comic. If unsure, use this website: http://colormind.io/ to extract a color palette from a characteristic image of the comic.>",
        "Image": "<A url to the image which represents the comic>",
        "Aliases": "<The other ways of that the comic can be called>",
        "Helptxt": "<A very short description of the comic>"
    }
    ```
    When you are done, paste the new information in the [configuration file](comics_details.json) under the last comic information.
2. Add a new command in [Comics.py](../Scripts/Comics.py) with the name of the comic under the last command. Just change the aliases to the ones you specified in the config file and set the `comic_name` variable to the name of the first value. 
3. All done! Thank you for contributing to BDBot!
