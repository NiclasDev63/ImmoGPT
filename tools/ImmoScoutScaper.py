from bs4 import BeautifulSoup
import utils.get_coordinates as get_coordinates


class ImmoScoutScraper:
    """
    A class that searches ImmoScout for suitable properties

    Attributes:
        search_data (dict): Dict which contains the important information for the search

    """

    def __init__(self, search_data: dict):
        self.data = search_data

    def prompt():
        pass

    def scrapImmos(self):
        pass
    
    def format_coords(self) -> str:
        
        """Try to convert the desired location into the appropriate format for Immoscout"""

        if "location" in self.data:
            coords = get_coordinates.get_coordinates(self.data["location"])
            if coords != -1:

                radius = 1
                if "radius" in self.data and int(self.data["radius"]) > 1:
                    radius = self.data["radius"]

                return str(coords[0]) + ";" + str(coords[1]) + ";" + str(radius)
        else:
            print("Can't parse location from json")
            return -1
    