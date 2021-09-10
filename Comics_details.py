import json


class comDetails():
    comicDetails = None

    def __init__(self):
        self.comicDetails = comDetails.load_details()

    @staticmethod
    def load_details():
        print("Loading Details.....")
        # Returns the comic details
        FILE_PATH = "./misc/comics_details.json"

        # Loads the comic details file
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            comData = json.load(f)

        return comData

    """@commands.command()
    async def reload(self):  # reloads the comic details
        comDetails.comicDetails = comDetails.load_details(self)"""
