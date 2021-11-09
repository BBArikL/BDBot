import json


# Class that manage the comic details
class comDetails():
    comicDetails = None
    FILE_PATH = "./misc/comics_details.json"

    def __init__(self):
        self.comicDetails = comDetails.load_details()

    @staticmethod
    def load_details():
        print("Loading Details.....")
        # Returns the comic details
        # Loads the comic details file
        with open(comDetails.FILE_PATH, 'r', encoding='utf-8') as f:
            com_data = json.load(f)

        return com_data
