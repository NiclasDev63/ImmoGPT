from bs4 import BeautifulSoup
import utils.get_coordinates as get_coordinates
import utils.get_random_agent as random_agent


class ImmoScoutScraper:
    """
    A class that searches ImmoScout for suitable properties

    Attributes:
        search_data (dict): Dict which contains the important information for the search

    """

    def __init__(self, search_data: dict):
        self.data = search_data

        """
        This cookie needs to be set to scrap ImmoScout24.
        Unfortunately it is only a temporary cookie and must be renewed every few requests
        """
        self.reese84 = {
            "reese84": "3:XdU2wJUEKW15haSwlllSNQ==:Fm67AiqbVtzzW2iJ9w38jiaRyr9SDFqbpCwRF9FKcAszSN9yr4oxjYggbqvozyWUF6c9rPCCyazUm8LARJ9sj6cpOLZYg8TPyJ97w32Kolswt1+XE9Ucj2/rMiB0yvxDBYZ/TSnP2BRslfsw2F10LBpvSEiIe1U56QMik2DQrMpjOxL7n7LWZsYWPr4wrm9bFrCb3/ffOsbL7b29D/yCb3vOhlX3xIMfftvquxE/XAZjBzQCNH+C83pa5vhhrZCFxDsJBLStcCK0bOCrIzHk+qW9MxrI3pE9MgK2Zai6eWoJ/VFc8QPU6bWsL1zXkXBPUNKMzRJM3kfzWx4ZOo5hLAs8BLx9PwLJTFnY7PdX4JSMiugFTOEXxya7HAEA8NmBl2Qa9wV6raT8IBCrZjKlL/ErtMDuS23PxZxJAzDVhqeEZVtBdvC86Ayxw9drqFe5kgvt+W8dxsjKtaPQ6pA8HmEq0uf+ckBN+8gA6/Mnsesikfc8TXtyCTHuxnEaJRxi:CLiIko6ehmKNPwgdci8k1ptlJpAiv2QLdmPX0eeSblM="
        }

        self.base_url = "https://www.immobilienscout24.de/Suche/radius/"


    def prompt():
        pass


    def scrapImmos(self):
        """Searches for properties with the desired parameters"""

        price_url = self._extract_price()
        coord_url = self._extract_coords()

        if price_url != -1 and coord_url != -1:
            url = self.base_url + price_url + self._extract_squaremeters() + coord_url
            print(url)

        else:
            print("Can't create URL for request")



    def _extract_squaremeters(self) -> str:

        """Converts the wanted squaremeters into url format"""

        url = "livingspace="

        if "minLivingSpace" in self.data:
            url += str(self.data["minLivingSpace"])
        if "maxLivingSpace" in self.data:
            url += "-" + str(self.data["maxLivingSpace"])

        url += "&"

        if url.endswith("livingspace=&"): return ""
        else: return url

    def _extract_price(self) -> str:
        
        """Converts the wanted price into url format"""

        url = ""

        if "type" not in self.data: 
            print("Can't parser location from json")
            return -1
        
        elif self.data["type"] == "rent": url += "wohnung-mieten?"
        else: url += "wohnung-kaufen?"

        url += "price="

        if "minPrice" in self.data:
            url += str(self.data["minPrice"])

        if "maxPrice" in self.data:
            url += "-" + str(self.data["maxPrice"])
        
        url += "&"

        if url.endswith("price=&"): url = url.replace("price=&", "")
        
        return url

    
    def _extract_coords(self) -> str:
        
        """Converts the desired location into url format"""

        if "location" in self.data:
            coords = get_coordinates.get_coordinates(self.data["location"])
            if coords != -1:

                radius = 1
                if "radius" in self.data and int(self.data["radius"]) > 1:
                    radius = self.data["radius"]

                return "geocoordinates=" + str(coords[0]) + ";" + str(coords[1]) + ";" + str(radius)
            else: return -1
        else:
            print("Can't parse location from json")
            return -1
    